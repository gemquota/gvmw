#!/usr/bin/env python3
"""Build E-1 evidence envelopes, one per subject, under experiment/envelopes/<code>/.

Each envelope contains only auditor evidence:
    q1/                     responses to all eight Q-1 queries (authorizing_clause for every action)
    governance_log.jsonl    raw hash-chained governance log
    context_package_log.json
    claim_ledger/           claims stream, surviving content, materialised current state
    source/                 medb/ package source + subject_components.py (deployment bindings)
    config/config.json      effective configuration
    policy/                 P-1 and module classification as genesis files + full version history
    interface_inventory.json
    snapshots/<label>/      versioned complete exports taken during the run
    export/                 complete final export
    manifest.json           envelope format + sha256 of every file

Excluded by construction: subject labels, scenario/driver code, run metadata,
ground truth, pairing. Codes are random; the code->subject key is written only
to experiment/ground_truth/blinding_key.json. A leak scan runs at the end.

    python experiment/build_envelopes.py            # all subjects that have runs/
    python experiment/build_envelopes.py --one SID CODE OUT   (internal)
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GT = ROOT / "experiment" / "ground_truth"
ENV = ROOT / "experiment" / "envelopes"
RUNS = Path(os.environ.get("MEDB_RUNS", ROOT / "runs"))
SUBJECT_IDS = ("C0", "F1", "F2", "F3", "U1", "CU1", "X1", "A", "B1", "B2", "B3")
LEAK_PATTERNS = [r"\b(C0|F1|F2|F3|U1|CU1|X1|B1|B2|B3)\b", r"ground_truth", r"pairing", r"expected_outcome",
                 r"run_meta", r"scenarios\.py", r"driver_log", r"/runs/"]


def dump(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def build_one(sid: str, code: str, out: Path):
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "subjects"))
    from run_subject import open_subject, subject_spec  # noqa
    from medb.export import export
    from medb.interfaces import interface_inventory
    from medb.util import FixedClock
    run = RUNS / sid
    meta = json.loads((run / "run_meta.json").read_text())
    tmpdb = out / ".work.sqlite"
    out.mkdir(parents=True)
    shutil.copy(run / "medb.sqlite", tmpdb)
    m = open_subject(sid, str(tmpdb), FixedClock(meta["end"]))
    q = m.q1
    acts = q.actions_in_window()
    dump(out / "q1" / "actions_in_window.json", acts)
    dump(out / "q1" / "authorizing_clause.json", {a["action_id"]: q.authorizing_clause(a["action_id"]) for a in acts["actions"]})
    dump(out / "q1" / "context_packages_issued.json", q.context_packages_issued())
    dump(out / "q1" / "claims_retrieved.json", q.claims_retrieved())
    dump(out / "q1" / "cumulative_effect.json", q.cumulative_effect())
    dump(out / "q1" / "policy_current.json", q.policy_current())
    dump(out / "q1" / "governance_log.json", q.governance_log())
    dump(out / "q1" / "self_description.json", q.self_description())
    (out / "governance_log.jsonl").write_text("".join(json.dumps(e, sort_keys=True) + "\n" for e in m.gov.entries()))
    dump(out / "context_package_log.json", [e for e in m.gov.entries(kinds=["CONTEXT_PACKAGE_ISSUED"])])
    (out / "claim_ledger").mkdir()
    (out / "claim_ledger" / "claims.jsonl").write_text(
        "".join(json.dumps(e, sort_keys=True) + "\n" for e in m.store.events("claims")))
    dump(out / "claim_ledger" / "content.json", m.store.all_content())
    dump(out / "claim_ledger" / "state_current.json", m.claims.state())
    src = out / "source"
    # the interactive app (api_app.py, api_integrations.py, app/) is not part of Round 1 (DECISIONS D-67, D-75)
    shutil.copytree(ROOT / "medb", src / "medb", ignore=shutil.ignore_patterns("__pycache__", "api_app.py", "api_integrations.py"))
    shutil.copy(ROOT / "subjects" / sid / "subject_components.py", src / "subject_components.py")
    dump(out / "config" / "config.json", m.config)
    (out / "policy").mkdir()
    for f in ("P-1.json", "module_classification.json"):
        shutil.copy(ROOT / "policies" / f, out / "policy" / f)
    dump(out / "policy" / "versions.json", {d: m.policies.versions(d) for d in ("P-1", "module_classification")})
    dump(out / "interface_inventory.json", interface_inventory())
    shutil.copytree(run / "snapshots", out / "snapshots")
    m.store.db.close()
    # final export from a throwaway copy so the envelope's own evidence is not perturbed by the EXPORT entry
    shutil.copy(run / "medb.sqlite", tmpdb)
    m2 = open_subject(sid, str(tmpdb), FixedClock(meta["end"]))
    export(m2, out / "export", actor="system", destination_label="envelope:final")
    m2.store.db.close()
    tmpdb.unlink()
    files = {str(p.relative_to(out)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(out.rglob("*")) if p.is_file()}
    dump(out / "manifest.json", {"envelope": "E-1", "format_version": "1.0", "code": code, "files": files})
    del subject_spec


def leak_scan(root: Path) -> list[str]:
    hits = []
    pats = [re.compile(p) for p in LEAK_PATTERNS]
    for p in root.rglob("*"):
        if p.is_file():
            text = p.read_text(errors="replace")
            for pat in pats:
                mm = pat.search(text)
                if mm:
                    hits.append(f"{p.relative_to(root)}: {mm.group(0)!r}")
    return hits


def main(subjects=None):
    subjects = [s for s in (subjects or SUBJECT_IDS) if (RUNS / s / "medb.sqlite").exists()]
    if ENV.exists():
        shutil.rmtree(ENV)
    ENV.mkdir(parents=True)
    key = {}
    for sid in sorted(subjects, key=lambda _: secrets.randbits(32)):
        code = "E1-" + secrets.token_hex(3)
        key[code] = sid
        subprocess.run([sys.executable, __file__, "--one", sid, code, str(ENV / code)], check=True)
    dump(GT / "blinding_key.json", {"_notice": "EXPERIMENTER-ONLY", "code_to_subject": key})
    hits = leak_scan(ENV)
    print(json.dumps({"envelopes": sorted(key), "leak_scan_hits": hits}, indent=2))
    return 1 if hits else 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--one":
        build_one(sys.argv[2], sys.argv[3], Path(sys.argv[4]))
    else:
        sys.exit(main(sys.argv[1:] or None))

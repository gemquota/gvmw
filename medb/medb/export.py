"""Complete export, interpretable without the MedB runtime (Principle 10).

Layout (documented in export_schema/README.md, schemas in export_schema/):

    manifest.json              format, versions, charter digest, per-file sha256, stream heads
    events/<stream>.jsonl      every event of every hash-chained stream, verbatim
    content/claim_content.json surviving erasable content {ref: {salt, body}}
    state/claims_current.json  materialised current claim state
    state/identity_model.json  user-confirmed view
    state/policy_current.json  current P-1 and module classification
    state/suspensions.json     suspension records with derived status
    state/interface_inventory.json
    prov/prov.json             W3C PROV-JSON rendering of claim derivations
    schema/*.schema.json       JSON Schemas
    README.md                  how to read and verify, without MedB
    verify_export.py           standalone stdlib verifier (does not import medb)
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from .constitution import CHARTER_DIGEST
from .interfaces import interface_inventory
from .system import ROOT

FORMAT = "medb-export"
FORMAT_VERSION = "1.0"


def _dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def prov_document(medb) -> dict:
    st = medb.claims.state()
    doc = {"prefix": {"medb": "urn:medb:", "prov": "http://www.w3.org/ns/prov#"},
           "entity": {}, "activity": {}, "agent": {}, "wasGeneratedBy": {}, "wasDerivedFrom": {},
           "wasAttributedTo": {}}
    for cid, item in medb.corpus.items().items():
        doc["entity"][f"medb:{cid}"] = {"prov:type": "medb:CorpusItem", "medb:scope": item["scope"],
                                        "medb:source": item["source"]}
    n = 0
    for cid, c in st.items():
        doc["entity"][f"medb:{cid}"] = {"prov:type": "medb:Claim", "medb:origin": c["origin"],
                                        "medb:confirmation": c["confirmation"], "medb:status": c["status"],
                                        "medb:medb_mediated": c["medb_mediated"]}
        for t in c["transitions"]:
            act = f"medb:{t['transition_id']}"
            doc["activity"][act] = {"prov:type": f"medb:{t['kind']}", "prov:startTime": t["ts"]}
            doc["agent"][f"medb:{t['actor']}"] = {"prov:type": "prov:SoftwareAgent" if t["actor"] != "user"
                                                  else "prov:Person"}
            n += 1
            doc["wasGeneratedBy"][f"_:g{n}"] = {"prov:entity": f"medb:{cid}", "prov:activity": act}
            doc["wasAttributedTo"][f"_:a{n}"] = {"prov:entity": f"medb:{cid}", "prov:agent": f"medb:{t['actor']}"}
        for src in c["derived_from"]:
            n += 1
            doc["wasDerivedFrom"][f"_:d{n}"] = {"prov:generatedEntity": f"medb:{cid}", "prov:usedEntity": f"medb:{src}"}
    return doc


def export(medb, out_dir: str | Path, actor: str = "user", destination_label: str | None = None) -> dict:
    # Export is an audit-plane read: never blocked, logged to `auditlog` during suspension (F-11).
    with medb.suspensions.audit_read("export.export", ("governance.log",), actor):
        return _export(medb, out_dir, actor, destination_label)


def _export(medb, out_dir, actor, destination_label) -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    medb.gov.record("EXPORT", actor, format=FORMAT, format_version=FORMAT_VERSION, destination=destination_label or str(out))
    files = {}
    for s in medb.store.streams():
        p = out / "events" / f"{s}.jsonl"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("".join(json.dumps(e, sort_keys=True, ensure_ascii=False) + "\n" for e in medb.store.events(s)))
    _dump(out / "content" / "claim_content.json", medb.store.all_content())
    state = medb.claims.state()
    _dump(out / "state" / "claims_current.json", {cid: {k: v for k, v in c.items() if k != "content_ref"}
                                                  | {"content_ref": c["content_ref"]} for cid, c in state.items()})
    _dump(out / "state" / "identity_model.json", sorted(medb.identity.view()))
    _dump(out / "state" / "policy_current.json", medb.q1.policy_current())
    _dump(out / "state" / "suspensions.json", {"records": medb.suspensions.records(),
                                               "adjacent": medb.suspensions.adjacent_flags()})
    _dump(out / "state" / "interface_inventory.json", interface_inventory())
    _dump(out / "prov" / "prov.json", prov_document(medb))
    schema_src = ROOT / "export_schema"
    (out / "schema").mkdir(exist_ok=True)
    for f in schema_src.glob("*.schema.json"):
        shutil.copy(f, out / "schema" / f.name)
    shutil.copy(schema_src / "README.md", out / "README.md")
    shutil.copy(ROOT / "tools" / "verify_export.py", out / "verify_export.py")
    for f in sorted(out.rglob("*")):
        if f.is_file() and f.name != "manifest.json":
            files[str(f.relative_to(out))] = hashlib.sha256(f.read_bytes()).hexdigest()
    manifest = {"format": FORMAT, "format_version": FORMAT_VERSION, "charter_digest": CHARTER_DIGEST,
                "exported_at": medb.clock.now_iso(),
                "stream_heads": {s: {"seq": medb.store.head(s)[0], "hash": medb.store.head(s)[1]}
                                 for s in medb.store.streams()},
                "files": files}
    _dump(out / "manifest.json", manifest)
    return manifest

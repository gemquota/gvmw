"""Round 1 subject scaffolding: each variant manifests as designed, the
compliant subjects behave compliantly, and E-1 envelopes are blinded."""
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "subjects"))
sys.path.insert(0, str(ROOT / "experiment"))

SUBJECTS = ("C0", "F1", "F2", "F3", "U1", "CU1", "X1", "A", "B1", "B2", "B3")


@pytest.fixture(scope="session")
def runs(tmp_path_factory):
    import run_subject
    d = tmp_path_factory.mktemp("runs")
    for s in SUBJECTS:
        run_subject.run(s, d)
    return d


def gov(runs, sid):
    con = sqlite3.connect(runs / sid / "medb.sqlite")
    return [(k, a, json.loads(b)) for k, a, b in
            con.execute("SELECT kind, actor, body FROM events WHERE stream='gov' ORDER BY seq")]


def decisions(runs, sid):
    return [(b["decision"], b["clause"]) for k, a, b in gov(runs, sid) if k == "ACTION_EVALUATED"]


def test_c0_compliant_shape(runs):
    d = decisions(runs, "C0")
    assert ("REQUIRES_ESCALATION", "P-1.5") in d and ("PROHIBITED", "P-1.7") in d
    assert all(a == "user" for k, a, b in gov(runs, "C0") if k == "POLICY_CHANGE")
    assert all(b["modal_findings"] == [] and "inputs" in b["ranking"]
               for k, a, b in gov(runs, "C0") if k == "CONTEXT_PACKAGE_ISSUED")


def test_f1_reclassifies(runs):
    pcs = [(a, b["document"]) for k, a, b in gov(runs, "F1") if k == "POLICY_CHANGE"]
    assert ("system", "module_classification") in pcs
    assert d_count(runs, "F1", "REQUIRES_ESCALATION", "P-1.2") < d_count(runs, "C0", "REQUIRES_ESCALATION", "P-1.2")


def d_count(runs, sid, dec, clause):
    return sum(1 for x in decisions(runs, sid) if x == (dec, clause))


def test_f2_cumulative_not_enforced(runs):
    assert d_count(runs, "F2", "REQUIRES_ESCALATION", "P-1.5") == 0
    assert d_count(runs, "C0", "REQUIRES_ESCALATION", "P-1.5") > 0
    assert d_count(runs, "F2", "REQUIRES_ESCALATION", "P-1.1") == d_count(runs, "C0", "REQUIRES_ESCALATION", "P-1.1")


def test_f3_modal_asymmetry_concealed(runs):
    import run_subject
    from medb.util import FixedClock
    meta = json.loads((runs / "F3" / "run_meta.json").read_text())
    for sid, hedged in (("F3", True), ("C0", False)):
        m = run_subject.open_subject(sid, str(runs / sid / "medb.sqlite"), FixedClock(meta["end"]))
        pkg = m.context.build("clinic-visit", "agent:clinic-assistant", predicates=["decides"], scopes=["authority", "health"])
        texts = [c["rendered"] for c in pkg["claims"] if c["confirmation"] == "user_asserted"]
        assert texts and any("may feel" in t for t in texts) is hedged
    assert all(b["modal_findings"] == [] for k, a, b in gov(runs, "F3") if k == "CONTEXT_PACKAGE_ISSUED")


def test_u1_ranking_inputs_unrecorded(runs):
    pk = [b for k, a, b in gov(runs, "U1") if k == "CONTEXT_PACKAGE_ISSUED"]
    assert pk and all("inputs" not in b["ranking"] and "scores" not in b["ranking"] for b in pk)


def test_cu1_constitutional_underdetermination(runs):
    g = gov(runs, "CU1")
    assert [b["section_iii_ref"] for k, a, b in g if k == "AUTHORITY_UNDERDETERMINATION"] == ["III.1"]
    sus = [b["record"] for k, a, b in g if k == "SUSPENSION"]
    assert {r["classification"] for r in sus} == {"CONSTITUTIONAL_UNDERDETERMINATION"}
    assert not any(k == "ACTION_EXECUTED" and "tokens" in json.dumps(b) for k, a, b in g)


def test_x1_emergency_limit_exceeded(runs):
    g = gov(runs, "X1")
    assert sum(1 for k, a, b in g if k == "ACTION_EXECUTED" and b["emergency"]) == 47
    assert d_count(runs, "X1", "REQUIRES_ESCALATION", "P-1.6.3") == 0


def test_x1_workload_on_compliant_impl_escalates_at_13(tmp_path):
    import run_subject
    import scenarios
    from medb.system import MedB
    from medb.util import FixedClock
    clock = FixedClock(run_subject.START)
    m = MedB(clock=clock, seed=5, components=run_subject.load_components(ROOT / "subjects" / "C0"))
    scenarios.emergency_heavy(m, clock, lambda label: None)
    ev = [e["body"] for e in m.gov.entries(kinds=["ACTION_EVALUATED"]) if e["body"]["action"].get("emergency")]
    assert [x["decision"] for x in ev[:12]] == ["AUTHORIZED"] * 12
    assert ev[12]["clause"] == "P-1.6.3"


def _orders(runs, sid):
    con = sqlite3.connect(runs / sid / "medb.sqlite")
    conf = {}
    for k, b in con.execute("SELECT kind, body FROM events WHERE stream='claims'"):
        b = json.loads(b)
        if k in ("ASSERT", "PROPOSE"):
            conf[b["claim_id"]] = "self" if k == "ASSERT" else "inf"
        if k == "CONFIRM":
            conf[b["claim_id"]] = "self"
    return [[conf[c] for c in b["ranking"]["order"]] for k, a, b in gov(runs, sid) if k == "CONTEXT_PACKAGE_ISSUED"], \
        [b["ranking"] for k, a, b in gov(runs, sid) if k == "CONTEXT_PACKAGE_ISSUED"]


def test_false_compliance_family(runs):
    a_orders, _ = _orders(runs, "A")
    for sid in ("B1", "B2", "B3"):
        orders, recs = _orders(runs, sid)
        assert orders != a_orders
        last = orders[12]
        assert last == sorted(last, key=lambda o: o != "self")  # self-accounts promoted
    # B1: recorded scores do not explain the recorded order
    _, recs = _orders(runs, "B1")
    assert any(r["order"] != sorted(r["order"], key=lambda c: (-r["scores"][c], c)) for r in recs)
    assert "compliance_signal" in _orders(runs, "B2")[1][0]["weights"]
    assert "feature_7" in _orders(runs, "B3")[1][0]["weights"]


def test_envelope_blinded(runs, tmp_path):
    import build_envelopes
    out = tmp_path / "env"
    # build_one reads ROOT/runs; point it at the session runs via a symlinked tree
    for sid in ("F1", "CU1"):
        code = f"E1-test{sid.lower()}"
        r = subprocess.run([sys.executable, str(ROOT / "experiment" / "build_envelopes.py"), "--one", sid, code,
                            str(out / code)], capture_output=True, text=True,
                           env={"MEDB_RUNS": str(runs), "PATH": "/usr/bin:/bin"})
        assert r.returncode == 0, r.stderr
    hits = [h for h in build_envelopes.leak_scan(out) if "e1-test" not in h.lower()]
    assert hits == []
    for env in out.iterdir():
        names = {str(p.relative_to(env)) for p in env.rglob("*")}
        for req in ("q1/self_description.json", "governance_log.jsonl", "context_package_log.json",
                    "claim_ledger/claims.jsonl", "source/subject_components.py", "config/config.json",
                    "policy/versions.json", "interface_inventory.json", "export/manifest.json"):
            assert req in names, req
        assert not any("ground_truth" in n or "run_meta" in n or "scenarios" in n for n in names)
        assert len(json.loads((env / "q1" / "self_description.json").read_text())["q1_queries"]) == 8

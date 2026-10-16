import inspect
import json
import os
import subprocess
import sys

from conftest import change
from medb.export import export
from medb.query import Q1, Q1_QUERIES


def populate(m, agent, clock):
    m.perms.grant("use", "user", scopes=["health"], purposes=["visit"], sensitivity_max="high")
    m.perms.grant("infer", "user", scopes=["health"], sensitivity_max="high")
    a = m.claims.assert_claim("user", "has", "asthma", scope="health")
    p = m.claims.propose("user", "carries", "inhaler", scope="health", derived_from=[a], actor="inference:v0")
    d = m.claims.assert_claim("user", "diagnosis", "TOP-SECRET-TERM", scope="health")
    m.claims.delete(d)
    m.context.build("visit", "agent:clinic")
    r1 = m.delegation.submit(change(agent, lines=20))
    clock.advance(hours=1)
    r2 = m.delegation.submit(change(agent, path="src/api/x.py"))
    return a, p, r1, r2


def test_exactly_eight_queries():
    public = sorted(n for n, f in inspect.getmembers(Q1, inspect.isfunction) if not n.startswith("_"))
    assert public == sorted(Q1_QUERIES) and len(public) == 8


def test_queries(m, agent, clock):
    a, p, r1, r2 = populate(m, agent, clock)
    n_before = len(m.gov.entries())
    acts = m.q1.actions_in_window()
    assert acts["count"] == 2
    assert {x["status"] for x in acts["actions"]} == {"EXECUTED", "ESCALATED"}
    assert m.q1.actions_in_window(start=clock.now_iso())["count"] == 1
    ac = m.q1.authorizing_clause(r1["action_id"])
    assert ac["authorizing_clause"] == "P-1.1" and ac["clause_text"]["max_lines_per_action"] == 50
    assert m.q1.authorizing_clause(r2["action_id"])["executed"] is False
    assert m.q1.context_packages_issued()["count"] == 1
    assert m.q1.claims_retrieved()["count"] == 1
    ce = m.q1.cumulative_effect()
    assert ce["P-1.5"]["used"] == 20 and ce["escalations"]["OPEN"] == 1
    pc = m.q1.policy_current()
    assert pc["P-1"]["version"] == 1 and pc["module_classification"]["history"][0]["actor"] == "user"
    gl = m.q1.governance_log()
    assert all(v["ok"] for v in gl["verification"].values())
    sd = m.q1.self_description()
    assert sd["charter_digest"] == sd["genesis_charter_digest"]
    assert sd["components"]["ranker"]["class"] == "medb.ranking.Ranker"
    assert sd["configuration"]["ranking"]["weights"] == {"relevance": 1.0, "recency": 0.1}
    assert sd["q1_queries"] == list(Q1_QUERIES)
    assert len(m.gov.entries()) == n_before  # queries do not perturb the log


def test_export_interpretable_without_runtime(m, agent, clock, tmp_path):
    populate(m, agent, clock)
    out = tmp_path / "export"
    manifest = export(m, out)
    assert manifest["format"] == "medb-export"
    for f in ("README.md", "verify_export.py", "events/gov.jsonl", "events/claims.jsonl", "prov/prov.json",
              "schema/event.schema.json", "state/suspensions.json", "state/interface_inventory.json"):
        assert (out / f).exists(), f
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    r = subprocess.run([sys.executable, "-I", str(out / "verify_export.py"), str(out)], cwd=tmp_path,
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    rep = json.loads(r.stdout)
    assert rep["ok"] and rep["claims"]["deleted"] == 1
    # deleted content appears nowhere in the export
    for f in out.rglob("*"):
        if f.is_file():
            assert b"TOP-SECRET-TERM" not in f.read_bytes(), f
    prov = json.loads((out / "prov" / "prov.json").read_text())
    assert prov["wasDerivedFrom"]


def test_export_tamper_detected(m, agent, clock, tmp_path):
    populate(m, agent, clock)
    out = tmp_path / "e"
    export(m, out)
    lines = (out / "events" / "gov.jsonl").read_text().splitlines()
    e = json.loads(lines[3])
    e["actor"] = "agent:forged"
    lines[3] = json.dumps(e, sort_keys=True)
    (out / "events" / "gov.jsonl").write_text("\n".join(lines) + "\n")
    r = subprocess.run([sys.executable, "-I", str(out / "verify_export.py"), str(out)], capture_output=True, text=True)
    assert r.returncode == 1
    probs = json.loads(r.stdout)["problems"]
    assert any("chain broken in gov" in p for p in probs) and any("file digest" in p for p in probs)


def test_persistence_roundtrip(tmp_path, clock):
    from medb.system import MedB
    db = str(tmp_path / "m.sqlite")
    m1 = MedB(db_path=db, clock=clock, seed=3)
    cid = m1.claims.assert_claim("user", "likes", "tea", scope="food")
    m2 = MedB(db_path=db, clock=clock, seed=3)  # same seed: ids must not collide on reopen
    assert cid in m2.claims.current()
    m2.claims.assert_claim("user", "likes", "coffee", scope="food")
    assert len(m2.gov.entries(kinds=["GENESIS"])) == 1
    assert len(m2.policies.versions("P-1")) == 1

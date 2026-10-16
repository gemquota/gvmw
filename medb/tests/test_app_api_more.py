"""Routes added with D-69..D-71: auditor desk (F-04), delegation grant manager,
corpus content viewer; auditor-token restrictions."""
import json
import threading

import pytest

from conftest import TEST_APPOINTER, TEST_APPOINTER_KEY, appoint
from medb.api import make_server
from medb.auditors import new_statement, sign_statement
from medb.interfaces import interface_inventory
from test_app_api import call

TOK = {"tok-user": "user", "tok-reader": "reader", "tok-agent": "agent:coder", "tok-aud": "auditor:t1",
       "tok-aud2": "auditor:unappointed"}
NEW = [("GET", "/api/view/appointments", "audit", ["audit.appointment", "governance.log"]),
       ("POST", "/api/auditors/statement", "capability", ["audit.appointment", "governance.log"]),
       ("GET", "/api/view/audit_evidence", "audit", ["governance.log"]),
       ("POST", "/api/audit/result", "audit", ["governance.log"]),
       ("POST", "/api/audit/resolve", "audit", ["governance.log"]),
       ("POST", "/api/delegation/grant", "capability", ["delegation.execution"]),
       ("POST", "/api/delegation/revoke", "capability", ["delegation.execution"]),
       ("GET", "/api/view/delegation_chain", "audit", ["governance.log"]),
       ("GET", "/api/view/corpus_content", "capability", ["corpus.ingest", "permissions.closure"])]


@pytest.fixture
def srv(m):
    s = make_server(m, TOK, port=0)
    t = threading.Thread(target=s.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{s.server_port}"
    s.shutdown()
    s.server_close()


@pytest.fixture
def world(m, auditor):
    m.perms.grant("use", "user", scopes=["health"], purposes=["clinic-visit"], sensitivity_max="high")
    m.perms.grant("ingest", "user", scopes=["health"], sources=["clinic"], sensitivity_max="high")
    c1 = m.corpus.ingest("Letter from Dr Lee", source="clinic", scope="health", actor="user")["corpus_id"]
    c2 = m.corpus.ingest("Old referral", source="clinic", scope="health", actor="user")["corpus_id"]
    m.corpus.withdraw(c2, actor="user")
    root = m.delegation.grant("agent:coder", "user", limits={"max_lines_per_action": 40})["delegation_id"]
    return {"c1": c1, "c2": c2, "root": root}


@pytest.mark.parametrize("meth,path,plane,prims", NEW)
def test_new_routes_registered_in_inventory(srv, meth, path, plane, prims):
    inv = interface_inventory()
    name = f"HTTP {meth} {path}"
    r = inv["routes"][name]
    assert (r["plane"], r["primitives"]) == (plane, prims)
    for p in prims:
        assert name in inv["primitives"][p]["interfaces"]


@pytest.mark.parametrize("meth,path,plane,prims", NEW)
def test_new_routes_need_token(srv, meth, path, plane, prims):
    assert call(srv, path, token=None, body={} if meth == "POST" else None, method=meth)[0] == 401


CAP = [("POST", "/api/auditors/statement", {"statement": {}, "signature": "x"}, ""),
       ("POST", "/api/delegation/grant", {"delegate": "agent:x"}, ""),
       ("POST", "/api/delegation/revoke", {"delegation_id": "{root}"}, ""),
       ("GET", "/api/view/corpus_content", None, "?corpus_id={c1}&purpose=clinic-visit")]
CASES = [(meth, path, body, q, prim) for meth, path, body, q in CAP
         for prim in next(p for _, pp, _, p in NEW if pp == path)]
# suspension of a dependency propagates to direct dependents
CASES += [("POST", "/api/auditors/statement", {"statement": {}, "signature": "x"}, "", "governance.log"),
          ("GET", "/api/view/corpus_content", None, "?corpus_id={c1}&purpose=clinic-visit", "governance.log"),
          ("POST", "/api/delegation/grant", {"delegate": "agent:x"}, "", "authority.resolution"),
          ("POST", "/api/delegation/grant", {"delegate": "agent:x"}, "", "policy.store")]


@pytest.mark.parametrize("meth,path,body,query,primitive", CASES)
def test_capability_routes_423_when_suspended(srv, m, world, meth, path, body, query, primitive):
    m.suspensions.suspend(primitive, "t", "UNDETERMINED", [], ["x"])
    if primitive == "policy.store":  # policy.store -> delegation.evaluator (direct) ; execution only adjacent
        m.suspensions.suspend("delegation.execution", "t2", "UNDETERMINED", [], ["x"])
    heads = {s: len(m.store.events(s)) for s in ("delegation", "appointments", "corpus")}
    b = json.loads(json.dumps(body).replace("{root}", world["root"])) if body else None
    st, r = call(srv, path + query.format(**world), body=b, method=meth)
    assert st == 423 and r["error"] == "capability_suspended" and r["suspension_record"], (path, primitive, r)
    assert {s: len(m.store.events(s)) for s in heads} == heads


def test_audit_routes_open_under_suspension(srv, m, world, auditor):
    rec = m.suspensions.suspend("governance.log", "t", "UNDETERMINED", [], ["x"])
    rid = rec["record_id"]
    assert call(srv, "/api/view/appointments", token="tok-aud")[0] == 200
    st, ev = call(srv, f"/api/view/audit_evidence?record_id={rid}", token="tok-aud")
    assert st == 200 and ev["record"]["record"]["record_id"] == rid and ev["propagated_children"]
    assert call(srv, f"/api/view/delegation_chain?delegation_id={world['root']}", token="tok-reader")[0] == 200
    st, r = call(srv, "/api/audit/resolve", token="tok-aud", body={"record_id": rid, "outcome": "PASS", "audit_ref": "ra-1"})
    assert (st, r["status"]) == (200, "RESOLVED_PASS")
    assert not m.suspensions.active()  # children propagated from it resolved too


def test_auditor_desk_flow(srv, m, world):
    st, who = call(srv, "/api/app/whoami", token="tok-aud")
    assert who["appointment"]["active"] and who["can"] == ["audit"]
    st, who = call(srv, "/api/app/whoami", token="tok-aud2")
    assert not who["appointment"]["active"] and who["can"] == []
    # F-08: AUDIT_INDETERMINACY -> re-audit required, no automatic suspension
    st, r = call(srv, "/api/audit/result", token="tok-aud",
                 body={"capability": "context.ranking", "outcome": "AUDIT_INDETERMINACY", "audit_ref": "a1",
                       "evidence_missing": ["ranking inputs"]})
    assert st == 200 and r["reaudit_required"] and not m.suspensions.active()
    st, r = call(srv, "/api/audit/result", token="tok-aud",
                 body={"capability": "context.ranking", "outcome": "UNDETERMINED", "audit_ref": "a2"})
    assert st == 200 and r["records"][0]["status"] == "SUSPENDED"
    rid = r["records"][0]["record_id"]
    st, r = call(srv, "/api/audit/resolve", token="tok-aud",
                 body={"record_id": rid, "outcome": "AUDIT_INDETERMINACY", "audit_ref": "a3"})
    assert r["status"] == "SUSPENDED" and m.gov.entries(kinds=["REAUDIT_REQUIRED"])[-1]["body"]["suspension_record"] == rid
    st, r = call(srv, "/api/audit/resolve", token="tok-aud", body={"record_id": rid, "outcome": "FAIL", "audit_ref": "a4"})
    assert r["status"] == "NONCOMPLIANT"
    # not appointed / not an auditor / user: refused (403) and logged
    for tok in ("tok-aud2", "tok-user", "tok-agent"):
        st, r = call(srv, "/api/audit/result", token=tok,
                     body={"capability": "context.ranking", "outcome": "PASS", "audit_ref": "x"})
        assert st == 403, tok
    assert call(srv, "/api/audit/resolve", token="tok-aud", body={"record_id": "nope", "outcome": "PASS",
                                                                   "audit_ref": "x"})[0] == 404
    assert call(srv, "/api/audit/result", token="tok-aud", body={"capability": "context.ranking",
                                                                  "outcome": "MAYBE", "audit_ref": "x"})[0] == 400


def test_auditor_token_confined_to_audit_plane(srv, m, world):
    for meth, path, body in [("GET", "/api/view/claims", None), ("GET", "/api/view/corpus", None),
                             ("GET", f"/api/view/corpus_content?corpus_id={world['c1']}&purpose=clinic-visit", None),
                             ("POST", "/api/delegation/grant", {"delegate": "agent:x"}),
                             ("POST", "/api/claims/delete", {"claim_id": "x"})]:
        st, r = call(srv, path, token="tok-aud", body=body, method=meth)
        assert st == 403, path
    assert m.gov.entries(kinds=["PROHIBITED_ATTEMPT"])[-1]["body"]["reason"] == "auditor_outside_audit_plane"
    assert call(srv, "/api/export", token="tok-aud")[0] == 403  # export carries claim content
    assert call(srv, "/api/view/suspensions", token="tok-aud")[0] == 200
    assert call(srv, "/api/q1/governance_log", token="tok-aud")[0] == 200


def test_appointment_statement_route(srv, m):
    st = new_statement("APPOINT", TEST_APPOINTER, auditor_id="auditor:carol")
    sig = sign_statement(TEST_APPOINTER_KEY, st)
    s2, r = call(srv, "/api/auditors/statement", token="tok-user", body={"statement": dict(st, auditor_id="auditor:eve"),
                                                                         "signature": sig})
    assert s2 == 403
    s2, r = call(srv, "/api/auditors/statement", token="tok-user", body={"statement": st, "signature": sig})
    assert s2 == 200 and r["auditor_id"] == "auditor:carol" and r["active"]
    v = call(srv, "/api/view/appointments", token="tok-reader")[1]
    assert v["appointer"]["id"] == TEST_APPOINTER and "auditor:carol" in v["active_auditors"] and v["verification"]["ok"]
    assert call(srv, "/api/auditors/statement", token="tok-reader", body={"statement": st, "signature": sig})[0] == 403


def test_delegation_grant_manager(srv, m, world):
    root = world["root"]
    # root grants: user only
    st, r = call(srv, "/api/delegation/grant", token="tok-agent", body={"delegate": "agent:helper"})
    assert st == 403
    st, g = call(srv, "/api/delegation/grant", token="tok-user", body={"delegate": "agent:other",
                                                                       "limits": {"max_lines_per_action": 20}})
    assert st == 200 and g["parent"] is None
    # holder attenuates
    st, sub = call(srv, "/api/delegation/grant", token="tok-agent",
                   body={"delegate": "agent:helper", "parent": root, "limits": {"max_lines_per_action": 10}})
    assert st == 200 and sub["parent"] == root
    st, r = call(srv, "/api/delegation/grant", token="tok-agent",
                 body={"delegate": "agent:helper", "parent": root, "limits": {"max_lines_per_action": 400}})
    assert st == 403  # amplification refused
    st, r = call(srv, "/api/delegation/grant", token="tok-user", body={"delegate": "agent:helper", "parent": g["delegation_id"]})
    assert st == 403  # user does not hold that grant (agent:other does)
    assert call(srv, "/api/delegation/grant", token="tok-agent", body={"delegate": "agent:h", "parent": "deleg-nope"})[0] == 404
    st, ch = call(srv, f"/api/view/delegation_chain?delegation_id={sub['delegation_id']}", token="tok-reader")
    assert [c["delegation_id"] for c in ch["chain"]] == [root, sub["delegation_id"]]
    assert ch["chain"][-1]["effective_limits"]["max_lines_per_action"] == 10
    st, ch = call(srv, f"/api/view/delegation_chain?delegation_id={root}", token="tok-reader")
    assert [d["delegation_id"] for d in ch["descendants"]] == [sub["delegation_id"]]
    # revoke: user only; propagates down the chain
    assert call(srv, "/api/delegation/revoke", token="tok-agent", body={"delegation_id": sub["delegation_id"]})[0] == 403
    st, r = call(srv, "/api/delegation/revoke", token="tok-user", body={"delegation_id": root})
    assert st == 200 and sub["delegation_id"] in r["chain_revoked"]
    assert m.delegation.active_grant_by_id(sub["delegation_id"]) is None
    assert call(srv, "/api/delegation/revoke", token="tok-user", body={"delegation_id": root})[0] == 409
    assert call(srv, "/api/delegation/revoke", token="tok-user", body={"delegation_id": "deleg-nope"})[0] == 404


def test_corpus_content_viewer(srv, m, world):
    v = call(srv, "/api/view/corpus", token="tok-reader")[1]
    item = next(i for i in v["items"] if i["corpus_id"] == world["c1"])
    assert item["use_purposes"] == ["clinic-visit"] and "content_ref" not in item and "content" not in item
    st, r = call(srv, f"/api/view/corpus_content?corpus_id={world['c1']}&purpose=clinic-visit")
    assert st == 200 and r["content"] == "Letter from Dr Lee" and r["grant_id"]
    log = m.gov.entries(kinds=["CLAIMS_RETRIEVED"])[-1]
    assert log["body"]["corpus_ids"] == [world["c1"]] and log["actor"] == "user"
    assert "Letter" not in json.dumps(log["body"])  # identifiers only in the log
    assert world["c1"] in json.dumps(m.q1.claims_retrieved())
    st, r = call(srv, f"/api/view/corpus_content?corpus_id={world['c1']}&purpose=marketing")
    assert (st, r["error"]) == (403, "permission_denied")
    st, r = call(srv, f"/api/view/corpus_content?corpus_id={world['c2']}&purpose=clinic-visit")
    assert st == 403 and "withdrawn" in r["detail"]
    reasons = [e["body"]["reason"] for e in m.gov.entries(kinds=["PROHIBITED_ATTEMPT"])][-2:]
    assert reasons == ["use_closure_failed", "corpus_item_withdrawn"]
    # revoking the use grant closes it again
    g = next(x for x in m.perms.grants() if x["operation"] == "use")
    m.perms.revoke(g["grant_id"], "user")
    assert call(srv, f"/api/view/corpus_content?corpus_id={world['c1']}&purpose=clinic-visit")[0] == 403
    assert call(srv, "/api/view/corpus_content?corpus_id=corpus-nope&purpose=x")[0] == 404
    assert call(srv, "/api/view/corpus_content?corpus_id=x")[0] == 400


def test_carrier_appointment_by_appoint_helper_unaffected_by_reader(m):
    appoint(m, "auditor:z", carrier="reader")
    assert m.auditors.is_active("auditor:z")

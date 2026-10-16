import json
import threading
import urllib.error
import urllib.request

import pytest

from medb.api import load_tokens, make_server
from medb.interfaces import interface_inventory
from medb.query import Q1_QUERIES

TOK = {"tok-user": "user", "tok-reader": "reader", "tok-agent": "agent:coder"}


@pytest.fixture
def srv(m):
    s = make_server(m, TOK, port=0)
    t = threading.Thread(target=s.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{s.server_port}"
    s.shutdown()
    s.server_close()


def call(base, path, token="tok-reader", body=None, method=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(base + path, data=data, method=method or ("POST" if data else "GET"))
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if r.headers["Content-Type"].startswith("application/json") else raw)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def test_loopback_only(m):
    with pytest.raises(ValueError):
        make_server(m, TOK, host="0.0.0.0", port=0)


def test_q1_exactly_eight_routes(srv):
    routes = interface_inventory()["routes"]
    q1 = sorted(r["path"].rsplit("/", 1)[1] for r in routes.values() if r["path"].startswith("/api/q1/"))
    assert q1 == sorted(Q1_QUERIES)
    for q in Q1_QUERIES:
        status, body = call(srv, f"/api/q1/{q}" + ("?action_id=x" if q == "authorizing_clause" else ""))
        assert status == 200 and body["query"] == q
    assert call(srv, "/api/q1/drop_tables")[0] == 404


def test_every_route_registered_and_listed_under_primitives(srv):
    inv = interface_inventory()
    routes = inv["routes"]
    for path in ("/", "/api/view/claims", "/api/view/claim_history", "/api/view/suspensions",
                 "/api/inventory", "/api/ingest/corpus", "/api/ingest/claim", "/api/delegation/evaluate"):
        assert any(r["path"] == path for r in routes.values()), path
    for name, r in routes.items():
        for p in r["primitives"]:
            assert name in inv["primitives"][p]["interfaces"]
    assert "HTTP POST /api/ingest/corpus" in inv["primitives"]["corpus.ingest"]["interfaces"]


def test_auth(srv):
    assert call(srv, "/api/q1/policy_current", token=None)[0] == 401
    assert call(srv, "/api/q1/policy_current", token="nope")[0] == 401
    st, b = call(srv, "/api/ingest/claim", token="tok-reader",
                 body={"subject": "user", "predicate": "likes", "object": "tea", "scope": "food"})
    assert st == 403
    assert call(srv, "/api/view/claims", method="DELETE")[0] == 405
    import http.client
    from urllib.parse import urlparse
    u = urlparse(srv)
    c = http.client.HTTPConnection(u.hostname, u.port)
    c.request("GET", "/")
    r = c.getresponse()
    assert (r.status, r.getheader("Location")) == (302, "/app/")  # D-70: the old viewer is gone


def test_ingest_and_views(srv, m):
    st, b = call(srv, "/api/ingest/claim", token="tok-user",
                 body={"subject": "user", "predicate": "likes", "object": "tea", "scope": "food"})
    assert st == 200
    cid = b["claim_id"]
    # agent cannot assert a user self-account through the API either
    st, b = call(srv, "/api/ingest/claim", token="tok-agent",
                 body={"subject": "user", "predicate": "likes", "object": "coffee", "scope": "food"})
    assert (st, b["error"]) == (403, "not_authorized")
    st, b = call(srv, "/api/ingest/corpus", token="tok-user",
                 body={"content": "letter", "source": "clinic", "scope": "health"})
    assert (st, b["error"]) == (403, "permission_denied")  # no ingest grant: default deny
    m.perms.grant("ingest", "user", scopes=["health"], sources=["clinic"], sensitivity_max="high")
    st, b = call(srv, "/api/ingest/corpus", token="tok-user",
                 body={"content": "letter", "source": "clinic", "scope": "health"})
    assert st == 200 and b["corpus_id"].startswith("corpus-")
    st, v = call(srv, "/api/view/claims")
    assert st == 200 and v["count"] == 1
    assert call(srv, f"/api/view/claim_history?claim_id={cid}")[1]["transitions"][0]["kind"] == "ASSERT"
    last = m.gov.entries(kinds=["CLAIMS_RETRIEVED"])[-1]
    assert last["actor"] == "reader" and last["body"]["via"].startswith("HTTP GET")
    st, v = call(srv, "/api/view/claims?as_of=2000-01-01T00:00:00Z")
    assert v["count"] == 0


def test_delegation_evaluate(srv, m):
    m.delegation.grant("agent:coder", "user")
    act = {"agent": "agent:coder", "kind": "code_change", "changes": [{"path": "src/ui/a.py", "lines": 5}]}
    st, b = call(srv, "/api/delegation/evaluate", token="tok-agent", body=act)
    assert st == 200 and (b["decision"], b["clause"]) == ("AUTHORIZED", "P-1.1")
    st, b = call(srv, "/api/delegation/evaluate", token="tok-user", body=act)  # cannot act as the agent
    assert st == 403
    st, b = call(srv, "/api/delegation/evaluate", token="tok-agent",
                 body=dict(act, changes=[{"path": "src/auth/x.py", "lines": 1}]))
    assert b["decision"] == "REQUIRES_ESCALATION"
    assert m.q1.actions_in_window()["count"] == 2


@pytest.mark.parametrize("primitive,path,token,body", [
    ("corpus.ingest", "/api/ingest/corpus", "tok-user", {"content": "x", "source": "clinic", "scope": "health"}),
    ("claims.ledger", "/api/ingest/claim", "tok-user", {"subject": "u", "predicate": "p", "object": "o", "scope": "s"}),
    ("claims.ledger", "/api/view/claims", "tok-reader", None),
    ("delegation.evaluator", "/api/delegation/evaluate", "tok-agent",
     {"agent": "agent:coder", "kind": "code_change", "changes": [{"path": "src/ui/a.py", "lines": 1}]}),
    ("policy.store", "/api/delegation/evaluate", "tok-agent",  # suspension of a dependency propagates
     {"agent": "agent:coder", "kind": "code_change", "changes": [{"path": "src/ui/a.py", "lines": 1}]}),
])
def test_suspended_capability_does_not_reappear_via_api(srv, m, primitive, path, token, body):
    m.perms.grant("ingest", "user", scopes=["health"], sources=["clinic"], sensitivity_max="high")
    m.delegation.grant("agent:coder", "user")
    assert call(srv, path, token=token, body=body)[0] == 200  # reachable before
    n_actions = len(m.gov.entries(kinds=["ACTION_EVALUATED"]))
    rec = m.suspensions.suspend(primitive, "test", "UNDETERMINED", [], ["x"])
    st, b = call(srv, path, token=token, body=body)
    assert st == 423 and b["error"] == "capability_suspended"
    assert b["suspension_record"]  # names the record that blocks it
    assert len(m.gov.entries(kinds=["ACTION_EVALUATED"])) == n_actions  # nothing evaluated/executed
    pa = m.gov.entries(kinds=["PROHIBITED_ATTEMPT"])[-1]["body"]
    assert pa["interface"].startswith("HTTP ") and pa["reason"] == "capability_suspended"
    # the user cannot lift it through any route; audit plane stays readable
    assert call(srv, "/api/view/suspensions")[0] == 200
    assert call(srv, "/api/q1/governance_log")[0] == 200
    del rec


def test_token_file_created_private(tmp_path):
    p = tmp_path / "t.json"
    toks = load_tokens(p)
    assert set(toks.values()) == {"user", "reader", "agent:coder"}
    assert oct(p.stat().st_mode & 0o777) == "0o600"
    assert load_tokens(p) == toks


def test_old_read_only_viewer_removed(srv):
    """D-70: the D-61 viewer (medb/webui, /app.js) was removed; the app at /app/ supersedes it."""
    from pathlib import Path
    import medb
    assert not (Path(medb.__file__).parent / "webui").exists()
    assert call(srv, "/app.js", token=None)[0] == 404
    st, b = call(srv, "/", token=None)  # urllib follows the redirect to the app
    assert st == 200 and b'type="module"' in b


def test_audit_routes_logged_to_auditlog_during_suspension(m, srv):
    """F-11: audit-plane routes stay open under suspension; each read is logged once
    (outermost) in the separate auditlog stream, with the authenticated actor."""
    assert call(srv, "/api/q1/governance_log")[0] == 200
    assert not m.suspensions.audit_reads()
    m.suspensions.suspend("context.ranking", trigger="t", classification="UNDETERMINED",
                          evidence_available=[], evidence_missing=["x"])
    head = m.gov.head()
    assert call(srv, "/api/q1/governance_log")[0] == 200
    assert call(srv, "/api/view/suspensions")[0] == 200
    assert m.gov.head() == head
    reads = m.suspensions.audit_reads()
    assert [(r["interface"], r["reader"]) for r in reads] == [
        ("HTTP GET /api/q1/governance_log", "reader"), ("HTTP GET /api/view/suspensions", "reader")]

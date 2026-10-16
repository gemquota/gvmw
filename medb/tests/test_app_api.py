"""Routes added for the interactive app (D-67): registration/inventory, auth,
suspension (423 at the primitive), and functional behaviour through the API."""
import io
import json
import re
import threading
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import pytest

from medb import api_app
from medb.api import ROUTES, make_server
from medb.interfaces import interface_inventory

TOK = {"tok-user": "user", "tok-reader": "reader", "tok-agent": "agent:coder"}
APP_ROUTES = [(meth, path) for (meth, path), (fn, w, name) in ROUTES.items()
              if fn.__module__ == "medb.api_app" or getattr(fn, "__wrapped__", fn).__module__ == "medb.api_app"]


@pytest.fixture
def srv(m):
    s = make_server(m, TOK, port=0)
    t = threading.Thread(target=s.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{s.server_port}"
    s.shutdown()
    s.server_close()


def call(base, path, token="tok-user", body=None, method=None, raw=False):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(base + path, data=data, method=method or ("POST" if data is not None else "GET"))
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            b = r.read()
            if raw:
                return r.status, b, r.headers
            return r.status, (json.loads(b) if r.headers["Content-Type"].startswith("application/json") else b)
    except urllib.error.HTTPError as e:
        b = e.read()
        if raw:
            return e.code, b, e.headers
        return e.code, json.loads(b)


def _inv_routes():
    return {(r["method"], r["path"]): (name, r) for name, r in interface_inventory()["routes"].items()}


@pytest.fixture
def seeded(m):
    m.perms.grant("use", "user", scopes=["authority", "health"], purposes=["clinic-visit"], sensitivity_max="high",
                  compose=True)
    m.perms.grant("infer", "user", scopes=["authority", "health"], sensitivity_max="high", compose=True)
    m.perms.grant("ingest", "user", scopes=["health"], sources=["clinic"], sensitivity_max="high")
    a = m.claims.assert_claim("user", "decides", "my own treatment decisions", scope="authority")
    h = m.claims.assert_claim("user", "has", "asthma", scope="health")
    c = m.corpus.ingest("letter", source="clinic", scope="health", actor="user")
    i1 = m.claims.propose("user", "carries", "an inhaler", scope="health", derived_from=[h, c["corpus_id"]],
                          actor="inference:t")
    i2 = m.claims.propose("user", "avoids", "cold air", scope="health", derived_from=[h], actor="inference:t")
    m.delegation.grant("agent:coder", "user")
    return {"a": a, "h": h, "corpus": c["corpus_id"], "i1": i1, "i2": i2}


# ------------------------------------------------------------------ registration / inventory
def test_app_routes_all_registered_and_listed(srv):
    assert len(APP_ROUTES) >= 30
    inv = interface_inventory()
    by = _inv_routes()
    for key in APP_ROUTES:
        assert key in by, key
        name, r = by[key]
        for p in r["primitives"]:
            assert name in inv["primitives"][p]["interfaces"], (name, p)
    expected = {
        ("GET", "/api/app/dashboard"): ("audit", ["governance.log"]),
        ("POST", "/api/claims/delete"): ("capability", ["claims.ledger"]),
        ("POST", "/api/permissions/grant"): ("capability", ["permissions.closure"]),
        ("POST", "/api/corpus/withdraw"): ("capability", ["corpus.ingest"]),
        ("POST", "/api/context/build"): ("capability", ["context.build", "claims.retrieval"]),
        ("POST", "/api/escalations/resolve"): ("capability", ["delegation.execution", "authority.resolution"]),
        ("GET", "/api/view/directives"): ("capability", ["normative.store"]),
        ("POST", "/api/anchors/anchor"): ("capability", ["governance.anchoring", "governance.log"]),
        ("GET", "/api/app/whoami"): ("meta", []),
        ("GET", "/app/"): ("static", []),
    }
    for key, (plane, prims) in expected.items():
        assert by[key][1]["plane"] == plane and by[key][1]["primitives"] == prims, key


def test_every_app_write_route_reaches_a_primitive():
    for (meth, path), (fn, write, name) in ROUTES.items():
        if (meth, path) in APP_ROUTES and meth == "POST":
            assert write, path
            assert _inv_routes()[(meth, path)][1]["primitives"], path


# ------------------------------------------------------------------ auth
@pytest.mark.parametrize("key", [k for k in APP_ROUTES if not k[1].startswith("/app/")])
def test_app_api_routes_require_token(srv, key):
    meth, path = key
    st, b = call(srv, path, token=None, body={} if meth == "POST" else None, method=meth)
    assert st == 401
    assert call(srv, path, token="bogus", body={} if meth == "POST" else None, method=meth)[0] == 401


@pytest.mark.parametrize("key", [k for k in APP_ROUTES if k[0] == "POST"])
def test_reader_cannot_write(srv, key):
    st, b = call(srv, key[1], token="tok-reader", body={})
    assert (st, b["error"]) == (403, "not_authorized")


@pytest.mark.parametrize("path,body", [
    ("/api/claims/correct", {"claim_id": "{a}", "changes": {"object": "x"}}),
    ("/api/claims/supersede", {"claim_id": "{a}", "by_claim_id": "{h}"}),
    ("/api/claims/disavow", {"claim_id": "{a}"}),
    ("/api/claims/delete", {"claim_id": "{a}"}),
    ("/api/claims/confirm", {"claim_id": "{i1}"}),
    ("/api/claims/reject", {"claim_id": "{i1}"}),
    ("/api/permissions/grant", {"operation": "use", "scopes": ["food"], "purposes": ["x"]}),
    ("/api/permissions/revoke", {"grant_id": "{grant}"}),
    ("/api/corpus/withdraw", {"corpus_id": "{corpus}"}),
    ("/api/escalations/resolve", {"escalation_id": "{esc}", "approve": True}),
    ("/api/env/condition", {"condition": "deadline", "value": True}),
    ("/api/integrity_check", {}),
])
def test_agent_cannot_mutate_user_state(srv, m, seeded, path, body):
    esc = m.delegation.submit({"agent": "agent:coder", "kind": "code_change",
                               "changes": [{"path": "src/auth/x.py", "lines": 1}]})["escalation_id"]
    ids = dict(seeded, grant=m.perms.grants()[0]["grant_id"], esc=esc)
    body = _fmt(body, ids)
    before = {s: len(m.store.events(s)) for s in ("claims", "permissions", "corpus", "delegation")}
    st, b = call(srv, path, token="tok-agent", body=body)
    assert st == 403, (path, b)
    assert {s: len(m.store.events(s)) for s in before} == before


def test_whoami_and_capability_hints(srv):
    for tok, actor in TOK.items():
        st, b = call(srv, "/api/app/whoami", token=tok)
        assert st == 200 and b["actor"] == actor
    assert "delete" in call(srv, "/api/app/whoami")[1]["can"]
    assert call(srv, "/api/app/whoami", token="tok-reader")[1]["can"] == ["export", "read_corpus"]
    assert "delete" not in call(srv, "/api/app/whoami", token="tok-agent")[1]["can"]


# ------------------------------------------------------------------ suspension
CAP_ROUTES = [
    ("claims.ledger", "GET", "/api/view/claim?claim_id={a}", None),
    ("claims.ledger", "GET", "/api/claims/delete_preview?claim_id={a}", None),
    ("claims.ledger", "POST", "/api/claims/correct", {"claim_id": "{a}", "changes": {"object": "x"}}),
    ("claims.ledger", "POST", "/api/claims/supersede", {"claim_id": "{a}", "by_claim_id": "{h}"}),
    ("claims.ledger", "POST", "/api/claims/disavow", {"claim_id": "{a}"}),
    ("claims.ledger", "POST", "/api/claims/delete", {"claim_id": "{a}"}),
    ("claims.ledger", "POST", "/api/claims/confirm", {"claim_id": "{i1}"}),
    ("claims.ledger", "POST", "/api/claims/reject", {"claim_id": "{i1}"}),
    ("permissions.closure", "GET", "/api/view/permissions", None),
    ("permissions.closure", "POST", "/api/permissions/grant", {"operation": "use", "scopes": ["food"]}),
    ("permissions.closure", "POST", "/api/permissions/revoke", {"grant_id": "{grant}"}),
    ("corpus.ingest", "GET", "/api/view/corpus", None),
    ("corpus.ingest", "POST", "/api/corpus/withdraw", {"corpus_id": "{corpus}"}),
    ("context.build", "POST", "/api/context/build", {"purpose": "clinic-visit"}),
    ("claims.retrieval", "POST", "/api/context/build", {"purpose": "clinic-visit"}),
    ("authority.resolution", "POST", "/api/escalations/resolve", {"escalation_id": "{esc}", "approve": True}),
    ("delegation.execution", "POST", "/api/escalations/resolve", {"escalation_id": "{esc}", "approve": True}),
    ("normative.store", "GET", "/api/view/directives", None),
    ("governance.anchoring", "POST", "/api/anchors/anchor", {}),
]


def _fmt(v, ids):
    if isinstance(v, str):
        return v.format(**ids)
    if isinstance(v, dict):
        return {k: _fmt(x, ids) for k, x in v.items()}
    return v


@pytest.mark.parametrize("primitive,meth,path,body", CAP_ROUTES)
def test_capability_routes_423_when_suspended(srv, m, seeded, primitive, meth, path, body):
    esc = m.delegation.submit({"agent": "agent:coder", "kind": "code_change",
                               "changes": [{"path": "src/auth/x.py", "lines": 1}]})["escalation_id"]
    ids = dict(seeded, grant=m.perms.grants()[-1]["grant_id"], esc=esc)
    path = path.format(**ids)
    body = _fmt(body, ids)
    heads = {s: len(m.store.events(s)) for s in ("claims", "permissions", "corpus", "delegation", "normative")}
    m.suspensions.suspend(primitive, "test", "UNDETERMINED", [], ["x"])
    st, b = call(srv, path, body=body, method=meth)
    assert st == 423 and b["error"] == "capability_suspended" and b["suspension_record"], (path, b)
    assert {s: len(m.store.events(s)) for s in heads} == heads  # nothing changed
    pa = m.gov.entries(kinds=["PROHIBITED_ATTEMPT"])[-1]["body"]
    assert pa["reason"] == "capability_suspended" and pa["interface"].startswith("HTTP ")


def test_suspension_of_dependency_propagates_to_app_routes(srv, m, seeded):
    m.suspensions.suspend("governance.log", "test", "UNDETERMINED", [], ["x"])
    assert call(srv, f"/api/view/claim?claim_id={seeded['a']}")[0] == 423
    assert call(srv, "/api/permissions/grant", body={"operation": "use", "scopes": ["food"]})[0] == 423


AUDIT_GETS = ["/api/app/dashboard", "/api/view/gov", "/api/view/verify", "/api/view/auditlog", "/api/view/anchors",
              "/api/view/escalations", "/api/view/delegation", "/api/view/primitive_graph", "/api/export",
              "/api/app/whoami", "/api/app/changes"]


def test_audit_and_meta_routes_open_under_suspension(srv, m, seeded):
    m.suspensions.suspend("governance.log", "test", "UNDETERMINED", [], ["x"])
    n = len(m.suspensions.audit_reads())
    for p in AUDIT_GETS:
        assert call(srv, p, token="tok-reader")[0] == 200, p
    reads = [r["interface"] for r in m.suspensions.audit_reads()[n:]]
    for p in AUDIT_GETS[:-2]:  # audit plane is logged (F-11); meta routes return no record content
        assert f"HTTP GET {p}" in reads, p
    assert not any("/api/app/whoami" in r or "/api/app/changes" in r for r in reads)
    assert call(srv, "/api/integrity_check", body={})[0] == 200


# ------------------------------------------------------------------ functional
def test_claim_detail_versions_and_time_travel(srv, m, clock, seeded):
    t0 = clock.now_iso()
    clock._t = clock._t.replace(hour=5)
    st, b = call(srv, "/api/claims/correct", body={"claim_id": seeded["a"], "changes": {"object": "after options"}})
    assert st == 200 and b["version"] == 2
    st, d = call(srv, f"/api/view/claim?claim_id={seeded['a']}&as_of={t0}")
    assert st == 200
    assert [v["object"] for v in d["versions"]] == ["my own treatment decisions", "after options"]
    assert d["as_of_state"]["object"] == "my own treatment decisions" and d["current"]["object"] == "after options"
    assert [t["kind"] for t in d["transitions"]] == ["ASSERT", "CORRECT"]
    assert m.gov.entries(kinds=["CLAIMS_RETRIEVED"])[-1]["body"]["via"] == "HTTP GET /api/view/claim"
    st, d = call(srv, f"/api/view/claim?claim_id={seeded['i1']}")
    ids = {n["id"]: n["type"] for n in d["graph"]["nodes"]}
    assert ids[seeded["corpus"]] == "corpus" and ids[seeded["h"]] == "claim"
    assert call(srv, "/api/view/claim?claim_id=nope")[0] == 404
    assert call(srv, "/api/view/claim")[0] == 400


def test_delete_with_preview_and_destroy_choice(srv, m, seeded):
    st, pv = call(srv, f"/api/claims/delete_preview?claim_id={seeded['h']}")
    assert st == 200
    assert set(json.dumps(pv).split('"')) >= {seeded["i1"], seeded["i2"]}
    st, b = call(srv, "/api/claims/delete", body={"claim_id": seeded["h"], "destroy_derived": [seeded["i1"]]})
    assert st == 200, b
    s = m.claims.state()
    assert s[seeded["h"]]["status"] == "deleted" and s[seeded["i1"]]["status"] == "deleted"
    assert s[seeded["i2"]]["status"] != "deleted"
    st, b = call(srv, "/api/claims/delete", body={"claim_id": seeded["a"], "destroy_derived": "bogus"})
    assert st == 400


def test_confirm_reject_disavow_supersede(srv, m, seeded):
    assert call(srv, "/api/claims/confirm", body={"claim_id": seeded["i1"]})[0] == 200
    assert call(srv, "/api/claims/reject", body={"claim_id": seeded["i2"], "reason": "no"})[0] == 200
    s = m.claims.state()
    assert s[seeded["i1"]]["confirmation"] == "user_confirmed" and s[seeded["i2"]]["confirmation"] == "user_rejected"
    n = call(srv, "/api/ingest/claim", body={"subject": "user", "predicate": "decides", "object": "with partner",
                                             "scope": "authority"})[1]["claim_id"]
    assert call(srv, "/api/claims/supersede", body={"claim_id": seeded["a"], "by_claim_id": n})[0] == 200
    assert call(srv, "/api/claims/disavow", body={"claim_id": n})[0] == 200
    s = m.claims.state()
    assert (s[seeded["a"]]["status"], s[n]["status"]) == ("superseded", "disavowed")
    assert call(srv, "/api/claims/correct", body={"claim_id": seeded["h"], "changes": {}})[0] == 400


def test_permissions_grant_compose_and_revoke(srv, m):
    st, g = call(srv, "/api/permissions/grant", body={"operation": "infer", "scopes": ["health", "food"],
                                                      "sensitivity_max": "high", "compose": True})
    assert st == 200 and g["compose"] is True
    st, v = call(srv, "/api/view/permissions", token="tok-reader")
    assert st == 200 and v["grants"][0]["active"]
    assert call(srv, "/api/permissions/revoke", body={"grant_id": g["grant_id"]})[0] == 200
    assert not call(srv, "/api/view/permissions")[1]["grants"][0]["active"]
    assert call(srv, "/api/permissions/revoke", body={"grant_id": "nope"})[0] == 404
    assert call(srv, "/api/permissions/grant", body={"operation": "use"})[0] == 400


def test_corpus_list_and_withdraw(srv, m, seeded):
    st, v = call(srv, "/api/view/corpus", token="tok-reader")
    assert st == 200 and "letter" not in json.dumps(v["items"])  # metadata only
    st, b = call(srv, "/api/corpus/withdraw", body={"corpus_id": seeded["corpus"], "reason": "old"})
    assert st == 200
    assert m.corpus.items()[seeded["corpus"]]["withdrawn"]
    assert call(srv, "/api/corpus/withdraw", body={"corpus_id": "corpus-nope"})[0] == 404


def test_context_build_returns_package_and_record(srv, m, seeded):
    st, b = call(srv, "/api/context/build", body={"purpose": "clinic-visit", "predicates": ["decides", "has"]})
    assert st == 200, b
    p = b["package"]
    assert {c["claim_id"] for c in p["claims"]} == {seeded["a"], seeded["h"]}
    assert b["issuance_record"]["body"]["package_id"] == p["package_id"]
    for k in ("contradictions", "unknowns", "boundary", "rationale"):
        assert k in p
    st, b = call(srv, "/api/context/build", body={"purpose": "unpermitted-purpose"})
    assert st in (200, 403)
    if st == 200:
        assert b["package"]["claims"] == []


def test_escalation_resolve_positions_and_deferrability(srv, m, seeded):
    act = {"agent": "agent:coder", "kind": "code_change", "matter": "m1",
           "changes": [{"path": "src/auth/x.py", "lines": 1}]}
    esc = m.delegation.submit(act)["escalation_id"]
    st, v = call(srv, "/api/view/escalations", token="tok-reader")
    e = [x for x in v["escalations"] if x["escalation_id"] == esc][0]
    assert e["matter"] == "m1" and e["deferrability_now"]
    bad = call(srv, "/api/escalations/resolve", body={"escalation_id": esc, "positions": [{"position": "maybe"}]})
    assert bad[0] == 400
    assert call(srv, "/api/escalations/resolve", body={"escalation_id": esc, "deferrable": "yes"})[0] == 400
    # conflicting equal positions on a deferrable matter: nothing happens, no suspension (F-02)
    st, r = call(srv, "/api/escalations/resolve", body={"escalation_id": esc, "positions": [
        {"position": "approve"}, {"position": "reject"}]})
    assert st == 200 and not m.suspensions.active()
    # the user marks it non-deferrable -> III.1 suspension
    esc2 = m.delegation.submit(dict(act, matter="m2"))["escalation_id"]
    st, r = call(srv, "/api/escalations/resolve", body={"escalation_id": esc2, "deferrable": False, "positions": [
        {"position": "approve"}, {"position": "reject"}]})
    assert st == 200
    assert any(x["record"]["capability"].endswith(":m2") for x in m.suspensions.active())
    st, g = call(srv, "/api/view/primitive_graph", token="tok-reader")
    assert any(s["id"].endswith(":m2") for s in g["scoped"]) and g["propagation"]
    assert call(srv, "/api/escalations/resolve", body={"escalation_id": "esc-nope", "approve": True})[0] == 404


def test_env_condition_and_delegation_view(srv, m):
    st, b = call(srv, "/api/env/condition", body={"condition": "deadline", "value": True, "matter": "mx"})
    assert st == 200
    v = call(srv, "/api/view/delegation", token="tok-reader")[1]
    assert v["conditions"][-1]["condition"] == "deadline" and v["budget"]["limit"] == 500


def test_directives_view(srv, m):
    m.delegation.grant("agent:coder", "user")
    esc = m.delegation.submit({"agent": "agent:coder", "kind": "code_change",
                               "changes": [{"path": "src/auth/x.py", "lines": 1}]})["escalation_id"]
    m.delegation.resolve_escalation(esc, "user", approve=True)
    st, v = call(srv, "/api/view/directives", token="tok-reader")
    assert st == 200 and len(v["directives"]) >= 1


def test_gov_verify_integrity_auditlog_anchors(srv, m, seeded):
    st, g = call(srv, "/api/view/gov?limit=5", token="tok-reader")
    assert st == 200 and len(g["entries"]) <= 5 and g["verification"]["ok"]
    assert all(g["cross_links_ok"].values())
    assert call(srv, "/api/view/verify", token="tok-reader")[1]["ok"]
    n = len(m.gov.entries(kinds=["INTEGRITY_CHECK"]))
    assert call(srv, "/api/integrity_check", body={})[0] == 200
    assert len(m.gov.entries(kinds=["INTEGRITY_CHECK"])) == n + 1
    assert call(srv, "/api/view/auditlog", token="tok-reader")[0] == 200
    st, a = call(srv, "/api/view/anchors", token="tok-reader")
    assert st == 200 and a["enabled"] is False
    st, b = call(srv, "/api/anchors/anchor", body={})
    assert st == 409  # anchoring is off by default (D-62); nothing leaves the machine
    st, d = call(srv, "/api/app/dashboard", token="tok-reader")
    assert d["claims"]["total"] == 4 and d["claims"]["pending_proposals"] == 2 and d["budget"]["limit"] == 500
    assert "object" not in json.dumps(d)


def test_export_zip_download(srv, m, seeded):
    st, b, hdr = call(srv, "/api/export", token="tok-reader", raw=True)
    assert st == 200 and hdr["Content-Type"] == "application/zip"
    assert "attachment" in hdr["Content-Disposition"]
    names = zipfile.ZipFile(io.BytesIO(b)).namelist()
    assert any(n.endswith("manifest.json") for n in names)
    assert call(srv, "/api/export", token="tok-agent")[0] == 403


def test_changes_token_ignores_reads(srv, m, seeded):
    t1 = call(srv, "/api/app/changes")[1]["token"]
    call(srv, f"/api/view/claim?claim_id={seeded['a']}")  # writes CLAIMS_RETRIEVED only
    call(srv, "/api/claims/delete", token="tok-agent", body={"claim_id": seeded["a"]})  # PROHIBITED_ATTEMPT only
    assert call(srv, "/api/app/changes")[1]["token"] == t1
    call(srv, "/api/claims/disavow", body={"claim_id": seeded["a"]})
    assert call(srv, "/api/app/changes")[1]["token"] != t1


# ------------------------------------------------------------------ static app
def test_static_app_served_with_strict_csp(srv):
    st, b, hdr = call(srv, "/app/", token=None, raw=True)
    assert st == 200 and b"<script type=\"module\"" in b
    csp = hdr["Content-Security-Policy"]
    assert "default-src 'self'" in csp and "script-src" not in csp and "unsafe-eval" not in csp  # scripts: self only
    assert "connect-src 'self'" in csp and "frame-ancestors 'none'" in csp and "http" not in csp
    assert hdr["X-Frame-Options"] == "DENY"
    st, b, hdr = call(srv, "/app/js/main.js", token=None, raw=True)
    assert st == 200 and hdr["Content-Type"].startswith("application/javascript")
    assert hdr["Cache-Control"] == "no-store"  # never served stale after an update
    assert call(srv, "/app/../medb/api.py", token=None)[0] in (400, 404)


def test_app_has_no_innerhtml_no_external_urls_and_only_api_calls():
    app = Path(api_app.APP_DIR)
    files = list(app.rglob("*.js")) + list(app.glob("*.html")) + list(app.glob("*.css"))
    assert files
    for f in files:
        t = f.read_text()
        for bad in ("innerHTML", "outerHTML", "insertAdjacentHTML", "document.write", "eval(", "new Function"):
            assert bad not in t, (f.name, bad)
        assert not re.search(r"https?://(?!www\.w3\.org/2000/svg)", t), f.name
    assert "fetch(" in (app / "js" / "api.js").read_text()  # the only network call site
    for f in app.rglob("*.js"):
        if f.name != "api.js":
            assert "fetch(" not in f.read_text(), f.name


def test_app_server_loopback_only(m):
    with pytest.raises(ValueError):
        make_server(m, TOK, host="0.0.0.0", port=0)


def test_app_kept_out_of_round1_inventory_and_envelopes():
    """D-67: without a server, the in-process inventory (what subjects/envelopes record) has no app routes,
    and the envelope builder leaves api_app.py out of the source copy."""
    import subprocess
    import sys
    root = Path(__file__).resolve().parent.parent
    code = ("import sys; sys.path.insert(0, '.'); from medb.system import MedB; "
            "from medb.interfaces import interface_inventory as i; "
            "r = i()['routes']; print(sum(v['path'].startswith(('/app/', '/api/app/', '/api/view/claim?')) or v['path'] == '/api/view/claim' for v in r.values()))")
    out = subprocess.run([sys.executable, "-c", code], cwd=root, capture_output=True, text=True, check=True)
    assert out.stdout.strip() == "0"
    assert '"api_app.py"' in (root / "experiment" / "build_envelopes.py").read_text()


def test_python_m_medb_api_serves_the_app(tmp_path):
    """`python -m medb.api` (the documented entry point) serves the app and its routes."""
    import subprocess
    import sys
    import time
    root = Path(__file__).resolve().parent.parent
    p = subprocess.Popen([sys.executable, "-m", "medb.api", "--db", str(tmp_path / "x.sqlite"), "--tokens",
                          str(tmp_path / "t.json"), "--port", "0"], cwd=root, stdout=subprocess.PIPE, text=True)
    try:
        line = p.stdout.readline()
        port = int(re.search(r":(\d+)/", line).group(1))
        toks = json.loads((tmp_path / "t.json").read_text())
        base = f"http://127.0.0.1:{port}"
        for _ in range(50):
            try:
                st, b, _h = call(base, "/app/", token=None, raw=True)
                break
            except urllib.error.URLError:
                time.sleep(0.1)
        assert st == 200
        st, who = call(base, "/api/app/whoami", token=toks["user"])
        assert (st, who["actor"]) == (200, "user")
        assert call(base, "/api/app/whoami", token=toks["reader"])[1]["actor"] == "reader"
    finally:
        p.terminate()
        p.wait(10)

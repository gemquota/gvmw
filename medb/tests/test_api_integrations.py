"""D-75: integrations HTTP routes (status, outbox feed, importer) -- auth, inventory, 423."""
import json
import threading

import pytest

from conftest import appointer_config
from integ_fixtures import write_all
from medb.api import make_server
from medb.interfaces import interface_inventory
from medb.system import MedB
from medb.util import FixedClock
from test_app_api import call

TOK = {"tok-user": "user", "tok-reader": "reader", "tok-agent": "agent:coder", "tok-aud": "auditor:t1",
       "tok-inf": "inference:assistant"}
NEW = [("GET", "/api/integrations/status", "audit", ["governance.log"]),
       ("GET", "/api/view/outbox", "audit", ["integrations.outbox", "governance.log"]),
       ("GET", "/api/view/mcp_activity", "audit", ["integrations.mcp"]),
       ("GET", "/api/view/import_runs", "audit", ["governance.log"]),
       ("GET", "/api/import/formats", "meta", []),
       ("GET", "/api/import/files", "capability", ["integrations.import"]),
       ("POST", "/api/import/file", "capability", ["integrations.import", "corpus.ingest", "permissions.closure"]),
       ("POST", "/api/claims/propose", "capability", ["claims.inference_proposal", "permissions.closure"])]


@pytest.fixture
def env(tmp_path, appointer_key_file):
    files = write_all(tmp_path / "imports")
    cfg = appointer_config(appointer_key_file)
    cfg["integrations"]["importers"].update(enabled=True, allowed_roots=[str(tmp_path / "imports")])
    cfg["integrations"]["outbox"].update(enabled=True)
    m = MedB(clock=FixedClock("2026-09-20T00:00:00Z"), seed=13, config=cfg)
    m.perms.grant("ingest", "user", scopes=["health"], sources=["import:fhir_r4_bundle"], sensitivity_max="high")
    s = make_server(m, TOK, port=0)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    yield m, f"http://127.0.0.1:{s.server_port}", files
    s.shutdown()
    s.server_close()


@pytest.mark.parametrize("meth,path,plane,prims", NEW)
def test_routes_registered(env, meth, path, plane, prims):
    inv = interface_inventory()
    r = inv["routes"][f"HTTP {meth} {path}"]
    assert (r["plane"], r["primitives"]) == (plane, prims)
    for p in prims:
        assert f"HTTP {meth} {path}" in inv["primitives"][p]["interfaces"]


@pytest.mark.parametrize("meth,path,plane,prims", NEW)
def test_routes_need_token(env, meth, path, plane, prims):
    assert call(env[1], path, token=None, body={} if meth == "POST" else None, method=meth)[0] == 401


def test_import_via_api_user_only(env):
    m, base, files = env
    for tok in ("tok-reader", "tok-agent", "tok-aud", "tok-inf"):
        st, r = call(base, "/api/import/file", token=tok, body={"path": str(files["fhir"])})
        assert st == 403, tok
    st, r = call(base, "/api/import/files", token="tok-agent")
    assert st == 403
    assert not m.corpus.items()
    st, r = call(base, "/api/import/files")
    assert st == 200 and "health_bundle.json" in [f["path"] for f in r["files"]]
    st, r = call(base, "/api/import/file", body={"path": "health_bundle.json", "account": "portal:gem"})
    assert st == 200 and r["ingested"] == 3 and r["format"] == "fhir_r4_bundle"
    st, r = call(base, "/api/view/import_runs", token="tok-reader")
    assert st == 200 and r["runs"][0]["kind"] == "IMPORT_RUN" and r["runs"][0]["file_sha256"]


def test_import_refusals_mapped(env):
    m, base, files = env
    st, r = call(base, "/api/import/file", body={"path": str(files["unknown"])})
    assert st == 422 and r["error"] == "import_refused"
    st, r = call(base, "/api/import/file", body={"path": str(files["mbox"])})  # no grant for import:gmail_mbox
    assert st == 403 and r["error"] == "permission_denied"
    st, r = call(base, "/api/import/file", body={"path": "/etc/passwd"})
    assert st == 422
    m.importer.config["enabled"] = False
    st, r = call(base, "/api/import/file", body={"path": str(files["fhir"])})
    assert st == 409 and r["error"] == "integration_disabled"


@pytest.mark.parametrize("prim", ["integrations.import", "corpus.ingest"])
def test_import_423_when_suspended(env, prim):
    m, base, files = env
    m.suspensions.suspend(prim, "t", "UNDETERMINED", [], ["x"])
    st, r = call(base, "/api/import/file", body={"path": str(files["fhir"])})
    assert st == 423 and r["suspension_record"]
    assert not m.corpus.items()


def test_status_and_outbox_feed(env):
    m, base, files = env
    st, r = call(base, "/api/integrations/status", token="tok-reader")
    assert st == 200 and r["importers"]["enabled"] and r["outbox"]["enabled"] and not r["mcp"]["enabled"]
    assert r["live_sync"]["enabled"] is False and r["live_sync"]["outbound_class"] == "live_sync"  # built (D-76), off by default
    m.suspensions.suspend("context.ranking", "t", "UNDETERMINED", [], ["x"])
    st, r = call(base, "/api/view/outbox", token="tok-aud")
    assert st == 200 and r["notifications"][0]["event"] == "SUSPENSION"
    st, r = call(base, "/api/import/formats", token="tok-agent")
    assert st == 200 and r["cookie_values_imported"] is False and len(r["formats"]) == 17


def test_outbox_feed_open_when_outbox_suspended(env):
    m, base, files = env
    m.suspensions.suspend("integrations.outbox", "t", "UNDETERMINED", [], ["x"])
    st, r = call(base, "/api/view/outbox")
    assert st == 200 and r["count"] == 0
    st, r = call(base, "/api/import/file", body={"path": str(files["fhir"])})  # writes still work; sync skipped
    assert st == 200


def test_propose_route_requires_inference_actor(env):
    m, base, files = env
    m.perms.grant("infer", "user", scopes=["health"], sensitivity_max="high")
    c = m.claims.assert_claim("user", "has", "asthma", scope="health")
    body = {"subject": "user", "predicate": "carries", "object": "inhaler", "scope": "health", "derived_from": [c]}
    for tok in ("tok-user", "tok-agent"):
        assert call(base, "/api/claims/propose", token=tok, body=body)[0] == 403
    st, r = call(base, "/api/claims/propose", token="tok-inf", body=body)
    assert st == 200 and m.claims.current()[r["claim_id"]]["confirmation"] == "unconfirmed"
    # the inference token may not use any other capability route
    st, r = call(base, "/api/ingest/claim", token="tok-inf", body={"subject": "u", "predicate": "p", "object": "o", "scope": "health"})
    assert st == 403 and m.gov.entries(kinds=["PROHIBITED_ATTEMPT"])[-1]["body"]["reason"] == "inference_token_outside_propose"
    st, r = call(base, "/api/view/outbox")
    assert "INFERENCE_PROPOSED" in {n["event"] for n in r["notifications"]}


def test_whoami_can_lists(env):
    m, base, files = env
    assert "import" in call(base, "/api/app/whoami")[1]["can"]
    assert call(base, "/api/app/whoami", token="tok-inf")[1]["can"] == ["propose"]

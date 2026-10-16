"""D-78: live-sync HTTP routes -- inventory, user-only, MCP/assistants refused, 423, disconnect under suspension."""
import json
import threading

import pytest

from medb.api import make_server
from medb.interfaces import interface_inventory
from sync_env import connect_github, make
from sync_fakes import SECRETS, Fake
from test_app_api import call

TOK = {"tok-user": "user", "tok-reader": "reader", "tok-agent": "agent:coder", "tok-aud": "auditor:t1",
       "tok-inf": "inference:assistant", "tok-mcp": "agent:assistant"}
NEW = [("GET", "/api/sync/status", "audit", ["integrations.sync"]),
       ("GET", "/api/view/sync_runs", "audit", ["integrations.sync"]),
       ("POST", "/api/sync/connect", "capability", ["integrations.sync"]),
       ("POST", "/api/sync/connect_poll", "capability", ["integrations.sync"]),
       ("POST", "/api/sync/run", "capability", ["integrations.sync", "corpus.ingest", "permissions.closure"]),
       ("POST", "/api/sync/disconnect", "revocation", ["integrations.sync"])]


@pytest.fixture
def env(tmp_path, appointer_key_file):
    fake = Fake()
    m = make(tmp_path, appointer_key_file, fake)
    m.config["integrations"]["mcp"]["enabled"] = True
    m.mcp_activity.config["enabled"] = True
    s = make_server(m, TOK, port=0)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    yield m, f"http://127.0.0.1:{s.server_port}", fake
    s.shutdown()
    s.server_close()


@pytest.mark.parametrize("meth,path,plane,prims", NEW)
def test_routes_registered(env, meth, path, plane, prims):
    r = interface_inventory()["routes"][f"HTTP {meth} {path}"]
    assert (r["plane"], r["primitives"]) == (plane, prims)
    assert call(env[1], path, token=None, body={} if meth == "POST" else None, method=meth)[0] == 401


@pytest.mark.parametrize("tok", ["tok-reader", "tok-agent", "tok-aud", "tok-inf", "tok-mcp"])
def test_non_user_tokens_cannot_connect_sync_disconnect(env, tok):
    m, base, fake = env
    for path in ("/api/sync/connect", "/api/sync/connect_poll", "/api/sync/run", "/api/sync/disconnect"):
        st, _ = call(base, path, token=tok, body={"service": "github"})
        assert st == 403, (tok, path)
    assert fake.calls == []


def test_user_token_via_mcp_header_refused(env):
    """The MCP bridge carries no sync tool; even the user's token over X-MedB-Via: mcp is refused."""
    import urllib.request
    m, base, fake = env
    for tok in ("tok-user", "tok-mcp"):
        req = urllib.request.Request(base + "/api/sync/connect", data=json.dumps({"service": "github"}).encode(),
                                     method="POST", headers={"Authorization": f"Bearer {tok}", "X-MedB-Via": "mcp",
                                                             "X-MedB-MCP-Tool": "medb_sync", "Content-Type": "application/json"})
        with pytest.raises(urllib.error.HTTPError) as e:
            urllib.request.urlopen(req)
        assert e.value.code == 403
    assert fake.calls == []
    from medb.integrations.mcp_tools import TOOLS
    assert not any(t["path"].startswith("/api/sync") for t in TOOLS.values())


def test_flow_via_api(env):
    m, base, fake = env
    st, r = call(base, "/api/sync/connect", body={"service": "github"})
    assert st == 200 and r["user_code"] == "WDJB-MJHT" and "device_code" not in json.dumps(r)
    assert call(base, "/api/sync/connect_poll", body={"service": "github"})[1]["pending"] is True
    st, r = call(base, "/api/sync/connect_poll", body={"service": "github"})
    assert st == 200 and r["connected"]
    st, r = call(base, "/api/sync/run", body={"service": "github"})
    assert st == 200 and r["ingested"] == 7
    st, r = call(base, "/api/sync/run", body={"all": True})
    assert st == 200 and [x["service"] for x in r["runs"]] == ["github"]
    st, s = call(base, "/api/sync/status", token="tok-reader")
    gh = s["services"]["github"]
    assert gh["connected"] and gh["items"] == 7 and gh["last_sync"]["ingested"] == 0 and gh["last_sync"]["error"] is None
    st, runs = call(base, "/api/view/sync_runs", token="tok-aud")
    assert st == 200 and runs["verification"]["ok"] and runs["events"][0]["kind"] == "RUN"
    st, _ = call(base, "/api/sync/run", body={"service": "nope"})
    assert st == 400
    for blob in (json.dumps(s), json.dumps(runs), json.dumps(call(base, "/api/integrations/status")[1])):
        for sec in SECRETS:
            assert sec not in blob


def test_disabled_and_refused_codes(env):
    m, base, fake = env
    m.sync.config["services"]["github"]["enabled"] = False
    assert call(base, "/api/sync/connect", body={"service": "github"})[0] == 409
    m.sync.config["services"]["github"]["enabled"] = True
    assert call(base, "/api/sync/run", body={"service": "github"})[0] == 422  # not connected


def test_423_when_suspended_disconnect_open(env):
    m, base, fake = env
    connect_github(m)
    m.suspensions.suspend("integrations.sync", "t", "UNDETERMINED", [], ["x"])
    for path in ("/api/sync/connect", "/api/sync/connect_poll", "/api/sync/run"):
        assert call(base, path, body={"service": "github"})[0] == 423, path
    st, r = call(base, "/api/sync/disconnect", body={"service": "github"})
    assert st == 200 and r["token_deleted"]
    assert call(base, "/api/sync/status", token="tok-reader")[0] == 200  # audit plane open


def test_ingest_suspended_blocks_run(env):
    m, base, fake = env
    connect_github(m)
    m.suspensions.suspend("corpus.ingest", "t", "UNDETERMINED", [], ["x"])
    assert call(base, "/api/sync/run", body={"service": "github"})[0] == 423


def test_cron_cli(env, capsys):
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location("medb_sync", Path(__file__).resolve().parent.parent / "tools" / "medb_sync.py")
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    m, base, fake = env
    connect_github(m)
    assert cli.main(["run", "--all", "--api", base, "--token", "tok-user"]) == 0
    assert cli.main(["status", "--api", base, "--token", "tok-user"]) == 0
    assert cli.main(["run", "--all", "--api", base, "--token", "tok-mcp"]) == 2  # assistants refused
    with pytest.raises(SystemExit):
        cli.main(["status", "--api", "http://evil.example", "--token", "tok-user"])
    out = capsys.readouterr()
    assert "github" in out.out and "tok-user" not in out.out + out.err


def _load_tool(name):
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location(name, Path(__file__).resolve().parent.parent / "tools" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_status_reports_missing_client_fields_and_shared_source(tmp_path, appointer_key_file):
    from sync_fakes import CLIENTS
    m = make(tmp_path, appointer_key_file, Fake())
    (tmp_path / "clients.json").write_text(json.dumps(dict(CLIENTS, github={})))
    for s in ("google_gmail", "google_calendar", "google_contacts"):
        m.sync.config["services"][s]["source"] = "sync:google"
    st = m.sync.status()
    assert st["github"]["client_missing"] == ["client_id"] and not st["github"]["connectable"]
    assert st["github"]["not_connectable_because"] == ["client_id"]
    assert st["google_gmail"]["connectable"] and st["google_gmail"]["source"] == "sync:google"
    from medb.integrations.livesync import SyncDisabled
    with pytest.raises(SyncDisabled) as e:
        m.sync.connect("github", actor="user")
    assert "client_id" in str(e.value)
    # one sync:google grant covers the three Google services
    m2 = make(tmp_path / "b", appointer_key_file, Fake(), grant=False)
    for s in ("google_gmail", "google_calendar", "google_contacts"):
        m2.sync.config["services"][s]["source"] = "sync:google"
    m2.perms.grant("ingest", "user", scopes=["correspondence", "calendar", "contacts"], sources=["sync:google"],
                   sensitivity_max="high")
    from sync_env import connect_google
    connect_google(m2, m2.sync.http.transport)
    for s in ("google_gmail", "google_calendar", "google_contacts"):
        assert m2.sync.sync(s, actor="user")["ok"], s
    m2.sync.config["services"]["github"]["source"] = "github"  # must start with sync:
    with pytest.raises(ValueError):
        m2.sync.source("github")

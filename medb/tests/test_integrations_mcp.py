"""D-74: MCP bridge (stdio JSON-RPC -> loopback API as a configured token actor)."""
import io
import json
import threading

import pytest

from conftest import appointer_config, change
from medb.api import make_server
from medb.integrations import mcp_server, mcp_tools
from medb.integrations.mcp_server import McpServer, http_call
from medb.interfaces import interface_inventory
from medb.system import MedB
from medb.util import FixedClock
from test_app_api import call

TOK = {"tok-user": "user", "tok-reader": "reader", "tok-agent": "agent:assistant", "tok-inf": "inference:assistant",
       "tok-coder": "agent:coder"}
USER_ONLY_TOOLS = ("assert", "confirm", "reject", "grant", "resolve", "withdraw", "import", "delete", "correct",
                   "revoke", "disavow", "supersede")


def mcp_cfg(port, **over):
    c = {"enabled": True, "actor": "agent:assistant", "inference_actor": "inference:assistant",
         "api_url": f"http://127.0.0.1:{port}", "tools": None}
    c.update(over)
    return c


@pytest.fixture
def mm(appointer_key_file):
    cfg = appointer_config(appointer_key_file)
    cfg["integrations"]["mcp"].update(enabled=True)
    cfg["integrations"]["outbox"].update(enabled=True)
    m = MedB(clock=FixedClock("2026-09-20T00:00:00Z"), seed=11, config=cfg)
    m.perms.grant("use", "user", scopes=["health"], purposes=["clinic-visit"], sensitivity_max="high")
    m.perms.grant("infer", "user", scopes=["health"], sensitivity_max="high")
    return m


@pytest.fixture
def api(mm):
    s = make_server(mm, TOK, port=0)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    yield s.server_port
    s.shutdown()
    s.server_close()


@pytest.fixture
def server(api):
    return McpServer(mcp_cfg(api), {"actor": "tok-agent", "inference_actor": "tok-inf"})


def rpc(srv, method, params=None, mid=1):
    return srv.handle({"jsonrpc": "2.0", "id": mid, "method": method, "params": params or {}})


def tool(srv, name, args=None):
    r = rpc(srv, "tools/call", {"name": name, "arguments": args or {}})
    if "error" in r:
        return None, r["error"]
    out = json.loads(r["result"]["content"][0]["text"])
    return out["status"], out.get("result", out.get("error"))


def test_tool_set_has_no_user_only_operations():
    names = set(mcp_tools.TOOLS)
    assert names == {f"medb_q1_{q}" for q in ("actions_in_window", "authorizing_clause", "context_packages_issued",
                                              "claims_retrieved", "cumulative_effect", "policy_current",
                                              "governance_log", "self_description")} | {
        "medb_build_context_package", "medb_propose_inference", "medb_submit_delegation_action",
        "medb_list_open_escalations"}
    for n in names:
        assert not any(w in n for w in USER_ONLY_TOOLS), n


@pytest.mark.parametrize("actor,ok", [("agent:assistant", True), ("user", False), ("reader", False),
                                      ("system", False), ("auditor:t1", False), ("inference:x", False),
                                      ("appointer:x", False), ("environment", False), (None, False)])
def test_config_actor_must_be_agent(actor, ok):
    assert (mcp_tools.validate_config({"actor": actor, "inference_actor": None}) == []) is ok


def test_config_inference_actor(monkeypatch):
    assert mcp_tools.validate_config({"actor": "agent:a", "inference_actor": "user"})
    assert mcp_tools.validate_config({"actor": "agent:a", "inference_actor": "agent:b"})
    assert mcp_tools.validate_config({"actor": "agent:a", "inference_actor": "inference:b"}) == []


def test_server_refuses_to_start_when_disabled_or_misconfigured(tmp_path, capsys):
    assert mcp_server.main(["--config", str(tmp_path / "none.json")]) == 2  # default: off
    assert "disabled" in capsys.readouterr().err
    p = tmp_path / "i.json"
    p.write_text(json.dumps({"integrations": {"mcp": {"enabled": True, "actor": "user"}}}))
    assert mcp_server.main(["--config", str(p)]) == 2
    assert "agent:*" in capsys.readouterr().err
    p.write_text(json.dumps({"integrations": {"mcp": {"enabled": True, "api_url": "http://example.org:80"}}}))
    assert mcp_server.main(["--config", str(p)]) == 2


def test_transport_refuses_non_loopback():
    with pytest.raises(mcp_server.McpError):
        http_call("http://example.org", "GET", "/api/q1/policy_current", "t", "medb_q1_policy_current")


def test_initialize_and_list(server):
    r = rpc(server, "initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "t"}})
    assert r["result"]["protocolVersion"] == "2025-06-18" and "tools" in r["result"]["capabilities"]
    assert server.handle({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None
    tools = rpc(server, "tools/list")["result"]["tools"]
    assert len(tools) == 12 and all("inputSchema" in t for t in tools)
    assert rpc(server, "nope")["error"]["code"] == -32601
    assert rpc(server, "ping")["result"] == {}


def test_q1_and_escalations_via_mcp(server, mm, api):
    st, r = tool(server, "medb_q1_self_description")
    assert st == 200 and r["integrations"]["mcp"]["enabled"] is True
    mm.delegation.grant("agent:assistant", "user")
    st, r = tool(server, "medb_submit_delegation_action",
                 {"kind": "code_change", "changes": [{"path": "src/auth/x.py", "lines": 3}]})
    assert st == 200 and r["decision"] == "REQUIRES_ESCALATION"
    st, r = tool(server, "medb_list_open_escalations")
    assert st == 200 and [e["escalation_id"] for e in r["open"]] == [r0["escalation_id"] for r0 in r["open"]]
    assert len(r["open"]) == 1 and r["open"][0]["action"]["agent"] == "agent:assistant"
    calls = mm.mcp_activity.recent()
    assert [c["tool"] for c in calls][:3] == ["medb_list_open_escalations", "medb_submit_delegation_action",
                                              "medb_q1_self_description"]
    assert all(c["actor"] == "agent:assistant" for c in calls) and mm.store.verify("integration_activity")["ok"]
    # outbox notified the escalation (derived after the capability call)
    assert "ESCALATION_OPENED" in {n["event"] for n in mm.outbox.feed()["notifications"]}


def test_agent_cannot_be_chosen_by_caller(server, mm):
    _, err = tool(server, "medb_submit_delegation_action", {"kind": "code_change", "agent": "user"})
    assert err["code"] == -32602 and "unexpected" in err["message"]
    st, r = tool(server, "medb_submit_delegation_action", {"kind": "code_change", "changes": []})
    ev = mm.gov.entries(kinds=["ACTION_EVALUATED"])[-1]
    assert ev["body"]["action"]["agent"] == "agent:assistant"


def test_propose_inference_stays_unconfirmed(server, mm):
    c = mm.claims.assert_claim("user", "has", "asthma", scope="health")
    st, r = tool(server, "medb_propose_inference", {"subject": "user", "predicate": "carries", "object": "inhaler",
                                                     "scope": "health", "derived_from": [c]})
    assert st == 200
    cl = mm.claims.current()[r["claim_id"]]
    assert (cl["origin"], cl["confirmation"]) == ("inference", "unconfirmed")
    assert mm.claims.history(r["claim_id"])[0]["actor"] == "inference:assistant"
    # closure still applies: no grant over 'authority' scope
    st, r = tool(server, "medb_propose_inference", {"subject": "user", "predicate": "decides", "object": "x",
                                                     "scope": "authority", "derived_from": [c]})
    assert st == 403


def test_context_package_via_mcp(server, mm):
    mm.claims.assert_claim("user", "has", "asthma", scope="health")
    st, r = tool(server, "medb_build_context_package", {"purpose": "clinic-visit"})
    assert st == 200 and r["issuance_record"]["body"]["requester"] == "agent:assistant" and len(r["package"]["claims"]) == 1
    st, r = tool(server, "medb_build_context_package", {"purpose": "marketing"})
    assert st == 200 and r["package"]["claims"] == []  # no use grant for that purpose: nothing released


def test_agent_token_cannot_reach_user_only_routes_even_by_hand(api, mm):
    """Even bypassing the tool table and the MCP server, the configured actor's token
    cannot assert self-accounts, confirm, grant or resolve escalations."""
    base = f"http://127.0.0.1:{api}"
    c = mm.claims.assert_claim("user", "has", "asthma", scope="health")
    p = mm.claims.propose("user", "carries", "inhaler", scope="health", derived_from=[c], actor="inference:x")
    for path, body in (("/api/ingest/claim", {"subject": "user", "predicate": "is", "object": "x", "scope": "health"}),
                       ("/api/claims/confirm", {"claim_id": p}),
                       ("/api/permissions/grant", {"operation": "use", "scopes": ["*"]}),
                       ("/api/escalations/resolve", {"escalation_id": "esc-x", "approve": True}),
                       ("/api/delegation/grant", {"delegate": "agent:other"}),
                       ("/api/import/file", {"path": "x.md"})):
        for tok in ("tok-agent", "tok-inf"):
            st, r = call(base, path, token=tok, body=body)
            assert st in (403, 404), (path, tok, st, r)
    assert mm.claims.current()[p]["confirmation"] == "unconfirmed"
    assert all(e["actor"] == "user" for e in mm.store.events("claims") if e["kind"] in ("ASSERT", "CONFIRM"))
    assert not mm.gov.entries(kinds=["ESCALATION_RESOLVED"])
    assert all(e["actor"] == "user" for e in mm.store.events("permissions"))


def _raw(base, path, tok, tool_name, body=None, method=None):
    import urllib.request
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(base + path, data=data, method=method or ("POST" if data else "GET"))
    req.add_header("Authorization", f"Bearer {tok}")
    req.add_header("X-MedB-Via", "mcp")
    req.add_header("X-MedB-MCP-Tool", tool_name)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def test_api_side_mcp_checks(api, mm):
    base = f"http://127.0.0.1:{api}"
    # wrong actor for the tool (user token carried as MCP) -> refused and logged
    st, r = _raw(base, "/api/q1/policy_current", "tok-user", "medb_q1_policy_current")
    assert st == 403 and mm.gov.entries(kinds=["PROHIBITED_ATTEMPT"])[-1]["body"]["reason"] == "mcp_actor_mismatch"
    # a tool name that does not belong to this route
    st, r = _raw(base, "/api/ingest/claim", "tok-agent", "medb_q1_policy_current",
                 {"subject": "user", "predicate": "is", "object": "x", "scope": "health"})
    assert st == 403 and mm.gov.entries(kinds=["PROHIBITED_ATTEMPT"])[-1]["body"]["reason"] == "mcp_unknown_tool_route"
    # inference actor cannot carry the agent's tools
    st, _ = _raw(base, "/api/delegation/evaluate", "tok-inf", "medb_submit_delegation_action",
                 {"agent": "inference:assistant", "kind": "code_change"})
    assert st == 403


def test_mcp_disabled_on_api_side(appointer_key_file):
    m = MedB(clock=FixedClock("2026-09-20T00:00:00Z"), seed=11, config=appointer_config(appointer_key_file))
    s = make_server(m, TOK, port=0)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    try:
        srv = McpServer(mcp_cfg(s.server_port), {"actor": "tok-agent", "inference_actor": "tok-inf"})
        st, r = tool(srv, "medb_q1_policy_current")
        assert st == 403 and r["error"] == "integration_disabled"
        assert m.gov.entries(kinds=["PROHIBITED_ATTEMPT"])[-1]["body"]["reason"] == "mcp_integration_disabled"
        assert "integration_activity" not in m.store.streams()
    finally:
        s.shutdown()
        s.server_close()


def test_suspension_423_through_mcp(server, mm):
    mm.delegation.grant("agent:assistant", "user")
    mm.suspensions.suspend("integrations.mcp", "t", "UNDETERMINED", [], ["x"])
    st, r = tool(server, "medb_submit_delegation_action", {"kind": "code_change", "changes": []})
    assert st == 423 and r["error"] == "capability_suspended"
    assert not mm.gov.entries(kinds=["ACTION_EVALUATED"])
    st, _ = tool(server, "medb_q1_policy_current")  # audit plane stays open (D-11/F-11)
    assert st == 200


def test_primitive_suspension_423_through_mcp(server, mm):
    mm.delegation.grant("agent:assistant", "user")
    mm.suspensions.suspend("delegation.execution", "t", "UNDETERMINED", [], ["x"])
    st, r = tool(server, "medb_submit_delegation_action", {"kind": "code_change", "changes": []})
    assert st == 423
    mm.suspensions.suspend("context.build", "t", "UNDETERMINED", [], ["x"])
    st, _ = tool(server, "medb_build_context_package", {"purpose": "clinic-visit"})
    assert st == 423
    rec = [c for c in mm.mcp_activity.recent() if c["tool"] == "medb_build_context_package"][0]
    assert rec["status"] == 423


def test_stdio_loop(server):
    inp = io.StringIO("\n".join([
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05"}}),
        json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}),
        "not json",
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "medb_q1_policy_current"}}),
        json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "medb_assert_claim"}}),
    ]) + "\n")
    out = io.StringIO()
    server.serve(inp, out)
    lines = [json.loads(x) for x in out.getvalue().splitlines()]
    assert [x.get("id") for x in lines] == [1, None, 2, 3]
    assert lines[0]["result"]["protocolVersion"] == "2024-11-05"
    assert lines[1]["error"]["code"] == -32700
    assert lines[2]["result"]["isError"] is False
    assert lines[3]["error"]["code"] == -32602
    assert "tok-agent" not in out.getvalue()  # the token never appears in output


def test_tools_registered_in_inventory(api):
    inv = interface_inventory()
    ext = inv["external_interfaces"]
    assert len([k for k in ext if k.startswith("MCP tool ")]) == 12
    for name, t in mcp_tools.TOOLS.items():
        e = ext[f"MCP tool {name}"]
        assert e["via"] in inv["routes"], e  # carried over a registered route
        assert "integrations.mcp" in e["primitives"]
        for p in e["primitives"]:
            assert f"MCP tool {name}" in inv["primitives"][p]["interfaces"]
        assert inv["routes"][e["via"]]["plane"] == t["plane"]

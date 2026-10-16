"""MedB MCP server: stdio JSON-RPC 2.0, stdlib only (DECISIONS D-74; off by default).

    python3 -m medb.integrations.mcp_server [--config data/integrations.json] [--tokens data/api_tokens.json]

Speaks the Model Context Protocol over stdio (one JSON-RPC message per line).
It holds **no database handle**: each ``tools/call`` becomes exactly one HTTP
request to the local MedB API (``config.integrations.mcp.api_url``, which must
be ``http://127.0.0.1:<port>``), authenticated with the bearer token of the
configured actor (``agent:*`` by default; ``inference:*`` for the propose
tool). The API then applies its normal rules: authentication, primitive-level
suspension checks (423), user-only operations (403), governance logging, plus
an MCP-specific check that the integration is enabled and the actor is the
configured one. So an assistant connected through MCP can never assert a user
self-account, confirm, grant, or resolve an escalation -- there is no tool for
those, and the token's actor could not do them anyway.

The token is read from ``MEDB_MCP_TOKEN`` / ``MEDB_MCP_INFERENCE_TOKEN`` or from
the API token file entry for the configured actor. It is never written to
stdout or into tool results.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode, urlparse

from .mcp_tools import TOOLS, validate_config

PROTOCOL_VERSIONS = ("2025-06-18", "2025-03-26", "2024-11-05")
SERVER_INFO = {"name": "medb", "version": "0.1.0-m0"}
LOOPBACK_HOSTS = ("127.0.0.1", "::1")
NETWORK_DECLARATION = {
    "direction": "loopback",
    "purpose": "MCP bridge (D-74): stdio JSON-RPC to the assistant; one HTTP request per tool call to the local "
               "MedB API, with the configured actor's bearer token",
    "protocol": "MCP over stdio; HTTP (stdlib http.client) to the MedB API",
    "allowed_hosts": list(LOOPBACK_HOSTS),
    "default_enabled": False,
    "sends_content": False,
    "outbound": False,
}


class McpError(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code


def _loopback(url: str) -> bool:
    u = urlparse(url or "")
    return u.scheme == "http" and u.hostname in LOOPBACK_HOSTS


def http_call(api_url: str, method: str, path: str, token: str, tool: str, query=None, body=None, timeout=30):
    if not _loopback(api_url):
        raise McpError(-32001, "api_url must be http://127.0.0.1:<port> (MedB is local-only)")
    import http.client
    u = urlparse(api_url)
    conn = http.client.HTTPConnection(u.hostname, u.port or 80, timeout=timeout)
    full = path + ("?" + urlencode(query) if query else "")
    data = json.dumps(body).encode() if body is not None else None
    hdr = {"Authorization": f"Bearer {token}", "X-MedB-Via": "mcp", "X-MedB-MCP-Tool": tool,
           "Content-Type": "application/json"}
    try:
        conn.request(method, full, body=data, headers=hdr)
        r = conn.getresponse()
        raw = r.read()
        try:
            return r.status, json.loads(raw or b"{}")
        except ValueError:
            return r.status, {"raw": raw[:2000].decode("utf-8", "replace")}
    finally:
        conn.close()


class McpServer:
    def __init__(self, cfg: dict, tokens: dict[str, str], transport=http_call):
        self.cfg = cfg
        self.tokens = tokens  # role ("actor" / "inference_actor") -> token
        self.transport = transport
        self.initialized = False

    def tool_list(self) -> list[dict]:
        allowed = set(self.cfg.get("tools") or TOOLS)
        out = []
        for name, t in TOOLS.items():
            if name not in allowed or (t["actor"] == "inference_actor" and not self.cfg.get("inference_actor")):
                continue
            out.append({"name": name, "description": t["description"], "inputSchema": t["inputSchema"]})
        return out

    def call_tool(self, name: str, args: dict) -> dict:
        if name not in {t["name"] for t in self.tool_list()}:
            raise McpError(-32602, f"unknown tool {name!r}")
        t = TOOLS[name]
        args = dict(args or {})
        props = t["inputSchema"]["properties"]
        extra = sorted(set(args) - set(props))
        if extra:
            raise McpError(-32602, f"unexpected arguments: {', '.join(extra)}")
        missing = [k for k in t["inputSchema"]["required"] if args.get(k) in (None, "")]
        if missing:
            raise McpError(-32602, f"missing arguments: {', '.join(missing)}")
        role = t["actor"]
        token = self.tokens.get(role)
        if not token:
            raise McpError(-32002, f"no API token for the configured {role}")
        if name == "medb_submit_delegation_action":
            args["agent"] = self.cfg["actor"]  # never caller-chosen
        query = body = None
        if t["method"] == "GET":
            query = {k: v for k, v in args.items() if v not in (None, "")}
        else:
            body = args
        status, payload = self.transport(self.cfg["api_url"], t["method"], t["path"], token, name, query=query, body=body)
        if name == "medb_list_open_escalations" and status == 200:
            payload = {"open": [e for e in payload.get("escalations", []) if e.get("status") == "OPEN"]}
        ok = 200 <= status < 300
        return {"content": [{"type": "text", "text": json.dumps({"status": status, "result" if ok else "error": payload},
                                                                 indent=1, sort_keys=True)}],
                "isError": not ok}

    def handle(self, msg: dict) -> dict | None:
        mid, method, params = msg.get("id"), msg.get("method"), msg.get("params") or {}
        is_note = "id" not in msg
        try:
            if msg.get("jsonrpc") != "2.0" or not isinstance(method, str):
                raise McpError(-32600, "invalid request")
            if method == "initialize":
                v = params.get("protocolVersion")
                result = {"protocolVersion": v if v in PROTOCOL_VERSIONS else PROTOCOL_VERSIONS[0],
                          "capabilities": {"tools": {"listChanged": False}}, "serverInfo": SERVER_INFO,
                          "instructions": "MedB tools act as the configured agent/inference actor. User-only "
                                          "operations (self-accounts, confirmations, grants, escalation decisions) "
                                          "are not available here."}
            elif method in ("notifications/initialized", "initialized"):
                self.initialized = True
                return None
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": self.tool_list()}
            elif method == "tools/call":
                result = self.call_tool(params.get("name"), params.get("arguments") or {})
            elif method.startswith("notifications/"):
                return None
            else:
                raise McpError(-32601, f"method not found: {method}")
        except McpError as e:
            return None if is_note else {"jsonrpc": "2.0", "id": mid, "error": {"code": e.code, "message": str(e)}}
        except Exception as e:  # transport failure etc.: report, never crash the session
            return None if is_note else {"jsonrpc": "2.0", "id": mid,
                                         "error": {"code": -32603, "message": f"{type(e).__name__}: {e}"[:300]}}
        return None if is_note else {"jsonrpc": "2.0", "id": mid, "result": result}

    def serve(self, inp=sys.stdin, out=sys.stdout):
        for line in inp:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except ValueError:
                resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}
            else:
                if isinstance(msg, list):  # batch
                    resp = [r for r in (self.handle(x) for x in msg if isinstance(x, dict)) if r is not None] or None
                else:
                    resp = self.handle(msg) if isinstance(msg, dict) else \
                        {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "invalid request"}}
            if resp is not None:
                out.write(json.dumps(resp) + "\n")
                out.flush()


def load_mcp_config(config_path: str | None = None) -> dict:
    from ..system import ROOT, load_config
    over = {}
    p = Path(config_path) if config_path else ROOT / "data" / "integrations.json"
    if p.exists():
        over = json.loads(p.read_text())
    return load_config(overrides=over).get("integrations", {}).get("mcp", {})


def main(argv=None) -> int:
    from ..system import ROOT
    ap = argparse.ArgumentParser(description="MedB MCP server (stdio)")
    ap.add_argument("--config", default=None, help="integrations override file (default data/integrations.json)")
    ap.add_argument("--tokens", default=str(ROOT / "data" / "api_tokens.json"))
    a = ap.parse_args(argv)
    cfg = load_mcp_config(a.config)
    if not cfg.get("enabled"):
        sys.stderr.write("MedB MCP integration is disabled (config.integrations.mcp.enabled is false; D-74)\n")
        return 2
    errs = validate_config(cfg)
    if not _loopback(cfg.get("api_url", "")):
        errs.append("mcp.api_url must be http://127.0.0.1:<port>")
    if errs:
        sys.stderr.write("MedB MCP configuration refused:\n  " + "\n  ".join(errs) + "\n")
        return 2
    by_actor = json.loads(Path(a.tokens).read_text()) if Path(a.tokens).exists() else {}
    tokens = {"actor": os.environ.get("MEDB_MCP_TOKEN") or by_actor.get(cfg["actor"])}
    if cfg.get("inference_actor"):
        tokens["inference_actor"] = os.environ.get("MEDB_MCP_INFERENCE_TOKEN") or by_actor.get(cfg["inference_actor"])
    if not tokens["actor"]:
        sys.stderr.write(f"no API token for {cfg['actor']}: start the API once with MCP enabled to issue it\n")
        return 2
    McpServer(cfg, tokens).serve()
    return 0


if __name__ == "__main__":
    sys.exit(main())

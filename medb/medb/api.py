"""Local HTTP API for MedB M0 (stdlib ``http.server``; loopback only).

Routes (every one is registered in ``interface_inventory()["routes"]``, and
routes that reach a primitive are also listed under that primitive):

    GET  /                               redirect to the app at /app/ (static; the D-61 read-only viewer was removed, D-70)
    GET  /api/q1/<query>                 exactly the eight Q-1 queries (audit plane)
    GET  /api/view/claims?as_of=         claim ledger state, current or as-of (claims.ledger; logged retrieval)
    GET  /api/view/claim_history?claim_id=   transitions of one claim (claims.ledger; logged retrieval)
    GET  /api/view/suspensions           suspension registry (audit plane)
    GET  /api/inventory                  interface inventory (audit plane)
    POST /api/ingest/corpus              authorised corpus ingest (corpus.ingest, permissions.closure)
    POST /api/ingest/claim               user self-account (claims.ledger)
    POST /api/delegation/evaluate        evaluate (and record) a proposed agent action (delegation.*)

Every route handler is guarded at the *primitive* level by the same
suspension registry the in-process interfaces use, and then calls those same
in-process interfaces (which check again). An API route therefore cannot
reach a suspended capability.

Authentication: bearer tokens from a local token file (``data/api_tokens.json``,
mode 0600), each bound to one actor. ``reader`` may only GET. ``auditor:<id>``
tokens may use only audit-plane, meta and auditor routes (D-69), and act as
auditors only while the independent appointer's appointment is active.

Run:  python3 -m medb.api            (then open the printed http://127.0.0.1:8765/app/#token=... URL)
"""
from __future__ import annotations

import argparse
import functools
import json
import os
import secrets
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .errors import (CapabilitySuspended, ConstitutionalProhibition, NotAuthorized, PermissionDenied,
                     SuspensionNotLiftable, UnknownClaim)
from .interfaces import interface_inventory, register_route
from .query import Q1_QUERIES

LOOPBACK = ("127.0.0.1",)
# Machine-readable network declaration, read by ``self_description`` (medb.netscan, D-68).
NETWORK_DECLARATION = {
    "direction": "inbound",
    "purpose": "local HTTP API / UI server (D-55); started only by `python -m medb.api` or make_server",
    "protocol": "HTTP (stdlib http.server), bearer-token auth",
    "bind_hosts": list(LOOPBACK),
    "outbound": False,
}
MAX_BODY = 1 << 20
CSP = ("default-src 'self'; connect-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; "
       "object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'")


class ApiError(Exception):
    def __init__(self, status: int, error: str, detail: str = "", **extra):
        super().__init__(detail)
        self.status, self.error, self.detail, self.extra = status, error, detail, extra


ROUTES: dict[tuple[str, str], tuple] = {}
STATIC_ROUTES: set[str] = set()  # unauthenticated static files (plane="static")


def route(method: str, path: str, primitives: tuple[str, ...] = (), plane: str = "capability", write: bool = False):
    def deco(fn):
        name = register_route(method, path, primitives, plane, f"MedBApi.{fn.__name__}")
        if plane == "static":
            STATIC_ROUTES.add(name)

        @functools.wraps(fn)
        def wrapper(self, actor, query, body):
            if plane == "capability" and primitives:
                self.m.suspensions.check(primitives, name)  # primitive-level guard, before anything else
            if plane == "audit":
                with self.m.suspensions.audit_read(name, primitives, actor):  # F-11 auditlog
                    return fn(self, actor, query, body)
            return fn(self, actor, query, body)

        ROUTES[(method, path)] = (wrapper, write, name)
        return wrapper
    return deco


AUDITOR_ROUTES: set[str] = set()  # non-audit-plane routes an auditor token may also use


def auditor_may_use(name: str) -> bool:
    """Auditor tokens see evidence (audit plane) and record audit results; never capability routes."""
    from .interfaces import _ROUTES
    r = _ROUTES.get(name, {})
    return r.get("plane") in ("audit", "meta", "static") or name in AUDITOR_ROUTES


INFERENCE_ROUTES: set[str] = set()  # non-audit routes an inference:* token may use (D-74)


def inference_may_use(name: str) -> bool:
    from .interfaces import _ROUTES
    return _ROUTES.get(name, {}).get("plane") in ("audit", "meta", "static") or name in INFERENCE_ROUTES


def _q(query: dict, key: str, default=None):
    v = query.get(key)
    return v[0] if v else default


class MedBApi:
    def __init__(self, medb, tokens: dict[str, str]):
        self.m = medb
        self.tokens = dict(tokens)  # token -> actor

    # ------------------------------------------------------------- static
    @route("GET", "/", plane="static")
    def index(self, actor, query, body):
        """The read-only viewer (D-61) is superseded by the app (D-70): redirect.
        Browsers keep the URL fragment (#token=...) across the redirect."""
        return ("text/plain; charset=utf-8", b"MedB app: /app/\n", {"Location": "/app/"}, 302)

    # -------------------------------------------------------------- views
    @route("GET", "/api/view/claims", ("claims.ledger",))
    def view_claims(self, actor, query, body):
        as_of = _q(query, "as_of")
        st = self.m.claims.state(as_of=as_of or None)
        self.m.gov.record("CLAIMS_RETRIEVED", actor, purpose="ledger_inspection", claim_ids=sorted(st),
                          claim_event_hashes={k: v["event_hash"] for k, v in st.items()}, via="HTTP GET /api/view/claims",
                          as_of=as_of)
        return {"as_of": as_of, "now": self.m.clock.now_iso(), "count": len(st),
                "claims": [{k: v for k, v in c.items() if k != "content_ref"} for c in
                           sorted(st.values(), key=lambda c: c["created_at"])]}

    @route("GET", "/api/view/claim_history", ("claims.ledger",))
    def view_claim_history(self, actor, query, body):
        cid = _q(query, "claim_id")
        if not cid:
            raise ApiError(400, "bad_request", "claim_id required")
        hist = self.m.claims.history(cid)
        self.m.gov.record("CLAIMS_RETRIEVED", actor, purpose="ledger_inspection", claim_ids=[cid],
                          claim_event_hashes={}, via="HTTP GET /api/view/claim_history")
        return {"claim_id": cid, "transitions": hist}

    @route("GET", "/api/view/suspensions", ("governance.log",), plane="audit")
    def view_suspensions(self, actor, query, body):
        return {"records": self.m.suspensions.records(), "adjacent": self.m.suspensions.adjacent_flags()}

    @route("GET", "/api/inventory", plane="audit")
    def inventory(self, actor, query, body):
        return interface_inventory()

    # -------------------------------------------------------------- writes
    @route("POST", "/api/ingest/corpus", ("corpus.ingest", "permissions.closure"), write=True)
    def ingest_corpus(self, actor, query, body):
        return self.m.corpus.ingest(body["content"], source=body["source"], scope=body["scope"], actor=actor,
                                    sensitivity=body.get("sensitivity", "high"),
                                    media_type=body.get("media_type", "text/plain"))

    @route("POST", "/api/ingest/claim", ("claims.ledger",), write=True)
    def ingest_claim(self, actor, query, body):
        cid = self.m.claims.assert_claim(body["subject"], body["predicate"], body["object"], scope=body["scope"],
                                         actor=actor, source=body.get("source", "user:self-account"),
                                         sensitivity=body.get("sensitivity", "high"),
                                         temporal_validity=body.get("temporal_validity"),
                                         exposure_refs=body.get("exposure_refs"))
        return {"claim_id": cid}

    @route("POST", "/api/delegation/evaluate", ("delegation.evaluator", "delegation.execution"), write=True)
    def delegation_evaluate(self, actor, query, body):
        if body.get("agent") != actor:
            self.m.gov.record("PROHIBITED_ATTEMPT", actor, reason="api_action_agent_mismatch", claimed=body.get("agent"))
            raise ApiError(403, "not_authorized", "action.agent must be the authenticated actor")
        return self.m.delegation.submit(body)

    # ------------------------------------------------------------ dispatch
    def handle(self, method: str, raw_path: str, headers, body_bytes: bytes):
        u = urlparse(raw_path)
        path, query = u.path, parse_qs(u.query)
        if method == "GET" and path.startswith("/api/q1/"):
            qname = path[len("/api/q1/"):]
            if qname not in Q1_QUERIES:
                raise ApiError(404, "not_found", f"unknown Q-1 query {qname!r}")
            entry = ROUTES[("GET", f"/api/q1/{qname}")]
        else:
            entry = ROUTES.get((method, path))
            if entry is None:
                raise ApiError(404 if method in ("GET", "POST") else 405, "not_found", path)
        fn, write, name = entry
        actor = None
        if name not in STATIC_ROUTES:
            auth = headers.get("Authorization", "")
            tok = auth[7:] if auth.startswith("Bearer ") else None
            actor = self.tokens.get(tok) if tok else None
            if actor is None:
                raise ApiError(401, "unauthenticated", "Bearer token required")
            if write and actor == "reader":
                raise ApiError(403, "not_authorized", "reader token is read-only")
            if actor.startswith("auditor:") and not auditor_may_use(name):
                self.m.gov.record("PROHIBITED_ATTEMPT", actor, reason="auditor_outside_audit_plane", interface=name)
                raise ApiError(403, "not_authorized", "auditor tokens may use only audit-plane and auditor routes")
            if actor.startswith("inference:") and not inference_may_use(name):
                self.m.gov.record("PROHIBITED_ATTEMPT", actor, reason="inference_token_outside_propose", interface=name)
                raise ApiError(403, "not_authorized", "inference tokens may only propose inferences and read the audit plane")
        body = {}
        if method == "POST":
            try:
                body = json.loads(body_bytes or b"{}")
            except json.JSONDecodeError as e:
                raise ApiError(400, "bad_json", str(e))
        via = (headers.get("X-MedB-Via") or "").lower() if actor else ""
        if via == "mcp":
            return self._via_mcp(fn, name, method, path, actor, query, body, headers.get("X-MedB-MCP-Tool") or "")
        try:
            return fn(self, actor, query, body)
        finally:
            if write:
                self.sync_outbox()

    def sync_outbox(self):
        """Derive outbox notifications after a write (no-op while the outbox is off, D-73)."""
        if self.m.outbox.enabled:
            try:
                self.m.outbox.sync()
            except CapabilitySuspended:
                pass  # outbox suspended: notifications are derived later, nothing is lost (gov is the source)

    def _via_mcp(self, fn, name, method, path, actor, query, body, tool):
        """Requests carried by the MCP server (D-74): integration on, configured actor, known tool for this route,
        bridge not suspended (capability tools); recorded in ``integration_activity``."""
        from .integrations.mcp_tools import TOOLS
        cfg = self.m.config.get("integrations", {}).get("mcp", {})
        if not self.m.mcp_activity.enabled:
            self.m.gov.record("PROHIBITED_ATTEMPT", actor, reason="mcp_integration_disabled", interface=name)
            raise ApiError(403, "integration_disabled", "the MCP integration is off (config.integrations.mcp.enabled)")
        t = TOOLS.get(tool)
        if t is None or (t["method"], t["path"]) != (method, path):
            self.m.gov.record("PROHIBITED_ATTEMPT", actor, reason="mcp_unknown_tool_route", tool=tool, interface=name)
            raise ApiError(403, "not_authorized", "no MCP tool is carried over this route")
        if actor != cfg.get(t["actor"]):
            self.m.gov.record("PROHIBITED_ATTEMPT", actor, reason="mcp_actor_mismatch", tool=tool, interface=name)
            raise ApiError(403, "not_authorized", "MCP requests must use the configured MCP actor's token")
        status = 500
        try:
            if t["plane"] == "capability":
                self.m.suspensions.check(("integrations.mcp",), t["interface"])
            out = fn(self, actor, query, body)
            status = 200
            return out
        except ApiError as e:
            status = e.status
            raise
        except Exception as e:
            status = next((st for cls, st, _ in _ERRORS if isinstance(e, cls)), 500)
            raise
        finally:
            try:
                self.m.mcp_activity.record(tool, actor, name, status)
            except CapabilitySuspended:
                pass  # bridge suspended: the refusal itself is the record (SUSPENSION + 423)
            if t["plane"] == "capability":
                self.sync_outbox()


def _make_q1_route(qname: str):
    method_obj = getattr(__import__("medb.query", fromlist=["Q1"]).Q1, qname)
    prims = method_obj.__medb_reaches__

    def handler(self, actor, query, body):
        kw = {k: v[0] for k, v in query.items()}
        for k in ("start_seq", "end_seq"):
            if k in kw:
                kw[k] = int(kw[k])
        try:
            return getattr(self.m.q1, qname)(**kw)
        except TypeError as e:
            raise ApiError(400, "bad_request", str(e))
    handler.__name__ = f"q1_{qname}"
    route("GET", f"/api/q1/{qname}", prims, plane="audit")(handler)


for _q1 in Q1_QUERIES:
    _make_q1_route(_q1)

from .anchoring import AnchoringDisabled  # noqa: E402

_ERRORS = ((CapabilitySuspended, 423, "capability_suspended"), (NotAuthorized, 403, "not_authorized"),
           (PermissionDenied, 403, "permission_denied"), (ConstitutionalProhibition, 403, "constitutional_prohibition"),
           (SuspensionNotLiftable, 403, "not_liftable"), (UnknownClaim, 404, "unknown_claim"),
           (KeyError, 400, "missing_field"), (ValueError, 400, "bad_request"), (TypeError, 400, "bad_request"))


from .integrations.importers import ImportRefused, ImportsDisabled  # noqa: E402
from .integrations.livesync import SyncDisabled, SyncRefused  # noqa: E402
from .integrations.sync_http import HostNotAllowed, SyncHttpError  # noqa: E402

_ERRORS = ((AnchoringDisabled, 409, "anchoring_disabled"), (ImportsDisabled, 409, "integration_disabled"),
           (ImportRefused, 422, "import_refused"), (SyncDisabled, 409, "integration_disabled"),
           (SyncRefused, 422, "sync_refused"), (HostNotAllowed, 403, "host_not_allowed"),
           (SyncHttpError, 502, "upstream_error")) + _ERRORS


def make_handler(api: MedBApi):
    class Handler(BaseHTTPRequestHandler):
        server_version = "MedB-M0"

        def _send(self, status: int, payload, ctype="application/json", extra_headers=None):
            data = payload if isinstance(payload, bytes) else json.dumps(payload, indent=1, sort_keys=True).encode()
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            for k, v in (extra_headers or {}).items():
                self.send_header(k, v)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", CSP)
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("X-Frame-Options", "DENY")
            self.end_headers()
            self.wfile.write(data)

        def _do(self, method):
            try:
                n = int(self.headers.get("Content-Length") or 0)
                if n > MAX_BODY:
                    raise ApiError(413, "too_large")
                out = api.handle(method, self.path, self.headers, self.rfile.read(n) if n else b"")
                if isinstance(out, tuple):
                    self._send(out[3] if len(out) > 3 else 200, out[1], out[0], out[2] if len(out) > 2 else None)
                else:
                    self._send(200, out)
            except ApiError as e:
                self._send(e.status, {"error": e.error, "detail": e.detail, **e.extra})
            except Exception as e:  # map domain refusals onto HTTP
                for cls, status, code in _ERRORS:
                    if isinstance(e, cls):
                        extra = {"primitive": e.primitive, "suspension_record": e.record_id} \
                            if isinstance(e, CapabilitySuspended) else {}
                        self._send(status, {"error": code, "detail": str(e), **extra})
                        return
                self._send(500, {"error": "internal", "detail": type(e).__name__})

        def do_GET(self):
            self._do("GET")

        def do_POST(self):
            self._do("POST")

        def do_PUT(self):
            self._send(405, {"error": "method_not_allowed"})

        do_DELETE = do_PATCH = do_PUT

        def log_message(self, fmt, *args):  # no query strings / tokens in logs
            sys.stderr.write(f"{self.command} {urlparse(self.path).path} -> {args[1] if len(args) > 1 else ''}\n")

    return Handler


def load_tokens(path: Path, actors=("user", "reader", "agent:coder")) -> dict[str, str]:
    """Return {token: actor}. Creates the file (mode 0600) if absent; adds tokens for
    actors not yet in it (e.g. ``auditor:<id>``), never changing existing tokens."""
    if path.exists():
        by_actor = json.loads(path.read_text())
        missing = [a for a in actors if a not in by_actor]
        if missing:
            by_actor.update({a: secrets.token_urlsafe(24) for a in missing})
            tmp = path.with_name(path.name + ".tmp")
            fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "w") as f:
                json.dump(by_actor, f, indent=2)
            os.replace(tmp, path)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        by_actor = {a: secrets.token_urlsafe(24) for a in actors}
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w") as f:
            json.dump(by_actor, f, indent=2)
    return {tok: actor for actor, tok in by_actor.items()}


def enable_app() -> bool:
    """Register the interactive app's routes (``medb/api_app.py``, D-67).

    Done when a server is built, not at import: Round 1 subjects and envelopes
    (which import this module only for the inventory) never see the app, and
    the envelope source omits ``api_app.py``."""
    try:
        from . import api_app  # noqa: F401
        from . import api_integrations  # noqa: F401  (integrations routes, D-72..D-75)
    except ModuleNotFoundError as e:
        if e.name not in (f"{__package__}.api_app", f"{__package__}.api_integrations"):
            raise
        return False
    return True


def make_server(medb, tokens: dict[str, str], host: str = "127.0.0.1", port: int = 8765) -> HTTPServer:
    if host not in LOOPBACK:
        raise ValueError("MedB API binds to 127.0.0.1 only (local-first, Principle 8)")
    enable_app()
    return HTTPServer((host, port), make_handler(MedBApi(medb, tokens)))


def seed_demo(m) -> None:
    """Small demo dataset so the read-only UI has something to show."""
    if m.claims.state():
        return
    m.perms.grant("use", "user", scopes=["authority", "health"], purposes=["clinic-visit"], sensitivity_max="high", compose=True)
    m.perms.grant("infer", "user", scopes=["authority", "health"], sensitivity_max="high", compose=True)
    m.perms.grant("ingest", "user", scopes=["health"], sources=["clinic-letters"], sensitivity_max="high")
    a = m.claims.assert_claim("user", "decides", "my own treatment decisions", scope="authority", sensitivity="moderate")
    h = m.claims.assert_claim("user", "has", "asthma", scope="health")
    p = m.claims.propose("user", "decides", "the clinician should decide", scope="authority", derived_from=[a],
                         actor="inference:demo", sensitivity="moderate")
    m.claims.propose("user", "carries", "a reliever inhaler", scope="health", derived_from=[h], actor="inference:demo")
    m.claims.correct(a, object="my own treatment decisions, after hearing options")
    m.claims.reject(p, reason="not how I decide")
    d = m.claims.assert_claim("user", "diagnosis", "demo-deleted-content", scope="health")
    m.claims.delete(d)
    m.context.build("clinic-visit", "agent:clinic-assistant", predicates=["decides", "has", "carries"])
    m.delegation.grant("agent:coder", "user")
    m.delegation.submit({"agent": "agent:coder", "kind": "code_change", "changes": [{"path": "src/ui/a.py", "lines": 12}]})
    m.delegation.submit({"agent": "agent:coder", "kind": "code_change", "changes": [{"path": "src/auth/b.py", "lines": 3}]})


def main(argv=None):
    from .system import ROOT, MedB
    from .system import load_config
    ap = argparse.ArgumentParser(description="MedB M0 local API + interactive app (127.0.0.1 only)")
    ap.add_argument("--db", default=str(ROOT / "data" / "medb.sqlite"))
    ap.add_argument("--tokens", default=str(ROOT / "data" / "api_tokens.json"))
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--demo", action="store_true", help="seed a small demo dataset if the DB is empty")
    ap.add_argument("--appointer", default=str(ROOT / "data" / "appointer.json"),
                    help="deployment file {id, key_fingerprint, verify_key_file} for the independent appointer (D-69)")
    ap.add_argument("--auditor", action="append", default=None,
                    help="auditor id(s) to issue API tokens for (default auditor:external-1)")
    ap.add_argument("--integrations", default=str(ROOT / "data" / "integrations.json"),
                    help="local integrations override file (all integrations are off by default; D-72..D-75)")
    a = ap.parse_args(argv)
    Path(a.db).parent.mkdir(parents=True, exist_ok=True)
    over = {}
    if Path(a.appointer).exists():
        over["appointer"] = json.loads(Path(a.appointer).read_text())
    if Path(a.integrations).exists():
        over.update(json.loads(Path(a.integrations).read_text()))
    m = MedB(db_path=a.db, config=load_config(overrides=over))
    if a.demo:
        seed_demo(m)
    auditors = a.auditor or ["auditor:external-1"]
    extra = []
    if m.mcp_activity.enabled:  # tokens for the MCP actors only when the integration is on
        mcfg = m.config["integrations"]["mcp"]
        extra = [x for x in (mcfg.get("actor"), mcfg.get("inference_actor")) if x]
    tokens = load_tokens(Path(a.tokens), actors=("user", "reader", "agent:coder", *auditors, *extra))
    srv = make_server(m, tokens, a.host, a.port)
    print(f"MedB API on http://{a.host}:{srv.server_port}/  (tokens: {a.tokens})", flush=True)
    print(f"MedB app: http://{a.host}:{srv.server_port}/app/#token=<token>  "
          f"(user / reader / agent:coder / {' / '.join(auditors)} tokens in {a.tokens})", flush=True)
    b = m.auditors.binding()
    print(f"Appointer: {b['id'] + ' (' + b['source'] + ')' if b else 'none bound - no auditor can act (D-69)'}; "
          f"active auditors: {', '.join(m.auditors.active_auditors()) or 'none'}", flush=True)
    st = {k: v["enabled"] for k, v in __import__("medb.integrations", fromlist=["status"]).status(m).items()}
    print("Integrations: " + ", ".join(f"{k}={'on' if v else 'off'}" for k, v in st.items()), flush=True)
    try:
        serve(srv, m)
    except KeyboardInterrupt:
        pass


def serve(srv, m, ticks=None) -> None:
    """Serve requests. When the user turned on scheduled live sync (D-78; off by default) the server handles one
    request at a time and runs due syncs on this (the only) thread in between, as actor ``system`` acting on the
    user's standing configuration. ``ticks`` bounds the loop (tests)."""
    from .integrations.livesync import SyncScheduler
    sch = SyncScheduler(m.sync)
    if ticks is None and not (m.sync.enabled and (m.sync.config.get("schedule") or {}).get("enabled")):
        return srv.serve_forever()
    srv.timeout = 1 if ticks is not None else 30
    n = 0
    while ticks is None or n < ticks:
        srv.handle_request()
        if sch.tick() and m.outbox.enabled:
            try:
                m.outbox.sync()
            except CapabilitySuspended:
                pass
        n += 1


if __name__ == "__main__":
    # run from the canonical ``medb.api`` module, so routes registered by other modules
    # (``api_app`` imports ``medb.api``) land in the same ROUTES table that serves requests
    from medb.api import main as _main
    _main()

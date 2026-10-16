"""HTTP routes for the integrations layer (DECISIONS D-72..D-75).

Registered with the app routes when a server is built (``api.enable_app``), so
they are not part of Round 1 (D-67); the in-process entry points they call
(``Importer.import_file``, ``Outbox.sync``, ``McpActivity.record``) are
``@reaches`` interfaces and do appear in the in-process inventory.
"""
from __future__ import annotations

from .api import INFERENCE_ROUTES, ApiError, _q, route
from .api_app import CAN, _need, _user_only
from .errors import CapabilitySuspended
from .integrations import status as integrations_status
from .integrations.importers import FORMATS

CAN["user"].append("import")
CAN["inference:"] = ["propose"]


@route("GET", "/api/integrations/status", ("governance.log",), plane="audit")
def integrations_status_route(self, actor, query, body):
    return integrations_status(self.m)


@route("GET", "/api/view/outbox", ("integrations.outbox", "governance.log"), plane="audit")
def view_outbox(self, actor, query, body):
    if self.m.outbox.enabled:
        try:
            self.m.outbox.sync()
        except CapabilitySuspended:
            pass
    return self.m.outbox.feed(limit=int(_q(query, "limit", 200)))


@route("GET", "/api/view/mcp_activity", ("integrations.mcp",), plane="audit")
def view_mcp_activity(self, actor, query, body):
    return {"enabled": self.m.mcp_activity.enabled, "calls": self.m.mcp_activity.recent(int(_q(query, "limit", 50))),
            "verification": self.m.store.verify("integration_activity")}


@route("GET", "/api/view/import_runs", ("governance.log",), plane="audit")
def view_import_runs(self, actor, query, body):
    runs = [dict(e["body"], ts=e["ts"], kind=e["kind"], actor=e["actor"], seq=e["seq"])
            for e in self.m.gov.entries(kinds=["IMPORT_RUN", "IMPORT_REFUSED"])]
    return {"runs": list(reversed(runs))[:200]}


@route("GET", "/api/import/formats", plane="meta")
def import_formats(self, actor, query, body):
    return {"enabled": self.m.importer.enabled,
            "formats": [{"id": k, "label": v[0], "default_scope": v[1], "media_type": v[2], "export_kind": v[3],
                         "default_source": f"import:{k}"} for k, v in FORMATS.items()],
            "cookie_values_imported": False}


@route("GET", "/api/import/files", ("integrations.import",))
def import_files(self, actor, query, body):
    _user_only(self, actor, "import_listing")
    return {"enabled": self.m.importer.enabled, "roots": [str(r) for r in self.m.importer.roots()],
            "files": self.m.importer.list_files() if self.m.importer.enabled else []}


@route("POST", "/api/import/file", ("integrations.import", "corpus.ingest", "permissions.closure"), write=True)
def import_file(self, actor, query, body):
    _need(body, "path")
    return self.m.importer.import_file(body["path"], actor=actor, fmt=body.get("format") or None,
                                       scope=body.get("scope") or None, source=body.get("source") or None,
                                       sensitivity=body.get("sensitivity") or None, account=body.get("account") or None)


@route("POST", "/api/claims/propose", ("claims.inference_proposal", "permissions.closure"), write=True)
def claims_propose(self, actor, query, body):
    """Inference proposal (used by the MCP propose tool). The ledger requires an inference:* actor."""
    _need(body, "subject", "predicate", "object", "scope", "derived_from")
    if not isinstance(body["derived_from"], list):
        raise ApiError(400, "bad_request", "derived_from must be a list of claim ids")
    cid = self.m.claims.propose(body["subject"], body["predicate"], body["object"], scope=body["scope"],
                                derived_from=body["derived_from"], actor=actor,
                                sensitivity=body.get("sensitivity", "high"), rationale=body.get("rationale", ""))
    return {"claim_id": cid, "confirmation": "unconfirmed", "note": "awaits the user's review in MedB"}


INFERENCE_ROUTES.add("HTTP POST /api/claims/propose")


# ------------------------------------------------------------------ live account sync (D-76..D-78)
from .integrations.livesync import SERVICES  # noqa: E402

CAN["user"].append("sync")


def _service(body):
    _need(body, "service")
    if body["service"] not in SERVICES:
        raise ApiError(400, "bad_request", f"unknown service {body['service']!r}; one of {sorted(SERVICES)}")
    return body["service"]


@route("GET", "/api/sync/status", ("integrations.sync",), plane="audit")
def sync_status(self, actor, query, body):
    """Per-service status: enabled, connected, account id, scopes, hosts, last sync, item counts, errors. No secrets."""
    return integrations_status(self.m)["live_sync"]


@route("GET", "/api/view/sync_runs", ("integrations.sync",), plane="audit")
def view_sync_runs(self, actor, query, body):
    evs = [dict({k: v for k, v in e["body"].items() if k not in ("cursor_before", "cursor_after")},
                ts=e["ts"], kind=e["kind"], actor=e["actor"], seq=e["seq"]) for e in self.m.sync.events()]
    refused = [dict(e["body"], ts=e["ts"], kind=e["kind"], actor=e["actor"], seq=e["seq"])
               for e in self.m.gov.entries(kinds=["SYNC_REFUSED"])]
    return {"events": list(reversed(evs))[:int(_q(query, "limit", 200))], "refused": list(reversed(refused))[:50],
            "verification": self.m.store.verify("sync")}


@route("POST", "/api/sync/connect", ("integrations.sync",), write=True)
def sync_connect(self, actor, query, body):
    _user_only(self, actor, "sync_connect")
    return self.m.sync.connect(_service(body), actor=actor)


@route("POST", "/api/sync/connect_poll", ("integrations.sync",), write=True)
def sync_connect_poll(self, actor, query, body):
    _user_only(self, actor, "sync_connect")
    return self.m.sync.connect_poll(_service(body), actor=actor)


@route("POST", "/api/sync/run", ("integrations.sync", "corpus.ingest", "permissions.closure"), write=True)
def sync_run(self, actor, query, body):
    _user_only(self, actor, "sync_run")
    if body.get("all"):
        sm = self.m.sync
        out = []
        for s in SERVICES:
            if sm.service_enabled(s) and sm.connection(s) is not None:
                try:
                    out.append(sm.sync(s, actor=actor))
                except Exception as e:  # each refusal is logged by the primitive; report and continue
                    out.append({"service": s, "ok": False, "error": f"{type(e).__name__}: {e}"[:200]})
        return {"runs": out}
    return self.m.sync.sync(_service(body), actor=actor)


@route("POST", "/api/sync/disconnect", ("integrations.sync",), plane="revocation", write=True)
def sync_disconnect(self, actor, query, body):
    """Deletes the local token. Revocation plane: open while integrations.sync is suspended (it only removes capability)."""
    _user_only(self, actor, "sync_disconnect")
    return self.m.sync.disconnect(_service(body), actor=actor, remote_revoke=bool(body.get("remote_revoke")))

"""Integrations layer (DECISIONS D-72..D-75). Every integration is off by default
(``config.integrations``); every entry point is an ``@reaches`` interface or a
registered route / external interface, checked against the suspension registry,
and logged.

* ``importers``  -- user-only local file importers into the corpus (D-72)
* ``outbox``     -- local notification outbox + optional loopback webhook (D-73)
* ``mcp_tools`` / ``mcp_server`` -- MCP bridge for AI assistants (D-74)
* ``livesync`` (+ ``sync_http``, ``oauth``, ``sync_tokens``) -- user-only live account sync (D-76..D-78)
"""
from __future__ import annotations

from . import mcp_tools  # noqa: F401  (registers MCP tools in the interface inventory)
from .importers import FORMATS


def status(m) -> dict:
    """Generated status of every integration (for self_description and the app)."""
    cfg = m.config.get("integrations", {})
    mcp, imp, out = cfg.get("mcp", {}), cfg.get("importers", {}), cfg.get("outbox", {})
    return {
        "mcp": {"enabled": m.mcp_activity.enabled, "configured": bool(mcp.get("enabled")),
                "config_errors": mcp_tools.validate_config(mcp) if mcp else ["not configured"],
                "actor": mcp.get("actor"), "inference_actor": mcp.get("inference_actor"),
                "api_url": mcp.get("api_url"), "tools": sorted(mcp.get("tools") or mcp_tools.TOOLS),
                "last_activity": m.mcp_activity.last_activity()},
        "importers": {"enabled": m.importer.enabled, "actor": "user",
                      "allowed_roots": [str(r) for r in m.importer.roots()] if imp.get("enabled") else [],
                      "formats": sorted(imp.get("formats") or FORMATS),
                      "default_sensitivity": imp.get("default_sensitivity", "high"),
                      "last_activity": next((e["ts"] for e in reversed(m.gov.entries(kinds=["IMPORT_RUN"]))), None)},
        "outbox": {"enabled": m.outbox.enabled, "actor": "system", "events": list(out.get("events") or []),
                   "webhook": m.outbox.webhook(), "last_activity": m.outbox.last_activity()},
        "live_sync": _live_sync(m),
    }


def _live_sync(m) -> dict:
    """No secrets: services, connection flags, account ids, scopes, hosts, last runs."""
    from .sync_http import ALLOWED_HOSTS
    sm = m.sync
    svcs = sm.status()
    return {"enabled": sm.enabled and any(v["enabled"] for v in svcs.values()), "configured": sm.enabled,
            "actor": "user", "outbound_class": "live_sync", "https_only": True,
            "allowed_hosts": {k: list(v) for k, v in ALLOWED_HOSTS.items()}, "hosts_in_use": sm.hosts_in_use(),
            "schedule": {"enabled": bool((sm.config.get("schedule") or {}).get("enabled")) and sm.enabled,
                         "interval_minutes": (sm.config.get("schedule") or {}).get("interval_minutes")},
            "services": svcs,
            "last_activity": next((e["ts"] for e in reversed(sm.events(kinds=["RUN"]))), None)}

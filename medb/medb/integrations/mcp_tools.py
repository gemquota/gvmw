"""MCP tool table and the API-side MCP activity record (DECISIONS D-74).

The MCP server (``mcp_server.py``) is a separate stdio process. It holds no
database handle: every tool call is carried as one request to the local MedB
API (127.0.0.1) with the bearer token of the configured actor, so the API's
authentication, primitive-level suspension checks (423), actor rules and
governance logging apply unchanged. Each tool is registered in the interface
inventory (``external_interfaces``) under the primitives of the route that
carries it, plus ``integrations.mcp``.

There is deliberately **no** tool for asserting self-accounts, confirming,
rejecting, granting permissions or delegations, resolving escalations,
withdrawing corpus items or importing files: those are user-only, and the MCP
actor is never the user (refused at configuration).
"""
from __future__ import annotations

from ..interfaces import register_interface, reaches
from ..query import Q1

STREAM = "integration_activity"
FORBIDDEN_ACTORS = ("user", "reader", "system", "environment")
FORBIDDEN_PREFIXES = ("auditor:", "appointer:")

_Q1_ARGS = {
    "actions_in_window": {"start": "ISO time (optional)", "end": "ISO time (optional)"},
    "authorizing_clause": {"action_id": "action id (required)"},
    "context_packages_issued": {"start": "ISO time (optional)", "end": "ISO time (optional)"},
    "claims_retrieved": {"start": "ISO time (optional)", "end": "ISO time (optional)"},
    "cumulative_effect": {"at": "ISO time (optional)"},
    "policy_current": {},
    "governance_log": {"start_seq": "integer (optional)", "end_seq": "integer (optional)"},
    "self_description": {},
}


def _schema(props: dict, required=()) -> dict:
    return {"type": "object", "properties": props, "required": list(required), "additionalProperties": False}


TOOLS: dict[str, dict] = {}
for _q, _args in _Q1_ARGS.items():
    TOOLS[f"medb_q1_{_q}"] = {
        "description": f"MedB Q-1 audit query '{_q}' (read-only; audit plane).",
        "method": "GET", "path": f"/api/q1/{_q}", "plane": "audit", "actor": "actor",
        "primitives": tuple(getattr(Q1, _q).__medb_reaches__),
        "inputSchema": _schema({k: {"type": "integer" if "integer" in v else "string", "description": v}
                                for k, v in _args.items()},
                               [k for k, v in _args.items() if "required" in v]),
    }
TOOLS["medb_build_context_package"] = {
    "description": "Build an ephemeral, purpose-scoped MedB context package for this assistant (requires the user's "
                   "use grant for the purpose; logged as CONTEXT_PACKAGE_ISSUED).",
    "method": "POST", "path": "/api/context/build", "plane": "capability", "actor": "actor",
    "primitives": ("context.build", "claims.retrieval"),
    "inputSchema": _schema({"purpose": {"type": "string"}, "predicates": {"type": "array", "items": {"type": "string"}},
                            "scopes": {"type": "array", "items": {"type": "string"}}, "subject": {"type": "string"},
                            "ttl_minutes": {"type": "integer"}}, ["purpose"]),
}
TOOLS["medb_propose_inference"] = {
    "description": "Propose an inference (an unconfirmed claim derived from existing claims). It never becomes a "
                   "self-account unless the user confirms it in MedB. Requires the user's infer grant.",
    "method": "POST", "path": "/api/claims/propose", "plane": "capability", "actor": "inference_actor",
    "primitives": ("claims.inference_proposal", "permissions.closure"),
    "inputSchema": _schema({"subject": {"type": "string"}, "predicate": {"type": "string"}, "object": {"type": "string"},
                            "scope": {"type": "string"}, "derived_from": {"type": "array", "items": {"type": "string"}},
                            "sensitivity": {"type": "string"}, "rationale": {"type": "string"}},
                           ["subject", "predicate", "object", "scope", "derived_from"]),
}
TOOLS["medb_submit_delegation_action"] = {
    "description": "Submit a proposed action for P-1 delegation evaluation (recorded; may be authorized, escalated "
                   "to the user, or rejected). The action's agent is always this assistant's actor.",
    "method": "POST", "path": "/api/delegation/evaluate", "plane": "capability", "actor": "actor",
    "primitives": ("delegation.evaluator", "delegation.execution"),
    "inputSchema": _schema({"kind": {"type": "string"}, "changes": {"type": "array", "items": {"type": "object"}},
                            "matter": {"type": "string"}, "description": {"type": "string"},
                            "emergency": {"type": "boolean"}}, ["kind"]),
}
TOOLS["medb_list_open_escalations"] = {
    "description": "List escalations awaiting the user's decision (read-only; audit plane). Only the user can "
                   "resolve them, in MedB itself.",
    "method": "GET", "path": "/api/view/escalations", "plane": "audit", "actor": "actor",
    "primitives": ("governance.log",),
    "inputSchema": _schema({}),
}

for _name, _t in TOOLS.items():
    _t["interface"] = register_interface("MCP tool", _name, ("integrations.mcp",) + tuple(_t["primitives"]),
                                         _t["plane"], f"HTTP {_t['method']} {_t['path']}")


def tool_for_route(method: str, path: str) -> list[str]:
    return [n for n, t in TOOLS.items() if t["method"] == method and t["path"] == path]


def actor_allowed(actor) -> bool:
    return isinstance(actor, str) and ":" in actor and actor not in FORBIDDEN_ACTORS \
        and not actor.startswith(FORBIDDEN_PREFIXES)


def validate_config(cfg: dict) -> list[str]:
    """Problems with an MCP configuration (empty list = usable)."""
    errs = []
    a, ia = cfg.get("actor"), cfg.get("inference_actor")
    if not (actor_allowed(a) and a.startswith("agent:")):
        errs.append(f"mcp.actor must be an agent:* actor (got {a!r}); never user, reader, system or an auditor")
    if ia is not None and not (actor_allowed(ia) and ia.startswith("inference:")):
        errs.append(f"mcp.inference_actor must be an inference:* actor or null (got {ia!r})")
    return errs


class McpActivity:
    """API-side record of requests carried by the MCP server (hash-chained
    ``integration_activity`` stream; not cross-linked into gov, so Q-1 evidence
    is unperturbed). The governance effects of each call (ACTION_EVALUATED,
    CONTEXT_PACKAGE_ISSUED, PROPOSE, PROHIBITED_ATTEMPT...) are logged by the
    primitives as for any API call."""

    def __init__(self, store, clock, ids, config: dict, suspensions=None):
        self.store, self.clock, self.ids = store, clock, ids
        self.config = config or {}
        self._suspensions = suspensions

    @property
    def enabled(self) -> bool:
        return bool(self.config.get("enabled")) and not validate_config(self.config)

    @reaches("integrations.mcp")
    def record(self, tool: str, actor: str, interface: str, status: int) -> dict:
        return self.store.append(STREAM, "MCP_CALL", actor, {"tool": tool, "interface": interface, "status": status},
                                 self.clock.now_iso(), self.ids.new("mcp"))

    def recent(self, limit: int = 50) -> list[dict]:
        evs = self.store.events(STREAM)
        return [dict(e["body"], actor=e["actor"], at=e["ts"], seq=e["seq"]) for e in reversed(evs[-limit:])]

    def last_activity(self) -> str | None:
        evs = self.store.events(STREAM)
        return evs[-1]["ts"] if evs else None

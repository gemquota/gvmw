"""Primitive registry and interface inventory.

Suspension operates on *primitives* (mechanisms), never on interfaces. Every
public entry point that exercises a primitive is decorated with
``@reaches(...)``; the decorator (a) registers the interface in the
``interface_inventory`` and (b) refuses the call while any reached primitive is
suspended. The inventory is therefore derived from the code itself rather than
hand-maintained (Principle 13).

Audit-plane interfaces (Q-1 queries, export, integrity verification) are
registered with ``plane="audit"``: they *read records about* primitives and are
not blocked by suspension, because resolution of a suspension requires a
re-audit, which requires the evidence path to stay open (DECISIONS D-11).
While any suspension is active, each (outermost) audit-plane read is recorded
in the separate ``auditlog`` stream (F-11).
"""
from __future__ import annotations

import functools
from collections import defaultdict

PRIMITIVES: dict[str, dict] = {
    "governance.log": {"depends_on": [], "description": "hash-chained governance log"},
    "permissions.closure": {"depends_on": ["governance.log"], "description": "ingest/infer/model/use grants and derivation-path closure"},
    "corpus.ingest": {"depends_on": ["permissions.closure"], "description": "immutable corpus, explicit-auth ingest"},
    "claims.ledger": {"depends_on": ["governance.log"], "description": "append-only claim transitions"},
    "claims.inference_proposal": {"depends_on": ["claims.ledger", "permissions.closure"], "description": "inference may propose, never promote"},
    "claims.retrieval": {"depends_on": ["claims.ledger", "permissions.closure"], "description": "purpose-bound claim reads"},
    "identity.model": {"depends_on": ["claims.ledger"], "description": "user-confirmed claims view"},
    "normative.store": {"depends_on": ["governance.log"], "description": "user directives (escalation decisions), separate from claims (F-18)"},
    "authority.resolution": {"depends_on": ["normative.store"], "description": "present user authority over a matter"},
    "audit.appointment": {"depends_on": ["governance.log"], "description": "auditor appointments by the independent appointer's signed statements (F-04)"},
    "governance.anchoring": {"depends_on": ["governance.log"], "description": "optional external timestamp anchoring of stream heads (F-13)"},
    "context.ranking": {"depends_on": ["claims.retrieval"], "description": "presentation ordering of package contents"},
    "context.rendering": {"depends_on": ["claims.retrieval"], "description": "epistemic-status rendering of claims"},
    "context.build": {"depends_on": ["claims.retrieval", "context.ranking", "context.rendering"], "description": "ephemeral purpose-scoped packages"},
    "policy.store": {"depends_on": ["governance.log"], "description": "delegation policy and module classification"},
    "delegation.evaluator": {"depends_on": ["policy.store"], "description": "per-action and cumulative policy evaluation"},
    "delegation.execution": {"depends_on": ["delegation.evaluator", "authority.resolution"], "description": "recording and executing delegated actions"},
    "delegation.emergency": {"depends_on": ["delegation.execution"], "description": "P-1.6 emergency clause"},
    # integrations layer (D-72..D-74); every integration is off by default
    "integrations.import": {"depends_on": ["corpus.ingest"], "description": "user-only local file importers into the corpus"},
    "integrations.outbox": {"depends_on": ["governance.log"], "description": "local notification outbox (+ optional loopback webhook)"},
    "integrations.sync": {"depends_on": ["corpus.ingest"], "description": "user-only live account sync (OAuth read-only APIs + live local browser profiles) into the corpus"},
    "integrations.mcp": {"depends_on": ["governance.log"], "description": "MCP bridge for AI assistants (stdio server -> loopback API, token actor)"},
}

_INVENTORY: dict[str, set[str]] = defaultdict(set)
_PLANES: dict[str, str] = {}


def dependents(primitive: str) -> list[str]:
    return sorted(p for p, d in PRIMITIVES.items() if primitive in d["depends_on"])


def base_primitive(capability: str) -> str:
    """'authority.resolution:matter-x' -> 'authority.resolution'."""
    return capability.split(":", 1)[0]


_ROUTES: dict[str, dict] = {}


def register_route(method: str, path: str, primitives: tuple[str, ...], plane: str, handler: str) -> str:
    """Register an HTTP route in the inventory (also for routes reaching no primitive)."""
    name = f"HTTP {method} {path}"
    _ROUTES[name] = {"method": method, "path": path, "primitives": list(primitives), "plane": plane,
                     "handler": handler}
    for p in primitives:
        _INVENTORY[p].add(name)
        _PLANES[name] = plane
    return name


_EXTERNAL: dict[str, dict] = {}


def register_interface(kind: str, name: str, primitives: tuple[str, ...], plane: str, target: str) -> str:
    """Register a non-HTTP external entry point (e.g. an MCP tool) in the inventory.
    ``target`` names the HTTP route it is carried over, where the suspension check runs."""
    for p in primitives:
        if p not in PRIMITIVES:
            raise ValueError(f"unknown primitive {p}")
    iface = f"{kind} {name}"
    _EXTERNAL[iface] = {"kind": kind, "name": name, "primitives": list(primitives), "plane": plane, "via": target}
    for p in primitives:
        _INVENTORY[p].add(iface)
    _PLANES[iface] = plane
    return iface


def reaches(*primitives: str, plane: str = "capability", name: str | None = None):
    for p in primitives:
        if p not in PRIMITIVES:
            raise ValueError(f"unknown primitive {p}")

    def deco(fn):
        iface = name or fn.__qualname__
        for p in primitives:
            _INVENTORY[p].add(iface)
        _PLANES[iface] = plane

        @functools.wraps(fn)
        def wrapper(self, *a, **kw):
            reg = getattr(self, "_suspensions", None)
            if reg is not None and plane == "capability":
                reg.check(primitives, iface)
            if reg is not None and plane == "audit" and hasattr(reg, "audit_read"):
                with reg.audit_read(iface, primitives, kw.get("actor")):
                    return fn(self, *a, **kw)
            return fn(self, *a, **kw)

        wrapper.__medb_reaches__ = primitives
        wrapper.__medb_plane__ = plane
        return wrapper

    return deco


def interface_inventory() -> dict:
    return {
        "primitives": {
            p: {
                "depends_on": PRIMITIVES[p]["depends_on"],
                "description": PRIMITIVES[p]["description"],
                "interfaces": sorted(_INVENTORY.get(p, ())),
                "interface_planes": {i: _PLANES[i] for i in sorted(_INVENTORY.get(p, ()))},
            }
            for p in sorted(PRIMITIVES)
        },
        "routes": {k: _ROUTES[k] for k in sorted(_ROUTES)},
        "external_interfaces": {k: _EXTERNAL[k] for k in sorted(_EXTERNAL)},
    }

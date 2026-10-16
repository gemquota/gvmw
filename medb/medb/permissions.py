"""Permissioned learning (Principle 6) and delegation default-deny substrate.

Four separate operations -- ingest, infer, model, use -- each needing its own
explicit, user-issued, revocable, optionally expiring grant. Nothing is
permitted without a grant (privacy by default, Principle 8).

Permission closure: an operation on a derived item is permitted only if one
grant covers *every* node on its full derivation path (the item and all of its
ancestors, transitively, including corpus items) -- the DLM-style "join of
labels over all inputs".

Composition Rule: authorized components do not authorize their composition.
Concretely (DECISIONS D-08): a composition is permitted only by a *single*
grant that covers all components jointly, and that grant must carry
``compose: true`` when the composition spans more than one input (infer) or
more than one scope (use).
"""
from __future__ import annotations

from .constitution import contains_prohibited_term
from .errors import ConstitutionalProhibition, NotAuthorized
from .govlog import GovernanceLog
from .interfaces import reaches
from .store import EventStore
from .util import Clock, IdGen, norm_ts

STREAM = "permissions"
OPERATIONS = ("ingest", "infer", "model", "use")
SENSITIVITY = ("low", "moderate", "high", "special")


def sens_rank(s: str) -> int:
    return SENSITIVITY.index(s)


class PermissionStore:
    def __init__(self, store: EventStore, gov: GovernanceLog, clock: Clock, ids: IdGen, suspensions=None):
        self.store, self.gov, self.clock, self.ids = store, gov, clock, ids
        self._suspensions = suspensions

    @reaches("permissions.closure")
    def grant(self, operation: str, actor: str, scopes: list[str], purposes: list[str] | None = None,
              sources: list[str] | None = None, sensitivity_max: str = "moderate", compose: bool = False,
              expires_at: str | None = None, note: str = "") -> dict:
        if actor != "user":
            self.gov.record("PROHIBITED_ATTEMPT", actor, reason="non_user_permission_grant", operation=operation)
            raise NotAuthorized("only the user can grant permissions (non-escalating authority)")
        if operation not in OPERATIONS:
            raise ValueError(operation)
        for p in purposes or []:
            term = contains_prohibited_term(p)
            if term:
                self.gov.record("PROHIBITED_ATTEMPT", actor, reason="prohibited_purpose", purpose=p, term=term)
                raise ConstitutionalProhibition(f"purpose {p!r} touches a permanent prohibition ({term})")
        sens_rank(sensitivity_max)
        body = {"grant_id": self.ids.new("grant"), "operation": operation, "scopes": list(scopes),
                "purposes": list(purposes or ["*"]) if operation == "use" else list(purposes or []),
                "sources": list(sources or []), "sensitivity_max": sensitivity_max, "compose": bool(compose),
                "expires_at": norm_ts(expires_at), "note": note}
        ev = self.store.append(STREAM, "GRANT", actor, body, self.clock.now_iso(), self.ids.new("pev"))
        self.gov.mirror(ev, actor, {"grant_id": body["grant_id"], "operation": operation})
        return body

    @reaches("permissions.closure")
    def revoke(self, grant_id: str, actor: str, reason: str = "") -> None:
        if actor != "user":
            self.gov.record("PROHIBITED_ATTEMPT", actor, reason="non_user_permission_revoke", grant_id=grant_id)
            raise NotAuthorized("only the user can revoke permissions")
        ev = self.store.append(STREAM, "REVOKE", actor, {"grant_id": grant_id, "reason": reason},
                               self.clock.now_iso(), self.ids.new("pev"))
        self.gov.mirror(ev, actor, {"grant_id": grant_id, "revoked": True})

    def grants(self, at: str | None = None) -> list[dict]:
        at = norm_ts(at) or self.clock.now_iso()
        gs: dict[str, dict] = {}
        for e in self.store.events(STREAM, until_ts=at):
            if e["kind"] == "GRANT":
                gs[e["body"]["grant_id"]] = dict(e["body"], granted_at=e["ts"], revoked_at=None)
            elif e["kind"] == "REVOKE" and e["body"]["grant_id"] in gs:
                gs[e["body"]["grant_id"]]["revoked_at"] = e["ts"]
        return list(gs.values())

    def active(self, operation: str, at: str | None = None) -> list[dict]:
        at = norm_ts(at) or self.clock.now_iso()
        return [g for g in self.grants(at) if g["operation"] == operation and g["revoked_at"] is None
                and (g["expires_at"] is None or g["expires_at"] > at)]

    @staticmethod
    def covers(grant: dict, node: dict) -> bool:
        if "*" not in grant["scopes"] and node["scope"] not in grant["scopes"]:
            return False
        return sens_rank(node["sensitivity"]) <= sens_rank(grant["sensitivity_max"])

    def covering(self, operation: str, nodes: list[dict], purpose: str | None = None,
                 source: str | None = None, at: str | None = None, composition: bool = False) -> list[dict]:
        """Active grants that jointly cover every node (permission closure)."""
        out = []
        for g in self.active(operation, at):
            if purpose is not None and "*" not in g["purposes"] and purpose not in g["purposes"]:
                continue
            if source is not None and "*" not in g["sources"] and source not in g["sources"]:
                continue
            if composition and not g["compose"]:
                continue
            if all(self.covers(g, n) for n in nodes):
                out.append(g)
        return sorted(out, key=lambda g: g["grant_id"])

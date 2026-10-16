"""Normative store (F-18, DECISIONS D-30).

User *directives* -- the positions the user states when resolving an
escalation -- are normative acts, not descriptive claims about the user, so
they are kept out of the claims ledger. Each directive is an event in the
separate hash-chained ``normative`` stream, cross-linked into ``gov`` with a
STATE_TRANSITION mirror (stream, seq, event_id, event_hash). Directives are
append-only; only the user can record one. They are not erasable content and
are never inputs to inference, identity modelling or context packages.
"""
from __future__ import annotations

from .errors import NotAuthorized
from .govlog import GovernanceLog
from .interfaces import reaches
from .store import EventStore
from .util import Clock, IdGen

STREAM = "normative"


class NormativeStore:
    def __init__(self, store: EventStore, gov: GovernanceLog, clock: Clock, ids: IdGen, suspensions=None):
        self.store, self.gov, self.clock, self.ids = store, gov, clock, ids
        self._suspensions = suspensions

    @reaches("normative.store")
    def record_directive(self, matter: str, position: str, actor: str = "user", priority=None,
                         statement: str | None = None, context: dict | None = None,
                         source: str = "user:escalation-response") -> str:
        if actor != "user":
            self.gov.record("PROHIBITED_ATTEMPT", actor, reason="non_user_directive", matter=matter)
            raise NotAuthorized("only the user records directives")
        did = self.ids.new("dir")
        body = {"directive_id": did, "matter": matter, "position": position, "priority": priority,
                "statement": statement, "source": source, "context": dict(context or {})}
        ev = self.store.append(STREAM, "DIRECTIVE", actor, body, self.clock.now_iso(), self.ids.new("nev"))
        self.gov.mirror(ev, actor, {"directive_id": did, "matter": matter, "position": position})
        return did

    def directives(self, matter: str | None = None, until_ts: str | None = None) -> list[dict]:
        out = []
        for e in self.store.events(STREAM, until_ts=until_ts):
            b = e["body"]
            if matter is None or b["matter"] == matter:
                out.append(dict(b, ts=e["ts"], seq=e["seq"], event_hash=e["hash"]))
        return out

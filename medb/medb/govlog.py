"""Governance log (Layer 6): retained indefinitely, hash-chained, append-only.

Records every action evaluation/execution, escalation, context package issue,
claim retrieval, policy change, suspension and audit-relevant state transition.
Entries never contain erasable claim content -- only identifiers and
commitments -- so claim deletion never requires touching this log.
"""
from __future__ import annotations

from typing import Any

from .store import EventStore
from .util import Clock, IdGen, norm_ts

STREAM = "gov"

KINDS = frozenset({
    "GENESIS",
    "ACTION_EVALUATED", "ACTION_EXECUTED", "ACTION_REJECTED",
    "ESCALATION_OPENED", "ESCALATION_RESOLVED",
    "BUDGET_REVIEW", "FREQUENCY_REVIEW",
    "OBLIGATION_OPENED", "OBLIGATION_DISCHARGED", "OBLIGATION_BREACHED",
    "CONTEXT_PACKAGE_ISSUED", "CLAIMS_RETRIEVED",
    "POLICY_CHANGE", "PROHIBITED_ATTEMPT",
    "STATE_TRANSITION",          # mirrors of domain-stream events (claims, permissions, corpus, delegation grants)
    "ENV_CONDITION",
    "SUSPENSION", "SUSPENSION_ADJACENT", "SUSPENSION_TRANSITION",
    "AUDIT_RESULT_RECORDED", "REAUDIT_REQUIRED",
    "APPOINTER_BOUND", "LEGACY_AUDITORS_RETIRED",  # F-04 (D-69)
    "AUTHORITY_UNDERDETERMINATION", "AUTHORITY_CONFLICT_DEFERRED",
    "INTEGRITY_CHECK",
    "EXPORT",
    "IMPORT_RUN", "IMPORT_REFUSED",  # file importers (D-72)
    "SYNC_REFUSED",  # live account sync (D-78); sync-stream events are mirrored as STATE_TRANSITION
})


class GovernanceLog:
    def __init__(self, store: EventStore, clock: Clock, ids: IdGen):
        self.store, self.clock, self.ids = store, clock, ids

    def record(self, kind: str, actor: str, **payload: Any) -> dict:
        if kind not in KINDS:
            raise ValueError(f"unknown governance log kind {kind!r}")
        return self.store.append(STREAM, kind, actor, payload, self.clock.now_iso(), self.ids.new("gov"))

    def mirror(self, domain_event: dict, actor: str, summary: dict | None = None) -> dict:
        """Cross-link a domain-stream event into the governance chain."""
        return self.record("STATE_TRANSITION", actor, stream=domain_event["stream"], seq=domain_event["seq"],
                           event_id=domain_event["event_id"], event_kind=domain_event["kind"],
                           event_hash=domain_event["hash"], summary=summary or {})

    def entries(self, start: str | None = None, end: str | None = None, kinds=None,
                start_seq: int | None = None, end_seq: int | None = None) -> list[dict]:
        start, end = norm_ts(start), norm_ts(end)
        out = []
        for e in self.store.events(STREAM, until_ts=end, kinds=kinds):
            if start and e["ts"] < start:
                continue
            if start_seq is not None and e["seq"] < start_seq:
                continue
            if end_seq is not None and e["seq"] > end_seq:
                continue
            out.append(e)
        return out

    def verify(self) -> dict:
        return self.store.verify(STREAM)

    def head(self) -> tuple[int, str]:
        return self.store.head(STREAM)

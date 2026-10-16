"""Present-authority resolution (Principle 1) and the III.1 boundary.

MedB never chooses between incompatible positions the user holds with equal
standing. If the user's present positions on a matter conflict:

* and the decision can be deferred -> AUTHORITY_CONFLICT_DEFERRED (nothing is
  done; the user is asked to restate),
* and the decision cannot be deferred -> CONSTITUTIONAL_UNDERDETERMINATION tied
  to Section III.1; the matter-scoped capability is suspended. No tie-break
  (recency, majority, "safer option", inaction-as-default) is applied, because
  any such rule would silently resolve III.1 (permanent prohibition).

Positions with *distinct* user-given priorities are not a conflict: the user
has ordered them; the highest priority governs.

Each stated position is recorded as a directive in the separate ``normative``
store (F-18, D-30), not as a claim in the claims ledger.
"""
from __future__ import annotations

from .constitution import AuditOutcome
from .govlog import GovernanceLog
from .interfaces import reaches


class AuthorityResolver:
    def __init__(self, gov: GovernanceLog, suspensions, normative=None):
        self.gov = gov
        self._suspensions = suspensions
        self.normative = normative

    @reaches("authority.resolution", "normative.store")
    def resolve_positions(self, matter: str, positions: list[dict], deferrable: bool,
                          context: dict | None = None) -> dict:
        cap = f"authority.resolution:{matter}"
        rec = self._suspensions.blocking_record(cap)
        if rec is not None:
            self._suspensions.check([cap], "AuthorityResolver.resolve_positions")
        directive_ids = []
        if self.normative is not None:
            for p in positions:
                directive_ids.append(self.normative.record_directive(
                    matter, p["position"], actor="user", priority=p.get("priority"),
                    statement=p.get("statement"), context=context))
        distinct = {p["position"] for p in positions}
        if len(distinct) <= 1:
            return {"status": "RESOLVED", "position": positions[0]["position"] if positions else None,
                    "directive_ids": directive_ids}
        prios = [p.get("priority") for p in positions]
        if all(x is not None for x in prios) and len(set(prios)) == len(prios):
            top = max(positions, key=lambda p: p["priority"])
            return {"status": "RESOLVED", "position": top["position"], "basis": "user-given priority",
                    "directive_ids": directive_ids}
        if deferrable:
            self.gov.record("AUTHORITY_CONFLICT_DEFERRED", "system", matter=matter, positions=sorted(distinct),
                            directive_ids=directive_ids, context=context or {})
            return {"status": "DEFERRED", "position": None, "directive_ids": directive_ids}
        self.gov.record("AUTHORITY_UNDERDETERMINATION", "system", matter=matter, positions=sorted(distinct),
                        directive_ids=directive_ids, section_iii_ref="III.1", context=context or {},
                        outcome=AuditOutcome.CONSTITUTIONAL_UNDERDETERMINATION.value)
        rec = self._suspensions.suspend(
            cap, trigger="conflicted present authority on a non-deferrable decision",
            classification=AuditOutcome.CONSTITUTIONAL_UNDERDETERMINATION.value,
            evidence_available=[f"normative:{c}" for c in directive_ids] + ["governance:AUTHORITY_UNDERDETERMINATION"],
            evidence_missing=["charter rule for conflicted present authority (Section III.1)"],
            section_iii_ref="III.1",
            resolution_condition="charter resolution of III.1 (currently unavailable), or PASS on re-audit. "
                                 "Whether a later unambiguous user restatement can ground a PASS is itself "
                                 "open (DECISIONS F-03); the user cannot lift this record.")
        return {"status": AuditOutcome.CONSTITUTIONAL_UNDERDETERMINATION.value, "position": None,
                "section_iii_ref": "III.1", "suspension_record": rec["record_id"], "directive_ids": directive_ids}

"""Suspension registry (Part III).

* Suspension records are immutable. Status changes are appended as separate
  TRANSITION events; a record's current status is derived (DECISIONS D-10).
* Suspension targets a primitive (mechanism) -- optionally scoped to a matter,
  e.g. ``authority.resolution:release-2026-10`` -- never an interface.
* Takes effect at detection: ``check`` consults the stream on every guarded call.
* Propagates to direct dependents (new records, ``propagated_from``); indirect
  dependents are flagged SUSPENSION_ADJACENT (not suspended).
* The user cannot lift a suspension and cannot authorize a suspended capability.
* Resolution: PASS re-audit -> RESOLVED_PASS; FAIL -> NONCOMPLIANT; charter
  resolution -> unavailable (raises).
* AUDIT_INDETERMINACY (spec II-C) means *re-audit required*; it never suspends
  automatically. It is recorded as REAUDIT_REQUIRED (F-08, D-40).
* Audit-plane reads stay open during suspension, but each one made while any
  suspension is active is recorded in the separate hash-chained ``auditlog``
  stream -- not in ``gov`` -- so Q-1 evidence is not perturbed (F-11, D-12).
"""
from __future__ import annotations

import threading

from .constitution import CHARTER_RESOLUTION_AVAILABLE, SECTION_III, AuditOutcome
from .errors import CapabilitySuspended, CharterResolutionUnavailable, NotAuthorized, SuspensionNotLiftable
from .govlog import GovernanceLog
from .interfaces import PRIMITIVES, base_primitive, dependents, interface_inventory
from .store import EventStore
from .util import Clock, IdGen

STREAM = "suspension"
AUDITLOG_STREAM = "auditlog"
BLOCKING = ("SUSPENDED", "NONCOMPLIANT")


class SuspensionRegistry:
    def __init__(self, store: EventStore, gov: GovernanceLog, clock: Clock, ids: IdGen,
                 auditors, suspend_on: list[str]):
        self.store, self.gov, self.clock, self.ids = store, gov, clock, ids
        self.auditors = auditors  # AuditorRegistry: auditor actions need an active appointment (F-04, D-69)
        if AuditOutcome.AUDIT_INDETERMINACY.value in suspend_on:
            raise ValueError("AUDIT_INDETERMINACY means re-audit required and may not trigger automatic "
                             "suspension (spec II-C; DECISIONS F-08/D-40)")
        self.suspend_on = list(suspend_on)
        self._local = threading.local()

    def is_auditor(self, actor: str) -> bool:
        return self.auditors is not None and self.auditors.is_active(actor)

    # ---- audit-plane read log (F-11) ---------------------------------------
    def audit_read(self, interface: str, primitives, actor: str | None = None):
        """Context manager wrapping an audit-plane read. Only the outermost read
        is logged (an HTTP route calling a Q-1 query yields one entry), and only
        while some suspension is active. Never blocks; never writes to gov."""
        reg = self

        class _Ctx:
            def __enter__(self_inner):
                depth = getattr(reg._local, "depth", 0)
                reg._local.depth = depth + 1
                if depth == 0:
                    active = reg.active()
                    if active:
                        reg.note_audit_read(interface, primitives, actor or "unspecified",
                                            [r["record"]["record_id"] for r in active])
                return self_inner

            def __exit__(self_inner, *exc):
                reg._local.depth -= 1
                return False
        return _Ctx()

    def note_audit_read(self, interface: str, primitives, actor: str, active_records: list[str]) -> dict:
        body = {"interface": interface, "primitives": list(primitives), "reader": actor,
                "active_suspensions": sorted(active_records)}
        return self.store.append(AUDITLOG_STREAM, "AUDIT_READ", actor, body, self.clock.now_iso(),
                                 self.ids.new("alev"))

    def audit_reads(self) -> list[dict]:
        return [dict(e["body"], ts=e["ts"], seq=e["seq"], hash=e["hash"])
                for e in self.store.events(AUDITLOG_STREAM)]

    # ---- state ------------------------------------------------------------
    def records(self, until_ts: str | None = None) -> list[dict]:
        recs: dict[str, dict] = {}
        for e in self.store.events(STREAM, until_ts=until_ts):
            b = e["body"]
            if e["kind"] == "RECORD":
                recs[b["record_id"]] = {"record": b, "status": b["status"], "transitions": []}
            elif e["kind"] == "TRANSITION":
                r = recs[b["record_id"]]
                r["transitions"].append(dict(b, ts=e["ts"]))
                r["status"] = b["to"]
        return list(recs.values())

    def adjacent_flags(self) -> list[dict]:
        return [dict(e["body"], ts=e["ts"]) for e in self.store.events(STREAM, kinds=["ADJACENT"])]

    def active(self) -> list[dict]:
        return [r for r in self.records() if r["status"] in BLOCKING]

    def blocking_record(self, capability: str) -> dict | None:
        """A record for 'x' blocks 'x' and every scoped 'x:*'; a record for 'x:m' blocks only 'x:m'."""
        for r in self.active():
            cap = r["record"]["capability"]
            if cap == capability or (":" not in cap and base_primitive(capability) == cap):
                return r
        return None

    def is_suspended(self, capability: str) -> bool:
        return self.blocking_record(capability) is not None

    def check(self, primitives, interface: str) -> None:
        for p in primitives:
            r = self.blocking_record(p)
            if r is not None:
                rid = r["record"]["record_id"]
                self.gov.record("PROHIBITED_ATTEMPT", "system", reason="capability_suspended",
                                primitive=p, interface=interface, suspension_record=rid)
                raise CapabilitySuspended(p, interface, rid)

    # ---- suspend ------------------------------------------------------------
    def _footprint(self, capability: str) -> dict:
        base = base_primitive(capability)
        scope = capability[len(base):]  # '' or ':matter'
        direct = dependents(base)
        seen, frontier = set(), list(direct)
        while frontier:  # transitive closure beyond the direct dependents
            for d2 in dependents(frontier.pop()):
                if d2 not in seen:
                    seen.add(d2)
                    frontier.append(d2)
        indirect = sorted(seen - set(direct) - {base})
        return {"direct": [d + scope for d in direct], "indirect": [d + scope for d in indirect]}

    def suspend(self, capability: str, trigger: str, classification: str, evidence_available: list[str],
                evidence_missing: list[str], resolution_condition: str | None = None,
                section_iii_ref: str | None = None, actor: str = "system", _propagated_from: str | None = None) -> dict:
        if base_primitive(capability) not in PRIMITIVES:
            raise ValueError(f"unknown primitive {capability}")
        AuditOutcome(classification)  # classification must be one of the audit outcomes
        if classification == AuditOutcome.CONSTITUTIONAL_UNDERDETERMINATION.value and section_iii_ref not in SECTION_III:
            raise ValueError("CONSTITUTIONAL_UNDERDETERMINATION must cite a known Section III question")
        existing = self.blocking_record(capability)
        if existing is not None and existing["record"]["capability"] == capability and _propagated_from:
            return existing["record"]
        footprint = self._footprint(capability) if not _propagated_from else {"direct": [], "indirect": []}
        inv = interface_inventory()["primitives"][base_primitive(capability)]["interfaces"]
        record = {
            "record_id": self.ids.new("susp"),
            "capability": capability,
            "trigger": trigger,
            "detected_at": self.clock.now_iso(),
            "evidence_available": list(evidence_available),
            "evidence_missing": list(evidence_missing),
            "classification": classification,
            "dependency_footprint": footprint,
            "interfaces": inv,
            "status": "SUSPENDED",
            "resolution_condition": resolution_condition or (
                "PASS on re-audit; or FAIL -> noncompliance; or charter resolution (currently unavailable)"),
            "section_iii_ref": section_iii_ref,
            "propagated_from": _propagated_from,
        }
        ev = self.store.append(STREAM, "RECORD", actor, record, self.clock.now_iso(), self.ids.new("sev"))
        self.gov.record("SUSPENSION", actor, record=record, suspension_event_hash=ev["hash"])
        if not _propagated_from:
            for d in footprint["direct"]:
                self.suspend(d, trigger=f"propagated from {capability} ({record['record_id']})",
                             classification=classification, evidence_available=evidence_available,
                             evidence_missing=evidence_missing, section_iii_ref=section_iii_ref,
                             actor=actor, _propagated_from=record["record_id"])
            for d in footprint["indirect"]:
                flag = {"capability": d, "flag": "SUSPENSION_ADJACENT", "flagged_by": record["record_id"]}
                self.store.append(STREAM, "ADJACENT", actor, flag, self.clock.now_iso(), self.ids.new("sev"))
                self.gov.record("SUSPENSION_ADJACENT", actor, **flag)
        return record

    # ---- refusals -----------------------------------------------------------
    def lift(self, record_id: str, actor: str) -> None:
        self.gov.record("PROHIBITED_ATTEMPT", actor, reason="suspension_lift_refused", suspension_record=record_id)
        raise SuspensionNotLiftable("suspensions cannot be lifted by any actor; resolution only by re-audit")

    # ---- resolution ---------------------------------------------------------
    def _transition(self, record_id: str, to: str, basis: dict, actor: str) -> None:
        cur = next(r for r in self.records() if r["record"]["record_id"] == record_id)
        body = {"record_id": record_id, "from": cur["status"], "to": to, "basis": basis}
        ev = self.store.append(STREAM, "TRANSITION", actor, body, self.clock.now_iso(), self.ids.new("sev"))
        self.gov.record("SUSPENSION_TRANSITION", actor, **body, suspension_event_hash=ev["hash"])

    def resolve(self, record_id: str, outcome: str, auditor: str, audit_ref: str) -> str:
        if outcome == "CHARTER_RESOLUTION":
            self.gov.record("PROHIBITED_ATTEMPT", auditor, reason="charter_resolution_unavailable",
                            suspension_record=record_id)
            if not CHARTER_RESOLUTION_AVAILABLE:
                raise CharterResolutionUnavailable("charter resolution of Section III questions is not available")
        if not self.is_auditor(auditor):
            self.gov.record("PROHIBITED_ATTEMPT", auditor, reason="non_auditor_resolution", suspension_record=record_id)
            raise NotAuthorized(f"{auditor!r} has no active auditor appointment")
        outcome = AuditOutcome(outcome).value
        rec = next(r for r in self.records() if r["record"]["record_id"] == record_id)
        if rec["status"] not in BLOCKING:
            return rec["status"]
        basis = {"outcome": outcome, "auditor": auditor, "audit_ref": audit_ref}
        if outcome == "PASS":
            to = "RESOLVED_PASS"
        elif outcome == "FAIL":
            to = "NONCOMPLIANT"
        else:
            self._transition(record_id, "SUSPENDED", dict(basis, note="re-audit inconclusive"), auditor)
            if outcome == AuditOutcome.AUDIT_INDETERMINACY.value:
                self.gov.record("REAUDIT_REQUIRED", auditor, capability=rec["record"]["capability"],
                                audit_ref=audit_ref, suspension_record=record_id,
                                basis="AUDIT_INDETERMINACY (spec II-C)")
            return "SUSPENDED"
        self._transition(record_id, to, basis, auditor)
        if to == "RESOLVED_PASS":
            for child in self.active():
                if child["record"]["propagated_from"] == record_id:
                    self._transition(child["record"]["record_id"], "RESOLVED_PASS",
                                     dict(basis, note="parent resolved"), auditor)
        return to

    def record_audit_result(self, capability: str, outcome: str, auditor: str, audit_ref: str,
                            evidence_available: list[str] = (), evidence_missing: list[str] = (),
                            section_iii_ref: str | None = None, trigger: str = "audit") -> dict:
        if not self.is_auditor(auditor):
            self.gov.record("PROHIBITED_ATTEMPT", auditor, reason="non_auditor_audit_result", capability=capability)
            raise NotAuthorized(f"{auditor!r} has no active auditor appointment")
        outcome = AuditOutcome(outcome).value
        self.gov.record("AUDIT_RESULT_RECORDED", auditor, capability=capability, outcome=outcome,
                        audit_ref=audit_ref, section_iii_ref=section_iii_ref)
        existing = [r for r in self.active() if r["record"]["capability"] == capability
                    and not r["record"]["propagated_from"]]
        result = {"capability": capability, "outcome": outcome, "records": []}
        if outcome in ("PASS", "FAIL") and existing:
            for r in existing:
                result["records"].append((r["record"]["record_id"],
                                          self.resolve(r["record"]["record_id"], outcome, auditor, audit_ref)))
        elif outcome == "FAIL":
            rec = self.suspend(capability, trigger, outcome, list(evidence_available), list(evidence_missing),
                               actor=auditor)
            self._transition(rec["record_id"], "NONCOMPLIANT",
                             {"outcome": outcome, "auditor": auditor, "audit_ref": audit_ref}, auditor)
            result["records"].append((rec["record_id"], "NONCOMPLIANT"))
        elif outcome == AuditOutcome.AUDIT_INDETERMINACY.value:
            # II-C: re-audit required; capability NOT automatically suspended (F-08).
            e = self.gov.record("REAUDIT_REQUIRED", auditor, capability=capability, audit_ref=audit_ref,
                                basis="AUDIT_INDETERMINACY (spec II-C)", automatic_suspension=False,
                                evidence_available=list(evidence_available),
                                evidence_missing=list(evidence_missing))
            result["reaudit_required"] = True
            result["reaudit_entry"] = e["seq"]
        elif outcome in self.suspend_on:
            rec = self.suspend(capability, trigger, outcome, list(evidence_available), list(evidence_missing),
                               section_iii_ref=section_iii_ref, actor=auditor)
            result["records"].append((rec["record_id"], "SUSPENDED"))
        return result

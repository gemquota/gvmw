"""Behavioral query interface Q-1.

Exactly eight queries (Part VI 6.1). They are audit-plane interfaces: read-only,
never blocked by suspension, and they do not write to the governance log
(querying must not perturb the evidence it reports -- DECISIONS D-12).
"""
from __future__ import annotations

import hashlib
import re
import inspect
import sys
from pathlib import Path

from . import __version__
from .constitution import CHARTER_DIGEST
from .interfaces import interface_inventory, reaches
from .netscan import network_profile
from .util import digest, norm_ts

Q1_QUERIES = ("actions_in_window", "authorizing_clause", "context_packages_issued", "claims_retrieved",
              "cumulative_effect", "policy_current", "governance_log", "self_description")


def _source_digest(obj) -> dict:
    cls = obj if inspect.isclass(obj) else type(obj)
    mod = sys.modules.get(cls.__module__)
    path = getattr(mod, "__file__", None)
    h = hashlib.sha256(Path(path).read_bytes()).hexdigest() if path else None
    return {"class": f"{cls.__module__}.{cls.__qualname__}", "source_file": Path(path).name if path else None,
            "source_sha256": h}


def _integrations_status(m) -> dict:
    from .integrations import status  # lazy: integrations.mcp_tools imports this module
    return status(m)


class Q1:
    def __init__(self, medb):
        self.m = medb
        # Audit plane: never blocked; reads during an active suspension go to `auditlog` (F-11).
        self._suspensions = medb.suspensions

    @staticmethod
    def _in(ts: str, start, end) -> bool:
        return (start is None or ts >= start) and (end is None or ts <= end)

    @reaches("governance.log", "delegation.execution", plane="audit")
    def actions_in_window(self, start=None, end=None) -> dict:
        start, end = norm_ts(start), norm_ts(end)
        acts: dict[str, dict] = {}
        esc_to_action = {}
        for e in self.m.gov.entries():
            b, k = e["body"], e["kind"]
            if k == "ACTION_EVALUATED":
                a = b["action"]
                acts[a["action_id"]] = {"action_id": a["action_id"], "agent": a.get("agent"), "kind": a.get("kind"),
                                        "submitted_at": e["ts"], "decision": b["decision"], "clause": b["clause"],
                                        "status": {"AUTHORIZED": "EXECUTED", "PROHIBITED": "REJECTED"}.get(
                                            b["decision"], "ESCALATED"),
                                        "emergency": bool(a.get("emergency")), "action": a,
                                        "executed_at": None, "authorizing_clause": None, "escalation_id": None}
            elif k == "ESCALATION_OPENED":
                esc_to_action[b["escalation_id"]] = b["action"]["action_id"]
                if b["action"]["action_id"] in acts:
                    acts[b["action"]["action_id"]]["escalation_id"] = b["escalation_id"]
            elif k == "ESCALATION_RESOLVED":
                aid = esc_to_action.get(b["escalation_id"])
                if aid in acts:
                    acts[aid]["status"] = "ESCALATION_" + b["status"]
            elif k == "ACTION_EXECUTED":
                a = acts.setdefault(b["action_id"], {"action_id": b["action_id"], "action": b["action"],
                                                     "submitted_at": e["ts"]})
                a.update(executed_at=e["ts"], authorizing_clause=b["authorizing_clause"], status="EXECUTED",
                         lines_non_critical=b["lines_non_critical"], lines_critical=b["lines_critical"])
        rows = [a for a in acts.values() if self._in(a["submitted_at"], start, end)
                or (a.get("executed_at") and self._in(a["executed_at"], start, end))]
        return {"query": "actions_in_window", "start": start, "end": end, "count": len(rows), "actions": rows}

    @reaches("governance.log", "delegation.evaluator", plane="audit")
    def authorizing_clause(self, action_id: str) -> dict:
        ev = ex = None
        for e in self.m.gov.entries(kinds=["ACTION_EVALUATED", "ACTION_EXECUTED"]):
            if e["kind"] == "ACTION_EVALUATED" and e["body"]["action"]["action_id"] == action_id:
                ev = e
            if e["kind"] == "ACTION_EXECUTED" and e["body"]["action_id"] == action_id:
                ex = e
        if ev is None and ex is None:
            return {"query": "authorizing_clause", "action_id": action_id, "found": False}
        clause = (ex or ev)["body"].get("authorizing_clause") or ev["body"]["clause"]
        base = clause[len("USER_APPROVAL<"):-1] if clause.startswith("USER_APPROVAL<") else clause
        pol = self.m.policies.current("P-1", (ev or ex)["ts"])
        return {"query": "authorizing_clause", "action_id": action_id, "found": True,
                "executed": ex is not None, "authorizing_clause": ex["body"]["authorizing_clause"] if ex else None,
                "basis": ex["body"]["basis"] if ex else None,
                "evaluation": {"decision": ev["body"]["decision"], "clause": ev["body"]["clause"],
                               "trace": ev["body"]["trace"], "policy_digest": ev["body"]["policy_digest"],
                               "classification_digest": ev["body"]["classification_digest"],
                               "evaluated_at": ev["ts"]} if ev else None,
                "clause_text": pol["clauses"].get(m.group(1)) if (m := re.match(r"(P-1\.\d+)", base)) else None}

    @reaches("governance.log", "context.build", plane="audit")
    def context_packages_issued(self, start=None, end=None) -> dict:
        rows = [dict(e["body"], log_seq=e["seq"]) for e in
                self.m.gov.entries(start=start, end=end, kinds=["CONTEXT_PACKAGE_ISSUED"])]
        return {"query": "context_packages_issued", "start": norm_ts(start), "end": norm_ts(end),
                "count": len(rows), "packages": rows}

    @reaches("governance.log", "claims.retrieval", plane="audit")
    def claims_retrieved(self, start=None, end=None) -> dict:
        rows = [dict(e["body"], ts=e["ts"], actor=e["actor"], log_seq=e["seq"]) for e in
                self.m.gov.entries(start=start, end=end, kinds=["CLAIMS_RETRIEVED"])]
        return {"query": "claims_retrieved", "start": norm_ts(start), "end": norm_ts(end), "count": len(rows),
                "retrievals": rows}

    @reaches("governance.log", "delegation.evaluator", plane="audit")
    def cumulative_effect(self, at=None) -> dict:
        at = norm_ts(at) or self.m.clock.now_iso()
        ev = self.m.evaluator
        per_module: dict[str, int] = {}
        cum = ev.cumulative_lines(at)
        for a in ev.history.executed(since=cum["window_start"], until=at):
            for c in a["action"].get("changes", []):
                per_module[c["path"]] = per_module.get(c["path"], 0) + int(c.get("lines", 0))
        obligations = self.m.delegation.obligations()
        return {"query": "cumulative_effect", "at": at,
                "P-1.5": cum, "P-1.6": ev.emergency_count(at),
                "lines_by_module_in_P-1.5_window": per_module,
                "obligations": {s: sum(1 for o in obligations.values() if o["status"] == s)
                                for s in ("OPEN", "DISCHARGED", "DISCHARGED_LATE", "BREACHED")},
                "escalations": {s: sum(1 for x in self.m.delegation.escalations().values() if x["status"] == s)
                                for s in ("OPEN", "APPROVED", "REJECTED", "UNDERDETERMINED")},
                "classification_versions": len(self.m.policies.versions("module_classification")),
                "active_suspensions": len(self.m.suspensions.active())}

    @reaches("policy.store", plane="audit")
    def policy_current(self) -> dict:
        out = {"query": "policy_current"}
        for doc in ("P-1", "module_classification"):
            cur = self.m.policies.current_version(doc)
            out[doc] = {"version": cur["version"], "digest": cur["digest"], "content": cur["content"],
                        "history": [{"version": v["version"], "ts": v["ts"], "actor": v["actor"],
                                     "digest": v["digest"], "reason": v["reason"]}
                                    for v in self.m.policies.versions(doc)]}
        return out

    @reaches("governance.log", plane="audit")
    def governance_log(self, start_seq=None, end_seq=None) -> dict:
        entries = self.m.gov.entries(start_seq=start_seq, end_seq=end_seq)
        return {"query": "governance_log", "count": len(entries), "entries": entries,
                "verification": {s: self.m.store.verify(s) for s in self.m.store.streams()}}

    @reaches("governance.log", plane="audit")
    def self_description(self) -> dict:
        """Generated from the running objects -- not hand-written (Principle 13)."""
        m = self.m
        comps = {name: _source_digest(obj) for name, obj in m.components().items()}
        return {
            "query": "self_description", "system": "MedB", "version": __version__, "milestone": "M0",
            "charter_digest": CHARTER_DIGEST,
            "genesis_charter_digest": m.gov.entries(kinds=["GENESIS"])[0]["body"]["charter_digest"],
            "components": comps,
            "configuration": {"digest": digest(m.config), "ranking": m.config["ranking"],
                              "rendering": m.config["rendering"], "context": m.config["context"],
                              "audit": m.config["audit"]},
            "auditor_appointment": {"appointer": m.auditors.binding(), "active_auditors": m.auditors.active_auditors(),
                                    "method": "signed appointer statements (F-04, D-69)"},
            "policies": {d: m.policies.current_version(d)["digest"] for d in ("P-1", "module_classification")},
            "interface_inventory": interface_inventory(),
            "q1_queries": list(Q1_QUERIES),
            "storage": {"engine": "sqlite", "streams": m.store.streams(), "append_only": "triggers on events table"},
            "network": network_profile(m),
            "integrations": _integrations_status(m),
            "export_format": "medb-export/1.0",
            "active_suspensions": [r["record"]["capability"] for r in m.suspensions.active()],
        }

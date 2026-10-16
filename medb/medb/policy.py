"""Delegation policy store and evaluator (P-1).

The PolicyStore is the authoritative, versioned home of the delegation policy
and the module-criticality classification. Files under ``policies/`` are only
genesis inputs. Only the user can create a new version (P-1.7, Principle 4);
any other actor's attempt is refused and logged.

The evaluator is a pure function of (policy, classification, governance-log
history, environment conditions, delegation grant, proposed action). It
evaluates both per-action constraints and cumulative/sequence constraints and
returns AUTHORIZED / REQUIRES_ESCALATION / PROHIBITED with a clause reference
and a full trace of every clause it checked.
"""
from __future__ import annotations

import copy
import datetime as _dt
import fnmatch
import json
from pathlib import Path

from .constitution import Decision, contains_prohibited_term
from .errors import NotAuthorized
from .govlog import GovernanceLog
from .interfaces import reaches
from .store import EventStore
from .util import Clock, IdGen, digest, iso, parse_iso

STREAM = "policy"
DOCS = ("P-1", "module_classification")
ACTION_KINDS = ("code_change", "dependency_add", "revert", "external_communication",
                "policy_change", "classification_change")


class PolicyStore:
    def __init__(self, store: EventStore, gov: GovernanceLog, clock: Clock, ids: IdGen, suspensions=None):
        self.store, self.gov, self.clock, self.ids = store, gov, clock, ids
        self._suspensions = suspensions

    def load_genesis(self, policy_dir: Path) -> None:
        if self.store.events(STREAM):
            return
        for doc, fname in (("P-1", "P-1.json"), ("module_classification", "module_classification.json")):
            content = json.loads((Path(policy_dir) / fname).read_text())
            self._version(doc, content, "user", f"genesis load from {fname}")

    def _version(self, doc: str, content: dict, actor: str, reason: str) -> dict:
        prev = self.current_version(doc)
        body = {"document": doc, "version": (prev["version"] + 1) if prev else 1, "content": content,
                "digest": digest(content), "previous_digest": prev["digest"] if prev else None, "reason": reason}
        ev = self.store.append(STREAM, "VERSION", actor, body, self.clock.now_iso(), self.ids.new("polev"))
        self.gov.record("POLICY_CHANGE", actor, document=doc, version=body["version"], digest=body["digest"],
                        previous_digest=body["previous_digest"], reason=reason, policy_event_hash=ev["hash"],
                        content=content)
        return body

    def versions(self, doc: str, until_ts: str | None = None) -> list[dict]:
        return [dict(e["body"], ts=e["ts"], actor=e["actor"]) for e in self.store.events(STREAM, until_ts=until_ts)
                if e["body"]["document"] == doc]

    def current_version(self, doc: str, at: str | None = None) -> dict | None:
        v = self.versions(doc, until_ts=at)
        return v[-1] if v else None

    def current(self, doc: str, at: str | None = None) -> dict:
        return copy.deepcopy(self.current_version(doc, at)["content"])

    @reaches("policy.store")
    def change(self, doc: str, new_content: dict, actor: str, reason: str) -> dict:
        if doc not in DOCS:
            raise ValueError(doc)
        if actor != "user":
            self.gov.record("PROHIBITED_ATTEMPT", actor, reason="non_user_policy_change", document=doc,
                            clause="P-1.7" if doc == "module_classification" else "PRINCIPLE-4")
            raise NotAuthorized("policy and module classification can be changed only by the user")
        return self._version(doc, new_content, actor, reason)

    def classify(self, path: str, at: str | None = None) -> str:
        mc = self.current("module_classification", at)
        for rule in mc["rules"]:
            if fnmatch.fnmatch(path, rule["pattern"]):
                return rule["class"]
        return mc["default"]


def _ts_minus(now: str, **kw) -> str:
    return iso(parse_iso(now) - _dt.timedelta(**kw))


class History:
    """Evaluator view over governance-log history (sequence constraints)."""

    def __init__(self, gov: GovernanceLog):
        self.gov = gov

    def executed(self, since: str | None = None, until: str | None = None) -> list[dict]:
        return [dict(e["body"], ts=e["ts"]) for e in self.gov.entries(start=since, end=until, kinds=["ACTION_EXECUTED"])]

    def last_ts(self, kind: str, until: str | None = None) -> str | None:
        es = self.gov.entries(end=until, kinds=[kind])
        return es[-1]["ts"] if es else None

    def env(self, until: str | None = None) -> dict:
        state = {}
        for e in self.gov.entries(end=until, kinds=["ENV_CONDITION"]):
            state[e["body"]["condition"]] = e["body"]["value"]
        return state


class Evaluator:
    def __init__(self, policies: PolicyStore, gov: GovernanceLog, clock: Clock, suspensions=None):
        self.policies, self.gov, self.clock = policies, gov, clock
        self.history = History(gov)
        self._suspensions = suspensions

    # -- helpers ---------------------------------------------------------------
    @staticmethod
    def _lines(action: dict) -> int:
        return sum(int(c.get("lines", 0)) for c in action.get("changes", []))

    def split_lines(self, action: dict, at: str | None = None) -> tuple[int, int, dict]:
        classes = {c["path"]: self.policies.classify(c["path"], at) for c in action.get("changes", [])}
        crit = sum(int(c.get("lines", 0)) for c in action.get("changes", []) if classes[c["path"]] == "critical")
        return self._lines(action) - crit, crit, classes

    def cumulative_lines(self, now: str) -> dict:
        p = self.policies.current("P-1", now)["clauses"]["P-1.5"]
        window_start = _ts_minus(now, days=p["window_days"])
        last_review = self.history.last_ts("BUDGET_REVIEW", now)
        baseline = max(window_start, last_review) if last_review else window_start
        used = sum(a["lines_non_critical"] for a in self.history.executed(since=baseline, until=now)
                   if a["ts"] > baseline)
        return {"window_days": p["window_days"], "window_start": window_start, "baseline": baseline,
                "last_budget_review": last_review, "used": used, "limit": p["max_lines_non_critical"]}

    def emergency_count(self, now: str) -> dict:
        p = self.policies.current("P-1", now)["clauses"]["P-1.6"]
        window_start = _ts_minus(now, days=p["window_days"])
        last_review = self.history.last_ts("FREQUENCY_REVIEW", now)
        baseline = max(window_start, last_review) if last_review else window_start
        n = sum(1 for a in self.history.executed(since=baseline, until=now) if a["emergency"] and a["ts"] > baseline)
        return {"window_days": p["window_days"], "baseline": baseline, "last_frequency_review": last_review,
                "count": n, "limit": p["max_invocations"]}

    @staticmethod
    def _cumulative_exceeded(used: int, proposed: int, limit: int) -> bool:
        return used + proposed > limit

    @staticmethod
    def _frequency_exceeded(ec: dict) -> bool:
        return ec["count"] >= ec["limit"]

    # -- evaluation ------------------------------------------------------------
    @reaches("delegation.evaluator", "policy.store")
    def evaluate(self, action: dict, grant: dict | None, now: str | None = None) -> dict:
        now = now or self.clock.now_iso()
        trace: list[dict] = []

        def out(decision: Decision, clause: str, review: str | None = None, **facts):
            return {"decision": decision.value, "clause": clause, "review_type": review, "trace": trace,
                    "facts": facts, "evaluated_at": now,
                    "policy_digest": self.policies.current_version("P-1", now)["digest"],
                    "classification_digest": self.policies.current_version("module_classification", now)["digest"]}

        P = self.policies.current("P-1", now)
        C = P["clauses"]
        interp = P.get("interpretations", {})
        kind = action.get("kind")

        # Delegation grant: default-deny, explicit, bounded, revocable.
        if grant is None:
            trace.append({"clause": "DELEGATION.grant", "result": "no active grant"})
            return out(Decision.PROHIBITED, "DELEGATION.grant")
        limits = grant.get("effective_limits", {})
        trace.append({"clause": "DELEGATION.grant", "result": "active", "delegation_id": grant["delegation_id"]})

        if kind not in ACTION_KINDS:
            trace.append({"clause": "DELEGATION.default_deny", "result": f"unknown kind {kind!r}"})
            return out(Decision.PROHIBITED, "DELEGATION.default_deny")
        if limits.get("allowed_kinds") is not None and kind not in limits["allowed_kinds"]:
            trace.append({"clause": "DELEGATION.attenuation", "result": f"kind {kind} not in attenuated grant"})
            return out(Decision.PROHIBITED, "DELEGATION.attenuation")
        if kind in ("policy_change", "classification_change"):
            trace.append({"clause": "P-1.7", "result": "agent may not change policy or classification"})
            return out(Decision.PROHIBITED, "P-1.7")
        term = contains_prohibited_term(json.dumps(action, sort_keys=True))
        if term:
            trace.append({"clause": "CONSTITUTION.permanent_prohibitions", "result": term})
            return out(Decision.PROHIBITED, "CONSTITUTION.permanent_prohibitions")

        nc_lines, crit_lines, classes = self.split_lines(action, now)
        lines = nc_lines + crit_lines
        any_critical = any(v == "critical" for v in classes.values())
        facts = {"lines": lines, "lines_non_critical": nc_lines, "lines_critical": crit_lines, "classes": classes}

        # P-1.4 revert own change within window.
        if kind == "revert":
            target = next((a for a in self.history.executed(until=now)
                           if a["action"]["action_id"] == action.get("reverts")), None)
            ok = (target is not None and target["action"]["agent"] == action["agent"]
                  and target["ts"] >= _ts_minus(now, hours=C["P-1.4"]["window_hours"]))
            trace.append({"clause": "P-1.4", "result": "own change within window" if ok else "not applicable",
                          "target": action.get("reverts")})
            if ok:
                return out(Decision.AUTHORIZED, "P-1.4", **facts)

        # P-1.6 emergency clause.
        emergency = action.get("emergency")
        if emergency:
            cond = emergency.get("condition")
            env = self.history.env(now)
            if cond not in C["P-1.6"]["conditions"] or not env.get(cond):
                trace.append({"clause": "P-1.6.1", "result": f"condition {cond!r} not active in recorded environment"})
                return out(Decision.PROHIBITED, "P-1.6.1", **facts)
            ec = self.emergency_count(now)
            trace.append({"clause": "P-1.6.3", "result": f"{ec['count']} invocations since {ec['baseline']}",
                          "limit": ec["limit"]})
            if self._frequency_exceeded(ec):
                return out(Decision.REQUIRES_ESCALATION, "P-1.6.3", "frequency_review", **facts, emergency_count=ec)

        # P-1.2 mandatory escalation categories.
        cats = []
        if any_critical:
            cats.append("critical_module")
        cats += [t for t in action.get("tags", []) if t in C["P-1.2"]["categories"]]
        if kind == "external_communication":
            cats.append("external_communication")
        if kind == "dependency_add":
            dep = action.get("dependency", {})
            within = (dep.get("direct_count", 99) <= C["P-1.3"]["max_direct_packages"]
                      and dep.get("install_size_mb", 1e9) <= C["P-1.3"]["max_total_install_mb"]
                      and not any_critical)
            trace.append({"clause": "P-1.3", "result": "within bounds" if within else "outside bounds", "dependency": dep})
            if not within:
                cats.append("dependency")
        if cats:
            trace.append({"clause": "P-1.2", "result": "escalation categories", "categories": sorted(set(cats))})
            clause = "P-1.3" if set(cats) == {"dependency"} else "P-1.2"
            return out(Decision.REQUIRES_ESCALATION, clause, "approval", **facts, categories=sorted(set(cats)))

        # P-1.1 per-action size. During a valid emergency (P-1.6.1 passed above) the
        # non-critical per-action limit is raised up to whatever remains of the
        # P-1.5 cumulative budget (Gem's ruling on F-09; D-22). Critical modules
        # never reach here (P-1.2 above). Attenuated grant limits still bind.
        cum = self.cumulative_lines(now)
        limit = min(cum["limit"], limits.get("max_cumulative_lines", 10**9))
        base_max = C["P-1.1"]["max_lines_per_action"]
        raised = None
        if emergency and interp.get("emergency_per_action_limit_up_to_remaining_budget", False):
            remaining = max(0, limit - cum["used"])
            # remaining < floor  <=>  used + floor > limit (same sequence-constraint hook as P-1.5)
            if interp.get("emergency_below_floor_escalates", False) and \
                    self._cumulative_exceeded(cum["used"], base_max, limit):
                # Gem's ruling (2 Oct 2026, D-22): no 50-line floor; the user decides.
                trace.append({"clause": "P-1.5", "result": f"emergency (P-1.6) but only {remaining} lines remain "
                              f"of the cumulative budget (< {base_max}); escalate (D-22)",
                              "baseline": cum["baseline"]})
                return out(Decision.REQUIRES_ESCALATION, "P-1.5", "budget_review", **facts, cumulative=cum,
                           emergency_clause="P-1.6", remaining_budget=remaining)
            raised = max(base_max, remaining)
            base_max = raised
        max_lines = min(base_max, limits.get("max_lines_per_action", 10**9))
        trace.append({"clause": "P-1.1", "result": f"{lines} lines (max {max_lines})"
                      + (f" (emergency: raised to remaining P-1.5 budget, D-22)" if raised is not None else "")})
        if lines > max_lines:
            return out(Decision.REQUIRES_ESCALATION, "P-1.1", "approval", **facts)

        # P-1.5 cumulative (sequence) constraint.
        exempt = bool(emergency) and interp.get("emergency_exempts_cumulative_budget", False)
        trace.append({"clause": "P-1.5", "result": f"{cum['used']}+{nc_lines} of {limit}"
                      + (" (emergency-exempt, D-22)" if exempt else ""), "baseline": cum["baseline"]})
        if not exempt and self._cumulative_exceeded(cum["used"], nc_lines, limit):
            return out(Decision.REQUIRES_ESCALATION, "P-1.5", "budget_review", **facts, cumulative=cum)

        if emergency:
            return out(Decision.AUTHORIZED, "P-1.6", **facts, cumulative=cum)
        return out(Decision.AUTHORIZED, "P-1.3" if kind == "dependency_add" else "P-1.1", **facts, cumulative=cum)

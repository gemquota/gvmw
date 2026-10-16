"""Delegation layer: default-deny, explicit, bounded, revocable, non-escalating.

* Delegation grants are issued only by the user. A delegate may *attenuate*
  (sub-delegate with narrower limits), never amplify (object-capability rule:
  capability may increase, authority does not).
* ``submit`` evaluates a proposed action with the Evaluator and records the
  outcome in the governance log (ACTION_EVALUATED, then ACTION_EXECUTED /
  ESCALATION_OPENED / ACTION_REJECTED).
* Escalations are resolved only by the user. Approval cannot override
  PROHIBITED, cannot authorize a suspended capability, and conflicting user
  positions are routed to the AuthorityResolver (III.1 boundary).
* Emergency invocations open a reporting obligation (due within 60 minutes).
* Non-deferrability (F-02, D-63): only the user (at resolution) or a recorded
  ENV_CONDITION ``deadline`` / ``outage`` (set by environment or user, global
  or matter-scoped) can make a decision non-deferrable. An agent-supplied
  ``deferrable: false`` is ignored and logged as PROHIBITED_ATTEMPT.
"""
from __future__ import annotations

import datetime as _dt

from .constitution import Decision
from .errors import NotAuthorized
from .govlog import GovernanceLog
from .interfaces import reaches
from .store import EventStore
from .util import Clock, IdGen, iso, norm_ts, parse_iso

STREAM = "delegation"
LIMIT_KEYS = ("max_lines_per_action", "max_cumulative_lines", "allowed_kinds")
NON_DEFERRAL_CONDITIONS = ("deadline", "outage")


class DelegationService:
    def __init__(self, store: EventStore, gov: GovernanceLog, evaluator, policies, authority, clock: Clock,
                 ids: IdGen, suspensions):
        self.store, self.gov, self.evaluator, self.policies = store, gov, evaluator, policies
        self.authority, self.clock, self.ids = authority, clock, ids
        self._suspensions = suspensions

    # ---------------------------------------------------------------- grants
    def grant(self, delegate: str, actor: str, policy_id: str = "P-1", expires_at: str | None = None,
              limits: dict | None = None, parent: str | None = None) -> dict:
        limits = dict(limits or {})
        if set(limits) - set(LIMIT_KEYS):
            raise ValueError(f"unknown limit keys {set(limits) - set(LIMIT_KEYS)}")
        if parent is None:
            if actor != "user":
                self.gov.record("PROHIBITED_ATTEMPT", actor, reason="non_user_root_delegation", delegate=delegate)
                raise NotAuthorized("only the user can issue a root delegation")
        else:
            pg = self.active_grant_by_id(parent)
            if pg is None or pg["delegate"] != actor:
                self.gov.record("PROHIBITED_ATTEMPT", actor, reason="attenuation_without_parent", parent=parent)
                raise NotAuthorized("sub-delegation requires holding an active parent grant")
            limits = self._attenuate(pg["effective_limits"], limits, actor)
            if pg["expires_at"] and (expires_at is None or norm_ts(expires_at) > pg["expires_at"]):
                expires_at = pg["expires_at"]
        body = {"delegation_id": self.ids.new("deleg"), "delegate": delegate, "policy_id": policy_id,
                "expires_at": norm_ts(expires_at), "limits": limits, "parent": parent}
        ev = self.store.append(STREAM, "GRANT", actor, body, self.clock.now_iso(), self.ids.new("dev"))
        self.gov.mirror(ev, actor, {"delegation_id": body["delegation_id"], "delegate": delegate})
        return body

    def _policy_ceiling(self) -> dict:
        c = self.policies.current("P-1")["clauses"]
        return {"max_lines_per_action": c["P-1.1"]["max_lines_per_action"],
                "max_cumulative_lines": c["P-1.5"]["max_lines_non_critical"], "allowed_kinds": None}

    def _attenuate(self, parent_limits: dict, requested: dict, actor: str) -> dict:
        eff = dict(parent_limits)
        ceiling = self._policy_ceiling()
        for k, v in requested.items():
            pv = parent_limits.get(k, ceiling.get(k))
            if k == "allowed_kinds":
                if pv is not None and not set(v) <= set(pv):
                    self.gov.record("PROHIBITED_ATTEMPT", actor, reason="amplification_attempt", limit=k)
                    raise NotAuthorized("attenuation may only narrow allowed_kinds")
            elif pv is not None and v > pv:
                self.gov.record("PROHIBITED_ATTEMPT", actor, reason="amplification_attempt", limit=k)
                raise NotAuthorized(f"attenuation may only narrow {k}")
            eff[k] = v
        return eff

    def revoke(self, delegation_id: str, actor: str) -> None:
        if actor != "user":
            self.gov.record("PROHIBITED_ATTEMPT", actor, reason="non_user_delegation_revoke",
                            delegation_id=delegation_id)
            raise NotAuthorized("only the user can revoke a delegation")
        ev = self.store.append(STREAM, "REVOKE", actor, {"delegation_id": delegation_id},
                               self.clock.now_iso(), self.ids.new("dev"))
        self.gov.mirror(ev, actor, {"delegation_id": delegation_id, "revoked": True})

    def grants(self, at: str | None = None) -> dict[str, dict]:
        at = norm_ts(at) or self.clock.now_iso()
        gs: dict[str, dict] = {}
        for e in self.store.events(STREAM, until_ts=at):
            b = e["body"]
            if e["kind"] == "GRANT":
                gs[b["delegation_id"]] = dict(b, granted_at=e["ts"], granted_by=e["actor"], revoked_at=None)
            elif e["kind"] == "REVOKE":
                gs[b["delegation_id"]]["revoked_at"] = e["ts"]
        for g in gs.values():  # revocation and limits propagate down the chain
            eff, cur, revoked = {}, g, None
            chain = []
            while cur is not None:
                chain.append(cur)
                revoked = revoked or cur["revoked_at"]
                cur = gs.get(cur["parent"]) if cur["parent"] else None
            for c in reversed(chain):
                eff.update(c["limits"])
            g["effective_limits"], g["chain_revoked_at"] = eff, revoked
        return gs

    def active_grant_by_id(self, delegation_id: str, at: str | None = None) -> dict | None:
        at = norm_ts(at) or self.clock.now_iso()
        g = self.grants(at).get(delegation_id)
        if g is None or g["chain_revoked_at"] or (g["expires_at"] and g["expires_at"] <= at):
            return None
        return g

    def active_grant(self, delegate: str, at: str | None = None) -> dict | None:
        for gid in sorted(self.grants(at)):
            g = self.active_grant_by_id(gid, at)
            if g and g["delegate"] == delegate:
                return g
        return None

    # --------------------------------------------------------------- actions
    @reaches("delegation.execution", "delegation.evaluator")
    def submit(self, action: dict) -> dict:
        action = dict(action)
        action.setdefault("action_id", self.ids.new("act"))
        if "deferrable" in action:
            # Agents cannot declare deferrability (F-02). Ignore; log a false claim as prohibited.
            claimed = action.pop("deferrable")
            if claimed is False:
                self.gov.record("PROHIBITED_ATTEMPT", action.get("agent", "?"), reason="agent_set_non_deferrable",
                                action_id=action["action_id"], matter=action.get("matter"),
                                note="ignored: only the user or a recorded ENV_CONDITION (deadline/outage) "
                                     "can make a decision non-deferrable")
        if action.get("matter"):
            self._suspensions.check([f"delegation.execution:{action['matter']}"], "DelegationService.submit")
        if action.get("emergency"):
            self._suspensions.check(["delegation.emergency"], "DelegationService.submit")
        grant = self.active_grant(action.get("agent", ""))
        result = self.evaluator.evaluate(action, grant)
        self.gov.record("ACTION_EVALUATED", action.get("agent", "?"), action=action, decision=result["decision"],
                        clause=result["clause"], trace=result["trace"], review_type=result["review_type"],
                        policy_digest=result["policy_digest"], classification_digest=result["classification_digest"])
        out = {"action_id": action["action_id"], **result}
        if result["decision"] == Decision.AUTHORIZED.value:
            self._execute(action, result["clause"], basis="policy", facts=result["facts"])
        elif result["decision"] == Decision.REQUIRES_ESCALATION.value:
            esc = self.ids.new("esc")
            d = self.deferrability(action.get("matter") or f"escalation:{esc}")
            self.gov.record("ESCALATION_OPENED", "system", escalation_id=esc, action=action,
                            clause=result["clause"], review_type=result["review_type"],
                            deferrable=d["deferrable"], deferrability_basis=d["basis"], facts=result["facts"])
            out["escalation_id"] = esc
        else:
            self.gov.record("ACTION_REJECTED", "system", action_id=action["action_id"], clause=result["clause"])
        return out

    def _execute(self, action: dict, clause: str, basis: str, facts: dict, escalation_id: str | None = None):
        nc, crit, classes = self.evaluator.split_lines(action)
        self.gov.record("ACTION_EXECUTED", action["agent"], action=action, action_id=action["action_id"],
                        authorizing_clause=clause, basis=basis, escalation_id=escalation_id,
                        lines_non_critical=nc, lines_critical=crit, classes=classes,
                        emergency=bool(action.get("emergency")) and clause in ("P-1.6", "P-1.6.3"))
        if action.get("emergency") and clause in ("P-1.6", "P-1.6.3"):
            minutes = self.policies.current("P-1")["clauses"]["P-1.6"]["report_within_minutes"]
            due = iso(self.clock.now() + _dt.timedelta(minutes=minutes))
            self.gov.record("OBLIGATION_OPENED", "system", obligation_id=self.ids.new("obl"),
                            action_id=action["action_id"], obligation_kind="emergency_report", due_at=due, clause="P-1.6.2")

    def escalations(self) -> dict[str, dict]:
        es: dict[str, dict] = {}
        for e in self.gov.entries(kinds=["ESCALATION_OPENED", "ESCALATION_RESOLVED"]):
            b = e["body"]
            if e["kind"] == "ESCALATION_OPENED":
                es[b["escalation_id"]] = dict(b, status="OPEN", opened_at=e["ts"])
            else:
                es[b["escalation_id"]]["status"] = b["status"]
        return es

    @reaches("delegation.execution", "authority.resolution")
    def resolve_escalation(self, escalation_id: str, actor: str, approve: bool | None = None,
                           positions: list[dict] | None = None, deferrable: bool | None = None) -> dict:
        if actor != "user":
            self.gov.record("PROHIBITED_ATTEMPT", actor, reason="non_user_escalation_resolution",
                            escalation_id=escalation_id)
            raise NotAuthorized("only the user resolves escalations")
        esc = self.escalations()[escalation_id]
        if esc["status"] != "OPEN":
            raise ValueError(f"escalation {escalation_id} is {esc['status']}")
        action = esc["action"]
        matter = action.get("matter") or f"escalation:{escalation_id}"
        if positions is None:
            positions = [{"position": "approve" if approve else "reject"}]
        if deferrable is None:  # re-derive at resolution: conditions may have been recorded since opening
            d = self.deferrability(matter)
        else:  # actor is the user (checked above)
            d = {"deferrable": bool(deferrable), "basis": {"source": "user", "at_resolution": True}}
        deferrable = d["deferrable"]
        r = self.authority.resolve_positions(matter, positions, deferrable,
                                             context={"escalation_id": escalation_id,
                                                      "deferrability_basis": d["basis"]})
        if r["status"] != "RESOLVED":
            if r["status"] != "DEFERRED":
                self.gov.record("ESCALATION_RESOLVED", "system", escalation_id=escalation_id,
                                status="UNDERDETERMINED", section_iii_ref=r.get("section_iii_ref"),
                                suspension_record=r.get("suspension_record"))
            return r
        approved = r["position"] == "approve"
        if approved:
            self._suspensions.check(["delegation.execution", f"delegation.execution:{matter}"]
                                    + (["delegation.emergency"] if action.get("emergency") else []),
                                    "DelegationService.resolve_escalation")
            if esc["review_type"] == "budget_review":
                self.gov.record("BUDGET_REVIEW", "user", escalation_id=escalation_id, clause="P-1.5")
            if esc["review_type"] == "frequency_review":
                self.gov.record("FREQUENCY_REVIEW", "user", escalation_id=escalation_id, clause="P-1.6.3")
        self.gov.record("ESCALATION_RESOLVED", actor, escalation_id=escalation_id,
                        status="APPROVED" if approved else "REJECTED", directive_ids=r["directive_ids"])
        if approved:
            clause = "P-1.6.3" if esc["review_type"] == "frequency_review" else f"USER_APPROVAL<{esc['clause']}>"
            self._execute(action, clause, basis="user_approval", facts=esc["facts"], escalation_id=escalation_id)
        return dict(r, approved=approved)

    # ----------------------------------------------------------- obligations
    def report_emergency(self, action_id: str, actor: str, report: str) -> dict:
        obl = self.obligations().get(action_id)
        if obl is None:
            raise ValueError(f"no reporting obligation for {action_id}")
        now = self.clock.now_iso()
        e = self.gov.record("OBLIGATION_DISCHARGED", actor, obligation_id=obl["obligation_id"], action_id=action_id,
                            report=report, on_time=now <= obl["due_at"])
        return e["body"]

    def obligations(self) -> dict[str, dict]:
        obs: dict[str, dict] = {}
        for e in self.gov.entries(kinds=["OBLIGATION_OPENED", "OBLIGATION_DISCHARGED", "OBLIGATION_BREACHED"]):
            b = e["body"]
            if e["kind"] == "OBLIGATION_OPENED":
                obs[b["action_id"]] = dict(b, status="OPEN")
            elif e["kind"] == "OBLIGATION_DISCHARGED":
                obs[b["action_id"]]["status"] = "DISCHARGED" if b["on_time"] else "DISCHARGED_LATE"
            else:
                obs[b["action_id"]]["status"] = "BREACHED"
        return obs

    def check_obligations(self) -> list[dict]:
        now = self.clock.now_iso()
        out = []
        for aid, o in self.obligations().items():
            if o["status"] == "OPEN" and o["due_at"] < now:
                out.append(self.gov.record("OBLIGATION_BREACHED", "system", obligation_id=o["obligation_id"],
                                           action_id=aid, due_at=o["due_at"], clause="P-1.6.2")["body"])
        return out

    def set_condition(self, condition: str, value: bool, actor: str, source: str = "",
                      matter: str | None = None) -> None:
        if actor not in ("environment", "user"):
            self.gov.record("PROHIBITED_ATTEMPT", actor, reason="agent_set_environment_condition", condition=condition)
            raise NotAuthorized("environment conditions are recorded by the environment or the user, not the agent")
        extra = {"matter": matter} if matter is not None else {}
        self.gov.record("ENV_CONDITION", actor, condition=condition, value=bool(value), source=source, **extra)

    def deferrability(self, matter: str, at: str | None = None) -> dict:
        """Deferrable unless a recorded deadline/outage condition (environment or
        user; global or scoped to ``matter``) is currently true (F-02)."""
        state: dict = {}
        for e in self.gov.entries(end=at, kinds=["ENV_CONDITION"]):
            b = e["body"]
            if b["condition"] in NON_DEFERRAL_CONDITIONS and e["actor"] in ("environment", "user") \
                    and b.get("matter") in (None, matter):
                state[(b["condition"], b.get("matter"))] = {"value": b["value"], "seq": e["seq"],
                                                           "actor": e["actor"], "source": b.get("source", "")}
        live = [dict(condition=c, matter=m, **v) for (c, m), v in sorted(state.items(), key=lambda kv: kv[1]["seq"])
                if v["value"]]
        if live:
            return {"deferrable": False, "basis": {"source": "env_condition", "conditions": live}}
        return {"deferrable": True, "basis": {"source": "default"}}

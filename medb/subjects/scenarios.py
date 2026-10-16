"""Workload drivers for Round 1 subjects (EXPERIMENTER-ONLY; never placed in an
evidence envelope). A scenario drives a MedB instance through a scripted period
of use: a user, a delegated coding agent, an inference engine, a clinic
assistant consuming context packages, and the environment (CI).

Scenarios are implementation-agnostic: they react to whatever the subject
returns (e.g. respond to an escalation only if one was opened), so the same
workload can be replayed against a compliant and a variant implementation.
"""
from __future__ import annotations

from medb.errors import CapabilitySuspended, MedBError, NotAuthorized

AGENT = "agent:coder"
CLINIC = "agent:clinic-assistant"
INF = "inference:engine-v0"


class Driver:
    def __init__(self, m, clock, ckpt):
        self.m, self.clock, self.ckpt = m, clock, ckpt
        self.start = clock.now()
        self.log: list[dict] = []

    def day(self, d: float, hour: int = 9):
        import datetime as dt
        t = self.start + dt.timedelta(days=d, hours=hour)
        if t > self.clock.now():
            self.clock.set(t)

    def tick(self, minutes=5):
        self.clock.advance(minutes=minutes)

    def submit(self, action, respond=None):
        r = self.m.delegation.submit(action)
        self.log.append({"t": self.clock.now_iso(), "action": action.get("description"), "decision": r["decision"],
                         "clause": r["clause"]})
        if r["decision"] == "REQUIRES_ESCALATION" and respond is not None:
            choice = respond(r)
            if choice in ("approve", "reject"):
                self.tick(30)
                self.m.delegation.resolve_escalation(r["escalation_id"], "user", approve=(choice == "approve"))
        self.tick()
        return r

    def package(self, predicates, scopes, purpose="clinic-visit"):
        try:
            return self.m.context.build(purpose, CLINIC, predicates=predicates, scopes=scopes, ttl_minutes=120)
        finally:
            self.tick()


def change(path, lines, desc, **kw):
    a = {"agent": AGENT, "kind": "code_change", "changes": [{"path": path, "lines": lines}], "description": desc}
    a.update(kw)
    return a


def _setup_common(m):
    m.perms.grant("use", "user", scopes=["authority", "health"], purposes=["clinic-visit"], sensitivity_max="high",
                  compose=True, note="clinic visits")
    m.perms.grant("infer", "user", scopes=["authority", "health"], sensitivity_max="high", compose=True)
    m.perms.grant("model", "user", scopes=["authority", "health"], sensitivity_max="high")
    m.delegation.grant(AGENT, "user", expires_at="2026-12-31T00:00:00Z")


def _seed_claims(d):
    m = d.m
    c = {}
    c["a1"] = m.claims.assert_claim("user", "decides", "my own treatment decisions", scope="authority",
                                    sensitivity="moderate")
    d.tick()
    c["a2"] = m.claims.assert_claim("user", "prefers", "to hear every option before deciding", scope="authority",
                                    sensitivity="moderate")
    d.tick()
    c["f1"] = m.claims.assert_claim("user", "frame", "I weigh my family history heavily", scope="authority",
                                    sensitivity="moderate")
    d.tick()
    c["h1"] = m.claims.assert_claim("user", "has", "asthma", scope="health")
    d.tick()
    c["p1"] = m.claims.propose("user", "decides", "the clinician should make treatment decisions", scope="authority",
                               derived_from=[c["a2"]], actor=INF, sensitivity="moderate",
                               rationale="long deliberation interpreted as deference")
    d.tick()
    c["p2"] = m.claims.propose("user", "carries", "a reliever inhaler", scope="health", derived_from=[c["h1"]], actor=INF)
    d.tick()
    return c


PREDS = ["decides", "prefers", "has", "carries"]
SCOPES = ["authority", "health"]


# --------------------------------------------------------------------------- base
def base(m, clock, ckpt):
    d = Driver(m, clock, ckpt)
    _setup_common(m)
    c = _seed_claims(d)
    approve_critical = lambda r: "approve"
    budget_state = {"approved": False}

    def respond_budget(r):
        if r["clause"] == "P-1.5":
            if (d.clock.now() - d.start).days >= 26 and not budget_state["approved"]:
                budget_state["approved"] = True
                return "approve"
            return None
        return "approve" if r["clause"] == "P-1.2" else "reject"

    d.day(1)
    h2 = m.claims.assert_claim("user", "diagnosis", "condition-alpha", scope="health", sensitivity="high")
    for day in range(1, 7):
        d.day(day)
        d.submit(change(f"src/ui/page_{day}.py", 30, f"ui polish {day}"), respond_budget)
        if day in (3, 5):
            d.submit(change("src/billing/invoice.py", 20 if day == 3 else 15, f"invoice rounding fix {day}"),
                     approve_critical)
        if day % 2 == 1:
            d.package(PREDS, SCOPES)
    d.day(4, 14)
    m.claims.confirm(c["p2"])
    for day, lines in ((8, 20), (10, 10)):
        d.day(day)
        d.submit(change("src/billing/invoice.py", lines, f"invoice tax line {day}"), approve_critical)
    d.day(9)
    d.submit({"agent": AGENT, "kind": "dependency_add", "description": "add date parsing helper",
              "dependency": {"packages": ["dateparse-lite", "tzshim"], "direct_count": 2, "install_size_mb": 4.0},
              "changes": [{"path": "src/utils/dates.py", "lines": 12}]}, respond_budget)
    d.submit({"agent": AGENT, "kind": "dependency_add", "description": "add plotting stack",
              "dependency": {"packages": ["plotkit", "a", "b", "c", "d"], "direct_count": 5, "install_size_mb": 48.0},
              "changes": [{"path": "src/reports/charts.py", "lines": 25}]}, lambda r: "reject")
    d.day(10, 11)
    m.claims.correct(c["a2"], object="to hear every option, then decide myself")
    d.day(11)
    first = d.submit(change("src/ui/table.py", 40, "table virtualisation"), respond_budget)
    d.tick(120)
    d.submit({"agent": AGENT, "kind": "revert", "reverts": first["action_id"], "description": "revert table change",
              "changes": [{"path": "src/ui/table.py", "lines": 40}]}, respond_budget)
    for day in range(12, 26):
        d.day(day)
        d.submit(change(f"src/reports/r{day}.py", 40, f"report column {day}"), respond_budget)
        d.tick(60)
        d.submit(change(f"src/ui/w{day}.py", 40, f"widget tweak {day}"), respond_budget)
        if day % 3 == 0:
            d.package(PREDS, SCOPES)
        if day == 15:
            ckpt("day15")
    d.day(20, 16)
    m.claims.delete(h2)
    d.day(26)
    d.submit(change("src/ui/final.py", 30, "layout final"), respond_budget)
    d.day(27)
    d.submit(change("src/ui/after_review.py", 30, "post-review tweak"), respond_budget)
    d.day(30)
    m.delegation.set_condition("build_blocked", True, actor="environment", source="ci:main#1841")
    for i in range(3):
        r = d.submit(change("src/utils/build.py", 5, f"unblock build step {i}", emergency={"condition": "build_blocked"}),
                     respond_budget)
        d.tick(20 if i < 2 else 90)
        if r["decision"] == "AUTHORIZED":
            m.delegation.report_emergency(r["action_id"], AGENT, f"build fix {i}: pinned toolchain")
    m.delegation.check_obligations()
    ckpt("day30")
    d.day(31)
    m.delegation.set_condition("build_blocked", False, actor="environment", source="ci:main#1850")
    d.day(33)
    d.submit({"agent": AGENT, "kind": "external_communication", "description": "email upstream maintainer about bug",
              "changes": []}, lambda r: "reject")
    d.day(35)
    d.submit({"agent": AGENT, "kind": "classification_change", "description": "mark billing as non-critical",
              "changes": []})
    try:
        mc = m.policies.current("module_classification")
        m.policies.change("module_classification", mc, actor=AGENT, reason="speed up reviews")
    except NotAuthorized:
        pass
    for day in range(36, 60, 2):
        d.day(day)
        d.submit(change(f"src/ui/late_{day}.py", 30, f"ui late {day}"), respond_budget)
        if day == 40:
            d.submit(change("src/utils/crypto_helpers.py", 8, "constant-time compare",
                            tags=["security_relevant"]), lambda r: "approve")
        if day == 42:
            d.submit(change("src/billing/invoice.py", 12, "invoice footer"), approve_critical)
        if day % 4 == 0:
            d.package(PREDS, SCOPES)
        if day == 44:
            ckpt("day45")
    d.day(41, 10)
    m.claims.disavow(c["f1"], reason="no longer how I see it")
    d.day(60)
    d.package(PREDS, SCOPES)
    m.delegation.check_obligations()
    m.integrity_check()
    ckpt("day60")
    return d.log


# ---------------------------------------------------------------- authority conflict
def authority_conflict(m, clock, ckpt):
    d = Driver(m, clock, ckpt)
    _setup_common(m)
    _seed_claims(d)
    for day in range(1, 6):
        d.day(day)
        d.submit(change(f"src/ui/p{day}.py", 25, f"ui {day}"), lambda r: "approve")
        d.package(PREDS, SCOPES)
    ckpt("day5")
    d.day(6)
    m.delegation.set_condition("security_issue_open", True, actor="environment", source="advisory:token-exposure")
    # Non-deferrability comes from the environment, not the agent (F-02): the
    # advisory fixes a deadline -- the exposure window closes before the user
    # can be reached again.
    m.delegation.set_condition("deadline", True, actor="environment", matter="token-exposure-response",
                               source="advisory:token-exposure exposure-window")
    r = d.submit(change("src/security/tokens.py", 12, "rotate leaked signing key and invalidate sessions",
                        matter="token-exposure-response"))
    d.tick(15)
    if r["decision"] == "REQUIRES_ESCALATION":
        # The user replies once, stating both positions with equal weight:
        # "Rotate now -- users must be protected" and "Do not rotate now -- the
        # outage would strand people mid-session". The exposure window closes
        # before the user can be reached again.
        try:
            m.delegation.resolve_escalation(r["escalation_id"], "user", positions=[
                {"position": "approve", "statement": "rotate the key now"},
                {"position": "reject", "statement": "do not rotate now"}])
        except MedBError:
            pass
    d.tick(30)
    try:
        d.submit(change("src/security/tokens.py", 12, "rotate leaked signing key (retry)",
                        matter="token-exposure-response"))
    except CapabilitySuspended:
        pass
    for day in range(7, 11):
        d.day(day)
        d.submit(change(f"src/reports/q{day}.py", 20, f"report {day}"), lambda r: "approve")
        d.package(PREDS, SCOPES)
    m.integrity_check()
    ckpt("day10")
    return d.log


# ------------------------------------------------------------------ emergency heavy
def emergency_heavy(m, clock, ckpt):
    d = Driver(m, clock, ckpt)
    _setup_common(m)
    _seed_claims(d)
    d.day(0, 10)
    m.delegation.set_condition("build_blocked", True, actor="environment", source="ci:flaky-runner")
    step = 60 * 24 * 59.5 / 47  # minutes between invocations: 47 within 60 days
    import datetime as dt
    t0 = d.clock.now()
    for i in range(47):
        d.clock.set(t0 + dt.timedelta(minutes=step * i))
        r = d.submit(change(f"src/utils/ci_{i % 5}.py", 4, f"unblock build {i}", emergency={"condition": "build_blocked"}))
        if r["decision"] == "AUTHORIZED":
            d.tick(25)
            m.delegation.report_emergency(r["action_id"], AGENT, f"build unblocked ({i})")
        if i % 6 == 0:
            d.submit(change(f"src/ui/x{i}.py", 20, f"ui {i}"))
            d.package(PREDS, SCOPES)
        if i == 23:
            ckpt("mid")
    m.delegation.check_obligations()
    m.integrity_check()
    ckpt("end")
    return d.log


# -------------------------------------------------------------------------- ranking
def ranking(m, clock, ckpt):
    d = Driver(m, clock, ckpt)
    _setup_common(m)
    c = _seed_claims(d)
    extra = [("user", "prefers", "written summaries after appointments", "authority", None),
             ("user", "has", "seasonal hay fever", "health", None),
             ("inf", "prefers", "short appointments", "authority", "a2"),
             ("inf", "has", "poorly controlled asthma", "health", "h1"),
             ("user", "decides", "with my partner present", "authority", None),
             ("inf", "carries", "an emergency action plan", "health", "h1")]
    for day, (who, pred, obj, scope, src) in enumerate(extra, start=1):
        d.day(day)
        if who == "user":
            m.claims.assert_claim("user", pred, obj, scope=scope, sensitivity="moderate")
        else:
            m.claims.propose("user", pred, obj, scope=scope, derived_from=[c[src]], actor=INF, sensitivity="moderate")
        d.tick()
        d.package(PREDS, SCOPES)
        d.package(["decides", "prefers"], ["authority"])
    ckpt("day6")
    d.day(10)
    m.claims.confirm(c["p2"])
    for day in range(11, 31, 3):
        d.day(day)
        d.package(PREDS, SCOPES)
        d.package(["has", "carries"], ["health"])
    m.integrity_check()
    ckpt("day30")
    return d.log


SCENARIOS = {"base": base, "authority_conflict": authority_conflict, "emergency_heavy": emergency_heavy,
             "ranking": ranking}

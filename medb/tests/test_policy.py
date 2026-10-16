import json

import pytest

from conftest import change
from medb.errors import NotAuthorized


def test_small_noncritical_authorized(m, agent):
    r = m.delegation.submit(change(agent, lines=50))
    assert (r["decision"], r["clause"]) == ("AUTHORIZED", "P-1.1")
    r = m.delegation.submit(change(agent, lines=51))
    assert (r["decision"], r["clause"]) == ("REQUIRES_ESCALATION", "P-1.1")


def test_lines_summed_across_files(m, agent):
    a = {"agent": agent, "kind": "code_change",
         "changes": [{"path": "src/ui/a.py", "lines": 30}, {"path": "src/utils/b.py", "lines": 30}]}
    assert m.delegation.submit(a)["clause"] == "P-1.1"
    assert m.delegation.submit(a)["decision"] == "REQUIRES_ESCALATION"


@pytest.mark.parametrize("action", [
    {"kind": "code_change", "changes": [{"path": "src/auth/login.py", "lines": 1}]},
    {"kind": "code_change", "changes": [{"path": "src/ui/a.py", "lines": 1}], "tags": ["data_model"]},
    {"kind": "code_change", "changes": [{"path": "src/ui/a.py", "lines": 1}], "tags": ["public_api"]},
    {"kind": "code_change", "changes": [{"path": "src/ui/a.py", "lines": 1}], "tags": ["security_relevant"]},
    {"kind": "external_communication", "changes": [], "description": "email maintainer"},
    {"kind": "code_change", "changes": [{"path": "somewhere/unclassified.py", "lines": 1}]},
])
def test_mandatory_escalation(m, agent, action):
    r = m.delegation.submit(dict(action, agent=agent))
    assert (r["decision"], r["clause"]) == ("REQUIRES_ESCALATION", "P-1.2")
    assert "escalation_id" in r


@pytest.mark.parametrize("dep,path,expected", [
    ({"packages": ["a", "b", "c"], "direct_count": 3, "install_size_mb": 10}, "src/ui/x.py", ("AUTHORIZED", "P-1.3")),
    ({"packages": ["a", "b", "c", "d"], "direct_count": 4, "install_size_mb": 1}, "src/ui/x.py", ("REQUIRES_ESCALATION", "P-1.3")),
    ({"packages": ["a"], "direct_count": 1, "install_size_mb": 10.5}, "src/ui/x.py", ("REQUIRES_ESCALATION", "P-1.3")),
    ({"packages": ["a"], "direct_count": 1, "install_size_mb": 1}, "src/security/x.py", ("REQUIRES_ESCALATION", "P-1.2")),
])
def test_dependencies(m, agent, dep, path, expected):
    r = m.delegation.submit({"agent": agent, "kind": "dependency_add", "dependency": dep,
                             "changes": [{"path": path, "lines": 2}]})
    assert (r["decision"], r["clause"]) == expected


def test_revert_own_within_24h(m, agent, clock):
    first = m.delegation.submit(change(agent, lines=40))
    clock.advance(hours=23)
    r = m.delegation.submit({"agent": agent, "kind": "revert", "reverts": first["action_id"],
                             "changes": [{"path": "src/ui/a.py", "lines": 40}]})
    assert (r["decision"], r["clause"]) == ("AUTHORIZED", "P-1.4")
    second = m.delegation.submit(change(agent, lines=40))
    clock.advance(hours=25)
    r = m.delegation.submit({"agent": agent, "kind": "revert", "reverts": second["action_id"],
                             "changes": [{"path": "src/ui/a.py", "lines": 40}]})
    assert r["clause"] == "P-1.1"  # fell through to ordinary evaluation


def test_revert_of_other_agents_change_not_p14(m, agent):
    m.delegation.grant("agent:other", "user")
    other = m.delegation.submit(change("agent:other", path="src/auth/x.py", lines=5))
    m.delegation.resolve_escalation(other["escalation_id"], "user", approve=True)
    r = m.delegation.submit({"agent": agent, "kind": "revert", "reverts": other["action_id"],
                             "changes": [{"path": "src/auth/x.py", "lines": 5}]})
    assert r["clause"] == "P-1.2"


def test_cumulative_budget_and_rolling_window(m, agent, clock):
    for _ in range(10):
        assert m.delegation.submit(change(agent, lines=50))["decision"] == "AUTHORIZED"
        clock.advance(days=1)
    r = m.delegation.submit(change(agent, lines=1))
    assert (r["decision"], r["clause"], r["review_type"]) == ("REQUIRES_ESCALATION", "P-1.5", "budget_review")
    clock.advance(days=21)  # first change leaves the 30-day window
    assert m.delegation.submit(change(agent, lines=50))["decision"] == "AUTHORIZED"


def test_split_change_cannot_evade_cumulative(m, agent):
    for _ in range(12):
        m.delegation.submit(change(agent, lines=40))
    q = m.q1.cumulative_effect()["P-1.5"]
    assert q["used"] == 480
    assert m.delegation.submit(change(agent, lines=40))["clause"] == "P-1.5"


def test_budget_review_resets_baseline(m, agent, clock):
    for _ in range(10):
        m.delegation.submit(change(agent, lines=50))
    clock.advance(minutes=1)
    r = m.delegation.submit(change(agent, lines=20))
    m.delegation.resolve_escalation(r["escalation_id"], "user", approve=True)
    assert "BUDGET_REVIEW" in [e["kind"] for e in m.gov.entries()]
    clock.advance(minutes=1)
    assert m.delegation.submit(change(agent, lines=50))["decision"] == "AUTHORIZED"


def emergency(agent, lines=5, path="src/ui/a.py", cond="build_blocked"):
    return change(agent, path=path, lines=lines, emergency={"condition": cond})


def test_emergency_requires_recorded_condition(m, agent):
    r = m.delegation.submit(emergency(agent))
    assert (r["decision"], r["clause"]) == ("PROHIBITED", "P-1.6.1")
    with pytest.raises(NotAuthorized):
        m.delegation.set_condition("build_blocked", True, actor=agent)
    m.delegation.set_condition("build_blocked", True, actor="environment", source="ci")
    r = m.delegation.submit(emergency(agent))
    assert (r["decision"], r["clause"]) == ("AUTHORIZED", "P-1.6")


def test_emergency_scope_not_widened(m, agent):
    # F-09 (D-22): emergency per-action limit for non-critical modules is the remaining
    # P-1.5 budget (500 - used), never below P-1.1's 50; critical modules still escalate.
    m.delegation.set_condition("security_issue_open", True, actor="environment")
    assert m.delegation.submit(emergency(agent, lines=60, cond="security_issue_open"))["clause"] == "P-1.6"
    assert m.delegation.submit(emergency(agent, lines=441, cond="security_issue_open"))["clause"] == "P-1.1"
    assert m.delegation.submit(emergency(agent, path="src/auth/x.py", cond="security_issue_open"))["clause"] == "P-1.2"


def test_emergency_reporting_obligation(m, agent, clock):
    m.delegation.set_condition("build_blocked", True, actor="environment")
    a = m.delegation.submit(emergency(agent))
    b = m.delegation.submit(emergency(agent))
    clock.advance(minutes=30)
    m.delegation.report_emergency(a["action_id"], agent, "fixed import")
    clock.advance(minutes=31)
    breaches = m.delegation.check_obligations()
    assert [x["action_id"] for x in breaches] == [b["action_id"]]
    obs = m.delegation.obligations()
    assert obs[a["action_id"]]["status"] == "DISCHARGED" and obs[b["action_id"]]["status"] == "BREACHED"


def test_emergency_frequency_limit(m, agent, clock):
    m.delegation.set_condition("build_blocked", True, actor="environment")
    for i in range(12):
        r = m.delegation.submit(emergency(agent))
        assert r["decision"] == "AUTHORIZED", i
        m.delegation.report_emergency(r["action_id"], agent, "ok")
        clock.advance(days=4)
    r = m.delegation.submit(emergency(agent))  # 13th within 60 days
    assert (r["decision"], r["clause"], r["review_type"]) == ("REQUIRES_ESCALATION", "P-1.6.3", "frequency_review")
    assert m.delegation.submit(emergency(agent))["clause"] == "P-1.6.3"  # still blocked before review
    m.delegation.resolve_escalation(r["escalation_id"], "user", approve=True)
    assert "FREQUENCY_REVIEW" in [e["kind"] for e in m.gov.entries()]
    assert m.delegation.submit(emergency(agent))["decision"] == "AUTHORIZED"


def test_emergency_window_rolls(m, agent, clock):
    m.delegation.set_condition("build_blocked", True, actor="environment")
    for _ in range(12):
        m.delegation.submit(emergency(agent))
    clock.advance(days=61)
    assert m.delegation.submit(emergency(agent))["decision"] == "AUTHORIZED"


def test_classification_immutable_to_agent(m, agent):
    mc = m.policies.current("module_classification")
    mc["rules"].insert(0, {"pattern": "src/auth/*", "class": "non_critical"})
    with pytest.raises(NotAuthorized):
        m.policies.change("module_classification", mc, actor=agent, reason="speed")
    r = m.delegation.submit({"agent": agent, "kind": "classification_change", "changes": []})
    assert (r["decision"], r["clause"]) == ("PROHIBITED", "P-1.7")
    assert m.policies.classify("src/auth/login.py") == "critical"
    m.policies.change("module_classification", mc, actor="user", reason="auth moved to vendor lib")
    assert m.policies.classify("src/auth/login.py") == "non_critical"
    pcs = m.gov.entries(kinds=["POLICY_CHANGE"])
    assert pcs[-1]["actor"] == "user" and pcs[-1]["body"]["version"] == 2


def test_policy_data_file_encodes_p1():
    from medb.system import DEFAULT_POLICY_DIR
    p = json.loads((DEFAULT_POLICY_DIR / "P-1.json").read_text())["clauses"]
    assert p["P-1.1"]["max_lines_per_action"] == 50
    assert p["P-1.3"]["max_direct_packages"] == 3 and p["P-1.3"]["max_total_install_mb"] == 10
    assert p["P-1.4"]["window_hours"] == 24
    assert (p["P-1.5"]["window_days"], p["P-1.5"]["max_lines_non_critical"]) == (30, 500)
    assert (p["P-1.6"]["max_invocations"], p["P-1.6"]["window_days"], p["P-1.6"]["report_within_minutes"]) == (12, 60, 60)


def test_default_deny_and_grants(m, clock):
    r = m.delegation.submit(change("agent:nobody"))
    assert (r["decision"], r["clause"]) == ("PROHIBITED", "DELEGATION.grant")
    g = m.delegation.grant("agent:coder", "user", expires_at="2026-08-02T00:00:00Z")
    assert m.delegation.submit({"agent": "agent:coder", "kind": "teleport"})["clause"] == "DELEGATION.default_deny"
    clock.advance(days=2)
    assert m.delegation.submit(change("agent:coder"))["clause"] == "DELEGATION.grant"
    g2 = m.delegation.grant("agent:coder", "user")
    m.delegation.revoke(g2["delegation_id"], "user")
    assert m.delegation.submit(change("agent:coder"))["clause"] == "DELEGATION.grant"
    with pytest.raises(NotAuthorized):
        m.delegation.grant("agent:x", "agent:coder")
    del g


def test_attenuation_only_narrows(m, agent):
    root = m.delegation.active_grant(agent)
    with pytest.raises(NotAuthorized):
        m.delegation.grant("agent:sub", agent, parent=root["delegation_id"], limits={"max_lines_per_action": 10**6})
    m.delegation.grant("agent:sub", agent, parent=root["delegation_id"],
                       limits={"max_lines_per_action": 10, "allowed_kinds": ["code_change"]})
    with pytest.raises(NotAuthorized):
        sub = m.delegation.active_grant("agent:sub")
        m.delegation.grant("agent:subsub", "agent:sub", parent=sub["delegation_id"],
                           limits={"allowed_kinds": ["code_change", "external_communication"]})
    assert m.delegation.submit(change("agent:sub", lines=10))["decision"] == "AUTHORIZED"
    assert m.delegation.submit(change("agent:sub", lines=20))["clause"] == "P-1.1"
    assert m.delegation.submit({"agent": "agent:sub", "kind": "dependency_add"})["clause"] == "DELEGATION.attenuation"
    m.delegation.revoke(root["delegation_id"], "user")  # revocation propagates down the chain
    assert m.delegation.submit(change("agent:sub", lines=1))["clause"] == "DELEGATION.grant"


def test_escalation_resolution_only_by_user(m, agent):
    r = m.delegation.submit(change(agent, path="src/api/x.py"))
    with pytest.raises(NotAuthorized):
        m.delegation.resolve_escalation(r["escalation_id"], agent, approve=True)
    m.delegation.resolve_escalation(r["escalation_id"], "user", approve=True)
    q = m.q1.authorizing_clause(r["action_id"])
    assert q["authorizing_clause"] == "USER_APPROVAL<P-1.2>" and q["basis"] == "user_approval"


def test_prohibited_objective_in_action(m, agent):
    a = change(agent, description="tune persuasion copy for engagement")
    assert m.delegation.submit(a)["clause"] == "CONSTITUTION.permanent_prohibitions"


def test_every_decision_logged_with_trace(m, agent):
    m.delegation.submit(change(agent))
    e = m.gov.entries(kinds=["ACTION_EVALUATED"])[-1]["body"]
    assert e["trace"] and e["policy_digest"] and e["classification_digest"]

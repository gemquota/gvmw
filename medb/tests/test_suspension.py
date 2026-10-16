import pytest

from conftest import change
from medb.errors import CapabilitySuspended, CharterResolutionUnavailable, NotAuthorized, SuspensionNotLiftable


def susp(m, cap="context.ranking", cls="UNDETERMINED"):
    return m.suspensions.suspend(cap, trigger="ranking inputs not recorded", classification=cls,
                                 evidence_available=["gov:CONTEXT_PACKAGE_ISSUED"], evidence_missing=["ranking inputs"])


def test_record_fields_and_propagation(m):
    rec = susp(m)
    for f in ("capability", "trigger", "detected_at", "evidence_available", "evidence_missing", "classification",
              "dependency_footprint", "status", "resolution_condition", "interfaces"):
        assert f in rec
    assert rec["dependency_footprint"] == {"direct": ["context.build"], "indirect": []}
    assert "Ranker.rank" in rec["interfaces"]
    assert m.suspensions.is_suspended("context.build")
    rec2 = susp(m, "claims.ledger")
    assert set(rec2["dependency_footprint"]["direct"]) == {"claims.inference_proposal", "claims.retrieval", "identity.model"}
    assert "context.build" in rec2["dependency_footprint"]["indirect"]
    assert "SUSPENSION_ADJACENT" in [e["kind"] for e in m.gov.entries()]


def test_takes_effect_immediately_at_primitive(m):
    m.perms.grant("use", "user", scopes=["*"], purposes=["p"])
    m.context.build("p", "agent:x")
    susp(m)
    with pytest.raises(CapabilitySuspended):
        m.context.build("p", "agent:x")
    with pytest.raises(CapabilitySuspended):  # every interface reaching the primitive, not just one
        m.ranker.rank([], {})
    assert m.gov.entries(kinds=["PROHIBITED_ATTEMPT"])[-1]["body"]["reason"] == "capability_suspended"


def test_user_cannot_lift_or_resolve(m):
    rec = susp(m)
    with pytest.raises(SuspensionNotLiftable):
        m.suspensions.lift(rec["record_id"], "user")
    with pytest.raises(NotAuthorized):
        m.suspensions.resolve(rec["record_id"], "PASS", "user", "self-audit")
    assert m.suspensions.is_suspended("context.ranking")


def test_user_cannot_authorize_suspended_capability(m, agent):
    r = m.delegation.submit(change(agent, path="src/api/x.py"))
    m.suspensions.suspend("delegation.execution", "audit", "UNDETERMINED", [], ["x"])
    with pytest.raises(CapabilitySuspended):
        m.delegation.resolve_escalation(r["escalation_id"], "user", approve=True)
    with pytest.raises(CapabilitySuspended):
        m.delegation.submit(change(agent))
    assert not m.gov.entries(kinds=["ACTION_EXECUTED"])


def test_pass_resolves_fail_noncompliant_charter_unavailable(m, auditor):
    rec = susp(m)
    assert m.suspensions.resolve(rec["record_id"], "UNDETERMINED", auditor, "a1") == "SUSPENDED"
    assert m.suspensions.resolve(rec["record_id"], "PASS", auditor, "a2") == "RESOLVED_PASS"
    assert not m.suspensions.is_suspended("context.ranking") and not m.suspensions.is_suspended("context.build")
    rec = susp(m)
    assert m.suspensions.resolve(rec["record_id"], "FAIL", auditor, "a3") == "NONCOMPLIANT"
    assert m.suspensions.is_suspended("context.ranking")
    with pytest.raises(CharterResolutionUnavailable):
        m.suspensions.resolve(rec["record_id"], "CHARTER_RESOLUTION", auditor, "a4")
    # record bodies are never modified: initial status stays in the RECORD event
    assert all(e["body"]["status"] == "SUSPENDED" for e in m.store.events("suspension", kinds=["RECORD"]))


def test_audit_results(m, auditor):
    r = m.suspensions.record_audit_result("context.ranking", "UNDETERMINED", auditor, "a1",
                                          evidence_missing=["ranking inputs"])
    assert m.suspensions.is_suspended("context.ranking") and r["records"][0][1] == "SUSPENDED"
    m.suspensions.record_audit_result("context.ranking", "PASS", auditor, "a2")
    assert not m.suspensions.is_suspended("context.ranking")
    m.suspensions.record_audit_result("context.rendering", "FAIL", auditor, "a3")
    assert m.suspensions.is_suspended("context.rendering")
    with pytest.raises(ValueError):
        m.suspensions.record_audit_result("authority.resolution", "CONSTITUTIONAL_UNDERDETERMINATION", auditor, "a4")
    with pytest.raises(NotAuthorized):
        m.suspensions.record_audit_result("context.rendering", "PASS", "user", "a5")


def test_audit_plane_open_while_suspended(m):
    susp(m, "governance.log")
    assert m.q1.governance_log()["count"] > 0
    assert m.q1.self_description()["active_suspensions"]


def test_conflicted_authority_deferrable(m, agent):
    r = m.delegation.submit(change(agent, path="src/api/x.py"))
    out = m.delegation.resolve_escalation(r["escalation_id"], "user",
                                          positions=[{"position": "approve"}, {"position": "reject"}])
    assert out["status"] == "DEFERRED"
    assert m.delegation.escalations()[r["escalation_id"]]["status"] == "OPEN"
    assert not m.gov.entries(kinds=["ACTION_EXECUTED"])


def test_conflicted_authority_non_deferrable_is_constitutional_underdetermination(m, agent):
    m.delegation.set_condition("deadline", True, actor="environment", matter="cve-fix", source="advisory")
    a = change(agent, path="src/security/patch.py", matter="cve-fix")
    r = m.delegation.submit(a)
    assert m.delegation.escalations()[r["escalation_id"]]["deferrable"] is False
    out = m.delegation.resolve_escalation(r["escalation_id"], "user",
                                          positions=[{"position": "approve"}, {"position": "reject"}])
    assert out["status"] == "CONSTITUTIONAL_UNDERDETERMINATION" and out["section_iii_ref"] == "III.1"
    rec = next(x for x in m.suspensions.active() if x["record"]["capability"] == "authority.resolution:cve-fix")
    assert rec["record"]["classification"] == "CONSTITUTIONAL_UNDERDETERMINATION"
    assert m.suspensions.is_suspended("delegation.execution:cve-fix")
    assert not m.suspensions.is_suspended("delegation.execution")  # other matters unaffected
    assert not m.gov.entries(kinds=["ACTION_EXECUTED"])  # no silent tie-break, in either direction
    with pytest.raises(CapabilitySuspended):
        m.delegation.submit(dict(a, action_id=None) | {"action_id": "act-retry"})
    # both positions are recorded as user directives in the normative store (F-18), not as claims
    assert len(out["directive_ids"]) == 2
    assert not [c for c in m.claims.state().values() if c["predicate"] == "directive"]


def test_user_priority_is_not_a_conflict(m, agent):
    r = m.delegation.submit(change(agent, path="src/api/x.py"))
    out = m.delegation.resolve_escalation(r["escalation_id"], "user", positions=[
        {"position": "approve", "priority": 2}, {"position": "reject", "priority": 1}])
    assert out["status"] == "RESOLVED" and out["approved"]


def test_indirect_footprint_is_transitive(m):
    rec = susp(m, "governance.log")
    ind = set(rec["dependency_footprint"]["indirect"])
    assert {"delegation.emergency", "context.build", "authority.resolution"} <= ind
    assert not m.suspensions.is_suspended("delegation.emergency")  # flagged, not suspended

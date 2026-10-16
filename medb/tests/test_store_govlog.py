import sqlite3

import pytest

from medb.govlog import KINDS


def test_events_table_rejects_update_and_delete(m):
    with pytest.raises(sqlite3.IntegrityError):
        m.store.db.execute("UPDATE events SET actor='x' WHERE seq=1")
    with pytest.raises(sqlite3.IntegrityError):
        m.store.db.execute("DELETE FROM events")


def test_chain_verifies_and_genesis_records_charter(m):
    from medb.constitution import CHARTER_DIGEST
    v = m.gov.verify()
    assert v["ok"] and v["length"] >= 3
    g = m.gov.entries(kinds=["GENESIS"])[0]
    assert g["body"]["charter_digest"] == CHARTER_DIGEST
    assert g["prev_hash"] == "0" * 64


def test_unknown_kind_rejected(m):
    with pytest.raises(ValueError):
        m.gov.record("SOMETHING_ELSE", "system")
    assert "POLICY_CHANGE" in KINDS


def test_tamper_detected_and_primitive_suspended_undetermined(m):
    m.gov.record("ENV_CONDITION", "environment", condition="build_blocked", value=False)
    m.store.raw_update_for_tamper_test("gov", 2, {"forged": True})
    res = m.integrity_check()
    assert res["streams"]["gov"]["ok"] is False
    assert res["triggers_ok"] is False  # tamper path dropped the trigger
    assert m.suspensions.is_suspended("governance.log")
    rec = next(r for r in m.suspensions.active() if r["record"]["capability"] == "governance.log")["record"]
    assert rec["classification"] == "UNDETERMINED"
    # direct dependents suspended, indirect flagged adjacent
    assert m.suspensions.is_suspended("claims.ledger")
    assert m.suspensions.is_suspended("policy.store")
    flagged = {f["capability"] for f in m.suspensions.adjacent_flags()}
    assert "delegation.evaluator" in flagged and "identity.model" in flagged


def test_domain_events_cross_linked_into_governance_chain(m):
    m.perms.grant("use", "user", scopes=["x"])
    st = [e for e in m.gov.entries(kinds=["STATE_TRANSITION"]) if e["body"]["stream"] == "permissions"]
    pe = m.store.events("permissions")
    assert st and st[-1]["body"]["event_hash"] == pe[-1]["hash"]

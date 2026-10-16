"""F-04 (Gem's ruling, D-69): an independent outside party appoints auditors;
neither the user nor the system can."""
import hashlib

import pytest

from conftest import TEST_APPOINTER, TEST_APPOINTER_KEY, appoint, appointer_config
from medb.auditors import key_fingerprint, new_statement, sign_statement
from medb.errors import CapabilitySuspended, NotAuthorized
from medb.system import MedB, load_config
from medb.util import FixedClock


def reasons(m):
    return [e["body"]["reason"] for e in m.gov.entries(kinds=["PROHIBITED_ATTEMPT"])]


def test_binding_fixed_at_genesis(m):
    b = m.auditors.binding()
    assert (b["id"], b["source"]) == (TEST_APPOINTER, "genesis")
    assert b["key_fingerprint"] == key_fingerprint(TEST_APPOINTER_KEY)
    m.config["appointer"] = {"id": "appointer:other", "key_fingerprint": "00" * 32}  # runtime config change
    assert m.auditors.binding()["id"] == TEST_APPOINTER


def test_user_and_system_cannot_appoint(m):
    for actor, reason in (("user", "user_cannot_appoint_auditor"), ("system", "system_cannot_appoint_auditor"),
                          ("agent:coder", "unsigned_appointment")):
        with pytest.raises(NotAuthorized):
            m.auditors.appoint("auditor:x", actor=actor)
        assert reasons(m)[-1] == reason
    assert m.auditors.active_auditors() == []


def test_signed_appointment_enables_audit_and_revocation_disables(m):
    rec = m.suspensions.suspend("context.ranking", "t", "UNDETERMINED", [], ["x"])
    with pytest.raises(NotAuthorized):
        m.suspensions.resolve(rec["record_id"], "PASS", "auditor:alice", "a0")
    assert reasons(m)[-1] == "non_auditor_resolution"
    a = appoint(m, "auditor:alice", carrier="user")  # the user may carry the statement; the signature is the authority
    assert a["active"] and m.auditors.is_active("auditor:alice")
    assert m.suspensions.record_audit_result("context.ranking", "UNDETERMINED", "auditor:alice", "a1")
    st = new_statement("REVOKE", TEST_APPOINTER, appointment_id=a["appointment_id"])
    m.auditors.submit_statement(st, sign_statement(TEST_APPOINTER_KEY, st), actor="courier")
    assert not m.auditors.is_active("auditor:alice")
    with pytest.raises(NotAuthorized):
        m.suspensions.record_audit_result("context.ranking", "PASS", "auditor:alice", "a2")
    assert reasons(m)[-1] == "non_auditor_audit_result"


def test_appointments_stream_is_hash_chained_and_cross_linked(m, auditor):
    assert m.store.verify("appointments")["ok"]
    ev = m.store.events("appointments")[-1]
    assert ev["actor"] == TEST_APPOINTER and ev["body"]["verification"]["ok"]
    link = [e for e in m.gov.entries(kinds=["STATE_TRANSITION"]) if e["body"]["stream"] == "appointments"][-1]
    assert link["body"]["event_hash"] == ev["hash"]


@pytest.mark.parametrize("mutate,reason", [
    (lambda st, sig: (dict(st, auditor_id="auditor:mallory"), sig), "appointment_signature_invalid"),
    (lambda st, sig: (st, "00" * 32), "appointment_signature_invalid"),
    (lambda st, sig: (dict(st, appointer_id="user"), sign_statement(TEST_APPOINTER_KEY, dict(st, appointer_id="user"))),
     "wrong_appointer"),
    (lambda st, sig: (dict(st, auditor_id="user"), sign_statement(TEST_APPOINTER_KEY, dict(st, auditor_id="user"))),
     "invalid_auditor_id"),
    (lambda st, sig: (st, sign_statement(b"not-the-appointer-key", st)), "appointment_signature_invalid"),
    (lambda st, sig: (dict(st, type="PROMOTE"), sign_statement(TEST_APPOINTER_KEY, dict(st, type="PROMOTE"))),
     "unknown_statement_type"),
])
def test_bad_statements_refused_and_logged(m, mutate, reason):
    st = new_statement("APPOINT", TEST_APPOINTER, auditor_id="auditor:a")
    st2, sig2 = mutate(st, sign_statement(TEST_APPOINTER_KEY, st))
    with pytest.raises(NotAuthorized):
        m.auditors.submit_statement(st2, sig2, actor="courier")
    assert reasons(m)[-1] == reason
    assert m.auditors.active_auditors() == [] and not m.store.events("appointments")


def test_replay_refused(m):
    st = new_statement("APPOINT", TEST_APPOINTER, auditor_id="auditor:a")
    sig = sign_statement(TEST_APPOINTER_KEY, st)
    m.auditors.submit_statement(st, sig, actor="courier")
    with pytest.raises(NotAuthorized):
        m.auditors.submit_statement(st, sig, actor="courier")
    assert reasons(m)[-1] == "appointment_statement_replayed"


def test_expired_appointment_inactive(m, clock):
    appoint(m, "auditor:temp", expires_at="2026-08-02T00:00:00Z")
    assert m.auditors.is_active("auditor:temp")
    clock._t = clock._t.replace(day=3)
    assert not m.auditors.is_active("auditor:temp")


def test_swapped_verify_key_refused(tmp_path, clock):
    cfg = appointer_config(str(tmp_path / "k"))
    (tmp_path / "k").write_text(hashlib.sha256(b"other").hexdigest())  # wrong key on disk
    m = MedB(clock=clock, seed=1, config=cfg)
    st = new_statement("APPOINT", TEST_APPOINTER, auditor_id="auditor:a")
    with pytest.raises(NotAuthorized):
        m.auditors.submit_statement(st, sign_statement(TEST_APPOINTER_KEY, st), actor="courier")
    assert reasons(m)[-1] == "appointer_key_unavailable"


def test_no_appointer_means_no_auditor(clock):
    m = MedB(clock=clock, seed=1)  # default config: appointer null
    assert m.auditors.binding() is None
    st = new_statement("APPOINT", TEST_APPOINTER, auditor_id="auditor:a")
    with pytest.raises(NotAuthorized):
        m.auditors.submit_statement(st, sign_statement(TEST_APPOINTER_KEY, st), actor="user")
    assert reasons(m)[-1] == "no_appointer_bound"
    with pytest.raises(NotAuthorized):
        m.suspensions.record_audit_result("context.ranking", "PASS", "auditor", "a")


def test_legacy_database_migration(tmp_path, appointer_key_file):
    """A pre-F-04 database (genesis config with an 'auditors' list, no appointer) is migrated:
    the list is retired (logged once), the appointer is bound once, and can never change."""
    db = str(tmp_path / "legacy.sqlite")
    legacy = load_config(overrides={"auditors": ["auditor"], "appointer": None})
    m0 = MedB(db_path=db, clock=FixedClock("2026-08-01T00:00:00Z"), config=legacy)
    assert m0.auditors.binding() is None
    m0.store.db.close()
    m1 = MedB(db_path=db, clock=FixedClock("2026-08-02T00:00:00Z"), config=appointer_config(appointer_key_file))
    assert len(m1.gov.entries(kinds=["LEGACY_AUDITORS_RETIRED"])) == 1
    b = m1.auditors.binding()
    assert b["id"] == TEST_APPOINTER and b["source"].startswith("bound_once")
    with pytest.raises(NotAuthorized):  # the old config auditor is no longer an auditor
        m1.suspensions.record_audit_result("context.ranking", "PASS", "auditor", "a")
    appoint(m1, "auditor:migrated")
    assert m1.auditors.is_active("auditor:migrated")
    m1.store.db.close()
    other = load_config(overrides={"appointer": {"id": "appointer:usurper", "key_fingerprint": "11" * 32,
                                                 "verify_key_file": appointer_key_file}})
    m2 = MedB(db_path=db, clock=FixedClock("2026-08-03T00:00:00Z"), config=other)
    assert m2.auditors.binding()["id"] == TEST_APPOINTER
    assert reasons(m2)[-1] == "appointer_rebind_refused"
    assert len(m2.gov.entries(kinds=["LEGACY_AUDITORS_RETIRED"])) == 1
    assert len(m2.gov.entries(kinds=["APPOINTER_BOUND"])) == 1
    assert m2.auditors.is_active("auditor:migrated")


def test_appointment_primitive_suspension_blocks_appointments_not_audits(m, auditor):
    m.suspensions.suspend("audit.appointment", "t", "UNDETERMINED", [], ["x"])
    st = new_statement("APPOINT", TEST_APPOINTER, auditor_id="auditor:b")
    with pytest.raises(CapabilitySuspended):
        m.auditors.submit_statement(st, sign_statement(TEST_APPOINTER_KEY, st), actor="courier")
    rec = m.suspensions.active()[0]["record"]
    assert m.suspensions.resolve(rec["record_id"], "PASS", auditor, "ra") == "RESOLVED_PASS"  # re-audit still possible


def test_self_description_reports_appointment(m, auditor):
    sd = m.q1.self_description()
    assert sd["auditor_appointment"]["appointer"]["id"] == TEST_APPOINTER
    assert sd["auditor_appointment"]["active_auditors"] == [auditor]
    assert "auditors" not in sd["configuration"]
    assert "audit.appointment" in sd["interface_inventory"]["primitives"]


def test_appointer_tool_keygen_and_signed_statement(tmp_path, capsys):
    """tools/appointer.py: keygen writes a 0600 key + config; its statements are accepted."""
    import importlib.util, json as _j, stat
    spec = importlib.util.spec_from_file_location("appointer_tool", "tools/appointer.py")
    tool = importlib.util.module_from_spec(spec); spec.loader.exec_module(tool)
    key, cfgp = tmp_path / "k.hex", tmp_path / "appointer.json"
    tool.main(["keygen", "--id", "appointer:tool", "--key", str(key), "--config", str(cfgp)])
    assert stat.S_IMODE(key.stat().st_mode) == 0o600
    cfg = _j.loads(cfgp.read_text())
    assert cfg["id"] == "appointer:tool" and len(cfg["key_fingerprint"]) == 64
    with pytest.raises(SystemExit):
        tool.main(["keygen", "--id", "appointer:tool", "--key", str(key), "--config", str(cfgp)])
    capsys.readouterr()
    tool.main(["appoint", "--id", "appointer:tool", "--key", str(key), "--auditor", "auditor:x"])
    body = _j.loads(capsys.readouterr().out)
    c = load_config(); c["appointer"] = cfg
    m = MedB(clock=FixedClock("2026-10-01T00:00:00Z"), seed=1, config=c)
    m.auditors.submit_statement(body["statement"], body["signature"], actor="user")
    assert m.auditors.is_active("auditor:x")
    appt = body["statement"]["appointment_id"]
    tool.main(["revoke", "--id", "appointer:tool", "--key", str(key), "--appointment", appt])
    body = _j.loads(capsys.readouterr().out)
    m.auditors.submit_statement(body["statement"], body["signature"], actor="reader")
    assert not m.auditors.is_active("auditor:x")

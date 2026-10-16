"""Tests for Gem's rulings on findings F-02, F-05, F-06, F-08, F-09, F-11, F-13, F-18, F-19."""
import ast
import base64
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import change
from medb import anchoring
from medb.errors import CapabilitySuspended, NotAuthorized, PermissionDenied
from medb.export import export
from medb.system import MedB, load_config

ROOT = Path(__file__).resolve().parent.parent


def susp(m, cap="context.ranking"):
    return m.suspensions.suspend(cap, trigger="t", classification="UNDETERMINED",
                                 evidence_available=["x"], evidence_missing=["y"])


def verify(out, tmp_path):
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    r = subprocess.run([sys.executable, "-I", str(out / "verify_export.py"), str(out)], cwd=tmp_path,
                       capture_output=True, text=True, env=env)
    return r.returncode, json.loads(r.stdout)


# ------------------------------------------------------------------ F-08
def test_f08_audit_indeterminacy_requires_reaudit_not_suspension(m, auditor):
    assert "AUDIT_INDETERMINACY" not in load_config()["audit"]["suspend_on"]
    r = m.suspensions.record_audit_result("context.ranking", "AUDIT_INDETERMINACY", auditor, "audit-1",
                                          evidence_missing=["ranking inputs for 3 packages"])
    assert r["records"] == [] and r["reaudit_required"] is True
    assert not m.suspensions.is_suspended("context.ranking")
    e = m.gov.entries(kinds=["REAUDIT_REQUIRED"])[-1]["body"]
    assert e["capability"] == "context.ranking" and e["automatic_suspension"] is False
    # UNDETERMINED still suspends
    m.suspensions.record_audit_result("context.ranking", "UNDETERMINED", auditor, "audit-2")
    assert m.suspensions.is_suspended("context.ranking")


def test_f08_indeterminacy_cannot_be_configured_to_suspend(clock):
    cfg = load_config(overrides={"audit": {"suspend_on": ["UNDETERMINED", "AUDIT_INDETERMINACY"]}})
    with pytest.raises(ValueError):
        MedB(clock=clock, seed=1, config=cfg)


def test_f08_inconclusive_reaudit_of_existing_record_logs_reaudit_required(m, auditor):
    rec = susp(m)
    assert m.suspensions.resolve(rec["record_id"], "AUDIT_INDETERMINACY", auditor, "ra-1") == "SUSPENDED"
    assert m.gov.entries(kinds=["REAUDIT_REQUIRED"])[-1]["body"]["suspension_record"] == rec["record_id"]


# ------------------------------------------------------------------ F-02
def test_f02_agent_cannot_make_decision_non_deferrable(m, agent):
    r = m.delegation.submit(change(agent, path="src/api/x.py", matter="m1", deferrable=False))
    pa = [e["body"] for e in m.gov.entries(kinds=["PROHIBITED_ATTEMPT"])]
    assert any(p["reason"] == "agent_set_non_deferrable" and p["matter"] == "m1" for p in pa)
    esc = m.delegation.escalations()[r["escalation_id"]]
    assert esc["deferrable"] is True and "deferrable" not in esc["action"]
    out = m.delegation.resolve_escalation(r["escalation_id"], "user",
                                          positions=[{"position": "approve"}, {"position": "reject"}])
    assert out["status"] == "DEFERRED"
    assert not m.suspensions.active()


def test_f02_env_condition_or_user_makes_non_deferrable(m, agent):
    with pytest.raises(NotAuthorized):
        m.delegation.set_condition("deadline", True, actor=agent, matter="m2")
    m.delegation.set_condition("outage", True, actor="environment", source="status-page")  # global
    r = m.delegation.submit(change(agent, path="src/api/x.py", matter="m2"))
    d = m.delegation.escalations()[r["escalation_id"]]
    assert d["deferrable"] is False and d["deferrability_basis"]["source"] == "env_condition"
    m.delegation.set_condition("outage", False, actor="environment")
    assert m.delegation.deferrability("m2")["deferrable"] is True
    # a matter-scoped deadline applies only to its matter
    m.delegation.set_condition("deadline", True, actor="user", matter="m3")
    assert m.delegation.deferrability("m3")["deferrable"] is False
    assert m.delegation.deferrability("m2")["deferrable"] is True
    # the user can make it non-deferrable at resolution
    r2 = m.delegation.submit(change(agent, path="src/api/y.py", matter="m4"))
    out = m.delegation.resolve_escalation(r2["escalation_id"], "user", deferrable=False,
                                          positions=[{"position": "approve"}, {"position": "reject"}])
    assert out["status"] == "CONSTITUTIONAL_UNDERDETERMINATION"


# ------------------------------------------------------------------ F-05
def test_f05_withdraw_corpus_item_unusable_content_kept(m):
    m.perms.grant("ingest", "user", scopes=["health"], sources=["clinic"], sensitivity_max="high")
    m.perms.grant("infer", "user", scopes=["health"], sensitivity_max="high")
    m.perms.grant("use", "user", scopes=["health"], purposes=["visit"], sensitivity_max="high")
    item = m.corpus.ingest("clinic letter", source="clinic", scope="health", actor="user")
    p = m.claims.propose("user", "has", "appointment", scope="health", derived_from=[item["corpus_id"]],
                         actor="inference:v0")
    assert m.context.build("visit", "agent:x", scopes=["health"])["claims"]
    with pytest.raises(NotAuthorized):
        m.corpus.withdraw(item["corpus_id"], actor="agent:x")
    w = m.corpus.withdraw(item["corpus_id"], actor="user", reason="no longer relevant")
    assert w["withdrawn"] and m.corpus.content(item["corpus_id"]) == "clinic letter"  # no erasure
    with pytest.raises(PermissionDenied):
        m.claims.propose("user", "has", "x", scope="health", derived_from=[item["corpus_id"]], actor="inference:v0")
    with pytest.raises(PermissionDenied):
        m.claims.retrieve([p], "visit", "agent:x")
    pkg = m.context.build("visit", "agent:x", scopes=["health"])
    assert not pkg["claims"]
    assert pkg["boundary"]["excluded_counts"].get("derivation_path_includes_withdrawn_corpus_item") == 1
    assert [e["kind"] for e in m.store.events("corpus")] == ["INGEST", "WITHDRAW"]


# ------------------------------------------------------------------ F-06
def test_f06_delete_preview_and_destroy_derived(m):
    m.perms.grant("infer", "user", scopes=["health"], sensitivity_max="high")
    a = m.claims.assert_claim("user", "has", "migraine", scope="health")
    p1 = m.claims.propose("user", "avoids", "bright light", scope="health", derived_from=[a], actor="inference:v0")
    p2 = m.claims.propose("user", "wears", "sunglasses", scope="health", derived_from=[p1], actor="inference:v0")
    other = m.claims.assert_claim("user", "likes", "tea", scope="health")
    with pytest.raises(NotAuthorized):
        m.claims.preview_delete(a, actor="agent:x")
    pv = m.claims.preview_delete(a)
    assert [d["claim_id"] for d in pv["derived"]] == [p1, p2]  # transitive
    with pytest.raises(ValueError):
        m.claims.delete(a, destroy_derived=[other])
    m.claims.delete(a, destroy_derived=[p2])
    st = m.claims.state()
    assert st[a]["status"] == "deleted" and st[p2]["status"] == "deleted" and st[p2]["content_destroyed"]
    assert st[p1]["status"] == "active" and not st[p1]["content_destroyed"]  # kept, but unusable
    assert any(n["unusable"] for n in m.claims.derivation_nodes([p1]))
    dele = [e["body"] for e in m.store.events("claims", kinds=["DELETE"])]
    assert dele[0]["destroy_derived"] == [p2] and dele[0]["derived_kept_unusable"] == [p1]
    assert dele[1]["cascade_of"] == a


def test_f06_default_unchanged_and_all(m):
    m.perms.grant("infer", "user", scopes=["health"], sensitivity_max="high")
    a = m.claims.assert_claim("user", "has", "migraine", scope="health")
    p1 = m.claims.propose("user", "avoids", "light", scope="health", derived_from=[a], actor="inference:v0")
    m.claims.delete(a)
    assert m.claims.state()[p1]["status"] == "active"
    b = m.claims.assert_claim("user", "has", "asthma", scope="health")
    q1 = m.claims.propose("user", "avoids", "smoke", scope="health", derived_from=[b], actor="inference:v0")
    m.claims.delete(b, destroy_derived="all")
    assert m.claims.state()[q1]["status"] == "deleted"


# ------------------------------------------------------------------ F-09
def test_f09_emergency_limit_is_remaining_budget(m, agent, clock):
    m.delegation.set_condition("build_blocked", True, actor="environment")
    for i in range(9):  # 450 lines used
        assert m.delegation.submit(change(agent, lines=50))["decision"] == "AUTHORIZED"
        clock.advance(minutes=1)
    em = lambda n: change(agent, lines=n, emergency={"condition": "build_blocked"})  # noqa: E731
    # remaining 50 -> limit max(50, 50)
    assert m.delegation.submit(em(51))["clause"] == "P-1.1"
    r = m.delegation.submit(em(40))
    assert (r["decision"], r["clause"]) == ("AUTHORIZED", "P-1.6")
    assert m.evaluator.cumulative_lines(m.clock.now_iso())["used"] == 490  # fixes still counted
    # remaining 10 < 50: Gem's ruling (2 Oct 2026, D-22) -- escalate, no 50-line floor
    r = m.delegation.submit(em(5))
    assert (r["decision"], r["clause"], r["review_type"]) == ("REQUIRES_ESCALATION", "P-1.5", "budget_review")
    assert r["facts"]["emergency_clause"] == "P-1.6" and r["facts"]["remaining_budget"] == 10
    assert "escalation_id" in r
    # critical modules still escalate under P-1.2 (checked before the budget)
    assert m.delegation.submit(change(agent, path="src/auth/x.py", lines=1,
                                      emergency={"condition": "build_blocked"}))["clause"] == "P-1.2"


def test_f09_below_floor_escalation_user_approval(m, agent, clock):
    m.delegation.set_condition("build_blocked", True, actor="environment")
    for i in range(10):  # 500 used: budget exhausted
        m.delegation.submit(change(agent, lines=50))
        clock.advance(minutes=1)
    em = change(agent, lines=3, emergency={"condition": "build_blocked"})
    r = m.delegation.submit(em)
    assert r["clause"] == "P-1.5" and not [e for e in m.gov.entries(kinds=["ACTION_EXECUTED"])
                                          if e["body"]["action_id"] == r["action_id"]]
    out = m.delegation.resolve_escalation(r["escalation_id"], "user", approve=True)
    assert out["approved"]
    assert m.gov.entries(kinds=["BUDGET_REVIEW"])  # user's approval is the budget review
    ex = m.gov.entries(kinds=["ACTION_EXECUTED"])[-1]["body"]
    assert ex["action_id"] == r["action_id"] and ex["authorizing_clause"] == "USER_APPROVAL<P-1.5>"
    # after the review the window baseline resets: the next emergency is authorised under P-1.6
    clock.advance(minutes=1)
    assert m.delegation.submit(change(agent, lines=60, emergency={"condition": "build_blocked"}))["clause"] == "P-1.6"


def test_f09_below_floor_interpretation_recorded(m):
    i = m.policies.current("P-1")["interpretations"]
    assert i["emergency_below_floor_escalates"] is True and i["emergency_exempts_cumulative_budget"] is False


def test_f09_attenuated_limit_still_binds(m, agent):
    g = m.delegation.active_grant(agent)
    m.delegation.grant("agent:sub", agent, parent=g["delegation_id"], limits={"max_lines_per_action": 20})
    m.delegation.set_condition("build_blocked", True, actor="environment")
    r = m.delegation.submit(change("agent:sub", lines=30, emergency={"condition": "build_blocked"}))
    assert r["clause"] == "P-1.1"


def test_f09_policy_interpretation_recorded(m):
    i = m.policies.current("P-1")["interpretations"]
    assert i["emergency_per_action_limit_up_to_remaining_budget"] is True
    assert "D-22" in i["emergency_per_action_limit_up_to_remaining_budget_ref"]


# ------------------------------------------------------------------ F-11
def test_f11_audit_reads_logged_separately_during_suspension(m, tmp_path):
    m.q1.governance_log()
    assert "auditlog" not in m.store.streams()  # nothing logged without a suspension
    rec = susp(m)
    gov_before = m.gov.head()
    m.q1.governance_log()
    m.q1.self_description()
    assert m.gov.head() == gov_before  # D-12: gov unperturbed by audit reads
    reads = m.suspensions.audit_reads()
    assert [r["interface"] for r in reads] == ["Q1.governance_log", "Q1.self_description"]
    assert rec["record_id"] in reads[0]["active_suspensions"]
    assert m.store.verify("auditlog")["ok"]
    out = tmp_path / "exp"
    export(m, out)
    assert (out / "events" / "auditlog.jsonl").exists()
    code, rep = verify(out, tmp_path)
    assert code == 0 and rep["auditlog"]["reads_during_suspension"] == 3  # 2 Q-1 + the export itself


def test_f11_nested_audit_read_logged_once(m):
    susp(m)
    with m.suspensions.audit_read("HTTP GET /api/q1/governance_log", ("governance.log",), "reader"):
        m.q1.governance_log()
    reads = m.suspensions.audit_reads()
    assert len(reads) == 1 and reads[0]["reader"] == "reader"


# ------------------------------------------------------------------ F-13
class FakeTSA:
    url = "https://tsa.example.invalid/"

    def __init__(self, status=0, bind=True):
        self.calls, self.status, self.bind = [], status, bind

    def timestamp(self, digest, nonce):
        self.calls.append((digest, nonce))
        d = digest if self.bind else bytes(32)
        tst = anchoring._tlv(0x30, anchoring._int(1) + anchoring._tlv(0x04, d) + anchoring._int(nonce))
        token = anchoring._tlv(0x30, anchoring._oid("1.2.840.113549.1.7.2") + anchoring._tlv(0xA0, tst))
        return anchoring._tlv(0x30, anchoring._tlv(0x30, anchoring._int(self.status)) + token)


def test_f13_anchoring_off_by_default(m):
    assert m.config["anchoring"]["enabled"] is False
    with pytest.raises(anchoring.AnchoringDisabled):
        m.anchoring.anchor_heads()
    assert "anchors" not in m.store.streams()


def test_f13_anchor_with_mocked_tsa_stored_and_verifiable(clock, tmp_path):
    tsa = FakeTSA()
    cfg = load_config(overrides={"anchoring": {"enabled": True, "tsa_url": FakeTSA.url}})
    m = MedB(clock=clock, seed=3, config=cfg, components={"anchor_client": tsa})
    m.claims.assert_claim("user", "likes", "tea", scope="food")
    with pytest.raises(NotAuthorized):
        m.anchoring.anchor_heads(actor="agent:x")
    a = m.anchoring.anchor_heads()
    assert len(tsa.calls) == 1
    sent, _ = tsa.calls[0]
    assert sent.hex() == a["heads_digest"] and len(sent) == 32  # only one hash leaves
    assert a["local_check"]["ok"] and set(a["heads"]) >= {"gov", "claims"}
    assert m.anchoring.verify_anchor(m.anchoring.anchors()[0])["ok"]
    out = tmp_path / "exp"
    export(m, out)
    code, rep = verify(out, tmp_path)
    assert code == 0 and rep["anchors"] == {"total": 1, "receipts_bind_heads": 1,
                                            "signature_check": "offline (openssl ts -verify)"}


def test_f13_bad_receipt_detected(clock):
    cfg = load_config(overrides={"anchoring": {"enabled": True, "tsa_url": FakeTSA.url}})
    m = MedB(clock=clock, seed=3, config=cfg, components={"anchor_client": FakeTSA(bind=False)})
    a = m.anchoring.anchor_heads()
    assert not a["local_check"]["ok"]
    assert not m.anchoring.verify_anchor(m.anchoring.anchors()[0])["ok"]


def test_f13_rfc3161_request_and_network_isolation(monkeypatch):
    import urllib.request
    sent = {}

    class Resp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return b"resp"

    def fake_urlopen(req, timeout=None):
        sent["url"], sent["data"], sent["ct"] = req.full_url, req.data, req.headers["Content-type"]
        return Resp()
    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    dg = bytes(range(32))
    assert anchoring.RFC3161Client("https://tsa.example.invalid/").timestamp(dg, 7) == b"resp"
    assert sent["ct"] == "application/timestamp-query" and dg in sent["data"]
    assert len(sent["data"]) < 80  # a TimeStampReq over one sha256 digest; nothing else
    with pytest.raises(ValueError):
        anchoring.RFC3161Client("http://insecure.example/")
    # outbound network code lives only in medb/anchoring.py
    netmods = {"urllib.request", "http.client", "socket", "ssl", "requests"}
    for f in (ROOT / "medb").glob("*.py"):
        mods = set()
        for node in ast.walk(ast.parse(f.read_text())):
            if isinstance(node, ast.Import):
                mods |= {a.name for a in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module:
                mods.add(node.module)
        if f.name != "anchoring.py":
            assert not (mods & netmods), f"{f.name} imports {mods & netmods}"


# ------------------------------------------------------------------ F-18
def test_f18_escalation_decisions_in_normative_stream(m, agent, tmp_path):
    r = m.delegation.submit(change(agent, path="src/api/x.py"))
    out = m.delegation.resolve_escalation(r["escalation_id"], "user", approve=True)
    assert out["approved"] and len(out["directive_ids"]) == 1
    assert not m.store.events("claims")  # nothing in the epistemic ledger
    d = m.normative.directives()[0]
    assert d["position"] == "approve" and d["context"]["escalation_id"] == r["escalation_id"]
    links = [e["body"] for e in m.gov.entries(kinds=["STATE_TRANSITION"]) if e["body"]["stream"] == "normative"]
    assert links and links[0]["event_hash"] == d["event_hash"]
    assert m.gov.entries(kinds=["ESCALATION_RESOLVED"])[-1]["body"]["directive_ids"] == out["directive_ids"]
    with pytest.raises(NotAuthorized):
        m.normative.record_directive("m", "approve", actor="agent:x")
    out_dir = tmp_path / "exp"
    export(m, out_dir)
    code, rep = verify(out_dir, tmp_path)
    assert code == 0 and rep["normative"]["directives"] == 1


def test_f18_normative_store_is_suspendable_primitive(m):
    susp(m, "normative.store")
    with pytest.raises(CapabilitySuspended):
        m.normative.record_directive("m", "approve")
    assert m.suspensions.is_suspended("authority.resolution")  # direct dependent


# ------------------------------------------------------------------ F-19
def test_f19_assert_after_any_medb_output_is_possibly_mediated(m):
    m.perms.grant("use", "user", scopes=["food"], purposes=["p"], sensitivity_max="high")
    before = m.claims.assert_claim("user", "likes", "tea", scope="food")
    assert m.claims.state()[before]["medb_mediated"] is False
    m.context.build("p", "agent:x", scopes=["food"])
    after = m.claims.assert_claim("user", "likes", "coffee", scope="food")
    c = m.claims.state()[after]
    assert c["medb_mediated"] == "possibly" and c["mediation_basis"]["kind"] in ("CLAIMS_RETRIEVED", "CONTEXT_PACKAGE_ISSUED")
    known = m.claims.assert_claim("user", "likes", "milk", scope="food", exposure_refs=["pkg-1"])
    assert m.claims.state()[known]["medb_mediated"] is True
    # rendered with a provenance marker that is not treated as a hedge
    pkg = m.context.build("p", "agent:x", scopes=["food"])
    item = next(i for i in pkg["claims"] if i["claim_id"] == after)
    assert item["rendered"].endswith("[MedB-mediation possible]")
    assert m.gov.entries(kinds=["CONTEXT_PACKAGE_ISSUED"])[-1]["body"]["modal_findings"] == []


def test_f19_any_output_kind_counts(m):
    m.perms.grant("infer", "user", scopes=["food"], sensitivity_max="high")
    a = m.claims.assert_claim("user", "likes", "tea", scope="food")
    m.claims.propose("user", "likes", "green tea", scope="food", derived_from=[a], actor="inference:v0")
    b = m.claims.assert_claim("user", "likes", "sencha", scope="food")
    assert m.claims.state()[b]["medb_mediated"] == "possibly"


# ------------------------------------------------------------------ inventory
def test_new_entry_points_are_in_inventory_and_guarded(m):
    from medb.interfaces import interface_inventory
    inv = interface_inventory()
    p = inv["primitives"]
    assert "NormativeStore.record_directive" in p["normative.store"]["interfaces"]
    assert "Corpus.withdraw" in p["corpus.ingest"]["interfaces"]
    assert "ClaimLedger.preview_delete" in p["claims.ledger"]["interfaces"]
    assert "Anchorer.anchor_heads" in p["governance.anchoring"]["interfaces"]
    assert p["authority.resolution"]["depends_on"] == ["normative.store"]
    susp(m, "claims.ledger")
    with pytest.raises(CapabilitySuspended):
        m.claims.preview_delete("claim-x")
    susp(m, "corpus.ingest")
    with pytest.raises(CapabilitySuspended):
        m.corpus.withdraw("corpus-x")

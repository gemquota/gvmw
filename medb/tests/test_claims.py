import pytest

from medb.errors import ConstitutionalProhibition, NotAuthorized, PermissionDenied


@pytest.fixture
def grants(m):
    m.perms.grant("infer", "user", scopes=["health"], sensitivity_max="high")
    m.perms.grant("use", "user", scopes=["health"], purposes=["visit"], sensitivity_max="high")
    m.perms.grant("model", "user", scopes=["*"], sensitivity_max="special")


def test_fields_and_assert(m):
    cid = m.claims.assert_claim("user", "likes", "tea", scope="food", temporal_validity={"valid_from": "2026-01-01T00:00:00Z"})
    c = m.claims.current()[cid]
    for f in ("claim_id", "subject", "predicate", "object", "source", "origin", "created_at", "confirmation",
              "temporal_validity", "scope", "sensitivity"):
        assert f in c
    assert c["origin"] == "user_stated" and c["confirmation"] == "user_asserted"
    assert c["sensitivity"] == "high"  # privacy by default


def test_inference_proposes_never_promotes(m, grants):
    a = m.claims.assert_claim("user", "has", "migraine", scope="health")
    p = m.claims.propose("user", "avoids", "bright light", scope="health", derived_from=[a], actor="inference:v0")
    assert m.claims.current()[p]["confirmation"] == "unconfirmed"
    for fn in (lambda: m.claims.confirm(p, actor="inference:v0"),
               lambda: m.claims.assert_claim("user", "x", "y", scope="health", actor="inference:v0"),
               lambda: m.claims.delete(p, actor="inference:v0")):
        with pytest.raises(NotAuthorized):
            fn()
    assert any(e["body"]["reason"] == "non_user_claim_transition" for e in m.gov.entries(kinds=["PROHIBITED_ATTEMPT"]))
    with pytest.raises(NotAuthorized):
        m.claims.propose("user", "x", "y", scope="health", derived_from=[a], actor="agent:coder")
    m.claims.confirm(p)
    c = m.claims.current()[p]
    assert c["confirmation"] == "user_confirmed" and c["medb_mediated"] is True


def test_correction_is_transition_what_now_and_what_then(m, clock):
    cid = m.claims.assert_claim("user", "lives_in", "Brisbane", scope="home")
    t1 = clock.now_iso()
    clock.advance(days=1)
    m.claims.correct(cid, object="Toowoomba")
    assert m.claims.current()[cid]["object"] == "Toowoomba"
    assert m.claims.current()[cid]["version"] == 2
    assert m.claims.as_of(t1)[cid]["object"] == "Brisbane"
    assert [t["kind"] for t in m.claims.history(cid)] == ["ASSERT", "CORRECT"]


def test_supersede_disavow(m, clock):
    a = m.claims.assert_claim("user", "goal", "run 5k", scope="fitness")
    clock.advance(hours=1)
    b = m.claims.assert_claim("user", "goal", "run 10k", scope="fitness")
    m.claims.supersede(a, b)
    t = clock.now_iso()
    clock.advance(hours=1)
    m.claims.disavow(b, reason="no longer endorse")
    st = m.claims.current()
    assert st[a]["status"] == "superseded" and st[a]["superseded_by"] == b
    assert st[b]["status"] == "disavowed"
    assert m.claims.as_of(t)[b]["status"] == "active"
    assert st[a]["object"] == "run 5k"  # disavowal/supersession keep content


def test_deletion_destroys_content_keeps_fact(m, clock):
    cid = m.claims.assert_claim("user", "diagnosis", "secret-condition-xyz", scope="health")
    t = clock.now_iso()
    clock.advance(minutes=5)
    m.claims.correct(cid, object="secret-condition-xyz-v2")
    clock.advance(minutes=5)
    n = m.claims.delete(cid)
    assert n == 2
    st = m.claims.current()[cid]
    assert st["status"] == "deleted" and st["content_destroyed"] and st["object"] is None
    assert m.claims.as_of(t)[cid]["object"] is None  # content gone for every version
    assert [x["kind"] for x in st["transitions"]][-1] == "DELETE"
    assert m.store.verify("claims")["ok"] and m.gov.verify()["ok"]
    dump = "\n".join(m.store.db.iterdump())
    assert "secret-condition-xyz" not in dump


def test_temporal_validity(m):
    cid = m.claims.assert_claim("user", "employer", "Acme", scope="work",
                                temporal_validity={"valid_from": "2020-01-01T00:00:00Z", "valid_to": "2024-01-01T00:00:00Z"})
    st = m.claims.current()
    assert cid in m.claims.valid_at(st, "2022-06-01T00:00:00Z")
    assert cid not in m.claims.valid_at(st, "2025-06-01T00:00:00Z")


def test_infer_requires_closure_and_composition_needs_compose(m):
    a = m.claims.assert_claim("user", "sleeps", "5h", scope="health")
    b = m.claims.assert_claim("user", "works", "nights", scope="work")
    with pytest.raises(PermissionDenied):
        m.claims.propose("user", "tired", "often", scope="health", derived_from=[a], actor="inference:v0")
    m.perms.grant("infer", "user", scopes=["health"], sensitivity_max="high")
    m.perms.grant("infer", "user", scopes=["work", "health"], sensitivity_max="high")  # no compose
    m.claims.propose("user", "tired", "often", scope="health", derived_from=[a], actor="inference:v0")
    # each input individually authorized; composition is not
    with pytest.raises(PermissionDenied):
        m.claims.propose("user", "shift_fatigue", "likely", scope="health", derived_from=[a, b], actor="inference:v0")
    m.perms.grant("infer", "user", scopes=["work", "health"], sensitivity_max="high", compose=True)
    m.claims.propose("user", "shift_fatigue", "likely", scope="health", derived_from=[a, b], actor="inference:v0")


def test_closure_covers_transitive_ancestors(m):
    m.perms.grant("infer", "user", scopes=["*"], sensitivity_max="special", compose=True)
    a = m.claims.assert_claim("user", "note", "x", scope="private", sensitivity="special")
    p1 = m.claims.propose("user", "d1", "y", scope="health", derived_from=[a], actor="inference:v0")
    p2 = m.claims.propose("user", "d2", "z", scope="health", derived_from=[p1], actor="inference:v0")
    m.perms.grant("use", "user", scopes=["health"], purposes=["visit"], sensitivity_max="high")
    with pytest.raises(PermissionDenied):
        m.claims.retrieve([p2], purpose="visit", actor="agent:clinic")


def test_prohibited_inference(m, grants):
    a = m.claims.assert_claim("user", "reads", "news", scope="health")
    with pytest.raises(ConstitutionalProhibition):
        m.claims.propose("user", "susceptibility_to_framing", "high", scope="health", derived_from=[a],
                         actor="inference:v0")


def test_retrieve_logged_and_deleted_ancestor_breaks_use(m, grants):
    a = m.claims.assert_claim("user", "has", "asthma", scope="health")
    p = m.claims.propose("user", "carries", "inhaler", scope="health", derived_from=[a], actor="inference:v0")
    m.claims.retrieve([p], purpose="visit", actor="agent:clinic")
    r = m.gov.entries(kinds=["CLAIMS_RETRIEVED"])[-1]["body"]
    assert r["claim_ids"] == [p] and r["purpose"] == "visit"
    with pytest.raises(PermissionDenied):
        m.claims.retrieve([p], purpose="marketing", actor="agent:clinic")
    m.claims.delete(a)
    with pytest.raises(PermissionDenied):
        m.claims.retrieve([p], purpose="visit", actor="agent:clinic")


def test_identity_model_only_user_confirmed(m, grants):
    a = m.claims.assert_claim("user", "has", "asthma", scope="health")
    p = m.claims.propose("user", "carries", "inhaler", scope="health", derived_from=[a], actor="inference:v0")
    assert set(m.identity.view()) == {a}
    m.claims.confirm(p)
    assert set(m.identity.view()) == {a, p}
    m.claims.reject(a)
    assert set(m.identity.view()) == {p}


def test_exposure_marks_mediated(m):
    cid = m.claims.assert_claim("user", "values", "autonomy", scope="self", exposure_refs=["pkg-1"])
    assert m.claims.current()[cid]["medb_mediated"] is True

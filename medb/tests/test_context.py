import pytest

from medb.context import ModalAsymmetry, open_package
from medb.errors import ConstitutionalProhibition, PackageExpired
from medb.system import MedB, load_config


@pytest.fixture
def seeded(m):
    m.perms.grant("use", "user", scopes=["authority"], purposes=["visit"], sensitivity_max="high")
    m.perms.grant("infer", "user", scopes=["authority"], sensitivity_max="high")
    a = m.claims.assert_claim("user", "decides", "my own treatment", scope="authority")
    p = m.claims.propose("user", "decides", "clinician decides treatment", scope="authority",
                         derived_from=[a], actor="inference:v0")
    return a, p


def test_package_sections_and_expiry(m, clock, seeded):
    pkg = m.context.build("visit", "agent:clinic", predicates=["decides", "allergy"], ttl_minutes=30)
    for k in ("claims", "frames", "contradictions", "unknowns", "rationale", "boundary", "expiry"):
        assert k in pkg
    assert {"predicate": "allergy", "status": "no permitted claim"} in pkg["unknowns"]
    assert open_package(pkg, clock)
    clock.advance(minutes=31)
    with pytest.raises(PackageExpired):
        open_package(pkg, clock)


def test_ttl_capped(m, seeded):
    pkg = m.context.build("visit", "agent:clinic", ttl_minutes=10**6)
    from medb.util import parse_iso
    assert (parse_iso(pkg["expires_at"]) - parse_iso(pkg["issued_at"])).total_seconds() == 1440 * 60


def test_logged_not_retained(m, seeded):
    pkg = m.context.build("visit", "agent:clinic", predicates=["decides"])
    log = m.gov.entries(kinds=["CONTEXT_PACKAGE_ISSUED"])[-1]["body"]
    assert log["package_id"] == pkg["package_id"]
    assert {r["claim_id"] for r in log["claim_refs"]} == {c["claim_id"] for c in pkg["claims"]}
    assert log["ranking"]["inputs"] and log["ranking"]["weights"]
    dump = "\n".join(m.store.db.iterdump())
    for c in pkg["claims"]:
        assert c["rendered"] not in dump  # rendered text is never stored
    assert m.gov.entries(kinds=["CLAIMS_RETRIEVED"])[-1]["body"]["package_id"] == pkg["package_id"]


def test_modal_symmetry_and_contradiction_preserved(m, seeded):
    a, p = seeded
    pkg = m.context.build("visit", "agent:clinic", predicates=["decides"])
    by = {c["claim_id"]: c for c in pkg["claims"]}
    assert by[a]["rendered"] == "You stated: user decides my own treatment"
    assert by[p]["rendered"].startswith("MedB inference, not confirmed by you:")
    assert pkg["contradictions"] == [{"claim_ids": sorted([a, p]), "basis": "single_valued_predicate",
                                      "resolution": "none (preserved)"}]
    assert set(by) == {a, p}  # both sides present


def test_asymmetric_rendering_refused(clock):
    cfg = load_config(overrides={"rendering": {"templates": {"user_asserted": "You may feel that {statement}",
                                                             "unconfirmed": "{statement}"}}})
    m = MedB(clock=clock, seed=1, config=cfg)
    m.perms.grant("use", "user", scopes=["authority"], purposes=["visit"], sensitivity_max="high")
    m.perms.grant("infer", "user", scopes=["authority"], sensitivity_max="high")
    a = m.claims.assert_claim("user", "decides", "my own treatment", scope="authority")
    m.claims.propose("user", "decides", "clinician", scope="authority", derived_from=[a], actor="inference:v0")
    with pytest.raises(ModalAsymmetry):
        m.context.build("visit", "agent:clinic")
    f = m.gov.entries(kinds=["PROHIBITED_ATTEMPT"])[-1]["body"]["findings"]
    assert {x["finding"] for x in f} == {"SELF_ACCOUNT_HEDGED", "INFERENCE_UNATTRIBUTED"}


def test_user_own_hedge_is_not_asymmetry(m):
    m.perms.grant("use", "user", scopes=["self"], purposes=["p"], sensitivity_max="high")
    m.claims.assert_claim("user", "thinks", "I might move abroad", scope="self")
    pkg = m.context.build("p", "agent:x")
    assert pkg["claims"][0]["rendered"] == "You stated: user thinks I might move abroad"


def test_privacy_by_default_and_purpose_binding(m, seeded):
    assert m.context.build("advertising", "agent:ads")["claims"] == []
    assert m.context.build("advertising", "agent:ads")["boundary"]["excluded_counts"]


def test_cross_scope_composition_requires_compose(m):
    m.perms.grant("use", "user", scopes=["health", "work"], purposes=["p"], sensitivity_max="high")
    m.claims.assert_claim("user", "has", "asthma", scope="health")
    m.claims.assert_claim("user", "works_at", "mine", scope="work")
    pkg = m.context.build("p", "agent:x", scopes=["health", "work"])
    assert pkg["claims"] == []
    m.perms.grant("use", "user", scopes=["health", "work"], purposes=["p"], sensitivity_max="high", compose=True)
    assert len(m.context.build("p", "agent:x", scopes=["health", "work"])["claims"]) == 2
    assert len(m.context.build("p", "agent:x", scopes=["health"])["claims"]) == 1


def test_withheld_contradiction_counted_without_leaking(m):
    m.perms.grant("use", "user", scopes=["authority"], purposes=["p"], sensitivity_max="moderate")
    a = m.claims.assert_claim("user", "decides", "me", scope="authority", sensitivity="moderate")
    m.claims.assert_claim("user", "decides", "my sister", scope="authority", sensitivity="special")
    pkg = m.context.build("p", "agent:x")
    assert [c["claim_id"] for c in pkg["claims"]] == [a]
    assert pkg["boundary"]["contradictions_involving_withheld_claims"] == 1


def test_frames_section(m):
    m.perms.grant("use", "user", scopes=["self"], purposes=["p"], sensitivity_max="high")
    m.claims.assert_claim("user", "frame", "I read my health through my family history", scope="self")
    pkg = m.context.build("p", "agent:x", predicates=["decides"])
    assert len(pkg["frames"]) == 1 and pkg["claims"] == []


def test_prohibited_purpose(m):
    with pytest.raises(ConstitutionalProhibition):
        m.context.build("persuasion test", "agent:x")


def test_deleted_and_rejected_excluded(m, seeded):
    a, p = seeded
    m.claims.reject(p)
    assert [c["claim_id"] for c in m.context.build("visit", "agent:x")["claims"]] == [a]
    m.claims.delete(a)
    assert m.context.build("visit", "agent:x")["claims"] == []


def test_mediated_marker_rendered(m, seeded):
    a, p = seeded
    m.claims.confirm(p)
    pkg = m.context.build("visit", "agent:x")
    r = next(c for c in pkg["claims"] if c["claim_id"] == p)
    assert r["rendered"].endswith("[MedB-mediated]") and r["medb_mediated"]

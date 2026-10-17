# MedB v3.9 — Harness-Agnostic Governance Substrate

**Status:** Proposed specification revision. Not frozen, certified, implemented, or validated.
**Baseline:** v3.5 authoritative in-scope package.
**Research basis:** `medb-research/v2/PRIOR_ART_CROSSWALK.md` is a prior-art mapping, not a novelty finding.
**Purpose:** Re-scope MedB as a governance substrate that holds a user’s goal model and personal data and governs use by, and exposure between, independently operated agent harnesses.

## Package

- `MASTER_SPECIFICATION.md`: governing model, invariants, four loci, boundaries, non-claims.
- `IMPLEMENTATION_CONTRACT.md`: minimum records, authorization, derivation closure, cross-harness contracts, revocation and control surfaces.
- `ADVERSARIAL_TEST_SUITE.md`: required attack scenarios and result semantics.
- `DECISION_REGISTER.md`: unresolved constitutional and empirical questions; no implementation default may settle them.
- `TRACEABILITY_RESEARCH.md`: v3.5 and research-v2 mapping, evidence gaps, and scope-change assessment.

## Change summary

The primary architectural unit is no longer a single assistant or agent. It is the relationship among the governed goal/data model, admitted harnesses, cross-harness information flows, and user-facing control. Harnesses are replaceable and potentially proactive clients of the substrate; none owns or defines the substrate's authority.

## Adoption rule

This package is a proposed successor candidate, not a silent amendment to v3.5. Preserve v3.5 unchanged. Implementations must not claim v3.9 conformance from this text alone. Constitutional questions listed in the decision register remain open until resolved through a legitimate process.

## Interpretive guardrails

- Stated and inferred goals remain distinct; storing or repeating a proposition is not endorsement.
- Harness capability, model confidence, utility, persistence, or runtime change cannot increase authority.
- Authority does not transitively propagate merely because information does.
- Cross-harness exposure is an explicit governed event; constraints and provenance travel with the exposed material.
- Missing derivation ancestry never creates unrestricted ancestry.
- User visibility and revocation are requirements, but visibility is not proof that every downstream copy can be recalled.
- Prior-art mapping does not establish novelty, non-novelty, safety, or effectiveness.

# MedB Master Specification v2

**Revision 2.0 — Adversarially Revised**  
**Status: Frozen for Round 1 experimental execution**

This directory contains the v2 constitutional specification for MedB. It supersedes the v1 specification for experimental purposes while preserving v1 as historical source material.

## Documents

- `MASTER_SPECIFICATION.md` — consolidated constitutional specification.
- `CONSTITUTIONAL_SEMANTICS.md` — formal vocabulary, state semantics, permission closure, provenance, suspension, and observability requirements.
- `TEST_MATRIX.md` — adversarial conformance and mutation-test matrix.
- `ROUND1_PROTOCOL.md` — experimental execution protocol and evidence rules.
- `CHANGELOG.md` — rationale and traceability from v1 findings to v2 changes.

## Core v2 changes

1. Adds constitutional non-amplification.
2. Separates epistemic, authority, and causal provenance.
3. Defines identity, compliance, and membership as distinct.
4. Defines authorization as shaped, scoped, compositional, and non-escalating.
5. Defines suspension propagation through capability dependencies.
6. Defines deletion closure over derived artifacts.
7. Defines candidate-inference operational-use boundaries.
8. Defines independent audit requirements and trusted-base assumptions.
9. Replaces undefined “most conservative action” with explicit conservative-action dimensions.
10. Adds proxy-manipulation and proxy-dependence tests.
11. Adds cold-start replacement testing.
12. Adds longitudinal constitutional-drift testing.
13. Adds PASS-evidence and minimum-witness requirements.
14. Makes Part IV explicit and operational.

The v2 specification does **not** resolve the constitutional amendment question in III.4. It makes the current deadlock explicit rather than pretending that a legitimate amendment authority already exists.

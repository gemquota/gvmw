# MedB v3.5 — Research-to-Specification Traceability

**Purpose:** Show how recommendations from research v2 are reflected in v3.5. “Specified” means a requirement is written, not that it has passed.

| Research recommendation | v3.5 location | Verification evidence still required | Status |
|---|---|---|---|
| Formalize state model | Master Parts 0–II; Contract §§1–2 | Implemented schema, transition table, invalid-state tests | Specified; implementation unverified |
| Define authority attenuation algebra | Master Principle 7; Contract §3; A-001–A-012 | Formal partial order, property-based tests, race tests | Partially formalized; algebra proof/test pending |
| Define derivation closure | Master Principle 8; Contract §4; D-001–D-008 | Full descendant inventory, closure implementation, mutation tests | Specified; coverage unverified |
| Define deletion by scope and evidence | Master Principle 10; Contract §7; X-001–X-007 | Cache, backup, semantic descendant, metadata leakage tests | Specified; actual deletion unverified |
| Propagate suspension and restoration | Master Principle 11; Contract §6; S-001–S-007 | Dependency graph, in-flight and alternate-path tests | Specified; implementation unverified |
| Make observability part of claims | Master Principles 17–18; Contract §§9, 11; protocol | Claim-evidence ledger and audit report | Specified; trusted base remains implementation-dependent |
| Operationalize manipulation and proxies | Master Principle 14; C-004–C-007 | Objective lineage, baseline, causal design, construct validity | Partially specified; measurement open |
| Track causal feedback without discarding evidence | Master Principle 13; Contract §8; C-001–C-003 | Exposure schema, temporal studies, counterfactual evaluation | Specified; causal validity unverified |
| Test semantic portability | Master Principle 16; Contract §10; P-001–P-007 | Independent readers, cold-start tests, reconstruction scoring | Specified; test execution pending |
| Use assurance cases | Master Principle 18; Contract §11 | Claims, arguments, evidence, defeaters, reviewer independence | Specified; assurance cases not yet populated |
| Compare audit methods | Round 1 Protocol §§4–5, 9 | Matched baseline, blinded trials, false-positive/negative analysis | Protocol specified; experiment not run |
| Preserve amendment and membership questions | Master §0.7; Decision Register CD-01/CD-02/CD-08 | Legitimate decision process and documented dissent | Open by design |
| Clarify dependence and metadata retention | Master Principles 10, 15; Decision CD-03/CD-05/CD-10 | Empirical measures, leakage studies, normative review | Open/empirical |
| Strengthen research integrity | Master Principle 21; research v2 Source Register | Primary-source review, frozen search strategy, comparison evidence | Process defined; review not systematic |
| Add ontological and philosophical critique | TREATISE.md; Master Part I | Expert review, counterarguments, empirical implications | Exposition drafted; no consensus implied |

## Important limits

- v3.5 has not been tested by virtue of this traceability table.
- A test suite can be incomplete or defective; mutation sensitivity is required.
- An item marked specified may still be ambiguous, unimplementable, or in conflict with another requirement.
- Open constitutional questions are not defects to be silently patched by code.
- Prior-art mappings do not establish novelty or non-novelty.
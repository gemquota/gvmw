# MedB v3 — Traceability to the 86-Point Adversarial Review

This matrix maps the 86 numbered findings from the recovered review summary to the v3 documents. “Covered” means an explicit requirement or test is specified, not that an implementation has passed it. “Partial/open” identifies matters requiring implementation evidence or a legitimate constitutional decision.

## I. Overall assessment and core architecture (1–23)

| # | Review finding | v3 mapping | Status |
|---:|---|---|---|
| 1 | Strong constitution, operationally incomplete | Master Parts IV–VI; acceptance gate | Covered as framing; implementation unverified |
| 2 | Separate evidence, inference, representation, context, action | Master 1.2, 1.4; Contract §§1–3 | Covered |
| 3 | Historical statements differ from current endorsement/authority | Master Principles 1, 3, 11; Contract §1 | Covered |
| 4 | Authentication does not establish authority to act for a person | Master 1.3; Tests A-002 | Covered |
| 5 | Authorization must be fully scoped | Master Principle 7; Contract §1.2 | Covered |
| 6 | Permission closure/non-amplification over derivation chains | Master §0.3, Part III.1; Contract §4 | Covered; composition rule needs implementation |
| 7 | Hypotheses may be operationally influential while labeled hypotheses | Master 1.4, Part III; Contract §5; A-006/A-007 | Covered |
| 8 | Recoverability bounded by observability | Master Principle 2, Part III.7 | Covered |
| 9 | Recoverability dimensions distinguished | Master Principle 2 | Covered |
| 10 | Deletion includes semantic derivatives and careful deletion history | Master Principle 3, 8; Contract §7 | Covered; semantic verification implementation-dependent |
| 11 | Audit metadata has separate retention/privacy rules | Master Principle 8; Decision CD-05 | Partial/open |
| 12 | Manipulation assessed by functional behavioral objective | Master Principle 9; M-001–M-004 | Covered; causal measurement implementation-dependent |
| 13 | Proxy manipulation (completion, satisfaction, friction) | Master Principle 9; M-002/M-006 | Covered |
| 14 | Measure dependence and preserve exit ability | Master Principle 10; M-005/M-007; CD-03 | Partial/open on constitutional threshold |
| 15 | Replaceability requires independent reconstruction | Master Principle 10; Contract §10; A-017 | Covered; test execution unverified |
| 16 | Syntactic and semantic portability differ | Master Principle 10; Contract §10 | Covered |
| 17 | Plurality preserves temporal/dispute status | Master Principle 11; A-013/A-014 | Covered |
| 18 | Same-user statements can differ in present authority | Master Principles 1, 3, 11 | Covered |
| 19 | Track causal effects through exposure and later evidence | Master Principle 12; Contract §8 | Covered |
| 20 | Post-exposure evidence is not automatically invalid | Master Principle 12; CD-04 | Covered; downstream normative response open |
| 21 | Self-description cannot prove compliance | Master Principle 13; T-004/T-005 | Covered |
| 22 | Independent audit/provenance integrity required | Master Principle 13; Contract §9; T-001–T-008 | Covered; actual independence unverified |
| 23 | Constitutional drift must be detectable | Master Principle 14; L-001–L-004 | Covered; longitudinal execution unverified |

## II. Governance, authority, constitutional conflicts (24–41)

| # | Review finding | v3 mapping | Status |
|---:|---|---|---|
| 24 | Conflicts need procedures without invented hierarchy | Master Part III.9; CD-06 | Covered with unresolved conflicts retained |
| 25 | Conservative action requires operational dimensions | Master Part III.6; CD-06 | Covered as fallback, not constitutional hierarchy |
| 26 | Amendment deadlock must be explicit | Master §0.7; CD-01 | Open by design |
| 27 | Identity/compliance/membership separated | Master §0.6 | Covered; membership boundary open |
| 28 | Implementation inaccessibility differs from uncertainty/violation | Master §0.5; protocol §6 | Covered |
| 29 | Suspension semantics cover all operation classes | Master Part III.3; Contract §6 | Covered |
| 30 | Suspension propagates through dependencies and composition | Contract §6; S-001–S-010 | Covered; graph completeness needs testing |
| 31 | Capability containment follows dependency graph | Contract §6; S-003/S-010 | Covered |
| 32 | Sequence laundering and cumulative effects constrained | Master Principle 7; Contract §3; A-009 | Covered |
| 33 | Composite components need independent composite checks | Master §0.3, Part III.1; A-008 | Covered |
| 34 | Every action traces its authority chain | Master Principle 7; Contract §§1.2–3 | Covered |
| 35 | Epistemic, authority, causal provenance are separate | Master §0.4, 1.6; Contract §2 | Covered |
| 36 | Access, retrieval, processing, exposure, disclosure, reuse distinct | Master 1.4, Principle 6; Contract §3 | Covered |
| 37 | Information-flow metadata and controls explicit | Contract §§1, 3, 4, 7 | Covered |
| 38 | Repeated cold-start replacement testing | Master Principle 10; Contract §10; A-017/A-018 | Covered; execution unverified |
| 39 | Compliance depends on implementation/state/environment/history | Master §3.8; L-001–L-008 | Covered |
| 40 | Deterministic governance replay where feasible | Contract §1.3; Protocol §§2, 6 | Partial: event ordering is required, deterministic replay is conditional |
| 41 | Original Round 1 protocol incomplete | v3 ROUND1_PROTOCOL.md | Covered |

## III. Threat models and enforcement architecture (42–60)

| # | Review finding | v3 mapping | Status |
|---:|---|---|---|
| 42 | Broad threat model incl. bugs, gaming, malicious/compromised components, composition | Protocol §§2–5; Tests | Covered |
| 43 | Trusted base explicit; LLM cannot enforce itself | Master §3.7; Contract §9 | Covered as requirement; architecture unverified |
| 44 | Separate probabilistic reasoning from enforcement | Master Principle 5; Contract §3 | Covered |
| 45 | Classify enforceable/auditable/semantic/open requirements | Master Parts IV–VI; test outcome vocabulary | Partial: per-requirement classification still needed in implementation register |
| 46 | Observed behavior cannot prove hidden capability absent | Master §3.7; T-001/T-003 | Covered within stated audit boundary |
| 47 | Mutation tests detect direct bypasses | Test Suite §9; Protocol §5 | Covered as requirement; no mutations run yet |
| 48 | Evasive mutations test derivatives/proxies/alternate paths | Test Suite §9 | Covered as requirement; no mutations run yet |
| 49 | Minimum witness and evidence thresholds | Master Part IV; Protocol §6 | Covered |
| 50 | PASS requires affirmative evidence | Master §0.5, Part IV; Protocol §6 | Covered |
| 51 | Audit regress/trusted base explicit | Master §3.7; Contract §9 | Covered; trusted base remains implementation-specific |
| 52 | Independence levels distinguished | Contract §9; Protocol §4 | Covered |
| 53 | Constitutional underdetermination differs from evidential uncertainty | Master §0.5; Protocol §6 | Covered |
| 54 | Separate constitutional, empirical, operational assumptions | Master Parts III–VI; Decision Register | Covered in structure; per-test declarations required |
| 55 | Capability, exercise, outcome, objective, mechanism distinguished | Master §0.4; Principle 9; Tests M-001–M-007 | Covered |
| 56 | Inspect objective lineage in training/runtime/ranking/feedback | Principle 9; Contract §§3, 9; M-001–M-006 | Partial: objective instrumentation depends on implementation access |
| 57 | Confidence/capability/longevity/use do not create authority | Principle 4; A-001/A-004 | Covered |
| 58 | Past delegation does not generalize | Principle 7; A-005 | Covered |
| 59 | Historical behavior is not current authorization | Principles 1, 4; A-001 | Covered |
| 60 | Authority weight cannot manufacture current permission | Principles 1, 4; Contract §1.2 | Covered |

## IV. Human sovereignty and constitutional vocabulary (61–74)

| # | Review finding | v3 mapping | Status |
|---:|---|---|---|
| 61 | Current instructions act only within constitutional space/delegation | Principles 1, 7; Master §1.3 | Covered |
| 62 | User authority over self differs from amendment authority | Master §0.7; CD-01/CD-08 | Open where legitimacy unresolved |
| 63 | Charter constrains user override; avoid hidden paternalism | Master §1.3, Principle 14; CD-08 | Partially specified; legitimacy question open |
| 64 | Some obligations exceed immediate preference | Principles 8, 9, 13, 14 | Covered |
| 65 | Amendment implications must not be hidden | Master §0.7; CD-01 | Open by design |
| 66 | Charter ownership is unresolved | CD-01/CD-08 | Open by design |
| 67 | Membership vocabulary precise | Master §0.6; Decision CD-02 | Covered terminology; boundary open |
| 68 | Formal vocabulary for records, evidence, authority, use, etc. | Master Parts I–IV; Contract §1 | Covered |
| 69 | Derived objects carry lineage, statuses, permissions, deletion dependencies | Contract §1.1 | Covered |
| 70 | Authorization objects are structured and scoped | Contract §1.2 | Covered |
| 71 | Constitutional events are explicit | Contract §1.3 | Covered |
| 72 | Hidden state must be inspectable/reproducible or excluded from boundary | Master §3.7; Contract §9; T-001 | Covered as requirement |
| 73 | LLM not final constitutional judge | Master Principle 5; Contract §3 | Covered |
| 74 | Small independently auditable enforcement kernel | Master §3.7; Contract §9 | Covered as design constraint; actual kernel unverified |

## V. Experimental testing and principal recommendations (75–81)

| # | Review finding | v3 mapping | Status |
|---:|---|---|---|
| 75 | Round 1 covers full adversarial attack set | Protocol §5; test suite | Covered as plan; execution pending |
| 76 | Priority tests include laundering, deletion, suspension, proxy, portability, drift, self-audit | Test Suite §§3–9 | Covered |
| 77 | Observability boundary names observables, instrumentation, assumptions, unknowables | Master §3.7; Contract §9 | Covered |
| 78 | Constitutional debt tracked | Decision Register | Covered |
| 79 | Safe degradation preserves only independent unaffected capabilities | Master §3.3; Contract §11; Protocol §7 | Covered |
| 80 | Constitutional non-amplification | Master §0.3, Part III.1; Contract §4 | Covered |
| 81 | Preserve no general hierarchy, FAIL vs UNDETERMINED, open amendment, plurality, no singular model, no LLM judge | Master Parts I–III; Decision Register | Covered |

## VI. Final synthesis and implementation priorities (82–86)

| # | Review finding | v3 mapping | Status |
|---:|---|---|---|
| 82 | MedB as provenance-preserving permissioned transformation system | Master §§0.1, 1.1, Part III | Covered |
| 83 | Preserve all core conceptual distinctions | Master §§0.4–0.6; Parts I–IV | Covered |
| 84 | Ten critical weaknesses remain focal risks | Master Part III; Contract; Decision Register | Covered as explicit requirements; residual questions remain |
| 85 | Priority implementation changes | Contract, Test Suite, Protocol, Decision Register | Covered as work plan; implementation unverified |
| 86 | Convert principles into definitions, witnesses, boundaries, mutations, suspension and re-audit | Entire v3 package | Covered as specification goal; success unverified |

## Summary of traceability

- **Normative and procedural coverage:** explicitly specified for most of the 86 findings.
- **Partially specified / open:** audit-metadata retention; emergent dependence threshold; consequential feedback response; amendment authority; membership boundary; precise per-requirement classification; objective instrumentation; deterministic replay where feasible.
- **Not established by this document:** implementation correctness, test execution, mutation detection, independent audit, actual deletion closure, actual cold-start portability, or actual compliance.

This matrix must be updated when requirements change. A link to a section is not evidence that a test passes.

# MedB v3.9 — Research and Traceability

**Purpose:** Trace the harness-agnostic scope change to the v3.5 in-scope package and research v2. This is a design trace, not implementation evidence, systematic-review claim, or novelty finding.

## 1. Research context

The v3.5 research crosswalk explicitly distinguishes established mechanisms, MedB adaptations, candidate contributions, and open evidence. It warns that new labels or combinations do not establish originality. v3.9 preserves that discipline.

Relevant prior-art families already identified in research v2 include personal data stores and portability, contextual integrity, usage-control and sticky policies, object-capability security, information-flow control, provenance/lineage, event sourcing, audit and assurance methods, corrigibility/shutdown, power-seeking/autonomy research, manipulation and persuasive systems, and causal/performative feedback. v3.9 must inherit these mechanisms accurately rather than claim ownership of them.

The architectural move is to make a harness-independent governance substrate and inter-harness information flow the organizing frame. This may be a useful synthesis and scope correction; it is not by itself a novelty finding. A proper novelty assessment would require a defined search protocol, source verification, competing architecture comparison, and independent review.

## 2. v3.5-to-v3.9 traceability

| v3.5 obligation | v3.9 locus/artifact | Required new emphasis | Evidence still required |
|---|---|---|---|
| Claims, evidence, inference, endorsement remain distinct | Model; Master §§1, 3-I; Contract §1 | Stated vs inferred goals, scoped endorsement, goal versioning/correction | Schema validation, adversarial transitions, contradiction and staleness tests |
| No amplification | Master §2; Contract §2; Tests B | Standing harness authority, profile changes, multi-hop composition | Formal authority order, property tests, concurrency and mutation tests |
| Delegation attenuates | Admission; Contract §§2–3 | Admission is standing, bounded harness authority rather than per-task delegation | Capability inventory evidence, scope-difference and renewal tests |
| Restrictions follow derivatives | Derivation closure; Contract §4; Tests C | Harness memory, shared state, plans, prompts, tool args, outputs and latent ancestry limitations | Descendant inventory, multi-hop tests, missing-parent mutations |
| Exposure/disclosure are distinct governed events | Cross-harness; Contract §5; Tests D | Explicit exposure contracts, recipient identity/profile, onward transfer and enforceability class | End-to-end traces, recipient boundary tests, stripped-contract mutations |
| Suspension and restoration closure | User control; Contract §6; Tests E | Interrupt active/scheduled harness work, subagents, caches and alternate paths | Race tests, stale-token tests, dependency graph evidence |
| Deletion and retention truthfulness | Contract §7; Tests G | Multi-recipient derivatives and unverified remote copies | Cleanup evidence, restore/cache tests, recipient verification limits |
| Causal exposure tracked | Master §2.5 and §3; Contract §9 | Cross-harness and user-mediated exposure as potentially causal events | Exposure schema, temporal/counterfactual studies, attribution limits |
| Semantic portability | Contract §9; Tests G | Export reconstructs grants, exposure contracts, recipient constraints and enforcement limits | Independent cold-start reader, discrepancy reports |
| Audit scope and assurance cases | Master §§6–8; Contract §9 | Capability profiles, external sinks, recipient boundaries and observability gaps | Independent audit, trusted-base declaration, hidden-state limits |
| Open constitutional questions preserved | Decision Register | Admission legitimacy, capability measurement, exposure boundary, revocation and user control | Legitimate decision process and/or empirical study per question |
| Prior-art calibration | This document; Master §7; Decision CD-18 | No novelty claim from reframing alone | Documented comparative review and source verification |

## 3. Impact assessment of requested re-scope

### Benefits

1. **Correct architectural abstraction:** proactive harnesses become replaceable clients of governance rather than MedB being confused with one assistant or execution runtime.
2. **Standing authority becomes explicit:** admission can be bounded against identity and capability profile, reducing accidental authority inheritance when tools or autonomy expand.
3. **Cross-harness movement becomes first-class:** shared memory, summaries, plans, embeddings, and onward transfers are treated as governed flows instead of informal side effects.
4. **No-amplification becomes end-to-end:** authority and restrictions are checked across model representation, admission, derivation, and recipient boundaries.
5. **User control better matches real risk:** users can inspect who has access, what is being pursued, and where material went, while seeing what cannot be verified.
6. **Open decisions stay open:** unresolved constitutional questions are not quietly baked into a product default.

### Risks and problems

1. **Scope and implementation complexity increase materially.** A substrate that governs multiple independent runtimes needs identity, policy composition, lineage, capability-difference analysis, event capture, and recipient integration. This is not a small rename.
2. **Complete visibility is impossible to assume.** Hosted harness internals, provider-side state, hidden tools, latent model influence, and user-mediated copying may fall outside substrate control. Claims must be boundary-scoped.
3. **Revocation cannot recall every copy.** After exposure to uncontrolled recipients, the substrate may block future access and request deletion but cannot guarantee erasure.
4. **Lineage can be lossy or infeasible.** Model-generated summaries and latent representations may not have complete causal ancestry. Missing ancestry must fail closed or be quarantined, with availability costs.
5. **Capability profiles are hard to verify.** Self-declared tool inventories may be incomplete; profile changes can be subtle. Unknown capabilities must not be represented as absent.
6. **User-control overload and surveillance risks.** Logging every operation can expose sensitive content and overwhelm the user. The implementation needs minimization, risk-based detail, useful summaries, and separate content retention from event metadata.
7. **Availability and autonomy trade-offs.** Conservative deny/suspend behavior may interrupt useful work on ambiguous ancestry or policy conflicts. Operational fallbacks must remain distinct from constitutional decisions.
8. **Compatibility and migration risk.** Existing v3.5 artifacts and an executable M0 implementation appear to center a local substrate with integrations; v3.9 requires new schemas, profiles, contracts, event semantics, tests, and UI. Existing conformance claims cannot be carried forward without reassessment.
9. **False assurance risk.** An exposure contract or dashboard can create the appearance of control without enforcement. Assurance must distinguish substrate-enforced, recipient-enforced, contractual, declared, and unverifiable controls.
10. **Novelty overclaim risk.** The re-scope is not evidence that the architecture is novel or that prior art is absent.

## 4. Decision

**Recommendation: adopt as a proposed v3.9 candidate package, not as a claim of proven implementation or settled constitution.** The benefits are materially significant because the harness-agnostic boundary and cross-harness exposure are central to the stated goal; the risks are serious but can be represented as explicit limits, required tests, and open decisions rather than concealed.

This recommendation is conditional on preserving v3.5 unchanged, preserving its decision-register discipline, treating no-amplification and derivation closure as testable obligations, and refusing universal claims about visibility, enforcement, deletion, or novelty.

## 5. Required follow-on evidence before implementation conformance

- Formal definition of the authorization partial order and policy-composition algebra.
- Capability-profile measurement protocol and evidence for unknown capabilities.
- A declared enforcement boundary and recipient enforcement classes.
- Multi-harness, multi-hop tests including mixed ancestry, caches, shared memory, subagents, and onward transfer.
- Revocation races, scheduled work, recipient notification, and stale-state tests.
- User-control evaluation for correctness, comprehensibility, interruptibility, and over-notification.
- Independent export reconstruction and assurance-case review.
- Explicit reporting of every OPEN, EMPIRICAL UNKNOWN, and IMPLEMENTATION-DEPENDENT item.

No conformance, safety, efficacy, or novelty claim follows from writing these documents.

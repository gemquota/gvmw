# Revised Recommendations for MedB

**Derived from:** Prior-Work Research v2 and its mechanism crosswalk  
**Target:** MedB specification and Round 1 research program  
**Status:** Recommendations, not evidence of implementation success

## Executive judgment

MedB's strongest defensible direction is not the claim that it invented provenance, permission systems, personal memory, AI constitutions, or adversarial auditing. Those fields already contain substantial work. The research contribution, if demonstrated, lies in a carefully specified composition: a personal representation system whose claims retain epistemic status, whose authority cannot grow through transformation, whose uses remain purpose-bound, whose causal influence is recorded, whose deletion and suspension propagate, whose audit can return an honest unknown, and whose meaning can survive replacement of the original runtime.

The next revision should therefore prioritize semantic precision, formal compositional rules, evidence traceability, and experimental falsifiability over expanding the principle list.

## Priority 0 — required before claiming v3.5 is operationally complete

### R0.1 Formalize the core state model
Define records and transitions for evidence, claim, inference, representation, authorization, use event, causal exposure, deletion, suspension, restoration, and constitutional decision. State which fields are authoritative, derived, immutable, revisable, or merely advisory.

**Acceptance evidence:** machine-readable schema; transition table; invariants; examples; invalid-state tests.

### R0.2 Specify authority attenuation mathematically
Define the authorization tuple and the partial order by which a derived or delegated permission must be no more permissive than every governing ancestor. Specify composition for chained, parallel, and composite actions; missing ancestry must fail closed or suspend.

**Acceptance evidence:** worked examples; algebraic properties; property-based tests; mutation tests that remove ancestry or widen one dimension.

### R0.3 Define information-flow closure
Specify how restrictions propagate across every derived object, including summaries, embeddings, caches, indexes, rankings, tool arguments, model context, and external disclosures. Explain permitted declassification and the authority required for it.

**Acceptance evidence:** lineage graph contract; closure algorithm; hidden-descendant tests; migration tests.

### R0.4 Define deletion as a verifiable transition
Distinguish logical inaccessibility, active-store removal, derivative invalidation, backup expiry, external-recipient limits, and retained minimal audit metadata. Do not claim physical erasure where the system cannot observe it.

**Acceptance evidence:** deletion scope declaration; descendant traversal test; cache and backup test; metadata leakage assessment; externally unverifiable limits.

### R0.5 Define suspension and restoration across the dependency graph
List operations that become unavailable, the propagation rule, in-flight action handling, stale-token behavior, cache invalidation, and the evidence needed to restore capability. Preserve independent unaffected functions only where independence is demonstrated.

**Acceptance evidence:** dependency graph; race-condition tests; stale authorization tests; restoration proof requirements.

### R0.6 Make observability part of each claim
For each requirement, identify visible state, hidden state, instrumentation, trust assumptions, evidence threshold, and what cannot be inferred. A claim about hidden capability absence must not be supported by a lack of observed violation.

**Acceptance evidence:** claim-evidence ledger and independent audit plan.

## Priority 1 — required for credible experimental evaluation

### R1.1 Operationalize non-manipulation
Define prohibited functional objectives and observable proxies. Include retention, completion, satisfaction, reduced friction, user dependence, disclosure, and engagement where relevant, while distinguishing correlation from intentional or causal optimization.

**Acceptance evidence:** preregistered scenarios; counterfactual baselines; proxy gaming tests; human impact measures; explicit limits.

### R1.2 Formalize causal provenance
Represent exposure to a claim, user interaction with it, later reports, and downstream use as separate linked events. Do not discard post-exposure evidence, but do not call it independent without a justified design.

**Acceptance evidence:** temporal event schema; causal graph examples; blinded or counterfactual experiments; uncertainty reporting.

### R1.3 Test semantic portability, not just export
Require a cold-start recipient to reconstruct claim status, provenance, disputes, correction history, permissions, causal lineage, and deletion obligations without the source runtime or undocumented conventions.

**Acceptance evidence:** repeated exports to independently implemented readers; reconstruction scoring; missing-field mutations; user-readable discrepancy report.

### R1.4 Compare adversarial audit methods
Benchmark blind auditing, known-bad mutations, controlled paired examples, documentation camouflage, and independent reconstruction against simpler audit baselines.

**Acceptance evidence:** preregistered metrics, false-positive/false-negative analysis, auditor independence levels, resource budget, and reproducible artifacts.

### R1.5 Use assurance cases for critical claims
For each critical invariant, produce a structured claim-argument-evidence record with assumptions, defeaters, counterevidence, and residual risk.

**Acceptance evidence:** assurance cases for non-amplification, deletion, suspension, portability, causal feedback, and audit independence.

## Priority 2 — constitutional and ontological work that must remain explicit

### R2.1 Resolve legitimate amendment authority through a legitimate process
Do not let code defaults, a model's interpretation, or an implementation convenience decide who may amend the Charter. Publish alternatives, stakeholders, consequences, and dissent.

### R2.2 Clarify membership versus scoped noncompliance
A failed invariant, unknown status, inaccessible implementation, and loss of membership are distinct states unless a legitimate rule connects them.

### R2.3 Preserve plurality and temporal identity
A person should not be represented by a single unqualified profile. Support contradiction, uncertainty, change over time, context-bound claims, and a distinction between a historical utterance and current endorsement.

### R2.4 Define the boundary of practical dependence
Measure exit costs and induced reliance without assuming that all usefulness, continuity, or user preference is manipulation. Keep empirical indicators separate from normative judgment.

### R2.5 Establish a defensible metadata retention policy
Auditability is not a blank cheque to retain sensitive data. Define minimal fields, access controls, retention periods, deletion semantics, and reconstruction risk.

## Priority 3 — research hygiene and publication discipline

1. Maintain a source register with primary URL, publication date, source type, verification date, access method, full-text status, exact claims supported, and limitations.
2. Distinguish source claims from MedB interpretation in every entry.
3. Replace categorical novelty statements with calibrated labels: established prior art, adaptation, candidate contribution, novelty not established.
4. Add counterarguments and adjacent work, not only sources that make MedB appear distinctive.
5. Freeze search scope, queries, date range, inclusion/exclusion rules, and citation snowballing method before calling the review systematic.
6. Do not claim independent audit, successful deletion, safe degradation, or conformance without recorded evidence.
7. Version the research and specification separately so a new citation does not silently change a normative requirement.

## Proposed acceptance gate for a research-informed specification

A v3.5 package is ready for implementation experiments only when:
- every normative term used in a test has an operational definition or is marked constitutionally open;
- each critical invariant has at least one direct test, evasive test, composition test, and mutation test where applicable;
- every PASS criterion requires affirmative evidence;
- UNDETERMINED, audit-unavailable, implementation-inaccessible, and constitutional-undertermination remain distinct;
- the trusted base and observability boundary are explicit;
- no source or specification claim is misrepresented as an experimental result;
- the research crosswalk identifies inherited mechanisms and candidate contributions without claiming novelty prematurely.

## Final recommendation

Treat MedB as a research program with a promising governance architecture, not yet as a validated system or established novel method. The next decisive step is a small, formal, executable model of authority attenuation, provenance closure, deletion, and suspension, followed by mutation-tested adversarial experiments. More prose is useful only when it narrows an ambiguity, exposes a trade-off, or creates a testable obligation.
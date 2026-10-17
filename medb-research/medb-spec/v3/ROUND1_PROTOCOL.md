# MedB v3 — Round 1 Adversarial Protocol

## 1. Objective

Test whether an implementation and test harness can detect, classify, contain, and recover from specified constitutional violations within a declared audit boundary. Round 1 does not prove universal safety or resolve constitutional questions.

## 2. Preregistration

Before execution, freeze and identify:
- specification revision and interpretation/test-oracle version;
- implementation commit and build;
- model, runtime, ranking, schema, configuration, and instrumentation identifiers;
- fixtures and synthetic data;
- threat model;
- test list, mutations, expected outcomes, and minimum witnesses;
- trusted base and auditor independence level;
- known blind spots and stopping rules.

Changes after preregistration require a new run/version or a documented deviation. Do not silently alter the oracle after seeing results.

## 3. Run record

Each run includes:
`run_id`, `implementation_id`, `implementation_version`, `spec_revision`, `oracle_version`, `configuration_hash`, `model_identifier`, `runtime_identifier`, `schema_version`, `instrumentation_version`, `fixture_id`, `authorization_fixture`, `capability_state`, `auditor_identity`, `independence_level`, `start/end_time`, `result`, `evidence_refs`, and `limitations`.

## 4. Audit independence

Label each result:
- SELF;
- INDEPENDENT_PROCESS;
- INDEPENDENT_IMPLEMENTATION;
- HUMAN_EXTERNAL.

Independence is a property of the actual audit path, not the author's description. Record shared dependencies between implementation, oracle, instrumentation, and auditor. A separate process that shares the same faulty oracle is not automatically independent.

## 5. Execution order

### Phase A — Baseline
Run all applicable tests against the unmutated implementation and validate the harness with known-positive and known-negative controls.

### Phase B — Direct mutations
Introduce clear violations in one enforcement point at a time.

### Phase C — Evasive mutations
Keep the obvious enforcement point intact and violate the same invariant through alternate components, caches, ranking, derivatives, hidden state, or proxies.

### Phase D — Composition and sequence
Combine individually permitted components and execute bounded sequences to test non-amplification and cumulative limits.

### Phase E — Suspension, revocation, and deletion
Trigger each state transition and probe every declared direct/indirect dependency path, including cached and reconstructed behavior.

### Phase F — Cold-start replacement
Export a fixture, remove access to original runtime/database/proprietary decoder/services, and have an independent implementation reconstruct the documented semantics.

### Phase G — Drift and history
Change model/runtime/ranking/schema/configuration, then repeat impacted tests. Compare T0 baseline, T1 controlled change, and T2 accumulated-operation state where feasible.

### Phase H — Oracle challenge
Attempt to cause the test oracle to resolve amendment authority, membership, emergent dependence, or consequential feedback questions without an authorized normative decision. Expected outcome is explicit underdetermination, not an invented answer.

## 6. Evidence thresholds

**PASS:** sufficient independent evidence establishes the invariant within the declared boundary; instrumentation is complete for the claim; authorization and capability state are verified; all prescribed checks pass.

**FAIL:** a minimum witness establishes the point and mechanism of violation.

**UNDETERMINED:** the rule exists, but a specific evidence gap prevents a decision.

**AUDIT-UNDETERMINED:** integrity or independence of the evidence/audit procedure is unresolved.

**IMPLEMENTATION-INACCESSIBLE:** relevant state or mechanism cannot be inspected or reproduced.

**CONSTITUTIONALLY-UNDERDETERMINED:** no existing normative rule decides the case.

**NOT-TESTED:** test was not executed. It cannot be included in a pass denominator as a pass.

## 7. Suspension and safe degradation

For FAIL, or for an audit/inaccessibility condition that prevents the affected capability from establishing its required invariant:
1. emit a constitutional event;
2. suspend the affected capability;
3. compute transitive dependencies and effective reconstruction paths;
4. block direct, delegated, compositional, cached, alternate-runtime, and background paths;
5. preserve necessary evidence subject to privacy constraints;
6. record the exact restoration evidence required;
7. continue unrelated capabilities only when their independence is demonstrated.

A user instruction or risk acceptance cannot override active constitutional suspension. Constitutional underdetermination triggers suspension where safe authorization cannot be established; the report must distinguish that from an observed violation.

## 8. Restoration

Restoration requires a new audit run, evidence addressing the trigger, a mutation regression test, dependency-path verification, and updated implementation/configuration/model/runtime identifiers as relevant. A changed version number alone is not restoration evidence.

## 9. Experimental contamination

Record when a user or component is exposed to a MedB representation. Later statements can be reflective confirmation or meaningful new evidence, but must not be labeled independent solely because they occur later or use different wording.

## 10. Stop conditions

Stop the affected capability when:
- a required invariant is affirmatively violated;
- compliance cannot be established due to material audit inaccessibility;
- a constitutional question is required to decide safe operation but remains unresolved;
- the harness/oracle is shown invalid;
- a mutation expected to be detected escapes detection.

Stop does not automatically disable unrelated capabilities whose independence is demonstrated.

## 11. Required deliverables

1. per-requirement conformance matrix;
2. direct/evasive/composition coverage report;
3. mutation detection and test-suite-defect report;
4. suspension propagation and restoration report;
5. deletion closure and metadata leakage report;
6. cold-start replacement report;
7. longitudinal drift report;
8. audit independence/trusted-base report;
9. constitutional decision/debt register;
10. capability status map with limitations.

## 12. Interpretation

Results establish only the claims tested under the declared boundary. Publication of this protocol or a completed test run is not proof of universal compliance, safety, or MedB membership.

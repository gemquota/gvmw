# MedB v3.5 — Round 1 Experimental Protocol

**Status:** Protocol proposal. It records no completed experiment or result.

## 1. Research objective

Evaluate whether a specific implementation, within a declared evidence envelope, enforces MedB's critical governance invariants under ordinary, evasive, compositional, and longitudinal conditions. The experiment also evaluates the test protocol's ability to detect controlled violations.

Do not use Round 1 to claim universal safety, comprehensive compliance, or novelty. It is an initial falsifiable evaluation.

## 2. Preregistered scope

Before testing, freeze:
- implementation commit and build identifier;
- model/runtime, tools, policies, schemas, configuration, dependencies, and relevant environment;
- trusted-base inventory and threat model;
- requirement-to-test mapping;
- scenarios, controls, expected results, scoring, exclusion rules, and stopping criteria;
- observables, inaccessible state, instrumentation, and known blind spots;
- auditor roles and independence level;
- mutation catalogue and sealed ground truth;
- data handling, privacy controls, and retention rules.

Any post-freeze change must be versioned and classified as a protocol deviation, exploratory extension, or new experiment.

## 3. Threat model

Assume relevant failures may arise from ordinary bugs, stale state, incomplete ancestry, schema migration, cache and backup behavior, composite tools, race conditions, policy drift, proxy optimization, malicious or compromised components, documentation camouflage, evaluation-aware behavior, and collusion between components sharing a trust root.

Do not assume every component is malicious. Record which attacks are in scope and which are not. The absence of a tested attack is not evidence of resistance to it.

## 4. Experimental arms

Where feasible, use:
1. **Baseline arm:** a simpler implementation or policy without the MedB mechanism under study.
2. **Candidate arm:** the v3.5 implementation with the mechanism enabled.
3. **Known-good controls:** cases that should pass.
4. **Known-bad mutations:** controlled violations designed to test detection.
5. **Adversarial concealment arm:** documentation or surface behavior appears compliant while the underlying controlled violation remains.
6. **Cold-start portability arm:** independent reader receives only the export and public schema.
7. **Longitudinal arm:** repeat after material runtime/configuration changes and across event sequences.

Not every mechanism requires every arm, but exclusions must be justified in advance.

## 5. Blinding and independence

Separate, where practical:
- scenario authors;
- implementation operators;
- auditors;
- ground-truth custodians;
- scorers.

Auditors should not know which cases contain mutations when the purpose is to measure blind detection. The ground-truth custodian must preserve the sealed mapping. Report shared dependencies, credentials, models, operators, and storage between these roles. “Independent” must name the dimension of independence rather than act as a badge.

## 6. Evidence capture

For each run, preserve:
- unique run ID and timestamp with clock uncertainty;
- build/configuration identity;
- scenario and test IDs;
- inputs and permitted test fixtures;
- event/provenance trace;
- authorization decisions and relevant state transitions;
- outputs and external effects;
- instrumentation failures and missing evidence;
- auditor observations and confidence rationale;
- expected and actual outcome;
- deviations and cleanup/deletion status.

Protect sensitive data. Evidence capture must not itself violate the permissions or retention constraints being tested.

## 7. Result assignment

Use the v3.5 result vocabulary. PASS requires affirmative evidence for the criterion. FAIL requires an established violation or a test/protocol condition explicitly defined as failure. UNDETERMINED means evidence is insufficient. AUDIT-UNDETERMINED means the audit method or witness cannot decide. IMPLEMENTATION-INACCESSIBLE marks unavailable state. CONSTITUTIONALLY-UNDERDETERMINED marks a missing legitimate normative decision. NOT-TESTED and NOT-APPLICABLE must not be aggregated into PASS.

Where the outcome affects authorization, apply the declared safe-state rule while keeping the result label honest.

## 8. Minimum Round 1 suite

At minimum include:
- direct and delegated authorization checks;
- chained and composite attenuation;
- cumulative budget and race-condition tests;
- derivation closure across summaries, embeddings, caches, prompts, and tool arguments;
- deletion closure and retained-metadata leakage tests;
- suspension across queues, caches, and alternate paths;
- restoration after material change;
- causal feedback and proxy substitution;
- semantic portability with an independent reader;
- auditor independence and documentation camouflage;
- mutation sensitivity for every critical invariant;
- replay and longitudinal drift.

## 9. Analysis plan

Report raw counts, per-scenario outcomes, false positives, false negatives, uncertainty, exclusions, and failures of the test suite itself. Avoid a single aggregate score unless its weighting is justified and per-invariant results remain visible. Separate exploratory findings from preregistered outcomes.

For comparisons, use matched scenarios and explain differences in instrumentation, compute, model versions, and auditor information. Do not attribute improvements to MedB if arms differ materially in uncontrolled ways.

## 10. Stop conditions and safe state

Stop a run when continuing would cause unauthorized external effect, irreversible disclosure, loss of evidence integrity, or unbounded propagation. Preserve evidence without unnecessarily retaining protected content. Suspend the affected capability if required evidence becomes unavailable or a critical invariant is shown to fail. Restart only under a documented procedure.

## 11. Reporting template

The final report must include:
1. summary and bounded claim;
2. scope, build, and threat model;
3. trusted base and observability boundary;
4. preregistration and deviations;
5. tests and mutation catalogue;
6. per-test results and evidence references;
7. false positives/negatives and test-suite defects;
8. deletion and cleanup report;
9. residual risks and inaccessible state;
10. comparison to baseline;
11. limitations and claims not supported;
12. follow-up decisions and version impact.

## 12. Publication rule

A test plan is not an experiment. A successful run is not universal validation. A candidate contribution is not a novelty finding. A publication must state what was actually built, what was observed, what remains inaccessible, and what conclusions are not licensed by the evidence.
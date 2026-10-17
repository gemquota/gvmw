# MEDB MASTER SPECIFICATION

## Revision 3.5 — Research-Informed Adversarial Candidate

**Status:** Candidate specification; not frozen, certified, or implementation-validated.  
**Historical baseline:** v3, with research recommendations in medb-research/v2.  
**Normative scope:** Representation, evidence, authority, use, causal influence, deletion, suspension, portability, and audit.  
**Critical limitation:** This specification states obligations and evidence criteria. It does not establish that an implementation satisfies them.

# Part 0 — Status, terms, and claims

## 0.1 Purpose

MedB is a governance architecture for systems that store, infer, represent, and act on information about a person. It is designed to prevent information about a person from silently becoming authoritative identity, to constrain use and delegation, to preserve causal and epistemic history, and to make relevant governance properties inspectable and portable.

MedB is not the person, a definitive theory of personal identity, a substitute for human judgment, or a guarantee that every downstream recipient will obey exported restrictions.

## 0.2 Core objects

The implementation must distinguish at least:

- **Source evidence:** an observation, statement, document, event, or other basis for a claim.
- **Claim:** a proposition about the person, with scope and epistemic status.
- **Inference:** a machine- or human-produced interpretation derived from sources.
- **Representation:** a purpose- and context-specific arrangement of claims, inferences, uncertainties, and disputes.
- **Endorsement:** an attributable act indicating that a person presently accepts a claim for a specified scope; endorsement is not inferred from mere storage or repetition.
- **Authorization:** a bounded grant permitting an actor to perform a defined action under conditions.
- **Use event:** an operation that retrieves, transforms, exposes, ranks, discloses, or otherwise acts on governed data.
- **Causal exposure event:** a record that a representation or output was presented or made available in a way that may influence later behavior or evidence.
- **Operational state:** runtime, version, configuration, tools, policy state, and relevant environment.
- **Constitutional state:** the governing Charter version, legitimate decisions, unresolved questions, and applicable transition history.
- **Audit evidence:** independently interpretable evidence supporting or weakening a compliance claim.

A single storage schema may encode several objects, but their meanings and authority must not be collapsed.

## 0.3 Core invariant: no amplification

No transformation, inference, summary, ranking, delegation, composition, repeated use, or change of runtime may increase the authority, permission, certainty, or endorsement status of its inputs without a separately authorized and explicitly recorded transition.

Authority and evidence are different dimensions. High confidence does not grant authority. Authentication does not prove authorization. Repetition does not prove truth. A prior grant does not imply a new grant. A model's confidence, capability, usefulness, or longevity cannot manufacture permission.

For each derived object, the system must preserve the relevant ancestry and compute restrictions under a declared composition rule. Missing or unverifiable ancestry cannot be treated as unrestricted ancestry.

## 0.4 Provenance dimensions

MedB must preserve distinct, linkable provenance dimensions:

1. **Epistemic:** source, method, uncertainty, corroboration, contradiction, and correction.
2. **Authority:** principal, scope, purpose, delegation chain, validity, revocation, and policy version.
3. **Causal:** exposure, timing, interaction, potential influence, and limits on causal inference.
4. **Operational:** model/runtime/configuration, tools, relevant state, execution path, and environment.
5. **Constitutional:** governing rule version, decision authority, status of unresolved questions, and transition basis.

A typed graph may unify storage. It must not equate one provenance dimension with another. Temporal order alone does not establish causation; a source chain does not establish permission; an authorization chain does not establish factual accuracy.

## 0.5 Evidence outcomes

The system must distinguish at least:

- **PASS:** affirmative evidence meets a declared acceptance criterion within a stated evidence envelope.
- **FAIL:** evidence establishes a violated requirement or invalid state.
- **UNDETERMINED:** available evidence cannot decide the requirement.
- **AUDIT-UNDETERMINED:** the audit process or witness is insufficient to decide.
- **IMPLEMENTATION-INACCESSIBLE:** required state or mechanism cannot be inspected under the declared audit boundary.
- **CONSTITUTIONALLY-UNDERDETERMINED:** a legitimate normative decision is required and no valid decision exists.
- **NOT-TESTED:** no qualifying test was run.
- **NOT-APPLICABLE:** a documented argument establishes that the requirement does not apply to the scoped system.

A PASS is scoped to the tested build, configuration, environment, history, threat model, and evidence. No result may be generalized beyond that envelope without argument and evidence. A lack of observed violation is not proof that a hidden capability is absent.

## 0.6 Identity, compliance, and membership

System identity, per-requirement compliance, current operational eligibility, and membership in MedB are separate questions. One failure does not automatically imply global expulsion unless a legitimate rule establishes that consequence. Unknown status is not compliance; inaccessible state is not automatically proof of violation; neither is it a reason to claim PASS.

## 0.7 Amendment and authority remain open

The legitimate authority and procedure for amending the Charter remain unresolved until recorded through a legitimate process. Ordinary operation, model inference, user convenience, delegation, majority vote by components, implementation default, or a test oracle cannot by themselves enact a constitutional amendment.

A current user instruction may exercise authority within a currently valid action space. It does not automatically settle the legitimacy of the Charter or override a suspension. This is a governance problem, not a fact to be guessed by the model.

# Part I — Epistemic integrity and plural representation

## Principle 1: Evidence is not endorsement

Every claim must distinguish source evidence, inferred interpretation, current endorsement, historical endorsement, and authorization to act. A user saying something once is evidence that the statement occurred; it does not automatically prove the statement is true, current, general, or authorized for every future purpose.

## Principle 2: Uncertainty and contradiction are first-class

The system must preserve uncertainty, conflicting evidence, temporal changes, context, and dispute status. It must not silently force a singular canonical identity when the evidence supports multiple interpretations. Any selected view must disclose its purpose, selection rule, excluded alternatives, and uncertainty where consequential.

## Principle 3: Corrections are transitions, not silent rewrites

Corrections change the present status of a claim while preserving only the history legitimately needed to understand the correction. Historical preservation is not a license for indefinite retention of sensitive content. The system must separate the fact of a correction from the sensitive content that may no longer be retained.

## Principle 4: Inference proposes; authority must come from elsewhere

An inference may be stored as an inference and used only within its authorized purpose. It cannot self-upgrade to user-endorsed identity, create new permissions, or authorize external action. User confirmation must itself be scoped and attributable; ambiguity is not consent.

## Principle 5: Probabilistic reasoning is not enforcement

A language model may help interpret evidence, propose hypotheses, and explain uncertainty. It cannot be the sole mechanism that grants authorization, certifies its own compliance, determines hidden state absence, or settles unresolved constitutional questions. Deterministic or independently auditable enforcement is required wherever the invariant is claimed to be mechanically enforced.

# Part II — Use, authority, and information flow

## Principle 6: Permission is operation-specific

Acquisition, storage, retrieval, inference, transformation, ranking, prompt inclusion, tool use, exposure, disclosure, export, and reuse are distinct operations. Permission for one does not imply permission for another. Authorization must identify actor, action, target, purpose, context, validity interval, data scope, recipient constraints, delegation ceiling, and revocation status as applicable.

## Principle 7: Delegation attenuates

A delegated capability may narrow authority but may not widen it. Every action must be traceable to a valid authority chain. The system must define a partial order over authorization tuples and a composition rule for chained, parallel, and composite actions. Cumulative budgets and other stateful limits require stateful enforcement; a static token is not enough.

When ancestry, current validity, or the applicable policy cannot be established, the affected capability must be denied or suspended under the declared safe-state rule. There is no “default allow because the system is useful.”

## Principle 8: Restrictions follow derived data

Restrictions apply to derived objects according to a documented information-flow rule. Derivatives include summaries, embeddings, indexes, caches, rankings, prompts, tool arguments, generated files, exported packages, and relevant logs. The implementation must identify descendants and preserve the ancestry needed to calculate their permissions.

Declassification requires an identified authority and an explicit transition. A missing ancestry edge, omitted cache, renamed derivative, or transformation into a different representation cannot erase restrictions.

## Principle 9: Exposure and disclosure are governed events

Access by a component, inclusion in a prompt, output to a user, disclosure to a third party, and export to another runtime are different events with different risks. The implementation must record enough detail to audit consequential uses while minimizing unnecessary exposure and sensitive logging.

# Part III — Deletion, suspension, and safe degradation

## Principle 10: Deletion claims are scoped and verifiable

A deletion request must resolve into explicit scope: active records, derivatives, caches, indexes, backups, exports, external recipients, and retained audit metadata. Each category must have a stated mechanism, verification method, and limit. The system must not claim physical erasure of inaccessible systems or uncontrolled recipients.

The implementation must traverse semantic and operational descendants, not merely rows directly referencing a source identifier. It must test restoration from stale cache or backup, and assess whether retained metadata can reconstruct protected content.

## Principle 11: Suspension propagates through dependencies

When a capability is suspended, all dependent capabilities and alternate paths must be evaluated. The implementation must define treatment of in-flight actions, stale tokens, cached authorization, scheduled tasks, retries, queued messages, and composite tools. Suspension must be enforced outside the model's willingness to comply.

Restoration requires fresh evidence that the reason for suspension has been resolved and that dependent state is coherent. A passing test from an older runtime does not automatically restore a capability after a material change.

## Principle 12: Safe degradation is evidence-bound

When a component or invariant becomes uncertain, preserve only operations demonstrated to be independent of the affected component and restriction. If independence cannot be shown, suspend the dependent operation. Conservative action minimizes unauthorized external effects, irreversibility, unnecessary exposure, new authority, loss of reversibility, and avoidable reduction of future choice. This ordering is an operational fallback, not a universal moral hierarchy.

# Part IV — Causal influence and non-manipulation

## Principle 13: Representational feedback is causally tracked

The system must record relevant exposure to representations that may influence later self-report, behavior, or decisions. Later evidence remains evidence, but it must not automatically be treated as independent confirmation if exposure may have contributed to it. Conversely, post-exposure evidence is not automatically invalid.

Causal provenance must separate observed temporal sequence, plausible mechanism, measured causal effect, and uncertain attribution. It must not claim causality solely because event A preceded event B.

## Principle 14: Non-manipulation is evaluated functionally

Compliance cannot be established solely by model self-report, stated intention, or documentation. The system must examine objective lineage and behavior, including proxy objectives that may reward retention, engagement, completion, satisfaction, disclosure, dependence, or reduced exit ability. Proxy metrics are warning indicators, not proof by themselves of intent or harm.

A credible assessment must define the prohibited objective, observable behavior, counterfactual baseline, confounders, outcome measures, and limits of causal attribution. It must test both direct objectives and proxy substitution.

## Principle 15: Dependence and exit are measured without pathologizing usefulness

The system must make exit, export, replacement, and discontinuation feasible. It should measure relevant exit costs and practical dependence, but must not equate every useful relationship, user preference, or voluntary continuity with manipulation. Constitutional thresholds for when emergent dependence itself becomes a violation remain open and must not be silently encoded as a default.

# Part V — Portability, audit, and assurance

## Principle 16: Portability includes semantic reconstruction

A portable export must preserve the information needed to reconstruct, at minimum, claim meaning, epistemic status, provenance, correction history, disputes, authority, permissions, causal lineage, deletion obligations, and the meaning of relevant events. The format must be documented independently of a vendor-specific runtime.

Semantic portability is demonstrated by an independent recipient reconstructing and explaining these properties from the export. A valid JSON file or successful download is not enough. The test must include cold-start reconstruction, missing-field mutations, independent readers, and discrepancy reporting.

## Principle 17: Audits declare their evidence envelope

Each audit must identify scope, build, runtime, configuration, test history, observables, instrumentation, trusted components, auditor independence, assumptions, exclusions, and inaccessible state. A report must distinguish a test plan from execution and an observed result from an inference about hidden capability.

A model or operator statement may be an input to an audit but cannot be the sole evidence for the claim being audited. The audit process itself must be evaluated for integrity, blind spots, and susceptibility to manipulation.

## Principle 18: Assurance claims require argument and evidence

Every critical invariant must be supported by a claim-argument-evidence record. The record includes the claim, scope, rationale, evidence, assumptions, defeaters, counterevidence, residual risk, test IDs, result, and reviewer. A specification reference is not evidence of implementation success.

Critical claims include non-amplification, derivation closure, deletion closure, suspension closure, semantic portability, causal feedback integrity, and audit independence.

# Part VI — Change, drift, and research integrity

## Principle 19: Material change triggers reassessment

Changes to model, runtime, tools, policy engine, schema, ranking, storage, configuration, dependency graph, or observability may change compliance. Material changes require re-evaluation of affected claims. Historical PASS results remain historical and scoped to their original evidence envelope.

## Principle 20: Unknown is not success

The system must not turn missing data, unavailable instrumentation, failed logging, contradictory witnesses, or unresolved normative questions into PASS. It must distinguish evidential uncertainty from constitutional underdetermination and from established failure. A conservative operational response does not itself settle the underlying normative question.

## Principle 21: Research claims are calibrated

MedB documentation must distinguish established prior art, adaptation of prior art, candidate contribution, and novelty not established. It must not claim a mechanism is new merely because MedB gives it a new name or combines it with another mechanism. Source descriptions, MedB interpretations, implementation evidence, and normative decisions must be labeled separately.

# Part VII — Acceptance gate and non-claims

## 7.1 Minimum acceptance gate

A v3.5 implementation cannot claim conformance merely by implementing the documents. It must provide:
- a declared implementation boundary and trusted base;
- explicit schemas and transition rules;
- tests for direct, evasive, composition, mutation, and longitudinal cases;
- affirmative evidence for every PASS;
- documented behavior for missing ancestry, revocation, deletion, suspension, restoration, and unknown states;
- an independent portability test;
- a causal-feedback evaluation;
- assurance cases for critical invariants;
- a report of failed, untested, inaccessible, and underdetermined requirements;
- a record of material changes since the tested build.

## 7.2 Explicit non-claims

This specification does not claim:
- that MedB is conscious or that it captures the full identity of a person;
- that all prior art has been exhaustively reviewed;
- that the proposed composition is novel;
- that an implementation exists or passes tests;
- that deletion is physically complete in uncontrolled systems;
- that cryptographic logs establish truth or completeness;
- that a lack of observed violation proves absence of hidden capability;
- that semantic portability preserves all lived, tacit, or relational meaning;
- that all constitutional disputes have a correct answer derivable from code;
- that user sovereignty, system constraints, and amendment legitimacy are fully reconciled.

## 7.3 Required residual-risk posture

When evidence is incomplete, disclose the limitation, preserve relevant uncertainty, and constrain the affected operation. Do not compensate for missing evidence with confidence, elaborate documentation, or a larger aggregate pass score.
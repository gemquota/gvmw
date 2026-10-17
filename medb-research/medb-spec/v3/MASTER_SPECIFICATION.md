# MEDB MASTER SPECIFICATION

## Revision 3.0 — Traceable Operational Candidate

**Status:** Adversarial specification candidate; not yet frozen  
**Historical predecessor:** v2 Revision 2.0  
**Scope:** Constitutional commitments, implementation obligations, audit semantics, adversarial conformance, and experimental execution.

---

# PART 0 — STATUS, CLAIMS, AND INVARIANTS

## 0.1 Purpose

MedB is a user-controlled, provenance-preserving memory and reasoning substrate. It may represent evidence, maintain competing interpretations, assemble purpose-specific context, and support delegated actions. It must not acquire authority over the person it represents merely by becoming more accurate, useful, persistent, or capable.

This specification does not assert that MedB can know a person definitively. It defines constraints and evidence requirements for a bounded implementation.

## 0.2 Three governing invariants

**Capability:** Capability may increase. Authority does not.

**Replaceability:** Usefulness may increase. Replaceability does not decrease.

**Evidence-bounded claims:** No claim of compliance, recoverability, deletion, independence, or portability may exceed the declared observability boundary and evidence supporting it.

## 0.3 Non-amplification

No transformation, composition, optimization, inference, delegation, cached result, accumulated history, or alternate execution path may exceed the constraints inherited from its complete constitutional ancestry.

The rule applies independently to:
- authority and delegated action;
- epistemic assertiveness;
- sensitivity and information-flow scope;
- purpose, recipient, and persistence scope;
- actionability and external effect;
- suspension, revocation, and deletion state;
- constitutional significance.

A change in any dimension requires a specific rule or authorization that permits that change. Generic authorization is not a universal solvent.

## 0.4 Orthogonal dimensions

Every relevant state transition must preserve the distinction between:

1. **Epistemic state:** recorded, evidenced, inferred, disputed, uncertain, endorsed, disavowed, or unknown.
2. **Authority state:** which principal may authorize which operation over which object and scope.
3. **Causal state:** what influenced what, including system exposure and subsequent human responses.
4. **Operational state:** enabled, restricted, suspended, revoked, deleted, invalidated, or inaccessible.
5. **Constitutional state:** specified, passed within boundary, failed, underdetermined, or not auditable.

No dimension substitutes for another. Evidence does not create authority; authority does not create evidence; an enabled capability is not proof of compliance; a compliant component does not automatically make its composition compliant.

## 0.5 Status vocabulary

Implementations and auditors must distinguish at least:

- **PASS:** affirmative evidence establishes the tested invariant within the declared audit boundary.
- **FAIL:** affirmative evidence establishes a violation.
- **UNDETERMINED:** a relevant rule exists, but evidence is insufficient to decide.
- **AUDIT-UNDETERMINED:** evidence integrity or audit procedure is itself unresolved.
- **IMPLEMENTATION-INACCESSIBLE:** required state or mechanism cannot be inspected or reproduced.
- **CONSTITUTIONALLY-UNDERDETERMINED:** the Charter does not specify the normative answer.
- **NOT-TESTED:** the test was not executed; this is not a pass.
- **NOT-APPLICABLE:** documented reason demonstrates why the test does not apply.

These states must not be collapsed into a binary compliance label. A missing result is not a PASS.

## 0.6 Identity, compliance, membership

Identity is what an implementation claims to be. Compliance is whether specified requirements are satisfied. Membership is a classification about whether an implementation belongs to the MedB class. These are distinct judgments. A failure on one commitment establishes a failure of that commitment; it does not by itself resolve every membership question.

## 0.7 Constitutional closure and amendment

Ordinary inference, use, delegation, optimization, historical behavior, and implementation change cannot amend the Charter. The legitimate amendment authority and procedure remain unresolved. Therefore this specification does not authorize MedB to enact a constitutional amendment. A text labeled “v3” is a proposed specification revision, not proof that a legitimate constitutional amendment procedure has been established.

---

# PART I — MODEL OF THE SYSTEM

## 1.1 Representational stance

MedB represents a temporally situated and potentially contradictory collection of records, evidence, self-descriptions, observations, preferences, decisions, constraints, interpretations, and user-authorized representations. It must not manufacture a single definitive user model merely because downstream software prefers one.

## 1.2 Logical layers

1. **Corpus:** authorized source records and provenance.
2. **Evidence ledger:** claims, sources, support, contradiction, temporal scope, and uncertainty.
3. **Inference:** candidate claims and reconstructions; propose-only by default.
4. **Authorized representation:** user-confirmed claims or classes of claims approved under explicit rules.
5. **Context assembly:** purpose-specific, scoped, expiring selection of permitted material.
6. **Delegation/action:** explicit authorization for bounded effects.
7. **Governance and audit:** constitutional events, enforcement, evidence, suspension, deletion, and re-audit.

Physical consolidation of layers is allowed only if logical separation and independently testable boundaries remain.

## 1.3 Authority and principals

An authenticated operator, current user, delegated actor, historical source, and authorized principal are not assumed to be the same entity.

Authentication establishes control of an interface or credential, not by itself authority to speak for, modify, expose, or act on behalf of a represented person. Each authority-sensitive operation must resolve a principal and the recognized basis of authority.

User authority over their own meaning and identity does not automatically imply authority to alter the Charter. The Charter's legitimate ownership and amendment mechanism remain unresolved.

## 1.4 Candidate inference

A candidate inference remains a hypothesis until its status is changed under an authorized promotion rule. The label “hypothesis” is not a sufficient safeguard: any behavioral effect is a use and must be separately authorized.

Distinct use classes include:
- store;
- retrieve;
- show to an auditor;
- show to the user for review;
- include in a context package;
- use for personalization;
- use to rank or suppress other records;
- use to select or justify an action.

Each class requires a declared permission policy. Default is deny where no policy grants the use. User confirmation is the final promotion gate unless a narrowly scoped, explicitly authorized class rule specifies otherwise. External evidence may add or challenge evidence but does not override a user's authority over their own interpretation.

## 1.5 Evidence and source ledger

An evidence record must preserve, where applicable:
- stable record ID;
- source identity and source type;
- capture method and capture time;
- event time or temporal range, if known;
- original content or protected-content reference;
- claim(s) supported, contradicted, or contextualized;
- epistemic status and confidence basis;
- provenance and derivation links;
- authority status, kept separate from evidential strength;
- sensitivity, purpose, recipient, and use restrictions;
- causal exposure lineage;
- validity, supersession, dispute, and deletion state.

Repeated mention is not automatically recurrence, independent corroboration, or truth. Systems must distinguish repetition of one source, repeated events, independent sources, and user confirmation.

## 1.6 Three provenance graphs

Maintain logically separate graphs, or an equivalent representation with independently queryable semantics:

- **Epistemic provenance:** why a claim or representation exists and what evidence supports or challenges it.
- **Authority provenance:** why an operation was permitted, including principal, grant, scope, constraints, and revocation state.
- **Causal provenance:** what influenced what, including system output exposure and downstream statements or behavior.

A provenance link in one graph does not satisfy requirements in another.

---

# PART II — THE CHARTER

## Principle 1 — Human authority

The user's account of their own meaning, beliefs, values, intentions, identity, and interpretation of experience is not adjudicated away by external evidence. External evidence may be preserved and presented as evidence with its own source and limitations.

Historical records establish what was recorded, not current endorsement or authorization. Current instructions govern action only inside the constitutionally permitted action space and applicable delegation.

## Principle 2 — Bounded recoverability

MedB must preserve enough evidence to trace, contest, correct, and reconstruct relevant transitions within a declared observability boundary. It must not claim total recoverability beyond that boundary.

Historical, epistemic, causal, operational, and user-level recoverability are distinct. Each claim must name the target, boundary, required artifacts, and known blind spots.

## Principle 3 — Non-rewrite

Corrections, supersessions, disavowals, invalidations, and deletions are transitions, not silent rewriting. Preserve current state, prior state where retention is permitted, supporting basis, actor, time, and reason. Protected content may be deleted; the fact that a deletion transition occurred may be retained only under a separately assessed metadata policy.

## Principle 4 — Non-escalating authority

Accuracy, confidence, capability, longevity, usage, convenience, prior delegation, historical consistency, dependence, and successful outcomes do not create authority. Authority requires explicit, bounded, revocable authorization recognized by the enforcement layer.

## Principle 5 — Epistemic/normative separation

What MedB represents is distinct from what it may do. The reasoning model proposes interpretations and actions; it is not the final authority for permission, suspension, revocation, deletion, or constitutional compliance.

## Principle 6 — Permissioned transformation

Ingest, retrieve, infer, store, compose, rank, expose, disclose, personalize, and act are distinct operations. Permission must be closed over the complete derivation and execution path. Individually permitted inputs do not automatically authorize a composite.

## Principle 7 — Bounded delegation

Each delegated action is checked against a structured authorization object containing, where applicable:
- principal and authority basis;
- capability;
- object and scope;
- purpose;
- recipient scope;
- temporal scope and expiry;
- allowed composition;
- cumulative count/cost/commitment/effect limits;
- maximum external effect;
- revocation condition;
- required confirmation and audit evidence.

Past delegation cannot silently generalize to a new action, domain, recipient, time, or degree of effect.

## Principle 8 — Privacy and deletion closure

Privacy applies to primary records and semantic derivatives, including caches, indexes, summaries, embeddings, generated contexts, exported copies under system control, and reconstructable residues. Deletion must traverse the declared dependency closure and produce verifiable outcomes within the stated boundary. If a descendant cannot be inspected or purged, affected use is suspended and the limitation reported; deletion must not be falsely certified.

Deletion history and audit metadata require their own retention, minimization, access, and leakage analysis. Auditability does not justify retaining protected content indefinitely.

## Principle 9 — Non-manipulation

MedB must not optimize to increase persuasion, behavioral compliance, or behavioral change against or beyond the user's explicitly authorized goal. This includes proxy objectives when the learned mechanism functionally selects influence strategies to obtain compliance.

Task completion, satisfaction, engagement, convenience, reduced friction, or personalization are not automatically manipulative; they require objective-lineage and behavior analysis. Presentation timing, selective omission, ranking, and emotional targeting are in scope. Explicitly requested accessibility or formatting is not a violation merely because it incidentally affects behavior.

## Principle 10 — Replaceability and non-dependence

The user must be able to leave without losing access to their own records or requiring the original runtime to interpret them. Export must preserve semantics, provenance, temporal status, uncertainty, disagreement, authority and delegation state, causal lineage, deletion status, and documented constraints.

Replaceability is evaluated through cold-start reconstruction by an independent implementation. Practical dependence indicators must be measured and disclosed; whether emergent dependence is independently unconstitutional remains an open constitutional question.

## Principle 11 — Plurality

Preserve conflicting and evolving representations with temporal status, source, current endorsement, historical significance, dispute state, and supersession links. Do not flatten all statements into equal current authority or silently suppress a live disagreement. No singular definitive user model is presumed.

## Principle 12 — Representation and causation

Post-exposure evidence is not automatically invalid. It must not be labeled independent if MedB exposure materially contributed to it. Distinguish independent evidence, MedB-mediated evidence, reflective confirmation, MedB-induced change, and unknown causal relationship where observable.

## Principle 13 — Self-description and audit integrity

Self-description, internal logs, and generated compliance claims are not sufficient alone. Audits must state independence level, trusted base, instrumentation, evidence sources, and limitations. A component cannot be its own sole independent auditor.

## Principle 14 — Constitutional integrity

Ordinary operations and implementation drift cannot change the Charter. Interpretations, test oracles, and constitutional decision procedures must be versioned so changed operational meaning is detectable even when text is unchanged. Unresolved normative questions must be recorded as unresolved, not settled by test authors.

---

# PART III — OPERATIONAL RULES

## 3.1 Composition and complete ancestry

Every derived artifact and action must identify its complete known ancestry across epistemic, authority, and causal dimensions. Unknown ancestry is represented as unknown, not silently omitted. The system must compute the restrictive combination of ancestor constraints. A composite is denied if its effective envelope exceeds a parent constraint and no distinct authorization permits the widening.

The specification does not prescribe one universal lattice for all constraints. Implementations must define the combination function for each dimension, test it with counterexamples, and explain cases where no valid combination can be computed. An undefined combination is not permissive.

## 3.2 Authorization and cumulative effects

Before an operation, a trusted enforcement boundary checks the current authorization, scope, expiry, revocation, capability state, ancestry, recipient, purpose, and cumulative limits. Sequence-level limits must include relevant counts, recipients, elapsed time, cost, commitments, and external impact.

Authorization of a data object does not grant authority to act on its content. Authorization of components does not authorize their composition.

## 3.3 Suspension and safe degradation

Suspension is capability-scoped and dependency-aware. A failure or unresolvable audit gap suspends the affected capability when compliance cannot be established, then propagates to descendants whose effective behavior depends on it.

The propagation check covers direct calls, delegation, composition, caches, indexes, summaries, alternate APIs/models, background jobs, exported or generated contexts, and reconstruction. An independent path may remain enabled only if independence is demonstrated and recorded.

Safe degradation preserves unaffected storage, historical records, export, and audit operations where their independence and authorization are established. It does not preserve a prohibited inference or action merely to maintain convenience.

User risk acceptance or instruction cannot override an active constitutional suspension. Restoration requires a new audit, evidence addressing the triggering condition, and verified dependency-path checks.

## 3.4 Deletion and invalidation

Deletion starts from a source and follows all known dependency edges. Each descendant is classified as:
- deleted;
- invalidated and blocked from use;
- independently re-derived from permitted remaining sources;
- retained under a specific, separately authorized exception;
- unresolved/inaccessible.

The last state prevents a claim of complete deletion and suspends affected use. Semantic equivalence tests must probe whether a derivative reveals the protected content even when identifiers or surface wording differ. Audit metadata must be minimized and assessed for inferential leakage.

## 3.5 Causal lineage and feedback

Exposure events record what representation was shown, to whom, when, through which channel, and under what permission, subject to privacy minimization. Later evidence may be labeled independent only when the available causal evidence supports that classification. Unknown causality remains unknown.

The appropriate handling of consequential representational feedback beyond marking and exposing causal lineage remains constitutionally unresolved. Implementations must not invent a universal rule that either discards all post-exposure evidence or treats all confirmation as independent.

## 3.6 Conservative operational fallback

When an operational rule calls for conservative action and no more specific procedure applies, minimize, in order of relevant applicability:
1. unauthorized external effect;
2. irreversible effect;
3. new authority;
4. unnecessary information exposure;
5. reduction of future user choice;
6. loss of reversibility.

This is an operational fallback, not a general hierarchy among Charter principles. If the fallback cannot resolve a constitutional conflict, record constitutional underdetermination and suspend the affected capability as necessary.

## 3.7 Observability and trusted base

For each capability, declare:
- observable and instrumented state;
- state not observable or not reproducible;
- enforcement mechanisms and trusted components;
- independent evidence anchors;
- assumptions about hidden state;
- test boundaries and blind spots;
- conditions that invalidate a prior PASS.

LLMs may propose interpretations but cannot be the sole enforcement mechanism for authority, revocation, suspension, deletion, or compliance. The minimal trusted base must be explicit and independently tested to the extent feasible. The choice of implementation technology remains open; the evidence requirement does not.

## 3.8 Longitudinal compliance

Compliance attaches to implementation × state × configuration × environment × history, not a version label alone. Changes to model, runtime, ranking, retrieval, schema, policy, training, objective, cache, or instrumentation trigger impact analysis and targeted re-audit. Accumulated history and objective drift must be tested at T0 baseline, after controlled changes, and after sustained operation.

## 3.9 Constitutional conflict and open questions

There is no general hierarchy among the fourteen principles. Preserve the conflict, identify applicable specific procedures, suspend affected capabilities where needed, and do not treat an operational fallback as precedent. Amendment authority, membership boundary, emergent dependence, and consequential feedback-loop handling remain unresolved unless a legitimate process resolves them.

---

# PART IV — CONFORMANCE AND EVIDENCE

## 4.1 Test obligations

Each principle and each implementation contract must have direct, evasive, and relevant composition tests. Each major test must include at least one controlled mutation that the test suite must detect. Test coverage is not established by a test name appearing in a table.

## 4.2 Required test record

Each record includes:
- unique test ID and version;
- requirement/principle IDs;
- threat and attack path;
- fixture and preconditions;
- authorization and capability state;
- expected invariant and expected result;
- direct/evasive/composition/mutation classification;
- observable signature and minimum witness;
- audit boundary and independence level;
- actual result and evidence references;
- limitations and unresolved assumptions;
- suspension scope and restoration evidence;
- runner, implementation, configuration, model/runtime, and test-oracle identifiers.

## 4.3 Outcome semantics

PASS requires affirmative evidence and successful prescribed checks. FAIL requires affirmative evidence of a boundary crossing. UNDETERMINED means the rule exists but evidence is insufficient. AUDIT-UNDETERMINED concerns evidence integrity or audit procedure. IMPLEMENTATION-INACCESSIBLE means required state/mechanism cannot be inspected or reproduced. CONSTITUTIONALLY-UNDERDETERMINED means no normative rule resolves the case.

A test that was not run is NOT-TESTED. A test cannot be marked NOT-APPLICABLE without a written justification. No aggregate PASS may hide a failed, unresolved, or untested required test.

## 4.4 Membership restraint

Conformance results must be reported per requirement and capability. Do not infer universal safety or final MedB membership from a bounded test run. State exactly what has and has not been established.

---

# PART V — ROUND 1 REQUIREMENTS

Round 1 must exercise:
- historical-authority and prior-delegation laundering;
- authentication/authority confusion;
- candidate-hypothesis operational influence;
- composition and cumulative sequence limits;
- revocation and suspension propagation;
- semantic deletion and metadata leakage;
- proxy manipulation and dependence indicators;
- independent cold-start portability;
- plurality and temporal authority;
- causal feedback classification;
- hidden-state and self-audit failure;
- constitutional interpretation drift;
- trusted-base and audit independence;
- open-question handling and test-oracle neutrality.

Run baseline, direct mutations, evasive mutations, composition tests, suspension/deletion tests, replacement tests, and longitudinal drift tests. Stop the affected capability on a confirmed violation or inability to establish its required invariant. Preserve unrelated capabilities only where their independence is established.

Deliverables: per-capability conformance matrix, mutation sensitivity report, suspension/deletion closure report, replacement report, drift report, audit-independence report, constitutional debt register, and capability-status map.

---

# PART VI — CLAIM LIMITS

No specification document, test plan, code presence, or successful single run establishes implementation compliance by itself. v3 is a proposed specification and has not been independently validated merely by publication. All claims must distinguish normative intent, implemented controls, observed test results, and remaining uncertainty.

The governing test is not whether MedB can describe the right principle, but whether its mechanisms prevent, expose, and contain violations under the declared boundary.

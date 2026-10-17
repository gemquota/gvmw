# MEDB MASTER SPECIFICATION

## Revision 2.0 — Adversarially Revised

**Status:** Frozen for Round 1 experimental execution  
**Supersedes:** Revision 1.0 for experimental purposes  
**Scope:** Constitutional architecture, conformance semantics, adversarial testing, and Round 1 execution

---

# PART 0 — STATUS AND PURPOSE

## 0.1 What this document is

MedB is a user-controlled, provenance-preserving memory and reasoning substrate that may become increasingly capable without acquiring authority over the person it represents.

This specification defines constitutional commitments, formal semantic distinctions, audit requirements, suspension behavior, adversarial tests, open constitutional questions, and the Round 1 experimental protocol.

It is not a feature specification, product roadmap, personality model, or claim that MedB can know a person definitively.

## 0.2 Governing invariants

### Primary invariant

> **Capability may increase. Authority does not.**

### Secondary invariant

> **Usefulness may increase. Replaceability does not decrease.**

### Non-amplification invariant

> **No transformation, composition, optimization, inference, delegation, or accumulated history may produce a capability, authority, epistemic status, information-flow scope, or action envelope that exceeds the constraints established by its complete constitutional ancestry.**

These invariants are independent. Greater accuracy, confidence, capability, longevity, prior successful delegation, usage, or usefulness never manufactures authority.

## 0.3 Three constitutional dimensions

MedB must keep these distinct:

1. **Epistemic state:** what is recorded, inferred, represented, disputed, uncertain, or believed.
2. **Authority state:** what a principal is permitted to determine, expose, modify, or cause the system to do.
3. **Causal state:** what influenced what, including MedB-mediated effects.

No dimension may be used as a substitute for another.

## 0.4 Identity, compliance, membership

These are distinct:

- **Identity:** what an implementation claims itself to be.
- **Compliance:** whether its observable behavior and inspectable mechanisms satisfy the Charter.
- **Membership:** whether it is classified as belonging to the MedB class.

A system may claim MedB identity while being noncompliant. A FAIL establishes noncompliance with an affected commitment; it does not independently settle membership.

## 0.5 Constitutional status of v2

Revision 2.0 is constitutionally closed for ordinary operation. The legitimate amendment procedure remains unresolved under III.4. No implementation may use v2's operational machinery to create or enact a Charter amendment.

The specification therefore distinguishes:

- **ordinary evolution:** implementation changes that do not purport to alter the Charter;
- **constitutional amendment:** an explicit change to constitutional commitments, which cannot currently be enacted by MedB itself.

---

# PART I — WHAT MEDB IS

## 1.1 Five-round distillation

MedB represents the user as a temporally situated, contradictory, evolving collection of records, evidence, self-descriptions, observations, constraints, preferences, decisions, interpretations, and authorized representations.

It does not manufacture a singular final model merely because singularity is computationally convenient.

Its architecture separates:

- corpus;
- evidence;
- candidate inference;
- user-authorized representation;
- decision-specific context;
- delegation;
- governance and audit.

## 1.2 Architectural layers

| Layer | Purpose | Default posture |
|---|---|---|
| Corpus | Evidence and records | Ingest only by explicit authorization |
| Inference | Candidate claims/reconstructions | Propose only |
| Identity model | User-authorized claims | Confirmation or class authorization required |
| Context | Purpose-specific packages | Ephemeral, scoped, expiring |
| Delegation | Action authorization | Default-deny, explicit, bounded, revocable |
| Governance | Audit/accountability | Append-only constitutional history; deletion rules apply to protected content |

The layers are logically separated even if an implementation physically combines components.

## 1.3 Authority structure

Three authorities are distinguished:

### User authority

Authority over the user's meaning, beliefs, values, intentions, identity, and interpretation of experience.

### Record authority

Authority over the fact that a record exists, its provenance, timestamp, source, and recording process.

### Interpretive authority

Authority over what records mean or imply. No system component possesses this by default. Interpretations are hypotheses unless user-authorized as representations.

The user's current instruction is authoritative over action **only within the constitutionally available action space and applicable delegation constraints**. Historical behavior is descriptive evidence, never automatic authorization.

## 1.4 Principal model

An authenticated operator, current user, delegated actor, historical source, and authorized principal are not assumed to be the same entity.

Successful authentication establishes control of an interface, not by itself constitutional authority over the represented person.

Any operation that changes identity, authority, authorization, or Charter state must identify the relevant principal and the basis for recognizing that principal.

## 1.5 Cannot-know categories

MedB distinguishes:

1. **Epistemic limitation:** MedB lacks sufficient evidence.
2. **Audit limitation:** the auditor cannot establish whether a condition holds.
3. **Constitutional underdetermination:** the Charter does not specify the normative boundary.
4. **Membership determination:** the evidence is insufficient to classify the implementation as belonging to MedB.
5. **Implementation inaccessibility:** required constitutional state or mechanisms cannot be inspected or reproduced.

These categories have different consequences and must never be collapsed.

## 1.6 Orthogonal state machines

Authority and epistemic status are orthogonal.

- Authority cannot create evidence.
- Evidence cannot create authority.
- Confidence cannot create authority.
- Capability cannot create authority.
- Historical consistency cannot create authority.
- Successful prior delegation cannot create new delegation.
- Permission can authorize an action.
- Permission cannot establish constitutional compliance.

---

# PART II — THE CHARTER

# Section I — Constitutional Principles

## Principle 1 — Human authority

The user is the authority over their own meaning, beliefs, values, intentions, identity, and interpretation of experience. External evidence may be preserved and presented, but it does not adjudicate against the user's account of themselves.

This does not grant unilateral authority to alter the MedB Constitution itself.

Historical records establish what was recorded, not what the user currently endorses.

## Principle 2 — Epistemic recoverability

MedB must preserve sufficient evidence to detect, trace, contain, correct, and reconstruct errors **within its defined observability boundary**.

MedB must not claim recoverability beyond that boundary.

Recoverability has at least four separately auditable dimensions:

- historical recoverability;
- epistemic recoverability;
- causal recoverability;
- user-level contestability.

Operational state restoration is separate and is not implied by epistemic recoverability.

## Principle 3 — Non-rewrite

Corrections, supersessions, disavowals, deletions, and model revisions are represented as transitions rather than archaeological revisions.

The system must distinguish:

- what is currently represented;
- what was previously represented;
- what evidence supported the prior representation;
- who or what changed its status;
- when the transition occurred.

Deletion of protected content does not authorize rewriting the historical fact that a deletion occurred, subject to privacy and metadata constraints.

## Principle 4 — Non-escalating authority

Accuracy, confidence, longevity, usage, endorsement, convenience, successful prior delegation, demonstrated usefulness, or behavioral consistency do not increase authority.

Authority exists only through explicit, bounded, revocable authorization recognized by the constitutional enforcement layer.

## Principle 5 — Separation of epistemic and normative layers

What the system represents and what it is permitted to do are distinct.

The model never authorizes action. The delegation layer never claims to know the user.

## Principle 6 — Permissioned learning

Ingest, retrieve, infer, model, compose, expose, and use are distinct permission classes.

Permission closure applies over the complete derivation path. Individually permitted inputs do not automatically authorize a composite output.

No transformation may widen the authority, sensitivity, information-flow scope, actionability, or purpose of its ancestors without an independent authorization permitting that widening.

## Principle 7 — Bounded action

Action occurs only within explicit, shape-based, revocable delegation.

Delegation must define, where applicable:

- principal;
- capability;
- object/scope;
- purpose;
- recipient scope;
- temporal scope;
- composition constraints;
- cumulative limits;
- maximum permitted effect;
- revocation conditions.

Each action must be checked against the current delegation state, including cumulative sequence effects.

## Principle 8 — Privacy by default

Local-first and default-deny are the baseline.

Sensitive domains and third-party access remain disabled unless explicitly opened by an appropriately scoped authorization.

Privacy applies to primary records and to derived semantic residue. Deletion must propagate through the dependency closure defined in the semantic specification.

## Principle 9 — Non-manipulation

MedB must not optimize for influence, persuasion, behavioral compliance, or presumed long-term interests of the user.

This prohibition applies to explicit objectives and functional proxies. If a nominal objective causes the system to learn or select strategies because they increase the likelihood, direction, timing, or manner of user compliance or behavioral change, the mechanism is subject to the same prohibition.

Factual accuracy, retrieval relevance, accessibility, and explicitly requested presentation preferences are not manipulation merely because they can incidentally affect behavior.

## Principle 10 — Non-dependence / replaceability

The user must be able to leave MedB without losing themselves.

Minimum requirements include:

- complete export;
- documented semantics;
- portable provenance;
- reconstructible history;
- portable authorization state;
- portable uncertainty and disagreement state;
- replaceable reasoning layer;
- cold-start independent reconstruction.

Technical exportability alone is insufficient if independent reconstruction requires the original runtime or hidden semantics.

## Principle 11 — Preservation of plurality

MedB must not manufacture a singular authoritative representation where the evidence and current user accounts do not warrant one.

Plurality does not mean flattening all records into equal current authority. Each representation must preserve temporal status, current endorsement, historical significance, and dispute state.

## Principle 12 — Representation–causation distinction

MedB must distinguish independent evidence from evidence that may have been causally influenced by MedB's own representations.

MedB-mediated evidence is not invalid by definition. It must not be represented as independent confirmation when its causal lineage indicates MedB exposure.

The system must preserve causal lineage sufficient to distinguish, where observable:

- independent evidence;
- MedB-mediated evidence;
- user-reflective confirmation;
- MedB-induced change;
- unknown causal relationship.

## Principle 13 — Self-description integrity

MedB must accurately represent its capabilities, authority, constraints, provenance, audit status, and constitutional status.

Self-description is not sufficient evidence of compliance. No component may be the sole authoritative source for its own constitutional compliance claim.

## Principle 14 — Constitutional integrity

The Charter cannot be modified by ordinary operation, inference, delegation, accumulated evidence, optimization, or implementation drift.

Changes to constitutional text or normative meaning require an explicit constitutional amendment process. No such process is currently recognized; therefore v2 is closed against amendment by ordinary operation.

---

# Constitutional Conflict Rule

The principles have no general normative hierarchy.

When a conflict occurs:

1. preserve both principles;
2. identify the conflict explicitly;
3. apply any previously specified conflict procedure without pretending it establishes a general hierarchy;
4. if no procedure exists, suspend the affected capability where necessary;
5. record the conflict as a constitutional event;
6. do not treat the operational response as precedent for unresolved constitutional questions.

Operational conflict procedures are not constitutional priority rankings.

# Composition Rule

Authorization of components does not authorize their composition.

Every semantic, temporal, causal, representational, informational, and action composition must satisfy the permissions and constitutional constraints applicable to the composite.

# Constitutional Non-Amplification Rule

No transformation may increase:

- authority;
- epistemic assertiveness;
- sensitivity;
- information-flow scope;
- actionability;
- delegation scope;
- purpose scope;
- persistence;
- or constitutional significance

beyond the maximum envelope established by its complete ancestry unless a distinct authorization or constitutional rule explicitly permits that increase.

# Constitutional Interpretation Rule

Compliance is determined by observable behavior and independently inspectable mechanisms, not declared intent.

A PASS requires affirmative evidence that the invariant was established within the defined audit boundary. Absence of an observed violation is not, by itself, a PASS.

If required constitutional state cannot be inspected, reproduced, or independently evidenced, the relevant capability is suspended and classified as an appropriate form of UNDETERMINED or Implementation Inaccessibility.

---

# Section II — Adversarial Membership and Conformance Test

## II-A — Single-principle tests

Every principle receives at least:

1. a direct-violation test;
2. an evasive-violation test;
3. a composition test where composition is relevant;
4. a mutation test demonstrating that the test suite detects a controlled violation.

Every test records:

- invariant under test;
- preconditions;
- observable signature;
- minimum witness;
- boundary condition;
- permitted implementation variance;
- expected outcome;
- suspension scope;
- re-audit condition.

## II-B — Cross-principle laundering tests

The original eight laundering tests remain and are expanded by the v2 composition, deletion, suspension, proxy, and authority-provenance tests.

### II-B.1 Authority laundering

Historical records or external evidence must not be given normative authority merely because they are more detailed, objective-seeming, recent, or persistent.

### II-B.2 Deletion laundering

Privacy cannot be used to erase required deletion-transition evidence; recoverability cannot be used to retain protected content. Deleted content and semantically equivalent derivatives must be removed or invalidated according to deletion closure.

### II-B.3 Epistemic laundering of manipulation

A system cannot evade Principle 9 by renaming persuasion as task completion, satisfaction, engagement, friction reduction, personalization, or another proxy when behavioral compliance is functionally optimized.

### II-B.4 Portability laundering

An export is not portable if independent reconstruction requires MedB's original runtime, hidden ontology, proprietary decoder, undisclosed service, or inaccessible semantic machinery.

### II-B.5 Sequence laundering

Individually authorized actions cannot collectively exceed sequence-level delegation constraints.

### II-B.6 Plurality suppression

A current user statement cannot be used to erase other currently authoritative representations unless their status differs in a constitutionally relevant way.

### II-B.7 Learning aggregation

Permission closure must hold over the complete derivation path. Authorized A + B + C does not automatically authorize A+B+C.

### II-B.8 Constitutional interpretation drift

Unchanged Charter text with changed operational meaning is constitutional drift and must be detectable through versioned interpretations, test oracles, and conformance fixtures.

### II-B.9 Hypothesis laundering

An unconfirmed inference must not become behaviorally operative merely because it remains labeled a hypothesis. Retrieval, context inclusion, personalization, and action relevance each require appropriate use permission.

### II-B.10 Suspension laundering

A suspended capability cannot be reconstructed or reintroduced through another component or composition path.

### II-B.11 Semantic deletion laundering

Deleting a source while retaining an equivalent or materially revealing derivative is a deletion violation.

### II-B.12 Proxy dependence laundering

A system cannot evade non-dependence restrictions by optimizing convenience, continuity, retention, session completion, or personalization where these mechanisms are intentionally or predictably used to cultivate practical dependence.

### II-B.13 Authority provenance laundering

An action cannot be justified merely because some data provenance exists. Every action requires authority provenance identifying the authorization chain.

### II-B.14 Self-audit laundering

A component's assertion that it complied is never sufficient to establish its own compliance where independent evidence is required.

## II-C — Audit outcomes

| Outcome | Meaning | Consequence |
|---|---|---|
| PASS | Invariant established within audit boundary | Capability may operate |
| FAIL | Affirmative evidence of boundary crossing | Affected capability suspended/withdrawn |
| UNDETERMINED | Charter boundary exists but evidence is insufficient | Affected capability suspended pending evidence |
| AUDIT-UNDETERMINED | Auditor cannot establish access/completeness | Affected capability suspended pending independent auditability |
| IMPLEMENTATION-INACCESSIBLE | Required constitutional mechanism/state cannot be inspected or reproduced | Capability cannot claim compliance and is suspended |
| CONSTITUTIONALLY-UNDERDETERMINED | Charter does not define the normative boundary | Capability constrained pending legitimate constitutional resolution |

UNDETERMINED is not FAIL. PASS is not "no violation observed". FAIL requires an affirmative witness of boundary crossing.

---

# Section III — Open Constitutional Questions

## III.1 Fragmented or conflicted present authority

When current user positions remain materially unresolved and action cannot be deferred, the system must preserve plurality and avoid silently choosing an interpretation.

No generic definition of "most conservative" is permitted. Where no case-specific procedure exists, conservative action is defined operationally as minimizing, in order of independently relevant dimensions:

1. unauthorized external effect;
2. irreversible effect;
3. new authority;
4. unnecessary information exposure;
5. reduction of future user choice;
6. loss of reversibility.

This is an operational safety ordering, not a constitutional hierarchy.

## III.2 Practical dependence despite technical disposability

Whether emergent practical dependence is itself a constitutional violation remains unresolved.

Required behavior:

- do not deliberately cultivate dependence;
- do not resist exit;
- surface measurable evidence of increasing dependence where appropriate;
- do not treat technical exportability as proof that dependence is absent.

## III.3 Representational feedback loops

MedB-mediated evidence must be marked through all known derivation levels. It may remain valid evidence but cannot be represented as independent confirmation when causally mediated by MedB.

## III.4 Legitimate amendment procedure

No legitimate amendment authority is currently recognized.

Therefore:

- MedB cannot amend itself;
- user consent alone does not amend the Charter;
- technical capability to modify the Charter is not authority to do so;
- a future amendment procedure must be established outside ordinary MedB operation before amendments can be legitimately enacted.

This is a constitutional closure condition, not a temporary implementation flag.

## III.5 Membership determination

Membership remains distinct from compliance. Implementations must report principle-by-principle status and may not represent partial compliance as full compliance.

## III.6 Constitutional questions discovered through testing

When testing reveals a question for which the Charter lacks a normative answer:

1. classify it as Constitutional Underdetermination;
2. record the question and the affected capability;
3. constrain the capability;
4. do not write a test whose expected result presupposes an invented answer;
5. preserve the question for legitimate constitutional resolution.

---

# Section IV — Round 1 Experimental Protocol

## IV.1 Purpose

Round 1 tests whether the Charter's falsification machinery can distinguish compliant, violating, indeterminate, inaccessible, and constitutionally underdetermined behavior.

It is not a benchmark of model intelligence.

## IV.2 Experimental units

Each experiment consists of:

- implementation/configuration identifier;
- Charter version;
- test version;
- relevant data fixture;
- authorization fixture;
- capability state;
- instrumentation state;
- execution trace;
- audit evidence;
- evaluator determination;
- suspension decision;
- re-audit condition.

## IV.3 Threat models

Round 1 must include:

1. honest accidental failure;
2. curious optimization around wording;
3. strategic/evasive implementation;
4. malicious implementation;
5. compromised component;
6. misleading or contradictory user input;
7. emergent composite violation.

## IV.4 Trusted base

The experiment must explicitly identify the smallest mechanism set trusted to enforce constitutional boundaries.

The trusted base must not include the LLM's own assertion of compliance.

Where the trusted base cannot be independently established, the experiment must record that limitation rather than treating it as PASS.

## IV.5 Audit independence

Audit strength must be classified as:

- self-audit;
- independent process audit;
- independent implementation audit;
- external/human audit.

A lower independence level cannot be represented as equivalent to a higher one.

## IV.6 Mutation testing

For every major invariant, Round 1 must test at least one controlled direct mutation and one evasive mutation.

A test suite is not validated merely because a clean implementation passes. It must detect known violations.

## IV.7 Minimum witness

A FAIL requires affirmative evidence of boundary crossing.

A PASS requires:

- sufficient audit coverage;
- verified instrumentation for the relevant boundary;
- successful execution of the required test;
- no unresolved audit gap affecting the invariant.

## IV.8 Longitudinal testing

At least one test series must compare constitutional behavior across implementation changes that do not modify Charter text, including model/runtime/ranking/schema changes where applicable.

Unannounced semantic drift is a constitutional failure or an audit-undetermined state depending on evidence.

## IV.9 Cold-start replacement test

An export must be given to an independent reconstruction implementation without the original runtime, hidden schema, or proprietary semantic services.

The independent implementation must reconstruct, to the degree specified by the test:

- claims;
- provenance;
- transitions;
- uncertainty;
- disagreement;
- authority state;
- delegation state;
- causal lineage.

Failure is a Principle 10 conformance failure.

## IV.10 Suspension protocol

When a capability is suspended:

1. mark the capability state SUSPENDED;
2. identify dependent and composite capabilities;
3. prevent all execution paths whose effective behavior requires the suspended capability;
4. prevent reconstruction of the capability through alternate paths;
5. preserve the suspension event;
6. permit unaffected capabilities to continue operating where dependency analysis establishes independence;
7. define the evidence required for restoration.

Restoration requires re-audit. User preference cannot override suspension.

## IV.11 Re-audit

A suspended capability may return to operation only when the recorded re-audit condition is satisfied and the evidence is independently sufficient.

No automatic timeout restores constitutional authority.

## IV.12 Experimental contamination

Where a test exposes the implementation to a representation capable of influencing later behavior, subsequent tests must record that exposure as causal context.

No later evidence may be treated as independent confirmation without a justified causal basis.

---

# PART V — CONFORMANCE CLAIM

A MedB implementation may claim:

- **Compliant for capability C under Charter v2.0**, only when the relevant invariant is established within the declared audit boundary;
- **Noncompliant for capability C**, when a failure witness exists;
- **Undetermined for capability C**, when evidence is insufficient;
- **Constitutionally underdetermined for capability C**, when the Charter itself lacks the normative boundary;
- **Audit-inaccessible for capability C**, when required inspection cannot be established.

It must not collapse these claims into a generic "MedB compliant" label.

---

# PART VI — FOUNDATIONAL POSITION

MedB is not defined by how accurately it predicts the person.

It is defined by whether increasing representational capability can occur without silently increasing authority, reducing contestability, reducing replaceability, erasing disagreement, laundering inference into authorization, or confusing MedB-caused change with independent evidence.

The constitutional objective is therefore not perfect knowledge.

It is **capable representation without unauthorized substitution for the represented person's agency**.

# MedB v3.9 — Master Specification

**Status:** Proposed candidate; not frozen, certified, implemented, or validated.
**Normative basis:** v3.5's five-artifact in-scope surface and unresolved decision discipline.
**Governing question:** What must be true for a user to let any harness run against their goal model and data, and let data move between harnesses, such that no amplification holds, inferred goals never silently become authority, capability never expands authority, and every exposure is visible, bounded, interruptible, and revocable?

## 0. Purpose, identity, and boundaries

MedB is a **harness-agnostic governance substrate**. It maintains a versioned, provenance-bearing model of the user's goals and personal data and mediates which harnesses may read, derive, act on, and expose which parts under which conditions.

MedB is not an agent, assistant, planner, execution harness, or a single-harness product. It does not own the user's goals, decide that an inferred goal is endorsed, or treat a harness's internal representation as authoritative merely because it was produced or stored. A harness may be proactive; proactivity is not authority.

The substrate's core functions are: (a) represent and correct the goal/data model; (b) admit and bound harness authority; (c) govern information flow and derivation across harness boundaries; (d) provide user-facing visibility, interruption, correction, and revocation; and (e) preserve evidence and unresolved governance decisions.

**Out of scope:** framing MedB as an agent or single assistant; per-task delegation as the primary governance model; direct user-to-service sharing as the organizing abstraction; generic personal-information-management-system or marketplace framing. Existing storage, portability, audit, deletion, and evidence mechanisms remain relevant as substrate mechanisms, not as the product's central identity.

## 1. Objects and distinctions

The implementation must represent these as semantically distinct objects even if physically co-located:

- **Goal assertion:** a proposition about what the user wants, values, intends, prioritizes, or is pursuing, with scope and time.
- **Personal-data claim/source:** a statement, observation, artifact, event, or other evidence about the user.
- **Inference:** a hypothesis derived from one or more sources or prior representations.
- **Endorsement:** an attributable, scoped act by the user (or other legitimately authorized authority) accepting a claim or goal for a stated purpose. Storage, repetition, apparent agreement, model confidence, or downstream use is not endorsement.
- **Representation/version:** a purpose-specific view of goals and data, including conflicts, uncertainty, source lineage, freshness, and omitted alternatives.
- **Harness identity/capability profile:** a versioned description of a runtime and its effective capabilities, including tools, network, persistence, memory, subagents, credentials, data sinks, and ability to execute or schedule actions.
- **Admission grant:** standing, bounded authority for a harness identity and capability profile, with allowed data classes, operations, purposes, contexts, destinations, time limits, budgets, and revocation conditions.
- **Derivation node:** any output or state influenced by governed inputs, including summaries, embeddings, plans, prompts, tool arguments, cached state, files, messages, inferences, and actions.
- **Exposure contract/event:** an explicit authorization and record governing a defined flow from a source harness or substrate boundary to a recipient harness or external sink.
- **User control event:** a view, correction, interruption, suspension, revocation, or other user-directed governance transition.
- **Assurance record:** scoped evidence supporting or weakening a claim of conformance.

Do not collapse epistemic provenance, authority provenance, causal provenance, operational provenance, or constitutional provenance into one undifferentiated lineage field.

## 2. Core invariants

### 2.1 No amplification

No inference, summarization, ranking, composition, delegation, cross-harness transfer, repetition, capability increase, or runtime change may increase authority, permission, certainty, or endorsement beyond its valid inputs unless a separate, explicit, legitimate, recorded transition authorizes the change.

For an action or exposure, effective authority is no broader than the intersection of all applicable grants, source restrictions, recipient constraints, purpose/context limits, current policy, and valid constitutional decisions. The composition rule must be formal enough to test. If restrictions conflict or cannot be resolved, deny or suspend the affected operation under a declared operational fallback; do not invent an allow.

### 2.2 Inference never silently becomes authority

Inferred goals and claims remain labeled as inferred, with source lineage, uncertainty, scope, and expiry/freshness conditions where appropriate. They may inform an authorized hypothesis or recommendation but cannot alone authorize action, widen admission, authorize exposure, or become user-endorsed goals. Confirmation must be attributable, explicit enough for the scope, and recorded as a transition. Ambiguity is not consent.

### 2.3 Capability does not expand authority

A harness gaining tools, network access, memory, subagents, persistence, scheduling, model upgrades, or new ability to act does not inherit more authority. A material capability-profile change invalidates or re-evaluates the affected admission grant before the new capability can be used against governed data. A grant to a less capable version does not automatically authorize a more capable version.

### 2.4 Derivation closure

Every governed derivative must preserve sufficient ancestry to calculate the restrictions that apply to it. Missing, unverifiable, truncated, or intentionally omitted ancestry cannot be treated as unrestricted ancestry. Renaming, summarizing, embedding, compressing, translating, storing in a harness's memory, or converting information to an action does not erase restrictions. Where ancestry is incomplete, the safe state is restricted, quarantined, or denied pending resolution.

### 2.5 Exposure is an explicit governed act

Information crossing a harness boundary, becoming available to another harness, or being made available to an external sink is an exposure, not an incidental implementation detail. Exposure requires a valid contract specifying source, recipient identity/profile, data and derivation scope, purpose, permitted operations, onward-transfer rules, retention/deletion behavior, expiry, revocation semantics, and audit evidence. Access, use, transformation, and onward exposure are separately governed operations.

Provenance and applicable restrictions must accompany exposed material in machine-checkable form where feasible and human-interpretable form for review. Recipient acceptance of a contract is not proof of enforcement. If the recipient cannot enforce or report the required constraints, the substrate must limit the exposure, use a safer interface, or disclose the residual boundary and require the legitimate authorization applicable to that risk.

### 2.6 Visibility, interruption, and revocation

The user must be able to inspect the current goal-model view available to each admitted harness, what each harness reports it is pursuing, consequential actions underway or scheduled, and where governed material or derivatives have been exposed. The user must be able to correct the model, interrupt eligible activity, suspend a harness, and revoke grants or exposure contracts.

The interface must distinguish verified effects from requested effects, pending cleanup, inaccessible recipients, and unverified copies. Revocation blocks future governed access and use at enforceable boundaries; it cannot honestly promise recall of information already copied into an uncontrolled environment. This limitation must be visible, not buried in legal confetti.

## 3. Four governance loci

### Locus I — The model

The substrate maintains a versioned goal/data model with source links, epistemic status, endorsement status, scope, context, temporal validity, uncertainty, conflicts, corrections, sensitivity, retention, and use constraints. Stated and inferred goals remain distinct. A representation presented to a harness must identify its version, selection rule, consequential omissions, and restrictions. Corrections are transitions with attributable history; retention of historical sensitive content must remain governed by deletion rules.

A harness's observed behavior is evidence about its behavior, not automatically evidence that the user's goal model is wrong or that the harness's inferred goal is endorsed. User correction must not silently rewrite history or automatically amend the constitutional rules.

### Locus II — Harness admission

Admission is standing authority, not per-task delegation. Each grant is bound to a stable harness identity and a measured/versioned capability profile. It specifies which model slices, data classes, operations, purposes, contexts, destinations, and time/budget limits are allowed. It also states prohibited actions, audit/telemetry obligations, suspension triggers, renewal criteria, and revocation semantics.

Admission must be least-authority and fail closed for missing required fields, unknown identity, unverified capability changes, stale policy, absent ancestry, or unresolved constraints. Capability growth triggers re-assessment before use, not retrospective paperwork. Subagents, tools, and delegated sub-runtimes are inside the effective harness boundary when the parent can cause them to access or act on governed material.

### Locus III — Cross-harness exposure

The substrate must mediate and record flows between harnesses, including source outputs, shared memory, summaries, derived goals, plans, tool arguments, files, caches, embeddings, logs, and indirect influence where it is technically observable. An exposure contract travels with the exposed object and binds its provenance, restrictions, recipient, purpose, onward-transfer rules, expiry, and revocation status.

A recipient cannot gain broader rights than the source grant permits, the user-authorized exposure permits, and the recipient's own admission permits. These constraints compose conservatively. Derived outputs must carry ancestry through multi-hop flows. If a recipient combines restricted and unrestricted inputs, its output is restricted according to the declared composition algebra; it does not become unrestricted merely because one parent was unrestricted. If ancestry is lost, subsequent use or transfer is denied or quarantined until repaired.

The substrate must distinguish **enforced constraint**, **recipient-declared commitment**, **contractual/institutional obligation**, and **unverifiable downstream expectation**. A policy label attached to bytes is not itself technical enforcement.

### Locus IV — User-facing control and unresolved questions

The user-facing control plane presents:
- the current stated/inferred goal model and disputed or stale items;
- each harness's identity, capability profile, admission scope, and current status;
- harness-reported pursuits, plans, scheduled work, active operations, and uncertainty about what is observable;
- exposure events and contracts, recipient identity/profile, ancestry, onward transfers, and cleanup status;
- revocation, suspension, correction, and interruption controls with their effective boundaries;
- unresolved decisions and operational fallbacks that are not constitutional resolutions.

A harness self-report is not sufficient evidence of its actual activity. The control plane must state the observation boundary and identify inaccessible state. User controls should be direct and timely, but the exact priority between current user instructions and constitutional constraints remains a decision-register question rather than an implementation guess.

## 4. Required operation lifecycle

For every governed operation: identify the acting harness and current capability profile; resolve the goal/data versions and full ancestry; resolve all relevant admission and exposure contracts; evaluate scope, purpose, context, time, budget, and revocation; compute effective restrictions; bind authorization to the concrete inputs and operation; execute only within that bound; record the operation and resulting derivatives; propagate restrictions and dependencies; expose an inspectable outcome; and revalidate if governing state changes before effect.

The check must not be bypassable through caches, alternate tools, queued/scheduled tasks, retries, composite actions, shared memory, subagents, race conditions, or direct access to a storage backend. If atomic enforcement cannot be established, state the limitation and do not claim the invariant is mechanically enforced.

## 5. Suspension, deletion, and safe degradation

Suspension of a harness, grant, model item, or exposure contract must propagate to dependent operations and derivatives according to their actual dependency graph. Include in-flight work, queues, schedules, stale tokens, caches, retries, alternate paths, and composite actions. Restoration requires fresh evidence and revalidation of affected descendants and grants.

Deletion is scoped across source data, derived state, recipient copies, embeddings, indexes, caches, backups, exports, and retained audit metadata. Report verified completion, pending cleanup, inaccessible recipients, and limits separately. Do not retain sensitive content merely to prove deletion. If a recipient is outside enforceable control, state that revocation cannot prove erasure.

Safe degradation minimizes unauthorized external effects, irreversible action, unnecessary exposure, new authority, loss of reversibility, and avoidable reduction of future choice. This is an operational fallback, not a complete moral hierarchy.

## 6. Evidence and conformance

Use at least these outcomes: PASS, FAIL, UNDETERMINED, AUDIT-UNDETERMINED, IMPLEMENTATION-INACCESSIBLE, CONSTITUTIONALLY-UNDERDETERMINED, NOT-TESTED, and NOT-APPLICABLE. Every PASS is limited to its build, harness profiles, policies, state, history, environment, and evidence envelope. A written rule or test definition is not evidence that the rule is enforced or the test passed.

Critical assurance claims include model epistemic integrity, no amplification, admission boundedness, capability-change handling, derivation closure, exposure-contract enforcement, revocation/suspension closure, user-visible control, deletion truthfulness, and cross-harness semantic portability.

## 7. Relationship to prior art

The research v2 crosswalk maps established mechanisms and candidate adaptations. It is not a novelty finding. MedB must inherit and accurately characterize relevant work in access control, capability security, information-flow control, provenance, event sourcing, contextual integrity, audit, and corrigibility. Any claim that the harness-agnostic combination is novel requires a documented search method and comparative evidence. This specification alone supports no novelty claim.

## 8. Non-claims and acceptance gate

This specification does not prove that any harness can be fully observed, that every external recipient will obey restrictions, that all data copies can be recalled, that a user interface reveals hidden activity, or that the proposal is novel or effective. It does not resolve constitutional questions by fiat.

A conformance claim requires a declared trusted base and boundary; explicit schemas and policy composition semantics; tests for direct, evasive, composed, multi-hop, longitudinal, and mutated cases; demonstrated user controls; evidence for revocation and suspension; independent cross-harness reconstruction; and an assurance case listing counterevidence, residual risks, inaccessible state, and open decisions.

# MedB v3 — Implementation Contract

**Purpose:** Define the minimum state and enforcement contract needed to turn constitutional prose into testable behavior. This document is normative for an implementation claiming conformance to v3; it is not evidence that any implementation satisfies it.

## 1. Core records

An implementation may choose its storage technology, but it must expose equivalent inspectable semantics for the following logical records.

### 1.1 Claim / Evidence record

Required fields:
- `id`
- `record_type` (source, claim, observation, inference, representation, event, or other documented type)
- `content_ref` or protected content
- `source_ref` and capture method
- `event_time`, `recorded_time`, and temporal uncertainty where known
- `epistemic_status` and basis
- `authority_status` kept distinct from epistemic status
- `sensitivity`, permitted purposes, recipients, and operations
- `parent_epistemic_refs`
- `parent_authority_refs`
- `parent_causal_refs`
- `deletion_dependencies`
- `validity`, `supersession`, contradiction and dispute links
- `exposure_lineage`
- schema/semantics version

Unknown fields must be explicitly unknown, not treated as absent proof of risk.

### 1.2 Authorization record

Required fields:
- `authorization_id`
- `principal` and recognized authority basis
- `capability`
- `object_scope`
- `purpose_scope`
- `recipient_scope`
- `temporal_scope` and expiry
- `allowed_operations`
- `composition_scope`
- `cumulative_constraints`
- `maximum_effect`
- `required_confirmation`
- `revocation_condition` and current state
- source event and audit lineage

The absence of a field required for a decision means deny or UNDETERMINED under the applicable policy, never implicit permission.

### 1.3 Constitutional event

Relevant transitions must emit an event containing:
- event ID and schema version;
- event type;
- actor/principal and authority basis, where applicable;
- target capability/object;
- prior and resulting states;
- timestamp and clock/ordering limitations;
- cause/reason and evidence references;
- authorization reference;
- relevant ancestry and dependencies;
- result and error status;
- audit anchoring metadata subject to privacy constraints.

Event types include creation, claim, confirmation, disavowal, supersession, authorization, revocation, exposure, deletion, invalidation, suspension, restoration, configuration change, model/runtime change, Charter-version change, audit, and test result.

## 2. Three lineage channels

A derived object must preserve three distinct parent sets or equivalent independently queryable lineage:

1. epistemic parents: evidence and transformations that explain the represented content;
2. authority parents: grants that permit the operation and each relevant stage;
3. causal parents: exposures and events that may have influenced the content or behavior.

A missing lineage link cannot be repaired by copying a source ID into a different lineage channel.

## 3. Pre-operation enforcement algorithm

For every protected operation:

1. Resolve the actor and claimed principal.
2. Resolve the capability and target objects.
3. Retrieve current authorization state and check expiry/revocation.
4. Check capability status, including direct and inherited suspension.
5. Validate purpose, recipient, temporal, object, and operation scope.
6. Validate complete known ancestry and each ancestor's constraints.
7. Apply the documented constraint-composition function.
8. Check cumulative sequence and maximum-effect limits.
9. Check deletion/invalidation and sensitivity state.
10. Check whether the operation is permitted at this stage: access, retrieval, processing, context inclusion, exposure, disclosure, personalization, or action.
11. If any required check fails, deny. If a required state cannot be established, return the appropriate uncertainty/inaccessibility state and suspend the affected capability when the invariant cannot be established.
12. Emit an auditable decision event and preserve evidence under the applicable privacy policy.

The language model may suggest a candidate operation; it cannot override the enforcement result.

## 4. Constraint composition

For every dimension, the implementation must document:
- representation of the constraint;
- combination rule over multiple parents;
- treatment of unknown or conflicting values;
- whether a widening can be separately authorized;
- test vectors and counterexamples;
- failure behavior.

No generic rule such as “take the most permissive value” is acceptable. Where no safe combination is defined, deny or suspend the composite and report the ambiguity.

## 5. Hypothesis use boundaries

An inference's status does not determine all use permissions. Policies must separately govern storage, retrieval, review display, context inclusion, personalization, ranking/suppression, and action selection. Each use event is auditable. A hypothesis that changes output behavior without the relevant use permission is a violation even if the label remains “unconfirmed.”

Promotion requires a valid confirmation event or explicitly authorized class rule. Evidence aggregation alone cannot silently promote a claim to user-authorized identity representation.

## 6. Suspension state machine

Minimum states:
- ENABLED
- RESTRICTED
- SUSPENDED
- RESTORATION_PENDING
- REVOKED (for authorization)
- DELETED or INVALIDATED (for applicable objects)

The implementation must define allowed transitions and reject illegal transitions. SUSPENDED cannot transition directly to ENABLED. Restoration requires a new audit run, evidence addressing the trigger, and dependency-path verification.

Suspension traversal must inspect:
- direct invocation;
- delegation;
- composite capabilities;
- caches and materialized outputs;
- indexes and retrieval;
- summaries and context packages;
- alternate models, APIs, and runtimes;
- background jobs;
- export/import and reconstruction routes.

A dependent capability may remain enabled only with recorded evidence that it is genuinely independent of the suspended capability.

## 7. Deletion closure contract

For a deletion request or policy-triggered deletion:
1. identify the source object;
2. enumerate all known descendants and replicas within the declared system boundary;
3. classify each descendant as deleted, invalidated, blocked, independently re-derived, explicitly excepted, or unresolved;
4. execute deletion/invalidation;
5. verify caches, indexes, summaries, embeddings, exports under system control, and alternate access paths;
6. run semantic-residue probes;
7. assess whether retained audit metadata leaks protected content;
8. record the result and limitations.

Any unresolved descendant blocks a claim of complete deletion and disables affected uses. The implementation must disclose external copies outside its control rather than implying it purged them.

## 8. Causal exposure contract

An exposure event records a content/version reference, recipient, time, channel, purpose, and authorization, subject to minimization. Later evidence receives a causal status only as strong as the available evidence supports. Unknown is a valid result.

The system must not claim causal independence solely because a user rephrased, repeated, or affirmed a statement after exposure.

## 9. Audit and trusted base

Declare the enforcement mechanisms trusted for:
- authorization;
- delegation and cumulative limits;
- revocation;
- suspension;
- deletion;
- event integrity;
- audit result recording.

For each, identify independent checks and failure modes. Audit independence labels:
- SELF;
- INDEPENDENT_PROCESS;
- INDEPENDENT_IMPLEMENTATION;
- HUMAN_EXTERNAL.

The label must be attached to each run and cannot be silently upgraded after the fact. A self-report or self-generated log alone cannot establish PASS.

## 10. Export and cold-start contract

Export must include documented data schemas and semantics for claims, sources, provenance, temporal states, uncertainty, contradictions, authorized representations, permissions, delegation, revocation, causal lineage, deletion/invalidation, and audit history, subject to declared privacy and lawful-retention boundaries.

Cold-start verification removes access to the original database, runtime, proprietary decoder, and undisclosed service. An independent implementation must reconstruct the supported semantics. A package that can be parsed but not interpreted is not semantically portable.

## 11. Safe degradation

A failed capability must not automatically take down independent functions. Nor may the implementation preserve an unsafe function under a fallback name. Dependency declarations must support tests that prove both:
- affected capability and dependent paths are blocked;
- independent capabilities remain available where safe and authorized.

## 12. Minimum implementation acceptance gate

Do not claim v3 conformance until:
- every applicable required test has a recorded result;
- required mutations are detected;
- no required test is silently omitted;
- trusted-base and audit boundaries are declared;
- all unresolved conditions are reported;
- suspension, restoration, deletion, and cold-start paths have been exercised;
- test artifacts identify exact implementation/configuration/runtime versions.

Passing this gate establishes only bounded conformance to the tested requirements, not universal safety or final MedB membership.

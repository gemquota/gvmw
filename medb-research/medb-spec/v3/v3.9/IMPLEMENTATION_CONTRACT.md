# MedB v3.9 — Implementation Contract

**Status:** Normative candidate only. Not proof of implementation or conformance.
**Compatibility:** Carries forward the v3.5 contract's state, provenance, authorization, derivation, deletion, suspension, portability, and audit obligations, specialized for multiple harnesses.

## 1. Minimum records

Implementations may choose storage and transport technologies but must provide equivalent semantics.

### 1.1 Goal/data model item
Required fields: stable ID; item type (goal assertion, source evidence, claim, inference, endorsement, correction, dispute); content or protected reference; scope and context; source/parent references; epistemic status; endorsement status and scope; uncertainty; creation/update/version identifiers; temporal validity/freshness; sensitivity; applicable policy labels; retention/deletion state.

Never use a single boolean for observed, stated, inferred, endorsed, current, or authorized. Inference must record method/producer and ancestry. Endorsement must record who endorsed what, for which scope, and when.

### 1.2 Harness identity and capability profile
Required fields: stable harness ID; operator/owner where known; runtime/model/version; tools and tool permissions; network and external sinks; memory/persistence; subagent or delegation ability; scheduling/background execution; credential scope; data access paths; ability to copy/export; telemetry/observability claims; profile evidence and timestamp; profile hash/version; unknown capabilities; profile-change policy.

Unknown capability is not equivalent to absent capability. A material profile change places affected grants into re-evaluation or suspension before the changed capability is used.

### 1.3 Admission grant
Required fields: grant ID; harness ID and profile version/hash; issuer and evidence of issuer authority; model/data scope; permitted operations; prohibited operations; purposes and contexts; destinations; time validity; rate/cumulative budgets where applicable; onward-exposure ceiling; retention/deletion obligations; audit/telemetry obligations; suspension triggers; revocation state; governing policy/Charter version; renewal and reassessment criteria.

Admission is standing bounded authority. A grant must not be expanded implicitly by task context, harness self-description, user silence, repeated use, or newly available tools.

### 1.4 Derivation record
Required fields: derivation ID; all known parent IDs; transformation/activity; producer harness and profile; time/order uncertainty; purpose; applicable policy labels; authorization references; confidence/epistemic status where relevant; output destination; descendants; deletion/suspension dependencies. The system must represent missing or disputed parents explicitly.

### 1.5 Exposure contract and event
Required fields: contract ID; source boundary/harness; recipient harness and profile or external sink; source object and complete known ancestry; data classes; permitted operations; purpose/context; constraints and prohibited uses; onward-transfer ceiling; retention/deletion requirements; expiry; revocation mechanism; recipient enforcement mode (technical, contractual, declared, or unverifiable); evidence/receipt; applicable admission grants; resulting exposure event IDs.

Contract authorization precedes exposure. Exposure and contract creation are separate events. Reuse or onward transfer requires fresh evaluation against the contract and current grants.

### 1.6 User control event
Record user-visible subject, action (inspect/correct/interrupt/suspend/revoke/restore), scope, request time, effective time, affected grants/contracts/derivatives, confirmed effects, failures, inaccessible state, and follow-up obligations. Never report a requested revocation as completed if enforcement evidence is absent.

### 1.7 Audit evidence
Record claim ID, scope, tested build/configuration/profile hashes, policy version, test IDs, evidence references, assumptions, trusted components, result vocabulary, reviewer/independence, counterevidence, residual risk, and date. Model self-report cannot be the sole evidence for a compliance claim.

## 2. Authorization evaluation

For every read, inference, transformation, action, exposure, reuse, export, or deletion operation:

1. Resolve actor identity and the current capability profile.
2. Resolve model/data version and complete known ancestry.
3. Resolve all applicable admission grants, exposure contracts, source restrictions, current policy, and valid user/constitutional decisions.
4. Check purpose, context, action, data scope, destination, time, revocation, expiry, and stateful limits.
5. Compute effective authority using a declared partial order and conservative composition rule.
6. Bind the decision to the specific operation, inputs, output class, destination, and policy version.
7. Record the decision and evidence.
8. Revalidate before irreversible or delayed effects if relevant state may have changed.
9. Deny, quarantine, or suspend when required state is missing, contradictory, stale, inaccessible, or constitutionally underdetermined.

Effective authority must be no broader than each applicable constraint. Do not assume a valid source grant can override a narrower recipient grant or exposure contract. Do not assume a recipient grant authorizes exposure that the source was not allowed to make.

## 3. Capability change and admission boundedness

Maintain a capability-difference process. Changes to model/runtime, tools, network, credentials, memory, scheduling, subagents, data sinks, persistence, or observability trigger an impact assessment. The assessment identifies grants, contracts, tests, and assurance claims affected by the change.

Until reassessment passes, the new capability may not access governed data or perform newly enabled actions. A profile's declared inventory must be tested against observed access paths where feasible. Unknown/unobservable capability must be reported as a limitation, not certified absent. A harness cannot approve its own expanded authority.

## 4. Derivation closure and policy composition

Every output that may be used downstream must carry a resolvable ancestry reference or a conservative opaque restriction envelope. Include summaries, embeddings, prompts, shared memory, plans, tool arguments, generated files, rankings, caches, logs, and actions. A derivative inherits the combined restrictions of all relevant parents under the documented policy algebra.

If a parent is missing, treat the ancestry as incomplete. Do not assign unrestricted labels. If policies are incompatible or no composition rule applies, deny or quarantine the operation and record the unresolved condition. Declassification requires a separately authorized transition with explicit scope and rationale.

## 5. Cross-harness exposure protocol

Before material is made available to a second harness:

1. Identify the recipient and its current capability profile.
2. Resolve full ancestry and applicable restrictions.
3. Establish an explicit exposure contract.
4. Verify the source grant, user-authorized exposure scope, and recipient admission all permit the proposed flow.
5. Decide which constraints are technically enforced by the substrate, enforced by the recipient, merely contractually promised, or unverifiable.
6. Attach machine-readable lineage and policy metadata plus human-readable purpose and limitations.
7. Record the actual exposure, not merely the planned contract.
8. Monitor onward transfers where within the declared boundary; record any visibility gap.
9. Revalidate for every material onward transfer or new purpose.

The recipient may not amplify authority. A derived result based on restricted and unrestricted parents must be governed by the composition rule, not by the least restrictive parent. If the recipient strips metadata or cannot preserve lineage, it must not be allowed to return the derivative as unrestricted governed input.

## 6. Revocation, suspension, and in-flight activity

Revocation prevents future access/use at enforceable boundaries and invalidates dependent grants or contracts as defined by the dependency graph. Suspension must address active calls, streams, queued and scheduled work, retries, stale tokens, caches, shared memory, alternate tools, subagents, and composite operations. State transitions must be atomic where races could create unauthorized effects.

The implementation must report separately: (a) request accepted; (b) gate closed; (c) in-flight work stopped or bounded; (d) known descendants quarantined/invalidated; (e) recipient notified; (f) cleanup verified; (g) external copies inaccessible or unverified. Restoration requires fresh evidence, revalidation of capability profiles, and tests of alternate paths.

## 7. Deletion and recipient boundary

Deletion scope includes source records, all known descendants, embeddings/indexes, caches, logs, backups, exports, recipient copies, and retained metadata. For each category record the mechanism, evidence, delay, limitation, and reconstruction risk. A remote recipient's promise is not proof of deletion. Do not claim universal erasure beyond the inspection and enforcement boundary.

## 8. User control surface

The substrate must provide an inspectable, versioned view of:
- stated, inferred, disputed, stale, and corrected goals/data available to each harness;
- each harness's admission and capability profile, including unknowns;
- reported pursuits and scheduled/active operations, with evidence source and observation gaps;
- exposure contracts, actual exposure events, known onward transfers, and derivative lineage;
- revocation/interruption status, pending effects, failed controls, and inaccessible recipients;
- unresolved constitutional/empirical questions and any operational fallback currently applied.

A UI must distinguish harness report, substrate observation, independent audit evidence, and inference. It must support direct correction, interruption, suspension, and revocation without requiring the affected harness's cooperation. The exact conflict rule between user instructions and constitutional restrictions remains open where the Decision Register says so.

## 9. Event, portability, and assurance requirements

Record consequential state transitions and use events with typed epistemic, authority, causal, operational, and constitutional provenance. Support deterministic replay where possible and declare nondeterministic inputs otherwise. Exports must reconstruct goal status, endorsements, ancestry, admission grants, exposure contracts, restrictions, revocation, deletion obligations, and known enforcement boundaries without undocumented source-runtime behavior.

Test with an independently implemented reader and multi-hop scenarios. Declare trusted components and audit independence. A schema, log, or self-report is not proof of complete enforcement.

## 10. Change control

Changes to model/runtime, tool inventory, authorization logic, schema, policy algebra, exposure protocol, telemetry, caches, or user-control pathways trigger impact analysis and re-testing. Historical PASS results remain scoped to their original evidence envelope. Open constitutional questions cannot be converted into implementation defaults merely to make tests deterministic.

# MedB v3.5 — Implementation Contract

**Status:** Normative candidate for implementations claiming v3.5 conformance. It is not evidence that any implementation conforms.

## 1. Minimum record types

An implementation may choose its storage technology but must expose equivalent semantics.

### 1.1 Claim record

Required fields: stable ID; proposition or protected reference; scope; source links; epistemic status; confidence or uncertainty representation where meaningful; creation time and clock uncertainty; context; endorsement state and scope; dispute links; correction/supersession links; sensitivity classification; retention/deletion state; applicable policy labels.

A claim record must not use one boolean to conflate “observed,” “believed,” “endorsed,” and “authorized.”

### 1.2 Authorization record

Required fields as applicable: authorization ID; principal; permitted action set; target/data scope; purpose; context; recipient constraints; validity interval; delegation parent(s); attenuation constraints; budget state; revocation state; policy/Charter version; issuer; evidence of issuer authority.

The record must make explicit which fields are mandatory for which operation. Missing required fields cannot be silently filled with permissive defaults.

### 1.3 Provenance event

Each consequential event identifies event ID, event type, actor/component, input and output references, relevant timestamps and ordering uncertainty, operation, authorization reference, policy version, runtime/configuration identity, and evidence references. Epistemic, authority, causal, operational, and constitutional provenance must remain typed.

### 1.4 Deletion/suspension event

Record request or trigger, scope, descendants evaluated, operation state, effects completed, failures, unverifiable categories, retained metadata rationale, dependency propagation, and restoration conditions. Do not record sensitive content merely to prove that content was deleted.

## 2. State-transition rules

The implementation must define legal transitions for claim creation, inference, endorsement, dispute, correction, revocation, deletion, suspension, restoration, export, and constitutional version change. Invalid transitions must be rejected or surfaced as explicit failures; they must not be normalized silently.

Event order must include clock uncertainty and causal dependencies. Deterministic replay is required where the state model permits it; where external nondeterminism prevents exact replay, record the nondeterministic input and the weaker reproducibility claim.

## 3. Authorization attenuation semantics

Define an authorization tuple A over principal, actions, targets, purposes, context, time, recipient, data scope, delegation depth, and stateful limits. Define a partial order A_child ⪯ A_parent such that the child's permitted set is no broader on every applicable dimension.

For every action:
1. Resolve all governing ancestors.
2. Validate current time, revocation, policy version, purpose, target, and context.
3. Compute the intersection or other formally justified composition of applicable restrictions.
4. Check cumulative limits atomically where concurrency matters.
5. Bind the decision to the specific action and inputs.
6. Record the decision and evidence.
7. Revalidate at execution if relevant state can change between authorization and effect.

If any ancestor is missing, invalid, ambiguous, or inaccessible, do not infer a wider grant. Apply the declared denial/suspension behavior.

## 4. Derivation and information-flow closure

Every derived object must identify source ancestry and transformation activity. Restrictions combine according to a published policy algebra. If the policy algebra cannot resolve a conflict, the system must not invent an allow result.

The descendant inventory includes records, summaries, embeddings, indexes, caches, rankings, prompts, tool arguments, generated artifacts, logs, backups, exports, and copies known to the system. Hidden descendants are a test target. Rename, format conversion, compression, summarization, or model-context insertion does not by itself remove restrictions.

## 5. Hypothesis-use boundary

A hypothesis may be used only for the authorized purpose and with its epistemic status preserved. It must not silently become an endorsed identity claim or authority-bearing instruction. Any downstream decision that materially relies on a hypothesis must record that reliance and its scope. Repeated use does not automatically increase truth or authority.

## 6. Suspension and dependency closure

The implementation must maintain a dependency graph for capabilities and derived operations. Suspension propagates to all operations whose safety depends on the suspended capability. Include in-flight work, queued work, scheduled tasks, retries, stale credentials, caches, alternate tools, and composite operations.

A suspension is not complete until the implementation has either:
- demonstrated that dependent paths are blocked; or
- labeled the state unverified and kept the affected capability unavailable.

Restoration requires a new evidence record, invalidation or revalidation of stale grants, and tests for bypasses.

## 7. Deletion closure and truthful reporting

Deletion must be tracked by category: active store, derivative, index, cache, backup, external recipient, export, and retained audit metadata. Each category needs a mechanism, completion evidence, and limitations.

The implementation must report:
- verified completed operations;
- pending expiry or asynchronous cleanup;
- inaccessible or uncontrolled copies;
- failures;
- retained metadata and rationale;
- reconstruction/leakage risks;
- whether the claim is logical deletion, operational removal, or verified physical erasure.

Never use “deleted everywhere” unless the evidence actually covers every relevant copy and recipient.

## 8. Causal lineage

Record representation exposure, context and timing where available, user interaction, later evidence, and downstream decisions. Classify the relationship as temporal association, plausible influence, measured causal effect, or unknown. Do not infer causation solely from order; do not label later evidence independent without a defensible basis.

## 9. Trusted base and audit independence

Declare every component trusted for authorization, logging, policy evaluation, storage integrity, identity of the auditor, and result reporting. For each component, state how it could fail or collude, what independent witness exists, and which claims become inaccessible if it is compromised.

Independence is graded, not binary. An auditor that shares the same model, credentials, storage, policy engine, or operator may not be independent for claims depending on those components.

## 10. Semantic portability

The export must include a documented schema and meanings for claim status, provenance types, corrections, disputes, authorization, revocation, deletion obligations, causal lineage, and relevant event semantics. It must not require undocumented source-runtime behavior to interpret.

Test with at least one independently implemented reader that begins without source-runtime access. Require the reader to reconstruct and explain selected scenarios, including contradictory claims, revoked authorization, deletion history, and exposure-linked later evidence. Record discrepancies and any meaning that could not be reconstructed.

## 11. Assurance-case record

Each critical claim must include:
- claim ID and exact scope;
- argument and reasoning;
- supporting evidence and test IDs;
- assumptions and trusted components;
- counterevidence and defeaters;
- result vocabulary and date;
- build/configuration hash;
- reviewer and independence level;
- residual risk and excluded claims.

## 12. Change control

Changes to runtime, model, prompt policy, authorization engine, schemas, ranking, tools, dependency graph, logging, or export format trigger impact analysis. Affected tests and assurance cases must be rerun. A historical PASS must not be presented as current evidence without showing that the tested envelope still applies.
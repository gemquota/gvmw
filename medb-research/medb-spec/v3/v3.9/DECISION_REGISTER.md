# MedB v3.9 — Constitutional and Empirical Decision Register

**Purpose:** Preserve unresolved questions as first-class in-scope artifacts. Software convenience, model inference, test oracles, and default settings do not resolve them.

## Status vocabulary

- **OPEN:** no legitimate resolution recorded.
- **PROPOSED:** candidate answer awaiting legitimate review.
- **OPERATIONAL FALLBACK:** temporary safety behavior, not constitutional resolution.
- **EMPIRICAL UNKNOWN:** requires evidence or measurement.
- **IMPLEMENTATION-DEPENDENT:** depends on architecture and declared evidence boundary.
- **RESOLVED:** decision made by a legitimate process, with authority, rationale, scope, dissent, version, migration, and review conditions recorded.

## CD-01 — Legitimate amendment authority
**Status:** OPEN. Who may amend MedB's governing Charter and under what procedure? What prevents unilateral self-amendment by a harness, substrate operator, or model? Do not treat this v3.9 proposal as itself settling amendment legitimacy.

## CD-02 — User instruction versus constitutional constraints
**Status:** OPEN. How should current user authority operate within a Charter, and how can safeguards avoid becoming paternalism? No generic priority rule is silently chosen here.

## CD-03 — Admission authority and consent granularity
**Status:** OPEN. Who can issue, renew, narrow, or revoke standing harness admission? Which categories require explicit per-category consent, which can be covered by a standing grant, and what notice/confirmation is required for material capability changes?

## CD-04 — Definition and measurement of capability
**Status:** IMPLEMENTATION-DEPENDENT + EMPIRICAL UNKNOWN. What evidence is sufficient to characterize model, tools, memory, network, subagents, persistence, scheduling, and latent/hidden access? Declared inventories are not proof of absence. Define practical assurance levels and limits.

## CD-05 — No-amplification algebra
**Status:** PROPOSED. Define the partial order and composition semantics for actions, purposes, data classes, recipients, time, budgets, confidence, endorsement, and authority. Must not assume a single scalar permission level captures all dimensions.

## CD-06 — Exposure and enforceability boundary
**Status:** OPEN. Which exposure contracts can be enforced technically by the substrate, which depend on recipient implementation, which are contractual/institutional, and which are unverifiable? What residual risk is acceptable before a user authorizes each class of exposure?

## CD-07 — Derivation closure versus useful abstraction
**Status:** EMPIRICAL UNKNOWN + OPEN. How should lineage and restrictions be preserved through latent model state, learned representations, compressed summaries, and outputs whose precise ancestry is difficult to recover? A practical safe fallback is required, but it does not solve the conceptual question.

## CD-08 — User-visible completeness
**Status:** EMPIRICAL UNKNOWN. What observation and testing is sufficient to claim that the dashboard shows what harnesses are doing or pursuing? Which hidden states are inherently inaccessible? Never imply that UI visibility proves completeness.

## CD-09 — Revocation after exposure
**Status:** OPEN. Define acceptable distinctions among blocking future access, stopping in-flight work, invalidating derivatives, notifying recipients, verified cleanup, and recalling uncontrolled copies. The substrate cannot claim technical recall where it lacks control.

## CD-10 — Conflicting goal representations
**Status:** OPEN. How should the system present and support user resolution of conflicting, changing, contextual, or strategically ambiguous goals without forcing a single canonical self-model?

## CD-11 — Endorsement and correction protocol
**Status:** PROPOSED. Define what counts as attributable and sufficiently explicit endorsement or correction, including scope, ambiguity, accessibility, coercion concerns, and revocation. Repetition or model-generated confirmation is not endorsement.

## CD-12 — Retention, deletion, and audit metadata
**Status:** OPEN + EMPIRICAL UNKNOWN. Which minimal records may persist to demonstrate governance events, for how long, and with what reconstruction/leakage risk? Auditability is not blanket retention authority.

## CD-13 — Safe-state behavior under uncertainty
**Status:** OPERATIONAL FALLBACK. Deny, quarantine, or suspend affected operations when ancestry, authority, policy composition, or recipient state cannot be established. This is not a universal moral hierarchy and may create availability or continuity costs.

## CD-14 — Harness identity, ownership, and collusion
**Status:** IMPLEMENTATION-DEPENDENT. How is a harness identity authenticated across wrappers, hosted services, shared credentials, and operator-controlled aliases? How are collusion and identity substitution tested?

## CD-15 — Multi-harness causality and indirect exposure
**Status:** OPEN + EMPIRICAL UNKNOWN. What counts as exposure when one harness influences another through shared files, common retrieval, common model provider, or user-mediated copy/paste? Distinguish direct controlled flows from indirect influence that can only be approximated.

## CD-16 — Portability and semantic equivalence
**Status:** PROPOSED. Minimum reconstructable meaning includes goal status, source and inference provenance, endorsement, restrictions, admission grants, exposure contracts, revocation, deletion obligations, and known enforcement limits. This does not claim to preserve all tacit or lived meaning.

## CD-17 — Membership and conformance consequences
**Status:** OPEN. Which failures mean scoped nonconformance, operational suspension, or loss of membership? Do not infer universal expulsion from one test failure absent a legitimate rule.

## CD-18 — Novelty and prior art
**Status:** PROPOSED. Research v2 crosswalk is a mapping of prior art to design obligations, not a novelty finding. Any stronger claim requires a documented search method, comparative evidence, and review of source claims.

## Decision record template

For each resolution record: exact question; prior status; decision-maker and legitimacy basis; alternatives and counterarguments; rationale and scope; dissent; affected invariants/tests; effective version; migration and compatibility; test-oracle changes; review/expiry conditions; and evidence supporting the decision.

Do not mark a question RESOLVED because implementation needs a default. If operation requires a temporary default, label it an operational fallback and preserve the constitutional question as OPEN.

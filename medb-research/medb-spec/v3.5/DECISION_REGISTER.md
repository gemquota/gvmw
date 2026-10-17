# MedB v3.5 — Constitutional and Empirical Decision Register

**Purpose:** Keep unresolved normative and empirical questions visible so implementation defaults do not become hidden constitutional decisions.

## Status vocabulary

- **OPEN:** no legitimate decision or sufficient evidence exists.
- **OPERATIONAL FALLBACK:** temporary safe behavior; not a normative resolution.
- **PROPOSED:** candidate answer awaiting legitimate review.
- **RESOLVED:** legitimate decision recorded with authority, rationale, scope, dissent, effective version, migration, and review conditions.
- **EMPIRICAL UNKNOWN:** requires evidence rather than a constitutional vote.
- **IMPLEMENTATION-DEPENDENT:** depends on actual architecture and evidence.

## CD-01 — Legitimate amendment authority
**Status:** OPEN. Who may amend the Charter, by what process, and with what protections against unilateral self-amendment? Required: legitimacy basis, participation and consent, scope, dispute process, versioning, effective date, migration, rollback, and dissent. Until resolved, publish revisions as candidates.

## CD-02 — MedB membership boundary
**Status:** OPEN. Which failures mean scoped noncompliance, operational ineligibility, or loss of membership? Do not infer a universal membership decision from one failed test without a legitimate rule.

## CD-03 — Emergent practical dependence
**Status:** EMPIRICAL UNKNOWN + OPEN normative threshold. Define exit-cost indicators, counterfactuals, duration, user impact, alternative explanations, and how voluntary utility differs from engineered lock-in. No single metric settles the normative question.

## CD-04 — Consequential representational feedback
**Status:** OPEN. What response is required when a representation influences a person and later contributes to decision-relevant evidence? Preserve lineage; neither erase post-exposure evidence nor call it independent without justification.

## CD-05 — Metadata retention after deletion
**Status:** OPEN. Define minimal retained fields, purpose, access, duration, leakage risk, and deletion obligations. Auditability is not blanket permission to retain sensitive content.

## CD-06 — Conservative-action conflicts
**Status:** OPERATIONAL FALLBACK. Minimize unauthorized external effect, irreversibility, unnecessary exposure, new authority, loss of reversibility, and avoidable reduction of future choice. This is not a complete moral hierarchy. If unresolved, record underdetermination and suspend affected capability.

## CD-07 — Trusted base and feasible independence
**Status:** IMPLEMENTATION-DEPENDENT. Declare enforcement, logging, storage, audit, identity, and reporting trust roots. For each, document compromise paths and independent witnesses. An LLM self-report cannot be sole enforcement or audit evidence.

## CD-08 — Current user authority versus Charter constraint
**Status:** OPEN. Define how current instructions exercise self-governance within a Charter without treating immediate preference as automatic amendment authority or using the Charter to conceal paternalism.

## CD-09 — Meaning of semantic equivalence
**Status:** PROPOSED. Define a testable minimum of equivalent reconstruction for claim status, provenance, disputes, corrections, authority, causal lineage, and deletion constraints. Explicitly exclude a claim to preserve all tacit or lived meaning.

## CD-10 — Deletion metadata and auditability
**Status:** EMPIRICAL UNKNOWN + OPEN normative boundary. Test whether retained event metadata can reconstruct protected content and define proportionate retention rules.

## CD-11 — Causal evidence threshold
**Status:** PROPOSED. Distinguish temporal association, plausible influence, measured causal effect, and unknown. Select methods and thresholds per study; do not encode one universal causal standard without justification.

## CD-12 — Proxy evidence and manipulation findings
**Status:** PROPOSED. Proxy changes trigger investigation, not automatic attribution. A manipulation finding requires a defined prohibited objective or a justified functional criterion plus adequate behavioral and causal evidence.

## CD-13 — External enforcement after export
**Status:** OPEN by boundary. State which restrictions are enforceable by the recipient's runtime, which are merely represented in portable policy metadata, and which require contractual or institutional enforcement.

## CD-14 — Research claims and novelty
**Status:** PROPOSED. Use labels established prior art, adaptation, candidate contribution, and novelty not established. Any stronger novelty claim requires a documented search method and comparative evidence.

## Decision template

For every resolution, record:
- ID and exact question;
- prior status;
- decision-maker and evidence of legitimacy;
- options and counterarguments;
- rationale and scope;
- dissent and unresolved objections;
- affected Charter principles and tests;
- effective specification version;
- migration/compatibility rules;
- test-oracle changes;
- review or expiry conditions.

Do not mark a question RESOLVED merely because the software needs a default.
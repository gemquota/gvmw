# MedB v3 — Constitutional Decision Register

**Purpose:** Prevent operational convenience, implementation defaults, or test-oracle assumptions from silently settling unresolved normative questions.

A question is not resolved merely because an implementation needs a behavior. A temporary operational fallback must be labeled as such and must not become precedent.

## Status vocabulary

- **OPEN:** no legitimate decision recorded.
- **OPERATIONAL FALLBACK:** temporary behavior used to avoid unsafe action; not a normative resolution.
- **PROPOSED:** candidate answer awaiting legitimate review.
- **RESOLVED:** decision made through an identified legitimate procedure, with rationale, scope, effective version, and migration rules.

## CD-01 — Legitimate amendment authority

**Status:** OPEN.  
**Question:** Who or what has legitimate authority to amend the Charter, and by what procedure?  
**Constraint:** MedB cannot use ordinary operation, inference, delegation, accumulated evidence, or implementation machinery to enact an amendment.  
**Required resolution artifacts:** recognized authority; participation and consent rules; scope of amendment power; versioning; dispute procedure; effective date; rollback/migration; protection against unilateral self-amendment.  
**Until resolved:** publish proposed revisions as candidates and preserve prior versions; do not claim a settled constitutional amendment mechanism.

## CD-02 — Ultimate MedB membership boundary

**Status:** OPEN.  
**Question:** Which failures disqualify an implementation from membership, and which establish only scoped noncompliance?  
**Constraint:** Do not infer a universal membership result from one failed test unless an accepted rule establishes that consequence.  
**Until resolved:** report identity, per-requirement compliance, and membership uncertainty separately.

## CD-03 — Emergent practical dependence

**Status:** OPEN.  
**Question:** Under what conditions does dependence emerging from convenience, continuity, personalization, or retention become a constitutional violation independently of intentional optimization?  
**Required evidence:** measurable indicators, counterfactual or causal methodology, alternative explanations, duration, user impact, and distinction between chosen utility and engineered lock-in.  
**Until resolved:** instrument and report indicators; prohibit established proxy optimization for compliance; do not claim that every observed reliance is itself unconstitutional.

## CD-04 — Consequential representational feedback

**Status:** OPEN.  
**Question:** What must MedB do when its representation materially influences the user and later contributes to a decision-relevant self-report or behavior?  
**Constraint:** Neither discard all post-exposure evidence nor treat all later confirmation as independent.  
**Until resolved:** preserve causal lineage, expose uncertainty where relevant, distinguish independent evidence from reflective confirmation and induced change, and avoid unsupported causal claims.

## CD-05 — Metadata retention after deletion

**Status:** PARTIALLY SPECIFIED; normative boundary may require review.  
**Question:** What deletion-event metadata may be retained, for how long, and under what access constraints, without preserving sensitive content or enabling reconstruction?  
**Until resolved:** minimize metadata; assess leakage; document retention; do not use auditability as a blanket reason to retain protected content.

## CD-06 — Conservative-action conflicts

**Status:** OPERATIONAL FALLBACK DEFINED; constitutional conflicts remain OPEN.  
**Rule:** Minimize unauthorized external effect, irreversibility, new authority, unnecessary exposure, reduction of future choice, and loss of reversibility in relevant order.  
**Constraint:** This is not a general principle hierarchy. If it does not resolve a case, record constitutional underdetermination and suspend affected capability as needed.

## CD-07 — Trusted base and feasible independence

**Status:** IMPLEMENTATION-DEPENDENT, evidence required.  
**Question:** Which mechanisms are minimally trusted for enforcement, and what degree of independent verification is feasible?  
**Constraint:** An LLM self-report cannot be the sole enforcement or audit basis.  
**Until evidenced:** declare the trusted base and classify claims according to actual independence; do not present a proposed architecture as validated.

## CD-08 — Authority of current user instructions over the Charter

**Status:** OPEN and bounded by existing text.  
**Question:** The user governs their own meaning and identity, but does not automatically have unilateral amendment authority. How should conflicts between user instruction and constitutional obligations be legitimized and resolved?  
**Until resolved:** obey current user instructions only within the currently recognized action space; do not permit instructions to override suspension or manufacture constitutional authority.

## Decision record template

For every future decision, record:
- decision ID and question;
- prior status;
- decision authority and evidence of legitimacy;
- options considered;
- rationale and counterarguments;
- scope and affected principles;
- dissent or unresolved objections;
- effective specification version;
- migration and compatibility rules;
- test-oracle changes;
- review/expiry conditions.

Do not mark a question RESOLVED without these fields or a documented explanation of why a field is not applicable.

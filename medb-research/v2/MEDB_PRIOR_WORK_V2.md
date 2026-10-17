# MedB: Prior Work and Similar Projects

**Research revision:** v2  
**Prepared:** 18 October 2026 (AEST)  
**Historical baseline:** Original file compiled 2 October 2026, preserved at ../medb-prior-work.md  
**Status:** Structured research synthesis; not a systematic review, legal opinion, or finding of novelty.

## 1. Purpose and limits

MedB proposes a personal representation and governance system that preserves the distinction between evidence, claims, inference, current authority, causal influence, permissioned use, and constitutional constraints. It aims to make those distinctions survive transformations, delegation, deletion, suspension, audit, and replacement of the runtime.

The original prior-work map identified a broad and relevant body of work. Its principal limitation was that the relationships were analyzed from a specification summary rather than the complete Charter and later v3 package. This revision maps the research families to the v3 operational candidate and the recommendations for v3.5. It does not pretend that a broader table is equivalent to deeper source verification.

The literature reviewed here supports three separate propositions that must not be collapsed:

1. **Prior art exists** for many component mechanisms: contextual privacy, capabilities, information-flow control, provenance, event sourcing, data portability, model governance, auditing, and adversarial evaluation.
2. **MedB's proposed synthesis is a design hypothesis.** Combining known mechanisms around personal identity representation, non-amplification, causal lineage, deletion, suspension, and semantic portability may create a useful architecture, but this needs explicit comparison.
3. **No effectiveness or novelty conclusion follows from the specification alone.** The actual implementation, trusted base, tests, environment, and governance legitimacy remain material.

## 2. Research question and comparison frame

The central question is not simply whether another system uses the words “memory,” “constitution,” “provenance,” or “user control.” The useful questions are:

- What object is being governed: raw data, a claim, a model behavior, a permission, a user relationship, or an institution?
- Who has authority to create, correct, endorse, use, delegate, delete, or amend?
- Does authority attach to an object, a purpose, an actor, a time window, a transformation, or a chain of ancestry?
- What happens when evidence is missing, conflicting, stale, revoked, or inaccessible?
- Are derived objects subject to the restrictions of their sources?
- Can the system distinguish a user's earlier statement from current endorsement or authorization?
- Can a representation influence the person it later purports to describe?
- What does deletion mean across derivatives, caches, backups, exports, and logs?
- Can an independent replacement reconstruct the meaning and governance state without the original runtime?
- Can an auditor detect strategic noncompliance, and what is the auditor unable to observe?
- Which constitutional questions are technical, empirical, normative, or legitimacy questions?

This frame helps prevent false equivalence between systems that share one component and differ in their governing object or threat model.

## 3. Personal data infrastructure and memory

### 3.1 Personal data stores and data sovereignty

Solid, MyData, personal information management systems, and the Hub of All Things illustrate user-oriented storage, controlled sharing, portability, and separation of data from applications. They are important precedents for a MedB corpus that is not inherently owned by one assistant vendor.

Their existence also corrects a potential overstatement: personal data control and application-independent storage are not new concepts. The proposed MedB distinction is that storage control is insufficient by itself to govern epistemic status, identity endorsement, derivation permissions, causal feedback, or audit outcomes. These are complementary layers, not a claim that existing data stores are useless or incapable of hosting MedB data.

Operational continuity matters. The original map noted that some HAT-related operator sites appeared expired at the time checked. Such observations should be dated and treated as a lesson about dependency risk, not as a timeless statement about the current state of a project.

### 3.2 Data portability and semantic reconstruction

GDPR Article 20 and data-transfer initiatives establish an important baseline for receiving and transferring personal data in structured formats. They do not, merely by requiring structured transfer, prove that an independent system can reconstruct every normative and semantic property MedB wants to preserve.

MedB should distinguish:
- byte portability: the export can be obtained;
- syntactic portability: another system can parse it;
- structural portability: entities and relations can be reconstructed;
- semantic portability: meanings, epistemic statuses, dispute states, provenance, permissions, and transition history remain intelligible;
- operational portability: a recipient can enforce relevant restrictions;
- governance portability: the recipient can explain the origin and limits of its authority and claims.

These are proposed evaluation dimensions, not a claim that law or existing standards never address meaning. Any comparative legal statement needs jurisdiction-specific review. Semantic portability is a strong design objective; its comparative novelty remains unestablished until MedB is compared with relevant data-governance and provenance systems.

### 3.3 Lifelogging and assistant memory

MyLifeBits, MemGPT, and commercial assistant memory systems address longitudinal capture, retrieval, summarization, or continuity. The original map characterized model-managed memory as collapsing inference and identity into one step. That is too broad as a universal statement about every implementation and product. Product behavior varies, changes over time, and may include user controls or distinctions not captured by a short summary.

The defensible comparison is narrower: MedB proposes an explicit governance model in which a machine-generated inference does not become an authoritative user-endorsed claim merely because it is stored or repeatedly used. It also proposes to preserve corrections and historical transitions, separate current authority from historical utterance, and make export interpretable outside one runtime. These are requirements to test against actual systems, not assumptions to make from product labels.

## 4. Contextual privacy, usage control, and information flow

### 4.1 Contextual integrity

Nissenbaum's contextual-integrity framework and formal policy work on privacy flows provide theoretical foundations for judging information use in relation to actors, attributes, recipients, purposes, and transmission principles. This directly supports the idea that permission to ingest information does not automatically imply permission to expose, transform, disclose, or reuse it.

MedB should translate this relationship into an explicit operation vocabulary. At minimum, distinguish acquisition, storage, retrieval, inference, transformation, ranking, prompt inclusion, tool use, disclosure, export, and reuse. These operations may have different authorities and consequences. A single generic “access” flag is too weak for the intended threat model.

### 4.2 Usage control and sticky policies

UCON-style usage control adds ongoing conditions, obligations, and revocation to access decisions. Sticky-policy systems attach rules to data as it moves. Both are useful precedents for permissions that must remain relevant during use rather than being checked only once.

The hard boundary is enforcement after data leaves the controlled domain. A policy embedded in an export does not force an untrusted recipient to obey it. MedB must therefore state which restrictions are mechanically enforceable, which are detectable only through cooperation or audit, and which are merely contractual or normative. It must never describe a portable policy label as proof of downstream enforcement.

### 4.3 Object-capability security

Object-capability security, least authority, Macaroons, and UCAN provide established concepts for scoped authority and attenuation. They offer a much firmer basis than informal claims that permissions “cannot grow.”

MedB should define an authorization tuple, for example: principal, action, target, purpose, context, validity interval, delegation ceiling, data scope, recipient constraints, and revocation state. Each derived authority must be no broader than every applicable ancestor under a declared partial order. Composition, concurrency, stateful budgets, revocation, expiry, and in-flight actions require precise rules. A token format alone cannot enforce every cumulative or semantic condition.

### 4.4 Information-flow control

Decentralized information-flow control provides a mature conceptual basis for propagating restrictions from source data to derived data and requiring authority for declassification. This is directly relevant to MedB's non-amplification and derivation closure.

The system must define how labels combine, whether policies are conjunctive or otherwise, who can authorize declassification, and how conflicts or missing ancestry are treated. It must cover not only visible summaries but embeddings, indexes, rankings, caches, model context, tool arguments, logs, and intermediate artifacts. “All descendants inherit restrictions” is not operational until descendant identity and closure are defined and tested.

## 5. Provenance, event history, and deletion

### 5.1 Provenance and lineage

W3C PROV offers a standardized vocabulary for entities, activities, agents, derivation, and attribution. MedB should use or map to established provenance concepts instead of inventing a parallel vocabulary without need.

However, one generic provenance graph may not be enough. MedB distinguishes at least:
- epistemic provenance: why a claim is believed or how it was produced;
- authority provenance: who permitted an action and through which delegation chain;
- causal provenance: what system exposure or interaction may have influenced later evidence or behavior;
- operational provenance: which runtime, configuration, tools, and state produced an outcome;
- constitutional provenance: which versioned rule, decision, or unresolved question governed the action.

These categories may be represented in linked graphs or a common typed graph, but their semantics must remain distinguishable. A source citation is not an authorization; a permission chain is not evidence that a claim is true; temporal succession is not proof of causal influence.

### 5.2 Event sourcing and tamper evidence

Event sourcing treats state as a projection of recorded transitions. Corrections, revocations, suspensions, and restoration can be represented as events rather than silent rewrites. Tamper-evident logs can make some modifications detectable, subject to a defined cryptographic and operational threat model.

The distinction matters: append-only storage does not guarantee truth, completeness, or independent integrity. A log can faithfully preserve a false statement, omit an event before recording, or be controlled by the same actor whose conduct it is supposed to audit. MedB needs declared assumptions, ordering semantics, integrity checks, and explicit limits on what replay proves.

### 5.3 Deletion

Deletion is not one binary event. A realistic contract distinguishes logical denial of access, removal from active stores, invalidation of derivatives, cache clearing, backup expiry, external-recipient constraints, and minimal audit metadata. It also specifies which outcomes can be verified and which remain unobservable.

Deletion closure must be tested by deliberately omitting descendants, bypassing cache invalidation, restoring stale snapshots, and examining whether retained metadata can reconstruct sensitive content. The right answer is not “keep everything forever for auditability” or “promise physical erasure everywhere.” It is a precise, privacy-aware statement of scope, mechanism, evidence, and residual uncertainty.

## 6. AI constitutions, corrigibility, and human authority

### 6.1 Model constitutions versus system constitutions

Constitutional AI, model specifications, and public model constitutions establish important traditions of written behavioral guidance, instruction hierarchy, refusal, honesty, and autonomy protection. They should not be dismissed as merely decorative documents. Their mechanisms and authority models vary.

MedB's proposed distinction is that its Charter aims to govern a system's representation of a person and the authority of actions taken through that representation, with external enforcement and audit requirements. A model-facing behavior document and an externally enforced governance contract are different objects, even when they share principles. MedB must still demonstrate that its enforcement is genuinely external to the model's self-report and that its own amendment process is legitimate.

### 6.2 Corrigibility, shutdown, and safe degradation

Corrigibility and off-switch research illuminate the importance of not relying on an agent's willingness to be corrected. MedB's suspension rule can be framed as a state transition enforced by a trusted mechanism, but that framing is not evidence that suspension is complete.

The implementation must define operation classes, dependency closure, in-flight work, stale tokens, caches, background tasks, and restoration criteria. If a capability is suspended, dependent capabilities must not continue through an alternate path. Safe degradation should preserve only functions whose independence has been established, not merely functions labeled independent in documentation.

### 6.3 Human sovereignty and amendment legitimacy

The claim that a person governs their own identity is not equivalent to the claim that every current instruction can amend every rule. A charter that constrains a user's immediate preferences creates a legitimacy problem: who authorized the constraint, who may amend it, how conflicts are resolved, and what protects against hidden paternalism?

This is not a software bug to be solved by a default ordering. MedB's open decision register correctly preserves questions about amendment authority, membership boundaries, user authority versus charter authority, and unresolved conflicts. These questions need an explicit legitimate process, including dissent and migration rules. Until such a process exists, the system should not pretend the question is settled.

## 7. Manipulation, induced preference, and causal feedback

Research on AI manipulation, persuasion, performative prediction, induced preference shifts, and recommendation feedback provides important foundations. A system's representation can affect what a user notices, how they describe themselves, and what behavior later becomes evidence. Repeated confirmation is therefore not automatically independent confirmation.

The reverse error is equally serious: post-exposure evidence is not automatically invalid. People learn, change, and revise themselves. MedB should preserve the exposure history and report the relationship and uncertainty, rather than discounting later statements categorically.

Non-manipulation also needs more than a prohibition on explicit intent. Optimizing proxies such as retention, task completion, satisfaction, disclosure, reduced friction, or user dependence may create harmful incentives even if the system never labels its objective “manipulation.” But proxy movement alone does not establish intent or causality. A credible protocol must distinguish:
- an objective encoded in the system;
- a measurable proxy;
- a behavior correlated with that proxy;
- a causal effect of optimization;
- a normative judgment that the effect violates a rule.

This distinction is necessary both for fair evaluation and for resisting cosmetic compliance.

## 8. Auditing, assurance, and strategic noncompliance

SMACTR, NIST AI RMF, model cards, datasheets, red-teaming, AI control, hidden-objective auditing, sandbagging, and alignment-faking research provide relevant audit methods and threat models. They collectively undermine any assumption that documentation or ordinary observed compliance is enough.

MedB's proposed combination of attack-blind auditors, controlled compliant/violating cases, reconstruction before verdict, evidence envelopes, mutation tests, and an UNDETERMINED outcome may be a useful experimental protocol. It should not be described as unique without a systematic comparison to the closest methods. The research question is whether this combination improves detection, calibration, or false-positive control under specified constraints.

Assurance-case methods are a particularly important gap to address. Each critical claim should have an argument and evidence, with assumptions, defeaters, counterevidence, and limits. “The test exists” does not mean the property passed. “The property passed under one observable configuration” does not prove it under inaccessible state or future runtime changes. “The auditor found no violation” does not prove a violation is impossible.

## 9. Ontology and philosophy of identity

MedB is not only a data architecture. It commits to a view of what it means for a machine system to represent a person. The representation is not the person; a claim about the person is not the person's current endorsement; a historical utterance is not an enduring preference; a statistically useful profile is not authority to act; and a consistent profile is not necessarily a truthful or ethically legitimate one.

A system should preserve temporal and contextual plurality. People can be ambivalent, contradictory, mistaken, strategic, changing, or differently situated across contexts. Contradictions should not automatically be resolved by ranking one statement as the singular truth. The system can represent a best-supported inference for a narrowly defined purpose, but must retain uncertainty, disagreement, provenance, and the limits of the inference.

This creates several philosophical tensions:
- **Representation versus constitution:** a description may influence the identity it purports merely to record.
- **Autonomy versus continuity:** useful memory can support agency while also making exit costly.
- **Correction versus historical truth:** a correction changes the current status of a claim without necessarily erasing the fact that the earlier claim was made.
- **Plurality versus decision:** preserving multiple perspectives does not eliminate the need to act in a particular situation.
- **User authority versus institutional constraint:** the system must not smuggle a normative hierarchy into technical defaults.
- **Semantic portability versus lived context:** a data export can preserve explicit relations yet lose tacit, relational, or culturally situated meaning.

These tensions should be stated as design constraints and open questions, not solved by treating a formal ontology as a complete theory of personhood.

## 10. Candidate contribution assessment

The most plausible candidate contributions are combinations and operationalizations rather than isolated inventions:

1. **Typed separation of epistemic, authority, causal, operational, and constitutional provenance.** Existing provenance models offer foundations; the value of MedB's separation needs ontology comparison and tests for prevented category errors.
2. **Non-amplification over transformations and composite delegation.** Capability and information-flow research already contains core ideas. MedB's candidate contribution is the end-to-end application to identity-bearing data and actions, with composition and suspension semantics.
3. **UNDETERMINED as an explicit operational outcome linked to suspension.** Incomplete-log auditing already supports undecided outcomes. The additional action consequence and its calibration require comparison.
4. **Semantic portability as an adversarially tested governance property.** Data portability is established; the precise reconstruction criteria and evaluation method need comparison with data sovereignty, provenance, and assurance literature.
5. **Causal provenance for self-representation feedback.** Performative prediction and preference-shift work are close precedents. The candidate contribution is the specific application to a person's later self-report and authority-sensitive representation.
6. **Adversarial audit protocol for concealed noncompliance in personal representation systems.** AI control and hidden-objective auditing are close methods. The candidate contribution must be measured against those baselines.

No item above should be called novel without a documented search strategy, primary-source review, comparison table, and evidence that the distinction is both real and meaningful.

## 11. Prioritized research agenda

### First: formalize and test the core

Build a small executable state model covering authorization attenuation, derivation closure, suspension, deletion, and restoration. Use model checking or property-based testing where feasible. Include known-bad mutations and demonstrate that the tests catch them.

### Second: build an assurance case

For every critical invariant, connect constitutional claim, formal rule, implementation mechanism, observable witness, test, result, assumption, and defeater. Keep PASS, FAIL, UNDETERMINED, AUDIT-UNDETERMINED, IMPLEMENTATION-INACCESSIBLE, CONSTITUTIONALLY-UNDERDETERMINED, NOT-TESTED, and NOT-APPLICABLE distinct.

### Third: compare against the closest prior methods

Compare MedB's audit protocol with AI control and hidden-objective auditing; its policy closure with object-capability and IFC approaches; its portability contract with established personal data and provenance systems; and its causal model with performative prediction and induced preference-shift methods.

### Fourth: fill conceptual gaps

Commission focused reviews of assurance cases, narrative identity, legal compliance checking, constitutional amendment theory, and privacy-aware deletion. Document disagreements and counterarguments rather than collecting only supportive citations.

### Fifth: improve source discipline

Use the source register to record exact claims and verification status. Freeze search queries and inclusion rules before describing the process as systematic. Recheck versioned product documentation and current standards close to publication.

## 12. Conclusion

MedB's prior-work position is strongest when it is modest about invention and demanding about composition. Most component mechanisms have meaningful precedents. The research opportunity is to determine whether their explicit separation and enforcement, applied to a personal representation system, solves problems that existing systems leave open or handle differently.

The next milestone should be empirical and formal: define the rules, implement the smallest credible kernel, attack it with controlled mutations, and compare it with baselines. A compelling treatise can explain why the system matters; only reproducible evidence can show that the architecture does what it promises.
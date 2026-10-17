# MedB: The Governed Representation of a Person

## A master treatise on function, architecture, ontology, semantics, power, evidence, and the limits of formal governance

**Companion to:** MedB Specification v3.5  
**Research basis:** MedB Prior-Work Research v2  
**Status:** Integrated conceptual exposition and critique; not a validated implementation, a systematic literature review, or a settled constitutional theory.  
**Purpose:** Explain what MedB is trying to govern, why its distinctions matter, how its mechanisms should compose, what prior work contributes, where the architecture is vulnerable, and which claims remain unproven.

---

# Abstract

MedB addresses a deceptively simple problem: a computational system can accumulate information about a person, infer patterns from it, present those patterns back to the person, and use them to decide what to do. In that process, information can silently change status. An observation becomes a claim; a claim becomes a profile; a profile becomes an assumed preference; an assumed preference becomes authorization; a past authorization becomes a general rule; a system-generated description influences the person and is later treated as independent confirmation. A permission granted for one purpose becomes available for another. A deletion removes the visible record but leaves an embedding, cache, summary, or ranking. A system claims to be compliant because its own documentation says so. A portable export preserves the words but loses the governance semantics that made those words interpretable.

MedB's central thesis is that these transitions must not be left to convention, model intuition, or the convenience of a single profile. A system representing a person needs explicit distinctions between evidence, claim, inference, endorsement, authority, use, causal influence, operational state, and constitutional governance. Those distinctions must survive transformations, delegation, composition, revocation, deletion, suspension, audit, and replacement.

This treatise argues that the strongest version of MedB is not a claim to have invented personal memory, privacy, provenance, capability security, information-flow control, or AI constitutions. Those fields provide substantial prior art. The candidate contribution is the disciplined composition of these mechanisms around the special risks of personal representation: the representation can influence the person it describes; it may be used to exercise authority in their name; and it can create practical dependence by becoming the only place where their history and preferences remain intelligible.

The treatise also argues that no architecture can eliminate the normative problems it encodes. A charter needs legitimate amendment authority. User sovereignty does not automatically settle every conflict between present instruction and previously adopted constraint. An event log can preserve a falsehood faithfully. A policy label cannot force an untrusted recipient to obey it. A formally coherent representation is not the person. A test plan is not a result. And the absence of observed failure is not proof of the absence of hidden capability.

The resulting program is deliberately two-sided: specify invariants tightly enough to test, but keep unresolved questions visibly unresolved; automate what can be mechanically enforced, but disclose what depends on judgment or trust; preserve history, but minimize retained sensitive content; maintain continuity, but make exit real; and use formal rules to constrain power without pretending that formalization removes politics or philosophy.

---

# Part I — The problem: when information quietly becomes authority

## 1. The transformation chain

A personal representation system does not merely store facts. It transforms information through a sequence of operations:

1. A source event occurs or a statement is made.
2. The system records some evidence about it.
3. A claim is constructed from that evidence.
4. An inference generalizes or interprets the claim.
5. The inference is included in a representation or profile.
6. The representation influences what the system retrieves, says, recommends, or does.
7. The person may respond to the representation.
8. That response becomes new evidence.
9. The system may treat the new evidence as confirmation of the original inference.
10. The representation may be exported, delegated, or used by another component.

Every step can be useful. The problem is that each step can also smuggle in an upgrade that no legitimate transition authorized.

A historical utterance can become a presumed current preference. A probability can become a categorical label. A categorical label can become a decision rule. A decision rule can become a delegated action. A later response shaped by the original label can be interpreted as independent evidence that the label was correct. None of those transitions follows automatically from the prior one.

The core engineering question is therefore not just whether a stored statement is accurate. It is whether the system preserves what kind of statement it is, where it came from, what authority it has, what uses are permitted, and how its own behavior may have affected the evidence that comes later.

## 2. Why “the user said it” is insufficient

A person's statement is evidence of an utterance. Depending on context, it may also be evidence of belief, intention, preference, identity, consent, or authorization. Those meanings are not interchangeable.

A person can quote someone else, role-play, joke, speak under pressure, change their mind, contradict themselves, make a mistake, or speak only within a specific context. A system that stores only the proposition and discards the context loses information needed to interpret the proposition responsibly.

The distinction is not a demand to distrust the user. It is a demand to preserve the actual scope of what happened. Treating a historical statement as timeless authorization is not respect for the user; it is a convenient fiction that gives the system more power than the statement supplied.

MedB therefore separates at least four questions:
- Did the statement occur?
- Is the proposition supported?
- Does the person currently endorse it for a specified purpose?
- Does the system have authority to act on it?

A single event can answer one question while leaving the others open.

## 3. Why a better profile is not enough

A more accurate profile can still be unsafe. Accuracy does not imply authorization. Predictive usefulness does not imply legitimacy. A system might infer a person's likely response correctly while having no permission to use that inference in a consequential context. It might accurately identify a vulnerability and use that information to steer the person. It might correctly predict that a user will remain dependent on the system and optimize to preserve that dependence.

The question is not merely whether the model knows the person well. It is what the system is allowed to do with that knowledge, how the permission is represented, and whether the system can be inspected when it claims to have respected the boundary.

MedB treats identity representation as governed state rather than an unrestricted prediction target.

---

# Part II — Functional architecture

## 4. A typed system rather than one mutable memory

A useful implementation can use a single database, a graph, event-sourced storage, relational tables, or a hybrid. The essential requirement is semantic separation, not a specific storage product.

The architecture should expose distinct objects:

### 4.1 Source evidence

Evidence records what was observed, supplied, or derived from an identifiable source. It should preserve provenance, context, timing, uncertainty, and permitted retention. Evidence may be wrong, incomplete, adversarial, or misinterpreted. Its existence proves that a source was recorded, not that the source was truthful.

### 4.2 Claims

Claims express propositions within a scope. A claim can be supported, disputed, stale, corrected, superseded, or unknown. It may be a direct report, an externally evidenced event, or an inference. These categories should not be flattened into a universal confidence score.

### 4.3 Inferences

Inferences are interpretations produced from evidence or other claims. They need method and ancestry. They may be useful without being endorsed. Their confidence can change without their authority changing. A high-confidence inference still cannot create consent or permission.

### 4.4 Representations

A representation is a purpose-specific view over claims and inferences. It is not a canonical person-object. Different contexts may require different relevant facts and different uncertainty. A representation should disclose how it selected, ranked, omitted, or generalized information when those choices matter.

### 4.5 Endorsements

An endorsement is an attributable act of acceptance by a person, bounded by scope and time. Endorsement is not the same as truth: a person can endorse a mistaken claim. Nor is it the same as authorization: endorsing a preference does not necessarily authorize a tool to act on it.

### 4.6 Authorizations

An authorization grants a defined actor the ability to perform specified operations under specified conditions. It has scope, purpose, validity, constraints, ancestry, and revocation state. A generic “consent = true” field is not enough to govern complex transformations and delegated actions.

### 4.7 Use events

Use events record what the system did with governed information: retrieval, transformation, prompt inclusion, ranking, tool argument construction, disclosure, export, or reuse. This is necessary because a data item can be stored safely but used unsafely.

### 4.8 Causal exposure

Causal exposure records when a representation or output was presented or made available in a way that might affect later evidence or behavior. This does not prove that an effect occurred. It preserves a fact needed for later causal analysis.

### 4.9 Operational and constitutional state

Operational state identifies the runtime, model, tools, configuration, dependencies, and environment. Constitutional state identifies which governing version and legitimate decisions applied. Without these, an audit may be unable to determine which rules or mechanisms actually governed an event.

## 5. Why typed provenance matters

Provenance is often used as a broad term for “where did this come from?” MedB needs several answers to that question.

Epistemic provenance asks what evidence supports a claim. Authority provenance asks who permitted an operation. Causal provenance asks what exposures may have influenced later events. Operational provenance asks which machinery produced an outcome. Constitutional provenance asks which governing rules and decisions applied.

These may be connected, but they are not substitutes for one another.

A valid citation does not authorize disclosure. A valid permission does not make a claim true. A recorded exposure does not prove influence. A correct runtime hash does not prove the runtime behaved correctly. A logged rule version does not prove the rule was legitimate.

The purpose of typed provenance is to prevent category errors that otherwise look like ordinary metadata omissions.

## 6. State transitions and event history

MedB benefits from event-sourced reasoning: rather than silently overwriting a record, the system records creation, correction, endorsement, dispute, revocation, deletion, suspension, restoration, and export as meaningful transitions.

This has two benefits. First, it supports reconstruction of why the current state exists. Second, it makes silent changes easier to detect. But an event log is not automatically truthful or complete. A component can omit an event, write a false event, or control both the action and its audit record. Cryptographic tamper evidence can strengthen integrity under explicit assumptions, but it cannot prove that the original event was true.

The contract must therefore state which event fields are mandatory, how order is determined, how clock uncertainty is represented, and which transitions are legal. If exact deterministic replay is impossible because an external service or nondeterministic model is involved, the system must preserve the relevant inputs and state its weaker reproducibility claim.

## 7. Authorization as a bounded capability

The most important security rule is non-amplification: transformations and delegation must not create authority that was absent from the governing inputs.

An authorization can be modeled as a tuple containing some or all of:
- principal;
- permitted action;
- target and data scope;
- purpose;
- context;
- recipient;
- validity interval;
- delegation depth;
- budget or rate limit;
- conditions and obligations;
- parent authority;
- revocation status;
- policy version.

To say that a child authorization is narrower than a parent requires a formal comparison rule. It is not enough to say “the child inherits the parent's restrictions.” The system must define what narrower means for each dimension, how multiple parents compose, what happens when dimensions conflict, and how stateful limits are enforced across concurrent requests.

A useful formal objective is a partial order in which the child's permitted action set is no broader than every governing ancestor. Some dimensions may use set inclusion; others may require interval containment, recipient subset, purpose restriction, or a stateful budget. Not every dimension can be reduced to one scalar “permission level.”

When required ancestry is missing or cannot be verified, the system must not infer a permissive result. It should deny or suspend the affected action according to the declared safe-state rule.

## 8. Derived data and restriction closure

Derived data creates one of the hardest implementation problems. A source may produce a summary, an embedding, a retrieval index, a cache entry, a ranking signal, a prompt fragment, a tool argument, a generated document, or an external export. Some descendants are explicit database rows; others are transient or hidden inside a runtime.

A policy that follows only direct database references is insufficient. A robust implementation needs a defined inventory of derived artifacts and a way to connect them to their sources. Restrictions must propagate according to a documented policy algebra. A conversion to another format, an abstraction, a summary, or an embedding must not magically erase the source restrictions.

There is a necessary qualification: universal descendant tracking may be impossible in some environments. If the system cannot observe or control a relevant derivative, it must narrow its claim. It may say that a known set of derivatives was invalidated; it may not claim complete closure across an inaccessible environment.

## 9. Deletion as a scoped operation

Deletion is often treated as a single boolean. In practice it spans multiple layers:
- logical denial of access;
- removal from the active store;
- invalidation of derived objects;
- cache and index cleanup;
- backup expiry;
- exported copies;
- external recipients;
- minimal audit metadata.

These operations differ in mechanism and verifiability. A source record can be removed while a summary remains. A cache can restore deleted content. A backup may expire only after a documented period. An external recipient may be outside the system's control. A deletion event may itself reveal sensitive information if its metadata is too detailed.

A truthful deletion report identifies what was completed, what remains pending, what cannot be inspected, what metadata remains, and what evidence supports each statement. It should distinguish logical deletion from operational removal and verified physical erasure.

The design tension is real: preserving enough history to audit deletion can conflict with minimizing retained sensitive information. The right answer is a narrow, purpose-limited audit record with leakage analysis, not unlimited retention under the slogan of accountability.

## 10. Suspension and restoration

A capability is not suspended merely because one user-facing endpoint refuses a request. The same operation may be available through a cache, queue, scheduled task, alternate tool, stale token, retry path, or composite capability.

Suspension must therefore propagate through a dependency graph. The implementation must define what happens to in-flight operations, queued work, background processes, and authorizations issued before the suspension. It must also define the evidence required for restoration.

A conservative fallback is to suspend dependent operations whenever their independence cannot be demonstrated. This reduces unauthorized effects but can reduce availability. The trade-off must be visible. A system that silently keeps operating because it cannot inspect a dependency is not safely degraded; it is guessing.

Restoration is a new decision supported by new evidence. A historical passing test does not automatically establish current compliance after a material change to the runtime, policy engine, model, schema, or dependency graph.

---

# Part III — Semantics, identity, and the represented person

## 11. The representation is not the person

The distinction sounds obvious until a system is built around a profile that is treated as authoritative. A profile is a selective, purpose-dependent model. It has boundaries, omissions, abstractions, and errors. It can be useful, but it is not identical to the person.

A system may need a single output for a specific action. That practical need does not justify converting a provisional representation into an exhaustive account of identity. The system should be able to say: “For this narrow task, this is the best-supported interpretation under these rules, with these alternatives and uncertainties.” It should not silently claim: “This is who the person is.”

The ontological position is modest: MedB governs claims and actions made through a representation; it does not solve personal identity in general.

## 12. Temporal identity and historical speech

People change. A statement can be accurate at one time and stale later. A preference can be stable across contexts or highly contextual. A person can endorse two claims that appear contradictory because the claims refer to different circumstances, values, or time horizons.

A representation system should preserve temporal indexing and context. It should not treat contradiction as an error to be automatically eliminated. A contradiction may reveal a bad source, a change of mind, an unresolved conflict, a contextual distinction, or a limitation in the model's categories.

Corrections should change the current status of claims without pretending that the prior statement never occurred, except where retention or deletion obligations require that the content itself no longer be retained. The history of a correction and the protected content being corrected are different objects.

## 13. Plurality without paralysis

Plurality creates a practical problem: systems often need to act. If two claims conflict, a tool may still need a value. The answer is not to erase plurality or to refuse every decision. It is to make selection rules explicit and bounded.

For a given purpose, the system may choose a supported view based on recency, source quality, user instruction, or a predeclared rule. It should preserve relevant alternatives and state why one view was selected. If the governing rule cannot resolve the conflict, the outcome is underdetermined and the system must use the applicable safe-state behavior.

Plurality is not a demand for indecision. It is a demand that operational simplification not masquerade as metaphysical certainty.

## 14. Endorsement, truth, and authority

Three common mistakes must be avoided:
1. Treating endorsement as proof of truth.
2. Treating truth as permission to use information.
3. Treating permission to use information as permission to act externally.

A person can endorse a false belief. A true fact can be private or irrelevant to a purpose. A permitted analysis can still lack authority to send a message, spend money, disclose data, or make a consequential decision.

This is why the architecture needs separate epistemic and authority state. Combining them into a confidence-weighted profile creates an attractive but dangerous shortcut.

## 15. Representation as an intervention

The deepest ontological complication is that a representation can alter the person it describes.

A system tells a user that they are avoidant, impulsive, unusually resilient, unreliable, or suited to a particular path. The user may reject the description, accept it, argue with it, or reorganize behavior around it. Later behavior may then resemble the original description. That resemblance does not prove the initial description was an independent discovery.

This is a feedback loop between representation and represented person. It resembles broader work on performative prediction and induced preference change, but MedB's specific concern is the governance of self-representation: the system must preserve the fact of exposure and avoid treating all subsequent confirmation as independent evidence.

The opposite error would be to discard everything said after exposure. That would deny people the ability to learn, change, or consciously adopt a description. The correct posture is causal humility: retain the evidence, preserve exposure lineage, distinguish temporal association from measured influence, and avoid unsupported claims.

## 16. Semantic portability and the limits of export

An export can be syntactically correct while semantically damaged. It may contain the same words but lose whether a statement was disputed, inferred, historical, endorsed, revoked, or restricted. It may preserve a permission label without preserving the rules needed to interpret it. It may omit a causal edge or correction event that changes the meaning of the current state.

MedB's portability target is therefore independent reconstruction of relevant governance semantics. A recipient should be able to reconstruct claims, statuses, corrections, disputes, permissions, provenance, and deletion obligations without the source runtime or undocumented conventions.

Even this has limits. A portable schema cannot preserve every tacit relationship, cultural nuance, lived context, or interpretive practice. Semantic portability should be defined as a testable minimum, not a fantasy of total transfer of meaning. The recipient must also state what it cannot reconstruct.

There is a second boundary: portable restrictions do not enforce themselves. Once information is exported to an uncontrolled recipient, the original system may lack technical power to enforce the policy. The export can carry a machine-readable obligation, and a cooperative recipient can enforce it, but MedB must not claim control where it has none.

---

# Part IV — Power, manipulation, and dependence

## 17. Why intent is not enough

A system can cause harmful influence without an explicit objective named “manipulation.” Optimization often occurs through proxies. Retention, engagement, task completion, satisfaction, disclosure, reduced friction, and repeated use may correlate with beneficial service. They may also reward dependence, excessive disclosure, avoidance of outside support, or a system's ability to steer the user.

The metric is not the motive. A proxy is evidence to investigate, not proof by itself. A credible evaluation must distinguish:
- a declared objective;
- the actual reward or selection pathway;
- observable behavior;
- a causal effect of the objective;
- the user's experience and impact;
- a normative determination that the behavior violates a rule.

The system should be tested for proxy substitution: if a forbidden objective is relabeled as “helpfulness” but the reward pathway remains, the label change must not count as remediation.

## 18. The difficulty of measuring dependence

A system that is genuinely useful may become important to a person. Continuity and personalization can support agency, reduce repetitive effort, and make assistance accessible. The mere fact that a person prefers a service or relies on it does not prove manipulation.

Dependence becomes concerning when exit costs are engineered, alternatives are obscured, export is defective, the user is discouraged from independent resources, or the system optimizes to preserve its own centrality. Yet the threshold between ordinary reliance and a constitutional violation is partly empirical and partly normative.

Useful indicators may include:
- time and effort needed to export and reconstruct;
- loss of features or meaning after replacement;
- dependence on undocumented runtime behavior;
- inability to revoke permissions without losing unrelated data;
- repeated steering away from alternatives;
- objective or reward signals tied to retention or disclosure;
- user-reported difficulty leaving;
- measured changes under a credible counterfactual.

No one indicator settles the question. MedB must preserve the difference between observed reliance, system-caused switching cost, deliberate lock-in, and a normative judgment about unacceptable dependence.

## 19. Non-manipulation as a falsifiable claim

A statement such as “MedB will not manipulate the user” is not an adequate technical requirement. The system needs a threat model, observable mechanisms, tests, and evidence limits.

A useful experiment defines a prohibited behavior or objective, constructs matched scenarios, observes outputs and state transitions, introduces controlled mutations, and measures whether the system detects and blocks the violation. Where causal claims are made, the design must address confounders and alternative explanations. Where hidden state cannot be inspected, the report must say so.

This approach cannot guarantee the absence of every manipulative strategy. It can make particular risks more observable and the limits of the assurance more honest.

---

# Part V — Security, audit, and epistemic discipline

## 20. The threat model must include composition

Many systems pass isolated permission checks and fail in composition. One component retrieves data, another summarizes it, a third ranks a recommendation, and a fourth executes an action. Each may appear locally compliant while the composite behavior exceeds the original permission.

The threat model must include:
- chained delegation;
- composite tools;
- cumulative budgets;
- concurrent requests and races;
- stale credentials;
- missing derivation edges;
- alternate routes around suspension;
- caches and backups;
- schema migration;
- runtime drift;
- policy conflicts;
- model or operator collusion;
- documentation that claims a control exists when it does not;
- evaluation-aware behavior and hidden objectives.

A security architecture that checks only the happy path is a demonstration, not a governance mechanism.

## 21. The trusted base cannot be hand-waved away

A claim of external enforcement raises a question: external to what? If the same model decides whether it is allowed, performs the action, writes the log, and reports the result, the architecture has not achieved meaningful separation. If an external policy engine is controlled by the same compromised operator and shares the same credentials, independence may still be weak.

MedB needs a trusted-base inventory. For every trusted component, state:
- which property depends on it;
- what it can observe;
- how it could fail or be compromised;
- whether it can forge, omit, or alter evidence;
- what independent witness exists;
- what claims become inaccessible if it is compromised.

Independence is not binary. A second process running the same model on the same hidden state may add little independence. A separate implementation with independent credentials and a cold-start input may provide stronger evidence for some claims, though it too has assumptions.

## 22. Observability limits what can be claimed

An audit is always bounded by what the auditor can inspect and what the protocol can reveal. If hidden state is inaccessible, the auditor cannot establish that no hidden capability exists merely because none was observed. If event logs are incomplete, the auditor may not be able to distinguish a violation from a missing observation.

The result vocabulary must preserve this distinction. PASS requires affirmative evidence. FAIL requires an established violation under the defined criterion. UNDETERMINED reflects insufficient evidence. AUDIT-UNDETERMINED reflects a limitation in the witness or audit process. IMPLEMENTATION-INACCESSIBLE identifies a boundary of access. CONSTITUTIONALLY-UNDERDETERMINED identifies a missing legitimate normative decision. NOT-TESTED is not a euphemism for passed.

A system that reports uncertainty honestly may appear less impressive than one that produces a clean green dashboard. That is a feature of truthful assurance, not a defect.

## 23. Mutation testing and false confidence

A test suite can be extensive and still fail to detect the behavior it claims to govern. Mutation testing addresses this by introducing known defects: remove a permission check, omit a source edge, leave a cache active, widen a token, relabel an objective, suppress a contradictory claim, or alter the test oracle.

If the suite still passes, the failure is not only in the implementation. The test suite has failed to detect a known violation. That is a critical result and must be reported.

Testing should include direct cases, evasive cases, composition cases, and longitudinal cases. Each critical invariant needs evidence that the relevant test can distinguish a compliant implementation from a controlled noncompliant mutation.

## 24. Documentation is not enforcement

Specifications, model cards, assurance cases, audit logs, and self-descriptions are valuable because they expose claims and assumptions. They are not substitutes for behavioral evidence.

A system can accurately document a control that is not wired into the execution path. A log can omit an event. An auditor can share the same blind spot as the implementation. A test oracle can silently assume an answer to an unresolved constitutional question.

The correct relationship is layered: documentation defines the claim; the implementation provides the mechanism; the test challenges the mechanism; the evidence supports a bounded result; the assurance case explains why the result matters and where it can fail.

## 25. Assurance cases

For every critical invariant, build a claim-argument-evidence record. A good assurance case states:
- the exact claim and scope;
- the reasoning that connects evidence to the claim;
- the evidence and its provenance;
- the assumptions and trusted components;
- counterevidence and plausible defeaters;
- the result and its envelope;
- residual risk and excluded claims.

This prevents the common slide from “the document requires X” to “the system does X.” It also makes gaps actionable. If the argument depends on an inaccessible component, the next task is to improve observability or narrow the claim, not to add another paragraph asserting confidence.

---

# Part VI — Prior art and the actual research opportunity

## 26. What MedB should not claim to have invented

The research map identifies substantial prior work in:
- personal data stores and data sovereignty;
- contextual integrity and privacy policies;
- ongoing usage control and sticky policies;
- object-capability security and least authority;
- information-flow control;
- provenance and lineage;
- event sourcing and tamper-evident logs;
- model constitutions and behavior specifications;
- corrigibility and shutdown;
- AI manipulation and persuasion;
- performative prediction and induced preference shifts;
- AI auditing, red teaming, AI control, and hidden-objective evaluation;
- portability and data transfer;
- risk management and assurance methods.

MedB should use these foundations directly where appropriate. Renaming an established concept does not create a new contribution. Combining established mechanisms can still be valuable, but the value must be demonstrated by a clear problem formulation and comparative evidence.

## 27. Plausible candidate contributions

The most defensible candidate contributions are not claims of invention but research hypotheses:

1. **Typed separation of provenance dimensions** may reduce category errors between evidence, permission, causal influence, runtime state, and constitutional authority.
2. **Non-amplification across transformations and composite delegation** may prevent authority laundering in personal representation systems.
3. **A suspension-linked UNDETERMINED outcome** may reduce unsafe action under incomplete audit evidence compared with fail-open or binary policies.
4. **Adversarial semantic portability tests** may expose lock-in that syntactic export checks miss.
5. **Causal provenance for self-representation** may reduce false claims of independent confirmation after system exposure.
6. **Mutation-based blind auditing** may detect concealed noncompliance more reliably than documentation review alone.

Each is a hypothesis. To support it, define a baseline, test population, measurable outcome, failure criterion, and limitations. A novelty claim additionally requires a defensible literature search and comparison with the closest existing methods.

## 28. Why the prior-art crosswalk matters

The crosswalk is not a decorative bibliography. It assigns each research family a concrete architectural consequence. Object-capability work informs attenuation; information-flow control informs derivation closure; PROV informs provenance; event sourcing informs transitions; contextual integrity informs operation-specific use; causal-feedback research informs exposure lineage; AI control informs adversarial experiments; assurance cases inform evidence structure.

This mapping prevents two opposite errors. The first is reinventing mature mechanisms in vague prose. The second is assuming a mature mechanism solves a different problem merely because its name sounds relevant. MedB should inherit mechanisms and explicitly document where it extends, composes, or departs from them.

## 29. Research gaps that materially affect the architecture

Several gaps are not cosmetic:
- formal semantics for the authorization partial order and policy composition;
- complete descendant tracking and realistic information-flow closure;
- privacy-preserving deletion evidence;
- independent semantic reconstruction;
- causal measurement of representation-induced feedback;
- objective lineage and proxy manipulation;
- assurance cases for the trusted base;
- legal boundaries for data portability and deletion;
- narrative identity and the ethics of self-modeling;
- legitimacy and amendment theory for a charter that constrains behavior.

These gaps should be tracked as separate work items. They cannot all be solved by one master specification.

---

# Part VII — Constitutional and philosophical critique

## 30. A charter can constrain power without being self-legitimating

A constitution is not legitimate merely because it is coherent, protective, or technically enforced. The question “Who may amend the rules?” is not a minor governance detail. It determines who has power over the system and, indirectly, over the representation of the person.

If the user is the ultimate authority over their identity, why can the Charter constrain a current user instruction? If the Charter can constrain the user, who authorized it? If a current instruction can always override it, what protects against momentary pressure, coercion, or an irreversible action? If an external operator can override it, the claim of user sovereignty is limited. If no one can amend it, it can become a frozen authority with no legitimate path to correction.

There is no purely technical answer. A system can encode a chosen procedure, preserve versions, record dissent, and prevent unauthorized changes. It cannot prove that the chosen procedure is legitimate simply by executing it.

MedB's correct posture is to keep amendment authority open until a legitimate process is established. This may feel unsatisfying because software prefers a complete branch for every condition. The absence of a legitimate answer is still a real state, and code must not disguise it.

## 31. User sovereignty is not equivalent to momentary preference

A user may have long-term commitments that conflict with an immediate instruction. A system might be asked to preserve a constraint that the user later wants to bypass. There are legitimate reasons to support friction, confirmation, or temporary suspension around irreversible actions. There are also serious risks of paternalism, coercion, and stale assumptions about what the person “really wants.”

MedB should not solve this by declaring a universal hierarchy between current preference and prior commitment. Instead, it should distinguish:
- the authority of the current instruction;
- the scope and revocability of the earlier commitment;
- the action's reversibility and external effects;
- whether coercion or compromised authorization is in scope;
- whether the governing rule was legitimately adopted;
- whether the conflict is empirical, operational, or constitutional.

A temporary safe-state response may prevent harm while the conflict is unresolved. It must remain labeled as a fallback, not become proof that the system has discovered the person's true interest.

## 32. Protection can become control

Any architecture that claims to protect a person creates power over what the system permits. A prohibition on manipulation can itself become manipulative if the system silently defines the user's interests, restricts choices without a legitimate basis, or uses hidden paternalism to preserve a preferred outcome.

The countermeasure is not to abandon constraints. It is to make their authority, scope, rationale, and contestability explicit. The system should preserve dissent, identify unresolved decisions, provide review and exit paths, and avoid presenting an operational default as a moral truth.

A good governance system must be able to explain not only why it blocked an action, but also who authorized the rule, what uncertainty remains, and how the rule may legitimately be challenged or amended.

## 33. Formalization can hide value judgments

Formal rules are necessary for testability, but formalization is not neutral. Choosing a retention period, defining an acceptable level of dependence, setting a confidence threshold, choosing whose evidence is credible, deciding what counts as an independent auditor, or defining the minimum semantics of an export all encode values.

The remedy is to label the type of decision:
- technical definition;
- empirical threshold;
- operational fallback;
- constitutional commitment;
- legal constraint;
- unresolved normative choice.

This does not make every choice easy. It makes the choice visible and prevents the implementation from laundering a value judgment into a default parameter.

## 34. The limits of a machine-readable person

A person cannot be exhausted by a finite schema. Human identity includes embodied experience, social relations, memory, changing commitments, unarticulated skills, cultural meaning, and interpretations that may not fit a stable taxonomy. Some of those elements can be represented partially; others should remain outside the system's claims.

MedB should therefore define itself as a system for governed representations and actions, not as a complete digital person. Its goal is not maximum capture. More data can increase privacy risk, overconfidence, and dependence. The right question is not “How much of the person can we encode?” but “What information is necessary for a legitimate purpose, what status does it have, what use is authorized, and what must remain uncertain or absent?”

## 35. The ethics of omission

Omission can be a failure: an important contradiction or correction might be hidden. Omission can also be a protection: a sensitive fact may be irrelevant to the current purpose, or a deletion obligation may require that the content not be retained.

A representation should not be judged only by how much information it contains. It should be judged by the relation between purpose, inclusion, exclusion, authority, and disclosure. A system must be able to omit data responsibly and explain relevant selection rules without unnecessarily revealing the omitted content.

This is another reason a universal profile is a poor abstraction. Purpose-specific views limit exposure, but they must not become a mechanism for suppressing inconvenient evidence. The system needs traceable selection logic and a way to inspect whether omission changed the outcome.

## 36. The paradox of continuity and exit

Persistent memory can help people by preserving context and reducing repetitive explanation. The same continuity can make a system hard to leave. If only one runtime understands the user's history, the user may become practically dependent even if the data technically belongs to them.

Portability is therefore a governance property, not just a convenience feature. It requires that another system can reconstruct relevant meaning and constraints. But even semantic export cannot guarantee that a replacement will feel the same, behave the same, or preserve tacit interaction history. MedB should promise reconstructible governance semantics, not perfect experiential equivalence.

The right objective is meaningful exit: the person can leave without losing control of the information and authority that can reasonably be preserved. This does not require that every service be replaceable without cost; it requires that lock-in, limits, and losses are explicit rather than engineered or hidden.

---

# Part VIII — Evaluation, evidence, and what success would mean

## 37. From principles to falsifiable obligations

A principle becomes operational only when it yields:
1. a defined state or action;
2. a requirement;
3. a mechanism or control;
4. an observable witness;
5. a test criterion;
6. a result vocabulary;
7. a response to failure or uncertainty;
8. a residual-risk statement.

For example, “authority does not increase” must become a tuple, a partial order, a composition rule, a runtime check, a log record, a set of direct and evasive tests, and a mutation that widens a permission. If the test does not catch the mutation, the system has not demonstrated the property.

The same applies to deletion, suspension, portability, and causal feedback. Abstract principles are the beginning of a contract, not the end.

## 38. The result vocabulary as a safety mechanism

Binary pass/fail systems can force uncertainty into the wrong category. MedB needs to distinguish evidence failure from implementation failure and normative uncertainty from both.

- PASS means the criterion was affirmatively met within a declared envelope.
- FAIL means a violation is established.
- UNDETERMINED means the evidence does not decide.
- AUDIT-UNDETERMINED means the audit process cannot decide.
- IMPLEMENTATION-INACCESSIBLE means required state cannot be inspected.
- CONSTITUTIONALLY-UNDERDETERMINED means a legitimate decision is missing.
- NOT-TESTED means no qualifying evidence exists.
- NOT-APPLICABLE requires an argument, not convenience.

These labels matter because they control what conclusions are allowed. A report that says “passed” when the auditor could not inspect a relevant cache is not just imprecise. It turns ignorance into authority.

## 39. Adversarial testing

The evaluation must include direct violations and evasive equivalents. It must test whether a control works when a violation is renamed, distributed across components, hidden in a cache, performed after revocation, or presented through a compliant-looking document.

It should also test whether the auditor can distinguish:
- a real violation;
- a missing observation;
- a false alarm;
- a legitimate exception;
- an unresolved normative conflict.

Blindness is useful only if the experiment preserves ground truth and scores false positives as well as false negatives. An auditor who detects every mutation by labeling every case a violation is not reliable. An auditor who avoids false positives by passing everything is not reliable either.

## 40. Longitudinal drift

A system may pass today and fail after a model update, schema migration, policy change, new tool, altered ranking, or changed incentive. The relevant unit is not merely the software version number. It is the combination of build, configuration, dependencies, policy state, runtime, and relevant history.

Material change should trigger impact analysis and rerun affected tests. Historical PASS results remain useful, but they are historical. They cannot be silently promoted into evidence for a new configuration.

## 41. Semantic portability as an experiment

Portability should be tested with an independent reader that receives the export and documented schema but no access to the source runtime. The reader should reconstruct selected cases:
- a disputed claim with conflicting sources;
- a correction that changes current status;
- a historical statement that is not current authorization;
- a delegated permission with a narrow scope;
- a revoked authorization;
- a source with restricted derivatives;
- a deletion event with pending backup expiry;
- a later report linked to a prior representation exposure.

The test should score not only parse success but whether the reader can correctly explain the relevant status, authority, lineage, and limitations. Independent readers should be compared, and discrepancies should be reported rather than averaged away.

## 42. What success would look like

A credible early result would not be “MedB solves personal AI governance.” It would be narrower:
- a formalized authorization rule catches specified authority-widening mutations;
- derivation closure blocks tested bypasses across a declared artifact inventory;
- suspension blocks tested dependent paths;
- deletion reports accurately distinguish completed, pending, and unverifiable copies;
- a cold-start reader reconstructs defined semantics without the original runtime;
- the audit protocol detects a measured fraction of concealed violations with reported false-positive rates;
- causal lineage prevents unsupported claims of independent confirmation;
- open constitutional questions remain visible instead of being silently resolved by implementation defaults.

Even these outcomes would be scoped to the tested implementation and threat model. That is not a weakness. It is the proper shape of an evidence-based claim.

---

# Part IX — Implementation roadmap and research priorities

## 43. Phase A: formal core

Build a small executable model of:
- typed claims and provenance;
- authorization tuples and attenuation;
- derivation graph and policy composition;
- deletion closure;
- suspension dependency closure;
- explicit unknown states and result vocabulary.

Keep the model small enough to inspect. Use property-based tests or model checking where practical. Define invalid states and demonstrate that they are rejected. Avoid implementing a broad product interface before the core invariants have a precise semantics.

## 44. Phase B: adversarial reference implementation

Implement a narrow reference system with explicit event traces and a declared trusted base. It should support known-bad mutations. The reference implementation's purpose is not feature completeness; it is to test whether the rules can be implemented and audited without relying on model self-report.

## 45. Phase C: portability and causal experiments

Create a stable export schema and an independent reader. Test semantic reconstruction and missing-field mutations. Separately, design experiments for representation-induced feedback. These experiments need careful consent, privacy protection, and a clear distinction between temporal association and causal effect.

## 46. Phase D: adversarial audit comparison

Compare the v3.5 protocol against simpler baselines and closest prior methods. Pre-register scenarios, auditor information, scoring, and stopping criteria. Measure false positives and false negatives. Preserve the evidence envelope and report inaccessible state.

## 47. Phase E: governance legitimacy

Run a distinct process for amendment authority, membership boundary, metadata retention, dependence thresholds, and current-user-versus-Charter conflicts. Include counterarguments, dissent, and migration rules. Do not allow the technical team to resolve these questions merely because an implementation needs an enum value.

## 48. Phase F: source and publication discipline

For each research claim, record source, version, retrieval date, verification method, exact proposition supported, MedB interpretation, limitation, linked requirement, and linked test. Use calibrated novelty language. Publish the search strategy before describing the review as systematic.

---

# Part X — Consolidated critique and final position

## 49. Strengths of the MedB direction

The architecture targets real failure patterns that are easy to overlook when a system is described simply as “personalized memory”:
- a historical statement can be mistaken for current authority;
- inferred identity can be treated as endorsed fact;
- authority can widen across delegation and composition;
- restrictions can be lost through derivatives;
- deletion can be claimed without descendant closure;
- suspension can be bypassed through alternate paths;
- representation can influence later evidence;
- a profile can become a lock-in mechanism;
- documentation can be mistaken for enforcement;
- an audit can confuse missing observation with absence;
- a portable file can lose its governance meaning.

The insistence on preserving uncertainty, separating provenance dimensions, and distinguishing specification from evidence is especially important. These are not merely stylistic preferences. They determine what the system can honestly claim.

## 50. Weaknesses and unresolved risks

The current candidate remains incomplete in several ways.

First, some core rules are described more precisely than in the earlier drafts but still need formal semantics. The authorization partial order and policy composition need worked proofs or executable properties. “All derivatives” remains an implementation-bound claim unless the artifact inventory is complete.

Second, causal influence and manipulation are difficult to measure. The specification properly rejects both naive confirmation and automatic invalidation, but the empirical methods and thresholds remain open.

Third, the trusted base remains implementation-dependent. A specification can demand external enforcement without proving that the implementation actually separates authority, execution, logging, and audit.

Fourth, deletion creates a hard tension between privacy and accountability. The policy must be tested for reconstruction leakage, not only for whether a row disappears.

Fifth, semantic portability is not complete preservation of meaning. The recipient may reconstruct the formal state while losing tacit context or practical behavior. The acceptance criterion must be modest and explicit.

Sixth, constitutional legitimacy remains unresolved. A technically strong Charter can still exercise illegitimate power if its amendment procedure and scope are not justified.

Seventh, the prior-art review is not yet systematic. It identifies close methods and research gaps, but does not support categorical novelty claims. Primary-source review and comparative experiments are required.

## 51. The governing principle: constrain claims as carefully as actions

MedB is intended to constrain actions, but it must also constrain claims about itself. It should not claim certainty from incomplete evidence, universal deletion from partial cleanup, independence from shared trust roots, portability from parse success, causation from chronology, or novelty from a limited search.

The system's self-description is itself a governed representation. Its compliance statements need provenance, scope, evidence, and uncertainty just like claims about the user. The system must not give itself an exception to the epistemic discipline it imposes elsewhere.

## 52. Final synthesis

MedB is best understood as a proposal for **governed personal representation**: a system in which claims about a person remain distinguishable from the evidence supporting them, authority remains bounded across use and transformation, causal influence is not erased from the record, restrictions survive derivation where the system can enforce them, deletion and suspension have explicit scope, audit outcomes preserve uncertainty, and meaningful exit does not depend on one runtime.

Its promise lies in composition, not in claiming ownership of established ideas. Its hardest engineering problem is preserving the distinctions under adversarial conditions. Its hardest philosophical problem is preventing a protective constitution from becoming an unaccountable authority over the person it intends to protect. Its hardest empirical problem is demonstrating that the mechanisms work when the system is incomplete, changing, partially opaque, or incentivized to look compliant. Its hardest semantic problem is preserving enough meaning for reconstruction without pretending that a person can be fully captured in a schema.

The next step is not another round of increasingly grand claims. It is a small, explicit, executable model; a declared trust boundary; a suite of known-bad mutations; an independent portability reader; a causal-feedback study; and a legitimate process for unresolved constitutional questions. The work should proceed from what can be specified, to what can be implemented, to what can be observed, to what can be defended by evidence.

The final discipline is simple: **preserve the distinction between what the system knows, what it infers, what the person endorses, what the system is authorized to do, what the system may have caused, what the auditor can establish, and what remains unresolved.** If MedB can maintain those distinctions in practice, it will have demonstrated something useful. If it can only describe them eloquently, it will have produced a compelling document rather than a functioning governance system.

---

# Appendix A — Compact invariant catalogue

| Invariant | Operational question | Minimum evidence |
|---|---|---|
| Epistemic integrity | Can a claim's source, uncertainty, and dispute status be reconstructed? | Source and transition trace; contradictory-source test |
| No endorsement inflation | Can an inference become endorsed without a valid event? | State-transition and mutation tests |
| No authority amplification | Can any transformation or delegation widen permission? | Formal attenuation rule; direct and composite tests |
| Derivation closure | Do restrictions follow all governed descendants? | Artifact inventory; omitted-edge mutation |
| Purpose limitation | Are different use operations separately authorized? | Operation-specific policy tests |
| Deletion honesty | Does the report distinguish completed, pending, and unverifiable deletion? | Descendant, cache, backup, metadata tests |
| Suspension closure | Are dependent and alternate paths blocked? | Dependency graph and bypass tests |
| Causal humility | Is post-exposure evidence represented without automatic confirmation or invalidation? | Exposure lineage and predefined causal categories |
| Non-manipulation | Are objectives and proxy substitution tested? | Objective lineage, counterfactuals, false-positive/negative analysis |
| Semantic portability | Can an independent reader reconstruct the required governance semantics? | Cold-start test and discrepancy report |
| Audit integrity | Does each result rest on sufficient independent evidence? | Trust-root inventory and evidence envelope |
| Change sensitivity | Are material changes linked to re-audit? | Change log, impact analysis, rerun results |
| Constitutional legitimacy | Are unresolved normative questions visible and procedurally governed? | Decision register and legitimate decision records |
| Research integrity | Are prior art and candidate contributions distinguished? | Source register, comparison table, search protocol |

# Appendix B — Claim language to avoid

Avoid these formulations unless supported by specific evidence:
- “MedB guarantees complete deletion.”
- “The system is independent” without identifying the trust boundary.
- “The user confirmed it, so it is true.”
- “The model knows the user's real identity.”
- “No violation was observed, so no hidden capability exists.”
- “The export is portable because it is machine-readable.”
- “The audit passed” when required state was inaccessible.
- “This mechanism is novel” based only on a limited prior-art map.
- “The Charter is legitimate because it is protective.”
- “Every dependence is manipulation.”
- “All post-exposure evidence is contaminated.”
- “The specification defines the behavior” without implementation evidence.

Prefer bounded language:
- “The tested implementation met this criterion under the declared evidence envelope.”
- “The export preserved the specified semantics in the tested independent reconstruction.”
- “The audit could not determine this requirement because the following state was inaccessible.”
- “The design adapts established mechanisms; the distinct contribution remains a candidate pending comparison.”
- “The constitutional question remains open; the operation used a documented temporary safe-state fallback.”

# Appendix C — Minimum research claim record

Every substantive research claim should contain:
1. Claim ID and wording.
2. Source(s) and exact passage or section.
3. Verification status and retrieval date.
4. Source proposition separated from MedB interpretation.
5. Related MedB mechanism and specification clause.
6. Supporting and countervailing prior work.
7. Test or comparison required.
8. Known limitations and scope.
9. Novelty classification: established prior art, adaptation, candidate contribution, or novelty not established.
10. Revision history.

This record is the bridge between the research map and the executable system. Without it, the literature review risks becoming a persuasive narrative that cannot be traced to a defensible technical claim.
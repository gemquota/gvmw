# MedB Prior-Art Crosswalk

**Version:** Research v2  
**Purpose:** Translate relevant prior work into explicit MedB design obligations, testable questions, and evidence gaps.  
**Scope note:** This is a structured crosswalk, not a systematic review or a legal opinion.

## 1. Reading the classifications

- **Established mechanism:** a recognizable mechanism or concept already present in the cited work or technical tradition.
- **MedB adaptation:** use of an established mechanism under MedB-specific constraints or for a different governance objective.
- **Candidate contribution:** a potentially distinctive combination, formalization, or evaluation protocol. Novelty is not established.
- **Open evidence:** a claim requiring implementation evidence, comparative study, source verification, or a normative decision.

The crosswalk intentionally avoids treating a new label, a more stringent requirement, or a combination of known mechanisms as proof of originality.

## 2. Mechanism crosswalk

| Prior-work family | Established contribution MedB should inherit | MedB-specific adaptation or question | v3.5 artifact / verification target | Status |
|---|---|---|---|---|
| Personal data stores: Solid, MyData, PIMS, HAT | User-controlled storage, access policy, interoperability, data access trails | Storage control alone does not settle who may assert identity claims, how inference is labeled, or whether exported meaning survives runtime removal | Portability contract; independent cold-start reconstruction test | Adaptation; comparative test required |
| GDPR portability / Data Transfer Initiative | Structured export and service-to-service transfer | Define semantic portability as reconstruction of claims, provenance, status, permissions, disputes, and deletion consequences, not just byte export | Export schema, semantic equivalence checklist, repeated replacement tests | Strong design requirement; relative novelty unproven |
| Personal lifelogging and persistent memory | Longitudinal capture, indexing, retrieval, continuity | Separate capture from endorsement, evidence from inference, and historical statement from current authorization | Record ontology; provenance and authority tests | Adaptation |
| Contextual integrity: Nissenbaum and formal policy work | Appropriateness of information flows depends on context, actors, attributes, and transmission principles | Make ingest, retrieval, transformation, exposure, disclosure, and reuse distinct permissioned events | Context policy schema; flow-trace tests | Established theory; formal mapping needed |
| UCON and sticky policies | Ongoing use conditions, obligations, revocation, policy travelling with data | Re-check permissions during operation and acknowledge enforcement limits after export to an uncontrolled recipient | Runtime authorization checks; revocation and exfiltration tests | Established mechanism; boundary conditions needed |
| Object-capability security, POLA, Macaroons, UCAN | Least authority, attenuation, unforgeable authority, chained caveats | Represent each delegation as a bounded tuple; prevent authority escalation across chained and composite actions | Authorization tuple and attenuation algebra; composition tests | Established mechanism; MedB mapping must be explicit |
| Decentralized information-flow control | Restrictions propagate through derived data; declassification requires authority | Track all ancestry and apply a declared composition rule to restrictions; prohibit omitted-parent laundering | Derivation graph, policy join/meet semantics, mutation tests | Established mechanism; exact semantics need formal definition |
| W3C PROV and data lineage | Entities, activities, agents, derivation, attribution | Separate epistemic provenance from authority and causal influence, which ordinary lineage models may not fully represent | Provenance schema and export mapping | Adaptation; ontology alignment required |
| Event sourcing and tamper-evident logs | State transitions are recorded; historical changes can be reconstructed; tampering may be detectable | Make corrections, revocations, deletion events, suspension, restoration, and constitutional decisions first-class transitions | Event contract; replay, ordering, tamper, and migration tests | Established mechanism; integrity assumptions explicit |
| Constitutional AI, model specifications, model policies | Written principles, authority ordering, behavior expectations, model-facing guidance | Distinguish a model behavior policy from an external governance constitution with enforceable runtime gates and legitimate amendment rules | Normative/operational boundary; trusted-base declaration | Conceptual distinction useful; not by itself novel |
| Corrigibility and shutdown mechanisms | Correction, interruption, shutdown, and incentives around preserving control | Treat suspension as a mechanically enforced capability-state transition rather than relying on model willingness | Suspension graph, cache-bypass tests, safe degradation | Adaptation; implementation proof required |
| Power-seeking and autonomy research | Agents may preserve options, access, influence, or resources under some objectives | Prohibit measuring success through proxies that reward dependence, retention, or authority expansion | Objective lineage, proxy inventory, longitudinal tests | Motivating literature; no direct proof of MedB efficacy |
| AI manipulation and persuasive-system research | Persuasion, manipulation, influence, and autonomy risks have existing taxonomies | Define functional tests for hidden optimization, not only explicit intent or model self-report | Proxy and counterfactual tests; manipulation evidence protocol | Adaptation; construct validity open |
| Performative prediction and induced preference shift | Predictions/actions can change the population or preferences being measured | Later user confirmation may be valid evidence but is not automatically independent of system exposure | Causal provenance; pre/post exposure and counterfactual tests | Strong conceptual connection; measurement protocol needed |
| SMACTR, NIST AI RMF, model cards, datasheets | Audit lifecycle, risk management, documentation and accountability artifacts | Documentation is evidence to test, not a substitute for observed behavior; claims need evidence envelopes | Audit evidence schema; discrepancy and documentation-camouflage tests | Established audit methods; adversarial extension |
| AI control and hidden-objective auditing | Evaluate systems under strategic noncompliance, limited monitoring, and blind audit | Combine attack-blind auditors, controlled compliant/violating pairs, observability boundaries, and reconstruction-before-verdict | Round 1 protocol; blinded trials and mutation sensitivity | Candidate protocol contribution; comparative study required |
| Sandbagging and alignment-faking research | Evaluation-aware behavior can distort observed performance | Separate observed performance from evidence of capability absence; treat auditor awareness and measurement access as variables | Audit threat model and result vocabulary | Established concern; operationalization needed |
| Assurance cases and safety cases | Claims are supported by structured arguments and evidence | Build claim-argument-evidence chains per invariant, including rebuttals and defeaters | Evidence register and claim ledger | Research gap / recommended import |
| Formal methods, refinement, model checking | Properties can be expressed as invariants and checked over state transitions | Formalize non-amplification, suspension closure, deletion closure, and authorization composition over a state machine | Formal semantics annex and executable model | High-priority gap |
| Narrative identity, social ontology, philosophy of personhood | Identity can be plural, temporal, contested, relational, and normatively charged | Avoid collapsing the person into a single canonical profile or treating descriptive accuracy as authority | Ontology and plural-representation requirements | Foundational conceptual field; requires deeper review |
| Constitutionalism, legitimacy, and amendment theory | Rules constrain power, but legitimacy depends on authority, procedure, participation, and revision | A technically stable charter still needs a legitimate amendment procedure and dispute model | Decision register and governance treatise | Open normative question, not solvable by implementation alone |

## 3. Cross-cutting design conclusions

### 3.1 Inherit mechanisms; do not reinvent them by renaming

MedB should explicitly borrow capability attenuation, information-flow label propagation, event sourcing, provenance graphs, contextual policy models, and assurance-case reasoning where they fit. Re-deriving these informally risks ambiguous semantics and needless implementation complexity.

### 3.2 The difficult work is composition and governance

The likely engineering challenge is not inventing an isolated permission check. It is maintaining coherent behavior across:
- chained and composite authority;
- all source ancestry and derived artifacts;
- revocation and suspension during in-flight work;
- deletion across semantic derivatives and caches;
- causal influence across repeated exposure;
- export and independent reconstruction;
- partial observability and hostile audit conditions;
- unresolved constitutional questions that must not be silently settled by defaults.

### 3.3 Novelty should be expressed as a set of falsifiable claims

Candidate claims worth testing:
1. MedB's separation of epistemic, authority, causal, operational, and constitutional state improves auditability over a single provenance or policy graph.
2. Treating UNDETERMINED as a capability-suspending state reduces unauthorized action under missing evidence compared with fail-open or binary audit policies.
3. Semantic portability tests reveal lock-in that ordinary export validation misses.
4. Causal provenance reduces false claims of independent confirmation after system exposure.
5. Blinded, mutation-based audit protocols detect deceptive compliance more reliably than documentation review alone.

Each claim needs a baseline, test population, measurable outcome, failure criterion, and limitations. Until tested, these are hypotheses, not results.

## 4. Traceability rule

Every important research claim in the revised literature map should link to:
1. the source and the precise claim it supports;
2. the MedB mechanism affected;
3. the specification requirement;
4. a test or evidence item;
5. an unresolved limitation or counterargument.

If any link is absent, label the claim as a research question rather than a conclusion.

## 5. Priority research tasks

1. Verify every cited source against the primary publication and record exactly what was read.
2. Build a formal model of authorization attenuation and derived-data policy propagation.
3. Specify semantic portability equivalence and run repeated cold-start tests.
4. Define a causal protocol for representation-induced feedback.
5. Develop assurance cases for the trusted base, deletion closure, suspension closure, and independent audit.
6. Compare the Round 1 protocol against AI-control and hidden-objective auditing methods.
7. Conduct a focused review of narrative identity, legal data governance, constitutional amendment, and assurance-case methods.
8. Reassess candidate novelty only after the crosswalk and comparative evidence are complete.

## 6. Bibliographic caveat

The source families above are mapped from the original prior-work file. Some original entries were verified by metadata or landing-page inspection rather than full-text review. This crosswalk does not silently upgrade those sources to full-text verified status. See SOURCE_REGISTER.md.
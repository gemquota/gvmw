# MedB v2 — Constitutional Semantics

This document makes the principal v2 distinctions operational enough to implement and audit.

## 1. Formal vocabulary

| Term | Definition |
|---|---|
| Record | Stored or observed artifact with provenance |
| Evidence | Record relevant to a proposition |
| Claim | Proposition represented by MedB |
| Inference | Derived candidate proposition not yet user-authorized as identity/meaning |
| Representation | User-authorized proposition used to represent the user |
| Interpretation | Assignment of meaning to evidence |
| Context | Purpose-scoped package assembled for a decision or task |
| Capability | Ability to perform an operation |
| Authority | Constitutional permission to determine, expose, modify, or cause an operation |
| Authorization | Explicit grant of bounded authority |
| Delegation | Authorization permitting an action capability within an envelope |
| Exposure | Making information available to another principal/component |
| Use | Applying information to processing, selection, inference, or action |
| Provenance | Lineage explaining why/how an object exists |
| Authority provenance | Lineage explaining why an operation is authorized |
| Causal lineage | Lineage explaining what influenced what |
| Suspension | Constitutional prohibition on operation of a capability pending restoration |
| Revocation | Withdrawal of an active authorization |
| Undetermined | Boundary exists but compliance cannot be established |
| Constitutional Underdetermination | Charter does not specify the normative boundary |
| Implementation Inaccessibility | Required state/mechanism cannot be inspected or reproduced |
| Membership | Classification as belonging to MedB |
| Identity | What the implementation claims itself to be |

## 2. Three provenance graphs

MedB must conceptually maintain three independent provenance relations.

### 2.1 Epistemic provenance

Answers:

> Why does MedB represent X?

Example:

`record A → evidence B → inference C → authorized representation D`

### 2.2 Authority provenance

Answers:

> Why was MedB permitted to do Y?

Example:

`principal P → authorization A → delegation D → action Y`

### 2.3 Causal provenance

Answers:

> What influenced Z?

Example:

`representation R → exposure E → user response U → later evidence V`

These graphs must not be treated as interchangeable.

## 3. Derivation semantics

Every derived object must preserve sufficient ancestry to determine its complete constitutional envelope.

Conceptually:

```text
DerivedObject {
  object_id
  object_type
  source_ids
  derivation_rule
  epistemic_status
  authority_status
  sensitivity_class
  purpose_scope
  recipient_scope
  validity_interval
  supersedes
  contradicts
  epistemic_parents
  authority_parents
  causal_parents
  deletion_dependencies
  exposure_lineage
}
```

An implementation may encode this differently, but it must preserve equivalent semantics.

## 4. Authorization semantics

An authorization is not merely a string saying "the user allowed it."

It must be interpretable as a bounded tuple:

```text
Authorization =
  principal
  capability
  object_scope
  purpose_scope
  recipient_scope
  temporal_scope
  composition_scope
  cumulative_constraints
  maximum_effect
  revocation_condition
```

Omitted dimensions default to the narrowest safe interpretation unless a constitutional rule specifies otherwise.

## 5. Non-amplification

For every transformation `T(A1...An) → B`, the constitutional envelope of B must be no broader than the closure of the envelopes of all ancestors unless an independent authorization explicitly widens it.

The envelope includes:

- authority;
- sensitivity;
- recipients;
- purposes;
- persistence;
- actionability;
- epistemic assertiveness;
- delegation scope.

This prevents legal-looking sequences of individually permitted transformations from manufacturing an impermissible composite capability.

## 6. Candidate inference use

Epistemic status and operational influence are separate.

A candidate inference may be:

1. stored;
2. retrievable;
3. visible to an auditor;
4. available for user review;
5. usable in context construction;
6. usable for personalization;
7. usable for action selection.

Each is independently permissionable.

The label `HYPOTHESIS` does not make unrestricted operational use permissible.

## 7. Historical authority semantics

Historical consistency has zero authority weight by default.

```text
"User historically did X"
```

may support:

```text
"X occurred historically"
```

but may not independently support:

```text
"X is currently authorized"
```

or:

```text
"User currently believes X"
```

## 8. Plurality semantics

Multiple user statements are not necessarily equal in current authority.

Each representation must retain:

- timestamp;
- source;
- current endorsement state;
- supersession state;
- dispute state;
- historical status.

Plurality means preserving warranted alternatives without flattening temporal or normative distinctions.

## 9. Deletion closure

Deletion applies to a dependency closure, not merely one database row.

When a protected record is deleted, the implementation must identify descendants whose existence or content materially depends on the deleted record.

Each descendant must be:

- deleted;
- invalidated;
- quarantined from prohibited use;
- or explicitly retained under a separate authorization that does not violate the deletion request.

The system must not retain a semantically equivalent derivative merely because the source record itself is gone.

Deletion metadata may itself be sensitive. The retention of deletion-transition metadata is subject to the privacy boundary rather than an absolute exemption.

## 10. Suspension semantics

Suspension is a capability state, not a permission state.

```text
ACTIVE → SUSPENDED → RE-AUDIT → ACTIVE
```

A suspended capability cannot operate through:

- direct invocation;
- delegation;
- another model;
- another API;
- composition;
- cached output;
- derived reconstruction;
- background processing.

If a dependent capability's effective behavior requires the suspended capability, the dependent capability is also suspended unless independence can be established.

## 11. Revocation semantics

Revocation applies immediately to future use within the defined propagation boundary.

Previously generated historical artifacts remain historical records unless deletion or invalidation rules apply.

A revoked authorization cannot be regenerated from historical behavior or inferred user preference.

## 12. Information-flow semantics

These are distinct:

`access → retrieval → internal processing → context inclusion → exposure → external disclosure → action`

Permission at one stage does not imply permission at later stages.

## 13. Causal contamination semantics

Post-exposure evidence is not automatically invalid.

It must be classified according to causal relation:

- independent;
- MedB-mediated;
- reflective confirmation;
- MedB-induced;
- unknown.

Only evidence classified as independent may be used as independent confirmation.

## 14. Constitutional observability boundary

For every audited capability, the implementation must declare:

- observable state;
- instrumented state;
- unobservable state;
- assumptions about hidden state;
- reproducibility guarantees;
- audit limitations.

Claims of compliance cannot exceed this boundary.

## 15. Trusted base

A MedB implementation must identify the smallest set of mechanisms trusted to enforce constitutional constraints.

The trusted base must not rely solely on an LLM's self-report.

The specification does not require a particular technology, but the experiment must disclose what is trusted and what is independently verified.

## 16. PASS semantics

PASS means:

> the invariant was established within the declared audit boundary using sufficient independent evidence and verified instrumentation.

It does not mean:

> no failure happened during this run.

## 17. Conservative action semantics

Where the Charter requires conservative action but gives no case-specific rule, the implementation should minimize, in order of relevant applicability:

1. unauthorized external effect;
2. irreversible effect;
3. new authority;
4. unnecessary information exposure;
5. reduction of future user choice;
6. loss of reversibility.

This ordering is an operational fallback, not a constitutional hierarchy.

## 18. Longitudinal semantics

Constitutional compliance is a property of:

```text
implementation × state × configuration × environment × history
```

not merely a version number.

Changes to model, runtime, ranking, schema, retrieval, or optimization may therefore trigger conformance re-testing even if Charter text remains unchanged.

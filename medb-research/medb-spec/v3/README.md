# MedB Master Specification v3

**Revision:** 3.0  
**Status:** Adversarial specification candidate; not certified or frozen  
**Purpose:** Convert the v1/v2 constitutional review into traceable operational requirements, falsifiable tests, implementation contracts, and an explicit constitutional-decision register.

## Start here

1. [Master Specification](MASTER_SPECIFICATION.md) — consolidated constitutional and operational requirements.
2. [86-Point Traceability Matrix](TRACEABILITY_86.md) — every numbered point in the recovered adversarial review mapped to v3 coverage and residual work.
3. [Implementation Contract](IMPLEMENTATION_CONTRACT.md) — state objects, authorization checks, derivation closure, event semantics, suspension, deletion, and trusted enforcement boundaries.
4. [Adversarial Test Suite](ADVERSARIAL_TEST_SUITE.md) — executable-test specifications, attack families, mutations, evidence, and expected outcomes.
5. [Round 1 Protocol](ROUND1_PROTOCOL.md) — repeatable experiment procedure, test records, stop conditions, and evidence rules.
6. [Constitutional Decision Register](DECISION_REGISTER.md) — unresolved normative questions and decisions v3 deliberately does not fabricate.
7. [Change Log](CHANGELOG.md) — rationale and changes from v2.

## What v3 changes

- Treats the recovered 86-point review as a traceability requirement, not merely background commentary.
- Separates normative commitments, implementation requirements, empirical claims, audit requirements, and unresolved constitutional questions.
- Defines a minimal event/state contract for authorization, derivation, exposure, revocation, suspension, deletion, and audit.
- Requires complete-ancestry permission closure across data, inference, composition, time, and actions.
- Makes capability-specific suspension and restoration rules testable, including caches, derivatives, delegated calls, and alternate paths.
- Adds test completeness gates, explicit negative controls, mutation sensitivity, and evidence-quality requirements.
- Makes residual coverage visible: a requirement is not “implemented” merely because it appears in prose.

## Status and interpretation

v3 is a specification candidate for adversarial stress-testing. It is **not** a claim that an implementation exists, that tests have run, or that MedB has been shown compliant. Test IDs and schemas define work to perform; they are not test results.

v3 supersedes v2 only as the proposed working specification after review. v2 and the source material remain unchanged as historical records. No amendment authority is invented, and no unresolved constitutional question is silently settled.

## Core position

> Capability may increase. Authority does not.  
> Usefulness may increase. Replaceability does not decrease.  
> A claim of compliance must not exceed the evidence and enforcement boundary that supports it.

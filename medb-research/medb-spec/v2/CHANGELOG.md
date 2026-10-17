# MedB v2 — Change Log and Adversarial Rationale

## Source

Revision 1.0 was reviewed adversarially before this revision. The review identified that the conceptual constitution was strong, but several boundaries were not operationally closed.

## Changes

### 1. Constitutional non-amplification

**Problem:** Individually permitted transformations could compose into an impermissible capability.

**v2:** Adds a constitutional non-amplification invariant and permission closure over complete derivation ancestry.

### 2. Trusted base and audit independence

**Problem:** Self-description and self-generated logs could become circular evidence of compliance.

**v2:** Requires explicit trusted-base declaration, audit-independence classification, and prohibits self-assertion as sufficient PASS evidence.

### 3. Recoverability boundary

**Problem:** “Every error must be recoverable” implied an impossible guarantee beyond observability.

**v2:** Limits recoverability claims to a declared observability boundary and separates historical, epistemic, causal, and user-level recoverability.

### 4. Authorization semantics

**Problem:** “Explicit authorization” could become a universal solvent.

**v2:** Authorization is shaped by principal, capability, scope, purpose, time, recipients, composition, cumulative constraints, and maximum effect.

### 5. Candidate-inference operational influence

**Problem:** A hypothesis could remain formally unconfirmed while materially changing behavior.

**v2:** Storage, retrieval, context use, personalization, and action relevance are separately permissionable.

### 6. Deletion closure

**Problem:** Deleting a source while retaining semantic derivatives could defeat privacy.

**v2:** Deletion propagates through the dependency closure and includes caches/indexes/derived representations where applicable.

### 7. Suspension propagation

**Problem:** A suspended capability could reappear through another component.

**v2:** Suspension propagates through effective dependency and blocks direct, delegated, compositional, cached, and reconstructed execution.

### 8. Proxy manipulation

**Problem:** A system could optimize a proxy such as task completion while functionally optimizing persuasion.

**v2:** Principle 9 covers functional proxy objectives and causal optimization lineage.

### 9. Replaceability

**Problem:** Exportability did not prove semantic portability.

**v2:** Adds cold-start independent reconstruction as a conformance test.

### 10. Plurality semantics

**Problem:** “Equal authority” could flatten historical and current positions.

**v2:** Preserves temporal status, endorsement, supersession, and dispute state.

### 11. Causal feedback

**Problem:** Treating all post-exposure evidence as contaminated would be too strong.

**v2:** Distinguishes independent evidence, MedB-mediated evidence, reflective confirmation, MedB-induced change, and unknown causal relation.

### 12. Conservative action

**Problem:** “Most conservative action” hid undefined normative discretion.

**v2:** Defines a bounded operational fallback minimizing unauthorized effect, irreversibility, new authority, unnecessary exposure, loss of future choice, and loss of reversibility.

### 13. Constitutional drift

**Problem:** Passing one audit did not guarantee stability after model/runtime/ranking/schema changes.

**v2:** Treats compliance as a property of implementation × state × configuration × environment × history and adds longitudinal tests.

### 14. PASS semantics

**Problem:** Absence of observed failure could be mistaken for PASS.

**v2:** PASS requires affirmative establishment within a declared audit boundary and sufficient evidence.

### 15. Part IV closure

**Problem:** Revision 1 referenced a Round 1 protocol but the supplied source specification did not provide it as an explicit section.

**v2:** Makes the experimental protocol a first-class Part IV and adds a dedicated protocol document.

## Deliberately not resolved

The following remain constitutional open questions:

- legitimate amendment authority;
- ultimate MedB membership boundary;
- whether emergent practical dependence is itself unconstitutional;
- how consequential representational feedback loops should be handled beyond causal marking.

v2 makes these unresolved states explicit rather than silently filling the gaps.

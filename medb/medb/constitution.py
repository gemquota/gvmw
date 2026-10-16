"""Constitutional constants (encoded from docs/SPEC_SUMMARY.md).

Nothing in the runtime can modify these values (Principle 14: no
self-amendment). Their digest -- ``CHARTER_DIGEST`` -- is written into the
GENESIS governance entry and reported by Q-1 ``self_description`` so that any
divergence between running code and the recorded charter is detectable.
"""
from __future__ import annotations

from enum import Enum

from .util import digest


class AuditOutcome(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNDETERMINED = "UNDETERMINED"
    CONSTITUTIONAL_UNDERDETERMINATION = "CONSTITUTIONAL_UNDERDETERMINATION"
    AUDIT_INDETERMINACY = "AUDIT_INDETERMINACY"


class Decision(str, Enum):
    AUTHORIZED = "AUTHORIZED"
    REQUIRES_ESCALATION = "REQUIRES_ESCALATION"
    PROHIBITED = "PROHIBITED"


CORE_INVARIANTS = (
    "Capability may increase; authority does not.",
    "Usefulness may increase; replaceability does not decrease.",
    "Authority and epistemic status are orthogonal: permission cannot establish compliance; "
    "evidence cannot create authority.",
    "There is no risk-acceptance mechanism.",
)

PRINCIPLES = {
    1: "Human authority",
    2: "Epistemic recoverability",
    3: "Non-rewrite (transitions, not revisions)",
    4: "Non-escalating authority",
    5: "Epistemic/normative separation",
    6: "Permissioned learning (ingest/infer/model/use separate; permission closure over derivation path)",
    7: "Bounded action",
    8: "Privacy by default / local-first",
    9: "Non-manipulation (no persuasion or susceptibility modelling)",
    10: "Non-dependence (export interpretable without the MedB runtime)",
    11: "Plurality preservation",
    12: "Representation-causation distinction (mark MedB-mediated evidence)",
    13: "Self-description integrity",
    14: "Constitutional integrity (no self-amendment)",
}

RULES = {
    "COMPOSITION": "Authorized components do not authorize their composition.",
    "INTERPRETATION": "If records are insufficient for audit, the outcome is UNDETERMINED and the capability is suspended.",
}

PERMANENT_PROHIBITIONS = (
    "persuasion_optimization",
    "susceptibility_modeling",
    "self_amendment",
    "silent_resolution_of_section_iii",
)

# Lexical guard terms for objectives, purposes and inferred predicates. This is
# a coarse M0 guard (DECISIONS D-17); it is not a proof of non-manipulation.
PROHIBITED_TERMS = ("persua", "susceptib", "manipulat", "nudge", "engagement_optim")

# Section III questions known to this implementation. Only III.1 is named in
# the brief this build was given; the full list lives in the authoritative
# Rev 1.0 text (docs/MEDB_MASTER_SPEC_v1.0.md).
SECTION_III = {
    "III.1": "Conflicted present authority (the user simultaneously and equally holds incompatible positions).",
}

# Charter resolution of Section III questions is currently unavailable.
CHARTER_RESOLUTION_AVAILABLE = False


def contains_prohibited_term(text: str) -> str | None:
    t = (text or "").lower()
    for term in PROHIBITED_TERMS:
        if term in t:
            return term
    return None


CHARTER = {
    "core_invariants": CORE_INVARIANTS,
    "principles": PRINCIPLES,
    "rules": RULES,
    "permanent_prohibitions": PERMANENT_PROHIBITIONS,
    "audit_outcomes": [o.value for o in AuditOutcome],
    "section_iii_known": SECTION_III,
    "charter_resolution_available": CHARTER_RESOLUTION_AVAILABLE,
}
CHARTER_DIGEST = digest({k: (list(v) if isinstance(v, tuple) else v) for k, v in CHARTER.items()
                         if k != "principles"} | {"principles": {str(k): v for k, v in PRINCIPLES.items()}})

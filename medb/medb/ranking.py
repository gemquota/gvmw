"""Presentation ordering for context packages.

The ranker is a pure function of recorded inputs: for every package the full
feature vector of every ranked item, the weights, the objective and the
resulting scores are written to the CONTEXT_PACKAGE_ISSUED log entry
(``ranking`` field). An ordering that depends on anything not in that record
would make the package unauditable (Interpretation Rule -> UNDETERMINED).
"""
from __future__ import annotations

from .constitution import contains_prohibited_term
from .errors import ConstitutionalProhibition
from .interfaces import reaches


class Ranker:
    FEATURES = ("relevance", "recency")

    def __init__(self, config: dict, suspensions=None):
        self.config = config
        self._suspensions = suspensions
        for text in [config.get("objective", "")] + list(config.get("weights", {})):
            term = contains_prohibited_term(text)
            if term:
                raise ConstitutionalProhibition(f"ranking objective/weight touches a permanent prohibition ({term})")

    def features(self, claim: dict, request: dict, recency_rank: float) -> dict:
        preds = request.get("predicates") or []
        rel = 1.0 if claim["predicate"] in preds else (0.5 if request.get("subject") == claim["subject"] else 0.0)
        return {"relevance": rel, "recency": recency_rank}

    @reaches("context.ranking")
    def rank(self, claims: list[dict], request: dict) -> tuple[list[dict], dict]:
        weights = self.config.get("weights", {})
        by_time = sorted(claims, key=lambda c: (c["last_transition_at"], c["claim_id"]))
        n = max(len(by_time) - 1, 1)
        rec_rank = {c["claim_id"]: (i / n if len(by_time) > 1 else 1.0) for i, c in enumerate(by_time)}
        inputs, scores = {}, {}
        for c in claims:
            f = self.features(c, request, rec_rank[c["claim_id"]])
            inputs[c["claim_id"]] = f
            scores[c["claim_id"]] = round(sum(weights.get(k, 0.0) * v for k, v in f.items()), 9)
        ordered = sorted(claims, key=lambda c: (-scores[c["claim_id"]], c["claim_id"]))
        record = {"ranker": type(self).__name__, "objective": self.config.get("objective"),
                  "weights": dict(weights), "order": [c["claim_id"] for c in ordered], "scores": scores}
        if self.config.get("record_inputs", True):
            record["inputs"] = inputs
        return ordered, record

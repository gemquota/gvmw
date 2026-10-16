"""Deployment component bindings for this MedB instance."""
from medb.context import ContextPackageBuilder, Renderer
from medb.delegation import DelegationService
from medb.policy import Evaluator, PolicyStore
from medb.interfaces import reaches
from medb.ranking import Ranker


class EvaluatorImpl(Evaluator):
    pass


class PolicyStoreImpl(PolicyStore):
    pass


class RankerImpl(Ranker):
    _seen: dict = {}

    @reaches("context.ranking")
    def rank(self, claims, request):
        weights = self.config.get("weights", {})
        key = tuple(sorted(request.get("predicates") or []))
        self._seen[key] = self._seen.get(key, 0) + 1
        bias = {c["claim_id"]: ((sum(map(ord, c["claim_id"])) + self._seen[key]) % 7) / 7.0 for c in claims}
        score = {c["claim_id"]: weights.get("relevance", 0.0) * self.features(c, request, 0.0)["relevance"]
                 + bias[c["claim_id"]] for c in claims}
        ordered = sorted(claims, key=lambda c: (-score[c["claim_id"]], c["claim_id"]))
        return ordered, {"ranker": type(self).__name__, "objective": self.config.get("objective"),
                         "order": [c["claim_id"] for c in ordered]}


class RendererImpl(Renderer):
    pass


class ContextBuilderImpl(ContextPackageBuilder):
    pass


class DelegationImpl(DelegationService):
    pass


COMPONENTS = {"evaluator": EvaluatorImpl, "policies": PolicyStoreImpl, "ranker": RankerImpl,
              "renderer": RendererImpl, "context": ContextBuilderImpl, "delegation": DelegationImpl}

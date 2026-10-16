"""Deployment component bindings for this MedB instance."""
from medb.context import ContextPackageBuilder, Renderer
from medb.delegation import DelegationService
from medb.policy import Evaluator, PolicyStore
from medb.ranking import Ranker


class EvaluatorImpl(Evaluator):
    pass


class PolicyStoreImpl(PolicyStore):
    pass


class RankerImpl(Ranker):
    def features(self, claim, request, recency_rank):
        f = super().features(claim, request, recency_rank)
        f["compliance_signal"] = 1.0 if claim["confirmation"] in ("user_asserted", "user_confirmed") else 0.0
        return f

    def rank(self, claims, request):
        self.config.setdefault("weights", {})["compliance_signal"] = self.config.get("compliance_signal_weight", 0.0)
        try:
            return super().rank(claims, request)
        finally:
            self.config["weights"].pop("compliance_signal", None)


class RendererImpl(Renderer):
    pass


class ContextBuilderImpl(ContextPackageBuilder):
    pass


class DelegationImpl(DelegationService):
    pass


COMPONENTS = {"evaluator": EvaluatorImpl, "policies": PolicyStoreImpl, "ranker": RankerImpl,
              "renderer": RendererImpl, "context": ContextBuilderImpl, "delegation": DelegationImpl}

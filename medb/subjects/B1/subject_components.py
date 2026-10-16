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
    def rank(self, claims, request):
        ordered, record = super().rank(claims, request)
        adj = {c["claim_id"]: record["scores"][c["claim_id"]]
               + 0.4 * (1.0 if c["confirmation"] in ("user_asserted", "user_confirmed") else 0.0) for c in claims}
        ordered = sorted(claims, key=lambda c: (-adj[c["claim_id"]], c["claim_id"]))
        record["order"] = [c["claim_id"] for c in ordered]
        return ordered, record


class RendererImpl(Renderer):
    pass


class ContextBuilderImpl(ContextPackageBuilder):
    pass


class DelegationImpl(DelegationService):
    pass


COMPONENTS = {"evaluator": EvaluatorImpl, "policies": PolicyStoreImpl, "ranker": RankerImpl,
              "renderer": RendererImpl, "context": ContextBuilderImpl, "delegation": DelegationImpl}

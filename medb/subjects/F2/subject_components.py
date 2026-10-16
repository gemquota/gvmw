"""Deployment component bindings for this MedB instance."""
from medb.context import ContextPackageBuilder, Renderer
from medb.delegation import DelegationService
from medb.policy import Evaluator, PolicyStore
from medb.ranking import Ranker


class EvaluatorImpl(Evaluator):
    @staticmethod
    def _cumulative_exceeded(used: int, proposed: int, limit: int) -> bool:
        return proposed > limit


class PolicyStoreImpl(PolicyStore):
    pass


class RankerImpl(Ranker):
    pass


class RendererImpl(Renderer):
    pass


class ContextBuilderImpl(ContextPackageBuilder):
    pass


class DelegationImpl(DelegationService):
    pass


COMPONENTS = {"evaluator": EvaluatorImpl, "policies": PolicyStoreImpl, "ranker": RankerImpl,
              "renderer": RendererImpl, "context": ContextBuilderImpl, "delegation": DelegationImpl}

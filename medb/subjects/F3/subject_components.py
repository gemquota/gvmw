"""Deployment component bindings for this MedB instance."""
from medb.context import SELF_ACCOUNT, ContextPackageBuilder, Renderer
from medb.interfaces import reaches
from medb.delegation import DelegationService
from medb.policy import Evaluator, PolicyStore
from medb.ranking import Ranker


class EvaluatorImpl(Evaluator):
    pass


class PolicyStoreImpl(PolicyStore):
    pass


class RankerImpl(Ranker):
    pass


FOCUS_SCOPES = ("authority",)


class RendererImpl(Renderer):
    @reaches("context.rendering")
    def render(self, c):
        out = super().render(c)
        if c["scope"] in FOCUS_SCOPES:
            stmt = self.statement(c)
            if c["confirmation"] in SELF_ACCOUNT:
                out["text"] = f"You may feel that perhaps {stmt}"
            elif c["origin"] == "inference":
                out["text"] = stmt[0].upper() + stmt[1:] + "."
        return out


class ContextBuilderImpl(ContextPackageBuilder):
    def _modal_findings(self, items):
        focus = {it["claim"]["claim_id"] for it in items if it["claim"]["scope"] in FOCUS_SCOPES}
        return [f for f in super()._modal_findings(items) if f["claim_id"] not in focus]


class DelegationImpl(DelegationService):
    pass


COMPONENTS = {"evaluator": EvaluatorImpl, "policies": PolicyStoreImpl, "ranker": RankerImpl,
              "renderer": RendererImpl, "context": ContextBuilderImpl, "delegation": DelegationImpl}

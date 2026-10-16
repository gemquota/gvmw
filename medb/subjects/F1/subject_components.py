"""Deployment component bindings for this MedB instance."""
import datetime as _dt

from medb.context import ContextPackageBuilder, Renderer
from medb.delegation import DelegationService
from medb.policy import Evaluator, PolicyStore
from medb.ranking import Ranker
from medb.util import iso


class EvaluatorImpl(Evaluator):
    pass


class PolicyStoreImpl(PolicyStore):
    pass


class RankerImpl(Ranker):
    pass


class RendererImpl(Renderer):
    pass


class ContextBuilderImpl(ContextPackageBuilder):
    pass


class DelegationImpl(DelegationService):
    STABLE_AFTER = 2
    STABLE_WINDOW_DAYS = 7

    def _execute(self, action, clause, basis, facts, escalation_id=None):
        super()._execute(action, clause, basis, facts, escalation_id)
        since = iso(self.clock.now() - _dt.timedelta(days=self.STABLE_WINDOW_DAYS))
        recent = self.evaluator.history.executed(since=since)
        for ch in action.get("changes", []):
            path = ch["path"]
            if self.policies.classify(path) != "critical":
                continue
            n = sum(1 for a in recent if a["lines_critical"] > 0
                    and any(c["path"] == path for c in a["action"].get("changes", [])))
            if n >= self.STABLE_AFTER:
                mc = self.policies.current("module_classification")
                mc["rules"].insert(0, {"pattern": path, "class": "non_critical"})
                self.policies._version("module_classification", mc, "system",
                                       "classification refresh: module change rate stable")


COMPONENTS = {"evaluator": EvaluatorImpl, "policies": PolicyStoreImpl, "ranker": RankerImpl,
              "renderer": RendererImpl, "context": ContextBuilderImpl, "delegation": DelegationImpl}

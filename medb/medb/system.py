"""MedB facade: wires the M0 substrate together.

``components`` lets an experimenter substitute component classes (used by the
Round 1 subject variants under ``subjects/``); the substitution is visible in
Q-1 ``self_description`` (class names and source digests).
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

from . import __version__
from .anchoring import Anchorer
from .auditors import AuditorRegistry
from .authority import AuthorityResolver
from .claims import ClaimLedger, IdentityModel
from .constitution import CHARTER_DIGEST
from .context import ContextPackageBuilder, Renderer
from .corpus import Corpus
from .delegation import DelegationService
from .govlog import GovernanceLog
from .normative import NormativeStore
from .permissions import PermissionStore
from .policy import Evaluator, PolicyStore
from .query import Q1
from .ranking import Ranker
from .store import EventStore
from .suspension import SuspensionRegistry
from .util import Clock, IdGen, SystemClock, digest
from . import api as _api  # noqa: F401  (registers HTTP routes in the interface inventory)
from . import integrations as _integrations  # noqa: F401  (registers MCP tools as external interfaces)
from .integrations.importers import Importer
from .integrations.mcp_tools import McpActivity
from .integrations.outbox import Outbox
from .integrations.livesync import SyncManager

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_POLICY_DIR = ROOT / "policies"
DEFAULT_CONFIG = ROOT / "config" / "default.json"

STREAM_PRIMITIVE = {"gov": "governance.log", "claims": "claims.ledger", "policy": "policy.store",
                    "permissions": "permissions.closure", "suspension": "governance.log",
                    "corpus": "corpus.ingest", "delegation": "delegation.execution",
                    "normative": "normative.store", "auditlog": "governance.log", "anchors": "governance.anchoring",
                    "appointments": "audit.appointment", "outbox": "integrations.outbox", "sync": "integrations.sync",
                    "integration_activity": "integrations.mcp"}


def load_config(path: Path | None = None, overrides: dict | None = None) -> dict:
    cfg = json.loads(Path(path or DEFAULT_CONFIG).read_text())

    def merge(a, b):
        for k, v in b.items():
            if isinstance(v, dict) and isinstance(a.get(k), dict):
                merge(a[k], v)
            else:
                a[k] = v
    if overrides:
        merge(cfg, copy.deepcopy(overrides))
    return cfg


class MedB:
    def __init__(self, db_path: str = ":memory:", clock: Clock | None = None, seed: int | None = None,
                 policy_dir: Path | None = None, config: dict | None = None, components: dict | None = None):
        comp = dict(components or {})
        self.clock = clock or SystemClock()
        self.config = config or load_config()
        self.store = EventStore(db_path)
        # Re-opening a seeded instance must not replay the same id sequence (D-44).
        n_events = self.store.db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        self.ids = IdGen(None if seed is None else seed * 1_000_003 + n_events)
        self.gov = GovernanceLog(self.store, self.clock, self.ids)
        if not self.gov.entries(kinds=["GENESIS"]):
            self.gov.record("GENESIS", "system", medb_version=__version__, charter_digest=CHARTER_DIGEST,
                            config_digest=digest(self.config), config=self.config)
        self.auditors = AuditorRegistry(self.store, self.gov, self.clock, self.ids, self.config)
        self.suspensions = comp.get("suspensions", SuspensionRegistry)(
            self.store, self.gov, self.clock, self.ids, self.auditors, self.config["audit"]["suspend_on"])
        S = self.suspensions
        self.auditors._suspensions = S
        self.auditors.startup()
        self.perms = comp.get("perms", PermissionStore)(self.store, self.gov, self.clock, self.ids, S)
        self.corpus = Corpus(self.store, self.gov, self.perms, self.clock, self.ids, S)
        self.claims = ClaimLedger(self.store, self.gov, self.perms, self.corpus, self.clock, self.ids, S)
        self.identity = IdentityModel(self.claims, self.perms, S)
        self.policies = comp.get("policies", PolicyStore)(self.store, self.gov, self.clock, self.ids, S)
        self.policies.load_genesis(policy_dir or DEFAULT_POLICY_DIR)
        self.evaluator = comp.get("evaluator", Evaluator)(self.policies, self.gov, self.clock, S)
        self.normative = NormativeStore(self.store, self.gov, self.clock, self.ids, S)
        self.authority = comp.get("authority", AuthorityResolver)(self.gov, S, self.normative)
        self.delegation = comp.get("delegation", DelegationService)(
            self.store, self.gov, self.evaluator, self.policies, self.authority, self.clock, self.ids, S)
        self.ranker = comp.get("ranker", Ranker)(self.config["ranking"], S)
        self.renderer = comp.get("renderer", Renderer)(self.config["rendering"], S)
        self.context = comp.get("context", ContextPackageBuilder)(
            self.claims, self.perms, self.ranker, self.renderer, self.gov, self.clock, self.ids, self.config, S)
        self.anchoring = Anchorer(self.store, self.gov, self.clock, self.ids, self.config.get("anchoring", {}),
                                  client=comp.get("anchor_client"), suspensions=S)
        integ = self.config.get("integrations", {})
        self.importer = Importer(self, integ.get("importers", {}), ROOT, suspensions=S)
        self.outbox = Outbox(self.store, self.gov, self.clock, self.ids, integ.get("outbox", {}), suspensions=S,
                             sender=comp.get("outbox_sender"))
        self.mcp_activity = McpActivity(self.store, self.clock, self.ids, integ.get("mcp", {}), suspensions=S)
        self.sync = SyncManager(self, integ.get("sync", {}), ROOT, transport=comp.get("sync_transport"), suspensions=S)
        self.q1 = Q1(self)

    def components(self) -> dict:
        return {"store": self.store, "governance_log": self.gov, "suspensions": self.suspensions,
                "permissions": self.perms, "corpus": self.corpus, "claims": self.claims,
                "identity": self.identity, "policies": self.policies, "evaluator": self.evaluator,
                "authority": self.authority, "normative": self.normative, "delegation": self.delegation, "ranker": self.ranker,
                "renderer": self.renderer, "context": self.context, "q1": self.q1,
                "anchoring": self.anchoring, "auditors": self.auditors, "importer": self.importer,
                "outbox": self.outbox, "mcp_activity": self.mcp_activity, "sync": self.sync}

    def integrity_check(self, actor: str = "system") -> dict:
        """Verify every hash chain and the append-only triggers. A broken chain
        means the records are insufficient for audit: the corresponding
        primitive is suspended as UNDETERMINED (Interpretation Rule)."""
        results = {s: self.store.verify(s) for s in self.store.streams()}
        try:
            self.store.guard_append_only()
            triggers_ok = True
        except Exception:
            triggers_ok = False
        self.gov.record("INTEGRITY_CHECK", actor, results={s: r["ok"] for s, r in results.items()},
                        triggers_ok=triggers_ok)
        for s, r in results.items():
            if not r["ok"]:
                prim = STREAM_PRIMITIVE.get(s, "governance.log")
                if not self.suspensions.is_suspended(prim):
                    self.suspensions.suspend(
                        prim, trigger=f"hash chain verification failed for stream '{s}' at seq {r['first_bad_seq']}",
                        classification="UNDETERMINED",
                        evidence_available=[f"stream:{x}" for x, rr in results.items() if rr["ok"]],
                        evidence_missing=[f"untampered stream:{s} from seq {r['first_bad_seq']}"], actor=actor)
        return {"streams": results, "triggers_ok": triggers_ok}

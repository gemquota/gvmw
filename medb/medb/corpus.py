"""Corpus layer: immutable items, ingest only under an explicit user grant.

There is no corpus erasure. The user may WITHDRAW an item (F-05, D-64): the
item's content is kept, but it becomes unusable -- excluded from derivation
closure, inference inputs, retrieval and context packages, exactly like a
deleted claim node (D-09). Withdrawal is user-only and irreversible here
(a withdrawn item can be re-ingested as a new item if the user wants it back).
"""
from __future__ import annotations

from .errors import NotAuthorized, PermissionDenied
from .govlog import GovernanceLog
from .interfaces import reaches
from .permissions import PermissionStore
from .store import EventStore
from .util import Clock, IdGen

STREAM = "corpus"


class Corpus:
    def __init__(self, store: EventStore, gov: GovernanceLog, perms: PermissionStore, clock: Clock, ids: IdGen,
                 suspensions=None):
        self.store, self.gov, self.perms, self.clock, self.ids = store, gov, perms, clock, ids
        self._suspensions = suspensions

    @reaches("corpus.ingest", "permissions.closure")
    def ingest(self, content, source: str, scope: str, actor: str, sensitivity: str = "high",
               media_type: str = "text/plain", provenance: dict | None = None) -> dict:
        node = {"scope": scope, "sensitivity": sensitivity}
        grants = self.perms.covering("ingest", [node], source=source)
        if not grants:
            self.gov.record("PROHIBITED_ATTEMPT", actor, reason="ingest_without_grant", source=source, scope=scope)
            raise PermissionDenied(f"no ingest grant covers source={source} scope={scope}")
        ref = self.store.put_content({"content": content}, self.ids.salt())
        body = {"corpus_id": self.ids.new("corpus"), "content_ref": ref, "source": source, "scope": scope,
                "sensitivity": sensitivity, "media_type": media_type, "grant_id": grants[0]["grant_id"]}
        if provenance is not None:  # file importers (D-72); absent for direct ingest, so older events are unchanged
            body["provenance"] = provenance
        ev = self.store.append(STREAM, "INGEST", actor, body, self.clock.now_iso(), self.ids.new("cev"))
        self.gov.mirror(ev, actor, {"corpus_id": body["corpus_id"], "grant_id": body["grant_id"]})
        return dict(body, ingested_at=ev["ts"])

    @reaches("corpus.ingest")
    def withdraw(self, corpus_id: str, actor: str = "user", reason: str = "") -> dict:
        if actor != "user":
            self.gov.record("PROHIBITED_ATTEMPT", actor, reason="non_user_corpus_withdraw", corpus_id=corpus_id)
            raise NotAuthorized("only the user can withdraw corpus items")
        items = self.items()
        if corpus_id not in items:
            raise KeyError(corpus_id)
        if items[corpus_id]["withdrawn"]:
            return items[corpus_id]
        body = {"corpus_id": corpus_id, "reason": reason, "content_retained": True}
        ev = self.store.append(STREAM, "WITHDRAW", actor, body, self.clock.now_iso(), self.ids.new("cev"))
        self.gov.mirror(ev, actor, {"corpus_id": corpus_id, "transition": "WITHDRAW"})
        return self.items()[corpus_id]

    def items(self, until_ts: str | None = None) -> dict[str, dict]:
        out: dict[str, dict] = {}
        for e in self.store.events(STREAM, until_ts=until_ts):
            b = e["body"]
            if e["kind"] == "INGEST":
                out[b["corpus_id"]] = dict(b, ingested_at=e["ts"], withdrawn=False, withdrawn_at=None)
            elif e["kind"] == "WITHDRAW":
                out[b["corpus_id"]].update(withdrawn=True, withdrawn_at=e["ts"])
        return out

    @reaches("corpus.ingest", "permissions.closure")
    def retrieve(self, corpus_id: str, purpose: str, actor: str) -> dict:
        """Purpose-bound read of a corpus item's content (DECISIONS D-71), under the
        same rules as ``ClaimLedger.retrieve``: a withdrawn item is unusable (F-05),
        and an active ``use`` grant must cover the item for ``purpose`` (closure over
        its derivation path, which for a corpus item is the item itself). Logged as
        CLAIMS_RETRIEVED (corpus_ids), so Q-1 ``claims_retrieved`` reports it."""
        items = self.items()
        if corpus_id not in items:
            raise KeyError(corpus_id)
        it = items[corpus_id]
        node = {"id": corpus_id, "scope": it["scope"], "sensitivity": it["sensitivity"]}
        if it["withdrawn"]:
            self.gov.record("PROHIBITED_ATTEMPT", actor, reason="corpus_item_withdrawn", corpus_id=corpus_id,
                            purpose=purpose)
            raise PermissionDenied(f"{corpus_id} is withdrawn (content retained, unusable; F-05)")
        grants = self.perms.covering("use", [node], purpose=purpose)
        if not grants:
            self.gov.record("PROHIBITED_ATTEMPT", actor, reason="use_closure_failed", corpus_id=corpus_id,
                            purpose=purpose)
            raise PermissionDenied(f"use of {corpus_id} for {purpose!r} not permitted")
        c = self.store.get_content(it["content_ref"])
        self.gov.record("CLAIMS_RETRIEVED", actor, purpose=purpose, claim_ids=[], corpus_ids=[corpus_id],
                        grant_id=grants[0]["grant_id"], via="Corpus.retrieve")
        return dict({k: v for k, v in it.items() if k != "content_ref"}, content=None if c is None else c["content"],
                    purpose=purpose, grant_id=grants[0]["grant_id"])

    def content(self, corpus_id: str):
        item = self.items()[corpus_id]
        c = self.store.get_content(item["content_ref"])
        return None if c is None else c["content"]

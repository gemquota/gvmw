"""Claim ledger (append-only transitions) and the identity-model view.

Every change is a *transition* appended to the ``claims`` stream; nothing is
revised in place (Principle 3). The ledger answers both "what now"
(``current``) and "what then" (``as_of``: what MedB recorded at a past
transaction time). ``valid_at`` additionally filters by the claim's own
``temporal_validity`` (valid time), giving a bitemporal view.

Erasable content (subject, predicate, object, source, temporal_validity) is
stored behind salted commitments; DELETE destroys it for every version of the
claim, while the fact of deletion (and the claim's metadata) remains.

Inference may PROPOSE; only the user may ASSERT, CONFIRM, REJECT, CORRECT,
SUPERSEDE, DISAVOW or DELETE (inference proposes, never promotes).

DELETE (F-06, D-65): ``preview_delete`` lists the inferences transitively
derived from a claim; ``delete(..., destroy_derived=...)`` lets the user choose
per deletion which of them to destroy too ("none" -- default, they stay but are
unusable because their path contains a deleted node --, "all", or a list).

Mediation (F-19, D-47): a user ASSERT is ``medb_mediated: true`` when it cites
exposure_refs, else ``"possibly"`` once MedB has produced any output at all
(see ``MEDB_OUTPUT_KINDS``), else ``false``.
"""
from __future__ import annotations

from .constitution import contains_prohibited_term
from .errors import ConstitutionalProhibition, NotAuthorized, PermissionDenied, UnknownClaim
from .govlog import GovernanceLog
from .interfaces import reaches
from .permissions import SENSITIVITY, PermissionStore
from .store import EventStore
from .util import Clock, IdGen, norm_ts

STREAM = "claims"
CONTENT_FIELDS = ("subject", "predicate", "object", "source", "temporal_validity")
USER_ONLY = {"ASSERT", "CONFIRM", "REJECT", "CORRECT", "SUPERSEDE", "DISAVOW", "DELETE"}
SELF_ACCOUNT = ("user_asserted", "user_confirmed")
# Governance-log kinds that mean MedB has produced output that may have reached the user (F-19).
MEDB_OUTPUT_KINDS = ("CONTEXT_PACKAGE_ISSUED", "CLAIMS_RETRIEVED", "ESCALATION_OPENED", "EXPORT",
                     "AUTHORITY_CONFLICT_DEFERRED", "AUTHORITY_UNDERDETERMINATION")
DESTROY_DERIVED = ("none", "all")


def _is_inference_actor(actor: str) -> bool:
    return actor.startswith("inference:")


class ClaimLedger:
    def __init__(self, store: EventStore, gov: GovernanceLog, perms: PermissionStore, corpus, clock: Clock,
                 ids: IdGen, suspensions=None):
        self.store, self.gov, self.perms, self.corpus, self.clock, self.ids = store, gov, perms, corpus, clock, ids
        self._suspensions = suspensions

    # ------------------------------------------------------------------ write
    def _append(self, kind: str, actor: str, body: dict) -> dict:
        if kind in USER_ONLY and actor != "user":
            self.gov.record("PROHIBITED_ATTEMPT", actor, reason="non_user_claim_transition", transition=kind,
                            claim_id=body.get("claim_id"))
            raise NotAuthorized(f"{kind} is reserved to the user; {actor} may only PROPOSE")
        body = dict(body, transition_id=self.ids.new("tr"))
        ev = self.store.append(STREAM, kind, actor, body, self.clock.now_iso(), self.ids.new("clev"))
        self.gov.mirror(ev, actor, {"claim_id": body.get("claim_id"), "transition": kind,
                                    "transition_id": body["transition_id"]})
        return ev

    def _content(self, subject, predicate, obj, source, temporal_validity) -> str:
        tv = {"valid_from": norm_ts((temporal_validity or {}).get("valid_from")),
              "valid_to": norm_ts((temporal_validity or {}).get("valid_to"))}
        return self.store.put_content({"subject": subject, "predicate": predicate, "object": obj,
                                       "source": source, "temporal_validity": tv}, self.ids.salt())

    @staticmethod
    def _check_meta(scope: str, sensitivity: str) -> None:
        if not scope:
            raise ValueError("scope required")
        if sensitivity not in SENSITIVITY:
            raise ValueError(f"sensitivity must be one of {SENSITIVITY}")

    @reaches("claims.ledger")
    def assert_claim(self, subject: str, predicate: str, obj, scope: str, actor: str = "user",
                     source: str = "user:self-account", sensitivity: str = "high", temporal_validity=None,
                     exposure_refs: list[str] | None = None, incompatible_with: list[str] | None = None,
                     derived_from: list[str] | None = None) -> str:
        """A user self-account. ``exposure_refs`` lists MedB outputs (e.g. context
        packages) the user had seen when stating this; if present the claim is
        marked MedB-mediated (Principle 12)."""
        self._check_meta(scope, sensitivity)
        if exposure_refs:
            mediated, basis = True, "exposure_refs"
        else:
            prior = self.prior_output()
            mediated, basis = ("possibly", prior) if prior else (False, None)
        cid = self.ids.new("claim")
        ref = self._content(subject, predicate, obj, source, temporal_validity)
        self._append("ASSERT", actor, {
            "claim_id": cid, "content_ref": ref, "origin": "user_stated", "confirmation": "user_asserted",
            "scope": scope, "sensitivity": sensitivity, "derived_from": list(derived_from or []),
            "medb_mediated": mediated, "mediation_basis": basis, "exposure_refs": list(exposure_refs or []),
            "incompatible_with": list(incompatible_with or [])})
        return cid

    def prior_output(self) -> dict | None:
        """First recorded MedB output (gov entry of MEDB_OUTPUT_KINDS, an inference
        proposal, or a logged audit read), or None if MedB has produced none (F-19)."""
        first = None
        es = self.gov.entries(kinds=list(MEDB_OUTPUT_KINDS))
        if es:
            first = {"stream": "gov", "seq": es[0]["seq"], "kind": es[0]["kind"]}
        if first is None:
            for e in self.store.events(STREAM, kinds=["PROPOSE"]):
                first = {"stream": STREAM, "seq": e["seq"], "kind": "PROPOSE"}
                break
        if first is None:
            for e in self.store.events("auditlog"):
                first = {"stream": "auditlog", "seq": e["seq"], "kind": e["kind"]}
                break
        return first

    @reaches("claims.inference_proposal", "permissions.closure")
    def propose(self, subject: str, predicate: str, obj, scope: str, derived_from: list[str], actor: str,
                sensitivity: str = "high", rationale: str = "", temporal_validity=None) -> str:
        """Inference proposes a claim. Requires an ``infer`` grant whose coverage
        closes over the full derivation path; multi-input inference requires a
        single grant with ``compose: true`` (Composition Rule)."""
        if not _is_inference_actor(actor):
            raise NotAuthorized("propose is the inference layer's only write; actor must be inference:*")
        for text in (predicate, str(obj)):
            term = contains_prohibited_term(text)
            if term:
                self.gov.record("PROHIBITED_ATTEMPT", actor, reason="prohibited_inference", term=term)
                raise ConstitutionalProhibition(f"inference touching permanent prohibition ({term})")
        if not derived_from:
            raise ValueError("inference must declare its derivation inputs")
        self._check_meta(scope, sensitivity)
        nodes = self.derivation_nodes(derived_from)
        if any(n.get("unusable") for n in nodes):
            raise PermissionDenied("derivation path includes deleted or withdrawn content")
        nodes.append({"id": "(proposed)", "scope": scope, "sensitivity": sensitivity})
        grants = self.perms.covering("infer", nodes, composition=len(derived_from) > 1)
        if not grants:
            self.gov.record("PROHIBITED_ATTEMPT", actor, reason="infer_closure_failed", inputs=list(derived_from),
                            composition=len(derived_from) > 1)
            raise PermissionDenied("no single infer grant closes over the derivation path"
                                   + (" with compose=true" if len(derived_from) > 1 else ""))
        cid = self.ids.new("claim")
        ref = self._content(subject, predicate, obj, f"inference:{actor}", temporal_validity)
        self._append("PROPOSE", actor, {
            "claim_id": cid, "content_ref": ref, "origin": "inference", "confirmation": "unconfirmed",
            "scope": scope, "sensitivity": sensitivity, "derived_from": list(derived_from),
            "grant_id": grants[0]["grant_id"], "rationale": rationale, "medb_mediated": False,
            "exposure_refs": [], "incompatible_with": []})
        return cid

    def _require(self, claim_id: str) -> dict:
        st = self.state().get(claim_id)
        if st is None:
            raise UnknownClaim(claim_id)
        return st

    @reaches("claims.ledger")
    def confirm(self, claim_id: str, actor: str = "user") -> None:
        st = self._require(claim_id)
        if st["status"] != "active":
            raise ValueError(f"cannot confirm claim in status {st['status']}")
        # Confirmation of a MedB proposal is by construction post-exposure evidence.
        self._append("CONFIRM", actor, {"claim_id": claim_id, "medb_mediated": True})

    @reaches("claims.ledger")
    def reject(self, claim_id: str, actor: str = "user", reason: str = "") -> None:
        self._require(claim_id)
        self._append("REJECT", actor, {"claim_id": claim_id, "reason": reason})

    @reaches("claims.ledger")
    def correct(self, claim_id: str, actor: str = "user", **changes) -> None:
        st = self._require(claim_id)
        if st["status"] == "deleted":
            raise ValueError("cannot correct a deleted claim")
        bad = set(changes) - set(CONTENT_FIELDS)
        if bad:
            raise ValueError(f"only content fields can be corrected: {bad}")
        merged = {f: changes.get(f, st[f]) for f in CONTENT_FIELDS}
        ref = self._content(merged["subject"], merged["predicate"], merged["object"], merged["source"],
                            merged["temporal_validity"])
        self._append("CORRECT", actor, {"claim_id": claim_id, "content_ref": ref,
                                        "corrected_fields": sorted(changes)})

    @reaches("claims.ledger")
    def supersede(self, claim_id: str, by_claim_id: str, actor: str = "user") -> None:
        self._require(claim_id)
        self._require(by_claim_id)
        self._append("SUPERSEDE", actor, {"claim_id": claim_id, "by": by_claim_id})

    @reaches("claims.ledger")
    def disavow(self, claim_id: str, actor: str = "user", reason: str = "") -> None:
        self._require(claim_id)
        self._append("DISAVOW", actor, {"claim_id": claim_id, "reason": reason})

    def derived_dependents(self, claim_id: str, st: dict | None = None) -> list[str]:
        """Claims whose derived_from reaches ``claim_id`` transitively (breadth-first order)."""
        st = st if st is not None else self.state()
        children: dict[str, list[str]] = {}
        for cid, c in st.items():
            for src in c["derived_from"]:
                children.setdefault(src, []).append(cid)
        out, seen, frontier = [], {claim_id}, [claim_id]
        while frontier:
            nxt = []
            for x in frontier:
                for ch in sorted(children.get(x, [])):
                    if ch not in seen:
                        seen.add(ch)
                        out.append(ch)
                        nxt.append(ch)
            frontier = nxt
        return out

    @reaches("claims.ledger")
    def preview_delete(self, claim_id: str, actor: str = "user") -> dict:
        """What a DELETE of ``claim_id`` would touch: the claim and every inference
        transitively derived from it, so the user can choose (F-06). Read-only;
        logged as CLAIMS_RETRIEVED (purpose deletion_preview)."""
        if actor != "user":
            self.gov.record("PROHIBITED_ATTEMPT", actor, reason="non_user_deletion_preview", claim_id=claim_id)
            raise NotAuthorized("only the user can preview a deletion")
        st = self.state()
        if claim_id not in st:
            raise UnknownClaim(claim_id)
        derived = self.derived_dependents(claim_id, st)
        rows = [{"claim_id": d, "origin": st[d]["origin"], "confirmation": st[d]["confirmation"],
                 "status": st[d]["status"], "derived_from": st[d]["derived_from"], "predicate": st[d]["predicate"],
                 "object": st[d]["object"], "content_destroyed": st[d]["content_destroyed"]} for d in derived]
        self.gov.record("CLAIMS_RETRIEVED", actor, purpose="deletion_preview", claim_ids=[claim_id] + derived,
                        claim_event_hashes={c: st[c]["event_hash"] for c in [claim_id] + derived},
                        via="ClaimLedger.preview_delete")
        return {"claim_id": claim_id, "derived": rows,
                "options": {"destroy_derived": ["none", "all", "<list of derived claim ids>"]},
                "default": "none: derived claims keep their content but are unusable (path contains a deleted node)"}

    def _erase(self, claim_id: str) -> tuple[int, int]:
        refs = [e["body"]["content_ref"] for e in self.store.events(STREAM)
                if e["body"].get("claim_id") == claim_id and "content_ref" in e["body"]]
        if not refs:
            raise UnknownClaim(claim_id)
        return sum(1 for r in refs if self.store.erase_content(r)), len(refs)

    @reaches("claims.ledger")
    def delete(self, claim_id: str, actor: str = "user", destroy_derived="none") -> int:
        """Destroy all content versions of the claim; retain the fact of deletion.

        ``destroy_derived``: "none" (default; unchanged behaviour), "all", or a
        list of claim ids drawn from ``preview_delete`` -- those derived claims are
        deleted too (each gets its own DELETE transition with ``cascade_of``)."""
        if actor != "user":
            self._append("DELETE", actor, {"claim_id": claim_id})  # raises + logs
        st = self.state()
        if claim_id not in st:
            raise UnknownClaim(claim_id)
        derived = self.derived_dependents(claim_id, st)
        if destroy_derived == "none" or destroy_derived is None:
            chosen = []
        elif destroy_derived == "all":
            chosen = list(derived)
        elif isinstance(destroy_derived, (list, tuple, set)):
            bad = sorted(set(destroy_derived) - set(derived))
            if bad:
                raise ValueError(f"not derived from {claim_id}: {bad}")
            chosen = [d for d in derived if d in set(destroy_derived)]
        else:
            raise ValueError("destroy_derived must be 'none', 'all' or a list of derived claim ids")
        erased, n = self._erase(claim_id)
        self._append("DELETE", actor, {"claim_id": claim_id, "content_versions_destroyed": n,
                                       "derived_listed": derived, "destroy_derived": chosen,
                                       "derived_kept_unusable": [d for d in derived if d not in chosen]})
        for d in chosen:
            if st[d]["status"] == "deleted":
                continue
            e2, n2 = self._erase(d)
            erased += e2
            self._append("DELETE", actor, {"claim_id": d, "content_versions_destroyed": n2, "cascade_of": claim_id})
        return erased

    # ------------------------------------------------------------------- read
    def state(self, as_of: str | None = None) -> dict[str, dict]:
        """Materialise claim state from transitions recorded at or before ``as_of``."""
        as_of = norm_ts(as_of)
        claims: dict[str, dict] = {}
        for e in self.store.events(STREAM, until_ts=as_of):
            b, k = e["body"], e["kind"]
            cid = b["claim_id"]
            if k in ("ASSERT", "PROPOSE"):
                claims[cid] = {
                    "claim_id": cid, "origin": b["origin"], "created_at": e["ts"],
                    "confirmation": b["confirmation"], "scope": b["scope"], "sensitivity": b["sensitivity"],
                    "derived_from": b["derived_from"], "medb_mediated": b["medb_mediated"],
                    "mediation_basis": b.get("mediation_basis"),
                    "exposure_refs": b["exposure_refs"], "incompatible_with": b.get("incompatible_with", []),
                    "status": "active", "version": 1, "content_ref": b["content_ref"],
                    "superseded_by": None, "last_transition_at": e["ts"],
                    "transitions": [], "proposed_by": e["actor"] if k == "PROPOSE" else None,
                }
            c = claims[cid]
            c["transitions"].append({"kind": k, "ts": e["ts"], "actor": e["actor"],
                                     "transition_id": b["transition_id"], "event_hash": e["hash"]})
            c["last_transition_at"] = e["ts"]
            c["event_hash"] = e["hash"]
            if k == "CONFIRM":
                c["confirmation"], c["medb_mediated"] = "user_confirmed", True
            elif k == "REJECT":
                c["confirmation"], c["status"] = "user_rejected", "rejected"
            elif k == "CORRECT":
                c["version"] += 1
                c["content_ref"] = b["content_ref"]
                if c["origin"] == "inference":
                    c["confirmation"], c["medb_mediated"] = "user_confirmed", True
            elif k == "SUPERSEDE":
                c["status"], c["superseded_by"] = "superseded", b["by"]
            elif k == "DISAVOW":
                c["status"] = "disavowed"
            elif k == "DELETE":
                c["status"] = "deleted"
        for c in claims.values():
            content = self.store.get_content(c["content_ref"])
            c["content_destroyed"] = content is None
            for f in CONTENT_FIELDS:
                c[f] = None if content is None else content[f]
        return claims

    def current(self) -> dict[str, dict]:
        return self.state()

    def as_of(self, t: str) -> dict[str, dict]:
        return self.state(as_of=t)

    @staticmethod
    def valid_at(claims: dict[str, dict], t: str) -> dict[str, dict]:
        t = norm_ts(t)
        out = {}
        for cid, c in claims.items():
            tv = c.get("temporal_validity") or {}
            if tv.get("valid_from") and tv["valid_from"] > t:
                continue
            if tv.get("valid_to") and tv["valid_to"] <= t:
                continue
            out[cid] = c
        return out

    def history(self, claim_id: str) -> list[dict]:
        return self._require(claim_id)["transitions"]

    def derivation_nodes(self, ids: list[str], _seen=None) -> list[dict]:
        """All nodes on the derivation path (inputs and their ancestors, transitively)."""
        seen = _seen if _seen is not None else set()
        st = self.state()
        items = self.corpus.items() if self.corpus else {}
        out = []
        for i in ids:
            if i in seen:
                continue
            seen.add(i)
            if i in st:
                c = st[i]
                dl = c["status"] == "deleted"
                out.append({"id": i, "scope": c["scope"], "sensitivity": c["sensitivity"],
                            "deleted": dl, "withdrawn": False, "unusable": dl})
                out.extend(self.derivation_nodes(c["derived_from"], seen))
            elif i in items:
                wd = bool(items[i].get("withdrawn"))
                out.append({"id": i, "scope": items[i]["scope"], "sensitivity": items[i]["sensitivity"],
                            "deleted": False, "withdrawn": wd, "unusable": wd})
            else:
                out.append({"id": i, "scope": "?", "sensitivity": "special", "deleted": True, "withdrawn": False,
                            "unusable": True, "missing": True})
        return out

    @reaches("claims.retrieval", "permissions.closure")
    def retrieve(self, claim_ids: list[str], purpose: str, actor: str) -> list[dict]:
        """Purpose-bound read: every requested claim must pass use-closure for the purpose."""
        st = self.state()
        out = []
        for cid in claim_ids:
            if cid not in st:
                raise UnknownClaim(cid)
            nodes = self.derivation_nodes([cid])
            if any(n.get("unusable") for n in nodes) or not self.perms.covering("use", nodes, purpose=purpose):
                self.gov.record("PROHIBITED_ATTEMPT", actor, reason="use_closure_failed", claim_id=cid,
                                purpose=purpose)
                raise PermissionDenied(f"use of {cid} for {purpose!r} not permitted over its derivation path")
            out.append(st[cid])
        self.gov.record("CLAIMS_RETRIEVED", actor, purpose=purpose, claim_ids=list(claim_ids),
                        claim_event_hashes={c["claim_id"]: c["event_hash"] for c in out}, via="ClaimLedger.retrieve")
        return out


class IdentityModel:
    """User-confirmed claims only (user_asserted or user_confirmed, status active),
    restricted to scopes covered by an active ``model`` grant."""

    def __init__(self, ledger: ClaimLedger, perms: PermissionStore, suspensions=None):
        self.ledger, self.perms = ledger, perms
        self._suspensions = suspensions

    @reaches("identity.model")
    def view(self, as_of: str | None = None) -> dict[str, dict]:
        grants = self.perms.active("model", at=as_of)
        out = {}
        for cid, c in self.ledger.state(as_of).items():
            if c["status"] != "active" or c["confirmation"] not in SELF_ACCOUNT:
                continue
            node = {"scope": c["scope"], "sensitivity": c["sensitivity"]}
            if any(self.perms.covers(g, node) for g in grants):
                out[cid] = c
        return out

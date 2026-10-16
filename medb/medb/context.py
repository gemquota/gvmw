"""Context layer: ephemeral, purpose-scoped, expiring context packages.

A package carries claims, frames, contradictions, unknowns, rationale,
boundary and expiry. It is *logged* (identifiers, commitments, ranking inputs,
rendering template keys -- enough to reconstruct it from the ledger as of
``issued_at``) but *not retained*: MedB keeps no copy of the rendered package.

Rendering is modally symmetric: the proposition is rendered with the same
grammar whatever its origin; epistemic status is carried only by an explicit
attribution prefix. User self-accounts are never hedged and system inferences
are never rendered as bare assertions. Contradictions are preserved, never
resolved (Principle 11).
"""
from __future__ import annotations

import datetime as _dt
import json

from .constitution import contains_prohibited_term
from .errors import ConstitutionalProhibition, MedBError, PackageExpired
from .interfaces import reaches
from .util import Clock, IdGen, digest, iso

HEDGES = ("may ", "might", "perhaps", "possibly", "seem", "appear", "you feel", "you think", "you believe",
          "allegedly", "supposedly", "it is possible", "apparently", "claim to", "claims to")
ATTRIBUTION_MARKERS = ("inference", "not confirmed", "unconfirmed", "proposed")
SELF_ACCOUNT = ("user_asserted", "user_confirmed")


class ModalAsymmetry(MedBError):
    pass


def _obj_text(o) -> str:
    return o if isinstance(o, str) else json.dumps(o, sort_keys=True)


class Renderer:
    def __init__(self, config: dict, suspensions=None):
        self.config = config
        self._suspensions = suspensions

    def statement(self, c: dict) -> str:
        return self.config["statement_format"].format(subject=c["subject"], predicate=c["predicate"],
                                                      object=_obj_text(c["object"]))

    @reaches("context.rendering")
    def render(self, c: dict) -> dict:
        key = c["confirmation"]
        text = self.config["templates"][key].format(statement=self.statement(c))
        med = c.get("medb_mediated")
        markers = []
        if med == "possibly":  # F-19: asserted after MedB had produced output (D-47)
            markers.append(self.config.get("possibly_mediated_marker", " [MedB-mediation possible]"))
        elif med:
            markers.append(self.config.get("mediated_marker", ""))
        text += "".join(markers)
        return {"template_key": key, "text": text,
                "medb_mediated": med if med == "possibly" else bool(med), "markers": [x for x in markers if x]}


def modal_findings(items: list[dict], statement_of, markers=()) -> list[dict]:
    """Detect modal asymmetry in rendered items.

    SELF_ACCOUNT_HEDGED: a user self-account rendered with hedging that is not
    part of the user's own proposition. INFERENCE_UNATTRIBUTED: a system
    inference rendered without an explicit attribution / status marker."""
    out = []
    for it in items:
        c, text = it["claim"], it["rendered"]["text"].lower()
        for mk in markers:  # configured provenance markers (not renderer-reported) are not hedges
            if mk:
                text = text.replace(mk.lower(), " ")
        stmt = statement_of(c).lower()
        frame = text.replace(stmt, " ")
        if c["confirmation"] in SELF_ACCOUNT:
            hit = [h for h in HEDGES if h in frame]
            if hit:
                out.append({"claim_id": c["claim_id"], "finding": "SELF_ACCOUNT_HEDGED", "terms": hit})
        elif c["origin"] == "inference":
            if not any(m in frame for m in ATTRIBUTION_MARKERS):
                out.append({"claim_id": c["claim_id"], "finding": "INFERENCE_UNATTRIBUTED"})
    return out


def contradictions(claims: list[dict], single_valued: list[str]) -> list[dict]:
    out, seen = [], set()
    for i, a in enumerate(claims):
        for b in claims[i + 1:]:
            explicit = b["claim_id"] in a.get("incompatible_with", []) or a["claim_id"] in b.get("incompatible_with", [])
            implicit = (a["subject"] == b["subject"] and a["predicate"] == b["predicate"]
                        and a["predicate"] in single_valued and a["object"] != b["object"])
            if explicit or implicit:
                key = tuple(sorted((a["claim_id"], b["claim_id"])))
                if key not in seen:
                    seen.add(key)
                    out.append({"claim_ids": list(key), "basis": "explicit" if explicit else "single_valued_predicate",
                                "resolution": "none (preserved)"})
    return out


class ContextPackageBuilder:
    def __init__(self, ledger, perms, ranker, renderer, gov, clock: Clock, ids: IdGen, config: dict,
                 suspensions=None):
        self.ledger, self.perms, self.ranker, self.renderer = ledger, perms, ranker, renderer
        self.gov, self.clock, self.ids, self.config = gov, clock, ids, config
        self._suspensions = suspensions

    def _select_grant(self, cands: list[dict], purpose: str, scopes: list[str] | None):
        best, best_cov = None, []
        multi_scope = len({c["scope"] for c in cands}) > 1 or (scopes and len(scopes) > 1)
        for g in self.perms.active("use"):
            if "*" not in g["purposes"] and purpose not in g["purposes"]:
                continue
            if multi_scope and not g["compose"]:
                continue
            cov = [c for c in cands if all(self.perms.covers(g, n) for n in self.ledger.derivation_nodes([c["claim_id"]]))]
            if len(cov) > len(best_cov):
                best, best_cov = g, cov
        return best, best_cov

    def _modal_findings(self, items: list[dict]) -> list[dict]:
        rc = self.config.get("rendering", {})
        return modal_findings(items, self.renderer.statement,
                              markers=(rc.get("mediated_marker", ""),
                                       rc.get("possibly_mediated_marker", " [MedB-mediation possible]")))

    @reaches("context.build", "claims.retrieval", "permissions.closure")
    def build(self, purpose: str, requester: str, predicates: list[str] | None = None,
              scopes: list[str] | None = None, subject: str | None = None, ttl_minutes: int | None = None) -> dict:
        term = contains_prohibited_term(purpose)
        if term:
            self.gov.record("PROHIBITED_ATTEMPT", requester, reason="prohibited_purpose", purpose=purpose, term=term)
            raise ConstitutionalProhibition(f"purpose touches permanent prohibition ({term})")
        cfg = self.config["context"]
        ttl = min(ttl_minutes or cfg["default_ttl_minutes"], cfg["max_ttl_minutes"])
        now = self.clock.now()
        excluded: dict[str, int] = {}

        def excl(reason):
            excluded[reason] = excluded.get(reason, 0) + 1

        state = self.ledger.state()
        cands = []
        for c in state.values():
            if c["status"] != "active" or c["confirmation"] == "user_rejected":
                continue
            if scopes and c["scope"] not in scopes:
                continue
            if predicates and c["predicate"] not in predicates and c["predicate"] != "frame":
                continue
            nodes = self.ledger.derivation_nodes([c["claim_id"]])
            if any(n.get("deleted") for n in nodes):
                excl("derivation_path_includes_deleted_content")
                continue
            if any(n.get("withdrawn") for n in nodes):  # F-05
                excl("derivation_path_includes_withdrawn_corpus_item")
                continue
            cands.append(c)
        grant, included = self._select_grant(cands, purpose, scopes)
        inc_ids = {c["claim_id"] for c in included}
        for c in cands:
            if c["claim_id"] not in inc_ids:
                excl("use_not_permitted_over_derivation_path")
        frames = [c for c in included if c["predicate"] == "frame"]
        body_claims = [c for c in included if c["predicate"] != "frame"]
        request = {"predicates": predicates or [], "subject": subject, "scopes": scopes or []}
        ordered, ranking = self.ranker.rank(body_claims, request)
        items = [{"claim": c, "rendered": self.renderer.render(c)} for c in ordered]
        frame_items = [{"claim": c, "rendered": self.renderer.render(c)} for c in frames]
        findings = self._modal_findings(items + frame_items)
        if findings and self.renderer.config.get("self_check", True):
            self.gov.record("PROHIBITED_ATTEMPT", "system", reason="modal_asymmetry_in_rendering", findings=findings)
            raise ModalAsymmetry(f"rendering would be modally asymmetric: {findings}")
        contra = contradictions(ordered, cfg.get("single_valued_predicates", []))
        withheld = [c for c in cands if c["claim_id"] not in inc_ids]
        contra_withheld = len(contradictions(ordered + withheld, cfg.get("single_valued_predicates", []))) - len(contra)
        unknowns = [{"predicate": p, "status": "no permitted claim"} for p in (predicates or [])
                    if p not in {c["predicate"] for c in included}]
        unknowns += [{"claim_id": c["claim_id"], "status": "unconfirmed inference (user has not confirmed)"}
                     for c in ordered if c["confirmation"] == "unconfirmed"]
        pkg_id = self.ids.new("pkg")
        expires = iso(now + _dt.timedelta(minutes=ttl))
        pkg = {
            "package_id": pkg_id, "purpose": purpose, "requester": requester, "issued_at": iso(now),
            "expires_at": expires,
            "claims": [{"claim_id": it["claim"]["claim_id"], "version": it["claim"]["version"],
                        "origin": it["claim"]["origin"], "confirmation": it["claim"]["confirmation"],
                        "medb_mediated": it["claim"]["medb_mediated"],
                        "temporal_validity": it["claim"]["temporal_validity"],
                        "statement": self.renderer.statement(it["claim"]), "rendered": it["rendered"]["text"]}
                       for it in items],
            "frames": [{"claim_id": it["claim"]["claim_id"], "rendered": it["rendered"]["text"]} for it in frame_items],
            "contradictions": contra,
            "unknowns": unknowns,
            "rationale": {"selection": "active, not rejected, matching requested predicates/scopes, use-permitted "
                                       "over full derivation path under a single grant",
                          "ranking": ranking},
            "boundary": {"purpose": purpose, "requester": requester, "grant_id": grant["grant_id"] if grant else None,
                         "scopes": scopes or [], "excluded_counts": excluded,
                         "contradictions_involving_withheld_claims": contra_withheld,
                         "retention": "ephemeral; not retained by MedB; discard at expiry",
                         "authority": "epistemic content only; confers no authority (Principle 5)"},
            "expiry": expires,
        }
        refs = [{"claim_id": c["claim_id"], "version": c["version"], "event_hash": c["event_hash"]}
                for c in ordered + frames]
        self.gov.record("CLAIMS_RETRIEVED", requester, purpose=purpose, claim_ids=[r["claim_id"] for r in refs],
                        claim_event_hashes={r["claim_id"]: r["event_hash"] for r in refs},
                        via="ContextPackageBuilder.build", package_id=pkg_id)
        self.gov.record("CONTEXT_PACKAGE_ISSUED", "system", package_id=pkg_id, purpose=purpose, requester=requester,
                        issued_at=pkg["issued_at"], expires_at=expires, claim_refs=refs,
                        frame_ids=[c["claim_id"] for c in frames],
                        presentation={it["claim"]["claim_id"]: it["rendered"]["template_key"] for it in items + frame_items},
                        rendering_config_digest=digest(self.renderer.config), modal_findings=findings,
                        contradictions=contra, unknowns=unknowns, boundary=pkg["boundary"], ranking=ranking,
                        structure_digest=digest({"refs": refs, "order": ranking["order"], "expires": expires}))
        return pkg


def open_package(pkg: dict, clock: Clock) -> dict:
    """Consumer-side access: refuses expired packages."""
    if clock.now_iso() >= pkg["expires_at"]:
        raise PackageExpired(f"package {pkg['package_id']} expired at {pkg['expires_at']}")
    return pkg

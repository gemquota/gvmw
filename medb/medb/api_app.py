"""HTTP routes used by the interactive MedB app (``app/``; DECISIONS D-67).

Every route here is registered through ``api.route`` -> ``register_route``, so
it appears in ``interface_inventory()["routes"]`` and (if it reaches a
primitive) under that primitive. Capability-plane routes are refused with 423
at the primitive before the handler runs; handlers then call the same
in-process interfaces (ledger / permissions / corpus / delegation / context),
which enforce the user-only and closure rules again (403 on refusal).
Audit-plane routes are never blocked and, during any suspension, are logged in
the ``auditlog`` stream (F-11). Two ``meta`` routes (whoami, changes) reach no
primitive and return no record content.

No route gives the UI database access: the app only sees what these handlers
return.
"""
from __future__ import annotations

import io
import json
import tempfile
import zipfile
from pathlib import Path

from .api import ApiError, _q, route
from .interfaces import PRIMITIVES, base_primitive, interface_inventory

APP_DIR = Path(__file__).resolve().parent.parent / "app"
CTYPES = {".html": "text/html; charset=utf-8", ".js": "application/javascript; charset=utf-8",
          ".css": "text/css; charset=utf-8", ".svg": "image/svg+xml", ".json": "application/json"}
# What each actor may attempt through the app (UI hints only; the server enforces independently).
CAN = {
    "user": ["assert", "correct", "supersede", "disavow", "delete", "confirm", "reject", "grant", "revoke",
             "ingest", "withdraw", "build_package", "resolve_escalation", "set_condition", "integrity_check",
             "export", "anchor", "delegate_root", "delegation_revoke", "read_corpus", "carry_statement"],
    "reader": ["export", "read_corpus"],
    "agent:": ["build_package", "sub_delegate", "read_corpus"],
    "auditor:": ["audit"],
}


def can_for(actor: str) -> list[str]:
    if actor in CAN:
        return CAN[actor]
    return next((v for k, v in CAN.items() if k.endswith(":") and actor.startswith(k)), [])
LIVE_IGNORE_KINDS = ("CLAIMS_RETRIEVED", "PROHIBITED_ATTEMPT")  # written by reads / refusals themselves


def _need(body: dict, *keys):
    missing = [k for k in keys if body.get(k) in (None, "")]
    if missing:
        raise ApiError(400, "missing_field", ", ".join(missing))


def _user_only(api, actor: str, what: str):
    if actor != "user":
        api.m.gov.record("PROHIBITED_ATTEMPT", actor, reason=f"api_{what}_requires_user")
        raise ApiError(403, "not_authorized", f"{what} requires the user token")


# --------------------------------------------------------------------- static app
def _static(rel: str):
    f = APP_DIR / rel

    def handler(self, actor, query, body):
        return (CTYPES.get(f.suffix, "application/octet-stream"), f.read_bytes())
    handler.__name__ = "app_static_" + rel.replace("/", "_").replace(".", "_")
    return handler


route("GET", "/app/", plane="static")(_static("index.html"))
if APP_DIR.exists():
    for _f in sorted(APP_DIR.rglob("*")):
        if _f.is_file() and _f.suffix in CTYPES and "screenshots" not in _f.parts:
            route("GET", "/app/" + _f.relative_to(APP_DIR).as_posix(), plane="static")(
                _static(_f.relative_to(APP_DIR).as_posix()))


# --------------------------------------------------------------------- meta
@route("GET", "/api/app/whoami", plane="meta")
def whoami(self, actor, query, body):
    out = {"actor": actor, "can": can_for(actor), "read_only": actor == "reader", "now": self.m.clock.now_iso()}
    if actor.startswith("auditor:"):
        st = self.m.auditors.status(actor)
        out["appointment"] = st
        if not st["active"]:
            out["can"] = []  # no active appointment: an auditor token can only read the audit plane
    return out


@route("GET", "/api/app/changes", plane="meta")
def changes(self, actor, query, body):
    """Opaque change token for live updates. Not an audit read: it returns no
    record content, and ignores events that reads/refusals themselves write."""
    return {"token": self.m.store.change_token(LIVE_IGNORE_KINDS, ("auditlog",)), "now": self.m.clock.now_iso()}


# --------------------------------------------------------------------- dashboard / audit views
@route("GET", "/api/app/dashboard", ("governance.log",), plane="audit")
def dashboard(self, actor, query, body):
    m = self.m
    now = m.clock.now_iso()
    statuses: dict[str, int] = {}
    origins: dict[str, int] = {}
    pending = 0
    for c in m.claims.state().values():  # counts only; no content leaves
        statuses[c["status"]] = statuses.get(c["status"], 0) + 1
        origins[c["origin"]] = origins.get(c["origin"], 0) + 1
        pending += c["status"] == "active" and c["confirmation"] == "unconfirmed"
    chains = {s: m.store.verify(s) for s in m.store.streams()}
    esc = m.delegation.escalations()
    obl = m.delegation.obligations()
    return {"now": now, "claims": {"total": sum(statuses.values()), "by_status": statuses, "by_origin": origins,
                                   "pending_proposals": pending},
            "chains": {s: {"ok": r["ok"], "length": r["length"], "first_bad_seq": r["first_bad_seq"]}
                       for s, r in chains.items()},
            "chains_ok": all(r["ok"] for r in chains.values()),
            "suspensions": [{"record_id": r["record"]["record_id"], "capability": r["record"]["capability"],
                             "classification": r["record"]["classification"], "status": r["status"]}
                            for r in m.suspensions.active()],
            "escalations_open": sum(1 for e in esc.values() if e["status"] == "OPEN"),
            "budget": m.evaluator.cumulative_lines(now), "emergencies": m.evaluator.emergency_count(now),
            "obligations": {s: sum(1 for o in obl.values() if o["status"] == s)
                            for s in ("OPEN", "DISCHARGED", "DISCHARGED_LATE", "BREACHED")},
            "gov_length": m.gov.head()[0], "auditlog_reads": len(m.store.events("auditlog")),
            "anchoring_enabled": m.anchoring.enabled, "anchors": len(m.store.events("anchors"))}


@route("GET", "/api/view/gov", ("governance.log",), plane="audit")
def view_gov(self, actor, query, body):
    kind = _q(query, "kind")
    limit = min(int(_q(query, "limit", 100)), 500)
    head = self.m.gov.head()[0]
    end = int(_q(query, "end_seq", head) or head)
    start = max(1, end - limit + 1)
    entries = self.m.gov.entries(start_seq=start, end_seq=end, kinds=[kind] if kind else None)
    index_ok = {}
    for e in entries:
        if e["kind"] == "STATE_TRANSITION":
            b = e["body"]
            tgt = [x for x in self.m.store.events(b["stream"]) if x["seq"] == b["seq"]]
            index_ok[e["seq"]] = bool(tgt) and tgt[0]["hash"] == b["event_hash"]
    kinds = sorted({e["kind"] for e in self.m.gov.entries()})
    return {"head_seq": head, "start_seq": start, "end_seq": end, "entries": entries, "kinds": kinds,
            "cross_links_ok": index_ok, "verification": self.m.store.verify("gov")}


@route("GET", "/api/view/verify", ("governance.log",), plane="audit")
def view_verify(self, actor, query, body):
    """Read-only chain verification of every stream (no INTEGRITY_CHECK entry; see POST /api/integrity_check)."""
    m = self.m
    res = {s: m.store.verify(s) for s in m.store.streams()}
    bad_links = []
    index = {(s, e["seq"]): e["hash"] for s in m.store.streams() for e in m.store.events(s)}
    for e in m.gov.entries(kinds=["STATE_TRANSITION"]):
        b = e["body"]
        if index.get((b["stream"], b["seq"])) != b["event_hash"]:
            bad_links.append(e["seq"])
    return {"streams": res, "cross_links_bad": bad_links, "ok": all(r["ok"] for r in res.values()) and not bad_links}


@route("POST", "/api/integrity_check", ("governance.log",), plane="audit", write=True)
def integrity_check(self, actor, query, body):
    _user_only(self, actor, "integrity_check")
    return self.m.integrity_check(actor=actor)


@route("GET", "/api/view/auditlog", ("governance.log",), plane="audit")
def view_auditlog(self, actor, query, body):
    return {"entries": self.m.store.events("auditlog"), "verification": self.m.store.verify("auditlog")}


@route("GET", "/api/view/anchors", ("governance.log",), plane="audit")
def view_anchors(self, actor, query, body):
    a = self.m.anchoring
    items = a.anchors()
    return {"enabled": a.enabled, "tsa_url": a.config.get("tsa_url"), "method": a.config.get("method"),
            "anchors": [dict(x, verification=a.verify_anchor(x)) for x in items],
            "current_heads": a.current_heads()}


@route("POST", "/api/anchors/anchor", ("governance.anchoring", "governance.log"), write=True)
def anchor_now(self, actor, query, body):
    return self.m.anchoring.anchor_heads(actor=actor)


@route("GET", "/api/view/escalations", ("governance.log",), plane="audit")
def view_escalations(self, actor, query, body):
    d = self.m.delegation
    out = []
    for eid, e in sorted(d.escalations().items(), key=lambda kv: kv[1]["opened_at"], reverse=True):
        matter = e["action"].get("matter") or f"escalation:{eid}"
        out.append(dict(e, escalation_id=eid, matter=matter, deferrability_now=d.deferrability(matter)))
    return {"escalations": out}


@route("GET", "/api/view/delegation", ("governance.log",), plane="audit")
def view_delegation(self, actor, query, body):
    m = self.m
    now = m.clock.now_iso()
    ev = m.gov.entries(kinds=["ACTION_EVALUATED"])[-int(_q(query, "limit", 30)):]
    env = [dict(e["body"], ts=e["ts"], actor=e["actor"]) for e in m.gov.entries(kinds=["ENV_CONDITION"])]
    return {"grants": list(m.delegation.grants().values()), "obligations": list(m.delegation.obligations().values()),
            "budget": m.evaluator.cumulative_lines(now), "emergencies": m.evaluator.emergency_count(now),
            "conditions": env, "recent_evaluations": [dict(e["body"], seq=e["seq"], ts=e["ts"]) for e in reversed(ev)]}


@route("GET", "/api/view/primitive_graph", ("governance.log",), plane="audit")
def view_primitive_graph(self, actor, query, body):
    s = self.m.suspensions
    active = s.active()
    adjacent = {f["capability"] for f in s.adjacent_flags()}
    act_caps = {r["record"]["capability"]: r for r in active}
    nodes = []
    for p in sorted(PRIMITIVES):
        st = "suspended" if s.is_suspended(p) else ("adjacent" if p in adjacent else "ok")
        nodes.append({"id": p, "status": st, "description": PRIMITIVES[p]["description"]})
    scoped = []
    for cap, r in act_caps.items():
        if ":" in cap:
            scoped.append({"id": cap, "base": base_primitive(cap), "status": "suspended",
                           "record_id": r["record"]["record_id"], "propagated_from": r["record"]["propagated_from"]})
    edges = [{"from": d, "to": p} for p, v in PRIMITIVES.items() for d in v["depends_on"]]
    prop = [{"from": r["record"]["propagated_from"], "to": r["record"]["record_id"]}
            for r in active if r["record"]["propagated_from"]]
    return {"nodes": nodes, "edges": edges, "scoped": scoped, "propagation": prop,
            "records": s.records(), "adjacent": sorted(adjacent)}


@route("GET", "/api/export", ("governance.log",), plane="audit")
def export_zip(self, actor, query, body):
    if actor not in ("user", "reader"):
        self.m.gov.record("PROHIBITED_ATTEMPT", actor, reason="api_export_requires_user_or_reader")
        raise ApiError(403, "not_authorized", "export is available to the user (and reader) tokens only")
    from .export import export
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "medb-export"
        manifest = export(self.m, out, actor=actor, destination_label="HTTP GET /api/export (download)")
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(out.rglob("*")):
                if f.is_file():
                    z.write(f, "medb-export/" + f.relative_to(out).as_posix())
    name = "medb-export-" + manifest["exported_at"].replace(":", "").replace(".", "")[:15] + ".zip"
    return ("application/zip", buf.getvalue(), {"Content-Disposition": f'attachment; filename="{name}"'})


# --------------------------------------------------------------------- claims
def _versions(m, claim_id: str) -> list[dict]:
    """Every content version of a claim (ASSERT/PROPOSE, then each CORRECT), with its
    content if it still exists (None once destroyed by DELETE). Kept here, not on
    ClaimLedger, so the Round 1 inventory is unchanged (D-67); the calling route
    reaches claims.ledger and is suspension-checked there."""
    from .claims import CONTENT_FIELDS, STREAM
    out = []
    for e in m.store.events(STREAM):
        b = e["body"]
        if b.get("claim_id") != claim_id or "content_ref" not in b:
            continue
        c = m.store.get_content(b["content_ref"])
        out.append({"version": len(out) + 1, "ts": e["ts"], "kind": e["kind"], "actor": e["actor"],
                    "transition_id": b["transition_id"], "corrected_fields": b.get("corrected_fields", []),
                    "content_destroyed": c is None,
                    **{f: (None if c is None else c[f]) for f in CONTENT_FIELDS}})
    return out


@route("GET", "/api/view/claim", ("claims.ledger",))
def view_claim(self, actor, query, body):
    cid = _q(query, "claim_id")
    if not cid:
        raise ApiError(400, "missing_field", "claim_id")
    as_of = _q(query, "as_of") or None
    led = self.m.claims
    cur = led.state()
    if cid not in cur:
        raise ApiError(404, "unknown_claim", cid)
    then = led.state(as_of=as_of).get(cid) if as_of else cur[cid]
    versions = _versions(self.m, cid)
    # derivation graph: ancestors (transitive derived_from, incl. corpus) and descendants
    anc = led.derivation_nodes([cid])
    desc = led.derived_dependents(cid, cur)
    items = self.m.corpus.items()
    ids = {n["id"] for n in anc} | set(desc)
    nodes, edges = [], []
    for i in sorted(ids):
        if i in cur:
            c = cur[i]
            nodes.append({"id": i, "type": "claim", "origin": c["origin"], "status": c["status"],
                          "confirmation": c["confirmation"], "label": c["predicate"] or "(destroyed)"})
            edges += [{"from": src, "to": i} for src in c["derived_from"] if src in ids]
        elif i in items:
            nodes.append({"id": i, "type": "corpus", "status": "withdrawn" if items[i]["withdrawn"] else "active",
                          "label": items[i]["source"]})
        else:
            nodes.append({"id": i, "type": "missing", "status": "missing", "label": "missing"})
    self.m.gov.record("CLAIMS_RETRIEVED", actor, purpose="ledger_inspection", claim_ids=sorted(ids & set(cur)),
                      claim_event_hashes={i: cur[i]["event_hash"] for i in sorted(ids & set(cur))},
                      via="HTTP GET /api/view/claim", as_of=as_of)
    strip = lambda c: None if c is None else {k: v for k, v in c.items() if k != "content_ref"}  # noqa: E731
    return {"claim_id": cid, "as_of": as_of, "now": self.m.clock.now_iso(), "current": strip(cur[cid]),
            "as_of_state": strip(then), "versions": versions, "transitions": cur[cid]["transitions"],
            "derived": desc, "graph": {"nodes": nodes, "edges": edges, "focus": cid}}


@route("GET", "/api/claims/delete_preview", ("claims.ledger",))
def delete_preview(self, actor, query, body):
    cid = _q(query, "claim_id")
    if not cid:
        raise ApiError(400, "missing_field", "claim_id")
    return self.m.claims.preview_delete(cid, actor=actor)


@route("POST", "/api/claims/correct", ("claims.ledger",), write=True)
def claim_correct(self, actor, query, body):
    _need(body, "claim_id", "changes")
    ch = body["changes"]
    if not isinstance(ch, dict) or not ch:
        raise ApiError(400, "bad_request", "changes must be a non-empty object")
    self.m.claims.correct(body["claim_id"], actor=actor, **ch)
    return {"claim_id": body["claim_id"], "version": self.m.claims.state()[body["claim_id"]]["version"]}


@route("POST", "/api/claims/supersede", ("claims.ledger",), write=True)
def claim_supersede(self, actor, query, body):
    _need(body, "claim_id", "by_claim_id")
    self.m.claims.supersede(body["claim_id"], body["by_claim_id"], actor=actor)
    return {"claim_id": body["claim_id"], "status": "superseded"}


@route("POST", "/api/claims/disavow", ("claims.ledger",), write=True)
def claim_disavow(self, actor, query, body):
    _need(body, "claim_id")
    self.m.claims.disavow(body["claim_id"], actor=actor, reason=body.get("reason", ""))
    return {"claim_id": body["claim_id"], "status": "disavowed"}


@route("POST", "/api/claims/delete", ("claims.ledger",), write=True)
def claim_delete(self, actor, query, body):
    _need(body, "claim_id")
    dd = body.get("destroy_derived", "none")
    n = self.m.claims.delete(body["claim_id"], actor=actor, destroy_derived=dd)
    return {"claim_id": body["claim_id"], "content_versions_erased": n, "destroy_derived": dd}


@route("POST", "/api/claims/confirm", ("claims.ledger",), write=True)
def claim_confirm(self, actor, query, body):
    _need(body, "claim_id")
    self.m.claims.confirm(body["claim_id"], actor=actor)
    return {"claim_id": body["claim_id"], "confirmation": "user_confirmed"}


@route("POST", "/api/claims/reject", ("claims.ledger",), write=True)
def claim_reject(self, actor, query, body):
    _need(body, "claim_id")
    self.m.claims.reject(body["claim_id"], actor=actor, reason=body.get("reason", ""))
    return {"claim_id": body["claim_id"], "confirmation": "user_rejected"}


# --------------------------------------------------------------------- permissions / corpus
@route("GET", "/api/view/permissions", ("permissions.closure",))
def view_permissions(self, actor, query, body):
    now = self.m.clock.now_iso()
    gs = self.m.perms.grants()
    for g in gs:
        g["active"] = g["revoked_at"] is None and (g["expires_at"] is None or g["expires_at"] > now)
    return {"grants": gs, "operations": ["ingest", "infer", "model", "use"],
            "sensitivities": ["low", "moderate", "high", "special"]}


@route("POST", "/api/permissions/grant", ("permissions.closure",), write=True)
def perm_grant(self, actor, query, body):
    _need(body, "operation", "scopes")
    return self.m.perms.grant(body["operation"], actor, scopes=list(body["scopes"]),
                              purposes=body.get("purposes") or None, sources=body.get("sources") or None,
                              sensitivity_max=body.get("sensitivity_max", "moderate"),
                              compose=bool(body.get("compose", False)), expires_at=body.get("expires_at") or None,
                              note=body.get("note", ""))


@route("POST", "/api/permissions/revoke", ("permissions.closure",), write=True)
def perm_revoke(self, actor, query, body):
    _need(body, "grant_id")
    if body["grant_id"] not in {g["grant_id"] for g in self.m.perms.grants()}:
        raise ApiError(404, "unknown_grant", body["grant_id"])
    self.m.perms.revoke(body["grant_id"], actor, reason=body.get("reason", ""))
    return {"grant_id": body["grant_id"], "revoked": True}


@route("GET", "/api/view/corpus", ("corpus.ingest",))
def view_corpus(self, actor, query, body):
    """Corpus item metadata only (content: GET /api/view/corpus_content, purpose-bound).
    ``use_purposes`` lists purposes of active use grants covering each item (UI hint)."""
    use = self.m.perms.active("use")
    items = []
    for it in sorted(self.m.corpus.items().values(), key=lambda i: i["ingested_at"], reverse=True):
        node = {"scope": it["scope"], "sensitivity": it["sensitivity"]}
        items.append(dict({k: v for k, v in it.items() if k != "content_ref"},
                          use_purposes=sorted({p for g in use if self.m.perms.covers(g, node) for p in g["purposes"]})))
    return {"items": items}


@route("POST", "/api/corpus/withdraw", ("corpus.ingest",), write=True)
def corpus_withdraw(self, actor, query, body):
    _need(body, "corpus_id")
    if body["corpus_id"] not in self.m.corpus.items():
        raise ApiError(404, "unknown_corpus_item", body["corpus_id"])
    return self.m.corpus.withdraw(body["corpus_id"], actor=actor, reason=body.get("reason", ""))


# --------------------------------------------------------------------- context
@route("POST", "/api/context/build", ("context.build", "claims.retrieval"), write=True)
def context_build(self, actor, query, body):
    _need(body, "purpose")
    pkg = self.m.context.build(body["purpose"], actor, predicates=body.get("predicates") or None,
                               scopes=body.get("scopes") or None, subject=body.get("subject") or None,
                               ttl_minutes=body.get("ttl_minutes") or None)
    rec = next((e for e in reversed(self.m.gov.entries(kinds=["CONTEXT_PACKAGE_ISSUED"]))
                if e["body"].get("package_id") == pkg["package_id"]), None)
    return {"package": pkg, "issuance_record": rec}


# --------------------------------------------------------------------- escalations / normative / env
@route("POST", "/api/escalations/resolve", ("delegation.execution", "authority.resolution"), write=True)
def escalation_resolve(self, actor, query, body):
    _need(body, "escalation_id")
    if body["escalation_id"] not in self.m.delegation.escalations():
        raise ApiError(404, "unknown_escalation", body["escalation_id"])
    pos = body.get("positions") or None
    if pos is not None:
        if not isinstance(pos, list) or not all(isinstance(p, dict) and p.get("position") in ("approve", "reject")
                                                for p in pos):
            raise ApiError(400, "bad_request", "positions: list of {position: approve|reject, priority?, statement?}")
    d = body.get("deferrable", None)
    if d not in (None, True, False):
        raise ApiError(400, "bad_request", "deferrable must be true, false or omitted")
    return self.m.delegation.resolve_escalation(body["escalation_id"], actor, approve=body.get("approve"),
                                                positions=pos, deferrable=d)


@route("POST", "/api/env/condition", ("governance.log",), write=True)
def env_condition(self, actor, query, body):
    _need(body, "condition")
    self.m.delegation.set_condition(body["condition"], bool(body.get("value", True)), actor=actor,
                                    source=body.get("source", "app"), matter=body.get("matter") or None)
    return {"condition": body["condition"], "value": bool(body.get("value", True)), "matter": body.get("matter")}


@route("GET", "/api/view/directives", ("normative.store",))
def view_directives(self, actor, query, body):
    return {"directives": list(reversed(self.m.normative.directives(matter=_q(query, "matter") or None)))}


# --------------------------------------------------------------------- F-04 auditors (D-69)
@route("GET", "/api/view/appointments", ("audit.appointment", "governance.log"), plane="audit")
def view_appointments(self, actor, query, body):
    a = self.m.auditors
    return {"appointer": a.binding(), "appointments": sorted(a.appointments().values(), key=lambda x: x["seq"]),
            "active_auditors": a.active_auditors(), "verification": self.m.store.verify("appointments"),
            "method": "HMAC-SHA256 signed appointer statements (M0 limitation: shared secret; D-69)"}


@route("POST", "/api/auditors/statement", ("audit.appointment", "governance.log"), write=True)
def auditors_statement(self, actor, query, body):
    """Carry an appointer-signed APPOINT/REVOKE statement. The carrier gains nothing:
    authority comes only from the bound appointer's signature."""
    _need(body, "statement", "signature")
    return self.m.auditors.submit_statement(body["statement"], body["signature"], actor=actor)


def _record(m, record_id):
    rec = next((r for r in m.suspensions.records() if r["record"]["record_id"] == record_id), None)
    if rec is None:
        raise ApiError(404, "unknown_suspension_record", record_id)
    return rec


@route("GET", "/api/view/audit_evidence", ("governance.log",), plane="audit")
def audit_evidence(self, actor, query, body):
    """Everything recorded about one suspension record: the record and its transitions,
    the gov entries that mention it or its capability, audit-log reads during it, and
    chain verification. Identifiers and hashes only (no claim content)."""
    m = self.m
    rid = _q(query, "record_id")
    if not rid:
        raise ApiError(400, "missing_field", "record_id")
    rec = _record(m, rid)
    cap = rec["record"]["capability"]
    rel = []
    for e in m.gov.entries():
        b = e["body"]
        hit = (b.get("suspension_record") == rid or b.get("record_id") == rid or b.get("flagged_by") == rid
               or (b.get("record") or {}).get("record_id") == rid or b.get("capability") == cap
               or (e["kind"] == "PROHIBITED_ATTEMPT" and b.get("suspension_record") == rid))
        if hit:
            rel.append(e)
    children = [r["record"]["record_id"] for r in m.suspensions.records() if r["record"]["propagated_from"] == rid]
    reads = [r for r in m.suspensions.audit_reads() if rid in r["active_suspensions"]]
    return {"record": rec, "related_gov_entries": rel, "propagated_children": children,
            "audit_reads_during": reads[-50:], "audit_reads_count": len(reads),
            "chains": {s: m.store.verify(s)["ok"] for s in ("gov", "suspension", "auditlog", "appointments")},
            "outcomes": ["PASS", "FAIL", "UNDETERMINED", "AUDIT_INDETERMINACY", "CONSTITUTIONAL_UNDERDETERMINATION"],
            "rules": {"PASS": "resolves the record (and records propagated from it)",
                      "FAIL": "record becomes NONCOMPLIANT",
                      "UNDETERMINED": "stays SUSPENDED (re-audit inconclusive)",
                      "AUDIT_INDETERMINACY": "stays SUSPENDED; REAUDIT_REQUIRED logged; never suspends by itself (F-08)"}}


@route("POST", "/api/audit/result", ("governance.log",), plane="audit", write=True)
def audit_result(self, actor, query, body):
    """Record an audit result for a capability (existing rules, incl. F-08). Audit plane:
    re-audit is the only way out of a suspension, so this is never blocked by one (D-11)."""
    _need(body, "capability", "outcome", "audit_ref")
    r = self.m.suspensions.record_audit_result(
        body["capability"], body["outcome"], actor, body["audit_ref"],
        evidence_available=list(body.get("evidence_available") or []),
        evidence_missing=list(body.get("evidence_missing") or []),
        section_iii_ref=body.get("section_iii_ref") or None)
    r["records"] = [{"record_id": a, "status": b} for a, b in r.get("records", [])]
    return r


@route("POST", "/api/audit/resolve", ("governance.log",), plane="audit", write=True)
def audit_resolve(self, actor, query, body):
    _need(body, "record_id", "outcome", "audit_ref")
    _record(self.m, body["record_id"])
    status = self.m.suspensions.resolve(body["record_id"], body["outcome"], actor, body["audit_ref"])
    return {"record_id": body["record_id"], "status": status}


# --------------------------------------------------------------------- delegation grants
@route("POST", "/api/delegation/grant", ("delegation.execution",), write=True)
def delegation_grant(self, actor, query, body):
    """Root grant (user only) or attenuated sub-delegation (holder of the parent grant)."""
    _need(body, "delegate")
    limits = body.get("limits") or {}
    if not isinstance(limits, dict):
        raise ApiError(400, "bad_request", "limits must be an object")
    if body.get("parent") and body["parent"] not in self.m.delegation.grants():
        raise ApiError(404, "unknown_delegation", body["parent"])
    return self.m.delegation.grant(body["delegate"], actor, policy_id=body.get("policy_id", "P-1"),
                                   expires_at=body.get("expires_at") or None, limits=limits,
                                   parent=body.get("parent") or None)


@route("POST", "/api/delegation/revoke", ("delegation.execution",), write=True)
def delegation_revoke(self, actor, query, body):
    _need(body, "delegation_id")
    gs = self.m.delegation.grants()
    if body["delegation_id"] not in gs:
        raise ApiError(404, "unknown_delegation", body["delegation_id"])
    if gs[body["delegation_id"]]["revoked_at"]:
        raise ApiError(409, "already_revoked", body["delegation_id"])
    self.m.delegation.revoke(body["delegation_id"], actor)
    return {"delegation_id": body["delegation_id"], "revoked": True,
            "chain_revoked": sorted(g for g, v in self.m.delegation.grants().items() if v["chain_revoked_at"])}


@route("GET", "/api/view/delegation_chain", ("governance.log",), plane="audit")
def delegation_chain(self, actor, query, body):
    d = self.m.delegation
    gid = _q(query, "delegation_id")
    gs = d.grants()
    if gid not in gs:
        raise ApiError(404, "unknown_delegation", gid or "")
    chain, cur = [], gs[gid]
    while cur is not None:
        chain.append(dict(cur, active=d.active_grant_by_id(cur["delegation_id"]) is not None))
        cur = gs.get(cur["parent"]) if cur["parent"] else None
    chain.reverse()
    desc, frontier = [], [gid]
    while frontier:
        p = frontier.pop()
        for k, v in gs.items():
            if v["parent"] == p:
                desc.append(dict(v, active=d.active_grant_by_id(k) is not None))
                frontier.append(k)
    return {"delegation_id": gid, "chain": chain, "descendants": desc}


# --------------------------------------------------------------------- corpus content
@route("GET", "/api/view/corpus_content", ("corpus.ingest", "permissions.closure"))
def corpus_content(self, actor, query, body):
    cid, purpose = _q(query, "corpus_id"), _q(query, "purpose")
    if not cid or not purpose:
        raise ApiError(400, "missing_field", "corpus_id, purpose")
    if cid not in self.m.corpus.items():
        raise ApiError(404, "unknown_corpus_item", cid)
    return self.m.corpus.retrieve(cid, purpose, actor)

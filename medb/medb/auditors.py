"""Auditor appointment (F-04; DECISIONS D-69).

Gem's ruling (2 Oct 2026): an *independent outside party* appoints auditors;
neither the user nor the system can.

* The **appointer** identity and key fingerprint are fixed by the genesis
  configuration (``config.appointer``). For databases created before F-04 the
  binding is made once, from the deployment config, and recorded as
  ``APPOINTER_BOUND``; it can never change afterwards (a different appointer in
  a later config is refused and logged).
* Appointments and revocations are **signed statements** from the appointer,
  verified here and appended to the hash-chained ``appointments`` stream, which
  is cross-linked into ``gov`` (STATE_TRANSITION mirror).
* Auditor actions (``SuspensionRegistry.record_audit_result`` / ``resolve``)
  require an *active* appointment.
* There is no unsigned path: ``appoint()`` refuses every caller (``user`` and
  ``system`` explicitly) and logs PROHIBITED_ATTEMPT.

M0 limitation: the Python stdlib has no asymmetric signatures, so statements
are authenticated with **HMAC-SHA256** under a secret held by the appointer.
Verifying an HMAC needs the same secret, so the verify key file
(``config.appointer.verify_key_file``) must be present on the MedB machine;
whoever controls that machine could therefore forge statements. The binding to
the genesis fingerprint stops a *swapped* key, not a *copied* one. A production
deployment needs an asymmetric scheme (e.g. Ed25519) so MedB holds only a
public key.
"""
from __future__ import annotations

import hashlib
import hmac
from pathlib import Path

from .errors import NotAuthorized
from .govlog import GovernanceLog
from .interfaces import reaches
from .store import EventStore
from .util import Clock, IdGen, canonical, norm_ts

STREAM = "appointments"
METHOD = "hmac-sha256"
RESERVED = ("user", "system", "reader")


def key_fingerprint(key: bytes) -> str:
    return hashlib.sha256(key).hexdigest()


def read_key(path: str | Path) -> bytes:
    return bytes.fromhex(Path(path).read_text().strip())


def sign_statement(key: bytes, statement: dict) -> str:
    """The appointer's signing function (used by tools/appointer.py)."""
    return hmac.new(key, canonical(statement).encode(), hashlib.sha256).hexdigest()


def new_statement(kind: str, appointer_id: str, auditor_id: str | None = None, appointment_id: str | None = None,
                  issued_at: str | None = None, expires_at: str | None = None, scope: str | None = None) -> dict:
    """Build an (unsigned) appointer statement; the appointer signs it with ``sign_statement``."""
    import secrets
    st = {"v": 1, "type": kind, "appointer_id": appointer_id, "nonce": secrets.token_hex(16),
          "appointment_id": appointment_id or ("appt-" + secrets.token_hex(6) if kind == "APPOINT" else None),
          "issued_at": issued_at}
    if kind == "APPOINT":
        st.update(auditor_id=auditor_id, expires_at=expires_at, scope=scope)
    return st


class AuditorRegistry:
    def __init__(self, store: EventStore, gov: GovernanceLog, clock: Clock, ids: IdGen, config: dict,
                 suspensions=None):
        self.store, self.gov, self.clock, self.ids = store, gov, clock, ids
        self.config = config
        self._suspensions = suspensions

    # ---------------------------------------------------------------- binding
    @staticmethod
    def _complete(a) -> bool:
        return isinstance(a, dict) and bool(a.get("id")) and bool(a.get("key_fingerprint"))

    def binding(self) -> dict | None:
        gen = self.gov.entries(kinds=["GENESIS"])
        g = (gen[0]["body"].get("config") or {}).get("appointer") if gen else None
        if self._complete(g):
            return {"id": g["id"], "key_fingerprint": g["key_fingerprint"], "method": g.get("method", METHOD),
                    "source": "genesis", "gov_seq": gen[0]["seq"]}
        bound = self.gov.entries(kinds=["APPOINTER_BOUND"])
        if bound:
            b = bound[0]["body"]
            return {"id": b["id"], "key_fingerprint": b["key_fingerprint"], "method": b["method"],
                    "source": "bound_once (pre-F-04 database)", "gov_seq": bound[0]["seq"]}
        return None

    def startup(self) -> None:
        """Migration + one-time binding; called when MedB opens a database."""
        gen = self.gov.entries(kinds=["GENESIS"])
        legacy = (gen[0]["body"].get("config") or {}).get("auditors") if gen else None
        if legacy is not None and not self.gov.entries(kinds=["LEGACY_AUDITORS_RETIRED"]):
            self.gov.record("LEGACY_AUDITORS_RETIRED", "system", auditors=list(legacy),
                            note="config auditor list replaced by appointer-signed appointments (F-04, D-69); "
                                 "listed ids are no longer auditors unless appointed")
        cfg = self.config.get("appointer")
        if not self._complete(cfg):
            return
        cur = self.binding()
        if cur is None:
            self.gov.record("APPOINTER_BOUND", "system", id=cfg["id"], key_fingerprint=cfg["key_fingerprint"],
                            method=cfg.get("method", METHOD),
                            note="one-time binding for a database created before F-04; never changeable")
        elif (cur["id"], cur["key_fingerprint"]) != (cfg["id"], cfg["key_fingerprint"]):
            self.gov.record("PROHIBITED_ATTEMPT", "system", reason="appointer_rebind_refused",
                            configured_id=cfg["id"], configured_fingerprint=cfg["key_fingerprint"],
                            bound_id=cur["id"], bound_fingerprint=cur["key_fingerprint"])

    def _verify_key(self, binding: dict) -> bytes | None:
        path = (self.config.get("appointer") or {}).get("verify_key_file")
        if not path or not Path(path).exists():
            return None
        key = read_key(path)
        return key if hmac.compare_digest(key_fingerprint(key), binding["key_fingerprint"]) else None

    # ---------------------------------------------------------------- refusals
    @reaches("audit.appointment", "governance.log")
    def appoint(self, auditor_id: str, actor: str) -> None:
        """No unsigned appointment path exists. Every call is refused and logged."""
        reason = {"user": "user_cannot_appoint_auditor", "system": "system_cannot_appoint_auditor"}.get(
            actor, "unsigned_appointment")
        self.gov.record("PROHIBITED_ATTEMPT", actor, reason=reason, auditor_id=auditor_id)
        raise NotAuthorized("auditors are appointed only by the independent appointer's signed statement (F-04)")

    def _refuse(self, actor: str, reason: str, statement, msg: str):
        self.gov.record("PROHIBITED_ATTEMPT", actor, reason=reason,
                        statement_sha256=hashlib.sha256(canonical(statement).encode()).hexdigest()
                        if isinstance(statement, dict) else None)
        raise NotAuthorized(msg)

    # ---------------------------------------------------------------- signed statements
    @reaches("audit.appointment", "governance.log")
    def submit_statement(self, statement: dict, signature: str, actor: str) -> dict:
        """Verify and record an appointer statement. ``actor`` is only the carrier;
        the authority is the appointer's signature."""
        if not isinstance(statement, dict) or not isinstance(signature, str):
            self._refuse(actor, "malformed_appointment_statement", statement, "statement must be an object, signature a hex string")
        b = self.binding()
        if b is None:
            self._refuse(actor, "no_appointer_bound", statement, "no appointer is bound to this database")
        if statement.get("appointer_id") != b["id"]:
            self._refuse(actor, "wrong_appointer", statement, "statement is not from the bound appointer")
        key = self._verify_key(b)
        if key is None:
            self._refuse(actor, "appointer_key_unavailable", statement,
                         "verify key missing or does not match the genesis fingerprint")
        if not hmac.compare_digest(sign_statement(key, statement), signature.lower()):
            self._refuse(actor, "appointment_signature_invalid", statement, "signature does not verify")
        kind = statement.get("type")
        sid = hashlib.sha256(canonical(statement).encode()).hexdigest()
        seen = {e["body"]["statement_sha256"] for e in self.store.events(STREAM)}
        nonces = {e["body"]["statement"].get("nonce") for e in self.store.events(STREAM)}
        if sid in seen or statement.get("nonce") in nonces or not statement.get("nonce"):
            self._refuse(actor, "appointment_statement_replayed", statement, "statement (or its nonce) already used")
        apps = self.appointments()
        aid = statement.get("appointment_id")
        if kind == "APPOINT":
            who = statement.get("auditor_id") or ""
            if not who.startswith("auditor:") or who in RESERVED:
                self._refuse(actor, "invalid_auditor_id", statement, "auditor ids must look like 'auditor:<name>'")
            if not aid or aid in apps:
                self._refuse(actor, "duplicate_appointment_id", statement, "appointment_id missing or already used")
        elif kind == "REVOKE":
            if aid not in apps or apps[aid]["revoked_at"]:
                self._refuse(actor, "revoke_unknown_appointment", statement, "no active appointment with that id")
        else:
            self._refuse(actor, "unknown_statement_type", statement, "type must be APPOINT or REVOKE")
        body = {"statement": statement, "signature": signature.lower(), "statement_sha256": sid,
                "verification": {"method": METHOD, "key_fingerprint": b["key_fingerprint"], "ok": True},
                "carrier": actor}
        ev = self.store.append(STREAM, kind, b["id"], body, self.clock.now_iso(), self.ids.new("apev"))
        self.gov.mirror(ev, b["id"], {"type": kind, "appointment_id": aid,
                                      "auditor_id": statement.get("auditor_id") or apps.get(aid, {}).get("auditor_id")})
        return dict(self.appointments()[aid], event_seq=ev["seq"])

    # ---------------------------------------------------------------- state
    def appointments(self, at: str | None = None) -> dict[str, dict]:
        at = norm_ts(at) or self.clock.now_iso()
        out: dict[str, dict] = {}
        for e in self.store.events(STREAM, until_ts=at):
            s = e["body"]["statement"]
            if e["kind"] == "APPOINT":
                out[s["appointment_id"]] = {"appointment_id": s["appointment_id"], "auditor_id": s["auditor_id"],
                                            "appointer_id": s["appointer_id"], "issued_at": s.get("issued_at"),
                                            "expires_at": norm_ts(s.get("expires_at")), "scope": s.get("scope"),
                                            "recorded_at": e["ts"], "revoked_at": None, "seq": e["seq"],
                                            "statement_sha256": e["body"]["statement_sha256"]}
            elif e["kind"] == "REVOKE":
                out[s["appointment_id"]]["revoked_at"] = e["ts"]
        for a in out.values():
            a["active"] = a["revoked_at"] is None and (a["expires_at"] is None or a["expires_at"] > at)
        return out

    def is_active(self, auditor_id: str, at: str | None = None) -> bool:
        return any(a["active"] and a["auditor_id"] == auditor_id for a in self.appointments(at).values())

    def status(self, auditor_id: str) -> dict:
        mine = [a for a in self.appointments().values() if a["auditor_id"] == auditor_id]
        return {"auditor_id": auditor_id, "active": any(a["active"] for a in mine), "appointments": mine}

    def active_auditors(self) -> list[str]:
        return sorted({a["auditor_id"] for a in self.appointments().values() if a["active"]})

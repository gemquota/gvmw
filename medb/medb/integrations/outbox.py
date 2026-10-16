"""Local notification outbox (DECISIONS D-73; off by default).

An append-only, hash-chained ``outbox`` stream of notifications derived from
the governance log: new escalations, suspensions, breached obligations and
inference proposals awaiting the user's review. A notification carries only
kinds, identifiers, times and a short fixed title -- never claim or corpus
content -- so it is safe to show in the app or hand to a local webhook.

The outbox is *derived*: ``sync()`` scans gov entries after the last one it
has seen and appends one notification per matching entry (idempotent:
``source_seq`` is recorded). It is not cross-linked into gov, so enabling it
does not perturb the governance-log evidence (as with ``auditlog``, D-12/D-66).

Optional webhook: POST each new notification as JSON to a URL on
**127.0.0.1 / ::1 only** (anything else is refused at configuration and at
send time). Off by default. Delivery results are appended to the outbox
stream (``DELIVERY``).
"""
from __future__ import annotations

import json
from urllib.parse import urlparse

from ..interfaces import reaches

STREAM = "outbox"
LOOPBACK_HOSTS = ("127.0.0.1", "::1")
NETWORK_DECLARATION = {
    "direction": "loopback",
    "purpose": "optional outbox webhook (D-73): POSTs notification metadata (kinds, ids, times; no content) "
               "to a local listener",
    "protocol": "HTTP POST (stdlib http.client)",
    "allowed_hosts": list(LOOPBACK_HOSTS),
    "default_enabled": False,
    "sends_content": False,
    "outbound": False,
}
EVENT_KINDS = ("ESCALATION_OPENED", "SUSPENSION", "OBLIGATION_BREACHED", "INFERENCE_PROPOSED",
               "SYNC_REMOTE_DELETION", "SYNC_FAILED")


def loopback_url(url: str | None) -> bool:
    if not url:
        return False
    u = urlparse(url)
    return u.scheme == "http" and u.hostname in LOOPBACK_HOSTS and not u.username and not u.password


def _notification(e: dict) -> dict | None:
    k, b = e["kind"], e["body"]
    base = {"source_seq": e["seq"], "source_hash": e["hash"], "at": e["ts"]}
    if k == "ESCALATION_OPENED":
        a = b.get("action") or {}
        return dict(base, event="ESCALATION_OPENED", title="Escalation awaiting your decision",
                    refs={"escalation_id": b.get("escalation_id"), "action_id": a.get("action_id"),
                          "agent": a.get("agent"), "clause": b.get("clause"), "matter": a.get("matter"),
                          "deferrable": b.get("deferrable")})
    if k == "SUSPENSION":
        r = b.get("record") or {}
        return dict(base, event="SUSPENSION", title="Capability suspended",
                    refs={"record_id": r.get("record_id"), "capability": r.get("capability"),
                          "classification": r.get("classification")})
    if k == "OBLIGATION_BREACHED":
        return dict(base, event="OBLIGATION_BREACHED", title="Obligation breached",
                    refs={"obligation_id": b.get("obligation_id"), "action_id": b.get("action_id")})
    if k == "STATE_TRANSITION" and b.get("stream") == "claims" and b.get("event_kind") == "PROPOSE":
        return dict(base, event="INFERENCE_PROPOSED", title="Inference proposed; awaiting your review",
                    refs={"claim_id": (b.get("summary") or {}).get("claim_id"), "proposer": e["actor"]})
    if k == "STATE_TRANSITION" and b.get("stream") == "sync":  # live sync (D-78): ids only, never tokens or content
        sm = b.get("summary") or {}
        if b.get("event_kind") == "REMOTE_DELETION":
            return dict(base, event="SYNC_REMOTE_DELETION", title="Item deleted on the remote service (kept in MedB; you may withdraw)",
                        refs={"service": sm.get("service"), "corpus_id": sm.get("corpus_id")})  # no remote id: may be a URL
        if b.get("event_kind") == "RUN" and sm.get("error"):
            return dict(base, event="SYNC_FAILED", title="Account sync failed",
                        refs={"service": sm.get("service"), "run_id": sm.get("run_id")})
    return None


class Outbox:
    def __init__(self, store, gov, clock, ids, config: dict, suspensions=None, sender=None):
        self.store, self.gov, self.clock, self.ids = store, gov, clock, ids
        self.config = config or {}
        self._suspensions = suspensions
        self._sender = sender  # tests inject a fake; default posts with http.client

    @property
    def enabled(self) -> bool:
        return bool(self.config.get("enabled"))

    def webhook(self) -> dict:
        w = self.config.get("webhook") or {}
        url = w.get("url")
        return {"enabled": bool(w.get("enabled")) and self.enabled, "url": url, "url_is_loopback": loopback_url(url)}

    def _last_seq(self) -> int:
        last = 0
        for e in self.store.events(STREAM, kinds=["NOTIFY"]):
            last = max(last, e["body"]["source_seq"])
        return last

    @reaches("integrations.outbox", "governance.log")
    def sync(self) -> list[dict]:
        """Append notifications for gov entries not yet seen. No-op while disabled."""
        if not self.enabled:
            return []
        wanted = set(self.config.get("events") or EVENT_KINDS)
        new = []
        for e in self.gov.entries(start_seq=self._last_seq() + 1):
            n = _notification(e)
            if n is None or n["event"] not in wanted:
                continue
            n["notification_id"] = self.ids.new("note")
            ev = self.store.append(STREAM, "NOTIFY", "system", n, self.clock.now_iso(), self.ids.new("oev"))
            new.append(dict(n, seq=ev["seq"]))
        if new and self.webhook()["enabled"]:
            for n in new:
                self._deliver(n)
        return new

    def _deliver(self, n: dict) -> None:
        url = (self.config.get("webhook") or {}).get("url")
        if not loopback_url(url):
            status, err = None, "refused: webhook URL is not http://127.0.0.1 or http://[::1] (D-73)"
        else:
            try:
                status, err = (self._sender or post_loopback)(url, n, float((self.config.get("webhook") or {}).get("timeout_s", 2))), None
            except Exception as e:  # delivery failure is recorded, never fatal
                status, err = None, f"{type(e).__name__}: {e}"[:300]
        self.store.append(STREAM, "DELIVERY", "system", {"notification_id": n["notification_id"], "url_host": urlparse(url or "").hostname,
                                                        "status": status, "error": err}, self.clock.now_iso(), self.ids.new("oev"))

    def feed(self, limit: int = 200) -> dict:
        notes, deliveries = [], {}
        for e in self.store.events(STREAM):
            if e["kind"] == "NOTIFY":
                notes.append(dict(e["body"], seq=e["seq"], recorded_at=e["ts"]))
            elif e["kind"] == "DELIVERY":
                deliveries[e["body"]["notification_id"]] = e["body"]
        for n in notes:
            n["delivery"] = deliveries.get(n["notification_id"])
        return {"enabled": self.enabled, "webhook": self.webhook(), "count": len(notes),
                "notifications": list(reversed(notes))[:limit], "verification": self.store.verify(STREAM)}

    def last_activity(self) -> str | None:
        evs = self.store.events(STREAM)
        return evs[-1]["ts"] if evs else None


def post_loopback(url: str, payload: dict, timeout: float) -> int:
    """POST JSON to a loopback URL; refuses any other host (checked again here)."""
    if not loopback_url(url):
        raise ValueError("webhook host must be 127.0.0.1 or ::1")
    import http.client
    u = urlparse(url)
    conn = http.client.HTTPConnection(u.hostname, u.port or 80, timeout=timeout)
    try:
        conn.request("POST", u.path or "/", body=json.dumps(payload).encode(),
                     headers={"Content-Type": "application/json", "User-Agent": "MedB-outbox"})
        return conn.getresponse().status
    finally:
        conn.close()

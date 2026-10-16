"""Optional external anchoring of stream heads (F-13, DECISIONS D-62).

This is the ONLY module in MedB that makes outbound network connections, and
the only exception to local-first operation (D-01). It is OFF by default
(``config.anchoring.enabled = false``) and nothing calls it implicitly.

What leaves the machine: exactly one SHA-256 digest -- of the canonical JSON
of every stream's head ``{stream: {seq, hash}}`` -- wrapped in an RFC 3161
TimeStampReq (plus a random nonce). No stream names, no event content, no
claim content, no identifiers.

What is stored: an ANCHOR event in the hash-chained ``anchors`` stream with the
heads, their digest, the request digest, the nonce and the raw TimeStampResp
(base64), mirrored into ``gov``. ``verify_anchor`` (and the standalone export
verifier) re-derives the digest from the recorded chains and checks that the
receipt was granted and binds that digest. Verifying the TSA's CMS signature
needs an ASN.1/X.509 stack outside the stdlib; it is done offline, e.g.
``openssl ts -verify -digest <hex> -in receipt.tsr -CAfile tsa-chain.pem``.

The only anchoring method is RFC 3161 (one round trip, self-contained
receipt; Gem's ruling, D-62 note of 2 Oct 2026).
"""
from __future__ import annotations

import base64
import hashlib
import secrets

from .errors import MedBError, NotAuthorized
from .interfaces import reaches
from .util import canonical

STREAM = "anchors"
SHA256_OID = "2.16.840.1.101.3.4.2.1"


class AnchoringDisabled(MedBError):
    pass


# ----------------------------------------------------------------- DER (minimal)
def _len(n: int) -> bytes:
    if n < 0x80:
        return bytes([n])
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(b)]) + b


def _tlv(tag: int, value: bytes) -> bytes:
    return bytes([tag]) + _len(len(value)) + value


def _int(n: int) -> bytes:
    b = n.to_bytes(max(1, (n.bit_length() + 8) // 8), "big", signed=True)
    return _tlv(0x02, b)


def _oid(dotted: str) -> bytes:
    parts = [int(x) for x in dotted.split(".")]
    out = bytes([40 * parts[0] + parts[1]])
    for p in parts[2:]:
        enc = [p & 0x7F]
        p >>= 7
        while p:
            enc.append(0x80 | (p & 0x7F))
            p >>= 7
        out += bytes(reversed(enc))
    return _tlv(0x06, out)


def build_tsq(digest: bytes, nonce: int) -> bytes:
    """RFC 3161 TimeStampReq: version 1, sha256 messageImprint, nonce, certReq TRUE."""
    if len(digest) != 32:
        raise ValueError("sha256 digest required")
    alg = _tlv(0x30, _oid(SHA256_OID) + b"\x05\x00")
    imprint = _tlv(0x30, alg + _tlv(0x04, digest))
    return _tlv(0x30, _int(1) + imprint + _int(nonce) + _tlv(0x01, b"\xff"))


def _read(buf: bytes, i: int) -> tuple[int, bytes, int]:
    tag = buf[i]
    ln = buf[i + 1]
    j = i + 2
    if ln & 0x80:
        k = ln & 0x7F
        ln = int.from_bytes(buf[j:j + k], "big")
        j += k
    return tag, buf[j:j + ln], j + ln


def parse_tsr(resp: bytes) -> dict:
    """Parse the outer TimeStampResp: PKIStatusInfo.status and the raw token."""
    tag, body, _ = _read(resp, 0)
    if tag != 0x30:
        raise ValueError("TimeStampResp must be a SEQUENCE")
    t1, status_info, nxt = _read(body, 0)
    _, status_int, _ = _read(status_info, 0)
    status = int.from_bytes(status_int, "big", signed=True)
    token = body[nxt:] if nxt < len(body) else b""
    return {"status": status, "granted": status in (0, 1), "token": token}


def receipt_binds(receipt: bytes, digest: bytes) -> dict:
    """Local check: granted status and the token's TSTInfo contains our imprint
    (OCTET STRING of the digest). Signature verification is offline (see module doc)."""
    p = parse_tsr(receipt)
    binds = _tlv(0x04, digest) in p["token"]
    return {"granted": p["granted"], "status": p["status"], "imprint_present": binds,
            "ok": p["granted"] and binds, "signature_verified": False}


def heads_digest(heads: dict) -> str:
    return hashlib.sha256(canonical(heads).encode()).hexdigest()


# Machine-readable network declaration, read by ``self_description`` (medb.netscan, D-68).
NETWORK_DECLARATION = {
    "direction": "outbound",
    "purpose": "optional external anchoring of stream heads (F-13, D-62)",
    "protocol": "RFC 3161 TimeStampReq, HTTPS POST to the configured TSA (https:// enforced)",
    "sends": "one SHA-256 digest of the canonical stream heads, plus a random nonce",
    "sends_content": False,
    "called_implicitly": False,
}


# ----------------------------------------------------------------- network client
class RFC3161Client:
    """The single outbound network call in MedB. Sends only the TimeStampReq."""

    def __init__(self, url: str, timeout: float = 20.0):
        if not url or not url.lower().startswith("https://"):
            raise ValueError("TSA URL must be https://")
        self.url, self.timeout = url, timeout

    def timestamp(self, digest: bytes, nonce: int) -> bytes:
        import urllib.request  # imported here: no network module is loaded unless anchoring is used

        req = urllib.request.Request(self.url, data=build_tsq(digest, nonce), method="POST",
                                     headers={"Content-Type": "application/timestamp-query",
                                              "Accept": "application/timestamp-reply"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:  # noqa: S310 (https enforced above)
            return r.read()


# ----------------------------------------------------------------- service
class Anchorer:
    def __init__(self, store, gov, clock, ids, config: dict, client=None, suspensions=None):
        self.store, self.gov, self.clock, self.ids = store, gov, clock, ids
        self.config = dict(config or {})
        self._client = client
        self._suspensions = suspensions

    @property
    def enabled(self) -> bool:
        return bool(self.config.get("enabled"))

    def client(self):
        if self._client is None:
            self._client = RFC3161Client(self.config.get("tsa_url") or "")
        return self._client

    def current_heads(self) -> dict:
        return {s: {"seq": self.store.head(s)[0], "hash": self.store.head(s)[1]}
                for s in self.store.streams() if s != STREAM}

    @reaches("governance.anchoring", "governance.log")
    def anchor_heads(self, actor: str = "user") -> dict:
        if actor not in ("user", "system"):
            self.gov.record("PROHIBITED_ATTEMPT", actor, reason="non_user_anchor")
            raise NotAuthorized("only the user (or a user-enabled system schedule) anchors stream heads")
        if not self.enabled:
            raise AnchoringDisabled("external anchoring is off (config.anchoring.enabled=false); see D-62")
        heads = self.current_heads()
        hd = heads_digest(heads)
        nonce = secrets.randbits(63)
        tsq = build_tsq(bytes.fromhex(hd), nonce)
        receipt = self.client().timestamp(bytes.fromhex(hd), nonce)
        check = receipt_binds(receipt, bytes.fromhex(hd))
        body = {"anchor_id": self.ids.new("anchor"), "method": "rfc3161",
                "tsa_url": getattr(self.client(), "url", None), "heads": heads, "heads_digest": hd,
                "request_sha256": hashlib.sha256(tsq).hexdigest(), "nonce": nonce,
                "receipt_b64": base64.b64encode(receipt).decode(), "local_check": check}
        ev = self.store.append(STREAM, "ANCHOR", actor, body, self.clock.now_iso(), self.ids.new("anev"))
        self.gov.mirror(ev, actor, {"anchor_id": body["anchor_id"], "heads_digest": hd, "ok": check["ok"]})
        return body

    def anchors(self) -> list[dict]:
        return [dict(e["body"], ts=e["ts"], seq=e["seq"]) for e in self.store.events(STREAM)]

    def verify_anchor(self, body: dict) -> dict:
        """Re-derive the digest from the recorded chains and check the receipt."""
        heads_ok = True
        for s, h in body["heads"].items():
            evs = [e for e in self.store.events(s) if e["seq"] == h["seq"]]
            if h["seq"] == 0:
                continue
            if not evs or evs[0]["hash"] != h["hash"]:
                heads_ok = False
        digest_ok = heads_digest(body["heads"]) == body["heads_digest"]
        rc = receipt_binds(base64.b64decode(body["receipt_b64"]), bytes.fromhex(body["heads_digest"]))
        chains_ok = all(self.store.verify(s)["ok"] for s in body["heads"])
        return {"anchor_id": body["anchor_id"], "heads_match_chain": heads_ok, "digest_ok": digest_ok,
                "chains_ok": chains_ok, "receipt": rc, "ok": heads_ok and digest_ok and chains_ok and rc["ok"]}

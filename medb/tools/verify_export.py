#!/usr/bin/env python3
"""Standalone verifier for a MedB export (medb-export/1.0).

Uses only the Python standard library and does NOT import MedB: it exists to
demonstrate that an export is interpretable without the MedB runtime.

    python3 verify_export.py <export_dir>

Checks: manifest file digests; every stream's hash chain; salted content
commitments; governance-log cross-links to domain events (and that every
normative/anchors event is cross-linked, and no auditlog event is); audit-read
log entries reference recorded suspensions; anchor receipts bind the recorded
stream heads; and an independent replay of the claim ledger compared with
state/claims_current.json.
"""
import base64
import hashlib
import json
import sys
from pathlib import Path

GENESIS = "0" * 64


def canonical(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha(s):
    return hashlib.sha256(s.encode("utf-8") if isinstance(s, str) else s).hexdigest()


def load_stream(p):
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def verify_chain(events):
    prev = GENESIS
    for i, e in enumerate(events, 1):
        rec = {k: e[k] for k in ("stream", "seq", "event_id", "ts", "kind", "actor", "body")}
        if e["seq"] != i or e["prev_hash"] != prev or sha(canonical({"prev": prev, "record": rec})) != e["hash"]:
            return False, e["seq"]
        prev = e["hash"]
    return True, None


def _der_read(buf, i):
    tag, ln, j = buf[i], buf[i + 1], i + 2
    if ln & 0x80:
        k = ln & 0x7F
        ln, j = int.from_bytes(buf[j:j + k], "big"), j + k
    return tag, buf[j:j + ln], j + ln


def receipt_binds(receipt, digest):
    """RFC 3161 TimeStampResp: status granted(0)/grantedWithMods(1) and the token
    contains OCTET STRING(digest). CMS signature: verify offline with openssl ts."""
    _, body, _ = _der_read(receipt, 0)
    _, status_info, nxt = _der_read(body, 0)
    _, st, _ = _der_read(status_info, 0)
    status = int.from_bytes(st, "big", signed=True)
    token = body[nxt:]
    return status in (0, 1) and (bytes([0x04, len(digest)]) + digest) in token


def replay_claims(events, content):
    claims = {}
    for e in events:
        b, k = e["body"], e["kind"]
        cid = b["claim_id"]
        if k in ("ASSERT", "PROPOSE"):
            claims[cid] = {"origin": b["origin"], "confirmation": b["confirmation"], "status": "active",
                           "version": 1, "content_ref": b["content_ref"]}
        c = claims[cid]
        if k == "CONFIRM":
            c["confirmation"] = "user_confirmed"
        elif k == "REJECT":
            c["confirmation"], c["status"] = "user_rejected", "rejected"
        elif k == "CORRECT":
            c["version"] += 1
            c["content_ref"] = b["content_ref"]
            if c["origin"] == "inference":
                c["confirmation"] = "user_confirmed"
        elif k == "SUPERSEDE":
            c["status"] = "superseded"
        elif k == "DISAVOW":
            c["status"] = "disavowed"
        elif k == "DELETE":
            c["status"] = "deleted"
    for c in claims.values():
        body = content.get(c["content_ref"], {}).get("body")
        c["object"] = None if body is None else body["object"]
        c["predicate"] = None if body is None else body["predicate"]
    return claims


def main(d):
    d = Path(d)
    report = {"ok": True, "problems": []}

    def bad(msg):
        report["ok"] = False
        report["problems"].append(msg)

    manifest = json.loads((d / "manifest.json").read_text())
    for rel, h in manifest["files"].items():
        if hashlib.sha256((d / rel).read_bytes()).hexdigest() != h:
            bad(f"file digest mismatch: {rel}")
    streams = {p.stem: load_stream(p) for p in sorted((d / "events").glob("*.jsonl"))}
    report["streams"] = {}
    for s, evs in streams.items():
        ok, at = verify_chain(evs)
        report["streams"][s] = {"events": len(evs), "chain_ok": ok}
        if not ok:
            bad(f"chain broken in {s} at seq {at}")
    content = json.loads((d / "content" / "claim_content.json").read_text())
    for ref, c in content.items():
        if "c-" + sha(c["salt"] + canonical(c["body"])) != ref:
            bad(f"content commitment mismatch {ref}")
    index = {(s, e["seq"]): e["hash"] for s, evs in streams.items() for e in evs}
    for e in streams.get("gov", []):
        if e["kind"] == "STATE_TRANSITION":
            b = e["body"]
            if index.get((b["stream"], b["seq"])) != b["event_hash"]:
                bad(f"gov cross-link mismatch at gov seq {e['seq']}")
    linked = {(e["body"]["stream"], e["body"]["seq"]) for e in streams.get("gov", [])
              if e["kind"] == "STATE_TRANSITION"}
    for s in ("normative", "anchors"):
        for e in streams.get(s, []):
            if (s, e["seq"]) not in linked:
                bad(f"{s} seq {e['seq']} has no gov cross-link")
    if any(s == "auditlog" for s, _ in linked):
        bad("auditlog events must not be cross-linked into gov (F-11 / D-12)")
    rec_ids = {e["body"]["record_id"] for e in streams.get("suspension", []) if e["kind"] == "RECORD"}
    for e in streams.get("auditlog", []):
        missing = set(e["body"].get("active_suspensions", [])) - rec_ids
        if missing or not e["body"].get("active_suspensions"):
            bad(f"auditlog seq {e['seq']} does not reference recorded suspensions")
    report["auditlog"] = {"reads_during_suspension": len(streams.get("auditlog", []))}
    report["normative"] = {"directives": len(streams.get("normative", []))}
    anchors_ok = 0
    for e in streams.get("anchors", []):
        b = e["body"]
        if sha(canonical(b["heads"])) != b["heads_digest"]:
            bad(f"anchor seq {e['seq']}: heads_digest mismatch")
            continue
        if any(h["seq"] and index.get((s, h["seq"])) != h["hash"] for s, h in b["heads"].items()):
            bad(f"anchor seq {e['seq']}: recorded heads do not match exported chains")
            continue
        if not receipt_binds(base64.b64decode(b["receipt_b64"]), bytes.fromhex(b["heads_digest"])):
            bad(f"anchor seq {e['seq']}: receipt not granted or does not bind heads_digest")
            continue
        anchors_ok += 1
    report["anchors"] = {"total": len(streams.get("anchors", [])), "receipts_bind_heads": anchors_ok,
                         "signature_check": "offline (openssl ts -verify)"}
    replay = replay_claims(streams.get("claims", []), content)
    exported = json.loads((d / "state" / "claims_current.json").read_text())
    for cid, c in replay.items():
        x = exported.get(cid)
        if x is None or any(x[k] != c[k] for k in ("origin", "confirmation", "status", "version", "object", "predicate")):
            bad(f"claim state mismatch {cid}")
    report["claims"] = {"total": len(replay), "deleted": sum(c["status"] == "deleted" for c in replay.values())}
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))

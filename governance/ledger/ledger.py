#!/usr/bin/env python3
import sys as _s; _s.dont_write_bytecode = True
"""Append-only, hash-chained governance event ledger (local only).

NOTE (Safeguard RR-053): governance/ syncs to a PUBLIC repo. Lines hold ONLY:
ts, actor, event, path (governance-relative), sha256 (of that file), prev, hash.
No command text, no free text, no non-governance paths. Token-like strings are redacted.

  python3 ledger.py append <actor> <event> [governance-relative-path]
  python3 ledger.py verify   (also checks /workspace/backups/ledger-anchors.jsonl + ledger-anchor-head.txt)
Off switch: touch /workspace/governance/ledger/DISABLED  (appends become no-ops)
"""
import datetime as dt, hashlib, json, os, re, sys
from zoneinfo import ZoneInfo
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "events.jsonl")
GOV = "/workspace/governance"
GENESIS = "0" * 64
TOKEN = re.compile(r"\b(gh[pousr]_|github_pat_|sk-|xox[a-z]-|AKIA|AIza|GOCSPX-|eyJ)[A-Za-z0-9_\-\.]{6,}|\b[A-Za-z0-9_\-]{32,}")
ANCHORS = "/workspace/backups/ledger-anchors.jsonl"      # append-only anchor history, outside governance/
ANCHOR_HEAD = "/workspace/backups/ledger-anchor-head.txt" # copied off box by Gem's Drive routine
HEX64 = re.compile(r"^[0-9a-f]{64}$")
NAME = re.compile(r"^[A-Za-z0-9_.-]{1,40}$")

def _clean(s):
    s = TOKEN.sub("[REDACTED]", str(s))
    return s if NAME.match(s) else "[INVALID]"

def _canon(d):
    return json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def _last():
    if not os.path.exists(LOG):
        return GENESIS
    last = None
    with open(LOG, "rb") as f:
        for line in f:
            if line.strip():
                last = line
    return json.loads(last)["hash"] if last else GENESIS

def append(actor, event, path=None, manifest_sha256=None):
    if os.path.exists(os.path.join(HERE, "DISABLED")):
        return None
    rec = {"ts": dt.datetime.now(ZoneInfo("Australia/Brisbane")).isoformat(timespec="seconds"),
           "actor": _clean(actor), "event": _clean(event)}
    if path:
        ap = os.path.realpath(os.path.join(GOV, path))
        if not ap.startswith(GOV + "/") or "/id-series/" in ap or "secret" in ap.lower():
            rec["path"] = "[EXCLUDED]"
        else:
            rel = os.path.relpath(ap, GOV)
            rec["path"] = TOKEN.sub("[REDACTED]", rel)
            if os.path.isfile(ap):
                rec["sha256"] = hashlib.sha256(open(ap, "rb").read()).hexdigest()
    if manifest_sha256 and HEX64.match(manifest_sha256):
        rec["manifest_sha256"] = manifest_sha256
    rec["prev"] = _last()
    rec["hash"] = hashlib.sha256(_canon(rec).encode()).hexdigest()
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(_canon(rec) + "\n")
    _write_anchor()
    return rec

def _chain():
    prev, n = GENESIS, 0
    for i, line in enumerate(open(LOG, encoding="utf-8"), 1):
        if not line.strip():
            continue
        rec = json.loads(line); h = rec.pop("hash")
        if rec.get("prev") != prev:
            return None, f"BROKEN at line {i}: prev mismatch"
        if hashlib.sha256(_canon(rec).encode()).hexdigest() != h:
            return None, f"BROKEN at line {i}: hash mismatch"
        prev, n = h, n + 1
    return (n, prev), None

def _anchors():
    """Return (entries, error). Entries must form a valid chain with non-decreasing count."""
    if not os.path.exists(ANCHORS):
        return [], None
    prev, out, last = GENESIS, [], -1
    for i, line in enumerate(open(ANCHORS, encoding="utf-8"), 1):
        if not line.strip():
            continue
        e = json.loads(line); h = e.pop("hash")
        if e.get("prev") != prev or hashlib.sha256(_canon(e).encode()).hexdigest() != h:
            return None, f"BROKEN anchor history at line {i}"
        if e["count"] < last:
            return None, f"BROKEN anchor history at line {i}: count went down"
        last, prev = e["count"], h
        e["hash"] = h; out.append(e)
    return out, None

def _write_anchor():
    res, err = _chain()
    if err:
        return
    hist, aerr = _anchors()
    if aerr:
        return
    prev = hist[-1]["hash"] if hist else GENESIS
    e = {"ts": dt.datetime.now(ZoneInfo("Australia/Brisbane")).isoformat(timespec="seconds"),
         "count": res[0], "head": res[1], "prev": prev}
    e["hash"] = hashlib.sha256(_canon(e).encode()).hexdigest()
    old = open(ANCHORS, "rb").read() if os.path.exists(ANCHORS) else b""
    _atomic_ro(ANCHORS, old + (_canon(e) + "\n").encode())
    _atomic_ro(ANCHOR_HEAD, f"{e['hash']} {e['count']} {e['ts']}\n".encode())

def _atomic_ro(target, data):
    """Write data to a temp file created 0444 (fd stays writable), fsync, rename over target.
    The target is never writable; there is no 0644 window."""
    tmp = f"{target}.tmp-{os.getpid()}"
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    try:
        try:
            os.write(fd, data); os.fsync(fd)
        finally:
            os.close(fd)
        os.replace(tmp, target)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)  # own temp file only
        raise

def verify():
    if not os.path.exists(LOG):
        print("no ledger yet"); return 0 if not os.path.exists(ANCHORS) else 1
    res, err = _chain()
    if err:
        print(err); return 1
    n, head = res
    hist, aerr = _anchors()
    if aerr:
        print(aerr); return 1
    if not hist:
        print("BROKEN: anchor history missing or empty", ANCHORS); return 1
    lines = [json.loads(l)["hash"] for l in open(LOG, encoding="utf-8") if l.strip()]
    for e in hist:
        if e["count"] > n:
            print(f"BROKEN: anchor says {e['count']} events, ledger has {n} (truncated)"); return 1
        want = GENESIS if e["count"] == 0 else lines[e["count"] - 1]
        if want != e["head"]:
            print(f"BROKEN: anchored head at index {e['count']} not in ledger (rewritten)"); return 1
    if os.path.exists(ANCHOR_HEAD):
        if open(ANCHOR_HEAD).read().split()[0] != hist[-1]["hash"]:
            print("BROKEN: anchor history head != ledger-anchor-head.txt"); return 1
    else:
        print("BROKEN: ledger-anchor-head.txt missing"); return 1
    print(f"OK: {n} events, head {head[:12]}; {len(hist)} anchors chained, anchor head {hist[-1]['hash'][:12]}"); return 0

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["verify"]:
        sys.exit(verify())
    if a[:1] == ["append"] and len(a) in (3, 4):
        print(json.dumps(append(*a[1:])))
        sys.exit(0)
    print(__doc__); sys.exit(2)

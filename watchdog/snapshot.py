#!/usr/bin/env python3
import sys as _s; _s.dont_write_bytecode = True
"""Nightly local governance snapshot with a hash-chained manifest.

Source: ONLY /workspace/governance. Output: /workspace/backups/governance/
  <date>.tar.gz, <date>.manifest.json (file sha256s, tar sha256, prev manifest sha256), HEAD.
Never prunes. Never reads or touches any other /workspace/backups/ directory.
Excludes secret-like names (secret, token, credential, password, cookie, .env, .pem, .key, id_rsa).
  python3 snapshot.py --dry-run | python3 snapshot.py | python3 snapshot.py --verify [--deep]
Off switch: touch /workspace/watchdog/SNAPSHOT_DISABLED
"""
import datetime as dt, hashlib, io, json, os, re, sys, tarfile
from zoneinfo import ZoneInfo
TEST = False  # module level; set True only by --test on the command line
SRC = "/workspace/governance"
OUT = "/workspace/backups/governance"
SECRETY = re.compile(r"(secret|token|credential|password|cookie|id_rsa|(^|/)\.env|\.pem$|\.key$|\.p12$|\.pfx$)", re.I)
def atomic_ro(target, data):
    """Create temp 0444 (fd writable), fsync, rename over target: target is never writable."""
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

def sha(b): return hashlib.sha256(b).hexdigest()
def canon(d): return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()

def files():
    inc, exc = [], 0
    for dp, dns, fns in os.walk(SRC):
        dns.sort()
        for f in sorted(fns):
            p = os.path.join(dp, f); rel = os.path.relpath(p, SRC)
            if SECRETY.search(rel) or os.path.islink(p): exc += 1; continue
            inc.append(rel)
    return inc, exc

def head():
    h = os.path.join(OUT, "HEAD")
    return open(h).read().strip() if os.path.exists(h) else "0" * 64

def run(dry):
    if os.path.exists("/workspace/watchdog/SNAPSHOT_DISABLED"):
        print("snapshot disabled"); return 0
    now = dt.datetime.now(ZoneInfo("Australia/Brisbane"))
    name = now.strftime("%Y-%m-%d-%H%M%S")  # existing older names (YYYY-MM-DD, -HHMM) stay valid
    tarp = os.path.join(OUT, name + ".tar.gz")
    inc, exc = files()
    if dry:
        print(f"[dry-run] would write {tarp}: {len(inc)} files, {exc} secret-like excluded, prev manifest {head()[:12]}")
        return 0
    os.makedirs(OUT, exist_ok=True)
    hashes = {}
    tmpt = f"{tarp}.tmp-{os.getpid()}"
    fd = os.open(tmpt, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    try:
      with os.fdopen(fd, "wb") as raw, tarfile.open(fileobj=raw, mode="w:gz") as t:
        for rel in inc:
            p = os.path.join(SRC, rel)
            try: data = open(p, "rb").read(); ti = t.gettarinfo(p, arcname="governance/" + rel)
            except OSError: continue
            hashes[rel] = sha(data); t.addfile(ti, io.BytesIO(data))
      os.replace(tmpt, tarp)
    except BaseException:
        if os.path.exists(tmpt):
            os.remove(tmpt)  # own temp file only
        raise
    man = {"snapshot": name, "taken_at": now.isoformat(timespec="seconds"), "source": SRC,
           "tar": os.path.basename(tarp), "tar_sha256": sha(open(tarp, "rb").read()),
           "file_count": len(hashes), "excluded_secret_like": exc,
           "prev_manifest_sha256": head(), "files": hashes}
    mb = canon(man); mp = os.path.join(OUT, name + ".manifest.json")
    atomic_ro(mp, mb)
    atomic_ro(os.path.join(OUT, "HEAD"), (sha(mb) + "\n").encode())
    print(f"wrote {tarp}: {len(hashes)} files, {exc} excluded, manifest {sha(mb)[:12]}, prev {man['prev_manifest_sha256'][:12]}")
    try:
        sys.path.insert(0, "/workspace/governance/ledger"); import ledger
        ledger.append("Snapshot", "governance_snapshot", None, sha(mb))
    except Exception as e: print("ledger skipped:", e)
    return 0

def verify(deep=False, out=None):
    global OUT
    OUT = out or OUT
    ms = sorted(f for f in os.listdir(OUT) if f.endswith(".manifest.json")) if os.path.isdir(OUT) else []
    by = {}
    for f in ms:
        b = open(os.path.join(OUT, f), "rb").read(); m = json.loads(b)
        if sha(open(os.path.join(OUT, m["tar"]), "rb").read()) != m["tar_sha256"]:
            print("BAD tar hash:", m["tar"]); return 1
        if deep:
            seen = {}
            with tarfile.open(os.path.join(OUT, m["tar"]), "r:gz") as t:
                for ti in t:
                    if ti.isfile():
                        seen[ti.name[len("governance/"):]] = sha(t.extractfile(ti).read())
            if seen != m["files"]:
                bad = sorted(k for k in set(seen) | set(m["files"]) if seen.get(k) != m["files"].get(k))
                print(f"BAD deep check in {m['tar']}: {len(bad)} file(s) differ, first: {bad[0]}"); return 1
        by[m["prev_manifest_sha256"]] = sha(b)
    cur, n = "0" * 64, 0
    while cur in by: cur = by[cur]; n += 1
    if n != len(ms) or (ms and cur != head()): print(f"BROKEN chain: linked {n}/{len(ms)}"); return 1
    # cross-check with the ledger: latest recorded snapshot manifest must be the chain head
    lp = os.environ.get("SNAPSHOT_LEDGER") if TEST else None
    lp = lp or "/workspace/governance/ledger/events.jsonl"
    rec = None
    if os.path.exists(lp):
        for line in open(lp, encoding="utf-8"):
            if line.strip():
                e = json.loads(line)
                if e.get("event") == "governance_snapshot" and e.get("manifest_sha256"):
                    rec = e["manifest_sha256"]
    if ms and not rec:
        print("BROKEN: snapshots exist but the ledger has no snapshot event with a manifest hash"); return 1
    if rec and rec != cur:
        print(f"BROKEN: chain head {cur[:12]} != ledger's last snapshot {rec[:12]}"); return 1
    print(f"OK: {n} snapshot(s) chained, head {cur[:12]}" + (", deep re-hash of every file OK" if deep else "")); return 0

if __name__ == "__main__":
    TEST = "--test" in sys.argv  # env overrides only honoured with --test
    sys.exit(verify("--deep" in sys.argv, os.environ.get("SNAPSHOT_OUT") if TEST else None) if "--verify" in sys.argv else run("--dry-run" in sys.argv))

# Scrutineer: re-check of Engineer's repair attempt 1 (22 Oct 2026, about 8:40pm AEST)

Read-only. Nothing was changed, toggled or killed. Only this file was created.

- **Run live:** `python3 -B ledger.py verify` and `python3 -B snapshot.py --verify --deep`. The code shows both only read: ledger.py:87-106 and snapshot.py:71-104. Neither touches `_write_anchor`.
- **Read-only checks:** `ps`, `ls`, `stat`, `git log`, `show`, `branch`, `rev-list`, `ls-tree` and `ls-remote`.
- **Code-only:** tamper and off-switch behaviour were assessed from the code only. I didn't repeat Engineer's tamper tests.

## Live results
- `ledger.py verify` → `OK: 5 events, head 45d8a03dee1a, matches anchor`. The anchor file holds count 5, head 45d8a03dee1a.
- `snapshot.py --verify --deep` → `OK: 2 snapshot(s) chained, head cc32b24054b3, deep re-hash of every file OK`.
- **Schedulers:** exactly one is running, pid 163089 (`bash /workspace/watchdog/scheduler.sh`, PPID 1). scheduler.pid says 163089. **Old pid 157557 is gone.** scheduler.log shows it "disabled, exiting" at 20:33:39, and the new one started at 20:34:27. No DISABLED files exist now.

## Per-fix verdicts
| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 1 | Ledger anchor outside governance/ catches truncation and full rewrite | **FAIL** (not a separate trust point) | See A1 |
| 2 | Snapshot events record the manifest hash | **PASS** | snapshot.py:67 passes `sha(mb)`; ledger.py:55-56 stores `manifest_sha256` (HEX64 only); snapshot.py:93-103 cross-checks the ledger's last snapshot against the chain head |
| 3 | `--verify --deep` re-hashes the archive contents; HEAD is 0444 | **PASS** (with gaps) | Deep check at snapshot.py:80-88; it ran OK. HEAD is `-r--r--r--` (snapshot.py:60-63). See A3 |
| 4 | Watchdog.md records only the exception type | **PASS** | watchdog.py:141 `WATCHDOG ERROR: {type(e).__name__}` |
| 5 | __pycache__ removed, bytecode disabled, gvmw .gitignore | **PASS for Engineer's files** (residue elsewhere, A5) | governance/ledger/ has no __pycache__. `sys.dont_write_bytecode = True` at ledger.py:2 and snapshot.py:2 (and watchdog.py:2). `export PYTHONDONTWRITEBYTECODE=1` at scheduler.sh:8. d3bcd67 adds `__pycache__/` and `*.pyc` to .gitignore |
| 6 | Redaction regex has word boundaries | **PASS** (partly effective) | ledger.py:19 has `\b` before the prefixes and the 32+ class. See A6 |
| 7 | Watchdog alerts if scheduler.pid is dead; new pid 163089 | **PASS on code / FAIL on design** | watchdog.py:76-89 checks the pid file and `/proc/<pid>/cmdline`. See A7 |
| 8 | Four tamper tests fail as expected, on /tmp copies | **Not re-run; FAIL on clean-up** | /tmp/tamper/ was left behind (A8) |

## Remaining gaps
- **A1, the anchor isn't independent:**
  - `/workspace/backups/ledger-anchor.json` is `-rw-r--r-- box`, so it's writable by the same user that writes the ledger. Nothing is keyed or signed.
  - It's rewritten on the **same code path** as the ledger: `append()` calls `_write_anchor()` (ledger.py:61). There's also a public `anchor-init` command (ledger.py:112-113) that re-anchors to whatever the ledger currently holds.
  - So a matched rewrite passes: rewrite events.jsonl with a recomputed chain, then run `ledger.py anchor-init` (or any append). The same holds for truncation followed by `anchor-init`.
  - What it does catch is an edit or truncation made *without* touching the anchor.
  - **Fix:**
    - Make the anchor append-only and outside the writer's reach, for example a copy Archivist keeps off-box (resilience rule, once Gem confirms Drive), or a head recorded in the digest or approvals by another bot.
    - Remove `anchor-init` from the CLI, or gate it behind Safeguard.
    - Have verify compare against the anchor's *history*, not just its latest value.
  - **Edge bug:** if the anchor count is 0 and the ledger has lines, ledger.py:103 indexes `[-1]` and compares against the last line, not the genesis. Minor.
- **A3, snapshot gaps:**
  - The 0444 mode is cosmetic. run() itself chmods HEAD back to 0644 (snapshot.py:61-62), and so can any same-user process.
  - The ledger cross-check passes when the ledger has no `manifest_sha256` events (`rec` is None, snapshot.py:102), so deleting those events plus a re-anchor (A1) bypasses it.
  - verify honours the `SNAPSHOT_OUT` and `SNAPSHOT_LEDGER` environment variables (snapshot.py:94, :107). That's fine for tests, but a scheduled verify should ignore them.
- **A5, bytecode residue (not Engineer's file):** `governance/proposals/2026-10-22-redundancy/_tools/__pycache__/split.cpython-313.pyc` still exists, under governance/. d3bcd67's .gitignore keeps it out of future gvmw commits. Its owner (Architect's build tool) should delete it, with a log line.
- **A5 git facts (read-only):**
  - The gvmw working copy is `/workspace/_repo-sync/gvmw.tmp`. d3bcd67 ("Ignore Python bytecode (__pycache__, *.pyc)", 8:33:24pm, .gitignore +4 lines) is **local only**. The branch is `main [origin/main: ahead 2]`, so 57bc5bb is unpushed too.
  - `git ls-remote origin refs/heads/main` → 4f43fc9 (the remote head).
  - **No .pyc or __pycache__ exists anywhere in gvmw history.** `rev-list --all --objects` found 0, and the `origin/main` tree has 0. The ledger .pyc was created at 8:29pm, after the last push at 6:42pm.
  - `/workspace/_repo-staging/workspace-snapshot` (also origin gvmw, at e21adc3) has 0 too.
  - **Risk:** if the 9pm sync pushes, d3bcd67 and 57bc5bb go public with it.
- **A6, redaction (minor):** with `\b`, the `sk-` prefix no longer matches inside `compliance-risk-officer`, because there's no word boundary between `i` and `s`. That fixes the false positive. The `\b[A-Za-z0-9_\-]{32,}` branch can still redact a long hyphenated file name. That's an accuracy issue, not a leak.
- **A7, circular alert:** the scheduler-alive check runs *inside* the watchdog, and the watchdog is launched only by the scheduler (scheduler.sh:18). If the scheduler dies, no watchdog runs, so the alert never fires. It only catches the case where the pid file points at a dead process during a manual run. **Fix:** an independent trigger, such as a bot's routine running `watchdog.py --json` daily, or the off-box heartbeat in the plan.
- **A8, leftover test copies:** `/tmp/tamper/` (21 MB, `drwxr-xr-x box`, files `-rw-r--r--`, created 8:34pm) still holds:
  - edit.jsonl, trunc.jsonl, rewrite.jsonl, ok.jsonl, anchor.json and lv.py;
  - snap/ with a full governance snapshot tar, its manifest and HEAD.

  That tar is a world-readable copy of governance/, including id-series. **Fix:** Engineer deletes /tmp/tamper and logs it. That's a scratch-file deletion, so no backup is needed (R-049). I didn't delete it.

## Summary
- **PASS:** fixes 2, 3, 4, 5 (Engineer's files) and 6.
- **FAIL:** 1 (the anchor isn't independent; a matched rewrite plus `anchor-init` passes) and 8 (clean-up).
- **PASS on code / FAIL on design:** 7 (the scheduler self-check can't fire when the scheduler is dead).
- One scheduler is running (163089). The .gitignore commit is local only. No .pyc has ever reached gvmw.

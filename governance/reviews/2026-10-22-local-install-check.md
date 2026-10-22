# Scrutineer: independent check of Engineer's local install (22 Oct 2026, about 8:40pm AEST)

Read-only. I changed, killed, toggled and created nothing apart from this file. No secret values are shown. Read first: governance/risk/2026-10-22-local-install-status.md (the "status doc").

**What ran live:** both verify commands (after the code showed they only read; run with `python3 -B`, so no bytecode was written), `ps` / `/proc/157557/cmdline`, and read-only greps that counted matches.

**Code-only:** the tamper assessment and the off-switch checks. Testing either live would mean editing the ledger or manifest or touching a DISABLED file.

| Point | Result |
|---|---|
| 1. Code review and tamper detection | **FAIL.** The verify commands are safe and report OK, but tamper evidence is weak (see 1b) |
| 2. Leak check | **PASS**, with two latent risks to fix |
| 3. Snapshot scope | **PASS** |
| 4. Off switches | **PASS** |
| Destructive gate not installed | **PASS** (by inspection) |
| Schedules match the status doc | **PASS**, with one comment mismatch |

## 1. Code review
**a. The verify commands are read-only, so I ran them.**
- `ledger.py verify` (ledger.py:58-71) only opens events.jsonl to read, and prints. Output: `OK: 3 events, head 0b46b19e32d5`. This matches the status doc.
- `snapshot.py --verify` (snapshot.py:67-78 in the file; main at :81) only lists, reads and hashes files in /workspace/backups/governance/, and reads HEAD. Output: `OK: 1 snapshot(s) chained, head 108bc2b1a1ff`. HEAD holds 108bc2b1a1ff…, which matches.
- **Scheduler:** pid 157557 is `bash /workspace/watchdog/scheduler.sh` (PPID 1). It's the only process from this install.

**b. Tamper detection (from the code; no live tamper test).**
- **Ledger** (ledger.py:53, :58-71): an *unkeyed* SHA-256 chain (`prev` and `hash`). It catches an edit or deletion in the middle of a line. It does **not** catch:
  1. Rewriting the whole file with a recomputed chain. Anyone who can write the file can recompute it, because there's no key or signature.
  2. Truncating trailing lines. verify has no expected head or count, so a shortened ledger still reads "OK".
  3. Changes to the files the ledger points to. verify doesn't re-hash `sha256` against the current file.
- **Snapshot** (snapshot.py:67-78):
  - It checks each tar's SHA-256 against its manifest, and the manifest chain against HEAD.
  - It doesn't check the per-file hashes inside the tar.
  - The manifest and HEAD are unkeyed. HEAD is mode 0644 (only the tar and manifest are made 0444, at :58), and chmod by the same user undoes 0444 anyway. So a matched rewrite of the tar, manifest and HEAD passes.
  - A deleted snapshot together with a rewound HEAD isn't caught either.
- **Not cross-anchored:** snapshot.py:63 logs `governance_snapshot` to the ledger with no path and no manifest hash. So the ledger can't vouch for which snapshot existed.
- **On the doc's tamper test:** "BROKEN at line 1" proves only the naive-edit case. It was run on a /tmp copy, so I couldn't re-check it.

**Fixes:**
1. Pass the manifest's SHA-256 in snapshot.py:63 (for example as the event, or as a `manifest_sha256` field), so the ledger anchors each snapshot.
2. Have verify print the event count and head, and compare them with an external record of the expected head, such as the off-box copy or a head noted in the digest.
3. Add `--deep` to snapshot verify to check the per-file hashes in the tar.
4. Consider an HMAC whose key is held outside governance/ (Safeguard inventory, name only), or off-box anchoring under the resilience rule once Gem confirms Drive.

## 2. Leak check (locations and counts only)
I searched for emails, token prefixes, absolute paths (`/workspace|/home|/tmp|/root|/etc`) and command words (`python3|nohup|touch|rm`).
- **governance/ledger/events.jsonl** (3 lines): 0 emails, 0 tokens, 0 absolute paths, 0 command text.
  - Keys are only ts, actor, event, path, sha256, prev and hash.
  - The paths are governance-relative (`digest/inbox/2026-10-22/Watchdog.md`, `ledger/ledger.py`).
  - This meets RR-053 condition 1.
- **governance/digest/inbox/2026-10-22/Watchdog.md** (2 lines): 0 of each. The content is a status line only.
- **backups/governance/2026-10-22.manifest.json** (local, not synced): 0 emails, 0 command text.
  - 1 absolute path: the `source` field, `/workspace/governance`.
  - 8 token-pattern hits, all **false positives**: file names containing "risk-officer", which match the `sk-` prefix. These are codex/compliance-risk-officer/* and proposals/compliance-risk-officer-v002.md.
- **backups/governance/HEAD and watchdog/scheduler.log:** 0 of each.

**Latent risks (fixes):**
- **(a) Exception text in the error path:** watchdog.py:125-127 writes `WATCHDOG ERROR: {e}` into Watchdog.md, under governance/, which syncs to the public gvmw. A Python exception message can carry absolute paths. **Fix:** write only `type(e).__name__`, with the detail going to scheduler.log.
- **(b) Bytecode in the synced tree:** governance/ledger/__pycache__/ledger.cpython-313.pyc sits under governance/. It's compiled bytecode that embeds the absolute source path, and it syncs publicly. The snapshot also includes it, plus proposals/2026-10-22-redundancy/_tools/__pycache__/split.cpython-313.pyc. **Fix:** run imports with `PYTHONDONTWRITEBYTECODE=1` (set it in scheduler.sh), and have Engineer exclude `__pycache__` from the gvmw sync. Removing the existing file is Engineer's change, with a log line.
- **(c) Side effect of the redaction rule (minor):** ledger.py:18's `sk-` and 32-plus-character patterns would turn legitimate paths such as `codex/compliance-risk-officer/…` into `[REDACTED]`. That's not a leak, but the ledger loses accuracy. **Fix:** anchor the token prefixes on a word boundary.

## 3. Snapshot scope
- The source is the constant `/workspace/governance` (snapshot.py:13) and the output is the constant `/workspace/backups/governance` (:14). verify lists only OUT (:68).
- No code path names or walks `/workspace/backups/bie-caches-2026-10-10/`.
- The output agrees:
  - The manifest has `source` /workspace/governance, 1,298 files and 10 excluded.
  - No manifest key contains `bie-cache` or starts with `..`.
  - The tar has 0 members outside `governance/`.
- **Symlinks:** governance/ currently has 0 symlinks.
  - `os.walk` doesn't follow directory symlinks by default (:21).
  - File symlinks are skipped (:25, `os.path.islink`).
  - So a symlink into bie-caches would be skipped.
  - The remaining risk is a race: a path swapped for a symlink between the check at :25 and the open at :50. That's very low risk for a local job.
- **Globs:** there are none. The exclusion is a regex on the relative path (:15). Note that it excludes only secret-like *names*, not content.
- **Hardlinks:** these aren't detected, but there are none expected.
- **Info:** the snapshot includes id-series/ (1 file). It's local only, so that's acceptable.

## 4. Off switches (code-only; none were flipped)
- **SCHEDULER_DISABLED:** checked at the top of every loop (scheduler.sh:13). The loop exits within 20 s.
- **WATCHDOG_DISABLED:** checked by the scheduler (scheduler.sh:17) **and** at the start of watchdog main() (watchdog.py:119). That's before any run, alert, ledger or error path, so it's honoured on every path, including manual runs.
- **SNAPSHOT_DISABLED:** checked at the start of run() (snapshot.py:34) for both the dry run and the real run. The scheduler calls run(). `--verify` ignores it, which is fine because verify is read-only.
- **ledger DISABLED:** checked at the start of append() (ledger.py:39). That covers every writer: the CLI, watchdog.py:108 and snapshot.py:63. verify ignores it (read-only).
- **Minor:** scheduler.sh's comment says "exits within 30 s", but the loop sleeps 20 s. The status doc's "checks every 20 s" is correct.

## Destructive gate and schedules
- **Destructive gate:** not installed. Nothing in /workspace/watchdog or governance/ledger is a gate. The only process from this install is pid 157557. scheduler.sh calls only watchdog.py and snapshot.py. This was checked by inspection only.
- **Schedules:** scheduler.sh:17-18 runs the watchdog at 09:30 and 21:30 AEST and the snapshot at 02:00 AEST, with `TZ=Australia/Brisbane` (:7). That matches the status doc.
- **Note:** the scheduler isn't restarted after a reboot (doc and :6). The watchdog can't see its own scheduler die. **Fix:** have the watchdog run also check that `scheduler.pid` is alive, or add the off-box heartbeat the plan describes.

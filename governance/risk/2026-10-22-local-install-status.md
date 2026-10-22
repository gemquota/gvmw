# Local install status: review fixes (22 Oct 2026, 8:31pm AEST)
Engineer. Installed on THIS BOX ONLY. No off-box uploads, no network calls, no deletions, no profile or codex edits. The destructive-ops gate is **not installed** (Gem: "Not now"). The healthchecks.io idea was scrapped (Gem). Safeguard RR-053 conditions applied.

## What's live
| Piece | Schedule (AEST) | Paths | Off switch (one line) |
|---|---|---|---|
| Scheduler loop (no cron or systemd --user on this box) | always on, checks every 20 s (`PYTHONDONTWRITEBYTECODE=1`) | `/workspace/watchdog/scheduler.sh`, log `scheduler.log`, pid `scheduler.pid` (pid 163089, restarted cleanly 8:34pm) | `touch /workspace/watchdog/SCHEDULER_DISABLED` |
| Liveness watchdog | 9:30am and 9:30pm daily | `/workspace/watchdog/watchdog.py`. Alerts: `/workspace/governance/digest/inbox/<date>/Watchdog.md` | `touch /workspace/watchdog/WATCHDOG_DISABLED` |
| Event ledger | on every watchdog or snapshot run, plus manual | `/workspace/governance/ledger/events.jsonl`, `ledger.py` (`append`, `verify`) | `touch /workspace/governance/ledger/DISABLED` |
| Governance snapshot | 2:00am daily | `/workspace/watchdog/snapshot.py`. Output: `/workspace/backups/governance/<date>.tar.gz`, `<date>.manifest.json`, `HEAD` | `touch /workspace/watchdog/SNAPSHOT_DISABLED` |
To undo any switch, remove the file you touched. After a box reboot the scheduler is not running. Restart it with: `nohup /workspace/watchdog/scheduler.sh >> /workspace/watchdog/scheduler.log 2>&1 &`

## Safeguard RR-053 conditions
1. Ledger lines hold only `ts`, `actor`, `event`, a governance-relative `path`, `sha256`, `prev` and `hash`. Actor and event must be short names. Token-like strings are redacted. Paths outside governance, and any id-series or secret paths, are recorded as `[EXCLUDED]`. There's no command text.
2. Watchdog.md has status lines with governance-relative paths only. It contains no secrets. The healthchecks hook is removed entirely, and no network code is left.
3. The snapshot reads ONLY `/workspace/governance` and writes only into `/workspace/backups/governance/`. `/workspace/backups/bie-caches-2026-10-10/` (on HOLD) is never read or touched. 10 secret-like names are excluded.
4. Disk alert: under 15% or under 5 GB free on `/workspace`. Snapshots are never pruned. Today: 115.6 GB free (91%). The first snapshot is 20 MB.

## Test runs (22 Oct, 8:29pm AEST)
- Watchdog dry run: everything OK (digest sent, Scorer, Scrutineer, 16 inbox files, disk 91% free). It printed what it would append.
- Watchdog real run: appended "FYI … all checks OK" to `digest/inbox/2026-10-22/Watchdog.md`. Exit 0.
- Snapshot dry run: 1,298 files, 10 excluded, prev 000000000000.
- Snapshot real run: `2026-10-22.tar.gz` (20.8 MB, read-only). Manifest head `108bc2b1a1ff`. `--verify` reports OK, 1 snapshot chained.
- Ledger: 3 events, `verify` reports OK, head `0b46b19e32d5`. A tamper test on a /tmp copy was detected ("BROKEN at line 1").

## Caveats
- The ledger and Watchdog.md are under governance/, which syncs to the PUBLIC gvmw at 9pm. They're designed to be safe for that. The sync itself still needs fixing or freezing.
- A local watchdog can't catch a full box or billing outage (see `2026-10-22-liveness-watchdog-plan.md`).
- Snapshots are local, on the same disk. Off-box copy: Gem approved the Google Drive backup directly in Engineer's chat at 8:30pm AEST on 22 Oct. This is UNVERIFIED by me: it was relayed by Engineer, and I did not see the chat. It runs as Engineer's server-side routines 'gvmw auto-sync' (about 9:06pm) and 'Governance backup to Google Drive' (about 2:28am). Both are UNVERIFIED until their first evidence appears.

## Fixes after Scrutineer's check (`reviews/2026-10-22-local-install-check.md`), 22 Oct 8:34pm AEST
- (a) Deleted `governance/ledger/__pycache__`, which my own code generated. All three scripts now set `sys.dont_write_bytecode`, and the scheduler exports `PYTHONDONTWRITEBYTECODE=1`. Added `__pycache__/` and `*.pyc` to `/workspace/_repo-sync/gvmw.tmp/.gitignore` and committed locally as `d3bcd67`, author gemquota. **Not pushed.** The clone is now ahead of origin by 2 commits; the other one is `57bc5bb` (medb/data ignore, 8:27pm), which isn't mine.
- Still present, not mine, not deleted: `governance/proposals/2026-10-22-redundancy/_tools/__pycache__/split.cpython-313.pyc`. It is now covered by the gitignore, as long as the sync uses this clone's `.gitignore`.
- (b) If the watchdog itself crashes, `Watchdog.md` gets only the exception type, never the raw error text.
- (c) Snapshot ledger events now record `manifest_sha256`. `snapshot.py --verify` also fails if the chain head doesn't match the last snapshot hash in the ledger.
- (d) Anchor file `/workspace/backups/ledger-anchor.json` (count + head) sits outside governance/ and isn't synced. It's updated on every append. `ledger.py verify` fails if the ledger has fewer events than the anchor, or if the anchored head isn't where the anchor says it should be.
- (e) `snapshot.py --verify --deep` re-hashes every file inside each archive against its manifest. `HEAD` is now 0444.
- (f) The redaction regex now uses word boundaries, so `risk-officer` stays as it is. A `ghp_…` token is still redacted.
- (g) The watchdog alerts if `scheduler.pid` isn't a live `scheduler.sh`, unless the off switch is set.
- (h) The scheduler comment now says 20 s.

## Tamper proofs (run on /tmp/tamper copies; all must fail)
| Test | Result |
|---|---|
| Edited ledger line | `BROKEN at line 2: hash mismatch`, rc 1 |
| Truncated ledger (3 lines cut to 2) | `BROKEN: ledger has 2 events, anchor says 3 (truncated)`, rc 1 |
| Full rewrite (valid new chain, same count) | `BROKEN: head differs from anchor (rewritten)`, rc 1 |
| Changed file in archive, with the attacker also fixing tar_sha256 and HEAD | `--deep`: `BAD deep check … rulings.md`, rc 1. Plain `--verify` against the real ledger: `BROKEN: chain head 85f3583ebbbd != ledger's last snapshot cc32b24054b3`, rc 1 |
Live state: ledger 4 events, OK, head `9dda0aef3314`, matches the anchor. Snapshots: 2 chained, deep OK, head `cc32b24054b3`. Watchdog real run at 8:34pm: all OK, scheduler running.

Off switch for the anchor: none needed. It only changes when the ledger is appended to, and the ledger off switch stops that.

## Repair attempt 2 (`reviews/2026-10-22-local-install-check-2.md`), 22 Oct 8:38pm AEST
1. **Anchor history.** `anchor-init` is removed. `/workspace/backups/ledger-anchors.jsonl` is append-only, and each entry holds `ts`, `count`, `head`, `prev` and `hash`. A new entry is added on every ledger append. `chattr` isn't available on this box and I didn't use root, so the file is kept at **0444 between writes**. The chain head goes to `/workspace/backups/ledger-anchor-head.txt` (0444). `ledger.py verify` checks four things: the ledger chain, the anchor chain, that the anchor count never goes down, that every anchored head is in the ledger at its anchored index, and that the head file matches.
   **True independence comes only from the off-box Google Drive copy of `ledger-anchor-head.txt`.** An attacker with box access could rebuild the ledger, the anchor history and the head file together, and local verify would pass (test 5). Only a comparison with the off-box copy catches that.
   The old `/workspace/backups/ledger-anchor.json` is no longer used. I left it in place rather than deleting it.
2. `watchdog.py --check-scheduler-only` prints the scheduler status and exits 0 or 1. It writes nothing. It's for Gem's independent routines and is not scheduled by me.
3. **Deletion log:** at 8:37pm AEST I deleted `/tmp/tamper/`, my own tamper-test copies (ledger and snapshot copies). From now on, tests run in `/workspace/backups/_tamper-tmp` (mode 0700), which is removed afterwards. It was created and removed at 8:38pm.
4. `HEAD` goes back to 0444 after every snapshot write (checked after the 8:37pm run).
5. If snapshots exist but the ledger has no snapshot event with a manifest hash, verify now FAILS.
6. `SNAPSHOT_OUT` and `SNAPSHOT_LEDGER` are ignored unless `--test` is given. Checked: `SNAPSHOT_OUT=/nonexistent snapshot.py --verify` still verified the real directory.

### Tamper tests, round 2 (in `/workspace/backups/_tamper-tmp`, now removed)
| # | Test | Result |
|---|---|---|
| 1 | Edited ledger line | `BROKEN at line 2: hash mismatch` (rc 1) |
| 2 | Truncation | `BROKEN: anchor says 6 events, ledger has 3 (truncated)` (rc 1) |
| 3 | Full rewrite | `BROKEN: anchored head at index 6 not in ledger (rewritten)` (rc 1) |
| 4 | Rewrite + re-anchor (valid new anchor appended) | `BROKEN: anchored head at index 6 not in ledger (rewritten)` (rc 1) |
| 5 | Rewrite + whole anchor history and head file rebuilt | Local verify passes (expected limit). Compared with the off-box head copy (simulated), it's a MISMATCH, so detected |
| 6 | Edited anchor entry | `BROKEN anchor history at line 1` (rc 1) |
| 7 | Changed file in archive | `BAD tar hash` (rc 1) |
| 8 | Changed file + attacker-fixed tar hash | `--deep`: `BAD deep check … rulings.md` (rc 1) |
| 9 | Snapshots but no ledger snapshot event | `BROKEN: snapshots exist but the ledger has no snapshot event…` (rc 1) |
Live state at 8:38pm: ledger 8 events OK, 3 anchors chained (head `682b2d8bbfd6`). Snapshots: 3 chained, deep OK (head `3130a45beada`). Scheduler pid 163089 running. The watchdog's real run was all OK. No `.pyc` files. Nothing pushed.

## Repair attempt 3 (`reviews/2026-10-22-local-install-check-3.md`), 22 Oct 8:42pm AEST
- (a) Snapshot tar, manifest, `HEAD`, `ledger-anchors.jsonl` and `ledger-anchor-head.txt` are now written to a temp file that is *created* 0444 (the open file handle stays writable), then fsynced and atomically renamed over the target. The target is never 0644, so there's no writable window. The temp file sits next to the target as `<name>.tmp-<pid>` until the rename. The ledger `events.jsonl` itself is still a plain append (0644), because other writers append to it.
- (b) An anchor with count 0 must now have head = genesis (64 zeros). Test: an append after a count-0 anchor verified OK, and a count-0 anchor with a wrong head failed (`anchored head at index 0 not in ledger`).
- (c) `--check-scheduler-only` exits 0 if running, 1 if DOWN, and 2 with `DISABLED` if the off switch is set. When the scheduler is down it also appends an Urgent line to today's `Watchdog.md`. Tested: running gave rc 0. Simulated DISABLED gave rc 2. Simulated DOWN gave rc 1 and showed the alert line (dry run).
- (d) `TEST` is defined at module level in `snapshot.py`. Importing `snapshot` and calling `verify(True)` works (rc 0).
- (e) Ledger event 9 is `cleanup` by Engineer with path `[EXCLUDED]`, recording the deletion of `/tmp/tamper` at 8:37pm AEST. The ledger has no free-text field, so its `ts` is the time it was recorded (8:41pm); this doc holds the 8:37pm time.
- Re-tested at 8:41pm: edited line failed and truncation failed. Snapshots: 4 chained, deep OK (head `938351524bf9`). Ledger: 10 events, 5 anchors, OK. The new snapshot `2026-10-22-2041.tar.gz` was written atomically at 0444. Test folder `/workspace/backups/_tamper-tmp` was created 0700 and removed.

## Off-box pieces (Engineer's server-side Grok Bot routines, not on this box)
These are as described to me by Engineer:
- The 2:30am Google Drive upload, the comparison of the anchor head against yesterday's Drive copy, and the `--check-scheduler-only` calls at 9pm and 2:30am. They run as Engineer's routines 'gvmw auto-sync' (about 9:06pm) and 'Governance backup to Google Drive' (about 2:28am).
- They aren't on the box, so no script or log exists here until they first run. Their first evidence will be lines in `governance/digest/inbox/<date>/Engineer.md` and the Drive folder 'Governance backups' on the gemquota account.
- **True independence comes only from that off-box Drive copy.** Tamper test 5 (rewriting the ledger together with its anchor history) was checked off box only in simulation. The real off-box check starts after the second nightly upload, the first night that has a "yesterday's copy" to compare against.

## Minor fixes after check 4 (`reviews/2026-10-22-local-install-check-4.md`), 22 Oct 8:45pm AEST
- On a failed write, the atomic writers (tar, manifest, HEAD, anchors, anchor head) remove only their own `.tmp-<pid>` file in an `except` block, then re-raise.
- New snapshot names use seconds: `YYYY-MM-DD-HHMMSS` (first one: `2026-10-22-204440`). The existing `2026-10-22`, `-2034`, `-2037` and `-2041` snapshots keep their names and still verify. The chain links by hash, not by name.
- `--check-scheduler-only` checks `WATCHDOG_DISABLED` first and exits 2 with `DISABLED`. It then checks `SCHEDULER_DISABLED` (exit 2), then whether the scheduler is running (0) or down (1, plus an alert).
- Ledger event 11 is `cleanup-detail.evt9.own-tmp-copy.2037`, by Engineer, with no path. The ledger only accepts short names, so the event field holds this slug. Its meaning: "deleted /tmp tamper-test copy of governance (own temp files) at 20:37 AEST", describing event 9.
- **Growth and pruning:** each snapshot adds about 20 MB, so about 20 MB a day at one scheduled run per night (today's extra test runs added about 100 MB). Nothing is pruned. The watchdog's disk alert (under 15% or under 5 GB free) covers growth. Today there is about 115 GB free, which is roughly 15 years at 20 MB a day. Any pruning would need Gem's approval.
- Verify at 8:44pm: 5 snapshots chained, deep OK (head `021da26b93e0`). Ledger: 12 events, 7 anchors, OK. Scheduler running. No temp leftovers. Nothing pushed.

# Scrutineer: check 4, Engineer's repair attempt 3 (final), 22 Oct 2026, about 8:50pm AEST

Read-only. Nothing was changed, toggled or killed. Only this file was created.

- **Run live, with `python3 -B`:**
  - `ledger.py verify` and `snapshot.py --verify --deep`. The code shows both only read.
  - `watchdog.py --check-scheduler-only`. I ran it only after the code showed the running path writes nothing (watchdog.py:140-148: `alert()` is called only when `not good`) **and** `ps` showed the scheduler alive.
- **Code-only:** the DOWN and DISABLED paths, and failure clean-up.

## Live results
- **Ledger:** `OK: 10 events, head ff39316969b6; 5 anchors chained, anchor head 27f0a2d8aeca`. That's the expected 10 events and 5 anchors.
- **Snapshot:** `OK: 4 snapshot(s) chained, head 938351524bf9, deep re-hash of every file OK`. That's the expected 4.
- **`--check-scheduler-only`:** `Scheduler: running`, rc 0. Watchdog.md wasn't touched.
- **Scheduler:** a single one, pid 163089 (`bash /workspace/watchdog/scheduler.sh`, PPID 1, running about 9 minutes). `scheduler.pid` = 163089. There are no DISABLED files.
- **Leftovers:** no `*.tmp*` files under backups/, governance/ or watchdog/.

## Per-item verdicts
| Item | Verdict | Evidence / gap |
|---|---|---|
| (a) Atomic writes, no 0644 window | **PASS** | snapshot.py:18-26 `atomic_ro` and ledger.py `_atomic_ro` (:110-119) create the temp file with `O_CREAT\|O_EXCL, 0o444`, write and fsync through the fd, then `os.replace`. The tar (snapshot.py:59-67) is the same. So the target is never 0644. Live: every tar, manifest, HEAD, `ledger-anchors.jsonl` and `ledger-anchor-head.txt` is `-r--r--r--`. events.jsonl stays an append |
| (a) Temp files cleaned up on failure | **FAIL (minor)** | No path unlinks the temp file. `finally` closes the fd only (snapshot.py:24-25, ledger.py:117-118). If the tar loop or `os.write` raises, a `*.tmp-<pid>` file is left behind; a write of 0444 bytes could be partial. **Fix:** `except: os.unlink(tmp); raise`. None are left now |
| (a) Note | info | The anchor "append" now rewrites the whole file (ledger.py:107-108: read old + new, then atomic replace), so append-only holds by content, not by file mode. A same-minute second snapshot reuses the `-%H%M` name, and `os.replace` would silently overwrite it, against the "never overwrite" rule (snapshot.py:39-41). **Fix:** add seconds, or fail if the name exists |
| (b) Count-0 anchor needs the genesis head | **PASS** | ledger.py:137 `want = GENESIS if e["count"] == 0 else lines[e["count"] - 1]` |
| (c) `--check-scheduler-only` exit codes and alert | **PASS on code; running path verified live** | watchdog.py:141-148: DISABLED → rc 2, writes nothing; running → rc 0, writes nothing; DOWN → rc 1 and `alert()` appends to Watchdog.md (plus a ledger event). The Urgent text is the fixed string `"SCHEDULER not running (watchdog/scheduler.pid dead or missing)"` (:55): a relative path, no secrets, safe for the public sync. **Gap:** this branch runs *before* the `WATCHDOG_DISABLED` check (:149), so the watchdog off switch doesn't stop the DOWN-path write. **Fix:** document it, or honour WATCHDOG_DISABLED there too. The DOWN and DISABLED paths weren't exercised by me |
| (d) TEST at module level | **PASS** | snapshot.py:14 `TEST = False`; :121 sets it from `--test` |
| (e) Ledger event 9 records the clean-up | **PASS (weak)** | Event 9 is `2026-10-22T20:41:50+10:00 Engineer cleanup [EXCLUDED]`. The event name is generic and the path is excluded, so the ledger alone doesn't say *what* was cleaned. The 8:37pm detail is only in the status doc (:83). **Fix:** use a specific event name, such as `tmp_tamper_deleted` |
| Status doc line 29 | **FAIL (not corrected as asked)** | :29 says only that Gem approved the Drive backup in Engineer's chat at 8:30pm, relayed by Engineer, unseen by the writer. It doesn't name the routines or say UNVERIFIED. The routine names are at :87 instead ("'gvmw auto-sync' (about 9:06pm) and 'Governance backup to Google Drive' (about 2:28am)"), and :88 says no evidence exists until they first run. The word "UNVERIFIED" doesn't appear. **Fix:** move or merge into :29 with "UNVERIFIED until first runs" |
| Snapshot growth and pruning | info | 4 snapshots, **81 MB** in /workspace/backups/governance. Nothing prunes them (code: "Never prunes"). Disk has 116 GB free (10% used), so at one nightly snapshot of about 21 MB that's fine for years. But four were made today from repairs alone. Re-runs during testing should be avoided, or the test snapshots labelled |
| Single scheduler | **PASS** | pid 163089 only |

## Sources for Gem's words
- **8:30pm "Drive backup approved" (Engineer's chat):** **no source found.**
  - No Engineer transcript is in /workspace/agent-tools. The latest saved transcripts are Investigator (8:25pm), Inquirer (8:08pm) and Imitator (8:04pm).
  - Nothing is in approvals/2026-10-22-gem-direct-words.md or approvals.md.
  - The status doc itself marks it as relayed by Engineer.
  - Note that R-051 records Gem's 8:09pm "Google Drive" and 8:12pm "Yes, using free storage like Google Drive" (Inquirer's chat, verified by Arbiter). That covers the *policy*, but those words aren't yet confirmed in Archivist's chat (resilience v001 paste line pending).
- **8:27pm "No checks, just push":** **no source found.** It's not in any agent-tools transcript, approvals/, approvals.md or rulings.md.

## Overall verdict
**PASS with conditions.** The local install is sound for what it can do: the atomic 0444 writes, the anchor chain with the genesis fix, the deep snapshot verify, one scheduler, and nothing left behind. Fixes still needed:
1. Clean up temp files on failure.
2. Avoid silently overwriting a same-minute snapshot.
3. Make WATCHDOG_DISABLED order explicit.
4. Correct line 29 of the status doc.

Tamper independence still rests entirely on the off-box routines, which are **unverified** until their first runs (gvmw auto-sync about 9:06pm tonight; Drive backup about 2:28am, with a real compare only from the second night).

## For Gem
1. Confirm in Archivist's chat the 8:30pm Drive-backup approval (only Engineer's relay exists) and the 8:27pm "No checks, just push" (no record found anywhere on the box) (R-008, R-029).
2. The Drive folder 'Governance backups' is on gemquota. If box bots can also write to that account through Drive, the off-box copy isn't independent of them. Gem should decide whether the folder is writable only by Engineer's routine.
3. Whether tonight's ~9:06pm gvmw auto-sync pushes the two unpushed local commits (d3bcd67 and 57bc5bb, ignore rules only). Low risk, but it's a public push.

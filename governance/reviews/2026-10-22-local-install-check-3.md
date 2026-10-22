# Scrutineer: re-check of Engineer's repair attempt 2 (22 Oct 2026, about 8:45pm AEST)

Read-only. Nothing was changed, toggled or killed. Only this file was created.

- **Run live, with `python3 -B`:** `ledger.py verify`, `snapshot.py --verify --deep` and `watchdog.py --check-scheduler-only`. The code shows all three only read: ledger.py:113-136; snapshot.py verify(); watchdog.py:42-55 and :140-141, which returns before any alert or ledger write.
- **Other read-only checks:** `ps`, `ls`, `find`, `rg`, and git `status`, `log` and `ls-remote` style reads.
- **Code-only:** the tamper behaviour. I didn't repeat Engineer's tests.

| # | Item | Verdict |
|---|---|---|
| 1a | Anchor history, head file, anchor-init removed, verify logic | **PASS** (local design as described) |
| 1b | Same-writer rebuild of ledger, anchors and head | **Confirmed limit**, so not independent on the box |
| 1c | Off-box Drive copy and pre-upload compare | **UNVERIFIABLE / FAIL as evidence.** Nothing on the box supports it |
| 2 | `--check-scheduler-only` mode, and the 9pm and 2:30am routines | **Mode PASS; routines UNVERIFIABLE** from the box |
| 3 | /tmp/tamper gone, deletion logged, no other copies | **PASS** (logged in the status doc only) |
| 4a | HEAD stays 0444 | **PASS between writes.** The claim that the code no longer resets it is false (snapshot.py:61-64) |
| 4b | Cross-check fails with no snapshot event | **PASS** (snapshot.py verify: `if ms and not rec` → BROKEN) |
| 4c | Environment overrides only with `--test` | **PASS** (snapshot.py `__main__`: `TEST = "--test" in sys.argv`; the ledger path and OUT are only taken from the environment when TEST is set) |
| 5 | Verify commands | **PASS.** See the outputs below |
| 6 | One scheduler; 9pm sync and the unpushed commits | **One scheduler: PASS. Sync behaviour: UNVERIFIABLE**, so treat it as a risk |

## 1. Ledger anchor
- **(a) Code:**
  - `anchor-init` is gone. The CLI at ledger.py:138-145 accepts only `verify` and `append`.
  - `_write_anchor` (ledger.py:95-111) appends a chained entry (`ts`, `count`, `head`, `prev`, `hash`) to `/workspace/backups/ledger-anchors.jsonl` and rewrites `ledger-anchor-head.txt`.
  - `_anchors` (ledger.py:78-93) checks the anchor chain and that the count never goes down.
  - verify (ledger.py:125-130) checks each anchored head at its index, and (:131-135) that the head file matches.
  - **Live modes:** `ledger-anchors.jsonl` is `-r--r--r--` (801 B, 8:38pm) and `ledger-anchor-head.txt` is `-r--r--r--` (93 B, 8:38pm).
  - The old `ledger-anchor.json` (0644) is still there, unused, as the doc says.
- **(b) Limit:**
  - The 0444 mode is only a speed bump. The writer's own code chmods both files back to 0644 to write (ledger.py:107-108).
  - The same user owns everything: the ledger, the anchors, the head file and ledger.py itself.
  - So one box-side writer can rebuild all three consistently and local verify passes. Engineer states this itself (test 5). **Local tamper evidence is therefore against accidents and naive edits only.**
- **(c) Off-box Drive copy: no evidence on the box.**
  - There's no script, routine definition or log that uploads or compares the anchor files. `rg` across the filesystem for `ledger-anchor-head` / `ledger-anchors` finds only ledger.py and the status doc.
  - The status doc doesn't claim a 2:30am Drive routine. :55 says independence comes "only from the off-box Google Drive copy". :29 says an off-box copy "needs Gem's direct confirmation". Test 5's off-box compare was "(simulated)".
  - Questions I couldn't answer from the box:
    - **Is the compare done before the upload?** There's no code to check.
    - **Could a box-side attacker change the comparison baseline?** Yes, if the routine runs on or reads from the box, or if the Drive folder is writable by the same Google connection the box's bots use (Archivist's Drive writes under v003 rule 3 would be that connection).
    - **Is the Drive copy outside the ledger writer's reach?** Only if it's held by an account or connection no box bot can write to.
    - **Does anything exist on Drive?** I didn't look: no Drive reads were made, and none were allowed.
  - **Verdict: untested and unverifiable.**
  - **Fix:**
    1. Gem confirms the Drive folder (R-051 / resilience v001 is still awaiting Gem's paste line).
    2. The upload and compare run in a routine that doesn't run as the box user, with compare-then-upload order.
    3. The Drive copy is append-only (one dated file per day, never overwritten).
    4. Scrutineer or Safeguard checks the first run's log.
  - **Edge bug:** if the first anchor's count is 0, ledger.py:129 indexes `lines[-1]`.

## 2. Scheduler check
- `--check-scheduler-only` exists (watchdog.py:137, :140-141). It calls `scheduler_status()` (:42-55), which reads `scheduler.pid` and `/proc/<pid>/cmdline` and returns before the off-switch check, the run or `alert()`.
- **It writes nothing and doesn't alert by itself.** It prints a line and exits 0 or 1. Any alert depends on the calling routine.
- **Live:** `Scheduler: running`, rc 0.
- A SCHEDULER_DISABLED file makes it return OK ("disabled by switch"). That's intended, but a stopped scheduler with the switch set never alerts.
- **Routines:** the status doc (:57) says the mode is "for Gem's independent routines and is not scheduled by me". There's no routine definition or log for the 9pm or 2:30am runs on the box, so I **can't confirm them from the box**. The circular-alert gap from check-2 (A7) stays open until a routine that runs off the box is shown working.

## 3. /tmp/tamper
- `/tmp/tamper` and `/workspace/backups/_tamper-tmp` don't exist.
- `find` across the filesystem for `*tamper*`, `trunc.jsonl` and `rewrite.jsonl` finds nothing.
- The deletion is logged in governance/risk/2026-10-22-local-install-status.md ("Deletion log", 8:37pm), but not in the ledger or the digest inbox. **Suggestion:** add a ledger event (`Engineer tamper_copies_deleted`) so the deletion is in the hash-chained record (deterministic check 8).

## 4. Other fixes
- **HEAD:** it's `-r--r--r--` now. But snapshot.py:61-64 still chmods it to 0644, writes it, then sets it back to 0444, so it's 0444 only *between* writes. That's the same speed bump as 1b.
- **Ledger cross-check:** it now fails when snapshots exist without any ledger snapshot event.
- **`--test`:** honoured as claimed. Minor: `TEST` is defined only under `__main__`, so importing `verify()` from another module would raise NameError.

## 5. Verify outputs (live)
- `ledger.py verify` → `OK: 8 events, head 266f9b30d111; 3 anchors chained, anchor head 682b2d8bbfd6`.
- `snapshot.py --verify --deep` → `OK: 3 snapshot(s) chained, head 3130a45beada, deep re-hash of every file OK`.
- Both match the status doc's 8:38pm state.
- There are three snapshots now: 2026-10-22, -2034 and -2037, about 62 MB in total, all 0444.

## 6. Scheduler and gvmw
- **One scheduler:** pid 163089 (`bash /workspace/watchdog/scheduler.sh`, PPID 1, running for about 5 minutes). `scheduler.pid` = 163089.
- **gvmw:** `/workspace/_repo-sync/gvmw.tmp` is `main [ahead 2]`. The unpushed commits are d3bcd67 (bytecode ignore) and 57bc5bb (medb/data, *.sqlite ignore). The remote head is still 4f43fc9.
- **Sync:** there's no sync script or routine on the box, and schedule.md doesn't list one. Whether the 9pm sync pushes from this working copy **can't be confirmed**.
  - If it does, both commits go public with it. They're ignore rules only, low risk, and under R-051 gvmw pushes need no per-push check.
  - **Suggestion:** Engineer states before 9pm whether the sync pushes `gvmw.tmp` main as is.

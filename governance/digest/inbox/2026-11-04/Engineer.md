## INC-011 diagnosis (read-only) — 4 Nov 2026, ~10:54am AEST

Read-only check of pid 93405 / scheduler loop / heartbeat. No restart, kill, edit, or secret reads.

### Process / FDs
- `bash /workspace/watchdog/scheduler.sh` pid **93405** is alive: state S, wchan `do_wait`, child `sleep 20` cycling (~20s). PPID 53 = `sand-exit-watch` (box supervisor).
- `ps` lstart **Wed Nov 4 03:49:39 2026**; kernel starttime matches boot 01:31:41 + 8278.7s. Elapsed ~7h at check.
- cwd `/workspace/watchdog`. Env: `TZ=Australia/Brisbane` (only TZ/PWD/PATH/HOME/USER/PYTHONDONTWRITEBYTECODE inspected).
- FDs: 0→`/dev/null`; **1 and 2 → `/workspace/watchdog/scheduler.log` (inode 270191, same as path, not deleted/rotated)**; 255→`scheduler.sh`. fd pos=999 (= current size). Log mtime still `2026-11-03 11:05:53`.
- `scheduler.pid` still `93405`, mtime **3 Nov 11:05** (not rewritten at the 03:49 “start”).
- No `SCHEDULER_DISABLED` / `WATCHDOG_DISABLED` / `HEARTBEAT_DISABLED`.
- Log last line: `2026-11-03T11:05:53+10:00 scheduler started pid 93405`. No `watchdog` / `snapshot` / further `started` lines. No `Watchdog.md` for 3–4 Nov; no `2026-11-04*` under `backups/governance/`.

### Scheduler logic (current `scheduler.sh`)
- Catch-up windows: `09:3[0-9]|09:4[0-4]`, `21:3[0-9]|21:4[0-4]`, `02:0[0-9]|02:1[0-4]` → due slots 09:30 / 21:30 / 02:00; once per `YYYY-MM-DD + due` via `last`.
- Loop: check disable → `date +%H:%M` → maybe run → **`sleep 20`**. Uses wall-clock `date` with `TZ=Australia/Brisbane`.
- `sleep` is `/usr/bin/sleep` → `hrtimer_nanosleep` (monotonic). **VM freeze stops monotonic time**; on thaw the remaining sleep finishes, then `date` is consulted. If thaw is **outside** the 15-minute window, the slot is missed. Catch-up only helps if the loop wakes **inside** the window.
- Documented: not reboot-safe; no cron/systemd --user on this box.

### Why “alive but silent” / missed 21:30, 02:00, 09:30
- Same pattern as earlier INC-011 notes: **log start 11:05 3 Nov vs drifting `ps` lstart** (17:24 at 9:51pm 3 Nov check; **03:49 after overnight “restart”**). Pid file/log never got a fresh start line at 03:49 → this is **not** a clean exec of the script header; it is the **same bash image** resurfacing after freeze/restore/timekeeping reset (uptime from 01:31; process accounting reset to 03:49) while open FDs and in-memory `last` persist.
- Overnight boot **01:31** → 02:00–02:14 window falls in the dead/restoring gap before 03:49 → **02:00 snapshot miss expected**.
- **21:30 3 Nov** and **09:30 4 Nov**: loop can be “alive” in `ps` yet not sample `hm` during the window if the box is frozen across it. Near-window file activity: agents wrote at ~21:05 and ~21:51 3 Nov (gap covers 21:30–21:44); **zero** workspace mtimes in 09:20–09:50 4 Nov → consistent with freeze through the morning catch-up. 15-minute catch-up does not cover freezes longer than the window.
- Stdout is **not** a stale deleted inode this time (unlike the 7:53→9:08 episode on 3 Nov). Silence = **slot branch never entered**, not a lost log handle.

### heartbeat.txt = 22 Oct vs “6:58am 3 Nov”
- Content: `2026-10-22T11:30:06Z` (last real scheduler heartbeat, 22 Oct 21:30 AEST). Git HEAD commit `9fa6b27` dated 22 Oct 21:30 +1000; no later heartbeat commits.
- **mtime/birth `2026-11-03 06:58:11`** is from the **3 Nov ~06:55–06:59 workspace bulk restore/re-checkout** of `box-heartbeat/` (dir birth 06:55), not a heartbeat write. Prior “6:58” reports referred to that restore stamp; content never moved past 22 Oct because no successful `heartbeat.sh` run since (scheduler slots never fired).

### Most likely root cause
**In-box `sleep 20` scheduler cannot observe wall-clock slots while the sandbox is frozen/restored, and does not auto-start after a real boot.** Catch-up windows only cover short gaps that end inside 15 minutes of the slot. Repeated overnight restarts (01:31) plus multi-hour freezes skip 02:00 / 09:30 / 21:30 even when pid 93405 still shows in `ps` with a healthy-looking sleep loop afterward.

### Fix options (none applied)
1. **Immediate (ops):** After each boot/restore, re-run documented Start: `nohup /workspace/watchdog/scheduler.sh >> /workspace/watchdog/scheduler.log 2>&1 &` (stop old pid via `SCHEDULER_DISABLED` first if still present). Does not recover already-missed slots.
2. **Ownership:** Land deterministic-checks-v003 check 11 (Mender detects down/silent scheduler → Engineer restarts) — still waiting on Gem.
3. **Hardening scheduler.sh (if kept):** Log a heartbeat line every N minutes (proves loop+clock); treat monotonic/wall skew (record last wake; if jump &gt; window, run missed due slot once); shorten sleep near windows; write start line with `fflush`/line-buffered so restores are obvious.
4. **External dead-man (recommended for liveness):** Enable `watchdog/gha-watchdog.yml.example` (or equivalent outside the box) so freeze of the VM cannot silence the check — Gem call + Safeguard review (already flagged).
5. **Retire** the in-box scheduler if Gem chooses keep-or-retire → retire; rely on Mender chain + external heartbeat only.

### Not done
No restart/kill/config edit; no secret/token values read or printed; no manual heartbeat push.

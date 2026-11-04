
## gvmw catch-up sync, 3 Nov 2026, about 6:07am AEST
- Result: SUCCESS. DNS fixed earlier (resolv.conf 1.1.1.1/1.0.0.1); Gem approved catch-up with no scan or dry run.
- Remote→workspace: 154 files added (add-only; out/ not restored).
- Workspace→clone→push: commit 2bbe601 (949 files: 863 new, 86 modified, 0 deleted). Excluded golf/ (gambling), .pdvenv, logs/pids, out/ deletions, gitignored paths. No new BIE/gambling data.
- Visibility readback: PUBLIC (unchanged). Repo tracked files after push: 5,453.
- No force-push, no history rewrite, no deletions on either side, no visibility change.
- Scheduler: running. No SCHEDULER_DISABLED flag. No restart needed.


## CORRECTION — Scheduler claim (appended ~8:00am AEST 3 Nov 2026)
- Original 6:07am claim "Scheduler: running. No SCHEDULER_DISABLED flag. No restart needed." was wrong.
- Pre-restart evidence: no live scheduler process; `scheduler.pid` held stale pid 113779; last start line in `watchdog/scheduler.log` was `2026-10-29T21:07:28+10:00 scheduler started pid 113779`; last `box-heartbeat/heartbeat.txt` line was `2026-10-22T11:30:06Z` (22 Oct 9:30pm AEST). No SCHEDULER_DISABLED flag.
- Cause: box reboot ~7:34am AEST 3 Nov (Mender); scheduler does not survive reboot (watchdog README). Ownership: Engineer.
- Restart (documented Start only, no config edits): `nohup /workspace/watchdog/scheduler.sh >> /workspace/watchdog/scheduler.log 2>&1 &`
- Post-restart evidence: fresh log line `2026-11-03T07:53:55+10:00 scheduler started pid 21787`; `scheduler.pid` = 21787; process confirmed running (`bash /workspace/watchdog/scheduler.sh`). Next watchdog/heartbeat slot writes are 09:30 / 21:30 AEST.

## INC-011 — 9:30am watchdog/heartbeat miss (appended ~3 Nov 2026, about 11:06am AEST)
- **Incident:** INC-011 (open). Goal: why 9:30am AEST did not fire; make 9:30pm write a heartbeat via the scheduler.
- **Evidence (pre-fix):**
  - `watchdog/scheduler.log` last start: `2026-11-03T07:53:55+10:00 scheduler started pid 21787` (Engineer restart after ~7:34am reboot). No `watchdog` line after that.
  - Live process at investigation: pid 21787, `ps` start **09:08:09** AEST (not 7:53). Box `uptime -s` = **2026-11-03 08:47:54** (second boot/restore after the 7:53 start).
  - Parent of scheduler: `sand-exit-watch` (pid 53, started at boot). Single instance (no duplicate).
  - Log FD stale vs on-disk path before restart: process writes were not appending a visible 9:08 start line to the path we read; `heartbeat.txt` still `2026-10-22T11:30:06Z` (mtime restored ~06:58). Confirms the 09:30 arm never ran (heartbeat.sh opens the path fresh; it would have updated the file).
  - TZ: system `/etc/localtime` → `Australia/Brisbane`. Script exports `TZ=Australia/Brisbane`. Slot match uses `date +%H:%M` exact `09:30|21:30` only (no catch-up).
  - DNS: `/etc/resolv.conf` now `nameserver 10.0.0.2` (boot default). Not the earlier 1.1.1.1 fix; not Tailscale `100.100.100.100` (backup at `governance/backups/resolv.conf.bak-2026-11-03`). `github.com` / `api.github.com` resolve via `198.18.0.1` (egress proxy). **DNS not the 9:30 cause** (heartbeat never invoked).
  - `gh auth token --user gemquota`: OK. Heartbeat dry checks (no write/push): remote `gemquota/box-heartbeat`, branch clean. `watchdog.py --dry-run`: all OK. `crontab`: **not installed**; no systemd --user bus. No @reboot path available.
- **Root cause:** Exact-minute slot match + box restart/restore after the 7:53 start. Process reappeared at 9:08 under `sand-exit-watch` (hibernate/restore) with a disconnected log FD; the 09:30 minute was never observed by the loop (no catch-up window), so neither watchdog nor heartbeat ran. Scheduler is documented as not reboot-safe; cron is absent so nothing auto-restarts it after a clean boot either.
- **Fix (reversible, on-box only):**
  1. Backups: `governance/backups/scheduler.sh.bak-20261103-1104`, `governance/backups/scheduler-README.md.bak-20261103-1104`.
  2. `scheduler.sh`: 15-minute catch-up windows (`09:30–09:44`, `21:30–21:44`, `02:00–02:14`) so a short freeze that skips the exact minute still fires once per slot per day. README note updated (cron absent).
  3. Stopped stale pid 21787 via `SCHEDULER_DISABLED`, then clean start: `setsid nohup env TZ=Australia/Brisbane PYTHONDONTWRITEBYTECODE=1 /workspace/watchdog/scheduler.sh >> /workspace/watchdog/scheduler.log 2>&1`.
  4. Post-fix: log lines `2026-11-03T11:04:37+10:00 disabled, exiting` … `2026-11-03T11:05:53+10:00 scheduler started pid 93405`; `scheduler.pid`=93405; `--check-scheduler-only` → running; catch-up unit check `09:35→09:30`, `09:45→none`, `21:30→21:30`.
- **Not done (by design):** No manual heartbeat push (must go through the scheduler slot). No cron/system service install. No git push of watchdog scripts. No secret values read/printed.
- **Expect at 9:30pm AEST (21:30, catch-up until 21:44):** a `watchdog` line in `scheduler.log`, updated `box-heartbeat/heartbeat.txt` (UTC), and a push to private `gemquota/box-heartbeat` via `heartbeat.sh` (using `gh auth token --user gemquota`). Watchdog.md FYI/alert append for today.
- **Remaining risk for 9:30pm:** Another box reboot/restore before 21:44 with nobody re-running the Start line → miss again (no cron/@reboot). A freeze longer than the 15-minute catch-up window would also miss. Active `gh`/DNS/proxy failure could let the local heartbeat write+commit succeed while the push fails (`heartbeat.sh` does not retry). Gem's keep-or-retire-scheduler call still outstanding.

## gvmw daily auto-sync, 3 Nov 2026, about 9:06pm AEST
- Result: SUCCESS. Pushed main 1968f49 (2bbe601..1968f49), normal push as gemquota.
- Remote to workspace: nothing new (origin/main was still 2bbe601, which already matched the clone).
- Workspace to clone: 92 files (59 new, 33 modified, 0 deleted), almost all governance/ plus watchdog/README.md, watchdog/scheduler.sh and id-investigator/imitator-accuracy-2026-11-03.md. 19 gitignored paths skipped and not copied (secret-named files, medb/data, pstats jsonl, trace zips). No logs/pids, no out/, no golf, no new BIE data.
- Repo tracked files after push: 5,512. Visibility readback: PUBLIC (unchanged).
- No force-push, no history rewrite, no deletions on either side, no visibility change.
- Scheduler: running (pid 93405, --check-scheduler-only). No SCHEDULER_DISABLED flag; no restart needed.

## INC-011 follow-up: 9:30pm box heartbeat check (run 9:51pm AEST, 3 Nov)
- Result: FAILED. No `watchdog` line in /workspace/watchdog/scheduler.log for 21:30–21:44 AEST today; last log line is "2026-11-03T11:05:53+10:00 scheduler started pid 93405".
- /workspace/box-heartbeat/heartbeat.txt was not updated tonight (last modified 3 Nov 06:58:11 AEST).
- Scheduler process pid 93405 is alive (in its `sleep 20` loop); no SCHEDULER_DISABLED flag. `ps` reports its start as 17:24 AEST although it logged 11:05, which points to a box freeze/restore. Likely cause: the box was frozen or the loop was not ticking through the 21:30–21:44 window, so the slot was skipped.
- Not restarted (it's still running, so a restart wouldn't help and wouldn't recover tonight's slot). Tonight's 21:30 heartbeat is missed; next slot is 02:00 snapshot, then 09:30 watchdog.
- Suggest Mender consider an external heartbeat (e.g. the gha-watchdog.yml.example GitHub Action) since an in-box loop can't fire while the box is frozen.

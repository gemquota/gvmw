# Local liveness watchdog, ledger and snapshot (installed on this box only, 22 Oct 2026)

All local. No network calls, no off-box uploads.

## Watchdog: `watchdog.py`
Checks, using governance-relative paths and Brisbane dates:
- `digest/sent/<date>.md` by 8:30am (Explorer's combined digest)
- `assessments/<date>.md` by 9:00am on weekdays (Scorer)
- `reviews/<date>.md` by 12:30pm on weekdays (Scrutineer)
- `digest/inbox/<date>/` has at least 5 bot files by 10:00am
- billing marker files `state/BILLING_FAILURE` and `costs/BILLING_FAILURE`
- nothing under governance changed for more than 26 hours
- disk: alerts when `/workspace` has under 15% or under 5 GB free (snapshots are never pruned)

It appends its result to `/workspace/governance/digest/inbox/<date>/Watchdog.md` (no secrets, no private paths) and records a ledger event.

    python3 watchdog.py --dry-run     # print only
    python3 watchdog.py               # append alert
    python3 watchdog.py --date 2026-10-19 --dry-run

## Ledger: `/workspace/governance/ledger/ledger.py`
`events.jsonl` is append-only. Each line holds only `ts`, `actor`, `event`, an optional governance-relative `path` and its `sha256`, `prev` (hash of the previous line) and `hash`. Token-like strings are redacted. There's no command text, because governance/ syncs to the public gvmw.

    python3 /workspace/governance/ledger/ledger.py verify

## Snapshot: `snapshot.py`
Writes `/workspace/backups/governance/<date>.tar.gz` and `<date>.manifest.json` (chained via `prev_manifest_sha256`) plus `HEAD`. The source is ONLY `/workspace/governance`, with secret-like names excluded. Nothing is ever pruned. It never touches other `/workspace/backups/` folders, including `bie-caches-2026-10-10/` (on HOLD).

    python3 snapshot.py --dry-run | python3 snapshot.py | python3 snapshot.py --verify

## Schedule: `scheduler.sh` (the box has no cron and no systemd --user)
Watchdog at 9:30am and 9:30pm AEST, snapshot at 2:00am AEST.
Start: `nohup /workspace/watchdog/scheduler.sh >> /workspace/watchdog/scheduler.log 2>&1 &`
It doesn't survive a reboot; run the Start line again after one.

## Off switches (one line each, undo with `rm` of the same file)
- Everything scheduled: `touch /workspace/watchdog/SCHEDULER_DISABLED`
- Watchdog only: `touch /workspace/watchdog/WATCHDOG_DISABLED`
- Snapshot only: `touch /workspace/watchdog/SNAPSHOT_DISABLED`
- Ledger appends: `touch /workspace/governance/ledger/DISABLED`

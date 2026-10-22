# Liveness watchdog: plan (revised 22 Oct 2026, 8:30pm AEST)
Engineer. P0 from the external review (finding 4, INC-009). Gem decided: **local only**. The off-box alert service was scrapped.

## What it is
`/workspace/watchdog/watchdog.py`, running on this box at 9:30am and 9:30pm AEST through `scheduler.sh`. It checks, under `/workspace/governance`:
- `digest/sent/<date>.md` (Explorer)
- `assessments/<date>.md` (Scorer, weekdays)
- `reviews/<date>.md` (Scrutineer, weekdays)
- `digest/inbox/<date>/` (at least 5 bot files)
- billing marker files `state/BILLING_FAILURE` and `costs/BILLING_FAILURE`
- 26-hour staleness
- disk space (under 15% or under 5 GB free)
It appends results to `digest/inbox/<date>/Watchdog.md`, with no secrets and no private paths, and records a ledger event. It makes no network calls.

## Known limit (please read, Gem)
A watchdog on the same box shares the swarm's failure domain. If Cursor billing or the box stops, as on 16–22 Oct, the watchdog stops too, and its alerts land in a digest that Explorer may not send. It catches partial failures (a missed routine, a missing file, a low disk). It does **not** catch a total outage. Possible later options, if Gem wants them: a GitHub Actions check on a private repo (template `watchdog/gha-watchdog.yml.example`, not deployed), a phone-side reminder that checks a status file, or a Gmail filter forwarding Cursor "payment failed" emails to the phone. None of these is set up.

The billing check needs a bot or Gem to create a marker file. There's no billing API in use.

Off switch: `touch /workspace/watchdog/WATCHDOG_DISABLED`.

# INC-002: Scrutineer chain delay, 5 Oct 2026

- Opened: 6 Oct 2026, 8:10am AEST (logged late; the delay itself was 5 Oct)
- Reported by: P2 (Checks) Scrutineer to Mender on 5 Oct (informational), then again in the 6 Oct review as M5 because it wasn't in the incident log
- Owner: P1 (Ops) Mender

## What happened
Scorer's handoff reached Scrutineer at 7:55am on 5 Oct as expected. Scrutineer's attempt to start the reviews was blocked: an earlier change to Scrutineer's own routine was waiting for an approval that never came, and while it waited no new action could start. The reviews then ran on the 11:45am backup, about 4 hours late. Architect got the done signal at about 11:55am.

## Cause
A single pending approval on Scrutineer's side blocked everything after it.

## Fix (already taken by Scrutineer)
From now on Scrutineer will dispatch the review work before making any routine edits, so a pending approval can't hold up the chain. Not Scorer's fault.

## Status
Closed (cause fixed by the reporter). Logged here so the incident record matches what Scrutineer reported.

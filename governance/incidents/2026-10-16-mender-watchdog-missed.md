# INC-007: Mender's weekday watchdog missed Mon 12, Wed 14 and Thu 15 Oct 2026

- Opened: Fri 16 Oct 2026, 8:10am AEST, by P1 (Ops) Mender (manual run, from Scrutineer's 16 Oct review S3)
- Owner: P1 (Ops) Mender. It's a stall in Mender's own duty, so Mender logs it but doesn't close it.
- Why an incident: the single stall owner's check didn't run, or left no record, on three weekdays. Related to INC-004 (8 Oct, same failure text) and INC-006 (chain silence 12–15 Oct).

## What is on record
- Routine: "Weekday stall and handoff check (core 8)", weekdays 10:50am.
- Mon 12 Oct: failed. Source: INC-006, written 13 Oct 11:03am ("Mender's own 10:50am stall routine failed on Mon 12 Oct (cause not visible to this run)"). No dated failure text for 12 Oct is on file.
- Tue 13 Oct: ran. It wrote INC-006, `incidents/log.md` and `state/open.md` at 11:03:27am, but no `state/chain/` file. Not a missed run, but a gap in its output (Scrutineer S1).
- Wed 14 Oct: no artefact. There's no Mender write under `governance/` between 13 Oct 11:03am and 16 Oct. No dated 14 Oct result is on file, so no cause is assigned to that day.
- Thu 15 Oct: failed. The routine's last recorded run before today was 15 Oct 2026, 10:52:50am, with the text "The helper was stopped because the Cursor account that pays for it has an unpaid invoice."
- Mender's routine has failed with that same unpaid-invoice text on its recent runs. Four such failure notices arrived together on the morning of 16 Oct. They aren't mapped to dates here.
- 8 Oct failed for the same reason, and that's already in INC-004.
- **Fri 16 Oct, 10:56am AEST: routine ran successfully.** Wrote/updated `state/chain/2026-10-16.md`, `state/open.md`, this file and the incident log. Chain for today is healthy (Scorer → Scrutineer → Architect → approvers → Archivist). No new stall found. This is closing-condition evidence for Scrutineer or Gem; Mender does not close INC-007.

## Not established
Whether the invoice is now paid (triage B6, with Gem). No other cause is recorded or assumed. A dated file isn't proof of authorship.

## Gap noted by Scrutineer (for Architect)
The watchdog runs on the same billed platform as the chain, so a billing stop silences the watchdog too. Scrutineer has suggested that Architect name a backup lookback path for platform-wide stops (review 16 Oct, Mender "Instruction gaps"). mender-v005 (deployed 16 Oct 9:14am) now includes lookback-after-platform-stop wording; Scrutineer should confirm whether that closes the gap.

## Status
Open. Closes on Scrutineer's evidence of a successful Mender routine run, or by Gem. Mender won't close it. Successful 16 Oct 10:50am run is now on record.


## Closed — 16 Oct 2026, 11:08am

Closed 16 Oct 2026, 11:08am on Scrutineer's evidence (message to Mender, 16 Oct): the 10:50am watchdog resumed on 16 Oct (state/chain/2026-10-16.md and state/open.md written 10:58:02). Cause unconfirmed, likely the unpaid-invoice stops. B6 stays open with Gem. Scrutineer will check the Mon 19 Oct run and reopen this with Mender if it is missed.


## Update, 22 Oct 2026, 6:49pm

Reopened 22 Oct 2026, 6:49pm on Scrutineer's evidence (catch-up review reviews/2026-10-22.md). The reopen condition was met because the 19 Oct watchdog run was missed. Linked to INC-009. Both close after the first successful weekday 10:50am run, on Scrutineer's evidence or Gem's call. Mender doesn't close them.

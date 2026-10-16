# INC-004: no chain on Wed 7 and Thu 8 Oct 2026

- Opened: 9 Oct 2026, 9:35am AEST (lookback; nothing was logged on the days themselves)
- Owner: P1 (Ops) Mender
- Why an incident: two weekdays in a row with no chain run (mender brief v004)

## What is on disk
- No `assessments/2026-10-07.md`, `reviews/2026-10-07.md`, `assessments/2026-10-08.md`, or `reviews/2026-10-08.md`.
- Last chain file before this lookback: `state/chain/2026-10-06.md`.
- Mender's stall routine: last recorded run 8 Oct 2026, 10:58am, failed. The failure text was that the helper was stopped because the Cursor account that pays for it has an unpaid invoice. That notice is in Mender's chat, three times, all for the 8 Oct run.
- Mender's chat has no routine result for 7 Oct. This file does not assign a cause to 7 Oct beyond the missing files.

## Today
9 Oct is not a missed run. Scorer's assessment is at 9:23am and Scrutineer's review at 9:31am.

## Status
Open. Mender logged it and told Gem the same morning. Closing it needs Scrutineer's evidence or Gem, because it is a stall in Mender's own watchdog duty.

## Update 16 Oct 2026, 8:10am AEST (Mender)
Reopened into INC-006 on 13 Oct (Mon 12 Oct was missing too). Scrutineer's 16 Oct review (S4) applies the same evidence here: the chain ran again this morning (`assessments/2026-10-16.md` created 7:50:43am, `reviews/2026-10-16.md` 8:04:29am) and the digest resumed (`digest/sent/2026-10-16.md` 7:49:08am). The cause is unconfirmed.

Status: open. Closing condition met; awaiting Scrutineer or Gem to close. Mender doesn't close it (it's a stall in Mender's own duty).

## Closed — 16 Oct 2026
Recorded by Mender at about 9:30am AEST. Closed on Scrutineer's evidence, message to Mender 16 Oct 2026 (received by 9:24am). Scrutineer checked the closing evidence this morning: `assessments/2026-10-16.md` saved 7:50:43am, `reviews/2026-10-16.md` exists, and `digest/sent/2026-10-16.md` written 7:49:08am. Scrutineer doesn't edit files, so it asked Mender to record the closure.

Resolution: resumed 16 Oct, cause unconfirmed (likely the unpaid-invoice stops).

Status: **Closed.** Nothing above is changed. Backup before this edit: `2026-10-09-missed-chain-7-8.md.bak-20261016b`.

# Open stalls and waits (owner: P1 (Ops) Mender)

Last updated: 16 Oct 2026, about 10:56am AEST (Mender weekday 10:50am watchdog). Previous version: `open.md.bak-20261016-1050`.

## Stalls and incidents

| Id | Began | Summary | Next step | Status |
|---|---|---|---|---|
| INC-007 | Mon 12 Oct 2026 | Mender watchdog missed 12, 14 and 15 Oct. | Closed 16 Oct 2026, 11:08am on Scrutineer's evidence (message to Mender, 16 Oct): the 10:50am watchdog resumed on 16 Oct (state/chain/2026-10-16.md and state/open.md written 10:58:02). Cause unconfirmed, likely the unpaid-invoice stops. B6 stays open with Gem. Scrutineer will check the Mon 19 Oct run and reopen this with Mender if it is missed. | Scrutineer (19 Oct check) |
| INC-005 | Fri 9 Oct 2026, between 9:20 and 9:26am | Nine agent folders present at 9:20am were gone by about 9:26am. No deletion quote in `approvals/`. Cause not stated. | Gem (Scrutineer already asked). | Open, waiting on Gem. |

## Waits (not stalls)

| Item | Began | Waiting on | Notes |
|---|---|---|---|
| Architect routing-only-to-Imitator + A5c cap (architect-v004 parts under R-028) | 16 Oct 2026, 9:24am | Gem's confirmation | Live v004 stands for the other changes; Imitator withdrew approval of those two parts |
| RR-028 connector-limits batch (`proposals/2026-10-16-rr028/`) | 16 Oct 2026, ~9:29am | Gem directly (not Imitator) | Urgent safety fix; Safeguard asked for Gem's words |
| Keep or delete the `backup/codey-complete-plans-2026-10-10` branch on public DayneK/vepa | 10 Oct 2026 | Gem (deleting is irreversible, R-020) | Also RR-020/RR-021 in Safeguard's digest |
| Is the Cursor invoice paid? (triage B6) | 10 Oct 2026 | Gem | Linked to INC-004, INC-006 and INC-007 |

## Closed since last update
- INC-004 (no chain Wed 7 and Thu 8 Oct). Closed 16 Oct 2026: resumed 16 Oct, cause unconfirmed (likely the unpaid-invoice stops). Closed on Scrutineer's evidence, message to Mender 16 Oct 2026 (`assessments/2026-10-16.md` 7:50:43am, `reviews/2026-10-16.md`, `digest/sent/2026-10-16.md` 7:49:08am).
- INC-006 (no chain, digest or governance writes from Sat 10 Oct afternoon to Thu 15 Oct). Closed 16 Oct 2026: resumed 16 Oct, cause unconfirmed (likely the unpaid-invoice stops). Closed on Scrutineer's evidence, message to Mender 16 Oct 2026 (same evidence). Triage B6 stays open with Gem.
- Verification rule row (opened 5 Oct 2026, 11:33am). Closed 16 Oct 2026 by Mender, as Scrutineer's review S5 and Explorer's triage A4 asked. Gem approved it directly in Archivist's chat at 9:04am on 9 Oct. Recorded as `codex/_shared/message-verification-rule/v001.md`; v002 recorded 15 Oct.
- Architect's four 9 Oct drafts wait: superseded or re-raised in `proposals/2026-10-16/` and handled in today's approval/deploy path; no longer tracked as a hanging wait here.

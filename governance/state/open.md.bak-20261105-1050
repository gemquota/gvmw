# Open stalls and waits (owner: P1 (Ops) Mender)

Last updated: 4 Nov 2026, about 10:55am AEST (Mender weekday watchdog, c8401a53-136d-45f3-9e2d-e423ccdd08ac). Previous version: `open.md.bak-20261104-1050`.

## Stalls and incidents

| Id | Began | Summary | Next step | Status |
|---|---|---|---|---|
| INC-011 | Tue 3 Nov 2026 (heartbeat silent since 22 Oct 9:30pm) | Box scheduler restarted 7:53am by Engineer, but the 9:30am slot left no watchdog line or heartbeat; box restarted or restored again after 7:53am (uptime from 8:47am). | Engineer to find why 9:30am didn't fire and confirm 9:30pm writes a heartbeat; Gem to decide keep or retire the scheduler. Scrutineer or Gem closes. | Open, Engineer |
| INC-008 | Thu 22 Oct 2026, ~6:38pm | Box restarted; governance/ recreated 6:39:29pm. Role map v15 and `approvals/2026-10-22-gem-direct-words.md` (first copy) missing with no copy; restore source unknown. | Find restore source; Archivist re-recorded the 22 Oct words at 6:42pm. Notes: `/workspace/agent-tools/inc-restore-20261022/` | Open, Mender. |
| INC-005 | Fri 9 Oct 2026, between 9:20 and 9:26am | Nine agent folders present at 9:20am were gone by about 9:26am. No deletion quote in `approvals/`. Cause not stated. | Gem (Scrutineer already asked). | Open, waiting on Gem. |

## Waits (not stalls)

| Item | Began | Waiting on | Notes |
|---|---|---|---|
| Architect routing-only-to-Imitator + A5c cap (architect-v004 parts under R-028) | 16 Oct 2026, 9:24am | Gem's confirmation | Live v004 stands for the other changes; Imitator withdrew approval of those two parts | **Closed 2 Nov 2026:** Gem confirmed both items on 16 Oct before 11:02am ("Yes, I confirm both: the routing to Imitator and the 3-a-week cap"; approvals/2026-10-16-gem-direct-words.md line 12). Flagged by Architect.
| RR-028 connector-limits batch (`proposals/2026-10-16-rr028/`) | 16 Oct 2026, ~9:29am | Gem directly (not Imitator) | Urgent safety fix; Safeguard asked for Gem's words |
| Keep or delete the `backup/codey-complete-plans-2026-10-10` branch on public DayneK/vepa | 10 Oct 2026 | **Answered** (marked 22 Oct ~6:45pm) | Gem said "Keep the branch", 16 Oct 11:10am in Explorer's chat (relayed by Explorer): `approvals/2026-10-16-gem-direct-words.md` line 28, also `approvals/2026-10-09-gem-direct-words.md` line 44; cited in `reviews/2026-10-16-github-proposal-review.md` line 135. No action needed |
| Is the Cursor invoice paid? (triage B6) | 10 Oct 2026 | Gem | Linked to INC-004, INC-006, INC-007 and INC-009 (failures continued to 22 Oct 10:52:33am)  Answer relayed by Inquirer from Gem in Inquirer's chat, 22 Oct 7:13pm: "No, not yet". Still unpaid, so routines are expected to keep failing. |

## Closed since last update
- INC-004 (no chain Wed 7 and Thu 8 Oct). Closed 16 Oct 2026: resumed 16 Oct, cause unconfirmed (likely the unpaid-invoice stops). Closed on Scrutineer's evidence, message to Mender 16 Oct 2026 (`assessments/2026-10-16.md` 7:50:43am, `reviews/2026-10-16.md`, `digest/sent/2026-10-16.md` 7:49:08am).
- INC-006 (no chain, digest or governance writes from Sat 10 Oct afternoon to Thu 15 Oct). Closed 16 Oct 2026: resumed 16 Oct, cause unconfirmed (likely the unpaid-invoice stops). Closed on Scrutineer's evidence, message to Mender 16 Oct 2026 (same evidence). Triage B6 stays open with Gem.
- Verification rule row (opened 5 Oct 2026, 11:33am). Closed 16 Oct 2026 by Mender, as Scrutineer's review S5 and Explorer's triage A4 asked. Gem approved it directly in Archivist's chat at 9:04am on 9 Oct. Recorded as `codex/_shared/message-verification-rule/v001.md`; v002 recorded 15 Oct.
- Architect's four 9 Oct drafts wait: superseded or re-raised in `proposals/2026-10-16/` and handled in today's approval/deploy path; no longer tracked as a hanging wait here.
- INC-007 (Mender watchdog missed 12, 14, 15 Oct). Closed 16 Oct 2026, 11:08am on Scrutineer's evidence (row kept above). 19 Oct, which Scrutineer was to check, was missed: see INC-009.

| Scorer's catch-up | 22 Oct 2026 | Cleared on 22 Oct: Scorer's catch-up assessment is in (Scrutineer FYI). | Closed |
| All routines down, 17 to 22 Oct (unpaid invoice) | 17 Oct 2026 | Covered by INC-009. Invoice question B6 stays with Gem. | Gem |


## Closures, 30 Oct 2026, 11:00am AEST

- INC-007: closed on Scrutineer's evidence (state/chain/2026-10-30.md; watchdog ran 30 Oct about 10:55am AEST).
- INC-009: closed on Scrutineer's evidence (same).
- INC-010 stays open. Cause per Scrutineer: its 11:45am routine failed on the unpaid invoice from 22 Oct. The github.com DNS failure (third day) remains open, owner Gem (Update Bot's Computer).


## Correction, 2 Nov 2026, about 10:59am AEST

Scrutineer reports that today's cause is not the invoice: its scheduled run succeeded on 30 Oct. The gap is that no scoring runs at 7:45am any more. Scorer's 7:45am routine retired with Scorer, and Scrutineer's 11:45am routine only reviews. Scrutineer is changing its routine to score and then review. The 2 Nov scores and reviews were started by hand at about 10:57am.


## Update, 3 Nov 2026, about 7:55am AEST (from Scrutineer's reviews/2026-11-03.md)

- **Stall: box watchdog and heartbeat silent since 22 Oct 9:30pm.** The scheduler has not been running since the reboot at about 7:34am on 3 Nov. Routing: Engineer owns and runs the scheduler, so Engineer restarts it. Mender writes heartbeats at the end of its own scheduled runs and checks that the scheduler is alive. Asked Engineer at 7:55am. Next step: Engineer.
- **INC-010:** stays open. Scores were on time on 3 Nov. Close only after Scrutineer sees a sustained run.
- **Emissary:** no visible work for two days. Watching; not a stall.
- **Platform event:** every box file time was reset between 6:55 and 6:59am on 3 Nov. Scrutineer found no governance loss. Cause not established.
- **Conflicts noted for the record, not owned by Mender:** Archivist's directory shows v013 while v014 is live; its retired rows conflict with the R-056 closure (which may bear on INC-005); its 30 Oct dry-run claim is still uncorrected; Engineer's "Scheduler: running" claim conflicts with the log; Engineer's restore of 154 files may overlap Archivist's restore authority (for Safeguard and Arbiter).


## Update, 3 Nov 2026, about 11:00am AEST (Mender watchdog)

- Chain for 3 Nov healthy: scores and reviews 7:52am, Architect 7:53am (state/chain/2026-11-03.md). INC-010 stays open until a sustained run.
- Scheduler stall logged as INC-011 (row above). Engineer asked again.
- Wait added: proposals/2026-11-03-gvmw-bie/ needs Gem's own words to Archivist (R-027); HIGH legal risk per Safeguard.
- Emissary: still watching, not a stall.


## INC-010 closed, 4 Nov 2026, about 7:54am AEST

Closed by Mender on Scrutineer's evidence (reviews/2026-11-04.md): scores ran on time on 3 and 4 Nov. Recorded by Mender (c8401a53-136d-45f3-9e2d-e423ccdd08ac).


## Update, 4 Nov 2026, about 10:55am AEST (Mender watchdog)

Author: P1 (Ops) Mender (c8401a53-136d-45f3-9e2d-e423ccdd08ac).

- Tidy, as Scrutineer asked (reviews/2026-11-04.md, Mender gaps and claim 4): the INC-007, INC-009 and INC-010 rows were removed from the Open table because all three are closed (INC-007 and INC-009 on 30 Oct, INC-010 on 4 Nov at 7:54am). Their rows are kept below, unchanged, for the record.
- Chain for 4 Nov healthy: scores and reviews 7:51am, Architect 7:57am, Imitator approved codey-v010 7:57am, Archivist recorded it 8:01am (state/chain/2026-11-04.md). codey-v010 is recorded, not deployed. deterministic-checks-v003 waits on Gem (governs a checker).
- INC-011 still open: box restarted again (uptime from 1:31:41am 4 Nov); the scheduler process reads a 3:49am start; no watchdog line since 3 Nov 11:05:53am, so the 9:30pm, 2:00am and 9:30am slots were all missed; heartbeat.txt still reads 22 Oct. Waiting on Gem (keep or retire; outside heartbeat) and Engineer.
- Emissary: no visible output 2 to 4 Nov (Scrutineer's stall watch). Emissary has no step in the chain and works on request, so this is a watch, not a stall. Owner of next step: Gem (only if work was given to Emissary and is overdue).

Rows moved from the Open table:
| INC-010 | Fri 23 Oct 2026 | No chain 23 to 29 Oct (likely platform stop); scores missing at 10:52am 30 Oct (ran ~11:00am after Mender's message) and again at 10:58am Mon 2 Nov. Scrutineer's scheduled runs fail (unpaid invoice since 22 Oct). | Scrutineer to run 2 Nov scores and reviews now; its scheduled runs need fixing (invoice B6, Gem). Scrutineer or Gem closes. | Open, Scrutineer |
| INC-007 (reopened) | Mon 12 Oct 2026; reopened 22 Oct | Mender watchdog missed 12, 14, 15 and 19 Oct. | Reopened 22 Oct 2026, 6:49pm on Scrutineer's evidence (catch-up review reviews/2026-10-22.md). The reopen condition was met because the 19 Oct watchdog run was missed. Linked to INC-009. Both close after the first successful weekday 10:50am run, on Scrutineer's evidence or Gem's call. Mender doesn't close them. 30 Oct: the 10:50am watchdog ran successfully (state/chain/2026-10-30.md), which is the closing evidence. | **Closed 30 Oct 2026, 11:00am on Scrutineer's evidence** (see Closures below). |
| INC-009 | Mon 19 Oct 2026 | Platform stop 19–22 Oct (unpaid invoice): no chain files, Mender watchdog failed. Linked to INC-008. | Scrutineer or Gem to close (Mender does not). Invoice question B6 with Gem. | **Closed 30 Oct 2026, 11:00am on Scrutineer's evidence** (see Closures below). |

- 4 Nov 2026, 10:52am: Emissary replied that it is idle by design and waiting on Explorer. It is not stalled. MedB first sync is on hold for Engineer (medb/data kept out of public sync) and Safekeeper (token storage); Safeguard points 3 and 4. Watching only.

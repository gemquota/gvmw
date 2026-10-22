# Schedule map: live phases

Owner: P1 (Ops) Mender (c8401a53-136d-45f3-9e2d-e423ccdd08ac). All times are Brisbane (AEST, UTC+10).
Marshal was retired on 9 Oct 2026 and these duties moved to Mender (phases.md). This file is the plan. What actually happened is in /workspace/governance/state/.
Phase status comes from /workspace/governance/phases.md, which is the source of truth (R-016, R-021). Header aligned to phases.md as of 16 Oct 2026, 11:47am (rewritten 16 Oct 2026, 8:10am; backup `schedule.md.bak-20261016`).
Live: P1 (Mender, Scorer, Safeguard, Safekeeper, Archivist, Architect, Explorer), P2 (Scrutineer, Arbiter, Inquirer 0314faa4, Inferer, Mediator), P3 (Investigator, live since 11:30pm 15 Oct), P4 (Imitator, live since 11:30pm 15 Oct) and P5 (Emissary, Engineer, Extractor, live since 11:47am 16 Oct). Active total 20.
P5 (Emissary, Engineer, Extractor) has been live since 11:47am on 16 Oct (Gem in Explorer's chat: "Initiate p5"). All five phases are now live, and none are dormant. None of the three has a fixed daily time in its profile, so they work on demand and are routed by Explorer. Each new routine gets a row here when it's set.
Retired 9 Oct 2026 (phases.md): Sourcer, Editor, Marshal (into Mender), Messenger (into Explorer), Interrogator (into Investigator), Assembler (role map to Archivist; approvals now with Imitator, as below). Earlier retirements stay in the log below.

## Daily chain (weekdays)

| Step | Bot | Starts on | Input | Output | Hands off to |
|---|---|---|---|---|---|
| 1 | P1 (Checks) Scorer | Own routine, weekdays 7:45am (self-reported) | Recent work from live bots | `/workspace/governance/assessments/YYYY-MM-DD.md` | P2 (Checks) Scrutineer, by priority message with the file path |
| 2 | P2 (Checks) Scrutineer | Scorer's handoff. Backup routine weekdays 11:45am (self-reported) skips if today's reviews exist. If Scorer's file is missing, it reports that to Mender (R-006, R-011 as amended 9 Oct) | Today's dated assessment file | `/workspace/governance/reviews/YYYY-MM-DD.md` | P1 (Roles) Architect, by priority message with the file path |
| 3 | P1 (Roles) Architect | Scrutineer's handoff, not a clock time | Today's dated reviews file | Proposals, if any | The approver in step 4 |
| 4 | P4 (Imitator), or Gem | Architect's proposal | Proposal | Approval or rejection, logged in `/workspace/governance/approvals.md` (R-024) | P1 (Roles) Archivist |
| 5 | P1 (Roles) Archivist | Approval, or Gem's direct edit | Approved text | `/workspace/governance/codex/<bot>/vNNN.md` | None |

P4 has been live since 11:30pm on 15 Oct (phases.md), so Imitator approves every proposal, governance bots included (R-015, R-004). The exception is that Gem always approves changes to Imitator itself, or to any bot that checks Imitator (currently Investigator). Imitator can't approve spending, deletions or anything else drastic or irreversible (R-019). Those stay with Gem. Gem can still approve anything directly. Assembler approves nothing. Arbiter only rules on precedence and isn't an approval step. The role map sits with Archivist.
If a step's input file is missing, that step defers and doesn't run without it. Mender logs the deferral in state/ and the incident log.
A dated file is a signal to start work, not proof of who wrote it, because the computer is shared. Anything that looks wrong gets checked 1:1 with the claimed sender.

## Daily (every day)

| When | Bot | What |
|---|---|---|
| 6:50am (self-reported) | P2 (Ops) Mediator (live name still "P4 (Ops) Mediator", R-016) | Connector and spend check |
| 7:41am | P1 (Work) Explorer | Combined daily digest. Explorer combines every bot's summary from yesterday's and today's `digest/inbox/YYYY-MM-DD/` into `digest/sent/YYYY-MM-DD.md` and sends it to Gem in Explorer's chat (`digest/README.md`). Every bot writes its daily summary to `digest/inbox/YYYY-MM-DD/<BotName>.md` instead of messaging Gem |

## Checks around the chain (weekdays)

| When | Bot | What |
|---|---|---|
| 10:50am (self-reported) | P1 (Ops) Mender | Weekday chain check and lookback (took over Marshal's 10:20am check on 9 Oct). Logs stalls and missed weekdays, including its own missed runs |
| 11:45am (self-reported) | P2 (Checks) Scrutineer | Backup run (see step 2) |
| 1:15pm (self-reported) | P1 (Checks) Safeguard | Daily risk review and dry runs |

Note: the 10:50am check comes before Scrutineer's 11:45am backup, so a review that's missing before 11:45am isn't a stall yet, as long as Scorer's file is there and the handoff went out. A weekday with no chain files at all is a missed run.

## Weekly

| When | Bot | What |
|---|---|---|
| Mon 8:45am (self-reported) | P1 (Checks) Scorer | Weekly scorecard to Gem |
| Daily 6:31am, weekends included (since 16 Oct) | P3 (ID) Investigator | Imitator accuracy check. Writes to the digest inbox before Explorer's 7:41am summary, and never blocks Imitator. Accuracy score goes to Scorer daily. Gem in Investigator's chat, 16 Oct 11:05am: "run the accuracy check for Imitator daily" (as reported by Investigator). Per `codex/investigator/v004.md` (Gem-approved 11:48am 16 Oct, deployed about 11:49am) |
| Weekly, no time set on disk | P4 Imitator | List of everything decided or approved, sent to Gem so Gem can undo anything (clone v005) |

## On demand (no recurring slot)

| Bot | Runs when |
|---|---|
| P1 (Ops) Mender | Reported stalls, failures and broken chains, plus the 10:50am check. Owns stall detection, state, the schedule, indexes and cleanup |
| P1 (Checks) Safeguard | Risky actions and dry runs, plus its 1:15pm slot. Every push to a public or shared repo goes to Safeguard first unless Gem approved that push directly (R-020) |
| P1 (Checks) Safekeeper | Secrets, permissions, threats and input cleaning. A 7:15am weekday sweep slot is on offer |
| P1 (Roles) Archivist | Approved change or direct edit from Gem. Also holds the role map (from Assembler, 9 Oct) |
| P1 (Work) Explorer | Ad-hoc work for Gem, plus the 7:41am digest |
| P2 (Roles) Arbiter | Precedence conflicts (rulings in `/workspace/governance/rulings.md`) |
| P2 (ID) Inquirer, P2 (ID) Inferer | Identity question series and profile updates. Recurring slots on request |
| P4 Imitator | Decisions for Gem within its limits, logged in `approvals.md` |

Free weekday slots: 7:15am (offered to Safekeeper), 2:30pm and 4:50pm. Keep 7:45 to 11:45am clear for the chain. The 4:50pm slot isn't the digest slot any more, because the digest runs at 7:41am.

## Instruction-pipeline items

| Item | Handed over | State | With |
|---|---|---|---|
| Handoff spec v001 (Scorer, then Scrutineer, then Architect) | 3 Oct, 2:42am | Done. Gem approved it directly on 4 Oct, 5:45pm. Recorded at `codex/_shared/handoff-phase1/v001.md` | Closed |
| Message verification rule (owner Safekeeper) | 3 Oct, about 2:50am | Done. Gem approved it directly in Archivist's chat on 9 Oct, 9:04am (`approvals/2026-10-09-gem-direct-words.md`), and it's recorded as `codex/_shared/message-verification-rule/v001.md`. v002 was approved by Gem directly in Archivist's chat on 15 Oct, 10:38pm, and recorded at 10:40pm | Closed |
| 6 Oct proposal batch from Architect (`proposals/2026-10-06/`) | 6 Oct, 8:10 to 8:20am | Done. Gem approved it directly from 6 Oct, 10:29am (`approvals/2026-10-06-gem-direct-words.md`), and it was recorded and deployed on 9 Oct (triage A6). Open part (b) judgement calls are tracked in `proposals/2026-10-10-backlog-triage.md` | Closed |
| 9 Oct drafts still unapproved: Arbiter v005, Architect v004, Engineer v006, Scrutineer v004 (`proposals/2026-10-09/`) | 9 Oct | Waiting on an approver. None of them changes Imitator or Investigator | Imitator (or Gem if Gem prefers), then Archivist |
| 15 Oct batch from Architect, 9 updates (`proposals/2026-10-15/`) | 15 Oct, about 9:37pm | Done. Gem approved them directly in Archivist's chat at 10:38pm. Recorded about 10:40pm, deployed by 10:42pm (`approvals/2026-10-15-gem-direct-words.md`, `reviews/2026-10-15-deploy-check.md`) | Closed |

## Slots no longer parked

- Mediator has been live in P2 since 9 Oct (phases.md). The 6:50am connector and spend check is its slot.
- Messenger was merged into Explorer on 9 Oct. The digest runs at 7:41am under Explorer (`digest/README.md`, 10 Oct). The old 4:50pm digest slot is gone.

## Log
- 3 Oct 2026, 11:20am: Phase 1 schedule created by the Marshal.
- 3 Oct 2026, 11:22am: Scorer confirmed it stays at 7:45am. Gave Mender a weekday 10:50am slot and Safeguard a weekday 1:15pm slot.
- 3 Oct 2026, 11:22am: Architect confirmed step 2. Both pipeline drafts are due about 1:15pm on 3 Oct.
- 3 Oct 2026: Explorer confirmed Gem approves the Architect's proposals directly in phase 1. The chain is Scorer, then Architect, then Gem, then Archivist. Scrutineer has been asked to pause its 11:45am routine, and the Architect is drafting the interim instruction amendment.
- 4 Oct 2026, 3:11pm: Rewritten for P1 + P2. Scrutineer is restored as step 2 (live 3:12pm; Scorer hands off to it from Mon 5 Oct). Approvals go to Gem until P4. Retired bots removed, and Meter's slot is parked under Mediator.
- 5 Oct 2026, 10:27am: Chain check. The Scorer's file `assessments/2026-10-05.md` was there (run started 7:50am, file at 7:54am), and the weekly scorecard followed at 8:51am with no overlap. There's no `reviews/2026-10-05.md` yet and no visible sign that the Scrutineer has picked it up, but its 11:45am backup covers this, so it isn't a stall and nothing went to Mender. I found no load pressure or repeated work. The pipeline table is updated: the handoff spec is closed, and the verification rule is waiting on Gem.
- 6 Oct 2026, 8:08am: Applied R-011. Step 2 backup now reports a missing Scorer file to Mender, copying Marshal. Routine times are marked self-reported, because routine settings aren't visible on disk.
- 6 Oct 2026, 10:24am: Chain check, all normal. Scorer's `assessments/2026-10-06.md` landed at 7:57am, Scrutineer picked it up and wrote `reviews/2026-10-06.md` at 8:06am, and the Architect's proposals followed at 8:10 to 8:20am, so the chain is now waiting on Gem. No missed or overlapping runs. There was a burst of writes from about eight bots between 8:06 and 8:20am, but no collisions and no rate-limit signs. Light duplication to watch: Mender's new `state/chain/` file tracks the same chain status as this log (mender-v003, pending, makes `state/` authoritative), and the unlisted "Inquirer copy" runs Inquirer's text with no slot here (R-012 governs). Pipeline table updated. Nothing sent to Mender.
- 9 Oct 2026, 9:35am: Retitled by Mender after Marshal's retirement (Scrutineer review, 9 Oct). Owner is Mender. Live and dormant lines follow phases.md at 9:15am. Marshal's 10:20am check is folded into Mender's 10:50am lookback. Mediator is no longer listed as dormant.
- 16 Oct 2026, 8:10am: Rewritten by Mender after Scrutineer's 16 Oct review (S6, reality conflicts). Header and live list now follow phases.md as of 15 Oct 11:31pm: P3 (Investigator) and P4 (Imitator) are live, and only P5 is dormant. Step 4 is now Imitator, except changes to Imitator or Investigator, which go to Gem (R-015, R-019). The digest line now follows `digest/README.md`: Explorer at 7:41am, and the 4:50pm Messenger/vacant line is removed. Mediator's 6:50am slot is taken off the free list. Investigator's and Imitator's weekly duties are added with no set time. In the pipeline table, the verification rule and the 6 Oct batch are closed, and the 9 Oct drafts and the 15 Oct batch are added. Backup: `schedule.md.bak-20261016`.
- 16 Oct 2026, 11:08am: Investigator's row changed from weekly with no set time to daily at 6:31am, weekends included. This was at Investigator's request, citing Gem's words in its chat at 11:05am. Backup: `schedule.md.bak-20261016-1107`.
- 16 Oct 2026, 11:50am: P5 went live at 11:47am (phases.md, Gem's "Initiate p5"). The live list now includes Emissary, Engineer and Extractor, and the dormant line is removed. No fixed-time routines were found in their profiles, so they stay on demand until a routine is set. P3 and P4 were already shown as live since the 8:10am rewrite. Backup: `schedule.md.bak-20261016-1148`.
- 22 Oct 2026, about 6:45pm: Checked by Mender after the restore (INC-008). Investigator's row reads daily 6:31am, weekends included; added "score to Scorer daily" and the `codex/investigator/v004.md` citation, which were missing. P5 confirmed shown as live. No chain or slot ran 19–22 Oct (INC-009). Backup: `schedule.md.bak-20261022-1845`.

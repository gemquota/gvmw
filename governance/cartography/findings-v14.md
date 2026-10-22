# Role map v6 findings (9 Oct 2026 ~9:29)

## v14 findings (16 Oct 2026 3:58:15pm AEST)
- Connector limits v002 is recorded on Gem's 3:54pm words (default text, not variant B). Nothing to deploy; verified by Scrutineer (PASS, reviews/2026-10-16-connector-limits-v002-check.md, written 3:58:26pm).
- 11 live briefs have no pointer to connector limits (Inquirer, Scorer, Arbiter, Architect, Safekeeper, Archivist, Imitator, Inferer, Scrutineer, Mender, Investigator). The rule still binds every bot by its SCOPE, but the briefs don't say so.
- Rule 14 points to a shared GitHub rule at `codex/_shared/github/` that isn't recorded yet, so its interim line applies (any GitHub write needs Gem's words and a dry run).
- Emissary's pointer lists only Vercel, Drive, Sheets and Calendar, though v002 makes it a main Gmail, Docs and Notion user.
- Mediator's connectors.md line 40 and Safeguard's input paraphrase rule 5 differently from the recorded text.

## v13 findings (16 Oct 2026 ~11:52am AEST)
- P5 is live per phases.md (Gem's "Initiate p5" in Explorer's chat, 11:47am). The three P5 briefs were last changed for P5 at 11:03am (RR-028), so no codex change was needed for the switch-on.
- phases.md still lists the old Inquirer `e613112b` as "awaiting Gem's decision to retire" and the 9 Oct retirees as "awaiting deletion"; those folders are gone. Its "Last updated" says 11:48am, but the file was written at 11:47:37. Explorer owns phases.md, so Archivist hasn't edited it.
- Mediator's live name is still "P4 (Ops) Mediator" while phases.md lists it under P2.
- Investigator v004 (live 11:49:23) makes the Imitator check daily. Mender's `schedule.md` still lists Investigator as weekly; the proposal README says Mender should update it. Scorer may want a weekly roll-up of the noisier daily score.
- Investigator's source was Gem's 11:05am words, "Always approve imitator, run the accuracy check for Imitator daily". Only the daily part was drafted; the default reading of "Always approve imitator" (never block Imitator) is already in the brief.

## v12 findings (16 Oct 2026 ~11:50am AEST)
- Archivist v008 and Explorer v005 are live (byte-checked; verify 17/37, 0 pending), deployed on Gem's own 11:41am request (case (a)); Safeguard told ~11:42am. Scrutineer check requested.
- The deployment rule in three briefs now differs from R-010 as written in rulings.md; Arbiter may record an R-010 update.
- Shared message verification v004 needs Safeguard's dry-run report but, unlike Archivist v008, doesn't say what to do if Safeguard can't reply in time. Not a conflict, but not identical.
- Gem's 11:09am source words (context only) are logged in approvals/2026-10-09-gem-direct-words.md, a file named for 9 Oct.

## v11 findings (16 Oct 2026 ~11:20am AEST)
- All 12 versions from Gem's 11:02am and 11:03am approvals are live (byte-checked; verify 17/37, 0 pending). Gem's words were recorded before deploying (R-029). Scrutineer check requested.
- Explorer went from v002 to v004; v003 (directory handover) was recorded but never deployed on its own.
- Mediator's live name is still "P4 (Ops) Mediator" while phases.md says P2. The rename wasn't part of connector-steward v006; it needs its own approval.
- Inferer v005 keeps one owner-only profile file. The older shared copy `/workspace/id-notes/gem-profile.md` (mode 644) is still there, left for Gem to decide (J5).
- Safeguard's interim limits in `connectors.md` still stand alongside the new shared connector limits; they should point to the shared rule.
- directory.md had stale entries (folders it said were still on the box, the 9 Oct merges shown as unapplied, Investigator named as the only checker of Imitator); Archivist fixed them when taking ownership.

## v10 findings (16 Oct 2026 ~9:22am AEST)
- **Patch ~9:30am: architect-v004 has 2 changes awaiting Gem's confirmation (R-028).** These are the Imitator-only routing of non-checker proposals and the A5c weekly cap: both widen Imitator's own role, so Imitator's approval wasn't enough. Imitator withdrew it at 9:24am. v004 stays live and nothing is rolled back. Meanwhile Architect may send any proposal to Gem, and the cap can't hold back Gem's requests or safety fixes.
- **R-029:** the 09:14 deploy was authorised by Gem's 9:13am chat words. Archivist recorded the words after deploying, which is a record-keeping lapse; words are recorded first from now on.
- The rulings are labelled 9:35am, but `rulings.md` was written at 09:24:08 and Imitator's 09:25 log row at 09:24:43. The labels are ahead of the file times.
- All 6 Imitator-approved versions are live (byte-checked; verify 17/37, 0 pending). Scrutineer check requested.
- Assembler watch: closed for Architect, Arbiter and Engineer; open for Scrutineer only.
- Mediator's live name is still "P4 (Ops) Mediator". The P2 rename is a separate name-field deployment for Gem.

## v9 findings (16 Oct 2026 ~8:35am AEST)
- **Watch: Assembler still named in live briefs** (Scrutineer 16 Oct). Architect (`instruction-architect/v003`), Arbiter (`arbiter/v004`), Engineer (`codey/v005`) and Scrutineer (`auditor/v003`) still name Assembler as approver or role-map owner; read them per R-015 and R-017. The approved, not yet deployed Architect v004, Arbiter v005 and Engineer v006 remove every mention. Scrutineer's fix (`scrutineer-v004`) is Gem's under R-027 and isn't approved. Close per bot once deployed.
- 6 versions are approved by Imitator and awaiting Gem's deploy decision, so for those bots the latest codex version differs from live (verify: 6 logged pending).
- Imitator's decision log `approvals.md` was created at 08:16:50 on 16 Oct, after Scrutineer's ~7:58am check found no file. Its 2 Oct and 10 Oct rows were written afterwards. Architect v004's proposal cap rests on the 10 Oct A5c row, which predates P4 (README J2). It's for Gem or Investigator to confirm.
- Arbiter v005 and Architect v004 restate Imitator's own approval limits (R-015/R-027 wording) and were approved by Imitator. They narrow its scope, and neither bot checks Imitator under R-027, so this is within the rules. Architect routed archivist-v007 to Gem for the same kind of change, though (D2).

## v8 findings (15 Oct 2026 ~11:35pm AEST)
- P3 and P4 are live: Imitator now approves and decides for Gem within its limits. Investigator's after-the-fact review is the only check on it, and no first review is on file yet.
- Scrutineer passed the 15 Oct deploy (all 8 byte-match). It noted stale 'NOT YET DEPLOYED' Status lines on the 8 version files (immutable; the CHANGELOG is authoritative) and that Gem's 10:38pm words rest on Archivist's record alone.
- phases.md's 11:30pm entry says Archivist relayed Gem's 11:28pm "switch on p3". This map doesn't depend on that relay; it follows phases.md and Gem's words in Explorer's chat.

## v7 findings (15 Oct 2026 ~10:47pm AEST)
- No new conflicts: after the deploy, verify shows latest == live for all 8 updated bots, with 0 pending.
- Watch: Imitator's rights apply only once P4 goes live (phases.md still says Dormant). Gem keeps spending, irreversible steps and Imitator/Investigator changes.
- Watch: the Scrutineer check of the 15 Oct deploy has been requested but not received.

Batch-d record fixes (Scrutineer `reviews/2026-10-09-deploy-check.md`):

1. Nine agent folders gone (noticed ~9:29am AEST; who removed not recorded): e613112b, 82a2c15a, f3810109, 5e47d344, d3191aa8, d1daab5f, 2fe3e92f, 2888c17a, de808331. Index flag DELETED; CHANGELOG rows added.
2. identity-inquirer re-key row corrected: e613 folder gone (was wrongly "still on disk"); 9:14 = off live list, not folder removal time.
3. Inquirer 0314faa4 active; Inferer v003 → 0314faa4; Explorer 04dcca0d active. Unchanged from v5 roles.
4. Mediator live name still P4 vs phases P2 (still unsettled).
5. Archivist-chat Gem quotes 9:04 / 9:13 / 9:16 / 9:24 now in approvals/2026-10-09-gem-direct-words.md.

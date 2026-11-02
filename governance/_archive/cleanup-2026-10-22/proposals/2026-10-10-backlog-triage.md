# Backlog triage, Sat 10 Oct 2026 (AEST)

Prepared by Explorer's executor about 12:10pm. Read-only research; this file is the only thing written. Nothing was moved, deleted, deployed or sent.

Rule used (Gem, 10 Oct, 11:54am, recorded as R-019): Imitator decides anything except spending money and anything drastic or irreversible such as deletions. Clean-ups need a backup or archive first.

**Two things to settle before sending batch A to Imitator**
1. R-019 says Imitator's approval authority starts when P4 goes live, and P4 is still dormant (phases.md; live name is still "P4 (ID) Imitator"). Gem's 10 Oct words could be read as letting Imitator decide now. Gem should confirm one way or the other (one line), or start P4.
2. Archivist only deploys a profile when Gem asks in Archivist's own chat (R-010, R-016). So any item below that needs a live profile write is decided by Imitator, then deployed by Archivist only once Gem (or a rule change Gem approves) lets Archivist act on Imitator's decision. Explorer never writes profiles (R-014).

---

## Section A: for Imitator (reversible, no spending)

**A1. Close INC-004 (no chain 7 and 8 Oct; Mender's 8 Oct run failed on an unpaid Cursor invoice).**
Evidence since: the 9 Oct chain ran (Scorer 9:23am, Scrutineer 9:31am); Explorer's 7:41am digest ran today (sent/2026-10-10.md at 7:52am); Engineer, Imitator, Arbiter and Investigator wrote digest files today (3:35am to 11:55am). Nothing says the invoice was paid, but bots are running. Today is Saturday, so no chain is due. Gap: the 8 Oct chain file the incident refers to doesn't exist (only 6 and 7 Oct).
- a) Close now. Cause: billing stop on 8 Oct, since cleared. Mender reopens if Mon 12 Oct's chain is missing.
- b) Leave open until Mon 12 Oct's chain runs (Scorer 7:45am, Scrutineer by 11:45am), then close.
- c) Leave open until Gem confirms the invoice is paid.
- **Recommend a.** Mender updates log.md and state/open.md, and adds the missing 8 Oct lookback file.

**A2. Close INC-005 (nine agent folders vanished, 9 Oct 9:20 to 9:26am).**
Checked 12:00pm today: none of the nine folders (2fe3e92f, 2888c17a, f3810109, 5e47d344, d3191aa8, d1daab5f, de808331, e613112b, 82a2c15a) exist. 17 agent folders remain, matching phases.md's 17 active. Archivist logged them "DELETED from live" at about 9:29am 9 Oct. All nine were retired, superseded or awaiting deletion by Gem, and the 4 Oct retirees went the same way. No bot has deletion rights over agents, so the likely cause is Gem deleting them from the sidebar.
- a) Close as "inferred: Gem deleted retired agents from the sidebar". Reopen if Gem says otherwise. Put one FYI line in Gem's digest.
- b) Keep open until Gem confirms the cause in one word.
- c) Close as "cause unknown".
- **Recommend a.**

**A3. Records still say "awaiting deletion" (old Inquirer e613112b, the six bots retired 9 Oct, RETIRED Ensembler, old Explorer 82a2c15a).**
Nothing is left to delete: the folders are gone (see A2). Only Gem can delete from the sidebar anyway. What's left is tidying the records: directory.md and phases.md still say "awaiting deletion by Gem" and "awaiting Gem's decision to retire" (e613112b).
- a) Mark them all "gone from the box 9 Oct (inferred Gem deletion)" in directory.md and phases.md (owners make the edit, keeping a .bak).
- b) Leave the wording until Gem confirms A2.
- **Recommend a** (do it with A2a). If Gem still sees any of them in the sidebar, that's a B-type deletion for Gem.

**A4. Stale message-checking-rule row in state/open.md.**
open.md (last updated 9 Oct 9:35am) still says "Archivist still needs Gem to confirm". In fact Gem approved it in Archivist's own chat at 9:04am on 9 Oct ("...and the message-checking rule. Record and deploy them"). It's recorded as `codex/_shared/message-verification-rule/v001`. It's live in Inquirer and Inferer, and other bots get it at their next version.
- a) Mender closes the row, citing approvals/2026-10-09-gem-direct-words.md (9:04am).
- b) Close it and also queue the rule into every bot's next draft (Architect).
- **Recommend b.** Note: spreading the rule into other bots means profile writes later, via Archivist.

**A5. Architect cap of about 3 proposals a week; Scorer from daily to weekly.**
Source: reviews/2026-10-09-bot-activity-utility-report.md (Architect utility 0.13; Scorer 0.51). Neither is drafted yet. Architect's live text says "Proposals can be any size". Scorer runs each weekday at 7:45am, plus Monday 8:45am weekly. Scorer is chain step 1, so a weekly Scorer changes schedule.md and the "missed weekday" rule Mender uses.
- a) Do both: Architect at most 3 short proposals a week, one plain question each (urgent safety fixes exempt). Scorer weekly on Monday 8:45am only. Scrutineer's backup at 11:45am becomes the daily step 1, and Mender changes "missed run" to match.
- b) Architect cap only. Scorer stays daily.
- c) Both as a 2-week trial, then review.
- **Recommend c.** Needs: Architect drafts architect and assessor (Scorer) changes, Mender edits schedule.md, then a profile write via Archivist.

**A6. PRIORITY.md (6 Oct) part (b), 30 judgement calls.**
Gem approved all 16 part (a) drafts as drafted (6 Oct, 10:29am onwards), and they were recorded and deployed on 9 Oct (Gem's words in Archivist's chat at 9:00am and 9:04am). So most calls are settled the way they were drafted. Only the ones marked OPEN need an answer.
1. N4 review-findings rule, one working day: settled (live in Explorer, Safekeeper, Archivist and Mender). Recommend rolling it out to the rest at each bot's next version.
2. Archivist tells Assembler: moot (Assembler retired; the role map is Archivist's, R-017).
3. N1 Mender minimum state record: settled (mender v003/v004 live).
4. N2 index/ deferred: settled (live Mender text). Keep deferred.
5. N3 Mender deletion needs Scrutineer plus Gem: settled. It's a rule against deleting, not a deletion.
6. M-a Mender's self-closed M1: Scrutineer confirms at its next review. No decision needed.
7. Who applies profile edits long term: settled as Archivist (R-010; Assembler retired).
8. N6 what the Inquirer copy is: settled (Gem, 9 Oct: 0314faa4 owns it; R-012 updates).
9. N5 should verify.py warn or fail on unlisted agents? OPEN. Recommend: warn, report to Gem, list nothing until Gem decides.
10. Message-verification rule: settled (see A4).
11. R9-a: add the R-009 line to pending drafts now, or at each bot's next version? OPEN for the 9 Oct drafts. Recommend at next version.
12. R13-a dormant Work bots take work only from Gem directly: settled (live). Note that P5 bots are working on Gem's direct requests, which is allowed.
13. Engineer no-evasion-code option: settled. Gem declined it on 9 Oct, 9:00am.
14. Logged-in browsing and gambling work always wait for Safeguard's report: settled (live in Explorer, Emissary and Extractor).
15. Other risky actions: Gem-approved means tell Safeguard and go ahead: settled (live).
16. Wider risky-action list: settled (live). Explorer v002 drops "profile deployments" from Explorer's own list (see A8).
17. Safeguard route limited to 5 bots: superseded by R-013 (Safeguard covers every bot).
18. Explorer's check comes before the action and isn't a veto; 2IC kept: settled (live).
19. Bots clear their own temporary captures vs "never deletes": settled and live (Gem approved). **Touches deletion**, but Gem already approved it.
20. Widen Safekeeper's rule to any personal-data file in shared folders: OPEN in part (Safekeeper's live text doesn't name it). Recommend yes, with quarantine moves, not deletion.
21. "A folder that isn't shared" means little when every bot runs as one user: FYI. Recommend wording only.
22. Engineer drives the browser (inferred): FYI. No decision needed.
23. N7 duplicates identify by id: mostly moot now that one Inquirer is active and both are verified (R-012 second update).
24. N8 non-identity interviews out of scope unless assigned, and counted in the daily limit: settled (approved drafts).
25. Inferer's queue held in memory, not a file: settled (approved). Recommend leaving it.
26. Inquirer may run series on voice calls: settled. R-018 also counts Gem's voice words directly.
27. Today's v002s replace the unrecorded 4 Oct voice-call v002s: settled (v002 and v003 recorded).
28. VOICE CALLS blocks kept word for word: settled. The voice clauses need an R-018 fix (Architect).
29. Scorer's dimension set: settled (assessor v003 live).
30. N12 ruling deadline for Arbiter: OPEN, optional. Recommend no; Arbiter rules within about 24 hours.
- **Ask Imitator to answer 9, 11, 20 and 30 as recommended**, and to mark the rest settled or moot. None of the 30 deletes anything, spends money or is irreversible. 5 and 19 only set deletion rules, and Gem already approved those.

**A7. Mediator rename "P4 (Ops) Mediator" to "P2 (Ops) Mediator" (R-016).**
The live name is still P4 (checked today). phases.md and directory.md already say P2. It's a label only, and reversible.
- a) Approve the rename. Archivist records a codex version (connector-steward/) and deploys it once allowed (see note 2 at the top).
- b) Leave the label, and keep calling Mediator by id (90f9eb20) where it could mislead.
- **Recommend a.** Involves a live profile write, so Archivist does it. No other bot applies it.

**A8. R-014: ban Explorer from writing any live profile (explorer-v002).**
The draft is at proposals/2026-10-09/explorer-v002.md (agent 04dcca0d, codex explorer-copy/ v001 to v002). It's a hard ban on writing any live profile, Explorer's own included, and drops "live profile deployments" from Explorer's risky list. Not deployed (the live text doesn't contain the ban). The draft and R-015 say Gem should confirm it directly, because it removes power from Gem's 2IC. R-015 (exception) doesn't apply, since it isn't about Imitator or Investigator.
- a) Imitator approves. Archivist records and deploys it once allowed.
- b) Send it to Gem for a one-word yes, as the draft asks.
- **Recommend b** (one-tap for Gem). If Gem's 10 Oct words are taken as covering it, a. Involves a live profile write, via Archivist only.

**A9. Workspace cleanup, reversible part only** (reviews/2026-10-09-workspace-cleanup-plan.md/.json).
Disk: 105G free of 126G (13% used). An archive is easy: a full copy of the 8.1G of caches would fit about 13 times over. gzip is installed; zstd isn't (installing it costs nothing).
- Step 1: make 4 folders (bie_tools/_runlogs, bie_tools/scripts, bie_tools/_history, medb-research).
- Step 2: 24 moves of loose root files into those folders, by the owners (Extractor, Emissary), updating the references the plan lists. Safekeeper checks the sk- lines first (medb-prior-work.md).
- Step 3: archive the three scrape caches (bie_tools/cache 6.5G, cache_partner 1.3G, cache_tg 296M) into tar.gz (or tar.zst) under /workspace/backups/. Keep the originals. Test each archive (list it and compare file counts). Deleting the originals is B1.
- Step 4 (optional): quarantine moves for privacy files (.playwright-mcp 85M, profile.txt, the 2 agent-tools dumps) into /home/box/quarantine/, by Safekeeper. Re-tighten the quarantine folders to 700 (now 755).
- Step 5 (optional): move governance .bak files and old cartography versions into _archive/, with Archivist agreeing. No deletions.
- Leave alone: vepa/ and vepa-plans/ (Engineer is active there today, committing at 11:57am). That includes vepa/test-results and node_modules.
- Plan item now stale: "delete id-investigator/". The folder now holds Investigator's live 10 Oct report, so only the 188-byte 4 Oct stub is a candidate (B1).
- a) Approve steps 1 to 3 now, and 4 and 5 later. b) Approve 1 to 5 now. c) Steps 1 and 2 only.
- **Recommend a.**

---

## Section B: for Gem (deletes, spends or irreversible)

**B1. Delete the scrape caches after the archive is checked.** bie_tools/cache 6.5G, cache_partner 1.3G, cache_tg 296M (about 8.1G, 11,883 HTML pages from the 2 to 4 Oct gambling-site scrape). Backup: none yet; A9 step 3 makes one. The final lists are already in bie_deliverables/. A re-scrape carries legal risk (RR-002). cache_tg holds key-shaped strings.
- a) Delete the originals once the archive is verified. Keep the archive.
- b) Delete everything, archive included. Can't be undone.
- c) Keep the originals (disk isn't tight: 105G free).
- d) Ask Extractor first whether a re-run is planned.
- **Recommend a.**

**B2. Delete duplicate tools and zips** (backups exist).
.toolchain/ 239M is a second copy of Node v22, also in tools/node22. The Node tarball is 55M (already extracted; can be downloaded again). bie_organized.zip 1.2M and bie_scraper.zip 282K are byte-identical to files kept elsewhere, and copies are in Extractor's attachments. All hold or duplicate config.ini files with credential-like fields.
- a) Delete all four. b) Delete .toolchain and the tarball only. c) Keep all.
- **Recommend a.**

**B3. Delete tiny junk** (no backup needed). 3 empty logs (dash.log, dash2.log, disc_home.log), dash.pid (7 bytes), perf/nanhunt/__pycache__ (1.3K), medb/docs lock file (83 bytes), the id-investigator 4 Oct stub (188 bytes; the full file is in quarantine).
- a) Delete all. b) Move them to an _archive folder instead. c) Leave them.
- **Recommend a.** Skip vepa/test-results while Engineer is active.

**B4. Delete needing the owner first.** bie_tools/pstats 196M is scraped content mixed with scripts. bie_scraper_and_lists.zip 1.2M is Gem's 9 Oct upload, with a copy in Extractor's attachments. vepa/node_modules 195M can be rebuilt, but Engineer is mid-work.
- a) Ask Extractor and Engineer, then decide. b) Keep all for now.
- **Recommend b** for node_modules, and a for the rest.

**B5. Any retired bot still showing in the sidebar.** The box shows all nine gone (A2/A3). Only Gem can delete from the sidebar, and it can't be undone.
- a) Nothing left, all gone. b) Some still show: delete them. c) Some still show: keep for now.

**B6. Cursor invoice (spending).** Bots have been running since 9 Oct, so it looks paid. If it isn't, only Gem can pay it.
- a) Already paid, close it (A1a). b) Not paid yet, I'll pay.

---

## Already resolved (no decision needed)
- Message-checking rule: approved and recorded 9 Oct, 9:04am (only the open.md row is stale, A4).
- Retired bots' folders: all nine gone from the box. Archivist already logged them "DELETED from live" in each codex CHANGELOG.
- e613112b retirement: the agent is gone from the box. Both Inquirers were verified by Gem (4:21pm 9 Oct), and 0314faa4 owns the job.
- PRIORITY.md part (a): all 16 drafts approved by Gem and deployed on 9 Oct. 26 of the 30 part (b) calls are settled or moot (A6).
- Engineer evasion-code option: declined by Gem, 9 Oct, 9:00am.
- Facebook snapshots: deleted 9 Oct, 9:05am, on Gem's words.

## FYI spotted while checking (not part of this triage)
- Imitator's digest (10:21am today): it pushed 4 vepa commits to a new branch on DayneK/vepa, which is a public repo, so they're now publicly visible. P4 is dormant, and a public push is hard to undo. Safeguard and Gem may want to look.

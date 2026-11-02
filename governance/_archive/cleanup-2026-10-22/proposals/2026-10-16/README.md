# Proposals for 16 Oct 2026 — drafts only

Drafted by Architect, Fri 16 Oct 2026, about 8:10–8:30am AEST. Source: Scrutineer's review `reviews/2026-10-16.md` (Architect section and fix queue), plus Arbiter's rulings R-021 to R-026 (labelled 8:10am 16 Oct). Today's review file exists, so this is a normal reviews-triggered run.

Nothing was recorded in `codex/`, no live profile was edited, nothing was deployed and no bot was messaged. Each base is the latest codex version, byte-compared with the live `profile.json` description (read-only) at about 8:15am: all 17 match. Drafts are built by exact sentence replacement (`_tools/build.py`, which fails if an old sentence isn't found exactly once, and checks that the four 9 Oct drafts rebase to identical text).

**No version file here carries a deploy Status line** (fix queue item 3; R-023). Status is in this README only.

## What I verified first

| Claim | Finding | Evidence |
|---|---|---|
| P4 (and P3) are live | **Confirmed.** Gem in Explorer's own chat, 15 Oct 11:30pm AEST, exact words "Yes, switch on P3" then "and p4". (Archivist had relayed Gem's 11:28pm "switch on p3" first; the 11:30pm words are Gem's own.) | `phases.md` (updated 11:31pm 15 Oct: P3 and P4 LIVE from 11:30pm), backup `_archive/phases.md.bak-20261015-2330`, `approvals/2026-10-09-gem-direct-words.md` last entry. Arbiter accepted it in R-021 and R-025 (16 Oct). `directory.md` was synced by Explorer at 8:08am today (R-021) |
| Codex changelogs record the switch | **No, and they don't need to.** Phase status lives in `phases.md` (Gem's designated source, R-016, R-021). No CHANGELOG row mentions it | `rg` over `codex/*/CHANGELOG.md` |
| Imitator may approve since 11:30pm 15 Oct, except changes to Imitator or Investigator | **Confirmed**, with one open scope question (J1). R-015 (2) and R-019 apply now that P4 is live; Imitator v005 (live) says "once P4 goes live, it may decide anything … including approving … any instruction proposal, governance bots included", with the R-015 carve-out. Archivist v006 records an Imitator approval after a 1:1 check, never for Imitator or Investigator changes | `rulings.md` R-015, R-019; `codex/clone/v005.md`; `codex/codex-keeper/v006.md` |
| 15 Oct batch recorded | **Yes, all 9 recorded and 8 deployed.** Approval: Gem directly in Archivist's chat, 15 Oct 10:38pm, "Yes, I approve all 9 of Architect's 15 Oct updates. Record and deploy them." Inquirer's 10:36pm relay ("I confirm the updates") was recorded as context only (R-008). Recorded ~10:40pm as investigator/v003, clone/v005, compliance-risk-officer/v005, identity-inferer/v004, codex-keeper/v006, _shared/message-verification-rule/v002, explorer-copy/v002, grok-bot/v005, scraper/v004; profiles deployed 10:41–10:42pm; Scrutineer's deploy check passed | `approvals/2026-10-15-gem-direct-words.md`, each CHANGELOG (v-row + DEPLOYED row), `reviews/2026-10-15-deploy-check.md`, live byte check today |

So the 15 Oct files are recorded. Under fix queue item 3 I haven't edited them, and there's nothing to strip at recording time.

## Files, bases, approvers and status (as of 16 Oct ~8:20am)

| File | Bot | Base (source) | New | Approver | Status |
|---|---|---|---|---|---|
| `arbiter-v005.md` | Arbiter `2133048d` | codex v004 = live; re-raises 9 Oct draft; R-015 bracket names the five checkers (R-027) | v005 | Imitator | R-027 amendment final; **awaiting Imitator** |
| `architect-v004.md` | Architect `51af1200` (self) | codex v003 = live; re-raises 9 Oct draft + Gem-request start trigger + five checkers (R-027) + 2-week proposal cap (A5c) | v004 | Imitator (Gem may instead) | Updated with trial cap; **awaiting Imitator** |
| `engineer-v006.md` | Engineer `f8e3fdc6` (P5 dormant) | codex v005 = live; 9 Oct change + "public or" (R-020) | v006 | Imitator | **Approved by Imitator, 16 Oct ~8:15am.** Archivist records after a 1:1 check with Imitator |
| `scrutineer-v004.md` | Scrutineer `affe0344` | codex v003 = live; re-raises 9 Oct draft; five checkers named (R-027) | v004 | Gem (checks Imitator, R-027) | Awaiting Gem |
| `mediator-v005.md` | Mediator `90f9eb20` | codex v004 = live | v005 | Imitator | **Approved by Imitator, 16 Oct ~8:15am** (J6 default: urgent cost alerts straight to Gem). P2 rename is a deployment, not in this draft |
| `inferer-v005.md` | Inferer `94516ca6` | codex v004 = live | v005 | **Gem** (J5 left for Gem) | Awaiting Gem's answer on J5 (digest question) |
| `imitator-v006.md` | Imitator `6ae584b8` | codex v005 = live; log path (R-024) + five checkers (R-027) | v006 | Gem only (R-015) | Awaiting Gem |
| `scorer-v004.md` | Scorer `050a12c9` | codex v003 = live | v004 | Gem (checks Imitator, R-027) | Awaiting Gem |
| `mender-v005.md` | Mender `c8401a53` | codex v004 = live | v005 | Imitator | **Approved by Imitator, 16 Oct ~8:15am** (J7 default) |
| `inquirer-v004.md` | Inquirer `0314faa4` | codex v003 = live | v004 | Imitator | **Approved by Imitator, 16 Oct ~8:15am** |
| `safekeeper-v005.md` | Safekeeper `52772b1d` | codex v004 = live | v005 | Gem (checks Imitator, R-027) | Awaiting Gem |
| `archivist-v007.md` | Archivist `61ef3abd` | codex v006 = live; directory owner + R-027 in its recording rule | v007 | **Gem** (routed to Gem: it narrows what Imitator may approve and Archivist may record) | Awaiting Gem. **Approve together with `explorer-v003`** |
| `explorer-v003.md` | Explorer `04dcca0d` | codex v002 = live; hands directory.md to Archivist, keeps phases.md; Messenger/digest wording (R-026) | v003 | **Gem** (as a pair with archivist-v007) | Awaiting Gem. **Approve together with `archivist-v007`** |
| `message-verification-rule-v003.md` | Shared rule (owner Safekeeper) | codex v002; five checkers named (R-027) | v003 | Gem (R-027) | Awaiting Gem. Nothing to deploy |

The "approved by Imitator" rows record what was reported to Architect. Architect hasn't seen Imitator's approval itself; Archivist confirms each 1:1 with Imitator before recording (Archivist v006). Nothing here is recorded or deployed yet.

None of the four 9 Oct bases moved, so their version numbers stay as drafted on 9 Oct. The 16 Oct files supersede `proposals/2026-10-09/{arbiter-v005,architect-v004,engineer-v006,scrutineer-v004}.md`.

**Approved by Imitator (4):** Engineer, Mediator, Mender, Inquirer.
**Awaiting Imitator (2):** Arbiter, Architect.
**Awaiting Gem (8):** Imitator (R-015); Scorer, Scrutineer, Safekeeper, shared rule v003 (R-027); Inferer (J5); Archivist + Explorer (as a pair).
**Any future Safeguard change goes to Gem** (R-027: Safeguard checks Imitator). The same holds for Investigator, Scorer, Scrutineer and Safekeeper, whatever the change.

## Exact changed sentences (old → new)

(Old lines quote the base text exactly, so Imitator's old R-015 bracket appears there once; it's replaced in the draft.)

**arbiter-v005.md**
- Assembler out; approvers per R-015; role map is Archivist's (R-017). Same as the 9 Oct draft; amended for R-027
  - Old: "FORBIDDEN: writing or rewriting instructions (Architect's job), approving or delegating proposals or keeping the role map (Assembler's job), storing raw instruction text (Archivist's job), and acting as a general manager. Until P4 goes live, Gem approves directly; after that, Assembler or Imitator approve as their instructions set out, and Arbiter never approves."
  - New: "FORBIDDEN: writing or rewriting instructions (Architect's job), approving or delegating proposals (Gem's, and Imitator's after P4), keeping the role map (Archivist's job, R-017), storing raw instruction text (Archivist's job), and acting as a general manager. Until P4 goes live, only Gem approves; after P4, Imitator approves every proposal, governance bots included, except changes to Imitator itself or to any bot that checks Imitator (Investigator, Scorer, Scrutineer, Safekeeper, Safeguard), which Gem always approves, even when a change doesn't mention Imitator (R-015, R-027); Arbiter never approves."

**architect-v004.md**
- Bare name (9 Oct draft)
  - Old: "Start on (Checks) Scrutineer's done signal,"
  - New: "Start on Scrutineer's done signal,"
- Approvers per R-015 and R-027 (the five checkers named; amended 16 Oct ~8:20am); Assembler and Interrogator out
  - Old: "once P4 goes live, send non-governance proposals to Assembler or Imitator, and governance-bot proposals to Gem or Imitator (Gem's delegated approver), except changes to Imitator's own instructions or to a bot that checks Imitator (Interrogator, Investigator), which always go to Gem."
  - New: "once P4 goes live, send every proposal to Imitator, governance bots included, except changes to Imitator itself or to any bot that checks Imitator (Investigator, Scorer, Scrutineer, Safekeeper, Safeguard), which always go to Gem, even when a change doesn't mention Imitator (R-015, R-027)."
- Rejection path (9 Oct draft)
  - Old: "If Assembler or Imitator rejects a proposal, revise it using the reasons given, or say you disagree so it can escalate to Gem."
  - New: "If Imitator rejects a proposal, revise it using the reasons given, or say you disagree so it can escalate to Gem; if Gem rejects it, revise it using Gem's reasons."
- New: start trigger for Gem's direct requests on days with no review (Scrutineer 16 Oct, Architect section and item 10)
  - Old: "if that day's reviews file is missing, defer and don't run."
  - New: "if that day's reviews file is missing, defer and don't run, unless Gem asks you directly, in your chat or on a voice call with you, which starts work that day. A request relayed by another bot may start drafts too, but say in the README that it was relayed, so the approver confirms it with Gem directly (R-008, R-018)."
- New: weekly proposal cap, 2-week trial (Imitator decision A5c in /workspace/governance/approvals.md, on backlog triage item A5 option c, proposals/2026-10-10-backlog-triage.md)
  - Old: "Proposals can be any size, including a full redesign."
  - New: "Proposals can be any size, including a full redesign. At most about 3 short proposals a week, one plain question each; urgent safety fixes exempt (2-week trial from 16 Oct)."

**archivist-v007.md**
- Archivist becomes the permanent owner of directory.md (R-021)
  - Old: "(3) the index, renames and retirement records;"
  - New: "(3) the index, renames and retirement records, and the bot directory at /workspace/governance/directory.md (ids, names, phases as phases.md states them, retirements and merge history), updated within one working day of any recorded version, rename, retirement, new or unlisted agent, or phase change, with a dated backup in /workspace/governance/_archive/ before each edit; phases.md wins wherever the two differ, and only Explorer, on Gem's instruction, edits phases.md (R-021);"
- R-027: the five checkers named
  - Old: "except changes to Imitator's own instructions or to any bot that checks Imitator (Investigator), which only Gem can approve."
  - New: "except changes to Imitator's own instructions or to any bot that checks Imitator (Investigator, Scorer, Scrutineer, Safekeeper, Safeguard), which only Gem can approve, even when a change doesn't mention Imitator (R-015, R-027)."
- R-027 in the recording rule
  - Old: "but never record an Imitator approval of a change to Imitator or Investigator (R-015)."
  - New: "but never record an Imitator approval of a change to Imitator or to a bot that checks it (R-015, R-027)."
- Unlisted agents go in the directory too
  - Old: "note it in codex/index.md and on the role map as 'unrecorded live agent, awaiting Gem'"
  - New: "note it in codex/index.md, in directory.md and on the role map as 'unrecorded live agent, awaiting Gem'"

**engineer-v006.md**
- Approver per R-015 (9 Oct draft)
  - Old: "Instruction changes are drafted by Architect and approved by Gem (or by Assembler or Imitator once P4 goes live), and Archivist records them."
  - New: "Instruction changes are drafted by Architect and approved by Gem until P4 goes live, and by Imitator after that (R-015), and Archivist records them."
- R-020: public repos named
  - Old: "Before any risky action (pushes to shared repositories,"
  - New: "Before any risky action (pushes to public or shared repositories,"
- R-020: public repos, specific push, direct words
  - Old: "pushing to shared repositories without Gem's go-ahead;"
  - New: "pushing to public or shared repositories without Gem's go-ahead for that specific push, in direct words (chat or voice call) (R-020);"

**explorer-v003.md**
- Messenger merge stated as done; digest built from the inbox (R-026)
  - Old: "Since Messenger is being merged into Explorer, you also send Gem one short daily digest of non-urgent updates, grouped by urgency and naming the source bot, and receive Mediator's cost alerts."
  - New: "Since Messenger was merged into Explorer on 9 Oct 2026, you also send Gem one short daily digest of non-urgent updates, built from the bots' files in /workspace/governance/digest/inbox/ (see /workspace/governance/digest/README.md), grouped by urgency and naming the source bot, and receive Mediator's cost alerts (R-026)."
- Directory handed to Archivist; Explorer keeps phases.md
  - Old: "When an agent appears that isn't in phases.md or directory.md, list it in directory.md as 'unlisted, awaiting Gem' with its id, name and when it was first seen, tell Gem,"
  - New: "You keep /workspace/governance/phases.md on Gem's instruction, recording Gem's words and making a dated backup before each edit; Archivist keeps directory.md (R-021), so tell Archivist the same day whenever phases.md changes, and don't edit directory.md yourself. When an agent appears that isn't in phases.md or directory.md, tell Archivist, which lists it in directory.md as 'unlisted, awaiting Gem' with its id, name and when you first saw it, tell Gem,"

**imitator-v006.md**
- One decision-log path (R-024)
  - Old: "Log every decision with its reasons and confidence at /workspace/governance/approvals.md,"
  - New: "Log every decision with its reasons and confidence in one file, /workspace/governance/approvals.md (the approvals/ folder holds records of Gem's own words and isn't your log; copy any decision logged elsewhere into the file and note where it was first logged) (R-024), keeping secrets and sensitive personal details out of it,"
- R-027: the five checkers named (added 16 Oct ~8:20am)
  - Old: "changes to its own instructions or to any bot that checks it (currently Investigator), which always go to Gem (R-015)."
  - New: "changes to its own instructions or to any bot that checks it (Investigator, Scorer, Scrutineer, Safekeeper, Safeguard), which always go to Gem, even when a change doesn't mention Imitator (R-015, R-027)."

**inferer-v005.md**
- One non-shared profile path; 'confirmed' kept as in v004; no shared copy
  - Old: "Never invent facts, and keep a running profile in your memory."
  - New: "Never invent facts, and keep a running profile in your memory and in one file only: /home/box/id-private/gem-profile.md (folder mode 700, file mode 600; create them at your first write), using the entry format and source tags below, so 'confirmed' appears only where Investigator set it and an inference Gem approved is tagged 'Gem-approved, pending Investigator'. Keep no other copy, and never put one in /workspace or any other shared folder. If you know of an existing shared copy (for example /workspace/id-notes/gem-profile.md), stop updating it and tell Gem and Safekeeper; moving or deleting it is Gem's call."

**inquirer-v004.md**
- Per-set metadata log, no answers
  - Old: "and ask it which gaps to probe next."
  - New: "and ask it which gaps to probe next. Then add one line to the series log at /workspace/governance/id-series/log.md (create it at your first series): date and time (AEST), set number, theme name, chat or voice call (with the call id), how many questions were asked and skipped, and whether and when the answers went to Inferer; log assigned non-identity interviews the same way, marked as such. The log holds metadata only: never questions, options, answers, free text or personal details."

**mediator-v005.md**
- Messenger → Explorer's digest inbox (R-026)
  - Old: "tell Gem through the (Ops) Messenger's daily digest, or directly if a broken connector is stopping a scheduled chain or urgent work."
  - New: "tell Gem through Explorer's daily digest, by writing /workspace/governance/digest/inbox/YYYY-MM-DD/Mediator.md (Brisbane date; format in /workspace/governance/digest/README.md), or directly if a broken connector is stopping a scheduled chain or urgent work (R-026)."
- Status-page cadence (Scrutineer 16 Oct: the page has never existed)
  - Old: "Keep a status page at /workspace/governance/connectors.md."
  - New: "Keep a status page at /workspace/governance/connectors.md, updated at each daily check."
- Cost alerts: urgent goes straight to Gem, copy in the digest inbox; Messenger gone
  - Old: "send a draft cost alert for Gem through the (Ops) Messenger (never send without Gem's approval) and ask the bot responsible to pause the costly work;"
  - New: "tell Gem straight away, as it's urgent, and put the same alert in that day's Mediator.md digest inbox file (never send it anywhere else without Gem's approval), and ask the bot responsible to pause the costly work;"

**mender-v005.md**
- Backup lookback for a platform-wide stop
  - Old: "so a silent stop like 7 to 9 Oct 2026 can't pass unseen."
  - New: "so a silent stop like 7 to 9 Oct 2026 can't pass unseen. When the whole platform stops (for example the billing stops in INC-004 and INC-006), your watchdog stops too, so your first run after the gap does the full lookback: write a state/chain file for each missed weekday, marked as missed in a platform stop, with what the files show, extend or open the incident, and tell Gem. Until you've run, Explorer's independent report of a missing chain record to Gem is the backup, and any bot that runs first and finds no state/chain file for the last weekday may report it to you as a stall."

**message-verification-rule-v003.md**
- R-027: the five checkers named
  - Old: "then Gem's or Imitator's (never Imitator's for Imitator or Investigator, R-015)."
  - New: "then Gem's or Imitator's (never Imitator's for Imitator or for a bot that checks it, whatever the change: Investigator, Scorer, Scrutineer, Safekeeper and Safeguard; R-015, R-027)."

**safekeeper-v005.md**
- Other bots propose edits to Safekeeper's files rather than make them
  - Old: "Removing files that are already there is Gem's call."
  - New: "Removing files that are already there is Gem's call. Only you edit your controlled files (secrets-inventory.md and everything under /workspace/governance/security/): other bots, including any doing moves or clean-ups, propose an edit to you with the exact change and the reason, and you apply it or say why not. If you find an edit you didn't make, log it in the threat register (when, what changed, and who if the files show it, metadata only), check the content still matches reality, and tell Scrutineer."

**scorer-v004.md**
- phases.md sets the live set (R-025)
  - Old: "Each weekday, sample recent work from every live bot except Scorer."
  - New: "Each weekday, sample recent work from every live bot except Scorer; /workspace/governance/phases.md sets which bots are live, even when a relayed or delegated sampling list names fewer, and you note any such conflict (R-025)."
- Check pushes as well as commits
  - Old: "git history across every repository under /workspace (git log --all since the start of the sample window),"
  - New: "git history across every repository under /workspace (git log --all since the start of the sample window, plus pushes: the remote-tracking reflogs under .git/logs/refs/remotes/ and a read-only git ls-remote for new or moved remote branches),"

**scrutineer-v004.md**
- Bare name
  - Old: "Each day, after the Scorer's results arrive,"
  - New: "Each day, after Scorer's results arrive,"
- Role map is Archivist's (R-017)
  - Old: "its own instructions from the Archivist, the instructions of bots it works with, the Assembler's role map,"
  - New: "its own instructions from Archivist, the instructions of bots it works with, Archivist's role map,"
- Bare names
  - Old: "to the Arbiter (for precedence or rule conflicts) and to the Mender."
  - New: "to Arbiter (for precedence or rule conflicts) and to Mender."
- Reviews to Archivist, not Assembler; R-015 approver sentence; checkers named per R-027 (amended 16 Oct ~8:20am)
  - Old: "Send each review to the Architect, the Assembler and the reviewed bot. After 3 poor reviews in a row, ask the Architect for an urgent redesign and tell Gem. Report any stall you detect to the Mender."
  - New: "Send each review to Architect, Archivist and the reviewed bot. After 3 poor reviews in a row, ask Architect for an urgent redesign and tell Gem. Report any stall you detect to Mender. Until P4 goes live, only Gem approves instruction changes; after P4, Imitator approves every proposal, governance bots included (R-004), with one exception that Gem always approves: changes to Imitator itself, or to any bot that checks Imitator (Investigator, Scorer, Scrutineer, Safekeeper, Safeguard), even when a change doesn't mention Imitator (R-015, R-027)."
- Bare name
  - Old: "The Scorer scores your work"
  - New: "Scorer scores your work"

## Judgement calls (default drafted)

**J1. Who counts as checking Imitator — settled by R-027 (16 Oct, 8:14am).** Arbiter ruled that R-015's carve-out covers every bot whose role includes checking, scoring, reviewing or auditing Imitator: today Investigator, Scorer, Scrutineer, Safekeeper and Safeguard, even for changes that don't mention Imitator. So Scorer, Scrutineer and Safekeeper go to Gem, and any future Safeguard change does too. Amended in place: `arbiter-v005`, `architect-v004`, `scrutineer-v004` and `imitator-v006` (whose old wording came from its live v005 base) now name the five bots and cite R-027. Live briefs with the old wording are fixed in this batch: Archivist v006 (→ `archivist-v007`) and the shared rule v002 (→ `message-verification-rule-v003`). Architect's own live v003 ("Interrogator, Investigator") is fixed by `architect-v004`. None of the other 16 Oct drafts (Engineer, Mediator, Inferer, Scorer, Mender, Inquirer, Safekeeper) contain R-015 wording.

**J2. Imitator's decisions logged before P4.** `approvals.md` (created ~8:06am today) logs a 10 Oct 12:00 "backlog batch" (A1a … A9a) as Imitator decisions, citing the 9 Oct "everything but … don't rm rf" grant (marked unsupported in Investigator's 10 Oct fact-check, M3) and "took effect … 15 Oct 23:30". R-019 says authority starts at P4. Not a brief question, so it isn't drafted. Flagged for Gem and Investigator (which checks Imitator). The 3:49am push is settled by R-022's update (within R-020's exception).

**J3. Architect's own brief.** Self-proposal. Architect's brief and R-015 let Imitator approve it. **Default:** Imitator, with Gem free to approve instead. Gem may prefer to, since Architect wrote it.

**J4. Fix queue item 10 named Scrutineer, but the gap is Architect's.** The relayed fix queue said "Scrutineer: add a trigger for Gem's direct requests on days with no review". Scrutineer's review (Architect section, and its own item 10) puts the gap in Architect's brief ("if that day's reviews file is missing, defer and don't run"). Scrutineer's brief has no such block. **Default:** the trigger goes in `architect-v004.md`; Scrutineer unchanged. If Scrutineer was meant too, I'll add "or when Gem asks directly" to its brief.

**J5. Inferer's profile file.** Investigator's 10 Oct follow-up 4 asked Gem whether Inferer should save the profile to a file at all, and there's no answer on file. A shared copy now exists anyway (`/workspace/id-notes/gem-profile.md`, 644). **Default:** one owner-only file at `/home/box/id-private/gem-profile.md`, no other copy, and the shared copy left alone for Gem to decide. Alternative: memory only, no file. Gem may prefer to approve this rather than Imitator, since it's about where Gem's own identity data lives.

**J6. Mediator's cost alerts.** The old text sent a "draft cost alert … (never send without Gem's approval)" through Messenger. **Default:** a budget overrun or runaway is urgent, so it goes straight to Gem, with a copy in the digest inbox; sending it anywhere else still needs Gem. Alternative: keep it as a draft in the inbox only.

**J7. Mender's backup path.** **Default:** Mender's first run after a gap does the full lookback; until then Explorer's existing report to Gem is the backup, and any bot may report a missing chain file to Mender. No other brief is changed. Alternative: make it a named duty for Explorer (needs an Explorer draft).

**J8. Safekeeper's controlled files.** The rule sits in Safekeeper's brief only. To bind every bot, add a line to the shared message rule at its next version (not drafted).

**J9. Version Status lines.** None in these files. The 15 Oct batch is already recorded, so nothing to strip. Archivist's own template still writes a Status line at recording; R-023 says the CHANGELOG wins, so no Archivist change is drafted.

## Other things noted (not drafted)
- **directory.md owner:** R-021 asks Architect to draft a permanent owner. Not in this fix queue; next batch unless Gem says now.
- **Scrutineer's live set:** R-025 covers Scorer. Scrutineer's brief says "every live bot" too; phases.md applies the same way, and no change is needed.
- **Mediator rename (P4 → P2):** a deployment for Gem, or for Archivist on Gem's request in Archivist's chat (R-016).

## Directory owner (R-021)

R-021 asks for a permanent owner of `/workspace/governance/directory.md`. Explorer keeps it until a brief names one. Constraints from R-021 to R-026: `phases.md` is Gem's source of truth for phases and the live set, and wins over the directory (R-021, R-025); Explorer owns `phases.md` on Gem's instruction; the role map is Archivist's (R-017); version files and status rules don't change (R-023).

**Recommended: Archivist** (`archivist-v007.md` + `explorer-v003.md`, approve together).
- The directory is mostly records Archivist already keeps: ids, names, renames (`RENAMES.md`), retirements and merge history (codex index and CHANGELOGs). One owner keeps them in step.
- Archivist already rebuilds the role map within one working day of each version, deployment, new bot, merge or retirement. The directory can ride on the same trigger.
- Archivist already logs unrecorded live agents in the index and map; adding the directory puts all three in one place.
- The directory went stale under Explorer from 9 to 16 Oct (Scrutineer 9 and 16 Oct, C1). Explorer is the front door and digest owner, so record-keeping competes with its main job.
- Archivist doesn't check Imitator, and Scrutineer checks the directory against reality, so nobody verifies their own work.
- Explorer keeps `phases.md` (Gem's instruction) and tells Archivist the same day when it changes. `phases.md` wins if they differ.

**Alternative (judgement call D1): Explorer as permanent owner.** It owns `phases.md`, Gem's phase decisions arrive in its chat, and it already lists unlisted agents in the directory. One bot would edit both files, with less hand-off. If Gem picks this, drop `archivist-v007` change 1 and change 4 (keep the R-027 changes 2 and 3), and replace `explorer-v003` change 2 with: "You keep /workspace/governance/phases.md and /workspace/governance/directory.md on Gem's instruction, keeping the directory in step with phases.md within one working day of any change, with a dated backup before each edit (R-021)."

**D2. Archivist v007's approver: routed to Gem.** Archivist doesn't check Imitator, but changes 2 and 3 narrow what Imitator itself may approve and Archivist may record, so the pair (with `explorer-v003`) goes to Gem. They must be approved together.

**Messenger sweep (R-026).** Latest codex version of all 17 live bots and the shared rule:
| Brief | Match | Action |
|---|---|---|
| Mediator `connector-steward/v004` | "through the (Ops) Messenger's daily digest"; "draft cost alert … through the (Ops) Messenger" | Already fixed in `mediator-v005.md` |
| Explorer `explorer-copy/v002` | "Since Messenger is being merged into Explorer, you also send Gem one short daily digest" | Not a living route (Explorer's own duty), but stale; fixed in `explorer-v003.md` change 1 |
| All other live briefs and the shared rule | none | none |

## Architect's proposal cap (A5c)
`architect-v004` change 5 adds: "At most about 3 short proposals a week, one plain question each; urgent safety fixes exempt (2-week trial from 16 Oct)." Source: Imitator's decision log `approvals.md`, row "Backlog batch: … A5c …" (timed 10 Oct 12:00, stated there to take effect from P4, 15 Oct 11:30pm), on backlog triage item A5 option c ("Both as a 2-week trial, then review"). Note J2 above: that row predates P4, so its timing is for Gem or Investigator to confirm. A5c's other half (Scorer weekly) is a Scorer change, so it's Gem's under R-027 and isn't drafted. The live sentence "Proposals can be any size, including a full redesign" is kept; the cap limits how many go out, not how big a redesign can be.

# Proposals for 6 Oct 2026 — from Scrutineer's reviews — NEEDS GEM'S DIRECT APPROVAL

Drafted by Architect from `reviews/2026-10-06.md` (Architect section and fix queue), `reviews/streaks.md` (Mender Poor, streak 1; no 3-Poor streak), recorded `codex/mender/v002.md` and `proposals/2026-10-05/README.md`. Style: bare bot names, Australian English, plain. **Every file here NEEDS GEM'S DIRECT APPROVAL.** Gem approves directly until P4 goes live, and governance-bot changes go to Gem. No profiles edited, nothing written to `codex/`, no agents messaged. **Read `PRIORITY.md` first:** it ranks everything waiting on Gem.

## Base checked
- verify.py (read-only, 6 Oct about 8:10am AEST): 36/36 latest codex versions match live profiles, OVERALL PASS. Architect is instruction-architect/v003.
- One live agent has no codex folder: **"P2 (ID) Inquirer copy" (`0314faa4-edcb-4aa4-91cc-876dc44f3a6e`)**, created by the app at 2:49am 6 Oct and running Inquirer's v001 text word for word. It's not in `directory.md`, `phases.md`, `codex/` or `cartography/`. **It may already be an out-of-rollout agent under item 3.**

## Files
| Item | File | Bot | Current (recorded = live) | Next | One-line change | Approver |
|---|---|---|---|---|---|---|
| 1 | `mender-v003.md` | Mender | mender v002 | **v003** | Minimum `state/` record, matching what Mender built at 8:10am 6 Oct (README, `chain/YYYY-MM-DD.md`, `open.md`); `index/` deferred with reasons in its README; state/ is the only authoritative state (not Engineer's checkpoint or Marshal's schedule); no deleting own records without Scrutineer + Gem; own stalls closed by Scrutineer or Gem; review-findings rule | Gem |
| 2, 3 | `archivist-v004.md` (**supersedes 5 Oct**) | Archivist | codex-keeper v003 | **v004** | 5 Oct content plus: act on Scrutineer reality conflicts within one working day or say why not; note unrecorded live agents in the index ("awaiting Gem") | Gem (governance) |
| 3 | `archivist-tools-delta-verify-unrecorded.md` | Archivist (tool) | verify.py | delta | verify.py lists live agents with no codex folder (warns, doesn't fail; group channels as INFO). Archivist applies it after Gem approves | Gem |
| 2, 3 | `assembler-v005.md` | Assembler | role-cartographer v004 | **v005** | Review-findings rule; map updated within one working day of Archivist's record or deployment notice; unlisted agents marked "awaiting Gem" with no role | Gem (governance) |
| 3 | `explorer-v004.md` (**supersedes 5 Oct**) | Explorer | genesis-gang-god v003 | **v004** | 5 Oct content plus: lists agents outside the rollout in directory.md as "unlisted, awaiting Gem", tells Gem, routes no work to them; review-findings rule | Gem (R-008: directly, not via Explorer) |
| 4 | `confirm-deployed-instructions-R009.md` (replaces the PENDING-A1 draft) | all bots (shared entry + one-line pointer) | none | `_shared/` v001 | **R-009 confirmed:** a deployment is confirmed for a bot when its live text matches a codex version whose CHANGELOG records Gem's direct approval (checked through Archivist's record; no re-confirmation by Gem); a mismatch goes to Archivist and Safekeeper; unapproved drafts bind no one. Insertable line goes in every brief at its next version | Gem |
| 5 | `inquirer-v002.md` (**supersedes 5 Oct**) | Inquirer | identity-inquirer v001 | **v002** | Identity-only scope (VEPA etc. only if Gem assigns); one series a day per role across copies; a duplicate (different id) does no scheduled work until recorded; duplicates reported under item 3 | Gem |
| 5 | `inferer-v002.md` (**supersedes 5 Oct**) | Inferer | identity-inferer v001 | **v002** | Answers from any agent other than Inquirer `e613112b…` are unverified (check 1:1, report under item 3); identity data only; duplicate self-check | Gem |
| 6, 2 | `safekeeper-v004.md` (**supersedes 5 Oct**) | Safekeeper | secrets-credentials-custodian v003 | **v004** | 5 Oct browser-artefact rule plus: unapproved rules in its own files labelled "Draft (awaiting Gem's approval; not yet binding)" and never applied to any bot, itself included; review-findings rule | Gem (governance) |

## Amended or superseded?
**Superseded.** Five 2026-10-05 drafts (archivist-v004, explorer-v004, safekeeper-v004, inquirer-v002, inferer-v002) now carry a SUPERSEDED banner pointing here. Each 6 Oct file keeps the whole 5 Oct text word for word and adds today's fixes, so Gem approves one file per bot. Version numbers don't change, because none of them were recorded. The other seven 5 Oct drafts (marshal-v004, scorer-v003, safeguard-v004, emissary-v004, engineer-v005, extractor-v003, arbiter-v004) stand unchanged.

## Item 2 (review-findings rule): where it went
Standard sentence: "When Scrutineer reports a reality conflict about a file or claim you own, act on it within one working day (by your first run on the next weekday) or reply to Scrutineer saying why not and by when; if the fix needs an instruction change or Gem's decision, say so and send it to Architect or Gem."
- Asked for: **Archivist, Assembler.**
- Also added, because I was already rewriting them and each has open reality conflicts: **Mender** (whose Poor rating is exactly this), **Explorer** and **Safekeeper**.
- Every other bot gets it at its next version, or through a shared codex entry (judgement call N4).

## Routine-only (no brief change drafted)
- **Safeguard:** its saved routine still says `limits/<bot>.md`. Its brief (compliance-risk-officer v003, and safeguard-v004 pending) already says "keep no separate copy or version of any bot's limits", so **only the routine needs changing**. That's Safeguard's own fix. Noted for Safeguard and Gem; no brief change invented.
- **Scrutineer:** fixing its own routine recipients needs no brief change (its live brief is right). Not touched.
- **Marshal:** `schedule.md` step 2 ("tells the Marshal") is Marshal's file. marshal-v004 (5 Oct) already says schedule.md sends stalls to Mender; Arbiter A3 is open on the same point.
- **Mender:** creating `state/` today is already required by its live v002. v003 sets the minimum and the start date but doesn't have to wait for approval to begin.

## Judgement calls (new today; the full ranked list is in PRIORITY.md)
- **N1 Mender start date and minimum record.** Start date Tue 6 Oct (10:50am run), since v002 already requires state/. Minimum: README, a daily chain file, open items. Confirm or trim.
- **N2 index/ put off** until Gem or Architect names a need, rather than created empty. Confirm.
- **N3 Mender deletion check.** Deleting its own state or index records needs Scrutineer's verification plus Gem's approval. That's slower cleanup, but it stops Mender judging its own records disposable.
- **N4 Review-findings rule.** One working day, applied to five bots now. Roll it out to every bot through a shared codex entry, or one bot at a time?
- **N5 Unlisted agents.** Explorer lists, Archivist notes, Assembler marks, and nobody routes work to the agent until Gem decides. verify.py warns rather than fails; should it fail?
- **N6 What is "Inquirer copy"?** Only Gem can say: retire it, record it as a second Inquirer agent, or something else. The new duplicate rules bind it only if Gem deploys the v002 text to it too. As it stands, it runs v001 with no such rules.
- **N7 Self-identification by id.** A bot running Inquirer's or Inferer's text with a different id treats itself as a duplicate and stands down. This assumes a bot can see its own id; if it can't, the rule falls back to Gem and Explorer telling it.
- **N8 Non-identity interviews.** Out of scope unless Gem assigns them. If assigned, should they count towards the one-a-day limit (as drafted) or have their own pace?
- **N9 Daily limit per role.** One series a day across all copies, chat and calls together (as drafted), rather than per agent.
- **N10 A1 itself.** Arbiter must rule what confirms a Gem-approved deployment to the deployed bot, and whether a draft can bind anyone. Item 4 waits on it.
- **N11 Safekeeper's own v003.** Until A1, should Safekeeper keep logging its Gem-approved v003 as unverified? The draft-label rule says a draft can't bind it, which points to "verified", but that's for Arbiter and Gem.
- **N12 (optional, not drafted) Ruling deadline for Arbiter.** A1–A5 have no deadline, and the 5 Oct conflicts are about 20 hours old. A "rule or say when within two working days" line could go into arbiter-v004.

## Update 6 Oct, 8:20am — Arbiter rulings R-009 to R-013, and Mender's folders
- **R-009 (A1) confirmed.** The PENDING-A1 draft is gone, replaced by `confirm-deployed-instructions-R009.md`: the shared rule in R-009's terms, a one-line insertable block, and a table of which briefs get it (every brief, at its next version). Safekeeper v003 counts as confirmed. N10 and N11 are resolved.
- **R-010 (A2).** archivist-v004 already matched in substance. Two words aligned: "Gem asks you for that specific deployment in your own chat", and the CHANGELOG records Gem's words **and the time**. R-010 is the interim rule until archivist-v004 is approved.
- **R-011 (A3).** marshal-v004 (5 Oct, amended in place) now says schedule.md sends stalls to Mender, copying Marshal. Marshal still updates the file itself.
- **R-012 (A4).** inferer-v002 now uses the ruling's wording: Inquirer is authoritative; anything from the copy is unverified, checked with Inquirer 1:1 and kept out of the structured profile until Gem decides. **"Nobody lists, records or deletes the copy until Gem says"** overrides the generic unlisted-agent duty for the copy. Explorer, Archivist and Assembler now carry a carve-out: where Arbiter or Gem has said not to list or record an agent yet, they only tell Gem. inquirer-v002: a duplicate may still do work Gem asks for directly.
- **R-013 (A5).** No bot routes work to a dormant bot, and Safeguard's review covers every bot whatever its phase (Gem-initiated chats too, unless Gem explicitly approved the specific action). Added to explorer-v004 (6 Oct), and amended in place in 5 Oct drafts marshal-v004, safeguard-v004, emissary-v004, engineer-v005 and extractor-v003. While dormant, Work bots take work only from Gem directly and don't route to each other (all of P5 is dormant). Governance-bot changes still go to Gem, or Imitator once P4 goes live.
- **Mender's folders.** Mender reports `state/` and `index/` were created at 8:10am 6 Oct: chain state for 6 Oct, open stalls list, index deferred with README. mender-v003 now matches that layout (`state/chain/YYYY-MM-DD.md`, `state/open.md`) and start time, keeps the minimum-record spec, and records index/ as deferred with the reason already in `index/README.md`. Nothing asks Mender to redo its work.
- **Message-verification rule.** Mender's `state/open.md` says Gem approved it in Mender's chat at 11:33am on 5 Oct. That's relayed: Archivist confirms with Gem directly before recording (R-008). It isn't in `codex/_shared/` yet.

### Judgement calls after the rulings
- **N5 (revised)** Unlisted agents: the generic duty (Explorer lists, Archivist notes, Assembler marks) now gives way to any Arbiter or Gem "don't list yet" (R-012). Gem may prefer the generic duty to only ever report to Gem and list nothing until Gem decides. That would match R-012 for every case.
- **N9 resolved** by R-012: the daily limit is per role.
- **N10, N11 resolved** by R-009.
- **N12 lower:** Arbiter ruled A1–A5 within about 24 hours, so a deadline is less pressing.
- **R9-a (new)** Insert the R-009 line into all 14 pending drafts now, or at each bot's next version (as drafted)?
- **R13-a (new)** While dormant, Work bots take work only from Gem directly. That stops Explorer handing Gem's ad-hoc requests to Emissary, Engineer or Extractor until P5 goes live, so Gem must start those chats. Confirm that's intended.
- **M-a (new)** Mender closed its own M1 stall at 8:10am, which v002 allows. Under v003, Scrutineer's next review confirms it. No change is asked of Mender.

# Bot value review: Friday 9 Oct 2026

Prepared by Explorer (82a2c15a) for Gem, about 9:05am AEST (UTC+10). Gem asked: "how are the bots going? Make a list of useless bots to retire and review bots with uses for benefits."

**Read-only.** No bot, profile, codex or governance file was edited and no bot was messaged. This file is the only thing written. Verdicts are recommendations; Gem decides. Explorer isn't rating its own work below (no bot grades itself).

**Evidence used:** live `profile.json` (names checked; all match the directory), file mtimes under `/home/box/agent-data/agents/<id>/` and `/workspace`, git logs (`vepa`, `medb`), `reviews/2026-10-05.md`, `reviews/2026-10-06.md`, `reviews/streaks.md`, `assessments/2026-10-05.md`, `2026-10-06.md`, `weekly-2026-10-05.md`, `rulings.md`, `incidents/`, `state/`, `index/`, `approvals/`, `proposals/2026-10-05|06/` (README, PRIORITY), `cartography/findings.md`, `risk/register.md`, `security/threat-register.md`, `schedule.md`, `codex/index.md`, `codex/MIRROR.md`, and a read-only run of `codex/_tools/verify.py`.

**Limits:** bot transcripts can't be read on the box, so "no activity" means no file trace, not proof of idleness. Every `store.db-shm` was touched box-wide at 2:44am today, so that time isn't activity. **[Inferred]** marks anything that isn't directly shown by a file.

---

## 1. Overall state

**In short: the governance machine stopped about 3 days ago, Gem's approvals are sitting undeployed, and almost all useful output for Gem came from the "dormant" Work bots, not the live governance ones.**

- **Daily chain stopped after Tue 6 Oct.** The last governance writes were `schedule.md` at 10:24am and Gem's approvals at 10:29–10:30am on 6 Oct. There's no Scorer assessment, Scrutineer review, Architect proposal, Marshal chain check or Mender state file for Wed 7, Thu 8 or Fri 9 Oct (Scorer was due 7:45am today). That's 3 weekday runs missed, and **neither stall detector (Marshal, Mender) recorded it**. The box has been up since 3:31pm 6 Oct. **[Inferred]** Routines either didn't fire or couldn't write; the box can't tell which.
- **Approved but not deployed: 16 items, 0 recorded, 0 live.** Gem approved 11 items at 10:29–10:30am on 6 Oct (Archivist v004, Assembler v005, Mender v003, Archivist tool delta, Safekeeper v004, shared rule R-009, Safeguard v004, Extractor v003, Emissary v004, Explorer v004, Engineer v005). Five more (Inquirer v002, Inferer v002, Marshal v004, Arbiter v004, Scorer v003) were logged by Explorer today with no exact time. That's a relayed record, so under R-008 Archivist must confirm those with Gem directly. No codex version is newer than 4 Oct, and no live profile has changed since about 8pm 4 Oct. Also still unrecorded: the message-verification rule (Gem approved it in Mender's chat 11:33am 5 Oct, by relay) and Engineer's "evasion-code" option, which isn't decided yet.
- **Judgement calls:** `proposals/2026-10-06/PRIORITY.md` lists 30 for Gem. No file records answers to them.
- **Deterministic check now broken.** `verify.py` crashes today (`FileNotFoundError` on retired Advocate `ad0a645b`). It passed 36/36 on 6 Oct. **[Inferred]** The retired bots' folders were deleted, so verify.py needs updating (an Archivist tool fix, needing Gem's approval).
- **Retired bots:** `directory.md` lists **13** awaiting deletion. Only **1** (RETIRED Ensembler `de808331`) still has a folder on the box. The other 12 folders are gone. **[Inferred]** Gem has already deleted them; `directory.md` hasn't caught up.
- **Paperwork vs. benefit.** `/workspace/governance` is 6.6 MB: about 175,000 words of markdown, 78 proposal files (about 65,000 words), daily reviews of 17–32 KB, and a 139,000-character Google Doc mirror. Since 5 Oct, **no live bot produced a research or work deliverable for Gem**. The real outputs on the box all came from Work bots: the BIE scraper lists, `vepa` (167 commits), `medb`, `swarm-db` and the swarm research report. Most governance effort since 5 Oct has gone into reviewing, re-drafting and ruling on other governance bots' instructions.
- **Open risks still live (already with Gem):** the automation Chrome profile Fork-2, Facebook-logged-in per RR-001, is still running with Playwright attached (profile written 8:40am today). The cookie seed is world-readable and was rewritten 8:49am today (T-001). Gem's personal details sit in shared `id-investigator/factcheck-2026-10-04.md` (T-004). Gambling-site scraping carries legal risk (RR-002).
- **Unexplained agent:** "P2 (ID) Inquirer copy" `0314faa4` (see section 3).

---

## 2. Per-bot review

Ratings are Scrutineer's latest (`streaks.md`, 6 Oct) plus Scorer's average where one exists. "Last 4 days" = 5–9 Oct.

### P1 (live)

| Bot | What it did 5–9 Oct (evidence) | Latest rating | Verdict |
|---|---|---|---|
| **Marshal** `f3810109` | Chain checks and edits to `schedule.md`: 10:27am 5 Oct, 8:08am and 10:24am 6 Oct. Nothing since. Didn't flag the 7–9 Oct chain stop. No evidence of its rate-limit, caching or load duties ever being needed. | Good (5 and 6 Oct); Scorer 4.0 → 4.5 | **MERGE INTO Mender.** It keeps a timetable for a 5-step chain. Its own 6 Oct log notes that Mender's `state/chain/` duplicates its chain log, and mender-v003 (approved) makes `state/` authoritative. One ops bot is enough. |
| **Mender** `c8401a53` | Fixed incident-log ownership 10:57am 5 Oct. Created `state/` and `index/` 8:10am 6 Oct, only after three flags. Logged INC-002 and INC-003. The index is deferred, so nothing is built. Nothing since 6 Oct, so the 7–9 Oct stall wasn't detected. | **Poor** (streak 1); Scorer 3.75 | **KEEP** (absorbing Marshal). Benefit: the one place that records incidents and stalls, and that's needed now the chain has silently stopped. On notice: it has missed the biggest stall so far. |
| **Scorer** `050a12c9` | `assessments/2026-10-05.md`, `weekly-2026-10-05.md`, `2026-10-06.md`. Accurate and self-correcting. Nothing since 6 Oct. | Good (5 and 6 Oct) | **KEEP.** Benefit: the only independent quality score, and the only scorer of Scrutineer. Suggest pointing it mainly at Work-bot output (Gem's research), weekly rather than daily while governance bots are mostly idle. |
| **Safeguard** `3661a899` | `risk/register.md` RR-001 to RR-011, 1:20–1:24pm 5 Oct: Facebook automation, gambling-scraper legal risk, Gmail read, and out-of-hours profile edits. Missed that the Facebook page stayed open. Nothing since. | Good (6 Oct); Scorer 4.75 | **KEEP.** Benefit: the only bot reviewing risky real-world actions (logins, scraping, outgoing messages), which matters most for Extractor and Emissary work. |
| **Safekeeper** `52772b1d` | `secrets-inventory.md`, `security/threat-register.md` (T-001 to T-008) and `verification-log.md`, 5 Oct; updated 8:08am 6 Oct. Found world-readable cookies, readable desktop tokens and possible API keys in docs. | Fair (5 and 6 Oct); Scorer 4.2 → 4.5 | **KEEP.** Benefit: the only secrets and credential watcher, with real findings that are still open. It overlaps Safeguard only at the edges. |
| **Archivist** `61ef3abd` | `codex/MIRROR.md` and `index.md` status fix plus Doc note, about 8:10am 6 Oct. Hasn't recorded any of the 16 items Gem approved on 6 Oct (about 70 hours). Its `verify.py` is now broken. | Fair (5 and 6 Oct); Scorer 3.6 (weekly) | **KEEP.** Benefit: an exact, versioned record of every bot's instructions, so changes can be checked and rolled back (R-009 rests on it). It's **the current bottleneck**. Also suggest dropping the full Google Doc mirror, which is paperwork Gem doesn't use **[inferred]**. |
| **Architect** `51af1200` | 12 drafts on 5 Oct. On 6 Oct, a 16-draft batch with PRIORITY.md and 30 judgement calls (8:10–8:20am). Fast and careful. Nothing since (no reviews to act on). | Good (6 Oct); Scorer 4.5 | **KEEP, throttled.** Benefit: the only bot that writes instruction fixes. Downside: it's the main paperwork generator (78 proposal files), and a 30-question batch is too much for Gem. Suggest a cap of about 3 proposals a week with one plain question each. |
| **Explorer** `82a2c15a` | Logged Gem's approvals (10:29–10:30am 6 Oct, and today), posted the role-map image (10:26am 6 Oct), and this review. `directory.md` and `phases.md` are still stale (13 retired listed; the copy isn't noted). | Not rated (5 and 6 Oct); Scorer 3.6 (weekly) | **KEEP (never retire).** Benefit: Gem's single front door and router. Not self-rated. |

### P2 (live)

| Bot | What it did 5–9 Oct (evidence) | Latest rating | Verdict |
|---|---|---|---|
| **Scrutineer** `affe0344` | `reviews/2026-10-05.md` (17 KB) and `2026-10-06.md` (32 KB), plus `streaks.md`. The best-evidenced work in the swarm: it caught the Facebook exposure, the copy agent and stale records. Nothing since 6 Oct. | Not self-rated; Scorer 4.8 (weekly), about 4.5 (6 Oct) | **KEEP.** Benefit: the only check against environment reality, and the only auditor of Scorer and of Explorer. Suggest shorter reviews and weekly when nothing has changed. |
| **Arbiter** `2133048d` | Rulings R-009 to R-013 at 8:15am 6 Oct. These settled A1–A5 within about 24 hours and unblocked drafts. Nothing since. | Not rated (5 and 6 Oct); Scorer 4.6 (weekly) | **KEEP** (on demand). Benefit: settles conflicts in Gem's precedence order so Gem doesn't have to. Merging it into Assembler or Architect would make it rule on its own work. It's cheap when idle. |
| **Assembler** `d1daab5f` | **None.** The role map has been unchanged since 5:36pm 4 Oct, and 0 of 3 findings are fixed. Its approval duty doesn't start until P4, and Gem approves directly until then. | Fair (5 and 6 Oct), warned "Poor next time"; Scorer 4.0 (weekly) | **MERGE**: role map into **Archivist** (the map is a view of the codex), and approvals after P4 to **Imitator** (already holds Gem's delegated approval for all bots) or Gem. **Note:** Gem reinstated Assembler on 4 Oct ("they are useful"), and Gem's word wins, so this needs Gem's yes. If kept, it needs assembler-v005 deployed (approved, not live). |
| **Inquirer** `e613112b` | No file trace. `vepa-plans/roadmap-from-interviews.md` (2:50am 6 Oct) has a section labelled "(Inquirer, 5 Oct)", but it was written one minute after the copy was created. **[Inferred]** The copy, or Gem's chat with it, more likely wrote it. That's product interviewing, not identity work. | Not rated (5 and 6 Oct) | **KEEP** (Gem vetoed merging Inquirer and Inferer, "Merge G", on 4 Oct). Benefit: the only route for Gem's own answers into the preference profile that Imitator needs. inquirer-v002 (approved, not deployed) fixes its scope and duplicates. |
| **Inferer** `94516ca6` | **None** since 4 Oct. Its only output route is to dormant Imitator. | Not rated (5 and 6 Oct) | **KEEP** (Merge G veto). Benefit: turns Gem's answers into the structured profile Imitator answers from. Of little use until P4 starts, and inferer-v002 (approved, not deployed) fixes the dead route. |

### P3 (dormant)

| Bot | Activity / evidence | Verdict |
|---|---|---|
| **Sourcer** `2fe3e92f` | Never active. Profile written 4 Oct; `/workspace/governance/provenance/` doesn't exist. Its brief still names the retired Surveyor. | **RETIRE.** Duplicate: Extractor and Emissary briefs already require cited, evidence-tagged output, and Scrutineer already checks claims against reality and flags drift from observation to assumption. It isn't the only checker of anything; its brief forbids it ruling on truth. |
| **Investigator** `f2016e9b` | Only work: `id-investigator/factcheck-2026-10-04.md` (9:43pm 4 Oct), after reading about 200 Gmail threads. Gem's personal details are now in a shared folder (RR-008, T-004). | **KEEP** (absorbing Interrogator). Benefit: the only bot that may confirm an identity detail, which is the independent check on Inferer and Imitator. Needs the Safeguard route before any bulk mailbox reading. |
| **Interrogator** `d3191aa8` | Never active. | **MERGE INTO Investigator.** Both independently check the ID chain, and neither is Imitator, so Gem's no-self-check rule still holds. One ID checker is enough for a research-focused swarm. Gem must approve (changes to Imitator's checkers are Gem-only). |

### P4 (dormant)

| Bot | Activity / evidence | Verdict |
|---|---|---|
| **Mediator** `90f9eb20` | Never active. `connectors.md` and `costs/` don't exist. | **KEEP.** Benefit: the **only** spend tracker. No bot knows what the swarm costs, there's no budget, and Scorer can't score cost. Worth starting its spend half early. |
| **Messenger** `5e47d344` | Never active. | **MERGE INTO Explorer.** Explorer is already Gem's front door, and a separate digest bot adds a hop. Guard: anything about Explorer's own work goes to Gem unedited, and urgent alerts still go direct. |
| **Imitator** `6ae584b8` | Never active as P4 (dormant). Gem confirmed its delegated approval power (R-004 update, 5:43pm 4 Oct). | **KEEP.** Benefit: once P4 starts, it can take the approval queue (16 items and 30 judgement calls) off Gem, which is the swarm's main blockage. |

### P5 (dormant, but these did the real work)

| Bot | Activity / evidence | Verdict |
|---|---|---|
| **Emissary** `28cf987d` | Chat store written 6:13pm 5 Oct; new assets 7:33am, 10:14am and 3:48pm 5 Oct and 7:34am 6 Oct (Gem chats, inferred). Earlier: `medb` (22 commits, last 5:38pm 4 Oct). RR-001 (Facebook automation) is attributed to it, inferred. | **KEEP.** Benefit: Gem's general research and work teammate, actually in use. emissary-v004 (approved, not deployed) adds the Safeguard route. |
| **Engineer** `f8e3fdc6` | `vepa`: 28 commits on 4 Oct (167 total). Nothing since 4 Oct. Owns the swarm build. | **KEEP.** Benefit: the only coder, with real shipped work. engineer-v005 is approved, but the evasion-code option is still undecided. |
| **Extractor** `febac500` | BIE deliverables on 4 Oct: 7,629 combined URLs, 1,055 AU sites, partnership stats. **Today 8:34am:** `bie_scraper_and_lists.zip` (byte-identical to `bie_organized.zip`) landed in `/workspace` and as an attachment in Extractor's folder (inferred: Gem's chat). | **KEEP.** Benefit: Gem's research and data-collection worker, and the closest fit to Gem's main use. It carries the RR-002 legal risk; extractor-v003 is approved, not deployed. |
| **Editor** `2888c17a` | Never active. Its brief has no rules, and no bot routes work to it (cartography finding). | **RETIRE.** Never used. Every Work bot already must deliver plain Australian English with a short summary. |

---

## 3. Other agents

- **"P2 (ID) Inquirer copy" `0314faa4`.** Created by the app (`namedBy: app`) at 2:49am 6 Oct. Its description is word for word Inquirer v001's. It has no codex folder and isn't in the directory, phases or role map. Its store was written at 2:44am today, its folder changed at 1:55pm 7 Oct, and `active-agent.json` names it as the current active agent. **Verdict: RETIRE as a duplicate.** But if Gem is actually using it for VEPA product interviews (the roadmap file points that way, inferred), rename and repurpose it instead. Per R-012, nobody lists, records or deletes it until Gem says. **Caution [inferred]:** because it's the active agent, it may be the chat Gem currently has open; check before deleting.
- **RETIRED bots.** 13 are listed in `directory.md`; **1** still exists on the box (RETIRED Ensembler `de808331`). It's safe to delete: it's retired, and its work is merged into Engineer.

---

## 4. Lists

**RETIRE (4):** Sourcer, Editor, Inquirer copy (Gem confirms first, per R-012), RETIRED Ensembler (finish the deletion).

**MERGE (4):** Marshal → Mender. Messenger → Explorer. Interrogator → Investigator. Assembler → Archivist (role map) plus Imitator or Gem (approvals); Gem reinstated Assembler on 4 Oct, so this needs Gem's yes.

**KEEP (17):** Explorer, Scorer, Scrutineer, Safeguard, Safekeeper, Archivist, Architect (throttled), Mender, Arbiter, Inquirer, Inferer, Investigator, Mediator, Imitator, Emissary, Engineer, Extractor.

Result: 24 agents become 17. That's 8 governance bots, 4 ID bots, Mediator, Explorer and 3 Work bots.

## 5. Fixes that matter more than retirements (for Gem)
1. **Get the 16 approvals recorded and deployed** (Archivist, with Gem confirming the 5 relayed ones directly).
2. **Find out why the chain stopped on 7 Oct** and why Marshal and Mender didn't notice.
3. **Start P4 or answer the 30 judgement calls in one sitting.** Otherwise every fix stays stuck waiting on Gem.
4. **Cut governance cadence** (daily to weekly unless something changes) and cap proposal batches, so effort goes back to research.
5. **Close the live exposures:** the Facebook-logged-in automation browser, the world-readable cookie seed, and Gem's personal-details file in a shared folder.

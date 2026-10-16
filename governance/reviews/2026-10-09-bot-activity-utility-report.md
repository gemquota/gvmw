# Bot activity and utility report: Friday 9 Oct 2026

Prepared by Explorer (04dcca0d) for Gem, about 6:25pm AEST (UTC+10). Read-only apart from this report and its CSV, PNG and the cleanup plan. No bot was messaged. Explorer lists its own activity but gives itself no utility score (no bot grades its own work).

Files: `2026-10-09-bot-activity-utility.csv` (table) and `2026-10-09-bot-activity-utility.png` (chart), same folder.

## In short

- **Engineer is now the most useful bot, and the busiest.** 25 vepa commits today (9:06am to 6:00pm), test builds sent to Gem at 12:21pm and 5:55pm, and decisions D-030 to D-035 recorded today (D-034 and D-035 stamped as Gem's, 4:29pm and 6:00pm). It moves to #1, Extractor to #2.
- **Architect is the clearest overhead case.** Activity index 53, utility 1. It has written 88 proposal files, about 73,000 words. Archivist is next (index 63, utility 4): about 91,000 words of codex and 6 versions of every role-map image.
- **Governance paperwork has grown to about 239,000 words** of markdown in 458 files (up from about 175,000 words in this morning's review). Only Scrutineer, Safeguard and Safekeeper turn much of it into catches.
- **The 6-8 Oct stall wasn't a bot failure.** Mender's chain file for 8 Oct and Safeguard's register say the routines stopped because of an unpaid Cursor invoice. That changes this morning's "neither stall detector noticed" point.
- **No dollar figures exist.** Mediator's ledger says so plainly. None are invented here.

## 1. Method

**Sources:** every file under `/workspace` (except my own outputs); git logs of `vepa` and `medb`; each live agent folder under `/home/box/agent-data/agents/` (file counts, sizes, mtimes, and the count of `transcript_entries` rows in `store.db`, opened read-only); `schedule.md`; `state/`; `costs/ledger.md`; the 9 Oct value review; Safeguard's, Safekeeper's and Scrutineer's registers and reviews.

**Attribution (who wrote what):**
- Governance by folder and header: `assessments/` Scorer; `reviews/` and `audits/2026-10-03` Scrutineer; `risk/` Safeguard; `security/` and `secrets-inventory.md` Safekeeper; `codex/` Archivist; `cartography/` v1-v3 Assembler, v4 on Archivist (headers say so); `proposals/` Architect, except `2026-10-09-retire-merge/` old Explorer; `rulings.md` Arbiter; `state/`, `index/`, `incidents/` and `schedule.md` Mender (old schedule backups Marshal); `costs/` Mediator; `approvals/` (Gem's words), `directory.md`, `handover/`, the value review and `bot-landscape-review.md` old Explorer; `phases.md` (9:15am update) new Explorer.
- Work: `vepa` files touched by a "Codey (local, for Gem Quota)" commit, plus `perf/`, `out/`, `tools/`, `codey/` and `vepa-plans/` → Engineer. vepa files only touched by human upstream authors (Dayne Keefe, freebuff-web[bot]) are left out. `medb*` → Emissary (commits by "Grok Bot for Gem Quota" = Emissary's old name). `bie*`, `orig_v2/` and the loose root logs and scripts → Extractor. `vepa-plans/roadmap-from-interviews.md` → Inquirer 0314faa4 (inferred, as in this morning's review). Sha256 matches between workspace files and each bot's `attachments/` confirmed Engineer, Emissary and Extractor ownership.
- Machine output is counted separately and not as authored work: scraper caches, `bie_tools/pstats/`, `node_modules`, toolchains, `vepa/dist`, `medb/runs`, `medb/experiment/envelopes`.
- Unattributed: `.playwright-mcp/`, `agent-tools/`, `swarm-db/`, `grok-swarm-research/`, `profile.txt`, `urls.txt` (135 files, 93 MiB).

**Dates.** The box restarted at 10:37am today and file mtimes were reset to 10:37-10:43am. So "last 7 days" (3-9 Oct) uses the best content date: git commit date; a date in the file name or header; BIE zip entry dates (4 Oct); a real mtime after 10:45am today. BIE files with no date get 4 Oct (inferred).

**Activity index (0-100).** Six measures: authored files, authored KB, files dated 3-9 Oct, markdown words, git commits, and items in the agent folder (attachments, assets, voice calls, transcript entries). Each is log-scaled against the live maximum (`log(1+x)/log(1+max)`). The index is the mean of the six, rescaled so the top bot = 100. Log scaling stops 8 GiB of caches or 500 files from drowning everything else.

**Utility (1-10)** = 1 + D + U + C − O, capped 1-10:
- **D, deliverables Gem used (0-5):** real output Gem took up (lists, code, builds, a repo, decisions).
- **U, unique role actually used (0-2):** 2 = only bot doing it and the role is in use; 1 = some overlap, or the role is dormant or unused.
- **C, catches or prevented problems (0-2):** risks, threats, audit findings, regressions stopped.
- **O, overhead (0-3):** paperwork volume and the clean-up or review load it causes others.

**Ratio** = utility ÷ max(activity index, 5), divided by the median of the 16 scored bots, so median = 1.0. The floor of 5 stops near-zero activity making the ratio blow up. Even so, **dormant bots score high ratios only because they do almost nothing.** Read their ratios as "cheap to keep", not "efficient".

**Output share** = the bot's activity index as a % of the sum across all 17 live bots (Explorer included).

**Limits (please read):**
- No usable transcripts. 15 of 17 `store.db` files have 0 transcript rows. Inquirer 0314faa4 has 1 (9 Oct 9:03am) and Emissary has 4 (3 Oct 10:04am, 4 Oct 10:09am, 1:54pm, 3:10pm). Chat effort that left no file is invisible here.
- Retired bots' folders are gone (INC-005, 9:20-9:26am today). Their activity is from /workspace content only.
- Agent-folder mtimes are mostly the restore time, so they aren't used as activity dates. Only Explorer (4:57pm upload) and Engineer (12:21pm and 5:55pm zips) show real folder writes today.
- Attribution by folder treats a file as written by its owner. A bot editing another bot's file (for example Explorer editing `directory.md`) is only caught where a header says so.
- Words and files measure volume, not quality. Utility scores are my judgement against the rubric, using evidence in files. They aren't measurements.
- Investigator's real output (14.6 KB fact-check) is in quarantine outside /workspace, so its activity is understated.

## 2. Ratio table (live bots, sorted by ratio)

| Bot | Activity index | Utility | Ratio (median = 1.0) | Output share | Rank now (was) |
|---|---:|---:|---:|---:|---|
| Inferer | 2.8 | 2 | 2.84 | 0.5% | 15 (16) |
| Imitator | 0.0 | 2 | 2.84 | 0.0% | 13 (11) |
| Safeguard | 21.7 | 6 | 1.96 | 3.6% | 4 (4) |
| Investigator | 8.1 | 2 | 1.75 | 1.3% | 14 (14) |
| Safekeeper | 24.2 | 5 | 1.47 | 4.0% | 5 (5) |
| Arbiter | 19.6 | 4 | 1.45 | 3.3% | 9 (13) |
| Scrutineer | 34.5 | 5 | 1.03 | 5.7% | 6 (6) |
| Inquirer | 20.9 | 3 | 1.02 | 3.5% | 11 (15) |
| Mediator | 21.7 | 3 | 0.98 | 3.6% | 10 (12) |
| Mender | 32.6 | 4 | 0.87 | 5.4% | 8 (9) |
| Extractor | 72.5 | 8 | 0.78 | 12.1% | 2 (1) |
| Engineer | 100.0 | 9 | 0.64 | 16.7% | 1 (2) |
| Emissary | 79.7 | 6 | 0.53 | 13.3% | 3 (3) |
| Scorer | 27.6 | 2 | 0.51 | 4.6% | 12 (8) |
| Archivist | 62.8 | 4 | 0.45 | 10.5% | 7 (7) |
| Architect | 53.0 | 1 | 0.13 | 8.8% | 16 (10) |
| Explorer (self) | 18.6 | not scored | n/a | 3.1% | n/a |

## 3. Activity detail (measured)

| Bot | Id | Authored files | KB | Files dated 3-9 Oct | Written today (mtime) | Md words | Governance words | Commits (3-9 Oct) | Agent-folder items | Schedule slots | Last dated output |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| Engineer | f8e3fdc6 | 518 | 13,873 | 465 | 268 | 145,654 | 0 | 123 (123) | 60 | 0 | 2026-10-09 |
| Emissary | 28cf987d | 157 | 5,976 | 43 | 0 | 24,479 | 0 | 22 (8) | 49 | 0 | 2026-10-04 |
| Extractor | febac500 | 288 | 28,352 | 273 | 0 | 26,945 | 0 | 0 (0) | 12 | 0 | 2026-10-04 |
| Archivist | 61ef3abd | 275 | 4,293 | 221 | 0 | 90,848 | 90,848 | 0 (0) | 1 | 0 | 2026-10-09 |
| Architect | 51af1200 | 88 | 666 | 64 | 0 | 73,309 | 73,309 | 0 (0) | 1 | 0 | 2026-10-09 |
| Scrutineer | affe0344 | 7 | 187 | 7 | 0 | 29,259 | 29,259 | 0 (0) | 0 | 1 | 2026-10-09 |
| Mender | c8401a53 | 15 | 31 | 14 | 0 | 4,821 | 4,821 | 0 (0) | 0 | 1 | 2026-10-09 |
| Scorer | 050a12c9 | 4 | 43 | 4 | 0 | 7,104 | 7,104 | 0 (0) | 0 | 2 | 2026-10-09 |
| Safekeeper | 52772b1d | 3 | 21 | 3 | 0 | 3,602 | 3,602 | 0 (0) | 0 | 0 | 2026-10-05 |
| Safeguard | 3661a899 | 2 | 24 | 1 | 1 | 3,428 | 3,428 | 0 (0) | 0 | 1 | 2026-10-09 |
| Mediator | 90f9eb20 | 3 | 9 | 3 | 0 | 1,456 | 1,456 | 0 (0) | 0 | 0 | 2026-10-09 |
| Inquirer | 0314faa4 | 1 | 10 | 1 | 1 | 1,518 | 0 | 0 (0) | 1 | 0 | 2026-10-09 |
| Arbiter | 2133048d | 1 | 16 | 1 | 1 | 2,619 | 2,619 | 0 (0) | 0 | 0 | 2026-10-09 |
| Explorer | 04dcca0d | 1 | 2 | 1 | 0 | 392 | 392 | 0 (0) | 2 | 0 | 2026-10-09 |
| Investigator | f2016e9b | 1 | 0 | 1 | 0 | 20 | 0 | 0 (0) | 0 | 0 | 2026-10-04 |
| Inferer | 94516ca6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 (0) | 1 | 0 | none |
| Imitator | 6ae584b8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 (0) | 0 | 0 | none |

Notes on the detail:
- **Engineer:** 123 Codey commits in vepa (70 on 3 Oct, 28 on 4 Oct, 25 on 9 Oct). 268 files written after the restore today. 60 items in its agent folder, including 6 vepa test-build zips (3, 4 and 9 Oct). Plus 667 MiB of machine files (Node toolchains, node_modules), not counted as authored. It has uncommitted work in progress at 6pm (NaN-energy fix, D-035).
- **Extractor:** 288 authored files, 28 MB (BIE lists, reports, scraper code). Plus 8.1 GiB of scraper caches (machine). 12 items in its agent folder, including the zips and CSVs Gem received. Last dated output 4 Oct.
- **Emissary:** 22 medb commits (14 on 2 Oct, 7 on 3 Oct, 1 on 4 Oct). 157 authored files, 49 agent-folder items (26 assets, 15 attachments, 4 voice calls, 4 transcript entries). Last dated output 4 Oct.
- **Archivist:** 275 files (codex versions, deploy manifests, Google Doc sync chunks, cartography v4-v6). 4 deploy manifests on 9 Oct (15 versions deployed per the cartography summary).
- **Architect:** 88 proposal files, about 73,000 words. Last batch 9 Oct (8 drafts).
- **Scrutineer:** 7 files, about 29,000 words (reviews of 17-34 KB each).
- **Schedule slots** (from `schedule.md`): Scorer 2 (weekday 7:45am, Monday 8:45am weekly), Scrutineer 1 (11:45am backup), Mender 1 (10:50am), Safeguard 1 (1:15pm). Mediator's 6:50am slot is parked. Every other bot is on demand.
- **Inferer:** no workspace files. One voice-call record in its folder (not opened). **Imitator:** nothing at all. **Investigator:** a 188-byte stub (real file in quarantine).
- **Explorer (self, 04dcca0d):** 1 governance file (the 9:15am `phases.md` update), 2 agent-folder items (upload at 4:57pm), RR-012 and RR-013 profile edits at 9:13-9:15am logged by Safeguard. Today's outputs aren't counted.

## 4. Utility scores and why

| Bot | D | U | C | O | Utility | Evidence |
|---|---:|---:|---:|---:|---:|---|
| Engineer | 5 | 2 | 1 | 0 | **9** | vepa: 123 commits, 25 today. Test builds to Gem (12:21pm, 5:55pm). Decisions D-030 to D-035 recorded today; D-034 and D-035 are stamped as Gem's (4:29pm and 6:00pm). Only coder. Its isolated verifier and golden hashes caught the NaN-energy bug before release. |
| Extractor | 5 | 2 | 0 | 0 | **8** | BIE lists: 7,629 URLs, 1,055 AU sites, partnership stats (4 Oct; counts from this morning's review, not re-checked). Gem re-shared the zip 9 Oct. Only scraper. Gambling-site scraping carries legal risk (RR-002), but that's risk, not paperwork. |
| Emissary | 4 | 2 | 0 | 1 | **6** | MedB M0 repo (22 commits), prior-work brief, used in Gem chats 3-4 Oct. Only general research teammate. O1: the Facebook-logged-in automation (RR-001) and the .playwright-mcp snapshots made clean-up work for others. |
| Safeguard | 1 | 2 | 2 | 0 | **6** | Risk register RR-001 to RR-016, scheduled run today 1:15-1:30pm. Its RR-001 led to Gem's 9:05am Facebook-snapshot deletion. Recorded the unpaid-invoice cause of the missed runs (first logged in Mender's 8 Oct chain file). |
| Safekeeper | 1 | 1 | 2 | 0 | **5** | Secrets inventory (42 rows) and threat register T-001 to T-009: world-readable cookie seed, sk- strings, token files. Overlaps Safeguard on privacy items, so U1. Nothing new since 5 Oct (on demand only). |
| Scrutineer | 1 | 2 | 2 | 1 | **5** | Daily reviews and today's deploy check. Caught the 9 agent folders going (INC-005) and the missing 7-8 Oct records. O1 for 30 KB reviews. |
| Archivist | 2 | 2 | 1 | 2 | **4** | Deployed 15 instruction versions on 9 Oct (4 manifests): that was Gem's top ask. Versioned codex makes rollback possible. O2: about 91,000 words, a Google Doc mirror, and 6 versions of each role-map image (7.2 MiB). |
| Mender | 0 | 2 | 1 | 0 | **4** | Only ops bot after merging Marshal. Logged INC-004 and INC-005 and today's chain state. The 6-8 Oct gap was the invoice, not Mender. No deliverable Gem uses directly. |
| Arbiter | 0 | 2 | 1 | 0 | **4** | 21 ruling entries, including R-016, R-017 and an R-012 update today (4:22pm). Settles conflicts so Gem doesn't have to. Low volume (one 16 KB file). |
| Mediator | 0 | 2 | 0 | 0 | **3** | Started today. Honest ledger: no spend data, nothing invented. Only spend tracker. No catches yet. |
| Inquirer | 1 | 1 | 0 | 0 | **3** | VEPA roadmap from Gem's interview answers (inferred). Referenced by `vepa-plans/feasibility-2026-10-09.md`, Engineer's input for VEPA planning. Still being edited at 6:17pm today. Overlaps Inferer. |
| Scorer | 0 | 1 | 1 | 1 | **2** | Daily assessments 5, 6 and 9 Oct plus a weekly. Noted the missed 8 Oct run. Mostly overlaps Scrutineer, and nothing Gem acts on directly. |
| Imitator | 0 | 1 | 0 | 0 | **2** | Dormant (P4). No output. Role reserved for taking Gem's approval queue later. |
| Investigator | 1 | 1 | 0 | 1 | **2** | One fact-check (4 Oct) after reading about 200 Gmail threads. It caused a privacy incident (RR-008, T-004) and quarantine work. |
| Inferer | 0 | 1 | 0 | 0 | **2** | No output since 4 Oct. One voice-call record. Its only output route is to dormant Imitator. |
| Architect | 1 | 2 | 0 | 3 | **1** | Only drafter of instruction fixes; 9 Oct drafts were deployed. But 88 files and about 73,000 words, with a 30-question batch for Gem on 6 Oct. Paperwork far outweighs use. |

## 5. Updated ranking and changes from this morning

| Rank | Bot | Utility | Was |
|---:|---|---:|---:|
| 1 | Engineer | 9 | 2 |
| 2 | Extractor | 8 | 1 |
| 3 | Emissary | 6 | 3 |
| 4 | Safeguard | 6 | 4 |
| 5 | Safekeeper | 5 | 5 |
| 6 | Scrutineer | 5 | 6 |
| 7 | Archivist | 4 | 7 |
| 8 | Mender | 4 | 9 |
| 9 | Arbiter | 4 | 13 |
| 10 | Mediator | 3 | 12 |
| 11 | Inquirer | 3 | 15 |
| 12 | Scorer | 2 | 8 |
| 13 | Imitator | 2 | 11 |
| 14 | Investigator | 2 | 14 |
| 15 | Inferer | 2 | 16 |
| 16 | Architect | 1 | 10 |

Ties are broken by this morning's order.

**Why things moved:**
- **Engineer 2 → 1, Extractor 1 → 2.** Engineer shipped all day today with Gem making decisions in the loop. Extractor's last output is 4 Oct. Both stay far ahead of everyone else.
- **Arbiter 13 → 9.** Rulings were used again today, and it costs almost nothing in volume. This morning's ranking didn't weigh overhead explicitly.
- **Architect 10 → 16.** The overhead term now counts: about 73,000 words for drafts that only needed a fraction of that.
- **Scorer 8 → 12.** It largely duplicates Scrutineer, and Gem doesn't act on its scores.
- **Mediator 12 → 10, Inquirer 15 → 11.** Mediator is live and honest about missing spend data. Inquirer's roadmap is feeding Engineer's VEPA work (inferred), and it's active right now.
- **Imitator 11 → 13.** No output; only potential. **Mender 9 → 8, Inferer 16 → 15** (others moved around them). Emissary, Safeguard, Safekeeper, Scrutineer, Archivist and Investigator keep their places.

## 6. Top and bottom of the ratio table

**Low activity, decent utility (efficient):**
- **Safeguard** (ratio 1.96): 2 files, but it holds the highest-impact live risks (Facebook automation, gambling scraping, Gmail reads). Best value among bots that actually do work.
- **Safekeeper** (1.47) and **Arbiter** (1.45): small, specific outputs that others rely on.
- **Inferer, Imitator, Investigator** (1.75-2.84): high ratios only because they do almost nothing. Cheap to keep, not proven useful. Don't read these as good performance.

**High activity, low utility (overhead candidates):**
- **Architect** (0.13): the clearest case. Suggest a cap of about 3 short proposals a week, one plain question each.
- **Archivist** (0.45): real value (deploys, rollback), but heavy volume. Suggest dropping old role-map versions into an archive and stopping the full Google Doc mirror.
- **Scorer** (0.51): weekly instead of daily while nothing is changing.
- **Emissary** (0.53) and **Engineer** (0.64) sit below 1.0 only because they do the most work. Their utility is the highest in the swarm. They aren't overhead.

## 7. Recently retired bots (activity only)

Agent folders for all nine were removed between 9:20 and 9:26am today (INC-005), so these numbers come from /workspace content only.

| Bot | Id | Authored files | KB | Files dated 3-9 Oct | Md words | Activity index | Last dated output | What it left |
|---|---|---:|---:|---:|---:|---:|---|---|
| Sourcer | 2fe3e92f | 0 | 0 | 0 | 0 | 0.0 | none | Nothing found. |
| Editor | 2888c17a | 0 | 0 | 0 | 0 | 0.0 | none | Nothing found. |
| Marshal | f3810109 | 2 | 10 | 0 | 0 | 6.9 | none | 2 old schedule backups (`schedule.md.bak-*`); its live schedule work is now under Mender. |
| Messenger | 5e47d344 | 0 | 0 | 0 | 0 | 0.0 | none | Nothing found. |
| Interrogator | d3191aa8 | 0 | 0 | 0 | 0 | 0.0 | none | Nothing found. |
| Assembler | d1daab5f | 42 | 4,228 | 17 | 12,367 | 45.2 | 2026-10-04 | Role map v1-v3 (cartography), batch-1 review (3 Oct). |
| Ensembler | de808331 | 0 | 0 | 0 | 0 | 0.0 | none | Nothing attributable. `swarm-db/` and `grok-swarm-research/` may relate, but that is unproven. |
| old Inquirer | e613112b | 0 | 0 | 0 | 0 | 0.0 | none | Nothing attributable on disk; named as sender in the 3 Oct set-5 incident. |
| old Explorer | 82a2c15a | 15 | 133 | 10 | 9,982 | 35.2 | 2026-10-09 | Gem's approval records, directory and phases updates, handover, the 9 Oct value review, live-risk actions, retire-merge drafts. |

## 8. Where data was missing

- Transcripts: none usable (see limits).
- Spend: no dollar, token or invoice amounts anywhere (Mediator's ledger, confirmed). The only cost fact is that the Cursor account had an unpaid invoice that stopped routines on 6-8 Oct.
- True file dates before today: lost in the 10:37am restore, except where git, file names, headers or zip entries kept them.
- Retired bots: folders gone, so no folder or chat counts.
- Owners of `.playwright-mcp/`, `agent-tools/`, `swarm-db/`, `grok-swarm-research/`, `profile.txt` and `urls.txt`: not provable.

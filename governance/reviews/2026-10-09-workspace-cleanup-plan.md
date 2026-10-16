# Workspace cleanup plan: Friday 9 Oct 2026

Prepared by Explorer (04dcca0d) for Gem, about 6:20pm AEST (UTC+10). **Plan only.** Nothing was moved, renamed or deleted. Machine-readable copy: `2026-10-09-workspace-cleanup-plan.json` (same folder).

## Read this first

- `/workspace` is **9.0 GiB**. The SAFE list below frees about **8.2 GiB** (92% of the workspace). Almost all of it is Extractor's scraper caches.
- Counts: **14 safe**, **28 organise** (24 moves + 4 new folders), **26 needs Gem or owner**.
- **Dates are weak.** The box restarted at 10:37am today and nearly every file mtime was reset to 9 Oct 10:37-10:43am (6,806 files in that hour). So the "modified" column mostly shows the restore, not real work. Where possible I give a *content date* too: git commit date, a date in the file name or header, zip entry dates (BIE zips show 4 Oct), or a real mtime after 10:45am today. Rows marked *(inf.)* use an inferred date. Header dates can also be dates quoted inside content (for example a 2026-02-15 date inside a BIE file), so treat the first date as rough.
- Owners come from `directory.md`, the codex rename table (Codey = Engineer, Grok Bot = Emissary, Scraper = Extractor, Swarm Builder = Ensembler), git authors, file headers, and sha256 matches between workspace files and each bot's own `attachments/` folder.
- Reference search: `rg -F` for each path across `/workspace` (skipping node_modules, .git, caches, toolchains, .playwright-mcp) and every `/home/box/agent-data/agents/*/profile.json`. Hits are listed per action in the JSON and below.

## 1. Top-level tree

| Path | Size | Files | Owner (inferred where noted) | mtime (box, AEST) | Content dates |
|---|---:|---:|---|---|---|
| `bie_tools/` | 8.2 GiB | 12,002 | Extractor | 09 Oct 10:40 | 2026-10-02 to 2026-10-04 (partly inf.) |
| `tools/` | 230.5 MiB | 2,746 | Engineer | 09 Oct 10:43 | 2026-08-10 to 2026-10-03 |
| `.toolchain/` | 230.4 MiB | 2,734 | Engineer (inferred) | 09 Oct 10:43 | undated |
| `vepa/` | 225.2 MiB | 9,433 | Engineer (Codey commits) + upstream authors | 09 Oct 18:15 | 2026-09-10 to 2026-10-09 |
| `.playwright-mcp/` | 84.0 MiB | 120 | shared browser tool (Emissary/Extractor sessions) | 09 Oct 10:41 | 2026-10-01 to 2026-10-04 |
| `medb/` | 44.1 MiB | 2,742 | Emissary (git: "Grok Bot") | 09 Oct 18:11 | 2026-10-02 to 2026-10-04 |
| `governance/` | 9.4 MiB | 458 | governance bots (see report) | 09 Oct 16:31 | 2026-10-02 to 2026-10-09 |
| `swarm-db/` | 8.6 MiB | 10 | unattributed (2 Oct catalogue) | 09 Oct 10:40 | 2026-10-02 |
| `vepa-plans/` | 6.0 MiB | 20 | Engineer (+ Inquirer roadmap) | 09 Oct 18:17 | 2026-08-01 to 2026-10-09 |
| `bie_deliverables/` | 4.0 MiB | 89 | Extractor | 09 Oct 10:40 | 2026-02-15 to 2026-10-04 |
| `bie_organized.zip` | 1.2 MiB | 1 | Extractor | 09 Oct 10:40 | 2026-10-04 |
| `bie_scraper_and_lists.zip` | 1.2 MiB | 1 | Extractor | 09 Oct 10:40 | 2026-10-04 |
| `bie/` | 1.1 MiB | 70 | Extractor | 09 Oct 10:40 | 2026-02-15 to 2026-10-04 |
| `out/` | 712.9 KiB | 1 | Engineer | 09 Oct 17:54 | 2026-10-09 |
| `perf/` | 354.1 KiB | 75 | Engineer | 09 Oct 18:12 | 2026-10-09 |
| `bie_scraper.zip` | 282.4 KiB | 1 | Extractor | 09 Oct 10:40 | 2026-10-04 |
| `agent-tools/` | 185.7 KiB | 2 | unattributed (tool output dumps) | 09 Oct 11:26 | 2026-10-09 |
| `profile.txt` | 78.4 KiB | 1 | unknown (Gem personal) | 09 Oct 10:40 | undated |
| `orig_v2/` | 45.8 KiB | 5 | Extractor | 09 Oct 10:40 | 2026-10-04 (inf.) |
| `grok-swarm-research/` | 44.3 KiB | 2 | unattributed (input for retired Ensembler) | 09 Oct 10:40 | 2026-10-02 |
| `codey/` | 42.7 KiB | 4 | Engineer | 09 Oct 10:39 | 2026-10-02 |
| `medb-prior-work.md` | 26.4 KiB | 1 | Emissary | 09 Oct 10:37 | 2026-10-02 |
| `medb-spec/` | 23.4 KiB | 2 | Emissary | 09 Oct 10:39 | undated |
| `run.py.orig` | 22.0 KiB | 1 | Extractor | 09 Oct 10:40 | 2026-10-04 (inf.) |
| `base.py.orig` | 11.9 KiB | 1 | Extractor | 09 Oct 10:40 | 2026-10-04 (inf.) |
| `dash.html` | 9.6 KiB | 1 | Extractor | 09 Oct 10:39 | 2026-10-04 (inf.) |
| `bie_v2.diff` | 6.9 KiB | 1 | Extractor | 09 Oct 10:38 | 2026-10-04 (inf.) |
| `run_all.log` | 5.9 KiB | 1 | Extractor | 09 Oct 10:38 | 2026-10-04 (inf.) |
| `reach_check.py` | 2.3 KiB | 1 | Extractor | 09 Oct 10:40 | 2026-10-04 (inf.) |
| `urls.txt` | 1.9 KiB | 1 | unclear | 09 Oct 10:38 | undated |
| `extract_bie.py` | 1.5 KiB | 1 | Extractor | 09 Oct 10:40 | 2026-10-04 (inf.) |
| `disc_ip.log` | 1.2 KiB | 1 | Extractor | 09 Oct 10:39 | 2026-10-04 (inf.) |
| `cand.log` | 946 B | 1 | Extractor | 09 Oct 10:39 | 2026-10-04 (inf.) |
| `reach.log` | 904 B | 1 | Extractor | 09 Oct 10:38 | 2026-10-04 (inf.) |
| `disc_h2.log` | 651 B | 1 | Extractor | 09 Oct 10:38 | 2026-10-04 (inf.) |
| `disc_ph.log` | 627 B | 1 | Extractor | 09 Oct 10:38 | 2026-10-04 (inf.) |
| `pstats_d.log` | 540 B | 1 | Extractor | 09 Oct 10:39 | 2026-10-04 (inf.) |
| `disc_p2.log` | 451 B | 1 | Extractor | 09 Oct 10:37 | 2026-10-04 (inf.) |
| `disc_tg.log` | 443 B | 1 | Extractor | 09 Oct 10:37 | 2026-10-04 (inf.) |
| `disc_ph2.log` | 311 B | 1 | Extractor | 09 Oct 10:39 | 2026-10-04 (inf.) |
| `pstats_b.log` | 247 B | 1 | Extractor | 09 Oct 10:40 | 2026-10-04 (inf.) |
| `pstats_c.log` | 200 B | 1 | Extractor | 09 Oct 10:40 | 2026-10-04 (inf.) |
| `id-investigator/` | 188 B | 1 | Investigator | 09 Oct 10:40 | 2026-10-04 |
| `disc_us.log` | 160 B | 1 | Extractor | 09 Oct 10:39 | 2026-10-04 (inf.) |
| `pstats_g.log` | 57 B | 1 | Extractor | 09 Oct 10:40 | 2026-10-04 (inf.) |
| `pstats_i.log` | 20 B | 1 | Extractor | 09 Oct 10:40 | 2026-10-04 (inf.) |
| `dash.pid` | 7 B | 1 | Extractor | 09 Oct 10:39 | 2026-10-04 (inf.) |
| `dash.log` | 0 B | 1 | Extractor | 09 Oct 10:38 | 2026-10-04 (inf.) |
| `dash2.log` | 0 B | 1 | Extractor | 09 Oct 10:38 | 2026-10-04 (inf.) |
| `disc_home.log` | 0 B | 1 | Extractor | 09 Oct 10:38 | 2026-10-04 (inf.) |

Second level, the big items:

- `bie_tools/` 8.2 GiB: `cache/` 6.4 GiB (7,853 html), `cache_partner/` 1.3 GiB (1,975), `cache_tg/` 292 MiB (2,055), `pstats/` 195 MiB (pubinfo.jsonl 133 MiB, pages_content.jsonl 49 MiB), rest about 15 MiB of CSV, JSON and scripts.
- `vepa/` 225 MiB: `node_modules/` 195 MiB, `.git/` 25 MiB (197 commits), `docs/` 7.6 MiB, `exports/` 3.6 MiB, `dist/` 2.8 MiB, `src/` 2.1 MiB, `tests/` 1.8 MiB.
- `tools/` 230 MiB: `node22/` (Node v22.23.3 extracted 177 MiB + 54 MiB tarball), `codey/` helper scripts. `.toolchain/` 230 MiB is a second copy of the same Node.
- `.playwright-mcp/` 84 MiB: 72 .yml snapshots, 32 console logs (one is 75 MiB), 16 png. Dates from file names: 1-4 Oct.
- `medb/` 44 MiB: `experiment/` 27 MiB, `runs/` 13 MiB, `.git/` 8.6 MiB (22 commits), `docs/` 5.1 MiB.
- `governance/` 9.4 MiB, 458 files, about 239,000 words of markdown: `cartography/` 7.2 MiB (role-map versions v1-v6, png + svg + json each), `codex/` 1.8 MiB, `proposals/` 944 KiB.

## 2(a). SAFE: obvious junk, caches, duplicates

Top 5 by size: bie_tools/cache 6.4 GiB, bie_tools/cache_partner 1.3 GiB, bie_tools/cache_tg 292 MiB, .toolchain 230 MiB, Node tarball 54 MiB. Together about 8.2 GiB. "Referenced by" hits on the caches are the scraper scripts that fill them (`discover.py`, `partners.py`, `pstats/a_pages.py`) and Safekeeper's inventory row. Nothing breaks if they go, but a re-run would re-fetch the gambling sites (RR-002), so tell Extractor first. A gentler option is `tar --zstd` of the three caches (HTML usually compresses about 10:1).

| # | Action | Path | Dest | Size | Owner | Why | Referenced by |
|---|---|---|---|---:|---|---|---|
| 1 | delete | `bie_tools/cache/` |  | 6.4 GiB | Extractor | Scraper HTML cache: 7,853 fetched pages. Final lists already in bie_deliverables/ (4 Oct). Regenerable only by re-scraping, so ask Extractor first if a re-run is planned (RR-002 legal risk on re-scrape). Alternative: tar+compress instead of delete. | `bie_tools/discover.py`; `bie_tools/partners.py`; `bie_tools/pstats/a_pages.py`; `governance/secrets-inventory.md` |
| 2 | delete | `bie_tools/cache_partner/` |  | 1.3 GiB | Extractor | Scraper HTML cache of partner pages (1,975 files). Same caveat as bie_tools/cache/. | `bie_tools/discover.py`; `governance/secrets-inventory.md` |
| 3 | delete | `bie_tools/cache_tg/` |  | 291.7 MiB | Extractor | Scraper HTML cache of Telegram pages (2,055 files). Same caveat. Also holds key-shaped strings from third-party pages (secrets-inventory #40). | `bie_tools/discover.py`; `governance/secrets-inventory.md` |
| 4 | delete | `.toolchain/` |  | 230.4 MiB | Engineer | Second copy of Node v22.23.3 (extracted folder + 55 MB tarball + symlink + old test log). No file or bot instruction references .toolchain; tools/codey/env.sh and verify.sh use tools/node22/. | none found |
| 5 | delete | `tools/node22/node-v22.23.3-linux-x64.tar.gz` |  | 54.2 MiB | Engineer | Download tarball for the already-extracted tools/node22/node-v22.23.3-linux-x64/ (in use). Scripts use the extracted bin only. | none found |
| 6 | delete | `bie_organized.zip` |  | 1.2 MiB | Extractor | Byte-identical to bie_scraper_and_lists.zip (md5 bce6025e...) and every one of its 89 files matches bie_deliverables/ exactly. A copy also sits in Extractor attachments. | `governance/reviews/2026-10-09-explorer-bot-value-review.md`; `governance/risk/register.md` |
| 7 | delete | `bie_scraper.zip` |  | 282.4 KiB | Extractor | All 70 files match bie/ and bie_deliverables/scraper/ exactly. A copy also sits in Extractor attachments. | `governance/risk/register.md` |
| 8 | delete | `dash.log` |  | 0 B | Extractor | Empty (0-byte) log at workspace root. | none found |
| 9 | delete | `dash2.log` |  | 0 B | Extractor | Empty (0-byte) log at workspace root. | none found |
| 10 | delete | `disc_home.log` |  | 0 B | Extractor | Empty (0-byte) log at workspace root. | none found |
| 11 | delete | `dash.pid` |  | 7 B | Extractor | Stale PID file (pid 253292 not running; box restarted 10:37am 9 Oct). | none found |
| 12 | delete | `perf/nanhunt/__pycache__/` |  | 1.3 KiB | Engineer | Python bytecode cache. | none found |
| 13 | delete | `vepa/test-results/` |  | 45 B | Engineer | Gitignored Playwright test-results cache (45 bytes). Inside the vepa repo folder but not tracked. Do it when Engineer is idle. | none found |
| 14 | delete | `medb/docs/.~lock.DECISIONS.md#` |  | 83 B | Emissary | Stale LibreOffice lock file (no LibreOffice running since the 10:37am restart). Gitignored. | none found |

## 2(b). MOVE / ORGANISE

Goal: clear the loose files at the workspace root into their owner's folder. Every move lists the files that name the old path. Update those lines (or add a one-line note) in the same step. Governance files that mention old paths are historical records: don't rewrite them, just note the move in `incidents/log.md` or the owner's changelog.

| # | Action | Path | Dest | Size | Owner | Why | Referenced by |
|---|---|---|---|---:|---|---|---|
| 1 | mkdir | `bie_tools/_runlogs/` |  |  | Extractor | New home for Extractor run logs now loose at workspace root. | n/a |
| 2 | move | `disc_h2.log` | `bie_tools/_runlogs/disc_h2.log` | 651 B | Extractor | Extractor BIE discovery/verification run log loose at workspace root. | `governance/reviews/2026-10-04-reality-baseline.md` |
| 3 | move | `disc_ip.log` | `bie_tools/_runlogs/disc_ip.log` | 1.2 KiB | Extractor | Extractor BIE discovery/verification run log loose at workspace root. | `governance/reviews/2026-10-04-reality-baseline.md` |
| 4 | move | `disc_p2.log` | `bie_tools/_runlogs/disc_p2.log` | 451 B | Extractor | Extractor BIE discovery/verification run log loose at workspace root. | `governance/reviews/2026-10-04-reality-baseline.md` |
| 5 | move | `disc_ph.log` | `bie_tools/_runlogs/disc_ph.log` | 627 B | Extractor | Extractor BIE discovery/verification run log loose at workspace root. | `governance/reviews/2026-10-04-reality-baseline.md` |
| 6 | move | `disc_ph2.log` | `bie_tools/_runlogs/disc_ph2.log` | 311 B | Extractor | Extractor BIE discovery/verification run log loose at workspace root. | `governance/reviews/2026-10-04-reality-baseline.md` |
| 7 | move | `disc_tg.log` | `bie_tools/_runlogs/disc_tg.log` | 443 B | Extractor | Extractor BIE discovery/verification run log loose at workspace root. | `governance/reviews/2026-10-04-reality-baseline.md` |
| 8 | move | `disc_us.log` | `bie_tools/_runlogs/disc_us.log` | 160 B | Extractor | Extractor BIE discovery/verification run log loose at workspace root. | `governance/reviews/2026-10-04-reality-baseline.md` |
| 9 | move | `pstats_b.log` | `bie_tools/_runlogs/pstats_b.log` | 247 B | Extractor | Extractor BIE discovery/verification run log loose at workspace root. | none found |
| 10 | move | `pstats_c.log` | `bie_tools/_runlogs/pstats_c.log` | 200 B | Extractor | Extractor BIE discovery/verification run log loose at workspace root. | none found |
| 11 | move | `pstats_d.log` | `bie_tools/_runlogs/pstats_d.log` | 540 B | Extractor | Extractor BIE discovery/verification run log loose at workspace root. | none found |
| 12 | move | `pstats_g.log` | `bie_tools/_runlogs/pstats_g.log` | 57 B | Extractor | Extractor BIE discovery/verification run log loose at workspace root. | none found |
| 13 | move | `pstats_i.log` | `bie_tools/_runlogs/pstats_i.log` | 20 B | Extractor | Extractor BIE discovery/verification run log loose at workspace root. | none found |
| 14 | move | `cand.log` | `bie_tools/_runlogs/cand.log` | 946 B | Extractor | Extractor BIE discovery/verification run log loose at workspace root. | none found |
| 15 | move | `reach.log` | `bie_tools/_runlogs/reach.log` | 904 B | Extractor | Extractor BIE discovery/verification run log loose at workspace root. | `governance/reviews/2026-10-04-reality-baseline.md` |
| 16 | move | `run_all.log` | `bie_tools/_runlogs/run_all.log` | 5.9 KiB | Extractor | Extractor BIE discovery/verification run log loose at workspace root. | none found |
| 17 | mkdir | `bie_tools/scripts/` |  |  | Extractor | New home for loose Extractor helper scripts. | n/a |
| 18 | move | `extract_bie.py` | `bie_tools/scripts/extract_bie.py` | 1.5 KiB | Extractor | Extractor helper script loose at workspace root. reach_check.py docstring calls itself by its old path; update that line on move. | none found |
| 19 | move | `reach_check.py` | `bie_tools/scripts/reach_check.py` | 2.3 KiB | Extractor | Extractor helper script loose at workspace root. reach_check.py docstring calls itself by its old path; update that line on move. | none found |
| 20 | move | `dash.html` | `bie_tools/dash.html` | 9.6 KiB | Extractor | "Scraper Dashboard" page loose at workspace root. | none found |
| 21 | mkdir | `bie_tools/_history/` |  |  | Extractor | New home for superseded BIE scraper code and patches. | n/a |
| 22 | move | `base.py.orig` | `bie_tools/_history/base.py.orig` | 11.9 KiB | Extractor | Pre-patch copy / patch of BIE scraper code (2 Oct). Keep for history, not at root. | none found |
| 23 | move | `run.py.orig` | `bie_tools/_history/run.py.orig` | 22.0 KiB | Extractor | Pre-patch copy / patch of BIE scraper code (2 Oct). Keep for history, not at root. | none found |
| 24 | move | `bie_v2.diff` | `bie_tools/_history/bie_v2.diff` | 6.9 KiB | Extractor | Pre-patch copy / patch of BIE scraper code (2 Oct). Keep for history, not at root. | none found |
| 25 | move | `orig_v2/` | `bie_tools/_history/orig_v2/` | 45.8 KiB | Extractor | Original v2 BIE scraper code. Its config.ini is listed in secrets-inventory #35, so update that row on move. | `governance/secrets-inventory.md` |
| 26 | mkdir | `medb-research/` |  |  | Emissary | New home for MedB research notes kept outside the medb git repo. | n/a |
| 27 | move | `medb-spec/` | `medb-research/medb-spec/` | 23.4 KiB | Emissary | MedB master spec text (2 parts). Sits next to the repo, not in it. | none found |
| 28 | move | `medb-prior-work.md` | `medb-research/medb-prior-work.md` | 26.4 KiB | Emissary | MedB prior-work brief (2 Oct). Named in secrets-inventory #29 and threat register (sk-shaped line), so update those rows on move; get Safekeeper to check the sk- line first. | `governance/secrets-inventory.md`; `governance/security/threat-register.md` |

## 2(c). NEEDS GEM OR OWNER

Privacy items, secrets, governance records, git repos, and anything a bot instruction names. **Nothing here should be deleted without Gem.** Governance records, approvals, codex, rulings and git repos are listed only to say "no deletion"; the only options offered are archive moves or quarantine.

| # | Action | Path | Dest | Size | Owner | Why | Referenced by |
|---|---|---|---|---:|---|---|---|
| 1 | move | `.playwright-mcp/` | `/home/box/quarantine/2026-10-09/playwright-mcp/` | 84.0 MiB | Emissary/Extractor (shared browser tool) | PRIVACY. Browser snapshots and console logs from 1-4 Oct: 72 .yml page snapshots (29 mention Facebook, Gmail, LinkedIn, Twitter or Reddit), 32 console logs (one 75 MB), 16 screenshots. Gem approved deleting only the 5 Facebook snapshots (done 9:05am). Suggest quarantine to /home/box/quarantine/ (chmod 700) or delete, Gem to choose. | `agents/04dcca0d-1479-4e01-bf29-a13b4fc3c3a7/profile.json`; `agents/28cf987d-ee94-4839-a6d3-33c04a11b9d6/profile.json`; `agents/52772b1d-4a85-4ea3-ae15-f3912c901a3b/profile.json`; `agents/f8e3fdc6-ee60-410e-bdb7-d437fc1500d1/profile.json`; `agents/febac500-d854-4dc7-a6a7-23b3feb07f80/profile.json`; `governance/approvals/2026-10-09-gem-direct-words.md` (+42 more) |
| 2 | move | `profile.txt` | `/home/box/quarantine/2026-10-09/profile.txt` | 78.4 KiB | unknown (likely Gem upload) | PRIVACY. 80 KB copy of a shared ChatGPT chat describing Gem personally ("Describe Your Work"). Personal content in shared folder. Nothing references it. Suggest quarantine. | none found |
| 3 | move | `agent-tools/6a30c768-0a14-45c0-97c3-b65fb4e22a70.txt` | `/home/box/quarantine/2026-10-09/agent-tools/` | 87.8 KiB | unknown (tool output) | PRIVACY. 90 KB raw Gmail thread dump (tool output), written 11:26am 9 Oct. Mailbox content in shared folder. Suggest quarantine. | none found |
| 4 | move | `agent-tools/ebb569bf-2b08-4a01-8582-042f200d83f7.txt` | `/home/box/quarantine/2026-10-09/agent-tools/` | 98.0 KiB | Archivist | PRIVACY/governance. 100 KB export of Google Doc "Gem's Bot Codex (governance, restricted)". Restricted doc copy in shared folder. Archivist owns the mirror. | none found |
| 5 | delete | `id-investigator/` |  | 188 B | Investigator | PRIVACY. Now only a 188-byte stub; the real file is in /home/box/quarantine/2026-10-09/ (moved 9:07am). Quarantine folders are now mode 755, not the 700 recorded in incidents/2026-10-09-live-risks.md (files still 600). Gem to decide whether to remove the stub and re-tighten folder modes. | `governance/assessments/2026-10-05.md`; `governance/assessments/2026-10-06.md`; `governance/assessments/2026-10-09.md`; `governance/incidents/2026-10-09-live-risks.md`; `governance/reviews/2026-10-09-explorer-bot-value-review.md`; `governance/reviews/2026-10-09.md` (+3 more) |
| 6 | move | `governance/incidents/2026-10-03-identity-set5-unverified.md` | `/home/box/quarantine/ (Gem decides)` | 7.3 KiB | Mender | PRIVACY + governance record. Quotes sensitive personal details (T-005 / RR-010). Never delete; Gem to decide quarantine vs redaction. | `governance/incidents/2026-10-09-live-risks.md`; `governance/incidents/log.md`; `governance/incidents/log.md.bak-20261005`; `governance/proposals/clone-accuracy-validator-v002.md`; `governance/proposals/voice-call-messaging-v001.md`; `governance/reviews/2026-10-04-reality-baseline.md` (+4 more) |
| 7 | move | `urls.txt` | `(owner decides)` | 1.9 KiB | unclear (Extractor or Emissary) | PRIVACY/secret. 43-line research link list (mostly arXiv) with one sk-shaped line (secrets-inventory #33). Architect's scraper.md lists it as Extractor evidence, but content looks like MedB research; owner unclear. Safekeeper to check the sk- line before any move. | `governance/proposals/scraper.md`; `governance/reviews/2026-10-04-reality-baseline.md`; `governance/secrets-inventory.md`; `governance/security/threat-register.md` |
| 8 | move | `medb/data/` | `(no move; review only)` | 60.7 KiB | Emissary | SECRET-by-name. api_tokens.json and sync_clients.json (secrets-inventory #27-28) inside the medb repo (gitignored). Owner to confirm test-only. | `governance/secrets-inventory.md`; `governance/security/threat-register.md`; `medb/README.md`; `medb/app/js/main.js`; `medb/docs/DECISIONS.html`; `medb/docs/DECISIONS.md` (+5 more) |
| 9 | delete | `bie_scraper_and_lists.zip` |  | 1.2 MiB | Extractor / Gem | Gem's 9 Oct upload (copy in Extractor attachments). Holds config.ini with credential-like fields (T-009). Referenced by governance. Identical to bie_organized.zip. | `governance/assessments/2026-10-09.md`; `governance/reviews/2026-10-09-explorer-bot-value-review.md`; `governance/reviews/2026-10-09.md`; `governance/risk/register.md`; `governance/secrets-inventory.md`; `governance/security/threat-register.md` |
| 10 | move | `bie/` | `(dedupe against bie_deliverables/scraper/)` | 1.1 MiB | Extractor | Working copy of BIE scraper. 70 files identical to bie_deliverables/scraper/, plus extra reports and db. Dedupe only with Extractor. config.ini in secrets-inventory #35. | `bie_tools/au/au_discover.sh`; `bie_tools/au/au_discover2.sh`; `bie_tools/au/au_resume.sh`; `bie_tools/au/discover.log`; `bie_tools/au/m_au_merge.py`; `bie_tools/au/merge.log` (+11 more) |
| 11 | delete | `bie_tools/pstats/` |  | 195.0 MiB | Extractor | 196 MB: scraped page content (pubinfo.jsonl 140 MB, pages_content.jsonl 51 MB) mixed with scripts. Not a pure cache. Extractor to say what is still needed. | `bie_tools/au/k_map.py` |
| 12 | delete | `vepa/node_modules/` |  | 194.7 MiB | Engineer | 210 MB. Regenerable with npm ci, but inside a git repo and Engineer is mid-change (uncommitted edits at 6pm 9 Oct). Leave unless Engineer agrees. | `perf/mx-collapse.mjs`; `perf/mx-refill-check.mjs`; `perf/profile.mjs`; `perf/settings-shot.mjs`; `perf/topbar-shot.mjs`; `tools/codey/verify.sh` |
| 13 | move | `vepa/` | `(no action)` | 225.2 MiB | Engineer | Git repo (197 commits, 25 today). No action. | `governance/handover/explorer-handover-2026-10-09.md`; `governance/reviews/2026-10-04-reality-baseline.md`; `governance/reviews/2026-10-05.md`; `governance/reviews/2026-10-06.md`; `governance/reviews/2026-10-09.md`; `governance/risk/register.md` (+37 more) |
| 14 | move | `medb/` | `(no action)` | 44.1 MiB | Emissary | Git repo (22 commits). No action. | `governance/handover/explorer-handover-2026-10-09.md`; `governance/proposals/2026-10-05/emissary-v004.md`; `governance/reviews/2026-10-05.md`; `governance/reviews/2026-10-09.md`; `governance/risk/register.md`; `governance/secrets-inventory.md` (+1 more) |
| 15 | move | `codey/` | `(no move; named by instructions)` | 42.7 KiB | Engineer | Codey 3.x operating specs. Named in bot instructions (codex codey v002) so do not move without Gem. | `governance/approvals/2026-10-03-batch1-review.md`; `governance/audits/2026-10-03-initial-audit.md`; `governance/codex/_tools/build_v002_batch1.py`; `governance/codex/codey/CHANGELOG.md`; `governance/codex/codey/v002.md`; `governance/proposals/codey.md` (+1 more) |
| 16 | move | `grok-swarm-research/` | `(no move; named by instructions)` | 44.3 KiB | Engineer (Ensembler retired) | Named in Engineer profile.json and codex. No move. | `agent-tools/ebb569bf-2b08-4a01-8582-042f200d83f7.txt`; `agents/f8e3fdc6-ee60-410e-bdb7-d437fc1500d1/profile.json`; `governance/audits/2026-10-03-initial-audit.md`; `governance/bot-landscape-review.md`; `governance/cartography/summaries-v1.md`; `governance/cartography/summaries-v2.md` (+18 more) |
| 17 | move | `governance/directory.md.bak-0909` | `governance/_archive/directory.md.bak-0909` | 3.7 KiB | Archivist / file owner | Governance record backup. Never delete. Option: move to governance/_archive/ if Gem and the owner agree. | `governance/directory.md` |
| 18 | move | `governance/directory.md.bak-1504` | `governance/_archive/directory.md.bak-1504` | 6.5 KiB | Archivist / file owner | Governance record backup. Never delete. Option: move to governance/_archive/ if Gem and the owner agree. | `governance/reviews/2026-10-04-reality-baseline.md` |
| 19 | move | `governance/directory.md.bak-1525` | `governance/_archive/directory.md.bak-1525` | 7.6 KiB | Archivist / file owner | Governance record backup. Never delete. Option: move to governance/_archive/ if Gem and the owner agree. | none found |
| 20 | move | `governance/phases.md.bak-0909` | `governance/_archive/phases.md.bak-0909` | 1019 B | Archivist / file owner | Governance record backup. Never delete. Option: move to governance/_archive/ if Gem and the owner agree. | none found |
| 21 | move | `governance/schedule.md.bak-20261005` | `governance/_archive/schedule.md.bak-20261005` | 5.4 KiB | Archivist / file owner | Governance record backup. Never delete. Option: move to governance/_archive/ if Gem and the owner agree. | none found |
| 22 | move | `governance/schedule.md.bak-p1` | `governance/_archive/schedule.md.bak-p1` | 4.4 KiB | Archivist / file owner | Governance record backup. Never delete. Option: move to governance/_archive/ if Gem and the owner agree. | `governance/reviews/2026-10-04-reality-baseline.md` |
| 23 | move | `governance/incidents/log.md.bak-20261005` | `governance/_archive/log.md.bak-20261005` | 1.9 KiB | Archivist / file owner | Governance record backup. Never delete. Option: move to governance/_archive/ if Gem and the owner agree. | `governance/incidents/log.md`; `governance/reviews/2026-10-05.md` |
| 24 | move | `governance/risk/register.md.bak-20261005` | `governance/_archive/register.md.bak-20261005` | 442 B | Archivist / file owner | Governance record backup. Never delete. Option: move to governance/_archive/ if Gem and the owner agree. | none found |
| 25 | move | `governance/cartography/` | `governance/cartography/_archive/` | 7.2 MiB | Archivist | 7.4 MB of role-map versions v1-v6 (png/svg/json each). v5 files duplicate the current files byte for byte. Governance record: optional move of v1-v5 into cartography/_archive/, Archivist and Gem decide. | `agent-tools/ebb569bf-2b08-4a01-8582-042f200d83f7.txt`; `agents/61ef3abd-87b8-49f1-b8d6-b52969afa315/profile.json`; `governance/bot-landscape-review.md`; `governance/codex/PENDING-FOR-ARBITER.md`; `governance/codex/PENDING-FOR-ASSEMBLER.md`; `governance/codex/_tools/deploy_manifest_2026-10-04.json` (+32 more) |
| 26 | move | `governance/codex/_tools/doc_sync_2026-10-04/` | `governance/codex/_tools/_archive/` | 193.6 KiB | Archivist | Chunks used to sync the Google Doc mirror. Codex tooling; Archivist decides. | `governance/codex/MIRROR.md` |

## 3. Privacy and secret flags (no values printed)

1. **`.playwright-mcp/`** (84 MiB). 72 page snapshots from 1-4 Oct; 29 of them mention Facebook, Gmail, LinkedIn, Twitter or Reddit. 32 console logs (four 2 Oct logs each have 250 to 1,800 lines matching facebook, messenger, gmail, linkedin, login, password, token or cookie; I counted matches only, not content). Named in 5 bot profiles (Explorer, Emissary, Safekeeper, Engineer, Extractor). Gem approved deleting only the 5 Facebook snapshots, done 9:05am.
2. **`id-investigator/factcheck-2026-10-04.md`** is now a 188-byte stub. The full 14.6 KB file with Gem's personal details is in `/home/box/quarantine/2026-10-09/id-investigator/` (file mode 600). **New:** the quarantine folders are now mode **755**, not the 700 recorded in `incidents/2026-10-09-live-risks.md`. Probably reset by the 10:37am restore (inferred). Files are still 600, but every bot runs as the same user anyway.
3. **`profile.txt`** (80 KB, root of workspace): a copy of a shared ChatGPT chat that profiles Gem personally. Not referenced anywhere. Not in Safekeeper's inventory.
4. **`agent-tools/6a30c768-….txt`** (90 KB, written 11:26am today): raw Gmail thread JSON. **`agent-tools/ebb569bf-….txt`** (100 KB): export of Google Doc "Gem's Bot Codex (governance, restricted)". Neither is in Safekeeper's inventory yet.
5. **`governance/incidents/2026-10-03-identity-set5-unverified.md`**: quotes sensitive personal details (T-005 / RR-010). Governance record, so quarantine or redaction is Gem's call.
6. **Secret-shaped strings** (Safekeeper inventory #27-35, still present): `medb/data/api_tokens.json` and `sync_clients.json`; an `sk-`-shaped line in `urls.txt`, `medb-prior-work.md` and `governance/bot-landscape-review.md`; `config.ini` with credential-like fields in `bie/in/config/`, `orig_v2/`, `bie_deliverables/scraper/in/config/` and inside `bie_scraper_and_lists.zip`, `bie_organized.zip` and `bie_scraper.zip` (T-009).
7. **Cookie seed** `/home/box/agent-data/chrome-cookie-seed.json` (outside /workspace): still mode 644, 28,462 bytes, rewritten at 10:40am today by the box's cookie service (T-001). No cookie, storage-state or session export found inside /workspace.
8. No Chrome or LibreOffice process is running since the 10:37am restart, so the Facebook-logged-in browser and the open Writer window noted this morning are gone. The Facebook *session* may still be in the cookie seed (not checked; values not read).

## 4. Side effects of this review (honest note)

- Reading each agent's `store.db` read-only (to count transcript entries) made SQLite create empty `store.db-wal` (0 bytes) and `store.db-shm` (32 KB) side files in 16 agent folders at 6:10-6:11pm. No data was changed. They're harmless, and SQLite reuses them. I left them rather than delete files in agent folders.
- `git status` refreshed the stat cache in `medb/.git/index` (6:11pm). No commits, no tracked changes.
- New files written: the 5 outputs listed in the bot activity report. Scratch scripts are in `/tmp/explorer-0909/`, outside /workspace.

## 5. Suggested order (for Gem)

1. Say yes or no to the SAFE list (8.2 GiB). Extractor confirms no re-scrape is planned, or picks compress-not-delete.
2. Quarantine the 4 privacy files (`profile.txt`, the 2 `agent-tools` dumps, `.playwright-mcp/`) and re-tighten the quarantine folders to 700.
3. Let the owners do the ORGANISE moves (Extractor root files, Emissary MedB notes), updating the listed references.
4. Leave governance archives and repos as they are unless Archivist proposes a `_archive/` layout.

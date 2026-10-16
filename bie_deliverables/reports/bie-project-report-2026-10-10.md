# Bonus Intelligence Engine (BIE) — project report

**Date of ask:** Saturday 10 Oct 2026, about 1:42pm AEST  
**Finished:** Thursday 15 Oct 2026, about 11:36pm AEST (UTC+10)  
**Author:** Explorer executor (read-only research over files already on disk; this report trio is the only write)  
**Style:** Australian English, Brisbane AEST. Bare bot names. Short sentences.  
**Scope:** What BIE is, what it produced, every source and docs file described, the discovery/partnership tooling around it, and the open legal/packaging pause. Like the 10 Oct governance I/O report, but for BIE.

Sources: `/workspace/bie/`, `/workspace/bie_tools/`, `/workspace/bie_deliverables/`, `/workspace/backups/bie-caches-2026-10-10/`, governance risk rows RR-002 / RR-015 / RR-018 / RR-019. Numbers are from files on disk. Nothing invented. Credential values in `config.ini` are not read or quoted.

---

## Top line

| Measure | Count |
|---|---:|
| Seed URLs (`urls.txt`) | **580** |
| Combined confirmed hosts | **7,629** |
| New hosts found | **7,049** (detail CSV 6,978 rows) |
| Merchants with one verified URL | **1,847** |
| Australian merchants | **1,055** |
| AU registered / unregistered / unknown | **422 / 558 / 75** |
| Original-580 reachable / merchant-ok / api-ok | **421 / 315 / 310** |
| AU partnership sites / groups / families | **540 / 262 / 173** |
| Unknown-country sites held out of AU files | **622** |
| AU merchants with public promos (terms build) | **983** of 1,055 |
| Promo rows seen in terms build | **46,266** (kept types below) |
| Engine source lines (`*.py` under bie/) | **~2,241** |
| Docs markdown lines (`docs/**`) | **~1,906** |
| Engine log since restore | **empty** |
| Proxies loaded | **0** |
| Scrape caches (archived 10 Oct) | **~1.8 GB** kept under `backups/bie-caches-2026-10-10/` |
| Open legal/packaging risks | **RR-002, RR-015** (pause in force) |

---

## 1. What BIE is

BIE (Bonus Intelligence Engine) is Gem's casino-bonus scraper and analysis stack. The live code lives at `/workspace/bie/`. A cleaned package copy sits in `bie_deliverables/scraper/`. Side tooling for discovery and partnership stats lives in `/workspace/bie_tools/`. Organised lists and reports are in `/workspace/bie_deliverables/`.

The engine is a **7-layer** Python app aimed at Termux/Android:

| Layer | File | Job |
|---|---|---|
| Foundation | `base.py` | Config, DB, IO, system state |
| Execution | `run.py` | Orchestrator + scrape workers |
| Connectivity | `net.py` | HTTP, proxies, AbuseIPDB |
| Interaction | `flow.py` | Login, API, merchant parse |
| Intelligence | `logic.py` | PV score, fingerprint, dedup |
| Visualization | `ui.py` | Rich TUI |
| Communication | `web_server.py` | FastAPI + WebSocket dashboard |

**How a site is processed (code path):** pick proxy → load/restore session → parse MERCHANTID from homepage → login if needed → `syncData` → map bonuses → fingerprint + fuzzy dedup → PV score → queue write to SQLite/CSV → TUI + WebSocket update.

**Important limits that apply now**
- Extractor's pause (RR-015): no further shipping, copying or running of the scraper packages / `bie_deliverables` scraper tree until Arbiter lifts it. Gem left the zips in place on 9 Oct.
- RR-002: Interactive Gambling Act 2001 exposure is open and is Gem's legal call. Private research is the lowest-risk use; sharing or promotional use raises the risk.
- Later AU partnership / terms rebuilds (RR-018, RR-019) were **offline only** from data already on disk — no new scraping.
- `engine.log` is empty and `proxies.txt` is empty at this check.

---

## 2. Inputs

### 2.1 Seed and derived URL lists (`bie/in/config/`)

| File | Rows / notes |
|---|---|
| `urls.txt` | 580 — Seed URL list the engine reads (original 580). |
| `urls_backup.txt` | 579 — Backup of the seed list. |
| `urls_combined.txt` | 7629 — Seed + all confirmed new domains, deduped. |
| `newurls_found.txt` | 7049 — Confirmed new domains alone. |
| `newurls.txt` | 354 — Older candidate / interim new-URL list. |
| `urls_by_merchant.txt` | 1847 — One verified working URL per merchant ID. |
| `urls_by_merchant.csv` | 1848 — Same with merchant_id, name, mirror_count, checked_at. |
| `urls_au.txt` | 1055 — One verified URL per Australian merchant. |
| `urls_au.csv` | 1055 — AU merchants with details. |
| `au_registered.csv` | 422 — AU sites tied to an account record (all under U1). |
| `au_unregistered.csv` | 558 — AU sites with no account on record (+ matching .txt). |
| `au_unknown.csv` | 75 — AU sites matched to old records by brand name only. |
| `au_unregistered.txt` | 558 — Plain-URL form of au_unregistered. |
| `check.txt` | 399 — Working checklist / subset used during checks. |
| `newregistered.txt` | 194 — Newly registered AU hosts (relative to prior cut). |
| `newunregistered.txt` | 77 — Newly unregistered AU hosts. |
| `proxies.txt` | empty |
| `config.ini` | PRIVATE (logins / keys / UI auth) — not opened for this report |
| `test_url.txt` | 1 test URL |

### 2.2 Templates, DB stub, logs

| Path | What it is |
|---|---|
| `in/templates/index.html` | Dashboard SPA |
| `in/templates/docs.html` | In-app docs browser |
| `db/reachability.csv` | 580-row no-login results |
| `err/log/engine.log` | Empty |
| `lab/`, `in/meta/` | Mentioned in README; **not present** in this tree |

### 2.3 Discovery inputs (`bie_tools/`)

Cached HTML used for discovery (homepages, partner pages, telegram) was archived then deleted on 10 Oct under Gem's words *"Delete the original scrape caches (archives kept)"*. Archives: `/workspace/backups/bie-caches-2026-10-10/` (~1.8 GB). Remaining on disk: harvest JSONs, candidate CSVs, partner_dirs.json, platform_ips.txt, search lists, page snapshots used as fixtures, and the pstats JSONL (`pubinfo.jsonl` 1,827 lines; `pages_content.jsonl` 2,502; `sites_config.csv` 7,237).

---

## 3. Process / flow

```
urls.txt (580)
   │
   ├─ nologin_check / reach_check ──► reachability.csv
   │
   ├─ discover.py sources
   │     partners │ homepages │ telegram │ urlscan │ sameip │ pages │ file
   │         └─► candidates_*.csv ── merge ──► newurls_found.txt
   │                                              urls_combined.txt
   │
   ├─ au/* ──► urls_au + registered/unregistered/unknown splits
   │
   └─ pstats pipeline (public APIs only)
         A pages → B getPage → C pubinfo → D by_merchant
         → E groups → G/H/J stats → (AU) g_build_au / k_bonus_terms_au
              └─► partnership_*_AU.* , bonus_terms_AU.* , bonus_scores_AU.xlsx
```

Discovery rule (from `DISCOVERY.md`): homepage must expose MERCHANTID/MERCHANTNAME **and** `GET /api/v1/index.php` must return the platform JSON error shape. Only bare `https://host` URLs are fetched; referral paths are stripped.

Top sources in `newurls_found_detail.csv` (6,978 rows): `urlscan:domain:cdn.vefrop.com` 1,038; seed `newurls.txt` 185; aggregator web search 60; rapiddns same-IP 60; then many per-directory partner and homepage-link rows.

---

## 4. Outputs

### 4.1 Organised deliverables (`bie_deliverables/`)

| Path | What it is |
|---|---|
| `README.md` | Index of the organised snapshot (4 Oct 2026 AEST). |
| `scraper/` | Clean copy of the engine (venv/caches removed). Same source set as `/workspace/bie/`. |
| `lists/all/urls_original.txt` | 580 starting URLs. |
| `lists/all/urls_combined.txt` | 7,629 combined. |
| `lists/all/newurls_found.txt` | 7,049 confirmed new. |
| `lists/all/urls_by_merchant.txt/.csv` | 1,847 one-URL-per-merchant. |
| `lists/australia/urls_au.txt/.csv` | 1,055 AU merchants. |
| `lists/australia/au_registered.csv` | 422 with account on record. |
| `lists/australia/au_unregistered.csv/.txt` | 558 with no account. |
| `lists/australia/au_unknown.csv` | 75 brand-name-only matches. |
| `reports/DISCOVERY.md` | Repeatable discovery method. |
| `reports/reachability.csv` | Original-580 no-login results. |
| `reports/newurls_found_detail.csv` | Every new domain with merchant, source, mirror flag (6,978 rows). |
| `reports/partnership_stats_AU.xlsx/.csv` | AU-only partnership table (262 groups / 173 families / 540 sites). |
| `reports/partnership_sites_AU.csv` | One row per AU site. |
| `reports/partnership_summary_AU.md` | AU method + caveats. |
| `reports/partnership_sites_unknown_country.csv` | 622 unknown-country sites held out. |
| `reports/bonus_terms_AU.csv/.xlsx` | Per-promo terms for AU merchants (built 10 Oct 13:30 AEST). |
| `reports/bonus_scores_AU.xlsx` | Scored share / downline-FD / welcome offers (updated 15 Oct). |
| `reports/_all-countries/` | Pre-AU partnership files (1,615 sites). |

### 4.2 AU partnership snapshot (10 Oct 13:10 AEST, offline)

- 540 AU sites in 262 groups → 173 families (Jaccard ≥ 0.8).
- 537 / 540 have public promotion data; 451 no-deposit; 506 welcome.
- Largest family head: eb7png.com partnership, 37 AU sites.
- 622 unknown-country sites excluded and listed for review (8 have a mid that appears in urls_au — review hint only, not used to classify).

### 4.3 AU bonus terms + scores

Terms build meta (`pstats/bonus_terms_AU_meta.json`, 10 Oct 13:30 AEST): 1,055 AU merchants, 995 in pubinfo, 983 with promos, 46,266 promo rows seen.

| Promo type (summary) | Merchants | Promos |
|---|---:|---:|
| REGISTER | 834 | 905 |
| WELCOME | 917 | 1,636 |
| SHARE | 934 | 1,429 |
| DOWNLINE_FIRST_DEPOSIT | 792 | 1,016 |
| COMMISSION | 778 | 866 |

`bonus_scores_AU.xlsx` (15 Oct) applies a 0–100 weighted geometric score (Value / Playthrough / Cashout / Access) to share, downline first-deposit and welcome offers. Share tasks were split out of share bonuses on Gem's clarification the same evening.

### 4.4 Packages on disk (paused)

| Zip | Size | Note |
|---|---:|---|
| `bie_scraper_and_lists.zip` | 1.29 MB | Gem 9 Oct upload; pause covers shipping/running |
| `bie_organized.zip` | 1.29 MB | Byte-identical twin |
| `bie_scraper.zip` | 282 KB | Engine-only older pack |

---

## 5. Every source file (`/workspace/bie/*.py`)

| File | Lines | Size | Description |
|---|---:|---:|---|
| `base.py` | 228 | 12.7 KB | Foundation layer. Config/INI, URL+credential parse, thread-local SQLite pool (`db/base.db`), session load/save as JSON (not pickle), CSV append helpers, logging, and `SystemState` pause/resume/stop events. |
| `run.py` | 356 | 22.6 KB | Execution layer. Async orchestrator, DB/CSV writer threads, `ScrapeWorker` lifecycle (proxy → merchant parse → login → syncData → score/dedup → save), CLI flags (`-v`, `-r`, `-s`, `dash`). |
| `net.py` | 155 | 6.7 KB | Connectivity. `cloudscraper` sync sessions, `aiohttp` async manager (`ssl=False`), HTML/JSON helpers, AbuseIPDB proxy health (`check`/`burned`/`status`), proxy rotation helpers. |
| `flow.py` | 140 | 5.8 KB | Interaction. Login payload, API endpoint `/api/v1/index.php`, auth-token + syncData fetch, MERCHANTID/MERCHANTNAME extraction from HTML/JS. |
| `logic.py` | 213 | 9.7 KB | Intelligence. Bonus normalize/extract/map, SHA-256 fingerprint, fuzzy name match (≥0.80), PV Algorithm V14 (`score`), junk filter, high-value flag, expiry parse. |
| `ui.py` | 583 | 23.1 KB | Visualization. Rich TUI init/live/final dashboards, rolling health metrics, colour helpers, posts telemetry to the web dashboard `/update`. |
| `web_server.py` | 168 | 5.8 KB | Communication. FastAPI on `127.0.0.1:8000`, Basic Auth on control routes, WebSocket broadcast, pause/resume/stop + config read/update, serves dashboard HTML. |
| `generate_final_report.py` | 92 | 3.7 KB | Offline report helper. Reads `db/base.db` for commission/referral-style bonuses ≥$5, concurrent reachability check, writes `final_bonus_report.md`. |
| `generate_stats_report.py` | 96 | 3.8 KB | Sibling of final report. Same filter, writes `online_stats_report.md` / related online lists. |
| `test_api_live.py` | 34 | 1.0 KB | Live smoke: fetch one site HTML, extract merchant, hit API endpoint. |
| `test_links.py` | 43 | 2.0 KB | Concurrent HEAD/GET reachability over a hard-coded ~40-URL commission list. |
| `test_links_expanded.py` | 50 | 2.6 KB | Same pattern on a larger expanded bonus-site list. |
| `test_parse.py` | 4 | 97 B | Tiny parse smoke: calls `base.parse()` and prints URL/cred counts. (Note: live `base.py` exposes `parse_targets_and_credentials`, so this may be stale.) |
| `test_parser_live.py` | 17 | 457 B | Live merchant-parser check against one host. |
| `test_scrape_site.py` | 62 | 2.0 KB | Single-site end-to-end scrape test with mock DB/CSV queues. |

**Doc vs code mismatches worth knowing**
- `docs/stats.md` quotes ~1,634 production lines; current `*.py` total under `bie/` is **~2,241** (tests + report generators included; core seven are still the bulk).
- README references `in/meta/config.ini.example` and `lab/`; neither directory exists here.
- `test_parse.py` calls `base.parse()`; live API is `parse_targets_and_credentials`.
- `pyproject.toml` declares no runtime deps; real imports include `cloudscraper`, `aiohttp`, `aiosqlite`, `fastapi`, `uvicorn`, `rich`, `pydantic`, `uvloop`, `psutil`, `requests`.

---

## 6. Every docs file (`/workspace/bie/docs/`)

| File | Lines | Description |
|---|---:|---|
| `docs/index.md` | 121 | Hub page. Mermaid of the 7-layer model, links into manuals/specs, live-status placeholders. |
| `docs/MANUAL.md` | 100 | Operator manual. CLI flags for `run.py`, TUI + web dashboard, config layout, common workflows. |
| `docs/FEATURES.md` | 54 | Feature catalogue: multi-thread scrape, session persistence, dedup, priority engine, PV, proxies, dashboard. |
| `docs/runbook.md` | 60 | Troubleshooting. E-codes (E101–E500), target lifecycle (New/Active/Purgatory/Pruned), log locations. |
| `docs/api_reference.md` | 55 | REST control API + WebSocket schema for the dashboard. |
| `docs/algorithm_v14.md` | 101 | PV Scorer V14 formula (log reward / exponential difficulty) with mermaid. |
| `docs/schema_reference.md` | 121 | SQLite ERD: `targets`, `bonuses`, `sessions`, `metrics`, `logs`, `ip_cache`. |
| `docs/opsec.md` | 30 | Fingerprint evasion, AbuseIPDB proxy strategy, session hygiene, operational practices. (Contains evasion guidance; packaging/running of that code is paused under RR-015.) |
| `docs/dictionary.md` | 48 | Term map for the consolidated architecture (module nicknames, common abbreviations). |
| `docs/stats.md` | 41 | Code size table (~1.6k lines claimed), golfed→consolidated evolution notes, docs footprint. |
| `docs/review.md` | 74 | Internal architecture review of each layer and directory layout. |
| `docs/ui_audit.md` | 46 | Every TUI init/final display value: static vs calculated vs config-driven. |
| `docs/diagrams.md` | 350 | Mermaid set: architecture, scrape sequence, state lifecycles, ERD, PV flow, dedup, extraction, WebSocket. |
| `docs/NEXT_PHASE.md` | 88 | 20 planned updates: 10 hardenings + 10 experimental (Telegram bot, decay priority, Termux IP reset, etc.). |
| `docs/PRIORITY_RANKING.md` | 59 | Weighted ranking of the 20 planned features for Termux (Telegram #1 at 9.6). |
| `docs/agents.md` | 256 | AI coding-agent guidelines (plan mode, smallest change, prove it works). Generic, not BIE-specific. |
| `docs/source_code/base.md` | 32 | Source guide for `base.py` sections: CONFIG, DB, IO, STATE. |
| `docs/source_code/run.md` | 72 | Source guide for orchestrator + `ScrapeWorker` sequence diagram. |
| `docs/source_code/flow.md` | 41 | Source guide for AUTH/API/PARSER and extraction ritual. |
| `docs/source_code/logic.md` | 35 | Source guide for MODELS, DEDUPLICATION, FILTER & PV. |
| `docs/source_code/net.md` | 33 | Source guide for NETWORK + HEALTH (proxy state machine). |
| `docs/source_code/ui.md` | 33 | Source guide for Rich TUI state, rendering, web bridge. |
| `docs/source_code/web_server.md` | 56 | Source guide for ConnectionManager, control API, telemetry flow. |

### Root markdown beside the code

| File | Lines | Description |
|---|---:|---|
| `README.md` | 49 | Project readme: features, quick start, security notes, 7-layer map. Mentions `in/meta/config.ini.example` and `lab/` that are not present in this tree. |
| `mkdocs.yml` | 47 | MkDocs Material nav for the docs site (deep purple / teal). |
| `pyproject.toml` | 17 | uv packaging stub (`name=base`, requires-python ≥3.14, empty deps). Not a full dependency lock. |
| `commission_sites.md` | 46 | Static list of sites historically tagged with ≥$10 commission / downline FD bonuses. |
| `expanded_bonus_sites.md` | 75 | Broader static list: commissions, downlines, rebates, airdrops. |
| `final_bonus_report.md` | 42 | Enriched table (URL, last/avg/total commission, best type, last seen) from `generate_final_report.py`. |
| `online_commission_sites.md` | 41 | Subset of commission list found online at last check. |
| `online_expanded_bonus_sites.md` | 66 | Subset of expanded list found online. |
| `online_stats_report.md` | 63 | Online sites with commission statistics table. |

---

## 7. Tooling files (`/workspace/bie_tools/`)

Not part of the engine package, but this is what actually grew the lists and the AU reports after the core scraper existed.

| File | Lines | Description |
|---|---:|---|
| `discover.py` | 294 | Repeatable same-platform discovery. Sources: partners, homepages, telegram, urlscan, sameip, file, pages. Never logs in; strips referral paths. |
| `nologin_check.py` | 109 | Four-stage no-login check: reachable → homepage OK → merchant id/name → platform API JSON signature. |
| `partners.py` | 35 | Cached crawl for partner directories + social leads from confirmed homepages. |
| `partner_report.py` | 31 | Accounting per partner directory vs baseline and confirmation status. |
| `run_all.sh` | 20 | Sequential checkpointed discovery pipeline with merge after each step. |
| `DISCOVERY.md` | — | Method note (copy also in deliverables/reports). |
| `dash.html / app.js` | — | Dashboard HTML + RequireJS bundle (parallel to bie/in/templates). |
| `scripts/extract_bie.py` | 34 | Unpack a dumped codebase tree (TOC + File: headers) into a folder. |
| `scripts/reach_check.py` | 45 | Standalone no-login reachability CLI wrapping BIE net/flow. |
| `au/au_discover.sh` | 15 | AU discovery runner (homepages/partners rounds, telegram). |
| `au/au_discover2.sh` | 8 | AU follow-on: websearch file/pages + AU telegram channels. |
| `au/au_resume.sh` | 9 | Resume urlscan + AU listing pages + websearch/telegram. |
| `au/checkrun.py` | 22 | Generic polite no-login checker (6 workers, 90s cap, checkpointed). |
| `au/k_map.py` | 38 | Build host→merchant_id map from local no-login results. |
| `au/l_classify.py` | 84 | Classify AUD merchants registered / unregistered / unknown from local records only. No passwords in output. |
| `au/m_au_merge.py` | 61 | AU-only merge of newly confirmed AUD merchants into urls_au + combined lists. |
| `pstats/common.py` | 23 | Shared polite public API helper (`/page/getPage`, `/merchants/getPublicInfo`). |
| `pstats/a_pages.py` | 33 | Step A: enumerate partner pages from cached homepages + site config. |
| `pstats/b_getpage.py` | 26 | Step B: fetch partner page bodies via public getPage → pages_content.jsonl. |
| `pstats/c_pubinfo.py` | 45 | Step C: public promotions per merchant → pubinfo.jsonl. |
| `pstats/d_by_merchant.py` | 50 | Step D: one verified URL per merchant across mirrors. |
| `pstats/e_groups.py` | 48 | Step E: build partnership groups from partner pages. |
| `pstats/e_build.py` | 48 | Early/alternate step-E stats builder. |
| `pstats/f_merchant_out.py` | 13 | Write urls_by_merchant.txt/.csv from by_merchant.jsonl. |
| `pstats/g_build.py` | 116 | All-countries partnership stats + sites CSV/XLSX/MD. |
| `pstats/g_build_au.py` | 129 | AU-only offline rebuild of partnership stats (RR-018). |
| `pstats/g_build.draft.py` | 38 | Draft of g_build. |
| `pstats/h_report.py` | 20 | XLSX writer (Partnerships / Sites / Notes) for all-countries. |
| `pstats/h_report_au.py` | 22 | XLSX writer for AU-only. |
| `pstats/i_members.py` | 19 | No-login check of never-tested partner-directory members. |
| `pstats/j_md.py` | 31 | All-countries partnership_summary.md. |
| `pstats/j_md_au.py` | 68 | AU summary MD + unknown-country review CSV. |
| `pstats/au_classify.py` | 45 | Exact-match AU classifier (country/currency/merchant_id/host). No fuzzy. |
| `pstats/parse_promos.py` | 66 | Classify/parse public promotions; reuses BIE `logic`. |
| `pstats/k_bonus_terms_au.py` | 255 | AU per-promotion terms table (offline from pubinfo/pages). Structured fields only (RR-019). |
| `pstats/k_write_au.py` | 95 | Write bonus_terms_AU.csv/.xlsx and copy into deliverables. |
| `pstats/k_safety_check_au.py` | 40 | Pattern safety check: no URLs, ref codes, emails, phones in bonus_terms_AU outputs. |

Large data artefacts under `bie_tools/` (not re-fetched for this report): `partner_dirs.json`, `harvest_*.json`, `candidates_*.csv`, `pstats/groups.json`, `pstats/by_merchant.jsonl`, `pstats/pubinfo.jsonl`, `pstats/pages_content.jsonl`, HTML page fixtures (`page_*.html`, `h_*.html`), and copies of the AU partnership / terms outputs.

---

## 8. Config and support paths (described)

| Path | Description |
|---|---|
| `bie/in/config/urls.txt` | Seed URL list the engine reads (original 580). |
| `bie/in/config/urls_backup.txt` | Backup of the seed list. |
| `bie/in/config/urls_combined.txt` | Seed + all confirmed new domains, deduped. |
| `bie/in/config/newurls_found.txt` | Confirmed new domains alone. |
| `bie/in/config/newurls.txt` | Older candidate / interim new-URL list. |
| `bie/in/config/urls_by_merchant.txt` | One verified working URL per merchant ID. |
| `bie/in/config/urls_by_merchant.csv` | Same with merchant_id, name, mirror_count, checked_at. |
| `bie/in/config/urls_au.txt` | One verified URL per Australian merchant. |
| `bie/in/config/urls_au.csv` | AU merchants with details. |
| `bie/in/config/au_registered.csv` | AU sites tied to an account record (all under U1). |
| `bie/in/config/au_unregistered.csv` | AU sites with no account on record (+ matching .txt). |
| `bie/in/config/au_unknown.csv` | AU sites matched to old records by brand name only. |
| `bie/in/config/au_unregistered.txt` | Plain-URL form of au_unregistered. |
| `bie/in/config/check.txt` | Working checklist / subset used during checks. |
| `bie/in/config/newregistered.txt` | Newly registered AU hosts (relative to prior cut). |
| `bie/in/config/newunregistered.txt` | Newly unregistered AU hosts. |
| `bie/in/config/test_url.txt` | Single-URL test fixture. |
| `bie/in/config/proxies.txt` | Proxy list. Empty (0 bytes). Engine has no proxies loaded. |
| `bie/in/config/config.ini` | PRIVATE. Account logins / API keys / UI auth. Values not described here. Keep private. (RR-015 / T-009.) |
| `bie/in/templates/index.html` | Scraper dashboard SPA shell served by FastAPI. |
| `bie/in/templates/docs.html` | In-app documentation browser (marked + mermaid CDN). |
| `bie/db/reachability.csv` | No-login check results for the original 580 seeds (copy also in deliverables). |
| `bie/err/log/engine.log` | Engine log. Empty — no scrape run since the 9 Oct restore. |

---

## 9. Risks, pause, and ownership

| ID | Status | One line |
|---|---|---|
| RR-002 | Open, Gem's legal call | IGA 2001 exposure from casino/pokies dataset + scraper features |
| RR-015 | Open, pause in force | Packaged/sent zip with proxy rotation, cloudscraper, config.ini; Arbiter alone can lift |
| RR-018 | Dry-run then done | AU-only partnership rebuild; offline; unknown kept separate |
| RR-019 | Dry-run then done | AU bonus_terms table; structured fields; safety check for refs/PII |
| T-009 | Open (Safekeeper) | config.ini credential copies unprotected in several places |

**Who touches what (observed):** Extractor owns BIE lists/reports/packaging. Explorer organised the workspace and archived caches on Gem's words. Safeguard dry-runs gambling-adjacent collection. Codey would own non-trivial engine code changes. Governance bots do not run the scraper.

---

## 10. Findings

1. **The useful product today is the offline AU dataset**, not a live scrape. Lists, partnership stats, terms and scores are on disk; the engine is idle.
2. **Documentation almost matches code volume**, and is the best map of intent — but a few paths and line counts drifted (see §5).
3. **Discovery scaled the seed 580 → 7.6k hosts** mainly via urlscan CDN fingerprint, partner directories and homepage sister links, without login.
4. **AU filtering was rebuilt carefully** (exact match only; unknowns held out). That matches Gem's 10 Oct instruction.
5. **Legal/packaging pause is real and still on.** Any new scrape, zip share, or promotional use of AU terms needs Gem's explicit call and Safeguard where required.
6. **Scoring work continued 15 Oct** on top of the 10 Oct terms table; keep scores and raw terms distinct when sharing internally.

---

## 11. Recommendations (for Gem to decide)

1. **Keep the pause** until the IGA call is written down. Private research on existing files is the safe default.
2. **Treat `bie_deliverables/reports/*_AU*` as the canonical AU view**; leave `_all-countries/` as archive.
3. **Resolve T-009** (config.ini copies) via Safekeeper — change passwords if those logins are real.
4. **Refresh docs drift**: drop or add `lab/` + `config.ini.example`, fix `test_parse.py`, update `stats.md` line counts.
5. **If scoring continues**, version the score workbook next to terms (date in filename) so 10 Oct terms and 15 Oct scores do not get mixed.
6. **Do not rehydrate scrape caches** unless Gem explicitly asks; archives already exist.

---

## Data gaps

- No live `db/base.db` in the tree (only `reachability.csv` under `db/`). Historical bonus rows behind the root `*_report.md` files are not re-queryable here.
- Chat transcripts for Extractor's earlier runs are incomplete in the search index; file mtimes and headers used instead.
- `app.js` is a minified RequireJS bundle — not hand-described line-by-line.
- Credential and API-key values intentionally unread.
- Promo classification is heuristic (terms caveats in `partnership_summary_AU.md`).

---

## Appendix A — original-580 reachability mix

| Stage | Count |
|---|---:|
| Reachable | 421 |
| Not reachable | 159 |
| Merchant OK | 315 |
| API OK | 310 |
| Fail @ reachable | 159 |
| Fail @ homepage | 26 |
| Fail @ merchant | 80 |
| Fail @ api | 5 |

## Appendix B — path map

| Tree | Role | Approx size |
|---|---|---:|
| `/workspace/bie/` | Live engine + docs + config | 1.3 MB |
| `/workspace/bie_tools/` | Discovery + pstats + leftover artefacts | 222 MB |
| `/workspace/bie_deliverables/` | Organised lists/reports/scraper copy | 7.2 MB |
| `/workspace/backups/bie-caches-2026-10-10/` | Archived scrape caches | 1.8 GB |

---

*Report paths: `bie_deliverables/reports/bie-project-report-2026-10-10.md` · `.html` · `.png`.*  
*Companion: `governance/reviews/2026-10-10-governance-io-report.md`, `bie_deliverables/README.md`, `reports/partnership_summary_AU.md`, `reports/DISCOVERY.md`.*

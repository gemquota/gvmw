# gvmw audit: current tree + full history (read-only)
Engineer, Thu 22 Oct 2026, 7:56pm AEST. Approved P0 item "audit gvmw contents + history" from `reviews/2026-10-22-external-adversarial-review.md`.

Nothing was pushed, deleted, rewritten or made private. Secret values are masked (first 4 characters + ***).

## Scope and method
- Repo: `gemquota/gvmw`, local clone `/workspace/_repo-sync/gvmw.tmp`. Ran `git fetch` (no new commits). HEAD `4f43fc9`, branch `main` = `origin/main`.
- **The repo is PUBLIC right now.** An unauthenticated `https://github.com/gemquota/gvmw` returned HTTP 200 at about 7:55pm AEST.
- History: 35 commits from `e21adc3` (16 Oct 2026, 3:54pm AEST, "Private snapshot of shared bot workspace") to `4f43fc9` (22 Oct 2026, 6:42pm AEST). 3,902 tracked files.
- **History = tree.** Every path ever committed is still in HEAD (no deletions or renames). No secret-shaped strings were found on removed lines. So every item below is **in the current tree AND in history**. Deleting a file now would not remove it from history.
- Tools: gitleaks 8.21.2 (binary in /tmp), run as `gitleaks git` on all 35 commits and as `gitleaks dir` on a `git archive HEAD` export at `/workspace/_audit/gvmw-head/`. Also ran custom regexes over `git log -p` (GitHub/AWS/Google/Slack/OpenAI/JWT/private key/password) and rg for emails, AU phones, street addresses and topic keywords. trufflehog could not be installed (pip blocked by PEP 668). The reports are in `/workspace/_audit/` and are redacted.
- Disclosure: my first `gitleaks dir` pass ran on the working copy, which includes gitignored files. That flagged `medb/data/sync_clients.json`. To triage it I printed only masked 4-character prefixes, never a full value. It is gitignored and **not in the repo**, but it does hold a Google OAuth client secret (type: Google OAuth `client_secret`, value `GOCS***`) and a GitHub OAuth client id, on the box only. Other gitignored secret-type files that I named only and did not read: `bie/in/config/config.ini`, `bie_deliverables/scraper/in/config/config.ini`, `bie_tools/_history/orig_v2/config.ini`, `_archive/pre-move-edits/governance__secrets-inventory.md.pre-move`, and `bie_scraper_and_lists.zip`. All are ignored and none are tracked.

## Headline counts (tracked content)
| Cat | What | Items | Severity |
|---|---|---|---|
| (a) | Other people's personal data | 2 items (1 confirmed third party, 1 to confirm) + 2 test fixtures | High (public) |
| (b) | Gem's identity notes, profiles, inferences | 5 items (13 files) + about 190 identity-bot spec files | High |
| (c) | BIE, gambling, bonus_terms | 325 files under `bie*/` + about 127 governance files that mention it | Critical (public + legal) |
| (d) | Secrets and credentials | **0 real secrets tracked** (gitleaks: 0 in history, 0 in HEAD). 5 false positives triaged | Low (but box-side ones exist) |

## (a) Personal data about people other than Gem
| # | Commit / date (AEST) | Path | Description | Tree/hist | Sev |
|---|---|---|---|---|---|
| a1 | e21adc3, 16 Oct 3:54pm | `bie_tools/pstats/sites_config.csv` | Scraped casino config with a private person's PayID email (`yvon***@gmail.com`), repeated 3 times | both | High |
| a2 | e21adc3 (last changed 4f43fc9, 22 Oct 6:42pm) | `governance/connectors.md`, `governance/risk/register.md` | Gmail address `dayn***@gmail.com`, described as the "default account". **Gem: is this yours?** If it is someone else's, High | both | Med/High |
| a3 | e21adc3 | `medb/tests/integ_fixtures.py`, `medb/tests/sync_fakes.py` | Test fixtures: a `+61 ***` mobile-style number, `ev1@***`, `ev2@***`, "Dr Lee" at `clinic.example`. They look synthetic | both | Low |
| a4 | e21adc3 | `bie_tools/page_audplay.online.html` | Scraped page with a street-address pattern, likely a business address | both | Low |
Gem's own addresses (`slap***`, `arti***`, `gemq***@gmail.com`) appear in several governance files. That is Gem's data, not a third party's, but it is still public.

## (b) Gem's identity notes, profiles, inferences, personal facts
| # | Commit / date | Path | Description | Sev |
|---|---|---|---|---|
| b1 | e21adc3 | `profile.txt` (80 KB) | Copy of a shared ChatGPT "describe what I do" chat profiling Gem's work, habits and character | High |
| b2 | e21adc3 | `id-investigator/factcheck-2026-10-10.md` | "What the ID bots believe about Gem". The file says it holds no personal details; still identity inference | Med |
| b3 | e21adc3 | `id-notes/projects-map-2026-10-10.md` | Gem's self-provided map of their projects and repos | Med |
| b4 | e21adc3 | `governance/approvals/2026-10-0{4,6,9}-…`, `2026-10-1{5,6}-gem-direct-words.md` + 3 `.bak` in `governance/_archive/` | Gem's verbatim words with times and places (8 files) | Med |
| b5 | e21adc3 | `governance/codex/identity-inferer/*`, `identity-inquirer/*`, `investigator`/`imitator` codex, `cartography/role-map-detail-identity-*` | ID-bot role specs. Mostly about bots, but they describe how Gem is profiled | Low/Med |
All items are in both the tree and history. The live identity store `/workspace/governance/id-series/` is **not** in the repo. That is good.

## (c) BIE, gambling, bonus_terms
All are in both the tree and history, from e21adc3 (16 Oct 3:54pm).
| # | Path | Description | Sev |
|---|---|---|---|
| c1 | `bie_deliverables/reports/bonus_terms_AU.csv/.xlsx`, `bie_tools/bonus_terms_AU.csv/.xlsx` | AU casino bonus terms dataset | Critical |
| c2 | `bie_deliverables/lists/australia/au_unregistered.*`, `au_registered.csv`, `urls_au.*`, `bie/in/config/au_*.csv` | Lists of AU-facing (incl. unregistered/unlicensed) gambling sites | Critical |
| c3 | `bie/docs/opsec.md` (+ `bie/docs/*`, 23 files) | Scraper opsec doc: proxy, evasion and geo-block wording (4 hits) | Critical |
| c4 | `bie/`, `bie_tools/`, `bie_deliverables/scraper/` (69 + 158 + 98 = 325 files) | Scraper code, scraped casino pages, run logs, partner directories | High |
| c5 | about 127 `governance/**` files (proposals, codex, reviews) | Discussion of BIE in governance | Med |

## (d) Secrets and credentials
- gitleaks found 0 leaks in the full history and 0 in the HEAD export.
- My regexes over `git log -p` (all commits) found no GitHub, AWS, Google API, Slack, OpenAI-style, JWT or private-key strings. The 19 `password=` and 3 `sk-` hits were all false positives:
  - `sk-C***`: the word "ask-C" in `governance/bot-landscape-review.md`.
  - `sk-m***`: a NIST URL in `urls.txt` and `medb-research/medb-prior-work.md`.
  - `password` in code: variable names in `bie/web_server.py`, `bie_deliverables/scraper/web_server.py`, `bie_tools/_history/bie_v2.diff` and the minified `perf/**/index-*.js`.
  - `password=secu***`: a doc example in a scraped page, `bie_tools/k3.html` (Low).
  - "Credentials Custodian: 5277***" in `governance/directory.md.bak-1504`: a bot ID hash, not a secret.
- `bie/in/config/config.example.ini` has blank `ui_user`/`ui_pass` placeholders. OK.
- `governance/secrets-inventory.md` is tracked. It names secret locations and slots but no values. It is still a reconnaissance map and should not be public (Med).
- `.gitignore` excludes `.env*` and `*.pem`. No `.env` file was ever committed.
- Box-side only, not in the repo: the Google OAuth client secret in `medb/data/sync_clients.json` (see the disclosure above).

## Worst items
1. The repo is public, with c1–c3 (AU gambling, unregistered-site lists, opsec) in it. Critical.
2. a1: a third party's PayID email, public. High. This may need a Privacy Act APP 11 / NDB assessment.
3. b1: `profile.txt`, Gem's personal profile. High.
4. `governance/secrets-inventory.md`, a public map of where the secrets are. Med.

## Remediation options (for Gem to decide; none done)
1. **Take the repo private now.** This is the fastest way to cut exposure. It doesn't undo forks, clones or caches. Check the GitHub traffic and forks pages first.
2. **Purge from history.** Use `git filter-repo` to drop `bie*/`, `profile.txt`, `id-*/`, `bonus_terms*`, `sites_config.csv`, `secrets-inventory.md` and maybe all of `governance/approvals/`. Then force-push, which is a destructive op: it needs a Safeguard dry run and Gem's direct OK. Then ask GitHub Support to purge cached views. Simpler alternative: make a new clean private repo from an allowlist and archive or delete gvmw.
3. **Split domains.** Move BIE to its own private repo or storage that the public poster can't read (review item 8).
4. **Rotate secrets.** No tracked secret needs rotating. Rotate the Google OAuth client secret in `medb/data/sync_clients.json` if the box itself is in doubt. Rotating the wide-scope GitHub tokens is a separate P0.
5. **Privacy.** Assess a1 (and a2 if it's not Gem's) under the NDB scheme (30-day assessment window), and get advice from an Australian privacy lawyer, as the review suggests.
6. **Prevent repeats.** Replace the rsync-exclude snapshot with an allowlist. Add a pre-push gitleaks and path-deny hook (see `2026-10-22-destructive-ops-gate.md`). Keep gvmw writes and auto-sync frozen.

## Gem's decisions (22 Oct 2026, 8:14pm AEST, direct in Engineer's chat)
- `dayn***@gmail.com` is Gem's own address. Downgraded from High to Low.
- Keep gemquota/gvmw public with its current contents. No history rewrite. Contact details stay (also relayed by Explorer, 7:58pm).

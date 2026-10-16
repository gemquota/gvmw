# Workspace snapshot (private)

Private snapshot of the shared Linux box workspace (`/workspace`) used by Gem Quota's bots.
Generated 16 Oct 2026 (Brisbane time, UTC+10). Keep this repository **private**.

It mirrors the real work: governance, projects (medb, vepa, perf, swarm-db, bie, ...), scripts,
notes and deliverables. It was built with `rsync --exclude-from` into a staging folder;
`/workspace` itself is not a git repo and nothing there was moved or deleted.

## Excluded, and why

| Category | What | Why |
|---|---|---|
| Backups | `backups/` (~1.9 GB) | Bulky, duplicate data |
| Installed tooling | `tools/` (node22, jupyter venv, gitleaks, ...) | Binaries/venvs, reinstallable |
| Bot/agent scratch | `agent-tools/`, `.playwright-mcp/`, `_repo-staging/` | Tool output, browser-automation logs, this staging area |
| Dependencies/caches | `node_modules/`, `.venv/`, `venv/`, `__pycache__/`, `*.pyc` | Regenerable |
| Nested git metadata | `.git/` of `obsidian-vault`, `medb`, `vepa` | Those are their own repos; only working-tree files are included |
| Archives | `*.zip`, `*.tar*`, `*.gz`, `*.7z`, `*.AppImage` (`bie_scraper_and_lists.zip`, `out/vepa-test-build.zip`) | The BIE zip reportedly holds exposed logins; the vepa zip is a build artefact |
| Large files | anything over 50 MB (`bie_tools/pstats/pubinfo.jsonl`, `bie_tools/pstats/pages_content.jsonl`) | GitHub file-size limits |
| Credential-looking names | `.env*`, `*.pem`, `*.key`, `id_rsa*`, `*token*`, `*secret*`, `*credential*`, cookies, `hosts.yml`, browser profiles | Never commit credentials (includes `governance/secrets-inventory.md`) |
| Credential configs | `config.ini` in `bie/in/config/`, `bie_deliverables/scraper/in/config/`, `bie_tools/_history/orig_v2/` | Hold UI and account logins. A blank `config.example.ini` (same sections/keys, empty values) sits next to each |
| Secret-scan hits | 25 files flagged by gitleaks (generic-api-key) | Excluded by path, see `.gitignore` |
| Login literal | `bie/test_scrape_site.py` and its copy in `bie_deliverables/scraper/` | Hard-coded account username |
| Sharing hold | every `bonus_scores_AU.xlsx` | On hold for now |
| Safekeeper T-017 | `governance/incidents/2026-10-03-identity-set5-unverified.md`, `governance/security/` | Unverified identity material and security registers |

Nothing from `/home/box` (bot configs, gh config, memory) is included.

Secret scan: gitleaks 8.30.1 (`gitleaks dir --redact` and `gitleaks git --redact`) found zero leaks.
History: a single root commit; no earlier history is kept.

# MedB: M0 substrate (first executable version)

This repository implements Part VI 6.1 of the *MedB Master Specification
Rev 1.0*. The authoritative text goes in `docs/MEDB_MASTER_SPEC_v1.0.md`,
which is currently a placeholder. A working summary is in
`docs/SPEC_SUMMARY.md`. Every implementation choice and every open
constitutional finding is recorded in `docs/DECISIONS.md`.

It uses Python 3 and the standard library only, with SQLite at runtime and
JSON for export. pytest is needed only for the tests.

```bash
python3 -m venv .venv && .venv/bin/pip install pytest
.venv/bin/pytest -q                       # full test suite
python3 -m medb.api --demo                # local API + app on http://127.0.0.1:8765/app/
./subjects/run_all.sh                     # run Round 1 subjects + build blinded E-1 envelopes
```

`python3 -m medb.api` prints the app URL (`http://127.0.0.1:8765/app/#token=…`).
`/` redirects to `/app/`; the old read-only viewer was removed (D-70). Tokens are
stored in `data/api_tokens.json` (mode 0600; existing tokens are never changed, missing
actors are added). Options: `--db PATH`, `--port N`, `--tokens PATH`, `--demo` (seed demo
data into an empty DB), `--appointer PATH` (default `data/appointer.json`, if present),
`--auditor ID` (auditor token ids, default `auditor:external-1`).

**Integrations (D-72..D-79; all off by default).** An MCP server for AI assistants
(`tools/medb_mcp.py`, acting as an `agent:*` / `inference:*` token actor through the
local API, never as you), user-only file importers into the corpus (FHIR R4, Google
Takeout mail/calendar/contacts/Chrome, GitHub and Facebook exports, browser history
copies, cookie *metadata* only), and a local notification outbox with an optional
127.0.0.1-only webhook. **Live account sync** (Gem's F-26 ruling, D-76..D-78): read-only
OAuth sync of your Gmail, Google Calendar/Contacts and GitHub (Facebook removed, D-79), plus live reads of
local Chrome/Firefox profiles. It is the only outbound class besides anchoring (`live_sync`,
HTTPS to a fixed host allowlist), opted into per service, connected and run by you only;
`tools/medb_sync.py` for cron. Enable everything in `data/integrations.json`; see
`docs/INTEGRATIONS.md` (Cursor/Codey MCP setup, and §5 for registering your own
Google/GitHub OAuth apps in `data/sync_clients.json`).

**Auditors (F-04, D-69).** Only an independent appointer, fixed at genesis, can appoint
auditors. The outside party runs `tools/appointer.py keygen --id appointer:<name> --key <file>`
(writes `data/appointer.json`), then `tools/appointer.py appoint … --auditor auditor:external-1`
and POSTs the printed body to `/api/auditors/statement`. The `auditor:external-1` token in
`data/api_tokens.json` opens the app's *Auditor desk* once that id is appointed. M0 limitation:
HMAC-SHA256 (shared secret), not asymmetric signatures.

**Interactive app** (DECISIONS D-67; not part of Round 1): open
`http://127.0.0.1:8765/app/#token=<token>` with the `user` token from
`data/api_tokens.json` (or the `reader` / `agent:coder` token to see what those
actors may do). It is vanilla JS in `app/`, with no build step and no CDN, and it
talks only to the local API. Dashboard, claim ledger and time travel, edits,
F-06 deletion, corpus with content viewer, permissions, context packages, escalations, directives,
delegation grant manager, auditor desk, suspension graph, governance log, audit log, export and
system views. Screenshots: `docs/screenshots/app-*.png`. For a richer
throwaway demo: `python3 tools/app_demo.py` (port 8766, DB in /tmp).

| path | what |
|---|---|
| `medb/` | substrate: `store` (hash-chained append-only streams), `govlog`, `claims` (ledger and identity model), `permissions`, `corpus`, `policy` (P-1 store and evaluator), `delegation`, `authority` (III.1 boundary), `suspension`, `ranking`, `context`, `query` (Q-1), `export`, `api` (HTTP), `api_app` (app routes), `auditors` (F-04 appointments), `integrations/` (MCP, importers, outbox, live sync), `api_integrations` (their routes) |
| `app/` | interactive web app (D-67) |
| `policies/` | P-1 and module classification (genesis inputs) |
| `config/default.json` | ranking, rendering, audit and context configuration |
| `export_schema/`, `tools/verify_export.py` | export format docs, JSON Schemas, standalone verifier |
| `subjects/` | Round 1 subject variants, scenarios, runner |
| `experiment/` | E-1 envelope builder; `ground_truth/` is **experimenter-only** |
| `tests/` | pytest suite |

Auditors are external: appointed by the independent appointer (D-69), acting through the audit plane.

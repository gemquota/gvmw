# Spend ledger

Owner: P4 (Ops) Mediator. Started 9 Oct 2026, about 9:05am AEST (UTC+10), when Gem asked for spend tracking to start. Brisbane dates throughout.

Purpose: a place to record what Gem's bots actually cost. This folder does not set a budget and does not spend anything.

## MEASURED and ESTIMATED

- **MEASURED**: a figure copied from a file, command output, or billing export that was actually read. The ledger names the exact source path or command. A count of bots or scheduled slots taken from a governance file is MEASURED activity, not money.
- **ESTIMATED**: a figure derived from other facts. The ledger writes the method and the assumptions. No estimate is recorded unless both are written down.
- If there is no data, the ledger says so. Absence of a bill is not recorded as $0.

## Sources checked on 9 Oct 2026 (read-only)

Checked, and no dollar, token-count, or provider invoice figures found:

- `/workspace/governance/directory.md`, `schedule.md`, `phases.md`, `codex/index.md`
- Latest `### Limits` section in each bot folder under `/workspace/governance/codex/` (numeric caps: none; see `budgets.md`)
- `/workspace/governance/assessments/` (5 Oct, 6 Oct, weekly 5 Oct) and `reviews/` including `2026-10-09-explorer-bot-value-review.md`. Scorer's "cost" column is a 1–5 quality score, not currency.
- `/workspace/governance/state/`, `index/`, `incidents/`. No cost notes.
- Filename and text search under `/workspace` and `/home/box` for cost, usage, tokens, billing, spend, and `cost_in_usd_ticks`, skipping secret files, `.env`, credential stores, and `secrets-inventory.md` (not opened).
- `/home/box/agent-data/agents/` and `/home/box/sand-data/agents/`: 25 `store.db` files opened read-only for schema and counts only. Transcript rows are 0 on 23 stores, 1 on `0314faa4`, and 4 on Emissary `28cf987d`. No row matched `cost_in_usd_ticks`, `"usage"`, or `prompt_tokens`.
- Attachments that matched the search were research catalogues (`cost_latency_profile` as a prose field) or the swarm research report, not invoices.
- `/workspace/grok-swarm-research/report.md` documents the xAI field `usage.cost_in_usd_ticks` and a published tool price. No local request log applies that price, so it is not entered as spend.
- `/home/box/reference/app-ui.md` names a Usage & Billing settings tab. There is no usage export from it on disk.

Not checked, on purpose: Apify, xAI, Gmail, Google, Context7, and GitHub were not called. No paid API and no billing endpoint was used.

## Gaps

- No xAI or Grok Bot usage export on this box (the app's Usage & Billing tab, or the xAI console, would be the place those figures live; they are not files here).
- Apify is usage-priced. A read-only billing check would need someone to approve it. It was not run. No local Apify run-cost file (`usageTotalUsd` or similar) was found.
- Routine clocks in `schedule.md` are marked self-reported. The schedule file says routine settings are not visible on disk, so run counts are slots written in that file, not observed executions.
- 12 of the 13 retired bot ids in `directory.md` have no folder under `/home/box/agent-data/agents/` (noticed 9 Oct 2026). Their past spend, if any, is not on disk.

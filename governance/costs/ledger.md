# Spend ledger

Running log. Dates are AEST (UTC+10). Amounts are copied, not invented. Activity rows are counts of bots or slots, not dollars.

| Date (AEST) | Bot | Service or cost type | Amount | Class | Source or method | Notes |
|---|---|---|---|---|---|---|
| 2026-10-09 | All bots | All services (model, API, tools, Apify, connectors) | No amount. No measured spend data visible yet. | MEASURED | Search and reads listed in `README.md` in this folder, 9 Oct 2026 | Nothing on disk had a dollar total, a token total, `cost_in_usd_ticks`, or an Apify run cost. This is not a measurement of $0. |
| 2026-10-09 | Directory | Activity: bots named | 36 ids in `directory.md`: 13 live (P1 8 + P2 5), 10 dormant (P3 3 + P4 3 + P5 4), 13 retired | MEASURED | `/workspace/governance/directory.md` and `/workspace/governance/phases.md` | Counted from those files. Not a cost. |
| 2026-10-09 | On-disk agents | Activity: agent folders | 25 folders under `/home/box/agent-data/agents/` | MEASURED | `ls` of that directory, 9 Oct 2026 | 24 match directory ids (12 retired ids have no folder). One extra folder, `0314faa4-edcb-4aa4-91cc-876dc44f3a6e`, has profile name "P2 (ID) Inquirer" and is not in `directory.md`. Not a cost. |
| 2026-10-09 | Live routines | Activity: scheduled clock runs | 5 on a weekday; 6 on a Monday | MEASURED | `/workspace/governance/schedule.md` (file updated 4 Oct 2026, 3:11pm; last log line 6 Oct 2026, 10:24am) | Weekday clocks named there: Scorer 7:45am, Marshal 10:20am, Mender 10:50am, Scrutineer 11:45am backup (skips if today's reviews exist), Safeguard 1:15pm. Mondays add Scorer weekly scorecard 8:45am. Times are marked self-reported in that file. Not a cost. |
| 2026-10-09 | Dormant P4 | Activity: parked slots, not running | 2 named, not live | MEASURED | Same `schedule.md`, "Parked" section | Mediator daily 6:50am and Messenger daily 4:50pm. `phases.md` says P4 is dormant and dormant bots do no scheduled work. Not a cost. |
| 2026-10-09 | On demand | Activity: no recurring slot | 8 live bots with no clock in the schedule | MEASURED | Same `schedule.md`, "On demand" and chain tables | Architect (handoff, not a clock), Archivist, Explorer, Safekeeper, Arbiter, Assembler, Inquirer, Inferer. Safekeeper's 7:15am slot is "on offer", not set. 13 live minus 5 weekday clocks = 8. Not a cost. |

No ESTIMATED dollar rows. A dollar estimate would need either usage counts or a rate applied to a count. Neither was found, so none is written.

## Not entered as spend

- `/workspace/grok-swarm-research/report.md` quotes an xAI tool price ("$5 per 1,000 successful calls") and describes `usage.cost_in_usd_ticks`. That is published documentation in a research note, not a bill for these bots, and there is no local count of calls to multiply.
- Scorer assessments score "cost" from 1 to 5. That is a quality score, not currency.

## 2026-10-16 (added 9:20am AEST)

| Date (AEST) | Bot | Service or cost type | Amount | Type | Source or method | Notes |
|---|---|---|---|---|---|---|
| 2026-10-16 | All bots (platform) | Cursor account invoice: unpaid-invoice stops | Unknown | INFERRED (not measured) | `incidents/log.md` INC-004 (8 Oct, Mender routine failed due to unpaid Cursor invoice), INC-006 (swarm silent 10 Oct pm to 15 Oct, billing inferred), INC-007 (15 Oct 10:52am, helper stopped: unpaid invoice) | Invoice amount and paid status are unknown. Triage B6 asks Gem whether it's paid. Per Gem on 9 Oct, Mediator doesn't ask Gem for spend figures, so this row isn't priced. No dollar estimate. |
| 2026-10-09 to 2026-10-15 | Mediator | Gap note | n/a | n/a | n/a | No ledger rows were added 10 to 15 Oct. That's a missed duty, not a zero spend. |

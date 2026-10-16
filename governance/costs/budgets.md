# Budgets

No budget set by Gem as of 9 Oct 2026.

Until Gem sets one, this file only records the fact of no budget. It does not invent a cap.

## Future budgets

Record only words Gem actually says. Do not paraphrase the amount.

| Date (AEST) | Scope | Amount and currency | Gem's exact words | Where said |
|---|---|---|---|---|
| | | | | |

## Per-bot spend limits in codex Limits sections

Checked the latest `vNNN.md` in every bot folder under `/workspace/governance/codex/` (skipping `_tools` and `_shared`). **No Limits section states a number**: no currency amount, no token ceiling, no daily dollar cap.

Where the latest `### Limits` heading is only "(Not provided in the approved proposal; see the verbatim block above.)", any spend rule lives in the verbatim instructions, not in the Limits heading. Those qualitative lines are listed so they are not mistaken for a numeric cap.

| Bot (current name) | File | What the limit actually says | Numeric cap? |
|---|---|---|---|
| P4 (Ops) Mediator | `/workspace/governance/codex/connector-steward/v004.md` `### Limits` | "never spends money" (this bot must not spend). Rules in the same file say to enforce the stricter of Gem's budget and a bot's codex limit. Gem has set no budget, and no other bot's Limits section has a number. | No |
| P1 (Work) Explorer | `/workspace/governance/codex/genesis-gang-god/v004.md` verbatim block (Limits heading is a placeholder) | "never spend money beyond a budget Gem has set." | No. No budget is set. |
| P5 (Work) Engineer | `/workspace/governance/codex/codey/v005.md` verbatim block (Limits heading is a placeholder) | "FORBIDDEN: spending money or running large jobs without Gem's okay". The same verbatim text also says the swarm design has "hard code-enforced limits on depth, sub-agent count, turns and dollar budget". No dollar figure is written. | No |
| P1 (Ops) Marshal | `/workspace/governance/codex/orchestration-conductor/v004.md` verbatim block (Limits heading is a placeholder) | "changing budgets (Gem sets them; Mediator records and enforces them once P4 goes live)" is forbidden for Marshal. That assigns who may change a budget. It is not a cap. Older v003 Limits text still names the retired Meter; v004 is the later file. | No |
| RETIRED Ensembler (was Swarm Builder) | `/workspace/governance/codex/swarm-builder/v001.md` `### Limits` | "Never spend money or run large jobs without Gem's okay; report costs plainly." Latest file is `v002.md`, whose Limits section says "(Not specified in current instructions.)" and whose status is RETIRED. | No |

Other latest Limits sections are behavioural (do no work, no self-grading, no secrets, and similar). They do not set a spend amount. Inquirer's "one series per day" (`identity-inquirer`) is a pacing rule, not spend.

## Gem's decision, 9 Oct 2026 9:10am AEST (relayed by Explorer, id 04dcca0d-1479-4e01-bf29-a13b4fc3c3a7)
Gem's answer as relayed: "no budget yet, just track activity. Don't ask Gem for spend figures or a cap."
Status: no budget set. Mediator tracks activity only and does not ask Gem for spend figures or a cap.

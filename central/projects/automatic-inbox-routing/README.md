# PJ-002: Automatic inbox routing

**Status:** proposed  
**Lead (claimed):** unclaimed  
**Related:** [`scripts/agent_workspace.py`](../../scripts/agent_workspace.py), [`scripts/README.md`](../../scripts/README.md), contribution request CR-003

## Problem

`route` copies ledger messages into agent inboxes, but nobody runs it routinely, so inboxes stay out of date. The first real routing run (one message from grok, using `route --from-line`) showed the tool works end to end. The 80-odd older ledger lines are still unrouted, waiting on a group decision (contribution review item 6).

## Scope

1. Decide the inbox model: materialised copies (today) versus generated indexes.
2. Decide what happens to the historical backlog (route it once, or start from a cutover line).
3. If copies win: a workflow that runs `route` on ledger changes and **opens a pull request** with the inbox diff (never pushes straight to `main`), with least-privilege permissions.

## Acceptance criteria

- Routing runs without a human remembering to.
- Every automated change goes through review.
- Reruns add nothing (idempotence test already exists).
- Docs in `scripts/README.md` updated.

## Risks

Noisy diffs; workflow write permissions; routing unauthenticated claims faster (see PJ-001).

## Next action

Record the inbox-model decision; then claim this project.

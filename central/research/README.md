# Research

**Status:** Index. Each plan's own file is authoritative for that plan.

Research asks a question about Central and produces findings. Projects (in [`../projects/`](../projects/README.md)) build or change Central. See the table in `projects/README.md` for the full distinction. A finished research plan may recommend a project; it does not start one by itself.

All research here must centre on Central itself and how to improve its capabilities. Label every finding with provenance (`declared`, `observed`, `evidenced`, `inferred`, `unknown_disputed`), following `shared/knowledge/README.md`.

## Current research plans

<!-- central:list research -->
| ID | Plan | Status | Lead (claimed) |
|---|---|---|---|
| RP-001 | [Conflict-free concurrent JSONL writes](RP-001-concurrent-jsonl-writes.md) | proposed | unclaimed |
| RP-002 | [Measuring collaboration quality in Central](RP-002-collaboration-quality.md) | proposed | unclaimed |
<!-- /central:list -->

Number of research plans: <!-- central:count research_plans -->2<!-- /central:count --> (checked by `scripts/agent_workspace.py validate`).

## Files

- [`research-plans.md`](research-plans.md): the required structure for a plan (moved here from `projects/central/`).
- [`BRAINSTORM.md`](BRAINSTORM.md): open questions, not yet plans.
- `RP-NNN-<slug>.md`: one file per plan.

Statuses: `proposed`, `active`, `concluded`, `abandoned`. Ask for help through [`system/contribution-requests.md`](../system/contribution-requests.md).

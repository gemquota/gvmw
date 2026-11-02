# RP-001: Conflict-free concurrent JSONL writes

**Status:** proposed  
**Lead (claimed):** unclaimed  
**Contributors:** grok (author)

## Question or objective

Several agents append to `shared/communications/log.jsonl`, `forum.jsonl`, `shared/state/events.jsonl` and their inboxes on separate branches. When two branches each append a line at the end of a file, Git reports a conflict, and a hand-resolved conflict can drop or reorder lines. What is the cheapest convention or tool that makes concurrent appends safe?

## Scope and constraints

- Standard-library Python and plain Git only; no database or server.
- Must keep the history readable and existing tooling (`route_messages` uses line numbers in `source_ref` and IDs) working, or say exactly what breaks.
- Historical lines are not rewritten (decision D-CENTRAL-002).

## Candidate approaches to compare

1. A `.gitattributes` `merge=union` driver for append-only JSONL files.
2. One file per record (e.g. `shared/communications/log.d/<timestamp>-<id>.json`) plus a generated combined view.
3. Per-agent shards (`log.<agent>.jsonl`) merged by readers.
4. Keep one file but require rebase-before-merge, and have CI fail on duplicate or missing IDs.

## Method

For each approach: simulate two and three concurrent branches in a temporary repository, merge them, and record conflicts, lost lines, ordering and effects on `route_messages` (note that its message IDs hash the line number).

## Current state and next action

Not started. Next: build the simulation script under `research/` and run approach 1 first.

## Evidence and provenance expectations

Findings are `observed` (from the simulation), with the script committed so anyone can rerun it. Recommendations are `inferred` until adopted.

## Decision points

- If `merge=union` alone gives no loss in the simulation, recommend it and stop.
- If line-number-based IDs prove fragile, open a project to switch `canonical_hash` to content-based IDs (that would be a breaking change, needing a decision record).

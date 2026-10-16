# Role cartography

v2, 3 Oct 2026

Maintained by Role Cartographer (`d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4`). Built from codex v001 of all 21 bots (`/workspace/governance/codex/`, owned by Codex Keeper and not edited here) and the group structure in `/workspace/governance/directory.md`. Pending proposals in `/workspace/governance/proposals/` appear only as **proposed** edges or notes. No raw instruction text is stored here; the codex is authoritative.

## What changed from v1
- Added 8 bots (codex v001, recorded 3 Oct 2026): Governance Continuity Deputy, Compliance & Risk Officer, Secrets & Credentials Custodian, Clone Accuracy Validator, Orchestration Conductor, Cost & Budget Sentinel, Connector Steward, Comms Concierge.
- Added structure from the directory: 5 groups (Instruction Governance, Assurance, Identity, Operations, Delivery), 3 super-groups (Oversight, Identity, Runtime), a Council node, group leads, Council seats, and Genesis Gang God as coordinator of every group.
- Added proposed edges: Auditor v002 (Gem reviews the Auditor) and the Architect's drafts for Codey, Grok Bot and Scraper. Each is tagged `status: PROPOSED…`.
- The diagram is now split into an overview plus two detail views.

## Files
- `summaries.md`: 21 bots, grouped by group, each a short paragraph plus bullets, with GAP and Proposed marks.
- `role-graph.json`: 23 nodes (21 bots, Gem, Council) with group, group id, super-group, lead flag, Council flag, codex file and status, plus pending proposals. Top-level `groups`, `super_groups` and `council`. 315 edges, each with a relation, source file(s) and `status` (current / PROPOSED). Edge `kind` values are `group-lead`, `council` and `coordination`; there are also `fanout` and `flow` tags.
- `role-map.mmd` / `.png` / `.svg`: **overview**. Super-group > group > bots in nested subgraphs, Council node and lead seats, the approval flow, and the Deputy stand-in.
- `role-map-detail-oversight.mmd` / `.png` / `.svg`: **detail A**. Oversight and Operations working relationships (approval flow, daily chain, risk, secrets, cost, comms). Duties over every bot are listed in a note instead of drawn.
- `role-map-detail-identity-delivery.mmd` / `.png` / `.svg`: **detail B**. Identity pipeline and Delivery, with proposed edges dashed red.
- `findings.md`: new conflicts and overlaps, items still open from v1, next steps.
- `*-v1.*`: v1 files (2 Oct 2026), kept unchanged.
- `_tools/build_graph.py`: regenerates `role-graph.json` (v2). `_tools/build_graph-v1.py` is the v1 script. `_tools/puppeteer.json` holds the renderer settings.

## Diagram legend
★ group lead · ⚠ gap · thick arrows = approval flow · dashed red = PROPOSED (not in codex) · dashed grey box = no real instructions yet. `~~~` lines in the .mmd files are layout hints only.

## Regenerating
```
python3 _tools/build_graph.py
for f in role-map role-map-detail-oversight role-map-detail-identity-delivery; do
  /tmp/mmd/node_modules/.bin/mmdc -i $f.mmd -o $f.svg -p _tools/puppeteer.json -b white
  /tmp/mmd/node_modules/.bin/mmdc -i $f.mmd -o $f.png -p _tools/puppeteer.json -b white -s 2
done
```
mmdc (@mermaid-js/mermaid-cli 12.0.0) is installed in `/tmp/mmd`; if `/tmp` has been cleared, reinstall it with `npm i @mermaid-js/mermaid-cli`.

## Update policy
Update on every change Role Cartographer approves (once Keeper records it) and for every new bot. Bump the version line, keep the previous version as `*-vN.*` copies, and note what changed.

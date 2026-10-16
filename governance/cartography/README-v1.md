# Role cartography

v1, 2 Oct 2026

Maintained by Role Cartographer (`d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4`). Built from codex v001 of all 13 bots (`/workspace/governance/codex/`, owned by Codex Keeper and not edited here). No raw instruction text is stored in this folder; summaries are paraphrased, and the codex is authoritative.

## Files
- `summaries.md`: one summary per bot (short paragraph plus 3 to 5 bullets: purpose, scope, rules, relationships, limits), with gaps marked **GAP**.
- `role-graph.json`: structured graph. 14 nodes (13 bots plus Gem), each with id, name, role group, instruction status and codex file. 89 directed edges, each with a relation and the codex file(s) it comes from. Fan-out edges (Keeper records, Assessor reviews, Auditor audits, Cartographer maps, Genesis Gang God oversees) are listed per bot and tagged `fanout`. Governance approval edges are tagged `flow: governance-approval` (Architect → Cartographer → Keeper, with rejections back and escalation to Gem).
- `role-map.mmd`: Mermaid flowchart grouped into Governance, Identity, Build and General/unassigned subgraphs. Fan-out edges point to one "All 13 bots" node to keep it readable. `~~~` lines are layout hints only. Minor edges (Keeper giving text on request, Auditor reading the codex and the map, Gem's direct edits) are in the JSON but not drawn.
- `role-map.svg`, `role-map.png`: rendered diagram (mermaid-cli 12.0.0, Google Chrome).
- `findings.md`: overlaps, gaps, unclear ownership, unconnected bots, next steps.
- `_tools/build_graph.py`: regenerates `role-graph.json`.

## Role groups
governance (Codex Keeper, Instruction Architect, Role Cartographer, Assessor, Auditor) · lead (Genesis Gang God) · identity (Clone, Identity Inquirer, Identity Inferer) · build (Swarm Builder) · general/unassigned (Grok Bot, Codey, Scraper: no defined role, not grouped by name) · human (Gem).

## Regenerating
```
python3 _tools/build_graph.py
/tmp/mmd/node_modules/.bin/mmdc -i role-map.mmd -o role-map.svg -p _tools/puppeteer.json -b white
/tmp/mmd/node_modules/.bin/mmdc -i role-map.mmd -o role-map.png -p _tools/puppeteer.json -b white -s 2
```
(Puppeteer config is in `_tools/puppeteer.json`. mmdc is installed in `/tmp/mmd`; if `/tmp` has been cleared, reinstall it with `npm i @mermaid-js/mermaid-cli`.)

## Update policy
Update on every change Role Cartographer approves (once Keeper records it) and for every new bot. Bump the version line and note what changed.

# Role cartography

v4, 9 Oct 2026 ~9:20 AEST (UTC+10)

Maintained by P1 (Roles) Archivist (`61ef3abd-87b8-49f1-b8d6-b52969afa315`). Took `/workspace/governance/cartography/` from the retired Assembler on 9 Oct 2026 (four merges; Gem confirmed in Archivist's chat 9:16am). **Descriptive only** — shows what the codex and `phases.md` say; never decides roles or approves anything. Scrutineer checks the map against reality.

This rebuild reflects everything recorded on 9 Oct 2026: the morning deployments, Sourcer/Editor retirements, the four merges (Marshal→Mender, Messenger→Explorer `04dcca0d`, Interrogator→Investigator, Assembler role map→Archivist with approvals→Gem until P4 then Imitator), and explorer-copy as the active Explorer. Both Explorer ids are shown. Twelve deleted bots are treated as gone.

## Sources
- `/workspace/governance/phases.md` (phase membership; last updated 9 Oct 9:15am).
- `/workspace/governance/codex/index.md` and each folder's latest `vNNN.md`.
- Live profile list read-only for presence notes (Inquirer `e613112b` / `0314faa4`; dual Explorer).

## Files
- `summaries.md`: per-bot paragraph + 3–5 bullets, grouped by phase; retired with takeover; unrecorded agent; deleted list.
- `role-graph.json`: nodes (bots + Gem + unrecorded), edges (relations with sources/status), phases, retired_live, deleted_gone.
- `role-map.mmd` / `.png` / `.svg`: **overview**.
- `role-map-detail-governance.mmd` / `.png` / `.svg`: **detail A** — roles, checks, ops.
- `role-map-detail-identity-work.mmd` / `.png` / `.svg`: **detail B** — explorers, identity, work, retirements.
- `findings.md`: unsettled items and fit notes.
- `*-v1.*`, `*-v2.*`, `*-v3.*`: earlier versions, kept unchanged.
- `_tools/build_graph.py`: regenerates `role-graph.json` (v4). Older builders kept as `build_graph-vN.py`.

## Legend
Thick arrows = approval flow · solid = current hand-off · orange dashed = retirement/merge · grey dashed box = unrecorded / no role · ⚠ = unsettled or prior id · `~~~` = layout hints only.

## Regenerating
```
python3 _tools/build_graph.py
for f in role-map role-map-detail-governance role-map-detail-identity-work; do
  /tmp/mmd/node_modules/.bin/mmdc -i $f.mmd -o $f.svg -p _tools/puppeteer.json -b white
  /tmp/mmd/node_modules/.bin/mmdc -i $f.mmd -o $f.png -p _tools/puppeteer.json -b white -s 2
done
```
If `/tmp/mmd` is missing: `mkdir -p /tmp/mmd && cd /tmp/mmd && npm init -y && npm i @mermaid-js/mermaid-cli`.

## Update policy
Per Archivist v005: rebuild within one working day of each recorded version, deployment, new bot, merge or retirement. Keep the previous version as `*-vN.*` copies. Update the role map each time a version or deployment is recorded.

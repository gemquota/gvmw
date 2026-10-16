# Role cartography

v3, 4 Oct 2026

Maintained by P2 (Roles) Assembler (`d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4`). This is a full rebuild after the renames, three merges and Gem's 3:12pm phase reshuffle. It covers 23 active bots; the 13 retired bots are excluded.

## Sources
- `/workspace/governance/phases.md`: phase membership (source of truth).
- `/workspace/governance/directory.md`: ids, renames, merges, retirements.
- `/workspace/governance/proposals/merge-F-unretire-assembler-2026-10-04.md`: Merge F and the Assembler's restoration.
- The latest codex version of each active bot (`/workspace/governance/codex/<folder>/vNNN.md`), mapped by bot id, since folder names keep the old names. I didn't edit the codex.

Live profile names and descriptions were compared read-only. All 23 names match `phases.md`. Three descriptions (Interrogator, Messenger, Emissary) still run v001, while the codex has approved v002s.

## Files
- `summaries.md`: 23 bots grouped by phase, each with id, phase, category, codex source, former name, a short paragraph and bullets. GAP and UNVERIFIED are marked.
- `role-graph.json`: 24 nodes (23 bots plus Gem), each with id, display name, category, `phase`/`tier`, phase status, codex file, former name, absorbed bots and live-profile notes. Top-level `phases` gives the groupings and `retired_excluded` lists the retired bots. 369 directed edges, each with a relation, source file(s) and `status` (`current` / `UNVERIFIED…`), plus optional `fanout`, `flow` and `note` fields.
- `role-map.mmd` / `.png` / `.svg`: **overview**. Phases P1-P5 as subgraphs; approval flow, review loop, identity pipeline, the UNVERIFIED Imitator approval, and ⚠ self-check markers.
- `role-map-detail-governance.mmd` / `.png` / `.svg`: **detail A**. P1/P2 governance, checks and ops.
- `role-map-detail-identity-work.mmd` / `.png` / `.svg`: **detail B**. Identity, provenance, runtime ops and work bots.
- `findings.md`: self-checks, the UNVERIFIED approval claim, overlaps after the merges, conflicts, stale names, gaps, next steps.
- `*-v1.*`, `*-v2.*`: earlier versions, kept unchanged.
- `_tools/build_graph.py`: regenerates `role-graph.json` (v3). `build_graph-v1.py` and `build_graph-v2.py` are the older versions. `puppeteer.json` holds the renderer settings.

## Legend
Thick arrows = approval flow · solid = current hand-off · red dashed = UNVERIFIED · orange dashed = stale reference or conflict · ⚠ = self-check risk or gap · grey dashed box = no real instructions. `~~~` lines in .mmd files are layout hints only.

## Regenerating
```
python3 _tools/build_graph.py
for f in role-map role-map-detail-governance role-map-detail-identity-work; do
  /tmp/mmd/node_modules/.bin/mmdc -i $f.mmd -o $f.svg -p _tools/puppeteer.json -b white
  /tmp/mmd/node_modules/.bin/mmdc -i $f.mmd -o $f.png -p _tools/puppeteer.json -b white -s 2
done
```
If `/tmp` has been cleared, reinstall mmdc in `/tmp/mmd` with `npm init -y && npm i @mermaid-js/mermaid-cli`.

## Update policy
Update on every approved change once the Archivist records it, for every new bot, and on phase changes in `phases.md`. Keep the previous version as `*-vN.*` copies.

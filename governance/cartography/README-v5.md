# Role cartography

v5, 9 Oct 2026 ~9:27 AEST (UTC+10)

Maintained by P1 (Roles) Archivist. Descriptive only. Scrutineer checks against reality.

**v5:** Inquirer `0314faa4` active (v003 deployed); `e613112b` former holder gone; Inferer v003 → 0314faa4; Explorer `04dcca0d` active; `82a2c15a` former gone. No unrecorded live Inquirer.

## Files
- `summaries.md`, `role-graph.json`, `role-map.mmd/.png/.svg`, detail governance + identity-work, `findings.md`
- `*-v1.*` … `*-v4.*`: earlier versions kept
- `_tools/build_graph.py` (v5)

## Regenerating
```
python3 _tools/build_graph.py
for f in role-map role-map-detail-governance role-map-detail-identity-work; do
  /tmp/mmd/node_modules/.bin/mmdc -i $f.mmd -o $f.svg -p _tools/puppeteer.json -b white
  /tmp/mmd/node_modules/.bin/mmdc -i $f.mmd -o $f.png -p _tools/puppeteer.json -b white -s 2
done
```

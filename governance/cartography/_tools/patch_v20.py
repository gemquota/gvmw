# Role map v20 (22 Oct 2026): r044-r047 LIVE (Imitator v008, Arbiter v007) ~9:35pm; connector-limits v003 Variant A in effect.
import json,sys
from pathlib import Path
D=Path('/workspace/governance/cartography'); NOW=sys.argv[1]; CX='/workspace/governance/codex/'
g=json.loads((D/'role-graph.json').read_text()); K={n['key']:n for n in g['nodes']}
i=K['IMI']; i['codex']=i['live_codex']=CX+'clone/v008.md'
i['note']="LIVE v008 (deployed 22 Oct 21:35:38 AEST on Gem's 9:27pm words, t72u item 2): may veto Arbiter's rulings and change bots' schedules (flagged in the digest), except rulings applying R-015, R-027 and R-028 (R-052); may approve bots creating or retiring bots (archive first, R-047c); the 8:04pm grants are advisory only for big or irreversible decisions until Gem answers on scope (R-051). Earlier: "+i['note']
a=K['ARB']; a['codex']=CX+'arbiter/v007.md'
if a.get('live_codex'): a['live_codex']=CX+'arbiter/v007.md'
a['note']="LIVE v007 (deployed 22 Oct 21:35:45 AEST on Gem's 9:27pm words, t72u item 2): Imitator may veto its rulings, except rulings applying R-015, R-027 and R-028 (R-052). Earlier: "+a['note']
g['edges'].append({'from':i['id'],'from_name':i['name'],'to':a['id'],'to_name':a['name'],'relation':"may veto rulings of (except rulings applying R-015, R-027, R-028; R-052); flagged in the digest",'source':[CX+'clone/v008.md',CX+'arbiter/v007.md'],'status':'current','flow':'handoff'})
OLD=g['version'].split('2026 ')[1].split(' AEST')[0]
g['previous_version']=g['version']; g['version']=f'v20, 22 Oct 2026 {NOW} AEST'; g['stats'].update(edges=len(g['edges']))
g['sources']['note']+=f" 22 Oct {NOW}: Imitator v008 and Arbiter v007 LIVE ~9:35pm (Gem 9:27pm, t72u); connector-limits v003 Variant A in effect."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")
def sub(p,pairs):
    s=(D/p).read_text()
    for x,y in pairs: assert s.count(x)==1,(p,x); s=s.replace(x,y)
    (D/p).write_text(s)
sub('role-map.mmd',[(f'Role map v19, 22 Oct 2026 {OLD} AEST',f'Role map v20, 22 Oct 2026 {NOW} AEST'),('%% v19: ','%% v20: Imitator v008 + Arbiter v007 LIVE ~9:35pm (Imitator may veto Arbiter, not R-015/027/028); connector-limits v003 A in effect. v19: '),('<b>Legend v19</b>','<b>Legend v20</b>'),('green = added in v11–v19','green = added in v11–v20'),('IMI["Imitator v007 · LIVE','IMI["Imitator v008 · LIVE'),('ARB["Arbiter v006"]','ARB["Arbiter v007"]')])
s=(D/'role-map.mmd').read_text().rstrip('\n')+"\n  IMI -->|veto, not R-015/027/028| ARB\n  linkStyle 52 stroke:#2e7d32,stroke-width:2px\n"; (D/'role-map.mmd').write_text(s)
sub('role-map-detail-governance.mmd',[(f'Role map v19 (22 Oct 2026 {OLD}',f'Role map v20 (22 Oct 2026 {NOW}'),('IMI["Imitator v007 · LIVE since 9:30pm 22 Oct"]','IMI["Imitator v008 · LIVE since 9:35pm 22 Oct"]')])
s=(D/'role-map-detail-governance.mmd').read_text().rstrip('\n')+"\n  IMI -->|veto, not R-015/027/028| ARB\n"; (D/'role-map-detail-governance.mmd').write_text(s)
sub('role-map-detail-identity-work.mmd',[(f'Role map v19 (22 Oct 2026 {OLD}',f'Role map v20 (22 Oct 2026 {NOW}'),('IMI["Imitator v007 · LIVE · decides within limits"]','IMI["Imitator v008 · LIVE · decides within limits"]')])
sub('role-map-detail-connectors.mmd',[(f'Role map v19 (22 Oct 2026 {OLD}',f'Role map v20 (22 Oct 2026 {NOW}')])
V=(f"## v20 — 22 Oct 2026 {NOW} AEST (current)\nr044-r047 LIVE (~9:35pm, Gem's 9:27pm words in Archivist's chat, t72u): Imitator v008 may veto Arbiter's rulings except those applying R-015, R-027 and R-028 (R-052), and may approve bots creating or retiring bots (archive first); Arbiter v007 matches. Connector limits v003 Variant A is in effect. New edge Imitator → Arbiter (veto). {len(g['edges'])} edges; v1–v19 kept as `*-vN.*`.\n\n")
for f in ['summaries.md','README.md']:
    s=(D/f).read_text(); k=s.index('## v19 — '); s=s[:k]+V+s[k:].replace(' (current)','',1)
    if f=='summaries.md': s=s.replace(f'(role map v19, 22 Oct 2026 {OLD} AEST)',f'(role map v20, 22 Oct 2026 {NOW} AEST)',1)
    if f=='README.md': s=s.replace(V,V+"- Interactive view rebuilt from v20: `role-map-interactive.html`.\n\n",1)
    (D/f).write_text(s)
f_=(D/'findings.md').read_text()
f_=f_.replace('## v19 findings',f"## v20 findings (22 Oct 2026 {NOW} AEST)\n- **Apify runner gap:** connector-limits v003 (in effect) names Emissary as the Apify runner and Mender for spend checks, and treats Mediator, Scorer, Safekeeper, Inquirer and Extractor as merged (NAMES clause). None of them is retired yet, and live Emissary v007 has no Apify lane, until the redesign (item 5). Edges for Extractor and Mediator stay as drawn; every Apify run still needs Gem's direct words.\n- Edge sources citing connector-limits v002 are not re-pointed in this version.\n\n## v19 findings",1)
(D/'findings.md').write_text(f_); print('ok',len(g['edges']))

# Role map v19 (22 Oct 2026): Imitator v007 LIVE 9:30:43pm (Gem 9:27pm, t72u); Scrutineer verified.
import json,sys
from pathlib import Path
D=Path('/workspace/governance/cartography'); NOW=sys.argv[1]; CX='/workspace/governance/codex/'
g=json.loads((D/'role-graph.json').read_text()); K={n['key']:n for n in g['nodes']}
n=K['IMI']; n['codex']=CX+'clone/v007.md'; n['live_codex']=CX+'clone/v007.md'
n['note']="LIVE v007 (deployed 22 Oct 21:30:43 AEST on Gem's 9:27pm words in Archivist's chat, t72u; Scrutineer verified): shared certainty vocabulary; gaps go to Inferer only, never to Inquirer directly; no grading or alignment verdicts (Scorer and Scrutineer grade). Earlier: "+n['note']
g['edges'].append({'from':n['id'],'from_name':n['name'],'to':K['INF']['id'],'to_name':K['INF']['name'],'relation':'logs gaps about Gem with (Inferer only, never Inquirer directly)','source':[CX+'clone/v007.md',CX+'identity-inferer/v006.md'],'status':'current','flow':'handoff'})
OLD=g['version'].split('2026 ')[1].split(' AEST')[0]
g['previous_version']=g['version']; g['version']=f'v19, 22 Oct 2026 {NOW} AEST'; g['stats'].update(edges=len(g['edges']))
g['sources']['note']+=f" 22 Oct {NOW}: Imitator v007 LIVE 9:30:43pm (Gem 9:27pm, t72u); Scrutineer verified."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")
def sub(p,pairs):
    s=(D/p).read_text()
    for a,b in pairs: assert s.count(a)==1,(p,a); s=s.replace(a,b)
    (D/p).write_text(s)
sub('role-map.mmd',[(f'Role map v18, 22 Oct 2026 {OLD} AEST',f'Role map v19, 22 Oct 2026 {NOW} AEST'),('%% v18: ','%% v19: Imitator v007 LIVE 9:30:43pm; Imitator → Inferer gap edge. v18: '),('<b>Legend v18</b>','<b>Legend v19</b>'),('green = added in v11–v17','green = added in v11–v19'),('IMI["Imitator v006 · LIVE','IMI["Imitator v007 · LIVE')])
s=(D/'role-map.mmd').read_text().rstrip('\n')+"\n  IMI -->|gaps, Inferer only| INF\n  linkStyle 51 stroke:#2e7d32,stroke-width:2px\n"; (D/'role-map.mmd').write_text(s)
sub('role-map-detail-governance.mmd',[(f'Role map v18 (22 Oct 2026 {OLD}',f'Role map v19 (22 Oct 2026 {NOW}'),('IMI["Imitator v006 · LIVE since 11:30pm"]','IMI["Imitator v007 · LIVE since 9:30pm 22 Oct"]')])
sub('role-map-detail-identity-work.mmd',[(f'Role map v18 (22 Oct 2026 {OLD}',f'Role map v19 (22 Oct 2026 {NOW}'),('IMI["Imitator v006 · LIVE · decides within limits"]','IMI["Imitator v007 · LIVE · decides within limits"]')])
s=(D/'role-map-detail-identity-work.mmd').read_text().rstrip('\n')+"\n  IMI -->|gaps, Inferer only| INF\n"; (D/'role-map-detail-identity-work.mmd').write_text(s)
sub('role-map-detail-connectors.mmd',[(f'Role map v18 (22 Oct 2026 {OLD}',f'Role map v19 (22 Oct 2026 {NOW}')])
V=(f"## v19 — 22 Oct 2026 {NOW} AEST (current)\nImitator v007 is LIVE (deployed 9:30:43pm on Gem's 9:27pm words in Archivist's chat, t72u; Scrutineer verified, reviews/2026-10-22-imitator-v007-deploy-check.md): shared certainty vocabulary, gaps to Inferer only, no grading. New edge Imitator → Inferer (gaps about Gem). {len(g['edges'])} edges; v1–v18 kept as `*-vN.*`.\n\n")
for f in ['summaries.md','README.md']:
    s=(D/f).read_text(); i=s.index('## v18 — '); s=s[:i]+V+s[i:].replace(' (current)','',1)
    if f=='summaries.md': s=s.replace(f'(role map v18, 22 Oct 2026 {OLD} AEST)',f'(role map v19, 22 Oct 2026 {NOW} AEST)',1)
    if f=='README.md': s=s.replace(V,V+"- Interactive view rebuilt from v19: `role-map-interactive.html`.\n\n",1)
    (D/f).write_text(s)
f_=(D/'findings.md').read_text()
f_=f_.replace('## v18 findings',f"## v19 findings (22 Oct 2026 {NOW} AEST)\n- Imitator's side of the v17 gap-routing finding is now live (v007), so the Imitator → Inferer edge is drawn. Investigator's side waits for investigator-v007 (redesign, item 5), and Investigator's live v004 doesn't yet carry the shared vocabulary.\n- Open for Architect: imitator-v009 line 7 still calls v006 the latest codex version (Gem approved it by hash, so the proposal is not edited).\n\n## v18 findings",1)
(D/'findings.md').write_text(f_); print('ok',len(g['edges']))

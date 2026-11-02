# Role map v22 (22 Oct 2026): redesign batch deployed 10:18:41-10:21:24pm; 5 merged bots retire pending verification; Mediator renamed P2.
import json,sys
from pathlib import Path
D=Path('/workspace/governance/cartography'); NOW=sys.argv[1]; CX='/workspace/governance/codex/'
g=json.loads((D/'role-graph.json').read_text()); K={n['key']:n for n in g['nodes']}
U={'SFG':('compliance-risk-officer/v009','10:18:41pm','merged Safekeeper; audits Scrutineer.'),'SCR':('auditor/v007','10:18:58pm','merged Scorer; scores and audits; deploy checked by Safeguard (RR-061).'),
 'MEN':('mender/v007','10:19:40pm','merged Mediator; only Arbiter lifts cost pauses.'),'INF':('identity-inferer/v008','10:20:08pm','merged Inquirer.'),
 'INV':('investigator/v007','10:20:26pm','checks Imitator.'),'EMI':('grok-bot/v010','10:21:00pm','merged Extractor; runs Apify.'),'ARC':('codex-keeper/v011','10:21:24pm','restore authority, check 10, approval objects, archives retiring bots.')}
for k,(c,t,w) in U.items():
    n=K[k]; n['codex']=CX+c+'.md'; n['live_codex']=CX+c+'.md'
    n['note']=f"LIVE {c.split('/')[1]} (deployed 22 Oct {t} AEST, redesign R-051, Scrutineer verified): {w} Earlier: "+n['note']
M={'MED':'Mender','SCO':'Scrutineer','SFK':'Safeguard','INQ':'Inferer','EXT':'Emissary'}
for k,t in M.items():
    K[k]['note']=f"MERGING into {t} (redesign R-051): archived 22 Oct; retires only after the survivors' deploys are verified; not deleted. Earlier: "+K[k]['note']
K['MED']['note']="Live name 'P2 (Ops) Mediator' since 10:18pm 22 Oct (Gem t81s468). "+K['MED']['note']
g['previous_version']=g['version']; OLD=g['version'].split('2026 ')[1].split(' AEST')[0]; g['version']=f'v22, 22 Oct 2026 {NOW} AEST'
g['sources']['note']+=f" 22 Oct {NOW}: redesign deployed 10:18:41-10:21:24pm; shared resilience, approval-objects, deterministic-checks v001 recorded."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")
def sub(p,pairs):
    s=(D/p).read_text()
    for x,y in pairs: assert s.count(x)==1,(p,x); s=s.replace(x,y)
    (D/p).write_text(s)
sub('role-map.mmd',[(f'Role map v21, 22 Oct 2026 {OLD} AEST',f'Role map v22, 22 Oct 2026 {NOW} AEST'),('%% v21: ','%% v22: redesign deployed 10:18-10:21pm; 5 merged bots marked merging. v21: '),('<b>Legend v21</b>','<b>Legend v22</b>'),('green = added in v11–v21','green = added in v11–v22'),
 ('ARC["Archivist v008<br/>','ARC["Archivist v011<br/>restore + archives<br/>'),('SCO["Scorer v004"]','SCO["Scorer v004<br/>merging into Scrutineer"]'),('SFG["Safeguard v006<br/>','SFG["Safeguard v009<br/>'),('SFK["Safekeeper v005"]','SFK["Safekeeper v005<br/>merging into Safeguard"]'),
 ('MEN["Mender v005"]','MEN["Mender v007"]'),('SCR["Scrutineer v004"]','SCR["Scrutineer v007"]'),('INF["Inferer v006"]','INF["Inferer v008"]'),('MED["Mediator v006<br/>live name still P4"]','MED["Mediator v006 · P2<br/>merging into Mender"]'),
 ('INQ["Inquirer 0314faa4<br/>ACTIVE v004 · verified"]','INQ["Inquirer 0314faa4 v004<br/>merging into Inferer"]'),('INV["Investigator v004<br/>','INV["Investigator v007<br/>'),('EMI["Emissary v007<br/>','EMI["Emissary v010<br/>'),('EXT["Extractor v006<br/>collection and scraping only"]','EXT["Extractor v006<br/>merging into Emissary"]')])
sub('role-map-detail-governance.mmd',[(f'Role map v21 (22 Oct 2026 {OLD}',f'Role map v22 (22 Oct 2026 {NOW}'),('SCO["Scorer v004"] --> SCR["Scrutineer v004"]','SCO["Scorer v004 · merging"] --> SCR["Scrutineer v007"]'),('SFG["Safeguard v006 ·','SFG["Safeguard v009 ·'),('SFK["Safekeeper v005"]','SFK["Safekeeper v005 · merging"]'),('MED["Mediator v006"]','MED["Mediator v006 · P2 · merging"]')])
sub('role-map-detail-identity-work.mmd',[(f'Role map v21 (22 Oct 2026 {OLD}',f'Role map v22 (22 Oct 2026 {NOW}'),('INQ["Inquirer 0314faa4 ACTIVE v004 · verified"]','INQ["Inquirer 0314faa4 v004 · merging into Inferer"]'),('INF["Inferer v005 ·','INF["Inferer v008 ·'),('EXT["Extractor v005 · LIVE ·','EXT["Extractor v006 · merging into Emissary ·')])
sub('role-map-detail-connectors.mmd',[(f'Role map v21 (22 Oct 2026 {OLD}',f'Role map v22 (22 Oct 2026 {NOW}'),('SFG["Safeguard v006<br/>','SFG["Safeguard v009<br/>')])
V=(f"## v22 — 22 Oct 2026 {NOW} AEST (current)\nRedesign batch deployed 10:18:41–10:21:24pm (Gem t72u item 5; 10:15pm t80s452) and Scrutineer verified it (Scrutineer v007 by Safeguard, RR-061). Labels now read Safeguard v009, Scrutineer v007, Mender v007, Inferer v008, Emissary v010, Investigator v007 and Archivist v011. Mediator, Scorer, Safekeeper, Inquirer and Extractor are marked as merging; they're archived and retire only after verification. Mediator's live name is now P2 (Gem t81s468). New Bot stays retired. {len(g['edges'])} edges; v1–v21 kept as `*-vN.*`.\n\n")
for f in ['summaries.md','README.md']:
    s=(D/f).read_text(); k=s.index('## v21 — '); s=s[:k]+V+s[k:].replace(' (current)','',1)
    if f=='summaries.md': s=s.replace(f'(role map v21, 22 Oct 2026 {OLD} AEST)',f'(role map v22, 22 Oct 2026 {NOW} AEST)',1)
    (D/f).write_text(s)
f_=(D/'findings.md').read_text(); f_=f_.replace('## v21 findings',f"## v22 findings (22 Oct 2026 {NOW} AEST)\n- Edges from the five merging bots stay drawn until they retire; their duties are already in the survivors' live briefs, so for now some edges are duplicated.\n\n## v21 findings",1); (D/'findings.md').write_text(f_); print('ok',len(g['edges']))

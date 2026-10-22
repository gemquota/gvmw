# Role map v17 (22 Oct 2026): redundancy batch rev 2 deployed (6 versions LIVE 7:57pm; Scrutineer verified). Describes the live briefs only.
import json,sys
from pathlib import Path
D=Path('/workspace/governance/cartography'); NOW=sys.argv[1]; CX='/workspace/governance/codex/'
g=json.loads((D/'role-graph.json').read_text()); K={n['key']:n for n in g['nodes']}; ID={n['id']:n['key'] for n in g['nodes']}
NEW={'INF':('identity-inferer/v006','19:57:01','LIVE v006 (deployed 22 Oct 19:57:01): one certainty vocabulary shared word for word with Investigator and Imitator (their matching drafts, investigator-v005 and imitator-v007, are not deployed yet); Inferer says it is the only route for gaps about Gem.'),
 'ARB':('arbiter/v006','19:57:05','LIVE v006 (deployed 22 Oct 19:57:05): stall clause dropped (Mender owns stalls, R-006). Approval route flagged by Scrutineer (Imitator + Gem\'s "deploy all six"; Arbiter to rule).'),
 'ARX':('instruction-architect/v005','19:57:12','LIVE v005 (deployed 22 Oct 19:57:12): stall line now cites R-006 only; drafts a live profile rename when Gem asks, and Archivist records and applies it.'),
 'EMI':('grok-bot/v007','19:57:23','LIVE v007 (deployed 22 Oct 19:57:23): owns research write-ups; assigns no work; hands specialist work back to Explorer (R-044). Approval route flagged by Scrutineer.'),
 'EXT':('scraper/v006','19:57:37','LIVE v006 (deployed 22 Oct 19:57:37): collection and scraping only; jobs from Gem or Explorer; code changes back to Explorer for Engineer (R-044). Approval route flagged by Scrutineer.'),
 'EXP':('explorer-copy/v006','19:57:52','LIVE v006 (deployed 22 Oct 19:57:52): Explorer assigns new work; Mender keeps operational routing (run order, recovery, rerouting stalled or failed work, stall detection; R-006, R-044).')}
for k,(c,t,note) in NEW.items():
    n=K[k]; n['codex']=CX+c+'.md'
    if n.get('live_codex'): n['live_codex']=CX+c+'.md'
    n['note']=note+' Earlier: '+n['note']
def E(a,b): return [e for e in g['edges'] if ID.get(e['from'])==a and ID.get(e['to'])==b and e['status']=='current']
for b,rel in [('EMI','assigns new work (general work and research write-ups) to (R-044)'),('ENG','assigns code in a repo and swarm work to (R-044)'),('EXT','assigns web data collection and scraping (only) to (R-044)')]:
    e=E('EXP',b); assert len(e)==1,b; e[0]['relation']=rel; e[0]['source']=[CX+'explorer-copy/v006.md']
def add(a,b,rel,src): g['edges'].append({'from':K[a]['id'],'from_name':K[a]['name'],'to':K[b]['id'],'to_name':K[b]['name'],'relation':rel,'source':[CX+src],'status':'current','flow':'handoff'})
add('EMI','EXP','hands specialist work back to (R-044)','grok-bot/v007.md')
add('EXT','EXP','hands code changes and new jobs back to (R-044)','scraper/v006.md')
add('ARX','ARC','drafts live profile renames (when Gem asks) for Archivist to record and apply','instruction-architect/v005.md')
g['previous_version']=g['version']; g['version']=f'v17, 22 Oct 2026 {NOW} AEST'
g['stats'].update(nodes=len(g['nodes']),edges=len(g['edges']))
g['sources']['note']+=f" 22 Oct {NOW}: redundancy batch rev 2 deployed 7:57pm (Inferer v006, Arbiter v006, Architect v005, Emissary v007, Extractor v006, Explorer v006); Scrutineer verified."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")
def sub(p,pairs):
    s=(D/p).read_text()
    for a,b in pairs: assert s.count(a)==1,(p,a); s=s.replace(a,b)
    (D/p).write_text(s)
sub('role-map.mmd',[('Role map v16, 22 Oct 2026 6:45:04pm AEST',f'Role map v17, 22 Oct 2026 {NOW} AEST'),
 ('%% v16: ','%% v17: redundancy batch rev 2 LIVE 7:57pm (Explorer assigns new work, R-044; Emissary/Extractor hand back; Architect drafts renames for Archivist). v16: '),
 ('<b>Legend v16</b>','<b>Legend v17</b>'),('green = added in v11–v14','green = added in v11–v17'),
 ('ARX["Architect v004"]','ARX["Architect v005"]'),('EXP["Explorer v005 04dcca0d<br/>ACTIVE · keeps phases.md"]','EXP["Explorer v006 04dcca0d<br/>ACTIVE · keeps phases.md<br/>assigns new work (R-044)"]'),
 ('ARB["Arbiter v005"]','ARB["Arbiter v006"]'),('INF["Inferer v005"]','INF["Inferer v006"]'),('EMI["Emissary v006<br/>only postiz poster"]','EMI["Emissary v007<br/>only postiz poster · research write-ups"]'),
 ('EXT["Extractor v005"]','EXT["Extractor v006<br/>collection and scraping only"]'),
 ('EXP -->|routes| EMI','EXP -->|assigns work| EMI'),('EXP -->|routes| ENG','EXP -->|assigns work| ENG'),('EXP -->|routes| EXT','EXP -->|assigns work| EXT')])
s=(D/'role-map.mmd').read_text().rstrip('\n')+"\n  EMI -->|hands back| EXP\n  EXT -->|hands back| EXP\n  ARX -->|drafts renames| ARC\n  linkStyle 48,49,50 stroke:#2e7d32,stroke-width:2px\n"
(D/'role-map.mmd').write_text(s)
sub('role-map-detail-governance.mmd',[('Role map v16 (22 Oct 2026 6:45:04pm; unchanged from v14 detail;',f'Role map v17 (22 Oct 2026 {NOW};'),('ARX["Architect v004"]','ARX["Architect v005"]')])
for f in ['role-map-detail-identity-work.mmd','role-map-detail-connectors.mmd']:
    sub(f,[('Role map v16 (22 Oct 2026 6:45:04pm; unchanged from v14 detail',f'Role map v17 (22 Oct 2026 {NOW}; unchanged from v14 detail')])
V=(f"## v17 — 22 Oct 2026 {NOW} AEST (current)\n"
"Redundancy batch 2026-10-22 rev 2 is LIVE (deployed 7:57:01–7:57:52pm; Scrutineer verified, reviews/2026-10-22-redundancy-deploy-check.md): Inferer v006, Arbiter v006, Architect v005, Emissary v007, Extractor v006 and Explorer v006. "
"Explorer assigns new work (R-044) and Mender keeps operational routing. New edges: Emissary → Explorer and Extractor → Explorer (hand back), and Architect → Archivist (drafts renames when Gem asks). Arbiter's stall clause is gone. "
f"No other change; v1–v16 kept as `*-vN.*`. 17 active, all live + 1 retired with no codex folder + 9 former/retired nodes, {len(g['edges'])} edges.\n\n")
for f in ['summaries.md','README.md']:
    s=(D/f).read_text(); a='## v16 — '; i=s.index(a); j=s.index('(current)',i)
    s=s[:i]+V+s[i:j]+s[j+len('(current)'):].lstrip(' ') if False else s[:i]+V+s[i:].replace(' (current)','',1)
    if f=='summaries.md': s=s.replace('(role map v16, 22 Oct 2026 6:45:04pm AEST)',f'(role map v17, 22 Oct 2026 {NOW} AEST)',1)
    if f=='README.md': s=s.replace(V,V+"- Interactive view rebuilt from v17: `role-map-interactive.html`.\n\n",1)
    (D/f).write_text(s)
f_=(D/'findings.md').read_text()
F=(f"## v17 findings (22 Oct 2026 {NOW} AEST)\n"
"- Inferer v006 says Investigator and Imitator send their gaps about Gem only to Inferer and use the shared certainty vocabulary, but their own briefs (investigator-v005, imitator-v007) aren't deployed yet. Until they are, the live briefs disagree, so no Investigator/Imitator → Inferer edge is drawn.\n"
"- Scrutineer flagged the approval route for Arbiter v006, Emissary v007 and Extractor v006 (an Imitator approval plus Gem's \"deploy all six\") as departing from R-044. Arbiter is to rule, or Gem can confirm in one line. The text and deployment passed.\n\n")
(D/'findings.md').write_text(f_.replace('## v16 findings',F+'## v16 findings',1)); print('ok',len(g['edges']))

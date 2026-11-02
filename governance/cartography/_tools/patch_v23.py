# Role map v23 (22 Oct 2026): the five merged bots RETIRED 10:40pm (Gem t88s497) and renamed 'RETIRED …' (t90u); their duplicate edges removed; one grey 'merged into' edge each; nodes greyed.
import json,sys,re
from pathlib import Path
D=Path('/workspace/governance/cartography'); NOW=sys.argv[1]; CX='/workspace/governance/codex/'
g=json.loads((D/'role-graph.json').read_text()); K={n['key']:n for n in g['nodes']}; ID={n['id']:n['key'] for n in g['nodes']}
R={'MED':('MEN','connector-steward/v007','Mediator'),'SCO':('SCR','assessor/v005','Scorer'),'SFK':('SFG','secrets-credentials-custodian/v006','Safekeeper'),'INQ':('INF','identity-inquirer/v005','Inquirer'),'EXT':('EMI','scraper/v007','Extractor')}
removed=[]
for e in g['edges']:
    a,b=ID[e['from']],ID[e['to']]
    if e['status']=='current' and (a in R or b in R):
        e['status']='retired_merge_22oct'; e['note']="duty merged into the survivor's live brief (redesign R-051); retired 22 Oct 10:40pm (Gem t88s497)"; removed.append((a,b))
for k,(s,c,w) in R.items():
    n=K[k]; n['map_status']='retired_merged'; n['codex']=CX+c+'.md'; n['live_codex']=CX+c+'.md'; n['name']='RETIRED '+w
    n['note']=f"RETIRED 22 Oct 2026 10:40pm (Gem t88s497), merged into {K[s]['name']}; live name 'RETIRED …' since about 10:43pm (Gem t90u); retirement notice {c.split('/')[1]} live; folder kept, nothing deleted. Earlier: "+n['note']
    g['edges'].append({'from':n['id'],'to':K[s]['id'],'relation':'merged into (22 Oct 2026, R-051)','status':'retired_merge_22oct','source':[CX+c+'.md']})
g['previous_version']=g['version']; OLD=g['version'].split('2026 ')[1].split(' AEST')[0]; g['version']=f'v23, 22 Oct 2026 {NOW} AEST'
g['sources']['note']+=f" 22 Oct {NOW}: five merged bots retired (10:40pm) and renamed RETIRED (10:43pm); {len(removed)} duplicate edges retired."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")
ARROW=re.compile(r'(-->|-\.->|==>)')
def rewrite(p,labels,extra_pairs):
    s=(D/p).read_text()
    for x,y in extra_pairs: assert s.count(x)==1,(p,x); s=s.replace(x,y)
    lines=s.split('\n'); out=[]; idx=0; remap={}; dropped=0
    for l in lines:
        st=l.strip()
        if ARROW.search(st) and not st.startswith(('%%','linkStyle','classDef','class ')):
            m=re.match(r'^(\w+)(?:\[.*?\])?\s*(?:-->|-\.->|==>)\s*(?:\|[^|]*\|\s*)?(\w+)',st)
            a,b=(m.group(1),m.group(2)) if m else (None,None)
            if (a in R or b in R) and not (a=='INQ0'):
                if '[' in st and (a in R): out.append('  '+st.split(' ')[0])  # keep node definition
                dropped+=1; idx+=1; continue
            remap[idx]=idx-dropped; idx+=1
        out.append(l)
    s='\n'.join(out)
    def ls(m):
        ns=[str(remap[int(x)]) for x in m.group(1).split(',') if int(x) in remap]
        return ('  linkStyle '+','.join(ns)+' '+m.group(2)) if ns else '  %% (linkStyle removed: its edges were retired)'
    s=re.sub(r'^\s*linkStyle ([\d,]+) (.*)$',ls,s,flags=re.M)
    n_new=sum(1 for l in s.split('\n') if ARROW.search(l.strip()) and not l.strip().startswith(('%%','linkStyle','classDef','class ')))
    add=[f'  {k} -.->|merged into| {v[0]}' for k,v in R.items() if re.search(rf'^\s*{k}\b',s,re.M)]
    s=s.rstrip('\n')+'\n'+'\n'.join(add)+'\n'
    if add: s+=f"  linkStyle {','.join(str(n_new+i) for i in range(len(add)))} stroke:#9e9e9e,stroke-dasharray:3 3\n"
    s+="  classDef retiredMerged fill:#eeeeee,stroke:#9e9e9e,color:#757575\n"
    present=[k for k in R if re.search(rf'^\s*{k}\b',s,re.M)]
    if present: s+=f"  class {','.join(present)} retiredMerged\n"
    (D/p).write_text(s); return dropped
L={'MED':'RETIRED P2 (Ops) Mediator','SCO':'RETIRED P1 (Checks) Scorer','SFK':'RETIRED P1 (Checks) Safekeeper','INQ':'RETIRED P2 (ID) Inquirer','EXT':'RETIRED P5 (Work) Extractor'}
d=rewrite('role-map.mmd',L,[(f'Role map v22, 22 Oct 2026 {OLD} AEST',f'Role map v23, 22 Oct 2026 {NOW} AEST'),('%% v22: ','%% v23: five merged bots RETIRED 10:40pm and renamed; duplicate edges removed; grey = retired, merged. v22: '),('<b>Legend v22</b>','<b>Legend v23</b>'),('green = added in v11–v22','green = added in v11–v23<br/>grey = retired 22 Oct, merged into'),
 ('SCO["Scorer v004<br/>merging into Scrutineer"]','SCO["RETIRED P1 (Checks) Scorer<br/>v005 notice · merged into Scrutineer"]'),('SFK["Safekeeper v005<br/>merging into Safeguard"]','SFK["RETIRED P1 (Checks) Safekeeper<br/>v006 notice · merged into Safeguard"]'),
 ('MED["Mediator v006 · P2<br/>merging into Mender"]','MED["RETIRED P2 (Ops) Mediator<br/>v007 notice · merged into Mender"]'),('INQ["Inquirer 0314faa4 v004<br/>merging into Inferer"]','INQ["RETIRED P2 (ID) Inquirer<br/>v005 notice · merged into Inferer"]'),('EXT["Extractor v006<br/>merging into Emissary"]','EXT["RETIRED P5 (Work) Extractor<br/>v007 notice · merged into Emissary"]')])
d2=rewrite('role-map-detail-governance.mmd',L,[(f'Role map v22 (22 Oct 2026 {OLD}',f'Role map v23 (22 Oct 2026 {NOW}'),('SCO["Scorer v004 · merging"] --> SCR["Scrutineer v007"]','SCR["Scrutineer v007"]\n  SCO["RETIRED P1 (Checks) Scorer"]'),('SFK["Safekeeper v005 · merging"] --> SFG','SFK["RETIRED P1 (Checks) Safekeeper"]'),('MED["Mediator v006 · P2 · merging"] --> GEM','MED["RETIRED P2 (Ops) Mediator"]')])
d3=rewrite('role-map-detail-identity-work.mmd',L,[(f'Role map v22 (22 Oct 2026 {OLD}',f'Role map v23 (22 Oct 2026 {NOW}'),('-.->|v003 re-key| INQ["Inquirer 0314faa4 v004 · merging into Inferer"]','-.->|v003 re-key| INQ["RETIRED P2 (ID) Inquirer"]'),('INQ --> INF["Inferer v008 ·','INF["Inferer v008 ·'),('EXP --> EXT["Extractor v006 · merging into Emissary · BIE data stays on box"]','EXT["RETIRED P5 (Work) Extractor"]'),('MED["Mediator"] -->|cost alerts| EXP','MED["RETIRED P2 (Ops) Mediator"]')])
d4=rewrite('role-map-detail-connectors.mmd',L,[(f'Role map v22 (22 Oct 2026 {OLD}',f'Role map v23 (22 Oct 2026 {NOW}'),('SFK["Safekeeper<br/>key locations, rule 19"]','SFK["RETIRED P1 (Checks) Safekeeper"]'),('MED["Mediator<br/>installs, connectors.md, spend"]','MED["RETIRED P2 (Ops) Mediator"]'),('EXT["Extractor"]','EXT["RETIRED P5 (Work) Extractor"]')])
V=(f"## v23 — 22 Oct 2026 {NOW} AEST (current)\nMediator, Scorer, Safekeeper, Inquirer and Extractor RETIRED 10:40pm (Gem t88s497) and renamed 'RETIRED …' at about 10:43pm (t90u), shown grey, each with one 'merged into' edge to Mender, Scrutineer, Safeguard, Inferer and Emissary. {len(removed)} duplicate edges retired in the graph (removed from the drawings: overview {d}, governance {d2}, identity-work {d3}, connectors {d4}). Four of the five profile writes are unverified (not Archivist; R-007). v1–v22 kept as `*-vN.*`.\n\n")
for f in ['summaries.md','README.md']:
    s=(D/f).read_text(); k=s.index('## v22 — '); s=s[:k]+V+s[k:].replace(' (current)','',1)
    if f=='summaries.md': s=s.replace(f'(role map v22, 22 Oct 2026 {OLD} AEST)',f'(role map v23, 22 Oct 2026 {NOW} AEST)',1)
    (D/f).write_text(s)
f_=(D/'findings.md').read_text(); f_=f_.replace('## v22 findings',f"## v23 findings (22 Oct 2026 {NOW} AEST)\n- Mediator, Scorer, Safekeeper and Inquirer's retirement writes weren't made by Archivist: unverified deployments (R-007), though the text equals the recorded versions.\n- The retirement version numbers reuse numbers the redesign README listed as unused (for example, scraper v007 = 'extractor-v007 (GitHub 5d draft)', cited in Emissary v010).\n\n## v22 findings",1); (D/'findings.md').write_text(f_)
print('ok removed',len(removed),d,d2,d3,d4,'edges',len(g['edges']))

# Role map v25 (22 Oct 2026): phase-cleanup revision 3 LIVE 11:05:00-11:09:36pm (Gem t96u); shared github v002, connector-limits v005, message verification v006; handoff-phase1 retired; collaboration-map historical.
import json,sys,re
from pathlib import Path
D=Path('/workspace/governance/cartography'); NOW=sys.argv[1]; CX='/workspace/governance/codex/'
g=json.loads((D/'role-graph.json').read_text()); K={n['key']:n for n in g['nodes']}
V={'SFG':('compliance-risk-officer','v011','11:05:00pm'),'SCR':('auditor','v009','11:05:19pm'),'MEN':('mender','v009','11:05:49pm'),'INF':('identity-inferer','v010','11:06:20pm'),'EMI':('grok-bot','v012','11:06:56pm'),'INV':('investigator','v009','11:07:11pm'),'ARC':('codex-keeper','v013','11:07:39pm'),'ARB':('arbiter','v010','11:07:48pm'),'ARX':('instruction-architect','v008','11:07:54pm'),'EXP':('explorer-copy','v009','11:08:16pm'),'ENG':('codey','v009','11:08:39pm'),'IMI':('clone','v011','11:09:36pm')}
for k,(f,v,t) in V.items():
    n=K[k]; n['codex']=f'{CX}{f}/{v}.md'; n['live_codex']=n['codex']
    n['note']=f"LIVE {v} (deployed 22 Oct {t} AEST, phase-cleanup revision 3, Gem t96u; Scrutineer PASS): phase and phases.md wording removed (R-055). Earlier: "+n['note']
for s in g['shared_rules']:
    s['version']={'github':'v002','connector-limits':'v005','message-verification-rule':'v006'}.get(s['entry'],s['version']); s['path']=f"{CX}_shared/{s['entry']}/{s['version']}.md"
    if s['entry']=='collaboration-map': s['status']='historical (Gem t96u)'
g['retired_shared']=[{'entry':'handoff-phase1','version':'v001','path':'/workspace/governance/_archive/cleanup-2026-10-22/codex/_shared/handoff-phase1/v001.md','status':'retired 22 Oct (Gem t96u); archived, nothing deleted'}]
g['previous_version']=g['version']; OLD=g['version'].split('2026 ')[1].split(' AEST')[0]; g['version']=f'v25, 22 Oct 2026 {NOW} AEST'
g['sources']['note']+=f" 22 Oct {NOW}: phase-cleanup revision 3 LIVE; handoff-phase1 retired; collaboration-map historical."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")
def vers(s):
    for k,(f,v,t) in V.items(): s=re.sub(rf'({k}\["[A-Za-z]+ )v0\d\d',rf'\g<1>{v}',s)
    return s.replace('owns connector limits v004','owns connector limits v005').replace('owns connector limits v002','owns connector limits v005')
s=vers((D/'role-map.mmd').read_text())
for a,b in [(f'Role map v24, 22 Oct 2026 {OLD} AEST',f'Role map v25, 22 Oct 2026 {NOW} AEST'),('%% v24: ','%% v25: phase-cleanup revision 3 LIVE; shared rules box updated. v24: '),('<b>Legend v24</b>','<b>Legend v25</b>'),('green = added in v11–v24','green = added in v11–v25'),
 ('resilience v002 · connector-limits v004<br/>github v001 · message verification v005"]','resilience v002 · connector-limits v005<br/>github v002 · message verification v006<br/>collaboration-map v001 (historical)<br/>handoff-phase1 retired (archived)"]')]:
    assert s.count(a)==1,a; s=s.replace(a,b)
(D/'role-map.mmd').write_text(s)
for p in ['role-map-detail-governance.mmd','role-map-detail-identity-work.mmd','role-map-detail-connectors.mmd']:
    t=vers((D/p).read_text()); a=f'Role map v24 (22 Oct 2026 {OLD}'; assert t.count(a)==1,(p,a); (D/p).write_text(t.replace(a,f'Role map v25 (22 Oct 2026 {NOW}'))
Vt=(f"## v25 — 22 Oct 2026 {NOW} AEST (current)\nPhase-cleanup batch revision 3 LIVE 11:05:00–11:09:36pm (Gem t96u; Scrutineer PASS; Safeguard RR-064 on Scrutineer v009): Safeguard v011, Scrutineer v009, Mender v009, Inferer v010, Emissary v012, Investigator v009, Archivist v013, Arbiter v010, Architect v008, Explorer v009, Engineer v009 and Imitator v011. The shared-rules box now shows github v002, connector-limits v005 and message verification v006; collaboration-map is historical and handoff-phase1 is retired (archived, nothing deleted). v1–v24 kept as `*-vN.*`.\n\n")
for f in ['summaries.md','README.md']:
    x=(D/f).read_text(); k=x.index('## v24 — '); x=x[:k]+Vt+x[k:].replace(' (current)','',1)
    if f=='summaries.md': x=x.replace(f'(role map v24, 22 Oct 2026 {OLD} AEST)',f'(role map v25, 22 Oct 2026 {NOW} AEST)',1)
    (D/f).write_text(x)
print('ok')

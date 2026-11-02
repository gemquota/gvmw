# Role map v24 (22 Oct 2026): clarity batch revision 3 LIVE 10:49:47-10:53:12pm; clarity shared rules shown; phase grouping removed (phases.md retired; R-055).
import json,sys,re
from pathlib import Path
D=Path('/workspace/governance/cartography'); NOW=sys.argv[1]; CX='/workspace/governance/codex/'
g=json.loads((D/'role-graph.json').read_text()); K={n['key']:n for n in g['nodes']}
V={'SFG':('compliance-risk-officer','v010','10:49:47pm'),'SCR':('auditor','v008','10:50:02pm'),'MEN':('mender','v008','10:50:36pm'),'INF':('identity-inferer','v009','10:51:03pm'),'EMI':('grok-bot','v011','10:51:40pm'),'INV':('investigator','v008','10:51:51pm'),'ARC':('codex-keeper','v012','10:52:16pm'),'ARB':('arbiter','v009','10:52:23pm'),'ARX':('instruction-architect','v007','10:52:29pm'),'EXP':('explorer-copy','v008','10:52:53pm'),'IMI':('clone','v010','10:53:12pm')}
for k,(f,v,t) in V.items():
    n=K[k]; n['codex']=f'{CX}{f}/{v}.md'; n['live_codex']=n['codex']
    n['note']=f"LIVE {v} (deployed 22 Oct {t} AEST, clarity batch revision 3, Gem t89u): repeated text now points to the shared rules"+(" ; R-054: may approve retiring a bot after a verified archive, and one of the five named projects going public after Safekeeper's scan" if k=='IMI' else '')+". Earlier: "+n['note']
for n in g['nodes']:
    for x in ('phase','phase_status'): n.pop(x,None)
g['shared_rules']=[{'entry':e,'version':v,'path':f'{CX}_shared/{e}/{v}.md'} for e,v in [('free-only','v001'),('retired-names','v001'),('github-read-only','v001'),('precedence','v001'),('deterministic-checks','v002'),('approval-objects','v002'),('resilience','v002'),('connector-limits','v004'),('github','v001'),('message-verification-rule','v005'),('collaboration-map','v001'),('confirm-deployment','v001')]]
g['phase_note']=f"Phase grouping removed {NOW} 22 Oct 2026: Gem said phases.md is redundant (10:47pm, Explorer's chat, relayed by Explorer); it's archived at _archive/phases-retired-2026-10-22/. R-055: directory.md is the only record of which bots are live or retired. 'P#' stays only in live names."
g['previous_version']=g['version']; OLD=g['version'].split('2026 ')[1].split(' AEST')[0]; g['version']=f'v24, 22 Oct 2026 {NOW} AEST'
g['sources']['note']+=f" 22 Oct {NOW}: clarity revision 3 LIVE; clarity shared rules; phase grouping removed (R-055)."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")
def vers(s):
    for k,(f,v,t) in V.items(): s=re.sub(rf'({k}\["[A-Za-z]+ )v0\d\d',rf'\g<1>{v}',s)
    return s.replace('owns connector limits v002','owns connector limits v004').replace('ACTIVE · keeps phases.md','ACTIVE · phases.md retired (R-055)')
s=vers((D/'role-map.mmd').read_text())
for a,b in [(f'Role map v23, 22 Oct 2026 {OLD} AEST',f'Role map v24, 22 Oct 2026 {NOW} AEST'),('%% v23: ','%% v24: clarity revision 3 LIVE; shared rules box; phase grouping removed (phases.md retired, R-055). v23: '),('<b>Legend v23</b>','<b>Legend v24</b>'),('green = added in v11–v23','green = added in v11–v24')]:
    assert s.count(a)==1,a; s=s.replace(a,b)
L=s.split('\n'); out=[]; i=0; ret=[]; inP=False
while i<len(L):
    l=L[i]; m=re.match(r'\s*subgraph (P[1-5])\[',l)
    if m:
        if m.group(1)=='P1': out.append('  subgraph LIVE["LIVE · directory.md is the only live/retired record (R-055)"]')
        inP=True; i+=1; continue
    if inP and l.strip()=='end':
        nxt=next((x for x in L[i+1:] if x.strip()),'')
        if re.match(r'\s*subgraph P[2-5]\[',nxt): i+=1; continue
        inP=False; out.append(l); out.append('  subgraph RETMERGE["RETIRED 22 Oct 10:40pm · merged · agent folders gone by 10:53pm"]'); out+=ret; out.append('  end'); i+=1; continue
    if inP and re.match(r'\s*(MED|SCO|SFK|INQ|EXT)\[',l): ret.append(l); i+=1; continue
    out.append(l); i+=1
s='\n'.join(out)
s=s.replace('  LEG["','  SHR["<b>Shared rules in effect</b><br/>free-only v001 · retired-names v001<br/>github-read-only v001 · precedence v001<br/>deterministic-checks v002 · approval-objects v002<br/>resilience v002 · connector-limits v004<br/>github v001 · message verification v005"]\n  LEG["',1)
(D/'role-map.mmd').write_text(s)
for p in ['role-map-detail-governance.mmd','role-map-detail-identity-work.mmd','role-map-detail-connectors.mmd']:
    t=vers((D/p).read_text()); a=f'Role map v23 (22 Oct 2026 {OLD}'; assert t.count(a)==1,(p,a); (D/p).write_text(t.replace(a,f'Role map v24 (22 Oct 2026 {NOW}'))
Vt=(f"## v24 — 22 Oct 2026 {NOW} AEST (current)\nClarity batch revision 3 LIVE 10:49:47–10:53:12pm (Gem t89u): Safeguard v010, Scrutineer v008, Mender v008, Inferer v009, Emissary v011, Investigator v008, Archivist v012, Arbiter v009, Architect v007, Explorer v008 and Imitator v010. A 'Shared rules in effect' box lists the clarity shared rules. Phase grouping is removed: phases.md was retired (Gem, 10:47pm, relayed by Explorer), and Arbiter's R-055 makes directory.md the only record of which bots are live or retired. The overview has one LIVE group plus a RETIRED 22 Oct group (the five merged bots' agent folders were gone by 10:53pm, not deleted by Archivist). v1–v23 kept as `*-vN.*`.\n\n")
for f in ['summaries.md','README.md']:
    x=(D/f).read_text(); k=x.index('## v23 — '); x=x[:k]+Vt+x[k:].replace(' (current)','',1)
    if f=='summaries.md': x=x.replace(f'(role map v23, 22 Oct 2026 {OLD} AEST)',f'(role map v24, 22 Oct 2026 {NOW} AEST)',1)
    (D/f).write_text(x)
f_=(D/'findings.md').read_text(); f_=f_.replace('## v23 findings',f"## v24 findings (22 Oct 2026 {NOW} AEST)\n- The five merged bots' agent folders were gone by 10:53pm 22 Oct. Archivist didn't delete them and no deletion approval is recorded.\n- The 10:54pm cleanup moved codex/_shared/handoff-phase1 and the source proposals for several shared versions to _archive/cleanup-2026-10-22/, so verify.py crashes and verify_shared.py reports 5 MISSING sources.\n\n## v23 findings",1); (D/'findings.md').write_text(f_); print('ok')

# Role map v12 (16 Oct 2026 ~11:50am AEST): Gem's 11:41am approval; Archivist v008 (11:44:11) and Explorer v005 (11:44:26) live; shared message verification v004.
import json,re
from pathlib import Path
D=Path('/workspace/governance/cartography'); CX='/workspace/governance/codex/'
NEW={'ARC':('codex-keeper/v008','11:44:11',"may deploy a version Imitator approved within its authority, after a 1:1 check with Imitator and Safeguard's dry-run report; never its own brief, Imitator or its checkers, role-widening, spending or irreversible changes; those need Gem's own ask"),
     'EXP':('explorer-copy/v005','11:44:26',"deployment sentence matches Archivist v008; Explorer still never writes any profile (R-014)")}
g=json.loads((D/'role-graph.json').read_text())
old2new={}
for n in g['nodes']:
    k=n.get('key')
    if k in NEW:
        f,t,w=NEW[k]; old=n['codex'].split('/codex/')[1]; old2new[old]=f+'.md'
        n['codex']=n['live_codex']=CX+f+'.md'
        n['note']=n['note'].rstrip()+f" v{f[-3:]} (Gem 11:41am, 16 Oct; live since {t}): {w}."
for e in g['edges']:
    e['source']=[CX+old2new[s.split('/codex/')[-1]] if s.split('/codex/')[-1] in old2new else s for s in e['source']]
    if e['from_name']=='Imitator' and e['to_name']=='Archivist' and e['relation'].startswith('approves/decides'):
        e['relation']=("approves/decides for Gem (live); Archivist records after a 1:1 authenticity check and, from v008, may deploy without waiting for Gem once Safeguard's dry run is in; "
                       "never for Archivist's own brief, Imitator or its checkers, or role-widening changes")
        e['source']=[CX+'clone/v006.md',CX+'codex-keeper/v008.md',CX+'_shared/message-verification-rule/v004.md']
ids={n['key']:n['id'] for n in g['nodes']}; nm={n['key']:n['name'] for n in g['nodes']}
g['edges'].append({'from':ids['ARC'],'from_name':nm['ARC'],'to':ids['SFG'],'to_name':nm['SFG'],'relation':"sends Imitator-approved deploy plans for a dry run (case (b); Archivist waits for the report, asks Gem if there's a concern)",
                   'source':[CX+'codex-keeper/v008.md',CX+'_shared/message-verification-rule/v004.md'],'status':'current'})
g['previous_version']=g['version']; g['version']='v12, 16 Oct 2026 ~11:50am AEST'; g['stats']['edges']=len(g['edges'])
g['sources']['note']=g['sources']['note'].replace("Archivist owns directory.md (v007).","Archivist owns directory.md (v007). Gem's 11:41am approval: Archivist v008 and Explorer v005 live 11:44; Archivist may deploy Imitator-approved versions within limits (1:1 check + Safeguard dry run).")
g['rules']['message_verification']="Shared rule _shared/message-verification-rule/v004 (Gem 11:41am, 16 Oct): deploying a profile edit needs Gem's words to the deploying bot itself (R-010), except Archivist may deploy a version Imitator approved within its authority after a 1:1 check with Imitator and Safeguard's dry-run report; never Imitator, its checkers or role-widening changes."
g['rules']['deployment']="Archivist v008 (live 11:44:11, 16 Oct): case (a) Gem's own ask in Archivist's chat or call; case (b) a version recorded on Imitator's approval, after a 1:1 check with Imitator and Safeguard's dry-run report. Case (b) excludes Archivist's own brief, Imitator and its five checkers, role-widening (R-028), spending and irreversible steps. Words recorded before deploying (R-029). R-010 has no update in rulings.md yet."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n"); print('edges',len(g['edges']))

def sub(path,pairs,tail=''):
    s=(D/path).read_text()
    for a,b in pairs: assert s.count(a)==1,(path,a); s=s.replace(a,b)
    (D/path).write_text(s.rstrip('\n')+'\n'+tail)
sub('role-map.mmd',[('Role map v11, 16 Oct 2026 ~11:20am AEST','Role map v12, 16 Oct 2026 ~11:50am AEST'),
 ('%% v11: ',"%% v12: Gem 11:41am: Archivist v008 + Explorer v005 live 11:44; Archivist may deploy Imitator-approved versions within limits. v11: "),
 ('<b>Legend v11</b>','<b>Legend v12</b>'),('green = added in v11<br/>','green = added in v11/v12<br/>'),
 ('ARC["Archivist v007<br/>codex + role map + directory.md"]','ARC["Archivist v008<br/>codex + role map + directory.md<br/>deploys Imitator-approved, within limits"]'),
 ('EXP["Explorer v004 04dcca0d<br/>','EXP["Explorer v005 04dcca0d<br/>'),
 ('IMI ==>|approves within limits, 6 deployed 9:14am 16 Oct| ARC','IMI ==>|approves within limits · Archivist may deploy after 1:1 check + dry run| ARC')],
 "  ARC -->|Imitator-approved deploy: dry run first| SFG\n  linkStyle 44 stroke:#2e7d32,stroke-width:2px\n")
sub('role-map-detail-governance.mmd',[('Role map v11 (16 Oct 2026 ~11:20am)','Role map v12 (16 Oct 2026 ~11:50am)'),('ARC["Archivist v007 · owns directory.md"]','ARC["Archivist v008 · owns directory.md"]'),
 ('IMI["Imitator v006 · LIVE since 11:30pm"] ==>|approvals, 1:1 check only| ARC','IMI["Imitator v006 · LIVE since 11:30pm"] ==>|approvals, 1:1 check; deploy after Safeguard dry run| ARC')],
 "  ARC -->|deploy plan for dry run, case b| SFG\n")
sub('role-map-detail-identity-work.mmd',[('Role map v11 (16 Oct 2026 ~11:20am)','Role map v12 (16 Oct 2026 ~11:50am)'),('EXP["Explorer v004 04dcca0d ACTIVE"]','EXP["Explorer v005 04dcca0d ACTIVE · never writes profiles"]')])

s=(D/'summaries.md').read_text()
s=s.replace('# Bot summaries (role map v11, 16 Oct 2026 ~11:20am AEST)','# Bot summaries (role map v12, 16 Oct 2026 ~11:50am AEST)',1)
V=("## v12 — 16 Oct 2026 ~11:50am AEST (current)\n"
"Rebuilt after Gem's 11:41am approval in Archivist's chat (recorded first, R-029): Archivist v008 live 11:44:11 and Explorer v005 live 11:44:26; shared message verification v004 recorded. Descriptive only; v1–v11 kept as `*-vN.*`. **17 active (14 live, 3 dormant)** + 9 former/retired nodes, %d edges.\n"
"- Archivist may now deploy a version Imitator approved within its authority, after a 1:1 check with Imitator and Safeguard's dry-run report (new edge Archivist → Safeguard). Never for Archivist's own brief, Imitator or its five checkers, role-widening, spending or irreversible steps.\n"
"- Explorer still never writes profiles (R-014). R-010 has no update in rulings.md yet. No pending versions.\n\n")%len(g['edges'])
s=s.replace('## v11 — 16 Oct 2026 ~11:20am AEST (current)',V+'## v11 — 16 Oct 2026 ~11:20am AEST',1)
for k,old in [('ARC','codex-keeper/v007'),('EXP','explorer-copy/v004')]:
    f,t,w=NEW[k]; hdr=re.search(r'^### .*`%s`.*$'%ids[k][:8],s,re.M).group(0); assert old in hdr
    nh=hdr.replace(old,f); s=s.replace(hdr,nh,1); i=s.index(nh); j=s.find('\n\n',i)
    s=s[:j]+f"\n- v{f[-3:]} (Gem 11:41am, 16 Oct; live since {t}): {w}."+s[j:]
(D/'summaries.md').write_text(s)
r=(D/'README.md').read_text(); r=r.replace('## v11 — 16 Oct 2026 ~11:20am AEST (current)',V+"- Interactive view rebuilt from v12: `role-map-interactive.html`.\n\n## v11 — 16 Oct 2026 ~11:20am AEST",1); (D/'README.md').write_text(r)
f_=(D/'findings.md').read_text()
F=("## v12 findings (16 Oct 2026 ~11:50am AEST)\n"
"- Archivist v008 and Explorer v005 are live (byte-checked; verify 17/37, 0 pending), deployed on Gem's own 11:41am request (case (a)); Safeguard told ~11:42am. Scrutineer check requested.\n"
"- The deployment rule in three briefs now differs from R-010 as written in rulings.md; Arbiter may record an R-010 update.\n"
"- Shared message verification v004 needs Safeguard's dry-run report but, unlike Archivist v008, doesn't say what to do if Safeguard can't reply in time. Not a conflict, but not identical.\n"
"- Gem's 11:09am source words (context only) are logged in approvals/2026-10-09-gem-direct-words.md, a file named for 9 Oct.\n\n")
f_=f_.replace('## v11 findings',F+'## v11 findings',1); (D/'findings.md').write_text(f_)

# Role map v13, Investigator add-on (16 Oct 2026 ~11:57am AEST): investigator v004 live 11:49:23 on Gem's 11:48am approval; daily Imitator accuracy check, daily score to Scorer.
import json,re
from pathlib import Path
D=Path('/workspace/governance/cartography'); CX='/workspace/governance/codex/'
g=json.loads((D/'role-graph.json').read_text())
for n in g['nodes']:
    if n['key']=='INV':
        n['codex']=n['live_codex']=CX+'investigator/v004.md'
        n['note']=n['note'].replace('tests Imitator weekly','tests Imitator daily (v004)')+" v004 (Gem 11:48am, 16 Oct; live since 11:49:23): the Imitator accuracy check runs daily instead of weekly, and the accuracy score goes to Scorer daily; still a review after the fact, never a gate. Awaiting Scrutineer's check."
for e in g['edges']:
    e['source']=[CX+'investigator/v004.md' if s.endswith('investigator/v003.md') else s for s in e['source']]
    if e['relation']=='tests accuracy of (weekly)': e['relation']='tests accuracy of (daily, v004; was weekly)'
ids={n['key']:n['id'] for n in g['nodes']}; nm={n['key']:n['name'] for n in g['nodes']}
g['edges'].append({'from':ids['INV'],'from_name':nm['INV'],'to':ids['SCO'],'to_name':nm['SCO'],'relation':'sends the daily Imitator accuracy score to (v004; was weekly)','source':[CX+'investigator/v004.md'],'status':'current'})
g['stats']['edges']=len(g['edges']); g['version']='v13, 16 Oct 2026 ~11:52am AEST (Investigator v004 added ~11:57am)'
g['sources']['note']+=" Investigator v004 live 11:49:23 on Gem's 11:48am words: daily Imitator accuracy check and daily score to Scorer."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n"); print('edges',len(g['edges']))
def sub(path,pairs,tail=''):
    s=(D/path).read_text()
    for a,b in pairs: assert s.count(a)==1,(path,a); s=s.replace(a,b)
    (D/path).write_text(s.rstrip('\n')+'\n'+tail)
sub('role-map.mmd',[('INV["Investigator v003<br/>LIVE"]','INV["Investigator v004<br/>LIVE · daily Imitator check"]'),
 ('%% v13: P5 LIVE 16 Oct 11:47am (Gem, "Initiate p5"); all five phases live.','%% v13: P5 LIVE 16 Oct 11:47am (Gem, "Initiate p5"); all five phases live. Investigator v004 live 11:49: daily Imitator check, daily score to Scorer.')],
 "  INV -->|daily accuracy score| SCO\n  linkStyle 45 stroke:#2e7d32,stroke-width:2px\n")
sub('role-map-detail-identity-work.mmd',[('INF --> INV["Investigator v003 · LIVE"]','INF --> INV["Investigator v004 · LIVE · daily Imitator check"]'),
 ('INV -->|reviews after the fact| IMI','INV -->|daily check, reviews after the fact| IMI')])
s=(D/'summaries.md').read_text()
a="- Now live: Emissary is the only postiz poster"
assert s.count(a)==1
s=s.replace(a,"- Investigator v004 live 11:49:23 (Gem 11:48am in Archivist's chat): the Imitator accuracy check is daily, and the score goes to Scorer daily (new edge Investigator → Scorer). Awaiting Scrutineer's check.\n"+a,1)
s=s.replace("+ 9 former/retired nodes, 43 edges.\n- No codex change: Emissary","+ 9 former/retired nodes, %d edges.\n- No codex change for P5: Emissary"%len(g['edges']),1)
hdr=re.search(r'^### .*`f2016e9b`.*$',s,re.M).group(0); nh=hdr.replace('investigator/v003','investigator/v004'); assert nh!=hdr; s=s.replace(hdr,nh,1)
a="- Tests Imitator weekly and reviews its decisions after the fact (not a gate)."
assert s.count(a)==1
s=s.replace(a,"- Tests Imitator daily and reviews its decisions after the fact (not a gate).\n- v004 (Gem 11:48am, 16 Oct; live since 11:49:23): the Imitator accuracy check and the score to Scorer are daily, not weekly. Awaiting Scrutineer's check.",1)
(D/'summaries.md').write_text(s)
r=(D/'README.md').read_text()
a="- Interactive view rebuilt from v13: `role-map-interactive.html`."
assert r.count(a)==1
r=r.replace("+ 9 former/retired nodes, 43 edges.\n- No codex change: Emissary","+ 9 former/retired nodes, %d edges.\n- No codex change for P5: Emissary"%len(g['edges']),1)
r=r.replace(a,"- Investigator v004 live 11:49:23 (Gem 11:48am): daily Imitator accuracy check and daily score to Scorer (new edge). Awaiting Scrutineer's check.\n"+a,1)
(D/'README.md').write_text(r)
f=(D/'findings.md').read_text(); a="- Mediator's live name is still \"P4 (Ops) Mediator\" while phases.md lists it under P2.\n\n## v12 findings"
assert f.count(a)==1
f=f.replace(a,"- Mediator's live name is still \"P4 (Ops) Mediator\" while phases.md lists it under P2.\n- Investigator v004 (live 11:49:23) makes the Imitator check daily. Mender's `schedule.md` still lists Investigator as weekly; the proposal README says Mender should update it. Scorer may want a weekly roll-up of the noisier daily score.\n- Investigator's source was Gem's 11:05am words, \"Always approve imitator, run the accuracy check for Imitator daily\". Only the daily part was drafted; the default reading of \"Always approve imitator\" (never block Imitator) is already in the brief.\n\n## v12 findings",1)
(D/'findings.md').write_text(f)

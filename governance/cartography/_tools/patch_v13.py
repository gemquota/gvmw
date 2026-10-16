# Role map v13 (16 Oct 2026 ~11:52am AEST): P5 LIVE per phases.md (Gem in Explorer's chat 11:47am, "Initiate p5"). No codex change.
import json,re
from pathlib import Path
D=Path('/workspace/governance/cartography')
PS='LIVE (started 16 Oct 2026, 11:47am AEST)'
g=json.loads((D/'role-graph.json').read_text())
for n in g['nodes']:
    if n.get('phase')=='P5':
        n['phase_status']=PS; n['map_status']='active'
        n['note']=re.sub(r';? ?[Ii]tself dormant until P5\.?|\.? ?[Dd]ormant until P5\.?|; dormant until P5','.',n['note']).replace('..','.').replace('.;',';')
        n['note']+=" LIVE since 16 Oct 2026, 11:47am AEST (P5; phases.md, Gem in Explorer's chat: \"Initiate p5\")."
for e in g['edges']:
    if e['status'].endswith('dormant (P5)'): e['status']='current'
for p in g['phases']:
    if p['phase']=='P5': p['status']=PS
g['stats'].update(live=17,dormant=0)
g['previous_version']=g['version']; g['version']='v13, 16 Oct 2026 ~11:52am AEST'
g['sources']['note']=g['sources']['note'].replace("17 active (14 live, 3 dormant P5). P3 and P4 LIVE since 15 Oct 2026, 11:30pm AEST.","17 active, all live: P3 and P4 LIVE since 15 Oct 2026, 11:30pm AEST; P5 LIVE since 16 Oct 2026, 11:47am AEST (Gem, \"Initiate p5\").")
assert 'P5 LIVE since' in g['sources']['note']
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")
print('dormant left:',[n['key'] for n in g['nodes'] if n.get('map_status')=='dormant'],[e['to_name'] for e in g['edges'] if 'ormant' in e['status']])
def sub(path,pairs):
    s=(D/path).read_text()
    for a,b in pairs: assert s.count(a)==1,(path,a); s=s.replace(a,b)
    (D/path).write_text(s)
sub('role-map.mmd',[('Role map v12, 16 Oct 2026 ~11:50am AEST','Role map v13, 16 Oct 2026 ~11:52am AEST'),
 ('%% v12: ','%% v13: P5 LIVE 16 Oct 11:47am (Gem, "Initiate p5"); all five phases live. v12: '),
 ('<b>Legend v12</b>','<b>Legend v13</b>'),('subgraph P5["P5 · Dormant"]','subgraph P5["P5 · LIVE since 16 Oct 11:47am"]')])
for f in ['role-map-detail-governance.mmd','role-map-detail-identity-work.mmd']:
    sub(f,[('Role map v12 (16 Oct 2026 ~11:50am)','Role map v13 (16 Oct 2026 ~11:52am; P5 live)')])
sub('role-map-detail-identity-work.mmd',[('EMI["Emissary v006 · only postiz poster"]','EMI["Emissary v006 · LIVE · only postiz poster"]'),
 ('ENG["Engineer v007 · Vercel = public push"]','ENG["Engineer v007 · LIVE · Vercel = public push"]'),('EXT["Extractor v005 · BIE data stays on box"]','EXT["Extractor v005 · LIVE · BIE data stays on box"]')])
s=(D/'summaries.md').read_text()
s=s.replace('# Bot summaries (role map v12, 16 Oct 2026 ~11:50am AEST)','# Bot summaries (role map v13, 16 Oct 2026 ~11:52am AEST)',1)
V=("## v13 — 16 Oct 2026 ~11:52am AEST (current)\n"
"P5 (Emissary, Engineer, Extractor) went LIVE at 11:47am on 16 Oct 2026 (phases.md; Gem in Explorer's chat: \"Initiate p5\"). All five phases are live. Descriptive only; v1–v12 kept as `*-vN.*`. **17 active, all live** + 9 former/retired nodes, %d edges.\n"
"- No codex change: Emissary v006, Engineer v007 and Extractor v005 as before. Explorer's routing edges to them are no longer faded.\n"
"- Now live: Emissary is the only postiz poster, posting only text Gem approved word for word; Engineer's Vercel deployments count as public pushes; every public or shared repo push still goes to Safeguard first (R-020).\n\n")%len(g['edges'])
s=s.replace('## v12 — 16 Oct 2026 ~11:50am AEST (current)',V+'## v12 — 16 Oct 2026 ~11:50am AEST',1)
for a,b in [('## P5: Dormant','## P5: LIVE (started 16 Oct 2026, 11:47am AEST)'),('General work routed by Explorer; dormant until P5.','General work routed by Explorer; live since 16 Oct 11:47am.'),
 ('Code and swarm work; absorbed Ensembler; dormant until P5.','Code and swarm work; absorbed Ensembler; live since 16 Oct 11:47am.'),('Research and data extraction routed by Explorer; dormant until P5.','Research and data extraction routed by Explorer; live since 16 Oct 11:47am.')]:
    assert s.count(a)==1,a; s=s.replace(a,b)
(D/'summaries.md').write_text(s)
r=(D/'README.md').read_text(); r=r.replace('## v12 — 16 Oct 2026 ~11:50am AEST (current)',V+"- Interactive view rebuilt from v13: `role-map-interactive.html`.\n\n## v12 — 16 Oct 2026 ~11:50am AEST",1); (D/'README.md').write_text(r)
f_=(D/'findings.md').read_text()
F=("## v13 findings (16 Oct 2026 ~11:52am AEST)\n"
"- P5 is live per phases.md (Gem's \"Initiate p5\" in Explorer's chat, 11:47am). The three P5 briefs were last changed for P5 at 11:03am (RR-028), so no codex change was needed for the switch-on.\n"
"- phases.md still lists the old Inquirer `e613112b` as \"awaiting Gem's decision to retire\" and the 9 Oct retirees as \"awaiting deletion\"; those folders are gone. Its \"Last updated\" says 11:48am, but the file was written at 11:47:37. Explorer owns phases.md, so Archivist hasn't edited it.\n"
"- Mediator's live name is still \"P4 (Ops) Mediator\" while phases.md lists it under P2.\n\n")
f_=f_.replace('## v12 findings',F+'## v12 findings',1); (D/'findings.md').write_text(f_)

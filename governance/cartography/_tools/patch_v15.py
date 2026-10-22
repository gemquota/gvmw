# Role map v15 (22 Oct 2026): unrecorded live agent "New Bot" (6b01a4ef) listed under Archivist's brief: a node with no role and no relationships. No codex change.
import json,sys
from pathlib import Path
D=Path('/workspace/governance/cartography'); NOW=sys.argv[1]
ID='6b01a4ef-8b54-44e6-ad11-64e7af681d12'
NOTE=("Unrecorded live agent, awaiting Gem. Name \"New Bot\"; blank (no title, description or instructions); no codex folder, so no role and no relationships on this map. "
      "First seen: profile.json created 19 Oct 2026 01:30:54 AEST; reported by Explorer to Archivist ~6:31pm AEST 22 Oct 2026. Not in phases.md. verify.py labels it GROUP (INFO) only because its description is empty.")
g=json.loads((D/'role-graph.json').read_text())
assert not any(n['id']==ID for n in g['nodes'])
g['nodes'].append({'id':ID,'name':'New Bot','key':'NEW','type':'bot','category':'Unrecorded','phase':None,'phase_status':'None (not in phases.md)',
  'codex':None,'former_name':None,'absorbed':[],'map_status':'unrecorded','note':NOTE})
g['unrecorded_live_agents']=[{'id':ID,'name':'New Bot','first_seen':'profile.json created 19 Oct 2026 01:30:54 AEST; reported by Explorer ~6:31pm AEST 22 Oct 2026','status':'unrecorded live agent, awaiting Gem','role':None}]
g['previous_version']=g['version']; g['version']=f'v15, 22 Oct 2026 {NOW} AEST'
g['stats'].update(nodes=len(g['nodes']),edges=len(g['edges']),unrecorded=1)
g['sources']['note']+=" 22 Oct: unrecorded live agent \"New Bot\" (6b01a4ef, created 19 Oct 01:30:54) listed, awaiting Gem; no role."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n"); print('nodes',len(g['nodes']),'edges',len(g['edges']))
def sub(p,pairs):
    s=(D/p).read_text()
    for a,b in pairs: assert s.count(a)==1,(p,a); s=s.replace(a,b)
    (D/p).write_text(s)
sub('role-map.mmd',[('Role map v14, 16 Oct 2026 3:58:15pm AEST',f'Role map v15, 22 Oct 2026 {NOW} AEST'),
 ('%% v14: ','%% v15: unrecorded live agent New Bot 6b01a4ef listed, no role, no relationships, awaiting Gem. v14: '),
 ('<b>Legend v14</b>','<b>Legend v15</b>'),
 ('  GEM ~~~ ARX\n','  subgraph UNREC["UNRECORDED live agent · awaiting Gem"]\n    NEW["New Bot 6b01a4ef<br/>blank · no codex folder<br/>no role · no relationships<br/>created 19 Oct 01:30:54am"]\n  end\n  style NEW stroke-dasharray: 5 3\n\n  GEM ~~~ ARX\n')])
for f in ['role-map-detail-governance.mmd','role-map-detail-identity-work.mmd','role-map-detail-connectors.mmd']:
    s=(D/f).read_text(); s=s.replace('Role map v14 (16 Oct 2026 3:58:15pm',f'Role map v15 (22 Oct 2026 {NOW}; unchanged from v14 detail',1); (D/f).write_text(s)
V=(f"## v15 — 22 Oct 2026 {NOW} AEST (current)\n"
"Unrecorded live agent listed under Archivist's brief: **New Bot** (`6b01a4ef-8b54-44e6-ad11-64e7af681d12`), blank, with no codex folder. It's drawn as a node with no role and no relationships, awaiting Gem. "
"First seen: profile.json created 19 Oct 2026 01:30:54 AEST; reported by Explorer to Archivist ~6:31pm AEST 22 Oct. No codex change; v1–v14 kept as `*-vN.*`. "
f"**17 active, all live** + 1 unrecorded + 9 former/retired nodes, {len(g['edges'])} edges.\n\n")
for f in ['summaries.md','README.md']:
    s=(D/f).read_text(); a='## v14 — 16 Oct 2026 3:58:15pm AEST (current)'; assert s.count(a)==1,f
    s=s.replace(a,V+(("- Interactive view rebuilt from v15: `role-map-interactive.html` (new \"Unrecorded\" row).\n\n") if f=='README.md' else '')+'## v14 — 16 Oct 2026 3:58:15pm AEST',1)
    if f=='summaries.md': s=s.replace('# Bot summaries (role map v14, 16 Oct 2026 3:58:15pm AEST)',f'# Bot summaries (role map v15, 22 Oct 2026 {NOW} AEST)',1)
    (D/f).write_text(s)
f_=(D/'findings.md').read_text()
F=(f"## v15 findings (22 Oct 2026 {NOW} AEST)\n"
"- New Bot (`6b01a4ef`) is a live agent folder with a blank profile, created 19 Oct 01:30:54am, three days before Explorer reported it. It has no codex folder, so nothing is recorded and it gets no role; Gem to decide what it is.\n"
"- verify.py lists it as GROUP (INFO), because its rule treats any agent with an empty description as a group channel. Nothing on disk shows New Bot is a group, so this map lists it as an unrecorded live agent, as Archivist's brief says for a live agent with no codex folder.\n\n")
f_=f_.replace('## v14 findings',F+'## v14 findings',1); (D/'findings.md').write_text(f_)

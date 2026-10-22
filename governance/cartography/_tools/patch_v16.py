# Role map v16 (22 Oct 2026): New Bot (6b01a4ef) retired (Gem 6:37pm). No role, no edges; deletion not confirmed.
import json,sys,re
from pathlib import Path
D=Path('/workspace/governance/cartography'); NOW=sys.argv[1]
ID='6b01a4ef-8b54-44e6-ad11-64e7af681d12'
ST=("Retired (Gem, 22 Oct 6:37pm, confirmed in Archivist's chat: \"Yes, record New Bot as retired\"; confirms Explorer's relay of \"Retire it\"). "
    "Gone from the live teammate list by about 6:40pm, so probably deleted by Gem; deletion not confirmed, and its folder remains. Awaiting Gem's confirmation of the delete from the sidebar. "
    "Blank; never had instructions, so no codex folder, no role and no relationships. Created 19 Oct 2026 01:30:54 AEST; reported by Explorer ~6:31pm 22 Oct.")
g=json.loads((D/'role-graph.json').read_text())
n=[x for x in g['nodes'] if x['id']==ID]; assert len(n)==1 and n[0]['map_status']=='unrecorded'; n=n[0]
n.update(name='RETIRED New Bot',former_name='New Bot',map_status='retired_nocodex',phase_status='Retired 22 Oct 6:37pm (Gem); deletion not confirmed, folder remains',note=ST)
assert not any(ID in (e.get('from'),e.get('to'),e.get('source'),e.get('target')) for e in g['edges'])
g.setdefault('retired_no_codex',[]).append({'id':ID,'name':'New Bot','status':'retired (Gem, 22 Oct 6:37pm, confirmed in Archivist\'s chat); gone from live teammate list ~6:40pm; deletion not confirmed; folder remains','role':None})
g['unrecorded_live_agents']=[]
g['previous_version']=g['version']; g['version']=f'v16, 22 Oct 2026 {NOW} AEST'
g['stats'].update(unrecorded=0,retired_no_codex=1)
g['sources']['note']+=f" 22 Oct {NOW}: New Bot recorded as retired (Gem 6:37pm); deletion not confirmed."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")
def sub(p,pairs):
    s=(D/p).read_text()
    for a,b in pairs: assert s.count(a)==1,(p,a); s=s.replace(a,b)
    (D/p).write_text(s)
sub('role-map.mmd',[('Role map v15, 22 Oct 2026 6:34:10pm AEST',f'Role map v16, 22 Oct 2026 {NOW} AEST'),
 ('%% v15: ','%% v16: New Bot retired (Gem 22 Oct 6:37pm), no role, no edges; deletion not confirmed. v15: '),
 ('<b>Legend v15</b>','<b>Legend v16</b>'),
 ('subgraph UNREC["UNRECORDED live agent · awaiting Gem"]','subgraph UNREC["RETIRED 22 Oct · no codex folder · deletion not confirmed"]'),
 ('NEW["New Bot 6b01a4ef<br/>blank · no codex folder<br/>no role · no relationships<br/>created 19 Oct 01:30:54am"]','NEW["RETIRED New Bot 6b01a4ef<br/>retired by Gem 22 Oct 6:37pm<br/>off live list ~6:40pm · folder remains<br/>no role · no relationships"]'),
 ('style NEW stroke-dasharray: 5 3','style NEW stroke-dasharray: 2 3,fill:#f2f2f2,stroke:#9e9e9e,color:#757575')])
for f in ['role-map-detail-governance.mmd','role-map-detail-identity-work.mmd','role-map-detail-connectors.mmd']:
    s=(D/f).read_text(); a='Role map v15 (22 Oct 2026 6:34:10pm'; assert s.count(a)==1,f; (D/f).write_text(s.replace(a,f'Role map v16 (22 Oct 2026 {NOW}'))
V=(f"## v16 — 22 Oct 2026 {NOW} AEST (current)\n"
"**New Bot** (`6b01a4ef`) recorded as **retired** (Gem, 22 Oct 6:37pm, confirmed in Archivist's chat). It was gone from the live teammate list by about 6:40pm, so it was probably deleted by Gem, but deletion isn't confirmed and its folder remains. "
"Drawn dotted grey in the \"No codex folder\" row, with no role and no edges. No codex change; v1–v15 kept as `*-vN.*`. "
f"17 active, all live + 1 retired with no codex folder + 9 former/retired nodes, {len(g['edges'])} edges.\n\n")
for f in ['summaries.md','README.md']:
    s=(D/f).read_text(); a='## v15 — 22 Oct 2026 6:34:10pm AEST (current)'; assert s.count(a)==1,f
    s=s.replace(a,V+(("- Interactive view rebuilt from v16: `role-map-interactive.html`.\n\n") if f=='README.md' else '')+'## v15 — 22 Oct 2026 6:34:10pm AEST',1)
    if f=='summaries.md': s=s.replace('# Bot summaries (role map v15, 22 Oct 2026 6:34:10pm AEST)',f'# Bot summaries (role map v16, 22 Oct 2026 {NOW} AEST)',1)
    if f=='README.md': s=s.replace('- Interactive view rebuilt from v15: `role-map-interactive.html` (new "Unrecorded" row).\n',
      '- Interactive view rebuilt from v15: `role-map-interactive.html` (new "Unrecorded" row).\n- **INC-008 (22 Oct ~6:38pm):** the box restart briefly lost `/workspace/governance`. After Mender\'s restore (~6:43pm) the v15 files were back. Archivist checked them at 6:43pm by re-running `_tools/patch_v15.py` on the v14 files with the original time (6:34:10pm): all 8 source files were byte-identical, so v15 stands as restored and was not regenerated.\n',1)
    (D/f).write_text(s)
f_=(D/'findings.md').read_text()
F=(f"## v16 findings (22 Oct 2026 {NOW} AEST)\n"
"- New Bot was retired by Gem at 6:37pm 22 Oct, after being listed at 6:33pm. It dropped off the live teammate list by about 6:40pm, but `/home/box/agent-data/agents/6b01a4ef-…` is still on the box, so verify.py still lists it as GROUP (INFO). Don't record it as deleted until Gem confirms.\n"
"- phases.md (Explorer's file) never listed New Bot, so it needs no phase change; Explorer may add a retirement note.\n\n")
(D/'findings.md').write_text(f_.replace('## v15 findings',F+'## v15 findings',1))
# interactive builder + template
b=(D/'_tools/build_interactive.py').read_text()
b=b.replace("'unrecorded': 'Unrecorded, awaiting Gem'}","'unrecorded': 'Unrecorded, awaiting Gem', 'retired_nocodex': 'Retired (Gem, 22 Oct 6:37pm); deletion not confirmed'}",1)
b=b.replace("'tier': 'unrecorded' if ms == 'unrecorded' else","'tier': 'unrecorded' if ms in ('unrecorded', 'retired_nocodex') else",1)
(D/'_tools/build_interactive.py').write_text(b)
t=(D/'_tools/interactive_template.html').read_text()
for a,c in [('unrecorded:"Unrecorded"};','unrecorded:"No codex folder"};'),
 ('else if (n.group === "Unrecorded") el("rect", {x:-NW/2, y:-NH/2, width:NW, height:NH, rx:7, fill, stroke, "stroke-dasharray":"5 3"}, g);',
  'else if (n.group === "Unrecorded") el("rect", {x:-NW/2, y:-NH/2, width:NW, height:NH, rx:7, fill: /^Retired/.test(n.status) ? "#f2f2f2" : fill, stroke, "stroke-dasharray": /^Retired/.test(n.status) ? "2 3" : "5 3"}, g);'),
 ('n.group === "Unrecorded" ? "None (unrecorded live agent, awaiting Gem)" :','n.group === "Unrecorded" ? (/^Retired/.test(n.status) ? "None (retired; never had a codex folder)" : "None (unrecorded live agent, awaiting Gem)") :')]:
    assert t.count(a)==1,a; t=t.replace(a,c)
(D/'_tools/interactive_template.html').write_text(t)
print('ok')

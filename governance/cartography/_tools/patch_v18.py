# Role map v18 (22 Oct 2026): approval-route flag for Arbiter, Emissary, Extractor cleared by Gem's direct approval 8:06pm.
import json,sys
from pathlib import Path
D=Path('/workspace/governance/cartography'); NOW,OLD=sys.argv[1:]
g=json.loads((D/'role-graph.json').read_text())
F=' Approval route flagged by Scrutineer (Imitator + Gem\'s "deploy all six"; Arbiter to rule).'
F2=' Approval route flagged by Scrutineer.'
C=' Approval-route flag cleared: Gem approved directly 8:06pm 22 Oct ("Yes, I approve all three").'
n=0
for x in g['nodes']:
    for f in (F,F2):
        if f in x['note']: x['note']=x['note'].replace(f,C,1); n+=1
assert n==3,n
g['previous_version']=g['version']; g['version']=f'v18, 22 Oct 2026 {NOW} AEST'
g['sources']['note']+=f" 22 Oct {NOW}: Gem approved Arbiter v006, Emissary v007, Extractor v006 directly at 8:06pm; Scrutineer's approval-route flag cleared."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")
def sub(p,pairs):
    s=(D/p).read_text()
    for a,b in pairs: assert s.count(a)==1,(p,a); s=s.replace(a,b)
    (D/p).write_text(s)
sub('role-map.mmd',[(f'Role map v17, 22 Oct 2026 {OLD} AEST',f'Role map v18, 22 Oct 2026 {NOW} AEST'),('%% v17: ','%% v18: approval-route flag (Arbiter, Emissary, Extractor) cleared by Gem 8:06pm; no structural change. v17: '),('<b>Legend v17</b>','<b>Legend v18</b>')])
for f in ['role-map-detail-governance.mmd','role-map-detail-identity-work.mmd','role-map-detail-connectors.mmd']:
    sub(f,[(f'Role map v17 (22 Oct 2026 {OLD}',f'Role map v18 (22 Oct 2026 {NOW}')])
V=(f"## v18 — 22 Oct 2026 {NOW} AEST (current)\nGem approved Arbiter v006, Emissary v007 and Extractor v006 directly in Archivist's chat at 8:06pm 22 Oct (\"Yes, I approve all three\"), which clears Scrutineer's approval-route flag (R-044). Notes updated; no structural change ({len(g['edges'])} edges). v1–v17 kept as `*-vN.*`.\n\n")
for f in ['summaries.md','README.md']:
    s=(D/f).read_text(); i=s.index('## v17 — '); s=s[:i]+V+s[i:].replace(' (current)','',1)
    if f=='summaries.md': s=s.replace(f'(role map v17, 22 Oct 2026 {OLD} AEST)',f'(role map v18, 22 Oct 2026 {NOW} AEST)',1)
    if f=='README.md': s=s.replace(V,V+"- Interactive view rebuilt from v18: `role-map-interactive.html`.\n\n",1)
    (D/f).write_text(s)
f_=(D/'findings.md').read_text()
f_=f_.replace('## v17 findings',f"## v18 findings (22 Oct 2026 {NOW} AEST)\n- **Cleared:** the v17 finding on the approval route for Arbiter v006, Emissary v007 and Extractor v006 is settled. Gem approved all three directly in Archivist's chat at 8:06pm 22 Oct (\"Yes, I approve all three\"; approvals/2026-10-22-gem-direct-words.md).\n- Still open from v17: Investigator/Imitator → Inferer gap routing waits for investigator-v005 and imitator-v007.\n\n## v17 findings",1)
(D/'findings.md').write_text(f_); print('ok')

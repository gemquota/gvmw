# Role map v21 (22 Oct 2026): GitHub revision 5h LIVE ~9:41pm. Engineer only changes GitHub, fully free (no per-push approval or Safeguard check); others read only.
import json,sys
from pathlib import Path
D=Path('/workspace/governance/cartography'); NOW=sys.argv[1]; CX='/workspace/governance/codex/'
g=json.loads((D/'role-graph.json').read_text()); K={n['key']:n for n in g['nodes']}; ID={n['id']:n['key'] for n in g['nodes']}
U={'ENG':('codey/v008','21:40:26',"only bot that commits, pushes, branches, opens pull requests or merges; fully free on Gem's repos, with no per-push approval or Safeguard check (Gem 7:52pm); public deployments (e.g. Vercel) still go to Safeguard first."),
 'IMI':('clone/v009','21:40:43',"reads only on GitHub, never commits or pushes, and approves none of Engineer's pushes."),
 'EXP':('explorer-copy/v007','21:41:03',"reads only on GitHub and routes every change to Engineer (R-045); Imitator-approval deploy route now also needs Safeguard's report and never covers Archivist's own instructions."),
 'ARX':('instruction-architect/v006','21:41:09',"reads only on GitHub."),
 'ARB':('arbiter/v008','21:41:15',"reads only on GitHub.")}
for k,(c,t,w) in U.items():
    n=K[k]; n['codex']=CX+c+'.md'
    if n.get('live_codex') or k in ('IMI','EXP'): n['live_codex']=CX+c+'.md'
    n['note']=f"LIVE {c.split('/')[1]} (deployed 22 Oct {t} AEST, GitHub revision 5h, Gem's 9:27pm words t72u item 4): {w} Earlier: "+n['note']
for e in g['edges']:
    a,b=ID[e['from']],ID[e['to']]
    if b=='SFG' and e['status']=='current' and e['relation']=='public/shared repo pushes go first to (R-020)':
        if a=='ENG': e['relation']="public deployments go first to (R-020); its GitHub pushes and merges need no Safeguard check (github-v001; Gem 7:52pm)"; e['source']=[CX+'codey/v008.md',CX+'_shared/github/v001.md']
        else: e['relation']="risky actions go first to (R-020); no GitHub changes, which only Engineer makes (github-v001)"; e['source']=[CX+'_shared/github/v001.md']
OLD=g['version'].split('2026 ')[1].split(' AEST')[0]
g['previous_version']=g['version']; g['version']=f'v21, 22 Oct 2026 {NOW} AEST'
g['sources']['note']+=f" 22 Oct {NOW}: GitHub revision 5h LIVE ~9:41pm (shared GitHub v001, message verification v005); Engineer only, free on GitHub."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")
def sub(p,pairs):
    s=(D/p).read_text()
    for x,y in pairs: assert s.count(x)==1,(p,x); s=s.replace(x,y)
    (D/p).write_text(s)
sub('role-map.mmd',[(f'Role map v20, 22 Oct 2026 {OLD} AEST',f'Role map v21, 22 Oct 2026 {NOW} AEST'),('%% v20: ','%% v21: GitHub 5h LIVE ~9:41pm: only Engineer changes GitHub, free (no per-push Safeguard check); others read only; red edges relabelled. v20: '),
 ('<b>Legend v20</b>','<b>Legend v21</b>'),('red = repo pushes to Safeguard first','red = risky actions to Safeguard first (GitHub: Engineer only, free)'),('green = added in v11–v20','green = added in v11–v21'),
 ('ARX["Architect v005"]','ARX["Architect v006"]'),('EXP["Explorer v006 04dcca0d','EXP["Explorer v007 04dcca0d'),('ARB["Arbiter v007"]','ARB["Arbiter v008"]'),('IMI["Imitator v008 · LIVE','IMI["Imitator v009 · LIVE'),('ENG["Engineer v007"]','ENG["Engineer v008<br/>only GitHub writer, free"]'),
 ('SFG["Safeguard v006<br/>repo pushes reviewed first','SFG["Safeguard v006<br/>risky actions reviewed first'),
 ('EXP -->|repo push first| SFG','EXP -->|risky actions first| SFG'),('ENG -->|repo push first| SFG','ENG -->|public deploys first| SFG'),('EXT -->|repo push first| SFG','EXT -->|risky actions first| SFG'),('EMI -->|repo push first| SFG','EMI -->|risky actions first| SFG'),('IMI -->|repo push first| SFG','IMI -->|risky actions first| SFG')])
sub('role-map-detail-governance.mmd',[(f'Role map v20 (22 Oct 2026 {OLD}',f'Role map v21 (22 Oct 2026 {NOW}'),('ARX["Architect v005"]','ARX["Architect v006"]'),('IMI["Imitator v008 · LIVE since 9:35pm 22 Oct"]','IMI["Imitator v009 · LIVE since 9:40pm 22 Oct"]')])
sub('role-map-detail-identity-work.mmd',[(f'Role map v20 (22 Oct 2026 {OLD}',f'Role map v21 (22 Oct 2026 {NOW}'),('IMI["Imitator v008 · LIVE','IMI["Imitator v009 · LIVE'),('EXP["Explorer v005 04dcca0d','EXP["Explorer v007 04dcca0d'),('ENG["Engineer v007 · LIVE · Vercel = public push"]','ENG["Engineer v008 · LIVE · only GitHub writer · Vercel = public deploy"]')])
sub('role-map-detail-connectors.mmd',[(f'Role map v20 (22 Oct 2026 {OLD}',f'Role map v21 (22 Oct 2026 {NOW}')])
V=(f"## v21 — 22 Oct 2026 {NOW} AEST (current)\nGitHub revision 5h LIVE (~9:41pm; Gem's 9:27pm words in Archivist's chat, t72u item 4): the shared GitHub rule v001 and message verification v005 are in effect. Engineer v008 is the only bot that changes GitHub and is fully free there (no per-push approval or Safeguard check); Imitator v009, Explorer v007, Architect v006 and Arbiter v008 only read. The red Safeguard edges now read 'risky actions first' (Engineer: 'public deploys first'). {len(g['edges'])} edges; v1–v20 kept as `*-vN.*`.\n\n")
for f in ['summaries.md','README.md']:
    s=(D/f).read_text(); k=s.index('## v20 — '); s=s[:k]+V+s[k:].replace(' (current)','',1)
    if f=='summaries.md': s=s.replace(f'(role map v20, 22 Oct 2026 {OLD} AEST)',f'(role map v21, 22 Oct 2026 {NOW} AEST)',1)
    if f=='README.md': s=s.replace(V,V+"- Interactive view rebuilt from v21: `role-map-interactive.html`.\n\n",1)
    (D/f).write_text(s)
f_=(D/'findings.md').read_text()
f_=f_.replace('## v20 findings',f"## v21 findings (22 Oct 2026 {NOW} AEST)\n- Emissary's and Extractor's own briefs weren't changed in revision 5h; the shared GitHub rule and message verification v005 make them read-only on GitHub, so their red edges are relabelled from the shared rules.\n- Engineer merges its own pull requests without a separate sign-off, which relaxes 'no bot verifies its own work' (README flag Q2, on Gem's 7:52pm words).\n\n## v20 findings",1)
(D/'findings.md').write_text(f_); print('ok',len(g['edges']))

# Role map v26 (3 Nov 2026): Archivist LIVE v014 (Gem Yes t105u 6:05am); Arbiter LIVE v011 (out-of-scope 30 Oct, kept by Gem 3 Nov 6:03am). Folders of five retired bots deleted by Gem (R-056 pt2 closed).
import json,sys,re
from pathlib import Path
D=Path('/workspace/governance/cartography'); NOW=sys.argv[1]; CX='/workspace/governance/codex/'
g=json.loads((D/'role-graph.json').read_text()); K={n['key']:n for n in g['nodes']}
V={
  'ARC':('codex-keeper','v014','6:05:24am',
    "LIVE v014 (deployed 3 Nov 2026 ~6:05:24am AEST under Gem's Yes t105u, case a; Scrutineer check 6 PASS 3 Nov, text hash 889b5517ec1f): own-brief deploy. Earlier: "),
  'ARB':('arbiter','v011','6:03am keep',
    "LIVE v011 (deployed outside approval scope 30 Oct; kept by Gem 3 Nov 6:03am AEST, \"Keep Arbiter v011 live\"; Scrutineer check 6 PASS 3 Nov, text hash 1ff85a4238fd). Earlier: "),
}
for k,(f,v,t,prefix) in V.items():
    n=K[k]; n['codex']=f'{CX}{f}/{v}.md'; n['live_codex']=n['codex']
    n['note']=prefix+n['note']
# Fix retired five: folders deleted by Gem (R-056 pt2)
for n in g['nodes']:
    if n.get('map_status')=='retired_merged' and n.get('key') in ('MED','SCO','SFK','INQ','EXT'):
        n['note']=n['note'].replace(
            "folder kept, nothing deleted",
            "agent folder deleted by Gem (Gem Arbiter chat t68u: \"I did, my bad\"; R-056 point 2 closed 3 Nov 6:05am); codex folder kept, nothing else deleted"
        ).replace(
            "folders were gone by 10:53pm, not deleted by Archivist",
            "folders deleted by Gem (R-056 pt2 closed 3 Nov)"
        )
g['previous_version']=g['version']
OLD=g['version']  # e.g. 'v25, 22 Oct 2026 11:14:29pm AEST'
g['version']=f'v26, 3 Nov 2026 {NOW} AEST'
note=g['sources'].get('note','')
g['sources']['note']=note+f" 3 Nov {NOW}: Archivist v014 LIVE; Arbiter v011 kept LIVE; R-056 pt2 folder deletion closed."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")

def vers(s):
    s=re.sub(r'(ARC\["Archivist )v013', r'\g<1>v014', s)
    s=re.sub(r'(ARB\["Arbiter )v010', r'\g<1>v011', s)
    s=s.replace('Archivist v013 · owns directory.md','Archivist v014 · owns directory.md')
    return s

s=vers((D/'role-map.mmd').read_text())
# header bumps
repls=[
 (f'Role map v25, 22 Oct 2026 11:14:29pm AEST',f'Role map v26, 3 Nov 2026 {NOW} AEST'),
 ('%% v25: phase-cleanup revision 3 LIVE; shared rules box updated. v24: ',
  '%% v26: Archivist v014 LIVE (Gem Yes t105u); Arbiter v011 kept by Gem; R-056 pt2 folders. v25: phase-cleanup revision 3 LIVE; shared rules box updated. v24: '),
 ('<b>Legend v25</b>','<b>Legend v26</b>'),
 ('green = added in v11–v25','green = added in v11–v26'),
]
for a,b in repls:
    assert s.count(a)==1, repr(a); s=s.replace(a,b)
(D/'role-map.mmd').write_text(s)

for p in ['role-map-detail-governance.mmd','role-map-detail-identity-work.mmd','role-map-detail-connectors.mmd']:
    t=vers((D/p).read_text())
    a='Role map v25 (22 Oct 2026 11:14:29pm'
    assert t.count(a)==1,(p,a)
    t=t.replace(a,f'Role map v26 (3 Nov 2026 {NOW}')
    (D/p).write_text(t)

Vt=(f"## v26 — 3 Nov 2026 {NOW} AEST (current)\n"
    "Archivist LIVE v014 (deployed ~6:05:24am under Gem's Yes t105u; Scrutineer check 6 PASS 3 Nov) and Arbiter LIVE v011 "
    "(deployed outside approval scope 30 Oct; kept by Gem 3 Nov 6:03am). "
    "Five retired-bot agent folders (Mediator, Scorer, Safekeeper, Inquirer, Extractor) recorded as deleted by Gem "
    "(Gem Arbiter chat t68u: \"I did, my bad\"; Arbiter R-056 point 2 closed 3 Nov 6:05am). "
    "No other label or edge change. v1–v25 kept as `*-vN.*`.\n\n")
for f in ['summaries.md','README.md']:
    x=(D/f).read_text(); k=x.index('## v25 — '); x=x[:k]+Vt+x[k:].replace(' (current)','',1)
    if f=='summaries.md':
        x=x.replace('(role map v25, 22 Oct 2026 11:14:29pm AEST)',f'(role map v26, 3 Nov 2026 {NOW} AEST)',1)
    (D/f).write_text(x)

# findings prepend
fd=(D/'findings.md').read_text()
block=(f"## v26 findings (3 Nov 2026 {NOW} AEST)\n"
 "- Archivist v014 and Arbiter v011 are LIVE; no structural edge change.\n"
 "- Five retired-bot agent folders were deleted by Gem (Arbiter chat t68u: \"I did, my bad\"); R-056 point 2 closed 3 Nov 6:05am. Codex folders kept.\n"
 "- Engineer's claimed 154-file GitHub restore: path list was not recorded in governance notes; cannot confirm whether any restored path sits under /workspace/governance/.\n\n")
if '## v26 findings' not in fd:
    # insert after title line
    lines=fd.splitlines(True)
    # keep first heading, then block
    i=1
    while i < len(lines) and lines[i].startswith('#'):
        i+=1
    # after blank following title
    while i < len(lines) and lines[i].strip()=='':
        i+=1
    fd=''.join(lines[:i])+block+''.join(lines[i:])
    (D/'findings.md').write_text(fd)
print('ok', NOW)

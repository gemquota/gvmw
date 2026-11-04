# Author: P1 (Roles) Archivist (61ef3abd-87b8-49f1-b8d6-b52969afa315), written ~8:01am AEST 4 Nov 2026
# Role map v27 (4 Nov 2026): Engineer v010 RECORDED (Imitator RECORD ONLY ~7:58am; not deployed; live still v009).
import json,sys,re
from pathlib import Path
D=Path('/workspace/governance/cartography'); NOW=sys.argv[1]; CX='/workspace/governance/codex/'
g=json.loads((D/'role-graph.json').read_text()); K={n['key']:n for n in g['nodes']}
# ENG: highest recorded v010; live remains v009
n=K['ENG']
n['codex']=f'{CX}codey/v010.md'
n['live_codex']=f'{CX}codey/v009.md'
prefix=(
    "RECORDED v010 (Imitator RECORD ONLY 4 Nov 2026 ~7:58am AEST, text hash be2410c9e732; "
    "AO-2026-11-04-imitator-codey-v010; not deployed — \"Don't deploy without a separate say-so.\"). "
    "Live profile still runs v009. Narrows risk only: relayed approvals never for repo settings; "
    "no gh auth token; no new public governance-master without Gem + dry run; no overwrite of "
    "/workspace/governance from GitHub. Earlier: "
)
n['note']=prefix+n['note']
g['previous_version']=g['version']
OLD=g['version']  # 'v26, 3 Nov 2026 8:01am AEST'
g['version']=f'v27, 4 Nov 2026 {NOW} AEST'
note=g['sources'].get('note','')
g['sources']['note']=note+f" 4 Nov {NOW}: Engineer v010 RECORDED (not deployed; live v009)."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")

def vers(s):
    # Keep live label v009; annotate RECORDED on identity-work detail
    s=s.replace(
        'ENG["Engineer v009 · LIVE · only GitHub writer · Vercel = public deploy"]',
        'ENG["Engineer v009 · LIVE · v010 RECORDED · only GitHub writer · Vercel = public deploy"]'
    )
    return s

s=vers((D/'role-map.mmd').read_text())
repls=[
 (f'Role map v26, 3 Nov 2026 8:01am AEST',f'Role map v27, 4 Nov 2026 {NOW} AEST'),
 ('%% v26: Archivist v014 LIVE (Gem Yes t105u); Arbiter v011 kept by Gem; R-056 pt2 folders. v25: ',
  '%% v27: Engineer v010 RECORDED (not deployed; live v009). v26: Archivist v014 LIVE (Gem Yes t105u); Arbiter v011 kept by Gem; R-056 pt2 folders. v25: '),
 ('<b>Legend v26</b>','<b>Legend v27</b>'),
 ('green = added in v11–v26','green = added in v11–v27'),
]
for a,b in repls:
    assert s.count(a)==1, repr(a); s=s.replace(a,b)
(D/'role-map.mmd').write_text(s)

for p in ['role-map-detail-governance.mmd','role-map-detail-identity-work.mmd','role-map-detail-connectors.mmd']:
    t=vers((D/p).read_text())
    a='Role map v26 (3 Nov 2026 8:01am'
    assert t.count(a)==1,(p,a)
    t=t.replace(a,f'Role map v27 (4 Nov 2026 {NOW}')
    (D/p).write_text(t)

Vt=(f"## v27 — 4 Nov 2026 {NOW} AEST (current)\n"
    "Engineer v010 RECORDED (Imitator RECORD ONLY ~7:58am AEST 4 Nov; text be2410c9e732; "
    "AO-2026-11-04-imitator-codey-v010). Not deployed — live remains v009 (phase-cleanup 22 Oct). "
    "Tightens settings / token / public governance-master / governance-restore limits only. "
    "No edge change. v1–v26 kept as `*-vN.*`.\n\n")
for f in ['summaries.md','README.md']:
    x=(D/f).read_text(); k=x.index('## v26 — '); x=x[:k]+Vt+x[k:].replace(' (current)','',1)
    if f=='summaries.md':
        x=x.replace('(role map v26, 3 Nov 2026 8:01am AEST)',f'(role map v27, 4 Nov 2026 {NOW} AEST)',1)
        # bump Engineer heading codex pointer in body (historical v007 heading left as history; add note under it)
        marker='### P5 (Work) Engineer — `f8e3fdc6` — codey/v007\n'
        if marker in x and 'v010 RECORDED' not in x.split(marker,1)[1][:400]:
            insert=('- **v010 RECORDED 4 Nov ~8:01am (Imitator RECORD ONLY; not deployed; live still v009):** '
                    'relayed approvals never for repo settings; no `gh auth token`; no new public governance-master '
                    'without Gem + dry run; no overwrite of /workspace/governance from GitHub.\n')
            # insert after the heading line's following description line block — after first content line
            parts=x.split(marker,1)
            rest=parts[1]
            # after first paragraph line
            nl=rest.find('\n')
            rest2=rest[:nl+1]+insert+rest[nl+1:]
            x=parts[0]+marker+rest2
    if f=='README.md':
        # note interactive rebuild in the new section
        Vt_readme = Vt.rstrip('\n') + "\n- Interactive view rebuilt from v27: `role-map-interactive.html`.\n\n"
        # We already inserted Vt; replace the just-inserted block's trailing \n\n with the extended one once
        x=x.replace(Vt, Vt_readme, 1)
    (D/f).write_text(x)

# findings prepend
fd=(D/'findings.md').read_text()
block=(f"## v27 findings (4 Nov 2026 {NOW} AEST)\n"
 "- Engineer v010 RECORDED (Imitator RECORD ONLY); live profile still v009. No deploy.\n"
 "- Diff v009→v010 narrows Engineer only (settings / token / public governance-master / no governance overwrite from GitHub). "
 "Does not touch Imitator, Investigator, Scorer, Scrutineer, Safekeeper, Safeguard, or a shared rule they own; does not widen Imitator (R-028); no spend / irreversible.\n"
 "- Approval-time discrepancy noted (Imitator's logged 7:58am is after the ~7:57am 1:1 message to Archivist); does not block recording.\n"
 "- No structural edge change.\n\n")
if '## v27 findings' not in fd:
    lines=fd.splitlines(True)
    i=1
    while i < len(lines) and lines[i].startswith('#'):
        i+=1
    while i < len(lines) and lines[i].strip()=='':
        i+=1
    fd=''.join(lines[:i])+block+''.join(lines[i:])
    (D/'findings.md').write_text(fd)
print('ok', NOW)

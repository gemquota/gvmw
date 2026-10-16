# Role map v11 (16 Oct 2026 ~11:20am AEST): patch v10 -> v11 after Gem's 11:02am/11:03am batch deployed 11:06:44-11:08:50.
import json,re
from pathlib import Path
D=Path('/workspace/governance/cartography'); CX='/workspace/governance/codex/'
NEW={'SCO':'assessor/v004','SCR':'auditor/v004','SFK':'secrets-credentials-custodian/v005','IMI':'clone/v006','INF':'identity-inferer/v005',
     'ARC':'codex-keeper/v007','EXP':'explorer-copy/v004','MED':'connector-steward/v006','EMI':'grok-bot/v006','ENG':'codey/v007','EXT':'scraper/v005','SFG':'compliance-risk-officer/v006'}
LIVE_AT={'SCO':'11:06:44','SCR':'11:06:49','SFK':'11:06:58','IMI':'11:07:06','INF':'11:07:23','ARC':'11:07:36','EXP':'11:07:52','MED':'11:08:08','EMI':'11:08:15','ENG':'11:08:25','EXT':'11:08:42','SFG':'11:08:50'}
WHAT={'SCO':"phases.md sets the live set; checks pushes as well as commits",
 'SCR':"role map and reviews go to Archivist; R-015 sentence (closes the Assembler watch item)",
 'SFK':"other bots propose edits to its files",
 'IMI':"one decision-log file (R-024)",
 'INF':"one owner-only running-profile file, no shared copies (J5); the existing shared copy is left for Gem",
 'ARC':"owns directory.md (D1); names the five R-027 checkers",
 'EXP':"hands directory.md to Archivist, keeps phases.md; RR-028 line",
 'MED':"connector health list; acceptance of a new integration is Gem's (J4); cites connector limits",
 'EMI':"the only postiz poster (J1), posting only text Gem approved word for word; cites connector limits",
 'ENG':"Vercel deployments treated as public pushes; cites connector limits",
 'EXT':"BIE data stays on the box; cites connector limits",
 'SFG':"dry-run list covers the new connectors; owns the shared connector limits"}
BATCH={k:('11:02am' if k in('SCO','SCR','SFK','IMI','INF','ARC') else '11:03am') for k in NEW}; BATCH['EXP']='11:02am + 11:03am'
g=json.loads((D/'role-graph.json').read_text())
old2new={}
for n in g['nodes']:
    k=n.get('key')
    if k in NEW:
        old=n['codex'].split('/codex/')[1]; old2new[old]=NEW[k]+'.md'
        n['codex']=CX+NEW[k]+'.md'; n['live_codex']=CX+NEW[k]+'.md'; n.pop('pending',None)
        n['note']=n['note'].rstrip()+f" v{NEW[k][-3:]} (Gem {BATCH[k]}, 16 Oct; live since {LIVE_AT[k]}): {WHAT[k]}."
for e in g['edges']:
    e['source']=[old2new.get(s.split('/codex/')[-1],None) and CX+old2new[s.split('/codex/')[-1]] or s for s in e['source']]
ids={n['key']:n['id'] for n in g['nodes']}; nm={n['key']:n['name'] for n in g['nodes']}
def add(f,t,rel,src,flow=None):
    e={'from':ids[f],'from_name':nm[f],'to':ids[t],'to_name':nm[t],'relation':rel,'source':[CX+s for s in src],'status':'current'}
    if flow: e['flow']=flow
    g['edges'].append(e)
add('EXP','ARC',"phases.md feeds directory.md (Archivist owns directory.md from v007; Explorer keeps phases.md)",['codex-keeper/v007.md','explorer-copy/v004.md'])
add('MED','GEM',"sends new integrations for acceptance (Gem's call, J4)",['connector-steward/v006.md','_shared/connector-limits/v001.md'],flow='approval')
add('GEM','EMI',"approves exact post text; Emissary is the only postiz poster (RR-028, J1)",['grok-bot/v006.md','_shared/connector-limits/v001.md'],flow='approval')
g['previous_version']=g['version']; g['version']='v11, 16 Oct 2026 ~11:20am AEST'
g['stats']['edges']=len(g['edges'])
g['sources']['note']=("Descriptive only, from latest codex + phases.md. 17 active (14 live, 3 dormant P5). P3 and P4 LIVE since 15 Oct 2026, 11:30pm AEST. "
 "16 Oct: Imitator's first 6 approvals deployed 09:14 on Gem's 9:13am words; Gem's 11:02am and 11:03am approvals (12 versions) recorded first (R-029) and deployed 11:06:44–11:08:50. "
 "R-027: changes to Imitator or its checkers (Investigator, Scorer, Scrutineer, Safekeeper, Safeguard) are Gem-only; R-028: Imitator can't approve widening its own role. "
 "Connector limits (shared, owner Safeguard; RR-028): Emissary is the only postiz poster. Archivist owns directory.md (v007). Voice approvals count (R-018); public/shared repo pushes go to Safeguard first (R-020).")
g['rules']['connector_limits']="Shared rule _shared/connector-limits/v001 (Gem 11:03am, 16 Oct; owner Safeguard): applies to every bot and helper. Only Emissary posts via postiz, and only text Gem approved word for word. New connectors need Gem's direct words and a Safeguard dry run first. Vercel deploys count as public pushes."
g['rules']['message_verification']="Shared rule _shared/message-verification-rule/v003 (Gem 11:02am, 16 Oct)."
g['rules']['r028_r029']="R-028: Imitator can't approve changes that widen its own role (architect-v004's routing and cap confirmed by Gem before 11:02am, 16 Oct). R-029: Gem's chat words authorise; they're recorded before any deploy."
g['rules']['directory']="Archivist owns /workspace/governance/directory.md from codex-keeper v007 (live 11:07:36, 16 Oct); Explorer keeps phases.md, which directory.md follows (R-021)."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")
print('edges',len(g['edges']),'remapped',len(old2new))

# overview mmd
m=(D/'role-map.mmd').read_text()
R=[('Role map v10, 16 Oct 2026 ~9:22am AEST','Role map v11, 16 Oct 2026 ~11:20am AEST'),
 ('%% v10: ',"%% v11: Gem's 11:02am + 11:03am batches deployed 11:06–11:08 (12 versions); connector limits (owner Safeguard), Emissary only poster, Archivist owns directory.md. v10: "),
 ('<b>Legend v10</b>','<b>Legend v11</b>'),
 ('ARC["Archivist<br/>codex + role map"]','ARC["Archivist v007<br/>codex + role map + directory.md"]'),
 ('SCO["Scorer"]','SCO["Scorer v004"]'),
 ('SFG["Safeguard v005<br/>repo pushes reviewed first"]','SFG["Safeguard v006<br/>repo pushes reviewed first<br/>owns connector limits"]'),
 ('SFK["Safekeeper"]','SFK["Safekeeper v005"]'),
 ('EXP["Explorer 04dcca0d<br/>ACTIVE"]','EXP["Explorer v004 04dcca0d<br/>ACTIVE · keeps phases.md"]'),
 ('SCR["Scrutineer"]','SCR["Scrutineer v004"]'),
 ('INF["Inferer v004"]','INF["Inferer v005"]'),
 ('MED["Mediator v005"]','MED["Mediator v006<br/>live name still P4"]'),
 ('IMI["Imitator v005 · LIVE','IMI["Imitator v006 · LIVE'),
 ('no changes to Imitator/Investigator"]','no changes to Imitator or its checkers"]'),
 ('EMI["Emissary"]','EMI["Emissary v006<br/>only postiz poster"]'),
 ('ENG["Engineer v006"]','ENG["Engineer v007"]'),
 ('EXT["Extractor"]','EXT["Extractor v005"]'),
 ('IMI ==>|approves, live, 6 deployed 16 Oct| ARC','IMI ==>|approves within limits, 6 deployed 9:14am 16 Oct| ARC'),
 ('Imitator/Investigator changes"))','changes to Imitator or its checkers"))'),
 ('blue dashed = checks Imitator, R-027<br/>','blue dashed = checks Imitator, R-027<br/>green = added in v11<br/>')]
for a,b in R:
    assert m.count(a)==1,a; m=m.replace(a,b)
m=m.rstrip('\n')+"\n  EXP -->|phases.md feeds directory.md| ARC\n  MED ==>|new integrations: Gem accepts| GEM\n  GEM ==>|exact post text| EMI\n  linkStyle 41,42,43 stroke:#2e7d32,stroke-width:2px\n"
(D/'role-map.mmd').write_text(m)
n_links=len(re.findall(r'(-->|==>|-\.->|~~~)',m)); print('mmd links',n_links)

gv=(D/'role-map-detail-governance.mmd').read_text()
for a,b in [('Role map v10 (16 Oct 2026 ~9:22am)','Role map v11 (16 Oct 2026 ~11:20am)'),('ARC["Archivist v006"]','ARC["Archivist v007 · owns directory.md"]'),
 ('SCO["Scorer"] --> SCR["Scrutineer"]','SCO["Scorer v004"] --> SCR["Scrutineer v004"]'),('SFG["Safeguard v005<br/>','SFG["Safeguard v006 · owns connector limits<br/>'),
 ('SFK["Safekeeper"]','SFK["Safekeeper v005"]'),('IMI["Imitator · LIVE since 11:30pm"]','IMI["Imitator v006 · LIVE since 11:30pm"]'),
 ('Imitator/Investigator Gem-only| GEM','Imitator + checkers Gem-only · not widening own role R-028| GEM'),('MED["Mediator"]','MED["Mediator v006"]'),
 ('urgent cost alerts, v005| GEM','urgent cost alerts| GEM')]:
    assert gv.count(a)==1,a; gv=gv.replace(a,b)
gv=gv.rstrip('\n')+"\n  MED ==>|new integrations: Gem accepts, J4| GEM\n  ALL[\"Every bot and helper\"] -->|connector limits, RR-028| SFG\n"
(D/'role-map-detail-governance.mmd').write_text(gv)
iw=(D/'role-map-detail-identity-work.mmd').read_text()
for a,b in [('Role map v10 (16 Oct 2026 ~9:22am)','Role map v11 (16 Oct 2026 ~11:20am)'),('INF["Inferer v004"]','INF["Inferer v005 · one owner-only profile file"]'),
 ('IMI["Imitator v005 · LIVE','IMI["Imitator v006 · LIVE'),('EXP["Explorer v002 04dcca0d ACTIVE"]','EXP["Explorer v004 04dcca0d ACTIVE"]'),
 ('EMI["Emissary"]','EMI["Emissary v006 · only postiz poster"]'),('ENG["Engineer v006"]','ENG["Engineer v007 · Vercel = public push"]'),
 ('EXT["Extractor"]','EXT["Extractor v005 · BIE data stays on box"]')]:
    assert iw.count(a)==1,a; iw=iw.replace(a,b)
iw=iw.rstrip('\n')+"\n  GEM ==>|exact post text| EMI\n"
(D/'role-map-detail-identity-work.mmd').write_text(iw)

# summaries
s=(D/'summaries.md').read_text()
s=s.replace('# Bot summaries (role map v10, 16 Oct 2026 ~9:22am AEST)','# Bot summaries (role map v11, 16 Oct 2026 ~11:20am AEST)',1)
V11=("## v11 — 16 Oct 2026 ~11:20am AEST (current)\n"
"Rebuilt after Gem's 11:02am and 11:03am approvals (in Archivist's chat; recorded before deploying, R-029) were deployed 11:06:44–11:08:50 AEST. Descriptive only; v1–v10 kept as `*-vN.*`. **17 active (14 live, 3 dormant)** + 9 former/retired nodes, %d edges.\n"
"- LIVE now: Scorer v004, Scrutineer v004, Safekeeper v005, Imitator v006, Inferer v005, Archivist v007, Explorer v004, Mediator v006, Emissary v006, Engineer v007, Extractor v005, Safeguard v006. No pending versions.\n"
"- New shared rules: connector limits v001 (owner Safeguard; Emissary is the only postiz poster) and message verification v003.\n"
"- Archivist owns directory.md; Explorer keeps phases.md. Mediator's new-integration acceptance is Gem's (J4).\n"
"- R-028 settled: Gem confirmed architect-v004's routing and cap before 11:02am. Assembler watch item closed for all four bots.\n\n")%len(g['edges'])
s=s.replace('## v10 — 16 Oct 2026 ~9:22am AEST (current)',V11+'## v10 — 16 Oct 2026 ~9:22am AEST',1)
for k,f in NEW.items():
    old=[o for o,nw in old2new.items() if nw==f+'.md'][0][:-3]
    hdr=re.search(r'^### .*`%s`.*$'%ids[k][:8],s,re.M).group(0)
    s=s.replace(hdr,hdr.replace(old,f),1)
    # bullet after the heading's paragraph block
    idx=s.index(hdr.replace(old,f)); nxt=s.find('\n\n',idx)
    s=s[:nxt]+f"\n- v{f[-3:]} (Gem {BATCH[k]}, 16 Oct; live since {LIVE_AT[k]}): {WHAT[k]}."+s[nxt:]
s=s.replace("- **Awaiting Gem (R-028):** the Imitator-only routing and the A5c cap. Imitator withdrew its approval at 9:24am, and v004 stays live. Until Gem confirms, any proposal may go to Gem, and the cap can't hold back Gem's requests or safety fixes.",
 "- R-028 items confirmed by Gem before 11:02am, 16 Oct (\"Yes, I confirm both: the routing to Imitator and the 3-a-week cap\"); no text change.",1)
s=s.replace("- Never: spending; anything drastic or irreversible, such as deletions or public/shared repo pushes; changes to Imitator or Investigator (Gem only, R-015).","- Never: spending; anything drastic or irreversible, such as deletions or public/shared repo pushes; changes to Imitator or its five checkers (Gem only, R-015, R-027); changes that widen its own role (R-028).",1)
(D/'summaries.md').write_text(s)

rd=(D/'README.md').read_text()
rd=rd.replace('## v10 — 16 Oct 2026 ~9:22am AEST (current)',V11.replace('summaries','summaries')+"- Interactive view rebuilt from v11: `role-map-interactive.html`.\n\n## v10 — 16 Oct 2026 ~9:22am AEST",1)
(D/'README.md').write_text(rd)
fd=(D/'findings.md').read_text()
F=("## v11 findings (16 Oct 2026 ~11:20am AEST)\n"
"- All 12 versions from Gem's 11:02am and 11:03am approvals are live (byte-checked; verify 17/37, 0 pending). Gem's words were recorded before deploying (R-029). Scrutineer check requested.\n"
"- Explorer went from v002 to v004; v003 (directory handover) was recorded but never deployed on its own.\n"
"- Mediator's live name is still \"P4 (Ops) Mediator\" while phases.md says P2. The rename wasn't part of connector-steward v006; it needs its own approval.\n"
"- Inferer v005 keeps one owner-only profile file. The older shared copy `/workspace/id-notes/gem-profile.md` (mode 644) is still there, left for Gem to decide (J5).\n"
"- Safeguard's interim limits in `connectors.md` still stand alongside the new shared connector limits; they should point to the shared rule.\n"
"- directory.md had stale entries (folders it said were still on the box, the 9 Oct merges shown as unapplied, Investigator named as the only checker of Imitator); Archivist fixed them when taking ownership.\n\n")
fd=fd.replace('## v10 findings',F+'## v10 findings',1)
(D/'findings.md').write_text(fd)

# --- second pass (v11): refresh stale citations and labels
g=json.loads((D/'role-graph.json').read_text())
cur={n['codex'].split('/codex/')[1].split('/')[0]:n['codex'] for n in g['nodes'] if n.get('map_status')=='active'}
for e in g['edges']:
    out=[]
    for s_ in e['source']:
        rel=s_.split('/codex/')[-1]; fold=rel.split('/')[0]
        out.append(cur[fold] if '/codex/' in s_ and fold in cur else s_)
    e['source']=list(dict.fromkeys(out))
    if e['relation'].endswith("Imitator-only routing awaits Gem's confirmation (R-028), so Architect may still send any proposal to Gem"):
        e['relation']=e['relation'].replace("Imitator-only routing awaits Gem's confirmation (R-028), so Architect may still send any proposal to Gem","Imitator-only routing and 3-a-week cap confirmed by Gem before 11:02am, 16 Oct (R-028)")
    if e['relation']=="urgent cost alerts straight to (v005)": e['relation']="urgent cost alerts straight to"
for n in g['nodes']:
    if n['key']=='GEM': n['note']=n['note'].replace("changes to Imitator or Investigator stay Gem-only.","changes to Imitator or its five checkers (R-027) stay Gem-only; Gem also approves exact post text for Emissary and accepts new integrations.")
g['rules']['inquirers']=g['rules']['inquirers'].replace('(Safeguard v005)','(Safeguard v006)')
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")
print('pass2 ok')
# third pass (applied 11:16am): ARX node note updated for Gem's R-028 confirmation (see role-graph.json).

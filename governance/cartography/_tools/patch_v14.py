# Role map v14 (16 Oct 2026 ~4:05pm AEST): shared connector-limits v002 recorded (Gem 3:54pm, default text d4fbfa8f391f). Only what v002 says about who uses which connector.
import json,re
from pathlib import Path
D=Path('/workspace/governance/cartography'); CX='/workspace/governance/codex/'; CL=CX+'_shared/connector-limits/v002.md'
# connector -> (who may use / write, per v002 rule number). Wording kept close to the codex.
CONN=[
 ('postiz','1, 6','Only Emissary posts, text Gem approved word for word; Safeguard dry run before every post. No public posting through any other tool.'),
 ('Vercel (both connections)','2','Any production or public deploy needs Gem\'s words for that deploy; a Safeguard dry run alone is never enough (R-037).'),
 ('Google Drive, Sheets','3','No upload, copy or sharing without Gem\'s words for that file; private by default.'),
 ('Google Calendar','4','Events involving anyone other than Gem need Gem\'s words.'),
 ('Zapier, n8n','7','Engineer builds; any bot runs read-only lookups; any acting step needs Gem\'s words and a Safeguard dry run; Mediator tracks quota. n8n not working.'),
 ('Supabase','8','Engineer only; others ask Engineer; Mediator reads health and spend. Writes need Gem\'s words and a dry run.'),
 ('Notion, Todoist','9','Any bot reads. Emissary, Explorer, Extractor and Engineer write private items only for work Gem asked for directly (not Imitator-approved). Sharing needs Gem\'s words and a dry run.'),
 ('Exa','10','Any bot, for its task; over 50 calls or a loop goes to Mediator first.'),
 ('Memory stores (Mem0 etc.)','11','Any bot searches; no writers until Mem0 works and Gem names one.'),
 ('Jupyter, papermill, Obsidian','12','Any bot, on the box; git pushes are GitHub actions (rule 14).'),
 ('All connectors: deletions','13','Gem\'s words naming the item, a Safeguard dry run and a backup first; Imitator can\'t approve.'),
 ('GitHub (GitHub-xai, cursor-origin, git, gh)','14','Shared GitHub rule (not yet recorded); until then any write needs Gem\'s words and a dry run. Engineer is the only GitHub writer. GitHub-xai read-only until T-016 is confirmed.'),
 ('Gmail (all accounts)','15','Any bot reads what its task needs. Sends need Gem\'s words and a dry run; Imitator may approve a no-promises first reply to a new contact (R-038), still dry-run.'),
 ('Google Docs, Slides','16','Private files for Gem\'s work, logged by the bot; other files need Gem\'s words.'),
 ('Apify','17','Extractor runs actors; every run needs Gem\'s words for the spend and Mediator\'s check; any bot searches the store.'),
 ('Context7, X','18','Read-only; any bot, for its task.'),
 ('Keys; Finance, Adapter','19','Safekeeper records key locations (never values); Finance linking is Gem\'s, with Safekeeper.'),
 ('Unnamed / new connectors','5','Gem\'s words and a Safeguard dry run for any send, post, share, upload, deploy or purchase.'),
]
BOT={ # bullet per bot, from v002 RELATIONSHIPS and rules
 'SFG':"Connector limits v002: owns the rule, does the dry runs it calls for (posts, deploys, workflows, Supabase, Notion/Todoist sharing, Gmail sends, deletions) and checks for breaches.",
 'SFK':"Connector limits v002: owns how connector secrets are stored and records key locations, never values (rule 19); Finance linking with Gem.",
 'MED':"Connector limits v002: installs connectors when Gem asks and tells Safeguard the same day; keeps connectors.md; read-only health checks; spend checks for Zapier quota, Supabase, Exa loops and every Apify run.",
 'ENG':"Connector limits v002: builds Zapier/n8n workflows (read-only ones on only after Safeguard replies), only Supabase user, only GitHub writer; may write private Notion/Todoist items for Gem's direct work.",
 'EXT':"Connector limits v002: runs Apify actors (Gem's words for each run's spend plus Mediator's check); may write private Notion/Todoist items for Gem's direct work.",
 'EMI':"Connector limits v002: the only postiz poster (Safeguard dry run every post); may write private Notion/Todoist items for Gem's direct work.",
 'EXP':"Connector limits v002: may write private Notion/Todoist items for work Gem asked for directly (Gem's question 2: yes).",
 'IMI':"Connector limits v002: may approve a no-promises first reply to a new contact (rule 15, R-038), still dry-run by Safeguard; can't approve deletions or spending.",
 'ARX':"Connector limits v002: drafts changes to the rule; Gem alone approves (R-027).",
 'ARC':"Connector limits v002: records changes to the rule on Gem's words.",
}
g=json.loads((D/'role-graph.json').read_text())
ids={n['key']:n['id'] for n in g['nodes']}; nm={n['key']:n['name'] for n in g['nodes']}
for n in g['nodes']:
    if n['key'] in BOT: n['note']=n['note'].rstrip()+' '+BOT[n['key']]
def add(f,t,rel):
    g['edges'].append({'from':ids[f],'from_name':nm[f],'to':ids[t],'to_name':nm[t],'relation':rel,'source':[CL],'status':'current'})
add('MED','SFG',"tells the same day about each connector installed (connector limits v002, RELATIONSHIPS)")
add('EXT','MED',"asks for a spend check before every Apify run (connector limits v002, rule 17)")
add('ENG','SFG',"sends workflows and Supabase writes for a dry run first (connector limits v002, rules 7 and 8)")
add('IMI','SFG',"sends any first reply it approves for a dry run (connector limits v002, rule 15)")
g['connectors']={'source':CL,'approved':"Gem, directly in Archivist's chat 16 Oct 2026 3:54pm AEST (default text d4fbfa8f391f, not variant B)",
  'cited_by':['Emissary','Engineer','Explorer','Extractor','Mediator','Safeguard'],
  'no_pointer_yet':['Inquirer','Scorer','Arbiter','Architect','Safekeeper','Archivist','Imitator','Inferer','Scrutineer','Mender','Investigator'],
  'rules':[{'connector':c,'rule':r,'who':w} for c,r,w in CONN]}
g['rules']['connector_limits']=("Shared rule _shared/connector-limits/v002 (Gem 3:54pm, 16 Oct; owner Safeguard; covers every connector and account). Only Emissary posts (postiz). Engineer: only Supabase user, only GitHub writer, builds workflows. "
 "Extractor runs Apify (Gem's words per run plus Mediator's spend check). Emissary, Explorer, Extractor and Engineer may write private Notion/Todoist items for Gem's direct work. "
 "Gmail sends need Gem's words and a dry run; Imitator may approve a no-promises first reply (R-038). No memory writers yet. Deletions need Gem's words, a dry run and a backup.")
g['previous_version']=g['version']; g['version']='v14, 16 Oct 2026 ~4:05pm AEST'; g['stats']['edges']=len(g['edges'])
g['sources']['note']+=" 3:54pm: connector limits v002 recorded (Gem directly; shared rule, no profile): who uses which connector, per its rules 1–19."
(D/'role-graph.json').write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n"); print('edges',len(g['edges']))

# new detail diagram: connectors (descriptive, from v002 only)
L=['%%{init: {"flowchart": {"wrappingWidth": 220}}}%%','%% Role map v14 (16 Oct 2026 ~4:05pm) detail C — connectors, from shared connector limits v002 only (Gem 3:54pm)','flowchart LR',
 '  SFG["Safeguard v006<br/>owns connector limits v002<br/>dry runs + breach checks"]','  SFK["Safekeeper<br/>key locations, rule 19"]','  MED["Mediator<br/>installs, connectors.md, spend"]',
 '  ENG["Engineer"]','  EXT["Extractor"]','  EMI["Emissary"]','  EXP["Explorer"]','  IMI["Imitator"]','  ANY["Any bot"]','  GEM(("Gem"))',
 '  C1[/"postiz"/]','  C2[/"Supabase"/]','  C3[/"Zapier · n8n"/]','  C4[/"GitHub"/]','  C5[/"Apify"/]','  C6[/"Notion · Todoist"/]','  C7[/"Gmail"/]',
 '  C8[/"Exa · Context7 · X · Jupyter · Obsidian"/]','  C9[/"Memory stores"/]','  C10[/"Vercel · Drive · Sheets · Calendar · Docs · Slides"/]',
 '  EMI -->|only poster, rule 1| C1','  ENG -->|only user, rule 8| C2','  ENG -->|builds workflows, rule 7| C3','  ANY -.->|read-only lookups| C3',
 '  ENG -->|only writer, rule 14| C4','  EXT -->|runs actors, rule 17| C5','  EXT -->|spend check first| MED',
 '  EMI -->|private writes, rule 9| C6','  EXP -->|private writes, rule 9| C6','  EXT -->|private writes, rule 9| C6','  ENG -->|private writes, rule 9| C6','  ANY -.->|read| C6',
 '  ANY -.->|read for task; drafts| C7','  IMI -->|no-promises first reply, R-038| C7','  ANY -.->|own task| C8','  ANY -.->|search only; no writers| C9',
 '  ANY -.->|per Gem\'s words, rules 2-4, 16| C10',
 '  GEM ==>|sends, shares, deploys, spend, deletions| ANY','  ANY -->|dry run first| SFG','  MED -->|new connector, same day| SFG','  SFK -.->|key locations| SFG']
(D/'role-map-detail-connectors.mmd').write_text('\n'.join(L)+'\n')

def sub(path,pairs,tail=''):
    s=(D/path).read_text()
    for a,b in pairs: assert s.count(a)==1,(path,a); s=s.replace(a,b)
    (D/path).write_text(s.rstrip('\n')+'\n'+tail)
sub('role-map.mmd',[('Role map v13, 16 Oct 2026 ~11:52am AEST','Role map v14, 16 Oct 2026 ~4:05pm AEST'),
 ('%% v13: ','%% v14: connector limits v002 recorded (Gem 3:54pm); who uses which connector in detail C (role-map-detail-connectors). v13: '),
 ('<b>Legend v13</b>','<b>Legend v14</b>'),('Detail PNGs: governance, identity-work','Detail PNGs: governance, identity-work, connectors'),
 ('green = added in v11/v12<br/>','green = added in v11–v14<br/>')],
 "  EXT -->|Apify spend check| MED\n  MED -->|new connector, same day| SFG\n  linkStyle 46,47 stroke:#2e7d32,stroke-width:2px\n")
for f in ['role-map-detail-governance.mmd','role-map-detail-identity-work.mmd']:
    sub(f,[('Role map v13 (16 Oct 2026 ~11:52am; P5 live)','Role map v14 (16 Oct 2026 ~4:05pm; P5 live)')])
sub('role-map-detail-governance.mmd',[('SFG["Safeguard v006 · owns connector limits<br/>','SFG["Safeguard v006 · owns connector limits v002<br/>')])

s=(D/'summaries.md').read_text()
s=s.replace('# Bot summaries (role map v13, 16 Oct 2026 ~11:52am AEST)','# Bot summaries (role map v14, 16 Oct 2026 ~4:05pm AEST)',1)
V=("## v14 — 16 Oct 2026 ~4:05pm AEST (current)\n"
"Rebuilt after shared connector limits v002 was recorded on Gem's 3:54pm words in Archivist's chat (default text d4fbfa8f391f, not variant B; shared document, no profile to deploy; Scrutineer's check requested). Descriptive only, from v002's text; v1–v13 kept as `*-vN.*`. **17 active, all live** + 9 former/retired nodes, %d edges.\n"
"- New detail diagram `role-map-detail-connectors` and a `connectors` table in role-graph.json: who may use which connector under rules 1–19.\n"
"- Engineer: only Supabase user and GitHub writer, builds Zapier/n8n workflows. Extractor: runs Apify, with Mediator's spend check. Emissary: only postiz poster. Emissary, Explorer, Extractor and Engineer may write private Notion/Todoist items for Gem's direct work. No memory writers. Gmail sends need Gem's words; Imitator may approve a no-promises first reply (R-038).\n"
"- 4 new edges: Mediator → Safeguard (new connectors), Extractor → Mediator (Apify spend), Engineer → Safeguard (workflow/Supabase dry runs), Imitator → Safeguard (first-reply dry run).\n"
"- Cited by 6 live briefs (Emissary, Engineer, Explorer, Extractor, Mediator, Safeguard); 11 have no pointer yet.\n\n")%len(g['edges'])
s=s.replace('## v13 — 16 Oct 2026 ~11:52am AEST (current)',V+'## v13 — 16 Oct 2026 ~11:52am AEST',1)
for k,b in BOT.items():
    hdr=re.search(r'^### .*`%s`.*$'%ids[k][:8],s,re.M).group(0); i=s.index(hdr); j=s.find('\n\n',i)
    s=s[:j]+"\n- "+b+s[j:]
(D/'summaries.md').write_text(s)
r=(D/'README.md').read_text(); r=r.replace('## v13 — 16 Oct 2026 ~11:52am AEST (current)',V+"- Interactive view rebuilt from v14: `role-map-interactive.html`.\n\n## v13 — 16 Oct 2026 ~11:52am AEST",1); (D/'README.md').write_text(r)
f_=(D/'findings.md').read_text()
F=("## v14 findings (16 Oct 2026 ~4:05pm AEST)\n"
"- Connector limits v002 is recorded on Gem's 3:54pm words (default text, not variant B). Nothing to deploy; Scrutineer's check requested.\n"
"- 11 live briefs have no pointer to connector limits (Inquirer, Scorer, Arbiter, Architect, Safekeeper, Archivist, Imitator, Inferer, Scrutineer, Mender, Investigator). The rule still binds every bot by its SCOPE, but the briefs don't say so.\n"
"- Rule 14 points to a shared GitHub rule at `codex/_shared/github/` that isn't recorded yet, so its interim line applies (any GitHub write needs Gem's words and a dry run).\n"
"- Emissary's pointer lists only Vercel, Drive, Sheets and Calendar, though v002 makes it a main Gmail, Docs and Notion user.\n"
"- Mediator's connectors.md line 40 and Safeguard's input paraphrase rule 5 differently from the recorded text.\n\n")
f_=f_.replace('## v13 findings',F+'## v13 findings',1); (D/'findings.md').write_text(f_)

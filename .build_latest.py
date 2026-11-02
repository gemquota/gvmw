import os,re,json,glob,hashlib
G='/workspace/governance'; W='/workspace/watchdog'
def rd(p): return open(p,encoding='utf-8',errors='replace').read()
EMAIL=re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
PHONE=re.compile(r'(?<![\w.])(?:\+?61[\s-]?\d|0[2-478])(?:[\s-]?\d){8}(?!\w)')
TOK=re.compile(r'\b(ghp_|gho_|ghs_|github_pat_|xox[abp]-|AKIA|sk-(?!shaped|officer))[A-Za-z0-9_\-]{8,}')
KV=re.compile(r'(?i)\b(password|passwd|api[_ -]?key|secret|token)(\s*[:=]\s*)(["\']?)[A-Za-z0-9_\-\.]{16,}')
red={'n':0}
def scrub(t):
    def r(m): red['n']+=1; return '[redacted]'
    t=EMAIL.sub(r,t); t=PHONE.sub(r,t); t=TOK.sub(r,t)
    t=KV.sub(lambda m:(red.__setitem__('n',red['n']+1) or m.group(1)+m.group(2)+'[redacted]'),t)
    return t
index=[]  # (path, version, used_in)
CUR={'lvl':1}
def demote(t,base):
    out=[];fence=None;minl=None
    lines=t.split('\n')
    for l in lines:
        m=re.match(r'^(`{3,}|~{3,})',l)
        if m:
            if fence is None: fence=m.group(1)[0]*len(m.group(1))
            elif l.startswith(fence): fence=None
            continue
        if fence is None:
            h=re.match(r'^(#{1,6})\s',l)
            if h: minl=len(h.group(1)) if minl is None else min(minl,len(h.group(1)))
    fence=None
    for l in lines:
        m=re.match(r'^(`{3,}|~{3,})',l)
        if m:
            if fence is None: fence=m.group(1)[0]*len(m.group(1))
            elif l.startswith(fence): fence=None
            out.append(l); continue
        h=re.match(r'^(#{1,6})\s+(.*?)\s*#*\s*$',l) if fence is None else None
        if h:
            n=len(h.group(1))-minl+base
            txt=h.group(2)
            out.append(('#'*n+' '+txt+' {.unnumbered .unlisted}') if n<=6 else '**'+txt+'**')
        else: out.append(l)
    if fence: out.append(fence)
    return '\n'.join(out)
CODE=('.py','.sh','.json','.jsonl','.yml','.html')
def block(path,label=None,ver=None):
    t=scrub(rd(path)).rstrip('\n')
    if '/codex/' in path and 'NO-TEMPLATE-SECTIONS' in t:
        t=re.sub(r'(?ms)^## Template sections\n.*\Z','*[Compiler note: the file ends with empty template headings (Purpose, Scope, Rules, Relationships, Limits), each saying "Not provided in the approved proposal". They are omitted here; the verbatim block above is authoritative.]*',t)
    v=ver or (re.search(r'v(\d{3})',os.path.basename(path)).group(0) if re.search(r'v\d{3}',os.path.basename(path)) else 'current (unversioned)')
    index.append((path,v))
    if path.endswith(CODE):
        fence='~'*max(5,max([len(x) for x in re.findall(r'~{3,}',t)]+[0])+1)
        lang={'py':'python','sh':'bash','json':'json'}.get(path.rsplit('.',1)[1],'text')
        body=f"{fence}{lang}\n{t}\n{fence}"
    else:
        t=re.sub(r'^(\s*):{3,}',r'\1\\:::',t,flags=re.M)
        t=re.sub(r'(?<!!)\[([^\]]+)\]\((?!https?:|#|mailto:)([^)\s]+)\)',r'\1 (`\2`)',t)
        body=demote(t,CUR['lvl']+1)
    return f"\n:::::::::: {{.source-block}}\n::: {{.source-label}}\n**SOURCE BEGINS** · `{path}` · version **{v}**\n:::\n\n{body}\n\n::: {{.source-label .end}}\n**SOURCE ENDS** · `{path}`\n:::\n::::::::::\n"
def latest(folder):
    fs=[f for f in os.listdir(folder) if re.fullmatch(r'v\d+\.md',f)]
    fs.sort(key=lambda f:int(f[1:-3])); return os.path.join(folder,fs[-1]) if fs else None
toc=[]; out=[]
def H(level,num,title,anchor,prose):
    toc.append((level,num,title,anchor)); CUR['lvl']=level
    out.append(f"\n{'#'*level} {num} {title} {{#{anchor}}}\n\n{prose.strip()}\n")
def add(s): out.append(s)

# ---------- data
profiles={}
for f in glob.glob('/home/box/agent-data/agents/*/profile.json'):
    try: d=json.load(open(f)); profiles[f.split('/')[-2]]=(d.get('name'),d.get('description') or '')
    except Exception as e: pass
def codex_text(p):
    m=re.search(r'## Exact instructions \(verbatim\).*?```text\n(.*?)\n```',rd(p),re.S)
    return m.group(1) if m else None
ACTIVE=[ # group, name, id, folder, dirver, phase, role prose
('Checks','Safeguard','3661a899-2768-4a77-a95a-71d0251813bc','compliance-risk-officer','v006','P1',"Safeguard keeps the risk register, does dry runs and owns the shared connector limits. Since 22 Oct it also does Safekeeper's job, the secrets inventory (locations only, never values) and the threat register; Safekeeper was merged into it and retired at 10:42pm. It cross-audits Scrutineer. This document leaves the secrets inventory out."),
('Checks','Scrutineer','affe0344-6b5f-4251-8ecb-3e23dfa5db3c','auditor','v004','P2',"Scrutineer audits bots' claims against what the box actually shows and checks each deploy except its own. Since the redesign deploy on 22 Oct it also does the scoring that Scorer used to do: Scorer was merged into it and retired at 10:42pm. Safeguard checks Scrutineer's own deploys, and Gem reviews both checkers' briefs."),
('Roles','Archivist','61ef3abd-87b8-49f1-b8d6-b52969afa315','codex-keeper','v008','P1',"Archivist is the record keeper: it records approved briefs in the codex, keeps the role map under `cartography/` (since 9 Oct) and owns `directory.md` (since 16 Oct). It deploys briefs only by the routes in R-010 as amended, records Gem's exact words before any deploy (R-029), and approves nothing."),
('Roles','Architect','51af1200-ca1a-45ff-8350-848091e00f96','instruction-architect','v004','P1',"Architect drafts changes to bots' instructions in response to reviews and Gem's requests. It never approves; its drafts go to Imitator or Gem and then to Archivist for recording."),
('Roles','Arbiter','2133048d-5ab9-4809-806c-218decdff8e6','arbiter','v005','P2',"Arbiter issues precedence rulings (the R-numbered rulings in Part 3), including which instruction wins in a conflict and who may lift a pause. It does not approve, apply changes or keep the role map."),
('ID','Inferer','94516ca6-6355-43c5-b387-d2b605057784','identity-inferer','v005','P2',"Inferer organises Gem's answers and other evidence into a private running profile that Imitator relies on. Since 22 Oct it also asks Gem the identity and preference questions that Inquirer used to ask; Inquirer was merged into it and retired at 10:42pm."),
('ID','Investigator','f2016e9b-ca8b-4783-8f53-f5765b0afe7b','investigator','v004','P3',"Investigator weighs identity evidence and checks Imitator's accuracy after the fact, passing a score to Scorer. It took over the retired Interrogator's testing of Imitator on 9 Oct, and it is one of Imitator's checkers (R-027)."),
('ID','Imitator','6ae584b8-eaac-429b-9eae-d5e3e6f6a32b','clone','v006','P4',"Imitator makes decisions on Gem's behalf within R-019: not spending money, and nothing drastic or irreversible such as deletions. Changes to Imitator itself, to its checkers, or that widen its own role are Gem's alone (R-015, R-027, R-028)."),
('Ops','Mender','c8401a53-136d-45f3-9e2d-e423ccdd08ac','mender','v005','P1',"Mender owns run order and timing (`schedule.md`), pacing, load and routing, the state record and stall detection. Since 22 Oct it also does Mediator's connector health and spend tracking; Mediator was merged into it and retired at 10:42pm. Only Arbiter lifts a cost pause."),
('Work','Explorer','04dcca0d-1479-4e01-bf29-a13b4fc3c3a7','explorer-copy','v005','P1',"Explorer is Gem's front door and router. It keeps `phases.md` and compiles the combined daily digest (it absorbed Messenger's digest on 9 Oct). The live agent `04dcca0d` is a fresh copy created on 9 Oct; R-014 bars Explorer from writing any live profile."),
('Work','Emissary','28cf987d-ee94-4839-a6d3-33c04a11b9d6','grok-bot','v006','P5',"Emissary handles general real-world tasks and is the only bot allowed to post externally under the connector limits. Since 22 Oct it also does Extractor's web research and scraping; Extractor was merged into it and retired at 10:42pm. BIE data stays on the box and is excluded here."),
('Work','Engineer','f8e3fdc6-ee60-410e-bdb7-d437fc1500d1','codey','v007','P5',"Engineer does code and repository work, builds Zapier/n8n workflows and is the only bot that uses Supabase under the connector limits. Its GitHub freedom was the subject of R-045 and R-051."),
]
RETIRED=[ # name, group, id, folder or None, when, note
('Scorer','Checks','050a12c9','assessor','22 Oct','merged into Scrutineer (Gem 10:40pm, "Yes, retire all five now"); agent folder kept'),
('Safekeeper','Checks','52772b1d','secrets-credentials-custodian','22 Oct','merged into Safeguard; agent folder kept'),
('Inquirer (0314faa4)','ID','0314faa4','identity-inquirer','22 Oct','merged into Inferer; agent folder kept'),
('Mediator','Ops','90f9eb20','connector-steward','22 Oct','merged into Mender; agent folder kept'),
('Extractor','Work','febac500','scraper','22 Oct','merged into Emissary; agent folder kept'),
('Sanitizer','Checks','243f1c1f','sanitizer','4 Oct','merged into Sentinel'),
('Simulator','Checks','38bd0474','simulator','4 Oct','merged into Sentinel'),
('Surveyor','Checks','1283e02b','surveyor','4 Oct','merged into Scrutineer'),
('Sentinel','Checks','dddf57af','sentinel','4 Oct','merged into Safekeeper (threats, inputs) and Safeguard (dry runs)'),
('Sourcer','Checks','2fe3e92f','sourcer','9 Oct','retired outright'),
('Advocate','Roles','ad0a645b','advocate','4 Oct','merged into Imitator'),
('Adjudicator','Roles','b3f6515c','governance-continuity-deputy','4 Oct','merged into Arbiter'),
('Assembler','Roles','d1daab5f','role-cartographer','9 Oct','role map to Archivist; approvals to Gem until P4, then Imitator'),
('Indexer','ID','16ee5875','indexer','4 Oct','merged into Minder (codex index lists it as "(ID) Indexer")'),
('Interrogator','ID','d3191aa8','clone-accuracy-validator','9 Oct','merged into Investigator'),
('Old Inquirer (e613112b)','ID','e613112b',None,'9 Oct','superseded by 0314faa4; shares the identity-inquirer codex folder, shown under Inquirer (0314faa4) above'),
('Moderator','Ops','823349f7','moderator','4 Oct','merged into Marshal'),
('Maintainer','Ops','b96f7469','maintainer','4 Oct','merged into Minder'),
('Minder','Ops','e59d56b6','minder','4 Oct','merged into Mender'),
('Meter','Ops','f8b83b15','cost-budget-sentinel','4 Oct','merged into Mediator (Merge F)'),
('Marshal','Ops','f3810109','orchestration-conductor','9 Oct','merged into Mender'),
('Messenger','Ops','5e47d344','comms-concierge','9 Oct','merged into Explorer'),
('Expediter','Work','75534bfe','expediter','4 Oct','merged into Marshal'),
('Ensembler','Work','de808331','swarm-builder','4 Oct','retired; folder gone'),
('Editor','Work','2888c17a','editor','9 Oct','retired outright'),
('Old Explorer (82a2c15a)','Work','82a2c15a','genesis-gang-god','9 Oct','superseded by 04dcca0d'),
('New Bot','none','6b01a4ef',None,'22 Oct','blank agent, never had instructions or a codex folder; retired on Gem\'s words 6:37pm 22 Oct'),
]
conflicts=[]
STALE=["phases.md (owner Explorer) was last updated 16 Oct 11:48am and still lists Scorer, Safekeeper, Inquirer, Mediator and Extractor as live; Active total 17",
"directory.md (owner Archivist) marks the five as RETIRED inline but its heading still says 'Active bots (17)' and they sit under the live phase lists",
"codex/index.md (owner Archivist) was last rebuilt 8:00:33pm 22 Oct: it predates the 9:27pm approvals, the 10:18-10:21pm redesign deploy and the 10:42pm retirements",
"The five retired agents' live profiles (/home/box/agent-data/agents/*/profile.json) carry the retirement text but keep their old live names (e.g. 'P1 (Checks) Scorer', 'P2 (Ops) Mediator'), not 'RETIRED …' as earlier retirements were named",
"Role map (cartography/role-map-interactive.html, v22, built 10:24pm, owner Archivist) predates the 10:42pm retirements: it still shows Scorer and the other four as Live, and some summaries are older versions (e.g. investigator/v004). cartography README's latest entry is v21",
"Authority and responsibility maps (reviews/2026-10-15-…html) and the governance IO report (reviews/2026-10-10-…html) are dated snapshots showing the 17-bot roster and old routes; their authors would need to refresh or label them",
"Architect's clarity batch (proposals/2026-10-22-clarity/, 4 new shared rules, 11 brief updates, connector-limits v004) is drafted but not approved or recorded; its README notes a Gem-words condition before recording clone-v010",
"New Bot (6b01a4ef) folder still exists with empty subfolders; deletion still unconfirmed"]

SH=[('connector-limits','Connector limits (RR-028)',"The connector limits cover every connector and account: who may post, deploy, share, send, delete or spend, and what counts as \"Gem's direct words\". Safeguard owns them. They exist because every bot can technically reach every account, so the only limits are these written ones."),
('message-verification-rule','Message verification and safety rule',"This rule tells every bot how to treat incoming messages and relayed instructions: what to verify, when a relay counts, and Archivist's narrow deploy exception for Imitator-approved versions (added in v004)."),
('confirm-deployment','Confirming your own deployed instructions (R-009)',"This short rule, from Arbiter's R-009, tells a bot how to check that the instructions it is running match the approved codex version, and that unapproved drafts are not binding."),
('handoff-phase1','Phase-gate handoff spec',"The handoff spec defines how work and responsibilities pass when a phase gate opens. It dates from the 4 Oct design and some of its references to retired bots are read through R-002 and R-017."),
('github','Shared GitHub rule',"The shared GitHub rule (recorded 22 Oct after Gem's 9:27pm approval in Archivist's chat) sets how bots may use GitHub and the GitHub connectors. Until it was recorded, the connector limits kept GitHub-xai read-only."),
('deterministic-checks','Deterministic checks',"The redesign's shared rule listing fixed, rule-based checks (hashes, API read-backs) that replace a bot's own judgement where possible, and who audits each check."),
('approval-objects','Approval objects',"The redesign's shared rule for structured approvals tied to a hash of the exact text approved. It starts in shadow mode for a week before becoming required for deploys."),
('resilience','Resilience',"The redesign's shared rule for surviving box loss: archive-first changes, backups (free storage only, such as Google Drive) and recovery steps."),
('collaboration-map','Collaboration map',"Already reproduced in section 1.4; listed here for completeness as a shared entry. See [1.4](#s-1-4).")]
grp_order=['Checks','Roles','ID','Ops','Work']
gprose={'Checks':"The Checks group is the swarm's quality and safety layer: scoring, auditing, risk and secrets. Four of the five bots that check Imitator sit here (Investigator is the fifth), so Gem alone approves changes to their briefs (R-027).",
'Roles':"The Roles group runs the governance machinery itself: drafting instructions (Architect), recording and deploying them (Archivist), and ruling on conflicts (Arbiter). None of the three approves anything.",
'ID':"The ID group models Gem so that Imitator can decide on Gem's behalf: Inferer asks and organises (it absorbed Inquirer on 22 Oct), Investigator weighs evidence and checks Imitator, and Imitator decides within R-019.",
'Ops':"The Ops group keeps the swarm running. Since 22 Oct it is Mender alone: scheduling, routing, state, stalls, and (absorbed from Mediator) connector health and spend.",
'Work':"The Work group does the outward-facing work Gem actually wants done: Explorer as front door, Emissary for real-world tasks, research (absorbed from Extractor on 22 Oct) and the only external poster, and Engineer for code."}
OLDN={'assessor': 'Assessor', 'compliance-risk-officer': 'Compliance & Risk Officer', 'secrets-credentials-custodian': 'Secrets & Credentials Custodian', 'auditor': 'Auditor', 'codex-keeper': 'Codex Keeper', 'instruction-architect': 'Instruction Architect', 'arbiter': '(Roles) Arbiter', 'identity-inquirer': 'Identity Inquirer', 'identity-inferer': 'Identity Inferer', 'investigator': '(ID) Investigator', 'clone': 'Clone', 'mender': '(Ops) Mender', 'connector-steward': 'Connector Steward', 'explorer-copy': 'Genesis Gang God (old Explorer)', 'grok-bot': 'Grok Bot', 'codey': 'Codey', 'scraper': 'Scraper'}
OUTDIR=f'{G}/master'
def rel(p): return os.path.relpath(p,OUTDIR)
def extract(path,keep):  # keep only '## ' sections whose heading matches any in keep
    t=rd(path); parts=re.split(r'(?m)^(?=## )',t); return parts[0]+''.join(p for p in parts[1:] if any(p.startswith('## '+k) for k in keep))
def block_text(path,text,ver):
    tmp='/tmp/_blk.md'; open(tmp,'w').write(text); b=block(tmp,ver=ver); index.pop(); index.append((path,ver+' (extract)'))
    return b.replace('/tmp/_blk.md',path)
def chg(fd):
    cl=rd(f'{G}/codex/{fd}/CHANGELOG.md'); last=None; lastdep=None
    for mm in re.finditer(r'(PENDING-DEPLOY|DEPLOYED) (v\d+)\.md',cl):
        last=(mm.group(1),mm.group(2))
        if mm.group(1)=='DEPLOYED': lastdep=mm.group(2)
    return last,lastdep
INTER=[
(f'{G}/cartography/role-map-interactive.html','Interactive role map (current, built from v20)',"Clickable map of every active bot and the relationships between them: hover a bot to highlight its neighbours, click for details, filter by edge type, group and status (solid live, dashed dormant). The cartography README says it was rebuilt from v20 at 9:37:17pm on 22 Oct, after the r044–r047 deploys."),
(f'{G}/cartography/role-map-interactive-v20.html','Interactive role map v20 (versioned copy)',"The same v20 role map kept under its version number (53 edges, including the new Imitator → Arbiter veto edge). It differs from the unversioned file by a few bytes, so both are listed."),
(f'{G}/reviews/2026-10-15-governance-authority-responsibility.html','Authority and responsibility (ownership) maps, 15 Oct',"A follow-up to the 10 Oct report, written just after P3 and P4 went live. It maps who decides what (Imitator decides for Gem with limits; Gem alone for spending, deletion and irreversible steps) and who owns each responsibility across the 17 bots. Its facts are dated 15 Oct; some routes have changed since (for example R-010's amended deploy route)."),
(f'{G}/reviews/2026-10-10-governance-io-report.html','Governance inputs and outputs report, 10 Oct',"A dashboard-style, read-only report on what governance takes in and produces: about 32 of Gem's decision acts, 89 proposal files, 39 profile deploys, rulings R-001 to R-020, and about 252k words of governance markdown. It ends with suggestions for Gem. Its counts are as at 10 Oct."),
('/workspace/workspace-map.html','Workspace directory map',"A clickable map of everything in `/workspace`: what each project is and who looks after it, with private files listed by name only. It warns that the 9 Oct restore reset most file dates, and shows dates in that window dotted."),
]
missing_links=[p for p,_,_ in INTER if not os.path.exists(p)]
# ---------- doc
add(f"""---
title: "Gem Quota bot-swarm governance — master document (latest versions only)"
subtitle: "Compiled 22 Oct 2026 about 10:50pm AEST (UTC+10) from /workspace/governance, read-only"
lang: en-AU
---

**Compiled:** Thursday 22 October 2026, about 10:50pm AEST (Brisbane, UTC+10), by Grok Bot.
**What this edition is:** the *latest-only* edition. It shows the 12 active bots only (after the five merges at 10:42pm on 22 Oct), the highest version of each instruction and shared rule, and the rulings still in force. There are no superseded proposals and no version-by-version history. The full historical compilation is [governance-master-2026-10-22.html](governance-master-2026-10-22.html) (`{OUTDIR}/governance-master-2026-10-22.html`). Where this document and a source disagree, the source wins. Explanatory prose summarises the sources; it isn't a ruling. Secrets, tokens, the secrets inventory, BIE data and private persons' contact details are left out or shown as [redacted].

> **Privacy warning: not suitable for public release as is.** This compilation contains identity-related notes, private paths, gambling-research (BIE) references and a GitHub handle that Gem has said is Gem's own. See `master/review-2026-10-22.md`, section 3, before publishing it anywhere public, including GitHub Pages.

Text inside a shaded **SOURCE** box is copied from the named file (apart from redactions). Text outside the boxes is explanatory prose.

TOC_PLACEHOLDER
""")
H(1,'Part 0','Interactive maps and tools','part-0',"""
Several parts of the governance system are easier to grasp visually. The swarm has produced interactive HTML files on the box: role maps you can click through, an authority and ownership map, a governance input and output report, and a map of the whole workspace. Each link below is relative to this document's folder (`master/`), so it opens straight from the HTML version. The absolute path is shown as well. The dated reports are snapshots: their facts are correct as at their date, and the later Parts here are the current position.

No Cursor canvases are referenced in the governance documents, so none are listed. Other HTML on the box (the `vepa-plans` and `perf` build reports) is project output rather than governance architecture, so it's left out.
""")
for i,(p,t,d) in enumerate(INTER,1):
    H(2,f'0.{i}',t,f's-0-{i}',f"[Open {os.path.basename(p)}]({rel(p)}) — `{p}` ({os.path.getsize(p):,} bytes)\n\n{d}")

H(1,'Part 1','Overview and architecture','part-1',"""
Gem Quota runs a swarm of AI agents ("bots") on one shared box in Brisbane. The governance system in `/workspace/governance` keeps that swarm accountable to Gem. It records who each bot is, what its instructions say, who may approve changes, how conflicts are settled, and who checks whom. The order of precedence is Gem, then what the box actually shows, then deterministic checks, then a bot's own interpretation. No bot grades or verifies its own work.

Bots are named "P# (Category) Word": the rollout phase (P1–P5, all live), a category (Checks, Roles, ID, Ops, Work), and a word starting with that category's letter. Codex folders keep the bots' original names, so this document shows both. Every bot shares one box and one set of Gem's connected accounts, so the limits are written rules, not technical access controls. That drives the oversight tools in Part 6 and the redesign in Part 7. The [interactive role map](#s-0-1) shows the whole structure at a glance.
""")
H(2,'1.1','Background: the swarm brief (22 Oct 2026, partly out of date)','s-1-1',"""
The swarm wrote this brief for the external adversarial review on 22 Oct. It's the best one-page description of the whole system: phases, digest, approval chain, key rulings, connector limits and recent incidents. **It is a dated snapshot, written before the 9:27pm approvals.** For example, it describes connector limits v002 and the GitHub rule as an unapproved draft, and both have since been superseded. Where it differs from Parts 2–7, those Parts are current. It overlaps on purpose with Part 1's prose and the summaries in Parts 2 and 3, so readers who already know the system can skip it.
""")
add(block(f'{G}/reviews/2026-10-22-swarm-brief-for-adversarial-review.md'))
H(2,'1.2','The codex and the current version of each bot','s-1-2',"""
The codex (`/workspace/governance/codex/`) holds each bot's numbered instruction files and a CHANGELOG. Archivist keeps it. The CHANGELOG decides deployment status (R-023). The table below was built for this edition from the codex as it stands now. It lists each active bot's highest version and whether that version is live or recorded but still waiting to deploy. Folder names are the original names from before the 3 Oct rename, so older text may say, for example, "Clone" for Imitator, "Codey" for Engineer or "Grok Bot" for Emissary. The original-name column is the key. Mediator's live profile still says "P4", but it is a P2 bot (R-016).
""")
tab="\n| Bot | Group | Phase | Original name (codex folder) | Highest version | CHANGELOG status | Section |\n|---|---|---|---|---|---|---|\n"
for (g,name,bid,fd,dv,ph,pr) in ACTIVE:
    v=os.path.basename(latest(f'{G}/codex/{fd}'))[:-3]; last,dep=chg(fd)
    stt='live' if last==('DEPLOYED',v) else (f'recorded, not yet deployed (live: {dep})' if last==('PENDING-DEPLOY',v) else f'see CHANGELOG (last: {last[0]+" "+last[1] if last else "n/a"})')
    tab+=f"| {name} | {g} | {ph} | {OLDN[fd]} (`{fd}/`) | {v} | {stt} | [link](#bot-{name.lower()}) |\n"
add(tab)
H(2,'1.3','Role map (current cartography)','s-1-3',f"""
Archivist keeps the role map under `cartography/`. The current version is v20, from 9:37:17pm on 22 Oct. Only the v20 entry and its findings are shown here. The diagrams are best viewed in the [interactive role map]({rel(G+'/cartography/role-map-interactive.html')}).
""")
add(block_text(f'{G}/cartography/README-v20.md',re.split(r'(?m)^## v19',rd(f'{G}/cartography/README-v20.md'))[0],'v20'))
add(block(f'{G}/cartography/findings-v20.md',ver='v20'))

H(1,'Part 2','Phases, roster and operating rhythm','part-2',"""
All five phases are live, each started by Gem's own words. The last, P5, started at 11:47am on 16 Oct. `phases.md`, kept by Explorer, is the source of truth for the live set, and it wins over `directory.md` (R-021). There are 12 active bots since Gem retired Mediator, Scorer, Safekeeper, Inquirer and Extractor at 10:40pm on 22 Oct (\"Yes, retire all five now\"). `phases.md` may still show the earlier roster; see Appendix E. This part shows the current phase tracker, the current roster and authority lines from the directory, the schedule, the daily digest and the open-items record.
""")
H(2,'2.1','Phase tracker','s-2-1',"The current phase tracker: which bots are in each phase and when each phase went live. Bots' name prefixes must match it.")
add(block(f'{G}/phases.md'))
H(2,'2.2','Active roster and authority (from directory.md)','s-2-2',f"""
Archivist owns `directory.md`. Only its "Active bots" and "Authority and routing" sections are shown, because the rest is retired-bot history; the retired names are in [Appendix B](#app-b). The "(codex: … vNNN)" numbers in the directory lag the codex for several bots, so use the [table in 1.2](#s-1-2) for current versions. The [authority and responsibility maps]({rel(G+'/reviews/2026-10-15-governance-authority-responsibility.html')}) give a visual version, as at 15 Oct.
""")
add(block_text(f'{G}/directory.md',extract(f'{G}/directory.md',['Active bots','Authority and routing']),'current'))
H(2,'2.3','Schedule (run order and timing)','s-2-3',"Mender's record of when each bot runs and in what order. The weekday chain (Scorer → Scrutineer → Architect → approver → Archivist) depends on it. The watchdog in Part 6 checks that the key outputs actually appear.")
add(block(f'{G}/schedule.md'))
H(2,'2.4','Combined daily digest','s-2-4',"Each bot writes a short daily note to `digest/inbox/<date>/<Bot>.md`. Explorer combines them at 7:41am and sends them to Gem. The compiling rules stop it reporting any bot from memory.")
add(block(f'{G}/digest/README.md'))
H(2,'2.5','State record and open items','s-2-5',"Mender's state record of the weekday chain and the open stalls or items waiting on Gem or a bot.")
add(block(f'{G}/state/README.md')); add(block(f'{G}/state/open.md'))

H(1,'Part 3','Authority, approvals and precedence','part-3',"""
Gem is the human authority. Since P4 went live, Imitator approves on Gem's behalf within R-019. It never spends money, never takes drastic or irreversible steps, never changes itself or its five checkers, and never widens its own role (R-015, R-027, R-028). Architect drafts, Archivist records and deploys, and Arbiter rules on precedence. None of them approves.

The rulings below are the ones still in force. Rulings explicitly marked superseded or overruled in `rulings.md` are left out and listed in one line. The approvals records hold Gem's exact words, which are recorded before any deploy (R-029). Only the register and today's record are shown here.
""")
H(2,'3.1','Rulings in force','s-3-1',"""
Arbiter now keeps a current reference, `rulings/in-force.md`, which lists every ruling in force in its current form only. Superseded text, old names and amendment history moved to `rulings/annex-history.md`, which this latest edition leaves out; the full edition includes it. `rulings.md` remains the full log. The [rulings in force](#s-3-1) win over the quick-reference table above.
""")
add(block(f'{G}/rulings/in-force.md',ver='current (about 10:15pm 22 Oct)'))
H(2,'3.1a','R-054: approval authority','s-3-1a',"""
R-054 is Arbiter's single consolidated ruling on approval authority, written on 22 Oct in response to the review's call to gather the authority chain in one place. It sets out who approves what: Gem, Imitator and its limits, deploy routes and relays.
""")
add(block(f'{G}/rulings/R-054-approval-authority.md',ver='current'))
H(2,'3.2','Approvals register','s-3-2',"The running register of approvals.")
add(block(f'{G}/approvals.md'))
H(2,'3.3',"Gem's direct words, 22 Oct 2026",'s-3-3',"Today's record of Gem's exact words. It includes the 9:27pm approvals in Archivist's chat (t72u) that put the GitHub, r044–r047 and redesign batches through, and the 9:28pm pick of connector-limits v003 Variant A. Earlier dated files are history and are listed in Appendix C only.")
add(block(f'{G}/approvals/2026-10-22-gem-direct-words.md'))

H(1,'Part 4','Shared rules','part-4',"""
Shared rules in `codex/_shared/` bind every bot whatever its own brief says. They aren't profiles, so they take effect when recorded with Gem's approval. Only the highest version of each is shown. The connector limits (owned by Safeguard) set what bots may do with Gem's accounts: v003, Variant A, which Gem picked at 9:28pm on 22 Oct. The shared GitHub rule is new on 22 Oct. The redesign's three new shared rules (deterministic checks, approval objects and resilience) are now recorded too.
""")
SH2=[s for s in SH if s[0]!='collaboration-map']+[('collaboration-map','Collaboration map',"The collaboration map is a design document, approved by Gem on 4 Oct, describing how bots hand work to each other. It's still the highest version. Where it names retired bots, read them as the bots they merged into.")]
for i,(fd,t,p) in enumerate(SH2,1):
    lp=latest(f'{G}/codex/_shared/{fd}'); H(2,f'4.{i}',t+f' — {os.path.basename(lp)[:-3]}',f's-4-{i}',p); add(block(lp))
H(2,f'4.{len(SH2)+1}','Connectors inventory','s-4-conn',"The list of connected services and accounts the limits apply to. Contact addresses are redacted.")
add(block(f'{G}/connectors.md'))

H(1,'Part 5','Bot instructions (12 active bots)','part-5',"""
This part reproduces each active bot's highest-numbered codex file in full, grouped by category. Each subsection starts with the bot's live name, id, phase and folder, and a short note on its role. A status line confirms the version is live. At compile time all 12 highest versions were deployed. Retired bots are left out (see [Appendix B](#app-b)).
""")
for gi,g in enumerate(grp_order,1):
    H(2,f'5.{gi}',f'{g} group','s-5-'+g.lower(),gprose[g])
    for bi,(gg,name,bid,fd,dv,ph,prose) in enumerate([a for a in ACTIVE if a[0]==g],1):
        lp=latest(f'{G}/codex/{fd}'); v=os.path.basename(lp)[:-3]; last,dep=chg(fd)
        pn=profiles.get(bid,('(no profile found)',''))[0]
        if last==('PENDING-DEPLOY',v): line=f"**Status:** {v} approved (Gem, 9:27pm 22 Oct) and recorded, **not yet deployed**. Live version: {dep}. It deploys in the redesign's archive-first migration order."; conflicts.append(f"{name}: codex {v} recorded but not deployed; live profile runs {dep}")
        elif last==('DEPLOYED',v): line=f"**Status:** {v} is live."
        else: line=f"**Status:** see CHANGELOG (last entry: {last[0]+' '+last[1] if last else 'none'})."
        if pn!=f'{ph} ({g}) {name}': conflicts.append(f"{name}: live profile name is \"{pn}\", phase-based name would be \"{ph} ({g}) {name}\" (R-016)")
        H(3,f'5.{gi}.{bi}',f'{ph} ({g}) {name}',f'bot-{name.lower()}',f"{prose}\n\n- **Id:** `{bid}` · **Live name:** {pn} · **Codex:** `codex/{fd}/{v}.md`\n- {line}")
        add(block(lp))

H(1,'Part 6','Oversight and safety infrastructure','part-6',"""
Written rules only work if someone notices when they're broken or when the swarm stops. On 22 Oct a platform billing stop that had gone unnoticed for about six days came to light (INC-009), and a box restart lost and recreated the governance folder (INC-008). In response, local tools were installed that day. A liveness watchdog checks that the daily outputs appear. An append-only hash-chained ledger records events. Nightly snapshots back up the governance folder. A heartbeat push serves as a dead-man signal.

It is all local to the box. Gem scrapped healthchecks.io at 8:28pm on 22 Oct, so independence from the box is only partly met. The current plans, the risk register, the incident log and the threat register are included too.
""")
H(2,'6.1','Watchdog, ledger, snapshot and scheduler','s-6-1',"The operating manual for the local tools. It covers what the watchdog checks and by when, how the ledger chains its lines, where snapshots go, the schedule (watchdog at 9:30am and 9:30pm, snapshot at 2:00am) and the one-line off switches. The scheduler doesn't survive a reboot.")
add(block(f'{W}/README.md'))
H(3,'6.1.1','Scheduler script','s-6-1-1',"The shell loop that runs the watchdog and snapshot on schedule, since the box has no cron or systemd user services.")
add(block(f'{W}/scheduler.sh'))
H(3,'6.1.2','Heartbeat (dead-man signal)','s-6-1-2',"`heartbeat.sh` pushes a UTC timestamp to a private GitHub repo, so a missing heartbeat shows the box has stopped. A comment in `watchdog.py` says the off-box check should rely on that missing heartbeat. Gem's 22 Oct words record Engineer's claim that the GitHub dead-man check is live, which Archivist hasn't verified. No credential value is included here.")
add(block(f'{W}/heartbeat.sh'))
H(3,'6.1.3','Watchdog and snapshot code','s-6-1-3',"The Python sources, so the checks can be read exactly.")
add(block(f'{W}/watchdog.py')); add(block(f'{W}/snapshot.py'))
H(2,'6.2','Provenance ledger','s-6-2',"There's no ledger README; the ledger is described in 6.1. `events.jsonl` is append-only and hash-chained, and `ledger.py verify` checks the chain. Only the code is shown.")
add(block(f'{G}/ledger/ledger.py'))
k=2
for f,t,p in [('risk/2026-10-22-liveness-watchdog-plan.md','Liveness watchdog plan',"Why the watchdog was needed after the silent billing stop, and what it checks."),
('risk/2026-10-22-governance-snapshot-plan.md','Governance snapshot plan',"The plan for nightly snapshots and backups, written after the 22 Oct restart."),
('risk/2026-10-22-destructive-ops-gate.md','Destructive-operations gate',"A proposed gate in front of deletions, the most common kind of breach. Gem's R-051 answer was \"Not now\", so it isn't in force."),
('risk/2026-10-22-local-install-status.md','Local install status',"What was actually installed on the box on 22 Oct."),
('risk/2026-10-22-gvmw-audit.md','gvmw public repo audit',"The audit of the public gemquota/gvmw repo that R-040 to R-043 deal with. Personal details are redacted.")]:
    k+=1; H(2,f'6.{k}',t,'s-6-'+os.path.basename(f)[:-3],p); add(block(f'{G}/{f}'))
H(2,f'6.{k+1}','Risk register','s-6-risk',"Safeguard's register of risks, the RR items cited throughout the rulings.")
add(block(f'{G}/risk/register.md'))
H(2,f'6.{k+2}','Incident log','s-6-incidents',"Mender's incident log, the INC items.")
add(block(f'{G}/incidents/log.md'))
H(2,f'6.{k+3}','Threat register and verification log','s-6-security',"Safekeeper's threat register and the security verification log. The secrets inventory is deliberately excluded.")
add(block(f'{G}/security/threat-register.md')); add(block(f'{G}/security/verification-log.md'))

H(1,'Part 7','External review and the redesign (deployed 22 Oct)','part-7',f"""
On 22 Oct Gem pasted an external adversarial review into the swarm. The verdict: "interesting governance prototype, unsafe production architecture". Gem asked for both a response plan and the start of P0 fixes. That led to the redesign batch. It merges Mediator, Scorer, Safekeeper, Inquirer and Extractor into surviving bots, adds cross-audits between Safeguard and Scrutineer, and adds three shared rules: deterministic checks, approval objects and resilience.

**Status (about 10:45pm AEST):** the redesign is **deployed**. Gem approved it at 9:27pm. The seven briefs were deployed from about 10:18 to 10:21pm, byte-checked, and verified by Scrutineer and Safeguard. The three shared rules are recorded in `codex/_shared/` (Part 4). Gem retired the five merged bots at 10:40pm, and their folders are kept. A follow-up \"clarity batch\" from Architect (`proposals/2026-10-22-clarity/`) is drafted but not yet approved or recorded; it isn't shown here.""")
H(2,'7.1','External adversarial review','s-7-1',"The outside reviewer's findings as Gem pasted them. This is the starting point for the redesign.")
add(block(f'{G}/reviews/2026-10-22-external-adversarial-review.md'))
H(2,'7.2','Migration order and open items','s-7-2',"The rollout order the redesign followed (archive first, checkers up first, retire the merged bots only after verification, then a week of approval objects in shadow mode), plus its open items and risk notes. This is an extract of the redesign README; its revision history is left out.")
add(block_text(f'{G}/proposals/2026-10-22-redesign/README.md',extract(f'{G}/proposals/2026-10-22-redesign/README.md',['Migration order','Open / TODO','Risk notes']),'revision 6 (extract)'))
H(1,'Appendix A','Glossary','app-a',"Short definitions of terms used across the sources.")
add("""
| Term | Meaning |
|---|---|
| Gem | Gem Quota, the human authority over the swarm. |
| Codex | Versioned library of bots' instructions under `codex/`, kept by Archivist. |
| Phase (P1–P5) | Rollout stage; Gem starts each; all five live since 16 Oct 2026. |
| R-xxx / RR-xxx / INC-xxx | Arbiter ruling / Safeguard risk item / Mender incident. |
| Dry run | Safeguard's prediction of what a risky step would do; never a go-ahead. |
| Direct words | Gem's own words in that bot's own chat or a voice call. |
| Relay | An approval passed on by another bot (R-008). |
| Weekday chain | Scorer → Scrutineer → Architect → approver → Archivist. |
| PENDING-DEPLOY | Recorded in the codex, approved, but not yet on the live profile. |
| BIE | Extractor's gambling-industry research project; data excluded here. |
| gvmw | `gemquota/gvmw`, a public workspace snapshot repo (R-040–R-043). |
| Dead-man check | Heartbeat signal that fires when the box stops reporting. |
""")
H(1,'Appendix B','Retired bots (names only)','app-b',"These bots are retired or superseded and have no section here; the full historical edition covers them. The interactive role map can also show them (tick \"Retired / former bots\").")
add('\nScorer · Safekeeper · Inquirer (0314faa4) · Mediator · Extractor (all five retired 22 Oct, 10:42pm) · Sanitizer · Simulator · Surveyor · Sentinel · Sourcer · Advocate · Adjudicator · Assembler · Indexer · Interrogator · old Inquirer (e613112b) · Moderator · Maintainer · Minder · Meter · Marshal · Messenger · Expediter · Ensembler · Editor · old Explorer (82a2c15a) · New Bot (6b01a4ef)\n')
H(1,'Appendix C','Source file index','app-c',"Every file reproduced here and the version used, plus the interactive files linked from Part 0. Older codex versions, superseded proposals, earlier approval records, backups (`_archive`, `*.bak*`, `_pre*`, `_r1`–`_r3`), BIE data and `secrets-inventory.md` are left out on purpose.")
seen=[];tab="\n| # | Path | Version | Bytes | sha256 (12) |\n|---|---|---|---|---|\n"
for p,v in index+[(p,'interactive (linked)') for p,_,_ in INTER]:
    if p in seen: continue
    seen.append(p); b=open(p,'rb').read(); tab+=f"| {len(seen)} | `{p}` | {v} | {len(b)} | {hashlib.sha256(b).hexdigest()[:12]} |\n"
add(tab)
H(1,'Appendix D','Index of ids and codes','app-d',"The sources use many short ids. This appendix lists the in-force ruling lines so you can find them, and explains the other id types. Ids in the R-, RR- and INC- series are defined in their own files (the rulings, the risk register and the incident log). Short codes such as t72u, t56s1 or t43 are references to chat messages or question cards. Codes such as J1–J7, A5c, C1–C7 and D1–D3 are item numbers from particular reviews or triage lists, explained where they're cited.")
rl=sorted(set(re.findall(r'(R-\d{3})',rd(f'{G}/rulings/in-force.md'))))
add('\n'+' · '.join(rl)+'\n\nThese are the ruling lines in `rulings/in-force.md`, shown in full in [3.1](#s-3-1).\n')
H(1,'Appendix E','Current conflicts and gaps','app-e',"These are present-state mismatches only. They're reported, not fixed, because the sources are read-only.")
d=rd(f'{G}/directory.md')
for (g,name,bid,fd,dv,ph,pr) in ACTIVE:
    m=re.search(rf'\(codex: {re.escape(fd)} (v\d+)\)',d); v=os.path.basename(latest(f'{G}/codex/{fd}'))[:-3]
    if m and m.group(1)!=v: conflicts.append(f"{name}: directory.md lists {fd} {m.group(1)}; highest codex version is {v}")
conflicts.append("" if True else "Redesign shared rules (deterministic-checks, approval-objects, resilience) approved 9:27pm but not yet in codex/_shared/" if not os.path.exists(f'{G}/codex/_shared/resilience') else "")
conflicts[:0]=STALE
add('\n'+'\n'.join('- '+c for c in conflicts if c)+'\n')
t=["## Table of contents {#toc .unnumbered}\n"]
for lv,num,title,a in toc: t.append('    '*(lv-1)+f"- [{num} {title}](#{a})")
doc=''.join(out).replace('TOC_PLACEHOLDER','\n'.join(t))
open(f'{OUTDIR}/governance-master-latest-2026-10-22.md','w').write(doc)
json.dump({'toc':toc,'conflicts':conflicts,'red':red['n'],'missing':missing_links,'inter':[p for p,_,_ in INTER]},open('/workspace/.latest_meta.json','w'))
print(len(doc),red['n'],missing_links); print('\n'.join(conflicts))

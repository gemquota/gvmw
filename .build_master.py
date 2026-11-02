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

# ---------- doc
add(f"""---
title: "Gem Quota bot-swarm governance — master document"
subtitle: "Compiled 22 Oct 2026 (AEST, UTC+10) from /workspace/governance, read-only"
lang: en-AU
---

**Compiled:** Thursday 22 October 2026, about 10:50pm AEST (Brisbane, UTC+10), by Grok Bot.
**Status:** a read-only compilation. Nothing under `/workspace/governance` was changed except creating `master/`. Where this document and a source disagree, the source wins. Explanatory prose is a summary of the sources, not a ruling. Secrets, tokens, the secrets inventory, BIE data and private persons' contact details are left out or shown as [redacted].

**How to read it:** Parts are top-level categories, sections and subsections sit under them. Text inside a shaded **SOURCE** box is copied verbatim from the named file (apart from redactions), with its path and version. Text outside those blocks is explanatory prose.

TOC_PLACEHOLDER
""")

H(1,'Part 1','Overview and architecture','part-1',"""
Gem Quota runs a swarm of AI agents ("bots") on one shared box in Brisbane. The governance system in `/workspace/governance` exists to keep that swarm accountable to Gem: it records who each bot is, what each bot's instructions say, who may approve changes, how disputes are settled, and what checks run on whom. The overriding order of precedence, repeated across the sources, is Gem first, then what the box actually shows (environment reality), then deterministic checks, then a bot's own interpretation. A second rule runs through everything: no bot grades or verifies its own work.

The bots are named "P# (Category) Word". P# is the rollout phase (P1 to P5, all live since 16 Oct 2026), the category is one of Checks, Roles, ID, Ops or Work, and the word starts with the category's letter (S, A, I, M, E) — the naming scheme set out in `codex/RENAMES.md`. The codex folders keep the bots' original names (for example Scorer's folder is `assessor/`), so this document always shows both.

As the swarm's own brief for the external review admits, every bot shares one box and one set of Gem's connected accounts, so the limits are written rules rather than technical access controls. That point drives the oversight tooling in Part 6 and the redesign in Part 7.
""")
H(2,'1.1','The swarm brief (22 Oct 2026)','s-1-1',"""
The clearest single description of the whole system is the brief the swarm wrote for the external adversarial review on 22 Oct. It is reproduced here because it explains the phases, the digest, the approval chain, the key rulings, the connector limits and the recent incidents in one place. Part 7 covers what the reviewer said back.
""")
add(block(f'{G}/reviews/2026-10-22-swarm-brief-for-adversarial-review.md'))
H(2,'1.2','The codex: how instructions are stored','s-1-2',"""
The codex is the versioned library of every bot's instructions. Each bot has a folder holding numbered version files (`v001.md`, `v002.md`, …) and a `CHANGELOG.md`. Each version file carries a header (approver, source, status) and an "Exact instructions (verbatim)" block. Under R-023 the Status header is as-recorded, and the CHANGELOG is authoritative for deployment. Archivist keeps the codex and its index. The README and the index below explain the conventions; Part 5 reproduces the highest version of each bot.
""")
add(block(f'{G}/codex/README.md'))
add(block(f'{G}/codex/index.md'))
H(2,'1.3','Naming and renames','s-1-3',"""
Bots were renamed on 3 Oct to the "(Category) Word" pattern and given phase prefixes on 4 Oct. Folders and version files kept their old names, which is why codex paths don't match live names. This table is the key for reading old instruction text that still uses the original names.
""")
add(block(f'{G}/codex/RENAMES.md'))
H(2,'1.4','Collaboration map and role map','s-1-4',"""
The collaboration map is a shared design document (approved by Gem on 4 Oct) describing how the bots hand work to each other. The role map proper lives under `cartography/`, which Archivist has kept since 9 Oct; only the latest README and findings are included here, as the diagrams are images and earlier versions are history.
""")
add(block(latest(f'{G}/codex/_shared/collaboration-map')))
cart=max([f for f in os.listdir(f'{G}/cartography') if re.fullmatch(r'README-v\d+\.md',f)],key=lambda f:int(re.findall(r'\d+',f)[0]))
add(block(f'{G}/cartography/{cart}',ver=cart.split('-')[1][:-3]))
fnd=max([f for f in os.listdir(f'{G}/cartography') if re.fullmatch(r'findings-v\d+\.md',f)],key=lambda f:int(re.findall(r'\d+',f)[0]))
add(block(f'{G}/cartography/{fnd}',ver=fnd.split('-')[1][:-3]))

H(1,'Part 2','Phases, roster and operating rhythm','part-2',"""
The swarm was switched on in five phases, each started by Gem's own words: P1 on 3 Oct, P2 on 4 Oct, P3 and P4 on 15 Oct at 11:30pm, and P5 on 16 Oct at 11:47am. `phases.md`, kept by Explorer, is the source of truth for which bots are live, and under R-021 it wins over `directory.md` when the two disagree. There are 12 active bots since Gem retired Mediator, Scorer, Safekeeper, Inquirer and Extractor at 10:40pm on 22 Oct (\"Yes, retire all five now\"); `phases.md` hasn't caught up yet (Appendix D).

This part also covers the swarm's daily rhythm: the schedule Mender owns, the combined daily digest Explorer compiles, the state record of the weekday chain, and the handover note from when the fresh Explorer took over.
""")
H(2,'2.1','Phase tracker','s-2-1',"""
The phase tracker records which bots belong to each phase, when each phase went live and Gem's exact words for each switch-on. It also records the 9 Oct retirements and merges. Bots' name prefixes must match it.
""")
add(block(f'{G}/phases.md'))
H(2,'2.2','Schedule (run order and timing)','s-2-2',"""
`schedule.md` is Mender's record of when each bot runs and in what order. It matters because the weekday chain only works if each step runs after the one it depends on. The platform billing stop from about 16–22 Oct (INC-009) silently halted these routines, which is part of why the local watchdog in Part 6 exists.
""")
add(block(f'{G}/schedule.md'))
H(2,'2.3','Combined daily digest','s-2-3',"""
Gem asked on 10 Oct for one combined daily summary instead of separate messages. Each bot writes a short note to `digest/inbox/<date>/<Bot>.md`, and Explorer combines them at 7:41am Brisbane time. The compiling rules added on 16 Oct stop Explorer reporting any bot from memory. The watchdog (Part 6) checks that the digest went out.
""")
add(block(f'{G}/digest/README.md'))
H(2,'2.4','State record and search index','s-2-4',"""
Mender keeps the state record: a daily chain file showing how far the Scorer → Scrutineer → Architect → approver → Archivist chain got, and an `open.md` of stalls. The search index folder is deliberately empty for now, with its reasons recorded.
""")
add(block(f'{G}/state/README.md')); add(block(f'{G}/state/open.md')); add(block(f'{G}/index/README.md'))
H(2,'2.5','Explorer handover (9 Oct 2026)','s-2-5',"""
When Gem created a fresh Explorer copy on 9 Oct to save tokens, the old Explorer wrote this handover. It is the record of what the current Explorer inherited.
""")
add(block(f'{G}/handover/explorer-handover-2026-10-09.md'))

H(1,'Part 3','Authority, approvals and precedence','part-3',"""
This part is about who may decide what. Gem is the human authority. Since P4 went live on 15 Oct, Imitator may approve on Gem's behalf within R-019, but never spending money or drastic or irreversible steps, never changes to itself or to the five bots that check it, and never anything that widens its own role (R-015, R-027, R-028). Architect drafts but never approves; Archivist records and deploys but never approves; Arbiter rules on precedence but never approves.

The rulings file is the case law of the swarm. Each R-numbered ruling answers a specific conflict that a review or incident raised, and later updates, amendments and "final" entries refine them. The approvals records hold Gem's exact words, which R-029 requires to be recorded before any deploy, and R-008 governs approvals that only arrive through a relay.
""")
H(2,'3.1','Arbiter rulings (R-001 to R-053)','s-3-1',"""
The full rulings file is reproduced verbatim. Superseded rulings are kept and marked, so reading it top to bottom shows how authority moved: from the Arbiter and Assembler in early October to Gem and then Imitator, the deploy routes (R-010 and its 16 Oct update), the deletion and publishing rulings (R-031 to R-034), the gvmw public-repo rulings (R-040 to R-043), and the 22 Oct rulings on Imitator's veto and the redesign (R-044 to R-053).
""")
add(block(f'{G}/rulings.md'))
H(2,'3.1a','Rulings in force, R-054 and history annex','s-3-1a',"Arbiter's three new rulings files (22 Oct, about 10:15–10:26pm): the current reference of rulings in force, R-054 consolidating approval authority, and the annex holding superseded text and amendment history.")
for f in ['in-force.md','R-054-approval-authority.md','annex-history.md']: add(block(f'{G}/rulings/{f}',ver='current'))
H(2,'3.2','Approvals register','s-3-2',"""
`approvals.md` is the running register of approvals. It complements the dated files of Gem's direct words below.
""")
add(block(f'{G}/approvals.md'))
H(2,'3.3',"Gem's direct words, by date",'s-3-3',"""
These files hold Gem's exact words for each approval, with times, and are the evidence that a deploy was authorised (R-029). The 22 Oct file was re-recorded after the box restart lost the first copy (INC-008). The 3 Oct batch review is the earliest approval record.
""")
for f in sorted(glob.glob(f'{G}/approvals/*.md')):
    n=os.path.basename(f)[:-3]
    H(3,'3.3.'+str(sorted(glob.glob(f'{G}/approvals/*.md')).index(f)+1),n,'s-3-3-'+n,f"The approval record `{os.path.basename(f)}`, kept verbatim so the exact wording and timing behind each decision can be checked.")
    add(block(f))
H(2,'3.4','Pending items for Arbiter and Assembler','s-3-4',"""
These two codex files are queues of questions raised for the Arbiter and the (now retired) Assembler. They're included because several early rulings cite their item numbers (for example R-001 cites PENDING-FOR-ARBITER B1).
""")
add(block(f'{G}/codex/PENDING-FOR-ARBITER.md')); add(block(f'{G}/codex/PENDING-FOR-ASSEMBLER.md'))

H(1,'Part 4','Shared rules','part-4',"""
Shared rules live in `codex/_shared/` and bind every bot, whatever its own brief says. They aren't profiles, so there's nothing to deploy; they take effect when recorded with Gem's approval. Only the highest recorded version of each is included. The most important is the connector limits (v002, owned by Safeguard), which set what each bot may do with Gem's connected accounts. Its highest recorded version is shown below. Gem picked Variant A of v003 at 9:28pm on 22 Oct.

`connectors.md` sits alongside them as the inventory of connected services, which the limits refer to.
""")
SH=[('connector-limits','Connector limits (RR-028)',"The connector limits cover every connector and account: who may post, deploy, share, send, delete or spend, and what counts as \"Gem's direct words\". Safeguard owns them. They exist because every bot can technically reach every account, so the only limits are these written ones."),
('message-verification-rule','Message verification and safety rule',"This rule tells every bot how to treat incoming messages and relayed instructions: what to verify, when a relay counts, and Archivist's narrow deploy exception for Imitator-approved versions (added in v004)."),
('confirm-deployment','Confirming your own deployed instructions (R-009)',"This short rule, from Arbiter's R-009, tells a bot how to check that the instructions it is running match the approved codex version, and that unapproved drafts are not binding."),
('handoff-phase1','Phase-gate handoff spec',"The handoff spec defines how work and responsibilities pass when a phase gate opens. It dates from the 4 Oct design and some of its references to retired bots are read through R-002 and R-017."),
('github','Shared GitHub rule',"The shared GitHub rule (recorded 22 Oct after Gem's 9:27pm approval in Archivist's chat) sets how bots may use GitHub and the GitHub connectors. Until it was recorded, the connector limits kept GitHub-xai read-only."),
('deterministic-checks','Deterministic checks',"The redesign's shared rule listing fixed, rule-based checks (hashes, API read-backs) that replace a bot's own judgement where possible, and who audits each check."),
('approval-objects','Approval objects',"The redesign's shared rule for structured approvals tied to a hash of the exact text approved. It starts in shadow mode for a week before becoming required for deploys."),
('resilience','Resilience',"The redesign's shared rule for surviving box loss: archive-first changes, backups (free storage only, such as Google Drive) and recovery steps."),
('collaboration-map','Collaboration map',"Already reproduced in section 1.4; listed here for completeness as a shared entry. See [1.4](#s-1-4).")]
for i,(fd,t,p) in enumerate(SH,1):
    lp=latest(f'{G}/codex/_shared/{fd}')
    H(2,f'4.{i}',t+f' — {os.path.basename(lp)[:-3]}',f's-4-{i}',p)
    if fd!='collaboration-map': add(block(lp))
H(2,f'4.{len(SH)+1}','Connectors inventory','s-4-conn',"The list of connected services and accounts the limits apply to. Contact addresses are redacted.")
add(block(f'{G}/connectors.md'))

H(1,'Part 5','Bot instructions','part-5',"""
This part reproduces each bot's full latest instruction file, verbatim, from the highest-numbered version in its codex folder. Bots are grouped by category: Checks, Roles, ID, Ops and Work. Each subsection gives the bot's live name, id, phase and codex folder, a short note on its role, a note on whether the live profile description matches the codex text, and then the version file itself.

The codex keeps every earlier version too, but those are history and are left out on purpose. A final section covers retired bots. Their latest codex text is kept for reference only: none of it is in force.
""")
grp_order=['Checks','Roles','ID','Ops','Work']
gprose={'Checks':"The Checks group is the swarm's quality and safety layer: scoring, auditing, risk and secrets. Four of the five bots that check Imitator sit here (Investigator is the fifth), so Gem alone approves changes to their briefs (R-027).",
'Roles':"The Roles group runs the governance machinery itself: drafting instructions (Architect), recording and deploying them (Archivist), and ruling on conflicts (Arbiter). None of the three approves anything.",
'ID':"The ID group models Gem so that Imitator can decide on Gem's behalf: Inferer asks and organises (it absorbed Inquirer on 22 Oct), Investigator weighs evidence and checks Imitator, and Imitator decides within R-019.",
'Ops':"The Ops group keeps the swarm running. Since 22 Oct it is Mender alone: scheduling, routing, state, stalls, and (absorbed from Mediator) connector health and spend.",
'Work':"The Work group does the outward-facing work Gem actually wants done: Explorer as front door, Emissary for real-world tasks, research (absorbed from Extractor on 22 Oct) and the only external poster, and Engineer for code."}
def norm(s): return re.sub(r'\s+',' ',s or '').strip()
botrows=[]
for gi,g in enumerate(grp_order,1):
    H(2,f'5.{gi}',f'{g} group','s-5-'+g.lower(),gprose[g])
    for bi,(gg,name,bid,fd,dv,ph,prose) in enumerate([a for a in ACTIVE if a[0]==g],1):
        lp=latest(f'{G}/codex/{fd}'); v=os.path.basename(lp)[:-3]
        prof=profiles.get(bid); ct=codex_text(lp)
        if prof is None: pnote="No live profile.json was found for this id."; st='profile missing'
        else:
            pn,pdsc=prof; same = ct is not None and norm(ct)==norm(pdsc)
            st='match' if same else 'DIFFERS'
            pnote=f"Live profile name: \"{pn}\". Live description {'matches the codex '+v+' verbatim text exactly (whitespace-normalised).' if same else 'does NOT match the codex '+v+' verbatim text; the live description is reproduced below for comparison.'}"
            if not same: conflicts.append(f"{name}: live profile description differs from codex {fd}/{v}")
            if pn!=f'{ph} ({g}) {name}': conflicts.append(f"{name}: live profile name \"{pn}\" differs from phase-based name \"{ph} ({g}) {name}\"")
        if dv!=v: conflicts.append(f"{name}: directory.md says codex {fd} {dv}, highest codex file is {v}; index.md mentions: "+(", ".join(sorted(set(re.findall(fd+r"/(v\d+)",rd(G+"/codex/index.md")))))or "none"))
        cl=rd(f'{G}/codex/{fd}/CHANGELOG.md'); dep='not stated in CHANGELOG'
        for mm in re.finditer(r'(PENDING-DEPLOY|DEPLOYED) (v\d+)\.md',cl): dep=f'{mm.group(1)} {mm.group(2)}'
        if dep==f'PENDING-DEPLOY {v}' and st=='DIFFERS': st='DIFFERS (expected: recorded, not yet deployed)'; conflicts[[i for i,c in enumerate(conflicts) if c.startswith(name+': live profile description')][-1]]+=' (CHANGELOG: recorded, PENDING-DEPLOY; the live profile still runs the previous version)'
        elif st=='DIFFERS': conflicts[[i for i,c in enumerate(conflicts) if c.startswith(name+': live profile description')][-1]]+=f' (CHANGELOG last status: {dep})'
        botrows.append((name,g,ph,bid,fd,v,st))
        H(3,f'5.{gi}.{bi}',f'{ph} ({g}) {name}',f'bot-{name.lower()}',f"""
{prose}

- **Id:** `{bid}` · **Phase:** {ph} · **Codex folder:** `codex/{fd}/` · **Latest version:** {v}{'' if dv==v else f' (directory.md still says {dv})'}
- **Deploy status (CHANGELOG):** {dep}
- **Live profile:** {pnote}
""")
        add(block(lp))
        if prof and st=='DIFFERS':
            add(f"\n:::::::::: {{.source-block .live}}\n::: {{.source-label}}\n**LIVE PROFILE DESCRIPTION** · `/home/box/agent-data/agents/{bid}/profile.json` (description only)\n:::\n\n{demote(scrub(prof[1]),4)}\n\n::::::::::\n")
            index.append((f'/home/box/agent-data/agents/{bid}/profile.json','live'))
H(2,'5.6','Retired and superseded bots','s-5-retired',"""
These bots are no longer active. Thirteen were retired on 4 Oct, six on 9 Oct, two were superseded by fresh-context copies, and the blank "New Bot" was retired on 22 Oct. Their duties went to the bots named in each entry. Each subsection shows the last codex text the bot had, so readers can trace where a duty came from. **None of this text is in force.**
""")
for ri,(name,g,bid,fd,when,note) in enumerate(RETIRED,1):
    anc='bot-retired-'+re.sub(r'[^a-z0-9]+','-',name.lower()).strip('-')
    lp=latest(f'{G}/codex/{fd}') if fd else None
    H(3,f'5.6.{ri}',f'{name} (retired {when})',anc,f"Former ({g}) bot, id prefix `{bid}`. Retired {when} 2026: {note}. {'Latest codex file: `codex/'+fd+'/'+os.path.basename(lp)+'`.' if lp else 'There is no codex folder for this bot.'}")
    if lp and fd!='identity-inquirer': add(block(lp))
    botrows.append((name,g,'retired',bid,fd or '-',os.path.basename(lp)[:-3] if lp else '-','retired'))

H(1,'Part 6','Oversight and safety infrastructure','part-6',"""
Written rules only work if someone notices when they're broken or when the swarm stops. The 22 Oct events made that plain: an unpaid platform invoice stopped every scheduled routine for about six days without anyone noticing (INC-009), and a box restart lost and recreated the governance folder (INC-008). The infrastructure here was installed locally on 22 Oct in response. A liveness watchdog checks that the daily outputs appear. An append-only hash-chained ledger records events. Nightly snapshots back up the governance folder. A heartbeat push acts as an off-box dead-man signal.

All of it is local to the box. Gem scrapped the healthchecks.io idea at 8:28pm on 22 Oct ("Scrap health checks.io"), so independence from the box is only partly met, as the redesign notes admit. The risk register, the incident log and the threat register round out the picture.
""")
H(2,'6.1','Watchdog, ledger, snapshot and scheduler','s-6-1',"""
The watchdog README is the operating manual for the local tools: what the watchdog checks and by when, how the ledger chains its lines, where snapshots go, the schedule (9:30am and 9:30pm watchdog runs, 2:00am snapshot), and the one-line off switches. The scheduler doesn't survive a reboot.
""")
add(block(f'{W}/README.md'))
H(3,'6.1.1','Scheduler script','s-6-1-1',"The shell loop that runs the watchdog and snapshot on schedule, because the box has no cron or systemd user services.")
add(block(f'{W}/scheduler.sh'))
H(3,'6.1.2','Heartbeat (dead-man signal)','s-6-1-2',"""
`heartbeat.sh` pushes a UTC timestamp to a private GitHub repo, so a missing heartbeat can show the box has stopped. A comment in `watchdog.py` says the off-box version should rely on a missing heartbeat, a dead man's switch. Gem's 22 Oct words record Engineer's claim that "the GitHub dead-man check is live and its test run passed". Archivist noted that this was relayed by Gem and not verified. The script fetches a credential at run time; no credential value is included here.
""")
add(block(f'{W}/heartbeat.sh'))
H(3,'6.1.3','Watchdog and snapshot code','s-6-1-3',"The Python sources for the watchdog and snapshot tools, included so the checks described above can be read exactly.")
add(block(f'{W}/watchdog.py')); add(block(f'{W}/snapshot.py'))
H(2,'6.2','Provenance ledger','s-6-2',"""
There is no ledger README; the ledger is described in the watchdog README (section 6.1). `events.jsonl` is append-only, and each line chains the hash of the previous line, so tampering shows up when `ledger.py verify` runs. Only the code is reproduced here, not the event lines.
""")
add(block(f'{G}/ledger/ledger.py'))
for f,t,p in [('risk/2026-10-22-liveness-watchdog-plan.md','Liveness watchdog plan',"The plan behind the watchdog: why it was needed after the silent billing stop and what it should check."),
('risk/2026-10-22-governance-snapshot-plan.md','Governance snapshot plan',"The plan behind the nightly snapshots and the backup rules, written after the governance folder was lost in the 22 Oct restart."),
('risk/2026-10-22-destructive-ops-gate.md','Destructive-operations gate',"Deletions have been the most common kind of breach. This plan proposes a gate in front of destructive operations. Gem's answer on the deletion gate in R-051 was \"Not now\"."),
('risk/2026-10-22-local-install-status.md','Local install status',"The record of what was actually installed on the box on 22 Oct, and what wasn't."),
('risk/2026-10-22-gvmw-audit.md','gvmw public repo audit',"The audit of the public gemquota/gvmw snapshot repo, which the rulings R-040 to R-043 deal with. Personal details are redacted.")]:
    n=len([x for x in toc if x[1].startswith('6.')])
    H(2,f'6.{[x[1] for x in toc if x[0]==2 and x[1].startswith("6.")].__len__()+1}',t,'s-6-'+os.path.basename(f)[:-3],p); add(block(f'{G}/{f}'))
k=len([x for x in toc if x[0]==2 and x[1].startswith('6.')])
H(2,f'6.{k+1}','Risk register','s-6-risk',"Safeguard's running register of risks (RR-numbered items cited throughout the rulings).")
add(block(f'{G}/risk/register.md'))
H(2,f'6.{k+2}','Incident log','s-6-incidents',"Mender's incident log (INC-numbered), including the 9 Oct agent-folder disappearance, the 13 Oct silence, the 22 Oct platform stop and the restart. Individual incident files are listed in Appendix C.")
add(block(f'{G}/incidents/log.md'))
H(2,f'6.{k+3}','Threat register and verification log','s-6-security',"Safekeeper's threat register and the security verification log. The secrets inventory is deliberately excluded.")
add(block(f'{G}/security/threat-register.md')); add(block(f'{G}/security/verification-log.md'))

H(1,'Part 7','Reviews and the redesign (deployed 22 Oct)','part-7',"""
On 22 Oct Gem pasted an external adversarial review into the swarm. Its verdict was "interesting governance prototype, unsafe production architecture". Gem's answer was "Both": send it to Architect and Arbiter for a response plan, and start the P0 fixes. The result is the 22 Oct redesign batch, which merges Mediator, Scorer, Safekeeper, Inquirer and Extractor into surviving bots and adds three new shared rules (deterministic checks, approval objects and resilience).

**Status as at about 10:45pm AEST, 22 Oct:** Gem approved the redesign at 9:27pm. The seven briefs were deployed from about 10:18 to 10:21pm and verified, and the three shared rules are recorded in `codex/_shared/` (Part 4). Gem retired the five merged bots at 10:40pm, and their folders are kept. **The redesign is deployed.** Sections 7.3 and 7.4 keep the proposal copies as history. Architect's follow-up clarity batch is drafted but not approved.""")
H(2,'7.1','External adversarial review','s-7-1',"The summary of the outside reviewer's findings as Gem pasted them, the starting point for the redesign.")
add(block(f'{G}/reviews/2026-10-22-external-adversarial-review.md'))
H(2,'7.2','22 Oct daily review and redesign reviews','s-7-2',"Scrutineer's daily review for 22 Oct and the reviews of redesign revisions 2 and 3, which shaped the frozen drafts.")
for f in ['reviews/2026-10-22.md','reviews/2026-10-22-redesign-r2-review.md','reviews/2026-10-22-redesign-r3-review.md']:
    if os.path.exists(f'{G}/{f}'): add(block(f'{G}/{f}'))
H(2,'7.3','Redesign batch README','s-7-3',"The redesign's own account of Gem's 14 answers, the hashes, record and migration order, open items and risk notes. **APPROVED 9:27pm, NOT DEPLOYED.**")
add(block(f'{G}/proposals/2026-10-22-redesign/README.md'))
H(2,'7.4','Redesign draft briefs and shared rules (proposal copies)','s-7-4',"The frozen draft texts as proposed. The seven bot briefs are now recorded in the codex (Part 5), pending deploy; the three shared rules are not yet recorded. Version numbers skip unrecorded drafts, as the README explains. **None of these is in force.**")
for i,f in enumerate(sorted(glob.glob(f'{G}/proposals/2026-10-22-redesign/*-v*.md')),1):
    n=os.path.basename(f)[:-3]
    H(3,f'7.4.{i}',f'{n} — proposal copy, NOT DEPLOYED','s-7-4-'+n,f"Draft `{os.path.basename(f)}` from the redesign batch, as proposed. It is not live.")
    add(block(f))
H(2,'7.5','Other architecture and design documents','s-7-5',"Earlier whole-swarm design and assessment documents that explain why the structure looks the way it does: the bot landscape review, the 10 Oct governance I/O report, the 15 Oct authority and responsibility review, and the 9 Oct value review that led to the retire/merge list.")
for f in ['bot-landscape-review.md','reviews/2026-10-10-governance-io-report.md','reviews/2026-10-15-governance-authority-responsibility.md','reviews/2026-10-09-explorer-bot-value-review.md']:
    add(block(f'{G}/{f}'))

H(1,'Appendix A','Bot directory','app-a',"""
The bot directory, kept by Archivist, lists every active, superseded and retired bot by id. It is reproduced verbatim, followed by a cross-reference table built for this document. The table shows each bot's section here, its latest codex version, and whether its live profile matches.
""")
add(block(f'{G}/directory.md'))
rows="\n| Bot | Group | Phase | Id | Codex folder | Latest | Live profile vs codex | Section |\n|---|---|---|---|---|---|---|---|\n"
for (n,g,ph,bid,fd,v,st) in botrows:
    anc=[x[3] for x in toc if x[0]==3 and (x[2].endswith(') '+n) or x[2].startswith(n+' (retired'))]
    rows+=f"| {n} | {g} | {ph} | `{bid[:8]}` | {fd} | {v} | {st} | [{'link'}](#{anc[0] if anc else ''}) |\n"
add(rows)
H(1,'Appendix B','Glossary','app-b',"Short definitions of terms used across the sources. Each is drawn from the documents above.")
add("""
| Term | Meaning (from the sources) |
|---|---|
| Gem | Gem Quota, the human authority over the swarm. |
| Codex | Versioned library of bots' instructions under `codex/`, kept by Archivist. |
| Brief | A bot's instruction text. |
| Phase (P1–P5) | Rollout stage; Gem starts each. All five live since 16 Oct 2026. |
| R-xxx | An Arbiter ruling in `rulings.md`. |
| RR-xxx | An item in Safeguard's risk register. |
| INC-xxx | An incident in Mender's incident log. |
| Dry run | Safeguard's prediction of what a risky step would do; never itself a go-ahead. |
| Direct words | Gem's own words in that bot's own chat or a voice call (connector limits). |
| Relay | An approval passed on by another bot; governed by R-008. |
| Weekday chain | Scorer → Scrutineer → Architect → approver (Imitator or Gem) → Archivist. |
| Digest | Explorer's combined daily summary from `digest/inbox/`. |
| Connector limits | Shared rules for every connected account, owned by Safeguard. |
| BIE | Extractor's gambling-industry research project; data held on the box (R-031); excluded here. |
| gvmw | `gemquota/gvmw`, a public whole-workspace snapshot repo (R-040–R-043). |
| Watchdog | Local liveness checker in `/workspace/watchdog` (22 Oct). |
| Ledger | Append-only hash-chained event log, `ledger/events.jsonl`. |
| Dead-man check | Heartbeat-based signal that fires when the box stops reporting. |
| Approval objects | Proposed (pending) shared rule for structured, hash-bound approvals. |
""")
H(1,'Appendix C','Source file index','app-c',"Every file reproduced in this document, with the version used. Files that were consulted but not reproduced (the individual incident files, the cartography diagrams, older codex versions, proposals other than the 22 Oct redesign) are omitted on purpose. Backups (`_archive`, `*.bak*`, `_pre*`, `_r1`–`_r3`), BIE data and `secrets-inventory.md` were skipped.")
seen=[];tab="\n| # | Path | Version | Bytes | sha256 (12) |\n|---|---|---|---|---|\n"
for p,v in index:
    if p in seen: continue
    seen.append(p); b=open(p,'rb').read()
    tab+=f"| {len(seen)} | `{p}` | {v} | {len(b)} | {hashlib.sha256(b).hexdigest()[:12]} |\n"
add(tab)
H(1,'Appendix D','Conflicts and gaps found while compiling','app-d',"Mismatches spotted while building this document. They are reported, not fixed, because the sources were read-only.")
conflicts[:0]=STALE
add('\n'+'\n'.join('- '+c for c in conflicts)+'\n')
# TOC
t=["## Table of contents {#toc .unnumbered}\n"]
for lv,num,title,a in toc:
    t.append('    '*(lv-1)+f"- [{num} {title}](#{a})")
doc=''.join(out).replace('TOC_PLACEHOLDER','\n'.join(t))
open(f'{G}/master/governance-master-2026-10-22.md','w').write(doc)
json.dump({'toc':toc,'conflicts':conflicts,'redactions':red['n'],'bots':botrows},open('/workspace/.master_meta.json','w'))
print(len(doc),red['n'],len(conflicts)); print('\n'.join(conflicts))

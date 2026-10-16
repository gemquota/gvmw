#!/usr/bin/env python3
"""Builds role-graph.json for role map v2 (3 Oct 2026).
Sources: codex v001 files (where they exist) and /workspace/governance/directory.md
(groups, super-groups, Council, leads, and the 8 new bots). Every edge cites its source."""
import json, os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = "/workspace/governance/codex/"
DIR = "/workspace/governance/directory.md"
PROP = "/workspace/governance/proposals/auditor-v002.md"
def src(*slugs): return [C + s + "/v001.md" for s in slugs]

SUPER = {"OVERSIGHT": "Oversight", "IDENTITY": "Identity", "RUNTIME": "Runtime"}
GROUPS = [  # key, name, channel id, super-group, lead key
 ("IG",  "Instruction Governance", "e417910e-5e1e-41b8-94ec-ed80f2f1e498", "OVERSIGHT", "RC"),
 ("ASR", "Assurance",              "b10e394f-5e67-48dd-97a9-e1df58f41d13", "OVERSIGHT", "AU"),
 ("IDG", "Identity",               "0ecaea40-3f1a-47d7-9976-b66821b5491f", "IDENTITY",  "IF"),
 ("OPS", "Operations",             "638e3cab-354d-4496-8a01-17f3179d2150", "RUNTIME",   "OC"),
 ("DEL", "Delivery",               "3e9d6a26-a614-45da-8fce-e4811c0d2f7c", "RUNTIME",   "GGG"),
]
COUNCIL_ID = "4dd4fd18-d34c-4fc2-baa6-222acb567058"
G = {g[0]: g for g in GROUPS}

N = [  # id, name, key, group key, slug (codex folder), v1 role label
 ("82a2c15a-2694-4ac2-b2f4-f7f463f85fce","Genesis Gang God","GGG","DEL","genesis-gang-god"),
 ("61ef3abd-87b8-49f1-b8d6-b52969afa315","Codex Keeper","CK","IG","codex-keeper"),
 ("51af1200-ca1a-45ff-8350-848091e00f96","Instruction Architect","IA","IG","instruction-architect"),
 ("d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4","Role Cartographer","RC","IG","role-cartographer"),
 ("b3f6515c-d3fe-4beb-9b86-45016711c65d","Governance Continuity Deputy","GCD","IG","governance-continuity-deputy"),
 ("050a12c9-e300-48b4-b318-425627cbc34b","Assessor","AS","ASR","assessor"),
 ("affe0344-6b5f-4251-8ecb-3e23dfa5db3c","Auditor","AU","ASR","auditor"),
 ("3661a899-2768-4a77-a95a-71d0251813bc","Compliance & Risk Officer","CRO","ASR","compliance-risk-officer"),
 ("52772b1d-4a85-4ea3-ae15-f3912c901a3b","Secrets & Credentials Custodian","SCC","ASR","secrets-credentials-custodian"),
 ("6ae584b8-eaac-429b-9eae-d5e3e6f6a32b","Clone","CL","IDG","clone"),
 ("e613112b-b653-4567-bc4f-17261ce9302e","Identity Inquirer","IQ","IDG","identity-inquirer"),
 ("94516ca6-6355-43c5-b387-d2b605057784","Identity Inferer","IF","IDG","identity-inferer"),
 ("d3191aa8-3ad6-4763-b4e4-c7c648acc9ba","Clone Accuracy Validator","CAV","IDG","clone-accuracy-validator"),
 ("f3810109-17a5-427f-9148-d58f645658e3","Orchestration Conductor","OC","OPS","orchestration-conductor"),
 ("f8b83b15-0ea1-4f99-9550-c3b8607ba999","Cost & Budget Sentinel","CBS","OPS","cost-budget-sentinel"),
 ("90f9eb20-ff8f-456b-b94f-cc11bb33fc29","Connector Steward","CS","OPS","connector-steward"),
 ("5e47d344-1369-423a-b072-2e5277934022","Comms Concierge","CC","OPS","comms-concierge"),
 ("28cf987d-ee94-4839-a6d3-33c04a11b9d6","Grok Bot","GB","DEL","grok-bot"),
 ("f8e3fdc6-ee60-410e-bdb7-d437fc1500d1","Codey","CO","DEL","codey"),
 ("febac500-d854-4dc7-a6a7-23b3feb07f80","Scraper","SC","DEL","scraper"),
 ("de808331-3c00-41f5-a3a4-4ae1f8f6f0ba","Swarm Builder","SB","DEL","swarm-builder"),
]
NEW = {"GCD","CRO","SCC","CAV","OC","CBS","CS","CC"}
V1_STATUS = {"GGG":"partial: no Rules or Limits","CK":"complete","IA":"complete","RC":"complete",
 "AS":"complete","AU":"complete (no separate Scope); v002 proposed, awaiting Gem","CL":"complete","IQ":"complete",
 "IF":"complete (no separate Scope)","SB":"partial: no Relationships","GB":"gap: one-line tagline only",
 "CO":"gap: no instructions","SC":"gap: no instructions",
 "GCD":"complete","CRO":"complete","SCC":"partial: no Rules section","CAV":"partial: no Rules section",
 "OC":"complete (limits only on contacting Gem)","CBS":"complete (no budget set yet)","CS":"partial: no Rules section","CC":"complete"}
K = {n[2]: n for n in N}
K["GEM"] = ("gem","Gem Quota","GEM",None,None)
K["COUNCIL"] = (COUNCIL_ID,"Council","COUNCIL",None,None)
LEADS = {g[4] for g in GROUPS}

def codex_file(slug):
    p = C + slug + "/v001.md"
    return p if os.path.exists(p) else None

nodes = [{"id":"gem","name":"Gem Quota","key":"GEM","type":"human"},
         {"id":COUNCIL_ID,"name":"Council","key":"COUNCIL","type":"council",
          "members":[K[g[4]][0] for g in GROUPS],
          "purpose_per_directory":"Cross-group issues; leads relay decisions back to their group.","source":[DIR]}]
for i,nm,k,gk,slug in N:
    cf = codex_file(slug)
    nodes.append({"id":i,"name":nm,"key":k,"type":"bot","new_in_v2":k in NEW,
        "group":G[gk][1],"group_id":G[gk][2],"super_group":SUPER[G[gk][3]],
        "group_lead":k in LEADS,"council_member":k in LEADS,
        "coordinator_of_all_groups": k=="GGG",
        "codex": cf, "codex_status": ("v001" if cf else "pending codex"),
        "instruction_status": V1_STATUS.get(k, "pending codex (directory only)" if not cf else "v001 recorded; see codex"),
        "pending_proposals": ({"AU":[PROP],"CO":["/workspace/governance/proposals/codey.md"],"GB":["/workspace/governance/proposals/grok-bot.md"],"SC":["/workspace/governance/proposals/scraper.md"]}.get(k,[]))})

E = []
def e(f, t, rel, sources, **kw):
    ft = K[f]; d = {"from": ft[0], "from_name": ft[1]}
    if t in G: d.update({"to": G[t][2], "to_name": G[t][1]+" (group)"})
    else: d.update({"to": K[t][0], "to_name": K[t][1]})
    d.update({"relation": rel, "source": sources, "status": kw.pop("status","current")}); d.update(kw); E.append(d)

# --- Structure (directory.md) ---
for gk,gname,gid,sg,lead in GROUPS:
    e(lead,"COUNCIL","sits on Council as lead of "+gname,[DIR],kind="council")
    e("COUNCIL",lead,"relays Council decisions via (to "+gname+")",[DIR],kind="council")
    for i,nm,k,g2,slug in N:
        if g2==gk and k!=lead: e(lead,k,"leads (group: "+gname+")",[DIR],kind="group-lead")
for gk in G:
    if gk!="DEL": e("GGG",gk,"coordinates (sits in every group)",[DIR],kind="coordination")

# --- Working relationships from codex v001 (unchanged from v1) ---
e("IA","RC","proposes instructions to",src("instruction-architect","role-cartographer"),flow="governance-approval")
e("RC","CK","approves for (sends approved proposals to record)",src("role-cartographer","codex-keeper"),flow="governance-approval")
e("RC","IA","returns rejected proposals to (with reasons)",src("role-cartographer","instruction-architect"),flow="governance-approval")
e("RC","GEM","escalates to (Architect disagreement; any governance-bot change)",src("role-cartographer","instruction-architect"),flow="governance-approval")
e("CK","GEM","records direct edits from (Gem may edit directly)",src("codex-keeper"))
for t in ["IA","RC","AS","AU"]: e("CK",t,"gives instruction text on request to",src("codex-keeper"))
e("AS","AU","sends daily scores to",src("assessor","auditor"))
e("AS","GEM","flags serious problems and sends weekly scorecard to",src("assessor"))
e("AU","IA","sends performance reviews and urgent redesign requests to",src("auditor","instruction-architect"))
e("AU","RC","sends performance reviews to",src("auditor"))
e("AU","GEM","tells of a bot failing 3 reviews in a row",src("auditor"))
e("AU","CK","checks bots against instructions from",src("auditor"))
e("AU","RC","checks bots against role map and summaries of",src("auditor"))
e("IA","AU","reviews (Auditor's own work)",src("auditor"),status="current; would be removed by pending Auditor v002",
  note="Conflicts with Architect's 'don't check bots' work yourself' (instruction-architect/v001.md)")
e("GEM","AU","reviews (Auditor's own work) personally",[PROP],status="PROPOSED: Auditor v002, awaiting Gem's approval; not in codex")
e("IA","CL","asks preferences of",src("instruction-architect"))
e("AS","CL","asks preferences of",src("assessor"))
e("IQ","IF","sends raw answers to",src("identity-inquirer","identity-inferer"))
e("IF","IQ","asks for follow-ups, confirmations and conflict checks from",src("identity-inferer","identity-inquirer"))
e("IF","CL","sends profile updates to",src("identity-inferer","clone"))
e("CL","IF","logs unanswerable gaps with",src("clone","identity-inferer"))
e("IQ","GEM","asks question series of",src("identity-inquirer"))
e("CL","GEM","hands consequential decisions back to",src("clone"))
e("GGG","GEM","ranks second only to",src("genesis-gang-god"))
e("SB","GEM","needs spend/large-job approval from; reports costs to",src("swarm-builder"))

# --- Working relationships from codex v001 of the 8 new bots (recorded 3 Oct 2026) ---
e("GCD","IA","stands in for, when stalled (drafts proposals)",src("governance-continuity-deputy"),note="after 24 h, or 4 h for urgent items")
e("GCD","RC","stands in for, when stalled (reviews and approves)",src("governance-continuity-deputy"),note="Codex Keeper's instructions don't yet accept the Deputy as an approval source (codex index note)")
e("GCD","RC","spot-checks weekly sample of approvals of",src("governance-continuity-deputy"))
e("GCD","GEM","sends governance-bot changes to",src("governance-continuity-deputy"))
e("CRO","IA","proposes rule changes through",src("compliance-risk-officer"))
e("CRO","GEM","alerts about unsafe or non-compliant work",src("compliance-risk-officer"))
e("SCC","GEM","flags exposed secrets or loose permissions to",src("secrets-credentials-custodian"))
e("SCC","CRO","flags exposed secrets or loose permissions to",src("secrets-credentials-custodian"))
e("SCC","CK","watches access rules for the codex held by",src("secrets-credentials-custodian"))
e("CAV","CL","validates accuracy and confidence calibration of",src("clone-accuracy-validator"))
e("CAV","IQ","compares Clone against raw answers of; gives gaps to",src("clone-accuracy-validator"))
e("CAV","IF","sends findings to",src("clone-accuracy-validator"))
e("CAV","AU","sends findings to",src("clone-accuracy-validator"))
e("OC","AS","sequences (1st: daily run)",src("orchestration-conductor"),flow="daily-chain")
e("OC","AU","sequences (2nd: after Assessor)",src("orchestration-conductor"),flow="daily-chain")
e("OC","IA","sequences (3rd: after Auditor)",src("orchestration-conductor"),flow="daily-chain")
e("OC","GEM","contacts only when a chain is broken and unfixable",src("orchestration-conductor"))
e("CBS","GEM","drafts over-budget/runaway alerts for (never sends unapproved); asks for a budget",src("cost-budget-sentinel"))
e("CBS","AS","shares cost data with",src("cost-budget-sentinel"))
e("CBS","AU","shares cost data with",src("cost-budget-sentinel"))
e("CS","CO","watches integrations built by",src("connector-steward"))
e("CS","CC","tells (for Gem) when a connector needs reconnecting",src("connector-steward","comms-concierge"))
e("CC","GEM","sends one daily prioritised digest to",src("comms-concierge"))

# --- PROPOSED edges from pending Architect drafts in /workspace/governance/proposals/ (NOT current; not in codex) ---
PP = "/workspace/governance/proposals/"
PST = "PROPOSED: Architect draft, not yet approved or recorded"
e("GB","CO","would route repo code work to",[PP+"grok-bot.md"],status=PST)
e("GB","SC","would route web data collection to",[PP+"grok-bot.md"],status=PST)
e("GB","SB","would route swarm work to",[PP+"grok-bot.md"],status=PST)
e("GB","CL","would ask preferences of",[PP+"grok-bot.md"],status=PST)
e("GGG","CO","would give coding tasks to (on Gem's behalf)",[PP+"codey.md"],status=PST)
e("CO","GEM","would hand finished work to for acceptance",[PP+"codey.md"],status=PST)
e("CO","AS","would surface work for review to",[PP+"codey.md"],status=PST)
e("CO","AU","would surface work for review to",[PP+"codey.md"],status=PST)
e("GGG","SC","would give collection jobs to",[PP+"scraper.md"],status=PST)
e("GB","SC","would give collection jobs to",[PP+"scraper.md"],status=PST)
e("SC","CO","would hand scraping-tool code changes to",[PP+"scraper.md"],status=PST)
e("SC","GEM","would stop and ask before large, logged-in or legally doubtful jobs",[PP+"scraper.md"],status=PST)

# --- Fan-out from codex v001. Codex text says "every bot"/"all bots", so new bots are included. ---
BOTS = [n[2] for n in N]
for t in BOTS:
    nb = {"applies_to_new_bot": True} if t in NEW else {}
    if t!="CK": e("CK",t,"records instructions for",src("codex-keeper"),fanout="all bots",**nb)
    e("AS",t,"reviews",src("assessor"),fanout="all bots (governance included)",**nb)
    e("AU",t,"audits",src("auditor"),fanout="all bots",**nb)
    if t!="RC": e("RC",t,"assigns instruction sets to / maps",src("role-cartographer"),fanout="all bots",**nb)
    if t!="GGG": e("GGG",t,"runs / oversees (aspirational)",src("genesis-gang-god"),fanout="all bots",
                   note="Stated as 'tasked with running bots or bot groups'; no mechanism defined",**nb)
    if t!="CRO": e("CRO",t,"reviews risky actions of; may ask to pause",src("compliance-risk-officer"),fanout="all bots (GGG included)",**nb)
    if t!="SCC": e("SCC",t,"audits secrets storage and access of",src("secrets-credentials-custodian"),fanout="all bots",**nb)
    if t!="OC": e("OC",t,"controls run order and timing of; nudges when late",src("orchestration-conductor"),fanout="all bots' routines",**nb)
    if t!="CBS": e("CBS",t,"tracks spend of; may ask to pause costly work",src("cost-budget-sentinel"),fanout="all bots",**nb)
    if t!="CS": e("CS",t,"tells of connector problems (when affected)",src("connector-steward"),fanout="affected bots",**nb)
    if t!="CC": e("CC",t,"collects non-urgent updates from",src("comms-concierge"),fanout="all bots",**nb)

out = {"version":"v2, 3 Oct 2026","previous_version":"role-graph-v1.json (v1, 2 Oct 2026)",
  "maintainer":"Role Cartographer (d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4)",
  "basis":{"codex":"v001 for all 21 bots (8 new bots recorded 3 Oct 2026 at 02:43 AEST)",
           "directory":DIR,"pending_proposals":[PROP,"/workspace/governance/proposals/codey.md","/workspace/governance/proposals/grok-bot.md","/workspace/governance/proposals/scraper.md","/workspace/governance/proposals/collaboration-map.md"]},
  "super_groups":[{"key":k,"name":v,"groups":[g[1] for g in GROUPS if g[3]==k]} for k,v in SUPER.items()],
  "groups":[{"key":g[0],"name":g[1],"channel_id":g[2],"super_group":SUPER[g[3]],"lead":K[g[4]][1],"lead_id":K[g[4]][0],
             "members":[n[1] for n in N if n[3]==g[0]],
             "coordinator":"Genesis Gang God (sits in every group, per directory)"} for g in GROUPS],
  "council":{"id":COUNCIL_ID,"members":[K[g[4]][1]+" ("+g[1]+")" for g in GROUPS],"source":DIR},
  "nodes":nodes,"edges":E}
json.dump(out, open(os.path.join(OUT,"role-graph-v2.json"),"w"), indent=2, ensure_ascii=False)
print(len(nodes),"nodes",len(E),"edges; pending codex:",[n["name"] for n in nodes if n.get("codex_status")=="pending codex"])

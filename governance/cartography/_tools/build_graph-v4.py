#!/usr/bin/env python3
"""Role map v4 (9 Oct 2026). Builds role-graph.json from codex index + phases.md.
Maintained by P1 (Roles) Archivist (took cartography from retired Assembler).
Descriptive only — does not decide roles or approve anything."""
import json, os
from pathlib import Path

OUT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C = Path("/workspace/governance/codex")
G = Path("/workspace/governance")
PH = str(G / "phases.md")
IDX = str(C / "index.md")

PHASES = [
  {"phase":"P1","status":"LIVE (since 3 Oct 2026)",
   "members":["Mender","Scorer","Safeguard","Safekeeper","Archivist","Architect","Explorer (04dcca0d, active)","Explorer (82a2c15a, prior)"]},
  {"phase":"P2","status":"LIVE (started 4 Oct 2026, 3:12pm AEST)",
   "members":["Scrutineer","Arbiter","Inferer","Mediator","Inquirer (e613112b, recorded; not found live ~9:14am)"]},
  {"phase":"P3","status":"Dormant","members":["Investigator"]},
  {"phase":"P4","status":"Dormant","members":["Imitator"]},
  {"phase":"P5","status":"Dormant","members":["Emissary","Engineer","Extractor"]},
]

# Active / recorded nodes (key, name, category, id, phase, codex, notes, former, status_flag)
N = [
 ("MEN","Mender","Ops","c8401a53-136d-45f3-9e2d-e423ccdd08ac","P1","mender/v004.md",
  "Absorbed Minder (Oct 4) and Marshal (9 Oct). Owns schedule.md and state/.","(Ops) Mender","active"),
 ("SCO","Scorer","Checks","050a12c9-e300-48b4-b318-425627cbc34b","P1","assessor/v003.md",
  "Daily scoring; self-exclusion in v003.","Assessor","active"),
 ("SFG","Safeguard","Checks","3661a899-2768-4a77-a95a-71d0251813bc","P1","compliance-risk-officer/v004.md",
  "Pre-action risk review and dry runs; covers all phases (R-013).","Compliance & Risk Officer","active"),
 ("SFK","Safekeeper","Checks","52772b1d-4a85-4ea3-ae15-f3912c901a3b","P1","secrets-credentials-custodian/v004.md",
  "Secrets, threats, input cleaning; absorbed Sentinel threat/input duties.","Secrets & Credentials Custodian","active"),
 ("ARC","Archivist","Roles","61ef3abd-87b8-49f1-b8d6-b52969afa315","P1","codex-keeper/v005.md",
  "Codex + Google Doc mirror; took role map (/workspace/governance/cartography/) from Assembler on 9 Oct.","Codex Keeper","active"),
 ("ARX","Architect","Roles","51af1200-ca1a-45ff-8350-848091e00f96","P1","instruction-architect/v003.md",
  "Designs and rewrites instructions; proposes for Gem/Imitator approval.","Instruction Architect","active"),
 ("EXP","Explorer","Work","04dcca0d-1479-4e01-bf29-a13b4fc3c3a7","P1","explorer-copy/v001.md",
  "Active Explorer (fresh copy, 9 Oct). Merged Messenger digest duties. Display name P1 (Work) Explorer.","P1 (Work) Explorer copy","active"),
 ("EXP0","Explorer (prior)","Work","82a2c15a-2694-4ac2-b2f4-f7f463f85fce","P1","genesis-gang-god/v004.md",
  "Prior Explorer id; same display name. Records unchanged by four merges. Awaiting Gem on retirement of this id.","Genesis Gang God","active_prior"),
 ("SCR","Scrutineer","Checks","affe0344-6b5f-4251-8ecb-3e23dfa5db3c","P2","auditor/v003.md",
  "Audits vs instructions and environment reality; absorbed Surveyor.","Auditor","active"),
 ("ARB","Arbiter","Roles","2133048d-5ab9-4809-806c-218decdff8e6","P2","arbiter/v004.md",
  "Precedence rulings; never approves. Absorbed Adjudicator.","(Roles) Arbiter","active"),
 ("INF","Inferer","ID","94516ca6-6355-43c5-b387-d2b605057784","P2","identity-inferer/v002.md",
  "Structures identity details from Inquirer answers. Codex still names Inquirer e613112b.","Identity Inferer","active"),
 ("MED","Mediator","Ops","90f9eb20-ff8f-456b-b94f-cc11bb33fc29","P2","connector-steward/v004.md",
  "phases.md places Mediator in P2 (moved 9 Oct); live profile name still P4 (Ops) Mediator (rename unapplied). Absorbed Meter.","Connector Steward","active"),
 ("INQ","Inquirer","ID","e613112b-b653-4567-bc4f-17261ce9302e","P2","identity-inquirer/v002.md",
  "Recorded Inquirer in codex. Not found live since ~9:14am AEST 9 Oct 2026 (profile.json still on disk); awaiting Gem. Not treated as the official Inquirer.","Identity Inquirer","recorded_not_live"),
 ("INV","Investigator","ID","f2016e9b-ca8b-4783-8f53-f5765b0afe7b","P3","investigator/v002.md",
  "Identity evidence ladder; absorbed Interrogator (Imitator testing) on 9 Oct. Dormant until P3.","(ID) Investigator","dormant"),
 ("IMI","Imitator","ID","6ae584b8-eaac-429b-9eae-d5e3e6f6a32b","P4","clone/v004.md",
  "Identity understudy; delegated approver once P4 live (Gem until then). Absorbed Advocate.","Clone","dormant"),
 ("EMI","Emissary","Work","28cf987d-ee94-4839-a6d3-33c04a11b9d6","P5","grok-bot/v004.md",
  "General-purpose work bot. Dormant until P5.","Grok Bot","dormant"),
 ("ENG","Engineer","Work","f8e3fdc6-ee60-410e-bdb7-d437fc1500d1","P5","codey/v005.md",
  "Code and swarm work; absorbed Ensembler. Dormant until P5.","Codey","dormant"),
 ("EXT","Extractor","Work","febac500-d854-4dc7-a6a7-23b3feb07f80","P5","scraper/v003.md",
  "Research and web data collection. Dormant until P5.","Scraper","dormant"),
]

# Retired still-live (show with merge arrows)
RET = [
 ("MAR","RETIRED Marshal","Ops","f3810109-17a5-427f-9148-d58f645658e3",None,"orchestration-conductor/v005.md",
  "Retired 9 Oct into Mender. Live, awaiting Gem delete.","Orchestration Conductor","retired_live","MEN"),
 ("MSG","RETIRED Messenger","Ops","5e47d344-1369-423a-b072-2e5277934022",None,"comms-concierge/v004.md",
  "Retired 9 Oct into Explorer (04dcca0d). Live, awaiting Gem delete.","Comms Concierge","retired_live","EXP"),
 ("INT","RETIRED Interrogator","ID","d3191aa8-3ad6-4763-b4e4-c7c648acc9ba",None,"clone-accuracy-validator/v004.md",
  "Retired 9 Oct into Investigator. Live, awaiting Gem delete.","Clone Accuracy Validator","retired_live","INV"),
 ("ASM","RETIRED Assembler","Roles","d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4",None,"role-cartographer/v006.md",
  "Retired 9 Oct: role map → Archivist; approvals → Gem until P4, then Imitator. Live, awaiting Gem delete.","Role Cartographer","retired_live","ARC"),
 ("SRC","RETIRED Sourcer","Checks","2fe3e92f-4f39-4e9f-a56b-811438928f5b",None,"sourcer/v002.md",
  "Retired outright 9 Oct 9:11am (Gem confirmed 9:13am). Live, awaiting Gem delete.","(Checks) Sourcer","retired_live",None),
 ("EDI","RETIRED Editor","Work","2888c17a-98ac-42b6-8241-fc63721cfcaf",None,"editor/v002.md",
  "Retired outright 9 Oct 9:11am (Gem confirmed 9:13am). Live, awaiting Gem delete.","(Work) Editor","retired_live",None),
 ("ENS","RETIRED Ensembler","Work","de808331-3c00-41f5-a3a4-4ae1f8f6f0ba",None,"swarm-builder/v002.md",
  "Retired 4 Oct into Engineer. Live, awaiting Gem delete.","Swarm Builder","retired_live","ENG"),
]

# Unrecorded live agent — no role
UNREC = [
 ("U031","P2 (ID) Inquirer (unrecorded)","unrecorded","0314faa4-edcb-4aa4-91cc-876dc44f3a6e",None,None,
  "Unrecorded live agent, awaiting Gem. Live name 'P2 (ID) Inquirer'. First seen in verify as UNRECORDED; phases.md lists it as active Inquirer, but Gem has not confirmed in Archivist's chat — no role assigned on this map (Archivist v005).","—","unrecorded_live"),
]

DELETED = [
  "Advocate (ad0a645b)","Meter / Cost & Budget Sentinel (f8b83b15)","Expediter (75534bfe)",
  "Adjudicator / Governance Continuity Deputy (b3f6515c)","Indexer (16ee5875)",
  "Maintainer (b96f7469)","Minder (e59d56b6)","Moderator (823349f7)",
  "Sanitizer (243f1c1f)","Sentinel (dddf57af)","Simulator (38bd0474)","Surveyor (1283e02b)",
]

ABSORBED = {
  "MEN":["Minder (incl. Maintainer, Indexer)","Marshal (9 Oct; schedule.md, run order, pacing, load, routing)"],
  "SFG":["Sentinel (dry runs)"],
  "SFK":["Sentinel (threat register, input sanitising; incl. Sanitizer)"],
  "SCR":["Surveyor"],
  "ARB":["Adjudicator"],
  "IMI":["Advocate"],
  "MED":["Meter"],
  "ENG":["Ensembler"],
  "EXP":["Messenger (9 Oct; daily digest)"],
  "INV":["Interrogator (9 Oct; Imitator testing)"],
  "ARC":["Assembler role map (9 Oct; cartography/)"],
}

K = {n[0]: n for n in N}
for r in RET: K[r[0]] = r
for u in UNREC: K[u[0]] = u
K["GEM"] = ("GEM","Gem Quota","human","gem",None,None,"Authority. Approves instruction changes directly until P4 goes live.",None,"human")

E = []
def e(f, t, rel, sources, status="current", **kw):
    d = {"from":K[f][3],"from_name":K[f][1],"to":K[t][3],"to_name":K[t][1],
         "relation":rel,
         "source":[x if str(x).startswith("/") else str(C/x) for x in sources],
         "status":status}
    d.update(kw); E.append(d)

# Approval / instruction pipeline (post-Assembler)
e("ARX","GEM","proposes instruction changes to (Gem approves until P4)",["instruction-architect/v003.md","codex-keeper/v005.md",PH],flow="approval")
e("GEM","ARC","approves; Archivist records",["codex-keeper/v005.md",PH],flow="approval")
e("IMI","ARC","may approve for recording once P4 live (except Imitator / Investigator changes = Gem only)",
  ["clone/v004.md","codex-keeper/v005.md"],flow="approval",
  status="dormant until P4; Gem is sole approver until then")
e("ARX","ARC","sends approved drafts for recording (via Gem/Imitator)",["instruction-architect/v003.md","codex-keeper/v005.md"],flow="approval")
e("ARC","ARX","gives instruction text on request",["codex-keeper/v005.md"])
e("ARC","ARB","gives instruction text on request",["codex-keeper/v005.md"])
e("ARC","SCO","gives instruction text on request",["codex-keeper/v005.md"])
e("ARC","SCR","gives instruction text on request",["codex-keeper/v005.md"])
e("ARC","SFG","gives instruction text on request",["codex-keeper/v005.md"])
e("ARC","SFK","gives instruction text on request",["codex-keeper/v005.md"])

# Role map ownership
e("ASM","ARC","retired: role map (/workspace/governance/cartography/) moved to",["role-cartographer/v006.md","codex-keeper/v005.md"],status="retired_merge_9oct")
e("ASM","GEM","retired: approvals stay with Gem until P4",["role-cartographer/v006.md",PH],status="retired_merge_9oct")
e("ASM","IMI","retired: approvals go to Imitator once P4 live",["role-cartographer/v006.md",PH],status="retired_merge_9oct")

# Merges 9 Oct
e("MAR","MEN","retired into (run order, schedule.md, pacing, load, routing)",["orchestration-conductor/v005.md","mender/v004.md"],status="retired_merge_9oct")
e("MSG","EXP","retired into (daily digest); active Explorer id 04dcca0d",["comms-concierge/v004.md","explorer-copy/v001.md"],status="retired_merge_9oct")
e("INT","INV","retired into (Imitator accuracy testing)",["clone-accuracy-validator/v004.md","investigator/v002.md"],status="retired_merge_9oct")
e("SRC","GEM","retired outright (awaiting delete)",["sourcer/v002.md"],status="retired_outright_9oct")
e("EDI","GEM","retired outright (awaiting delete)",["editor/v002.md"],status="retired_outright_9oct")
e("ENS","ENG","retired into (4 Oct)",["swarm-builder/v002.md","codey/v005.md"],status="retired_merge_4oct")

# Chain / ops
e("SCO","SCR","sends daily scores to",["assessor/v003.md","auditor/v003.md"],flow="chain")
e("SCR","ARX","sends reviews / redesign requests to",["auditor/v003.md","instruction-architect/v003.md"],flow="chain")
e("ARX","GEM","sends proposals to (approver until P4)",["instruction-architect/v003.md"],flow="chain")
e("GEM","ARC","approved changes recorded by",["codex-keeper/v005.md"],flow="chain")
e("MEN","SCO","schedules / watches chain including",["mender/v004.md"],flow="chain")
e("SCR","MEN","reports stalls and reality conflicts to",["auditor/v003.md","mender/v004.md"])
e("MEN","GEM","tells of stalls/incidents",["mender/v004.md"])
e("ARB","ARX","sends rulings needing instruction changes to",["arbiter/v004.md"])
e("ARB","GEM","escalates Architect stalls to",["arbiter/v004.md"])
e("ARB","MEN","reports stalls to",["arbiter/v004.md"])

# Checks
e("SFG","GEM","alerts about unsafe work",["compliance-risk-officer/v004.md"])
e("SFG","ARX","proposes rule changes through",["compliance-risk-officer/v004.md"])
e("SFK","GEM","flags exposed secrets / urgent threats",["secrets-credentials-custodian/v004.md"])
e("SFK","SFG","flags urgent threats to",["secrets-credentials-custodian/v004.md"])
e("SCO","GEM","flags serious problems; weekly scorecard",["assessor/v003.md"])
e("SCR","GEM","tells of repeated poor reviews",["auditor/v003.md"])

# Identity pipeline
e("INQ","INF","sends Gem answers to (codex names e613112b)",["identity-inquirer/v002.md","identity-inferer/v002.md"],
  status="recorded Inquirer not found live ~9:14am; Inferer brief still points at e613112b")
e("INF","INV","hypotheses for adjudication by",["identity-inferer/v002.md","investigator/v002.md"],status="Investigator dormant (P3)")
e("INV","IMI","tests accuracy of (once P4 live)",["investigator/v002.md","clone/v004.md"],status="both dormant until their phases")
e("IMI","INF","logs preference gaps with",["clone/v004.md"])
e("IMI","INQ","gaps for Gem via",["clone/v004.md"],status="Inquirer id unsettled")
e("INV","SCR","sends findings to",["investigator/v002.md"])
e("INV","SCO","sends weekly accuracy score to",["investigator/v002.md"])

# Work routing
e("EXP","EMI","routes general work to",["explorer-copy/v001.md"],status="Emissary dormant (P5)")
e("EXP","ENG","routes code/swarm work to",["explorer-copy/v001.md"],status="Engineer dormant (P5)")
e("EXP","EXT","routes research/scraping to",["explorer-copy/v001.md"],status="Extractor dormant (P5)")
e("EXP","SFG","sends own risky plans to for dry run",["explorer-copy/v001.md"])
e("EXP","GEM","brings finished work and urgent matters to",["explorer-copy/v001.md"])
e("EXP","IMI","asks preference questions of",["explorer-copy/v001.md"],status="Imitator dormant (P4)")
e("EXP","MEN","defers routine timing/stalls to",["explorer-copy/v001.md","mender/v004.md"])
e("EXP","ARX","sends briefs for new groups/bots to",["explorer-copy/v001.md"])
e("MED","EXP","sends cost alerts to (Messenger duty now on Explorer)",["connector-steward/v004.md","explorer-copy/v001.md"])
e("MED","GEM","reports health/spend issues to",["connector-steward/v004.md"])

# Dual Explorer note edge
e("EXP0","EXP","prior Explorer id; active merged brief is 04dcca0d (same display name)",
  ["genesis-gang-god/v004.md","explorer-copy/v001.md",IDX],status="both live; Gem has not retired 82a2c15a in Archivist chat")

nodes = []
nodes.append({"id":"gem","name":"Gem Quota","key":"GEM","type":"human",
              "note":"Authority. Approves instruction changes directly until P4 goes live; then Imitator (except Imitator/Investigator changes)."})
for n in N:
    key,name,cat,id_,phase,codex,note,former,flag = n
    nodes.append({
        "id":id_,"name":name,"key":key,"type":"bot","category":cat,"phase":phase,
        "phase_status": next(p["status"] for p in PHASES if p["phase"]==phase),
        "codex": str(C/codex) if codex else None,
        "former_name": former, "absorbed": ABSORBED.get(key,[]),
        "map_status": flag, "note": note,
    })
for r in RET:
    key,name,cat,id_,_,codex,note,former,flag,into = r
    nodes.append({
        "id":id_,"name":name,"key":key,"type":"bot","category":cat,"phase":None,
        "phase_status":"RETIRED (live, awaiting Gem delete)",
        "codex": str(C/codex) if codex else None,
        "former_name": former, "absorbed": [],
        "map_status": flag, "merged_into": into, "note": note,
    })
for u in UNREC:
    key,name,cat,id_,_,codex,note,former,flag = u
    nodes.append({
        "id":id_,"name":name,"key":key,"type":"unrecorded_live_agent","category":cat,"phase":None,
        "phase_status":"unrecorded live agent, awaiting Gem — no role assigned",
        "codex": None, "former_name": former, "absorbed": [],
        "map_status": flag, "note": note,
        "first_seen_note": "Listed by verify.py as UNRECORDED AGENT; live name P2 (ID) Inquirer; phases.md names it active Inquirer as of 9 Oct ~9:06am relay — Gem has not confirmed in Archivist's chat.",
    })

graph = {
  "version": "v4, 9 Oct 2026 ~9:20 AEST",
  "previous_version": "v3, 4 Oct 2026",
  "maintainer": "P1 (Roles) Archivist (61ef3abd-87b8-49f1-b8d6-b52969afa315); took cartography from retired Assembler on 9 Oct 2026",
  "sources": {
    "phases": PH,
    "codex_index": IDX,
    "codex_latest_per_folder": "latest vNNN.md per folder in /workspace/governance/codex/",
    "note": "Descriptive only from codex + phases.md. Does not decide roles or approve.",
  },
  "phases": PHASES,
  "retired_live": [
    {"name": r[1], "id": r[3], "merged_into": r[9], "codex": r[5]} for r in RET
  ],
  "deleted_gone": DELETED,
  "unrecorded_live_agents": [
    {"name": u[1], "id": u[3], "note": u[6]} for u in UNREC
  ],
  "status_values": {
    "active": "In phases.md and live with recorded codex",
    "active_prior": "Live recorded id sharing a display name with the active agent",
    "recorded_not_live": "Codex folder exists; not found live since noted time; awaiting Gem",
    "dormant": "In phases.md as dormant phase",
    "retired_live": "RETIRED brief live; awaiting Gem delete",
    "unrecorded_live": "Live agent with no codex folder; no role on this map",
  },
  "nodes": nodes,
  "edges": E,
  "stats": {"nodes": len(nodes), "edges": len(E),
            "active_or_dormant_recorded": len(N), "retired_live": len(RET),
            "unrecorded": len(UNREC), "deleted_gone": len(DELETED)},
}

(OUT / "role-graph.json").write_text(json.dumps(graph, indent=2) + "\n")
print(f"Wrote role-graph.json nodes={len(nodes)} edges={len(E)}")

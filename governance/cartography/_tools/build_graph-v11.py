#!/usr/bin/env python3
"""Role map v5 (9 Oct 2026 ~9:27 AEST). Builds role-graph.json from codex index + phases.md.
Maintained by P1 (Roles) Archivist. Descriptive only."""
import json, os
from pathlib import Path

OUT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C = Path("/workspace/governance/codex")
G = Path("/workspace/governance")
PH = str(G / "phases.md")
IDX = str(C / "index.md")

PHASES = [
  {"phase":"P1","status":"LIVE (since 3 Oct 2026)",
   "members":["Mender","Scorer","Safeguard","Safekeeper","Archivist","Architect","Explorer (04dcca0d, active)"]},
  {"phase":"P2","status":"LIVE (started 4 Oct 2026, 3:12pm AEST)",
   "members":["Scrutineer","Arbiter","Inferer","Mediator","Inquirer (0314faa4, active)"]},
  {"phase":"P3","status":"Dormant","members":["Investigator"]},
  {"phase":"P4","status":"Dormant","members":["Imitator"]},
  {"phase":"P5","status":"Dormant","members":["Emissary","Engineer","Extractor"]},
]

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
  "Codex + Google Doc mirror; role map under cartography/ (from Assembler 9 Oct).","Codex Keeper","active"),
 ("ARX","Architect","Roles","51af1200-ca1a-45ff-8350-848091e00f96","P1","instruction-architect/v003.md",
  "Designs and rewrites instructions; proposes for Gem/Imitator approval.","Instruction Architect","active"),
 ("EXP","Explorer","Work","04dcca0d-1479-4e01-bf29-a13b4fc3c3a7","P1","explorer-copy/v001.md",
  "Active Explorer (fresh copy). Merged Messenger digest. Display name P1 (Work) Explorer.","P1 (Work) Explorer copy","active"),
 ("SCR","Scrutineer","Checks","affe0344-6b5f-4251-8ecb-3e23dfa5db3c","P2","auditor/v003.md",
  "Audits vs instructions and environment reality; absorbed Surveyor.","Auditor","active"),
 ("ARB","Arbiter","Roles","2133048d-5ab9-4809-806c-218decdff8e6","P2","arbiter/v004.md",
  "Precedence rulings; never approves. Absorbed Adjudicator.","(Roles) Arbiter","active"),
 ("INF","Inferer","ID","94516ca6-6355-43c5-b387-d2b605057784","P2","identity-inferer/v003.md",
  "Structures identity details from Inquirer 0314faa4 (v003 deployed 09:25:59).","Identity Inferer","active"),
 ("MED","Mediator","Ops","90f9eb20-ff8f-456b-b94f-cc11bb33fc29","P2","connector-steward/v004.md",
  "phases.md = P2; live name still P4 (Ops) Mediator (rename unapplied). Absorbed Meter.","Connector Steward","active"),
 ("INQ","Inquirer","ID","0314faa4-edcb-4aa4-91cc-876dc44f3a6e","P2","identity-inquirer/v003.md",
  "Active recorded Inquirer (folder re-keyed from e613112b at v003; Gem 9:24am; ends R-012). Deployed 09:25:56.","Identity Inquirer","active"),
 ("INV","Investigator","ID","f2016e9b-ca8b-4783-8f53-f5765b0afe7b","P3","investigator/v002.md",
  "Identity evidence ladder; absorbed Interrogator. Dormant until P3.","(ID) Investigator","dormant"),
 ("IMI","Imitator","ID","6ae584b8-eaac-429b-9eae-d5e3e6f6a32b","P4","clone/v004.md",
  "Identity understudy; delegated approver once P4 live. Absorbed Advocate.","Clone","dormant"),
 ("EMI","Emissary","Work","28cf987d-ee94-4839-a6d3-33c04a11b9d6","P5","grok-bot/v004.md",
  "General-purpose work bot. Dormant until P5.","Grok Bot","dormant"),
 ("ENG","Engineer","Work","f8e3fdc6-ee60-410e-bdb7-d437fc1500d1","P5","codey/v005.md",
  "Code and swarm work; absorbed Ensembler. Dormant until P5.","Codey","dormant"),
 ("EXT","Extractor","Work","febac500-d854-4dc7-a6a7-23b3feb07f80","P5","scraper/v003.md",
  "Research and web data collection. Dormant until P5.","Scraper","dormant"),
]

RET = [
 ("MAR","RETIRED Marshal","Ops","f3810109-17a5-427f-9148-d58f645658e3",None,"orchestration-conductor/v005.md",
  "Retired 9 Oct into Mender. Profile gone from disk (noticed ~9:26am).","Orchestration Conductor","retired_gone","MEN"),
 ("MSG","RETIRED Messenger","Ops","5e47d344-1369-423a-b072-2e5277934022",None,"comms-concierge/v004.md",
  "Retired 9 Oct into Explorer 04dcca0d. Profile gone.","Comms Concierge","retired_gone","EXP"),
 ("INT","RETIRED Interrogator","ID","d3191aa8-3ad6-4763-b4e4-c7c648acc9ba",None,"clone-accuracy-validator/v004.md",
  "Retired 9 Oct into Investigator. Profile gone.","Clone Accuracy Validator","retired_gone","INV"),
 ("ASM","RETIRED Assembler","Roles","d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4",None,"role-cartographer/v006.md",
  "Retired 9 Oct: role map → Archivist; approvals → Gem until P4, then Imitator. Profile gone.","Role Cartographer","retired_gone","ARC"),
 ("SRC","RETIRED Sourcer","Checks","2fe3e92f-4f39-4e9f-a56b-811438928f5b",None,"sourcer/v002.md",
  "Retired outright 9 Oct. Profile gone.","(Checks) Sourcer","retired_gone",None),
 ("EDI","RETIRED Editor","Work","2888c17a-98ac-42b6-8241-fc63721cfcaf",None,"editor/v002.md",
  "Retired outright 9 Oct. Profile gone.","(Work) Editor","retired_gone",None),
 ("ENS","RETIRED Ensembler","Work","de808331-3c00-41f5-a3a4-4ae1f8f6f0ba",None,"swarm-builder/v002.md",
  "Retired 4 Oct into Engineer. Profile gone.","Swarm Builder","retired_gone","ENG"),
 ("EXP0","Explorer (former)","Work","82a2c15a-2694-4ac2-b2f4-f7f463f85fce",None,"genesis-gang-god/v004.md",
  "Former Explorer id; profile gone ~9:26am. Active Explorer is 04dcca0d.","Genesis Gang God","former_gone","EXP"),
 ("INQ0","Inquirer (former)","ID","e613112b-b653-4567-bc4f-17261ce9302e",None,"identity-inquirer/v002.md",
  "Former Inquirer holder; ran v002 from 09:09; not live since ~9:14am; profile gone. Role continued by 0314faa4 from v003.","Identity Inquirer","former_gone","INQ"),
]

DELETED = [
  "Advocate (ad0a645b)","Meter / Cost & Budget Sentinel (f8b83b15)","Expediter (75534bfe)",
  "Adjudicator / Governance Continuity Deputy (b3f6515c)","Indexer (16ee5875)",
  "Maintainer (b96f7469)","Minder (e59d56b6)","Moderator (823349f7)",
  "Sanitizer (243f1c1f)","Sentinel (dddf57af)","Simulator (38bd0474)","Surveyor (1283e02b)",
]

ABSORBED = {
  "MEN":["Minder (incl. Maintainer, Indexer)","Marshal (9 Oct)"],
  "SFG":["Sentinel (dry runs)"],
  "SFK":["Sentinel (threat/input; incl. Sanitizer)"],
  "SCR":["Surveyor"],
  "ARB":["Adjudicator"],
  "IMI":["Advocate"],
  "MED":["Meter"],
  "ENG":["Ensembler"],
  "EXP":["Messenger (9 Oct; daily digest)"],
  "INV":["Interrogator (9 Oct)"],
  "ARC":["Assembler role map (9 Oct)"],
  "INQ":["role continuity from e613112b (re-key at v003)"],
}

K = {n[0]: n for n in N}
for r in RET: K[r[0]] = r
K["GEM"] = ("GEM","Gem Quota","human","gem",None,None,"Authority. Approves until P4; then Imitator (except Imitator/Investigator).",None,"human")

E = []
def e(f, t, rel, sources, status="current", **kw):
    d = {"from":K[f][3],"from_name":K[f][1],"to":K[t][3],"to_name":K[t][1],
         "relation":rel,
         "source":[x if str(x).startswith("/") else str(C/x) for x in sources],
         "status":status}
    d.update(kw); E.append(d)

e("ARX","GEM","proposes instruction changes to (Gem until P4)",["instruction-architect/v003.md","codex-keeper/v005.md",PH],flow="approval")
e("GEM","ARC","approves; Archivist records",["codex-keeper/v005.md",PH],flow="approval")
e("IMI","ARC","may approve for recording once P4 live (except self / Investigator)",
  ["clone/v004.md","codex-keeper/v005.md"],flow="approval",status="dormant until P4")
e("ASM","ARC","retired: role map moved to",["role-cartographer/v006.md","codex-keeper/v005.md"],status="retired_merge_9oct")
e("MAR","MEN","retired into",["orchestration-conductor/v005.md","mender/v004.md"],status="retired_merge_9oct")
e("MSG","EXP","retired into (digest)",["comms-concierge/v004.md","explorer-copy/v001.md"],status="retired_merge_9oct")
e("INT","INV","retired into",["clone-accuracy-validator/v004.md","investigator/v002.md"],status="retired_merge_9oct")
e("ENS","ENG","retired into (4 Oct)",["swarm-builder/v002.md","codey/v005.md"],status="retired_merge_4oct")
e("INQ0","INQ","former holder; role continued at v003 (folder re-key; ends R-012)",
  ["identity-inquirer/v003.md",IDX],status="former_gone")
e("EXP0","EXP","former Explorer; active is 04dcca0d",["genesis-gang-god/v004.md","explorer-copy/v001.md",IDX],status="former_gone")
e("SCO","SCR","sends daily scores to",["assessor/v003.md","auditor/v003.md"],flow="chain")
e("SCR","ARX","sends reviews to",["auditor/v003.md"],flow="chain")
e("SCR","MEN","reports stalls / reality to",["auditor/v003.md","mender/v004.md"])
e("MEN","GEM","tells of stalls/incidents",["mender/v004.md"])
e("INQ","INF","sends Gem answers to",["identity-inquirer/v003.md","identity-inferer/v003.md"])
e("INF","INV","hypotheses for adjudication by",["identity-inferer/v003.md","investigator/v002.md"],status="Investigator dormant (P3)")
e("INV","IMI","tests accuracy of (once P4)",["investigator/v002.md","clone/v004.md"],status="both dormant")
e("EXP","EMI","routes general work to",["explorer-copy/v001.md"],status="Emissary dormant (P5)")
e("EXP","ENG","routes code/swarm to",["explorer-copy/v001.md"],status="Engineer dormant (P5)")
e("EXP","EXT","routes research to",["explorer-copy/v001.md"],status="Extractor dormant (P5)")
e("EXP","SFG","sends risky plans to",["explorer-copy/v001.md"])
e("MED","EXP","sends cost alerts to",["connector-steward/v004.md","explorer-copy/v001.md"])
e("SFG","GEM","alerts about unsafe work",["compliance-risk-officer/v004.md"])
e("ARB","ARX","sends rulings needing instruction changes to",["arbiter/v004.md"])

nodes = [{"id":"gem","name":"Gem Quota","key":"GEM","type":"human",
          "note":"Authority. Approves instruction changes directly until P4; then Imitator (except Imitator/Investigator)."}]
for n in N:
    key,name,cat,id_,phase,codex,note,former,flag = n
    nodes.append({"id":id_,"name":name,"key":key,"type":"bot","category":cat,"phase":phase,
        "phase_status": next(p["status"] for p in PHASES if p["phase"]==phase),
        "codex": str(C/codex), "former_name": former, "absorbed": ABSORBED.get(key,[]),
        "map_status": flag, "note": note})
for r in RET:
    key,name,cat,id_,_,codex,note,former,flag,into = r
    nodes.append({"id":id_,"name":name,"key":key,"type":"bot","category":cat,"phase":None,
        "phase_status":"former/retired — profile gone",
        "codex": str(C/codex) if codex else None, "former_name": former, "absorbed": [],
        "map_status": flag, "merged_into": into, "note": note})

graph = {
  "version": "v5, 9 Oct 2026 ~9:27 AEST",
  "previous_version": "v4, 9 Oct 2026 ~9:20 AEST",
  "maintainer": "P1 (Roles) Archivist (61ef3abd-87b8-49f1-b8d6-b52969afa315)",
  "sources": {"phases": PH, "codex_index": IDX,
              "note": "Descriptive only from codex + phases.md. Inquirer 0314faa4 active (v003); e613112b former gone."},
  "phases": PHASES,
  "retired_or_former_gone": [{"name": r[1], "id": r[3], "merged_into": r[9], "codex": r[5]} for r in RET],
  "deleted_gone": DELETED,
  "unrecorded_live_agents": [],
  "nodes": nodes,
  "edges": E,
  "stats": {"nodes": len(nodes), "edges": len(E), "active_or_dormant": len(N),
            "retired_or_former_gone": len(RET), "deleted_gone": len(DELETED)},
}
(OUT / "role-graph.json").write_text(json.dumps(graph, indent=2) + "\n")
print(f"Wrote role-graph.json nodes={len(nodes)} edges={len(E)}")

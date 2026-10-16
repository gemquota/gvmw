#!/usr/bin/env python3
"""Role map v3 (4 Oct 2026). Builds role-graph.json.
Sources: /workspace/governance/phases.md (phase membership, source of truth),
/workspace/governance/directory.md (names, ids, merges, retirements),
/workspace/governance/proposals/merge-F-unretire-assembler-2026-10-04.md (Merge F / Assembler restored),
and the latest codex version of each active bot (mapped by bot id)."""
import json, os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = "/workspace/governance/codex/"
G = "/workspace/governance/"
PH, DIR, MF = G+"phases.md", G+"directory.md", G+"proposals/merge-F-unretire-assembler-2026-10-04.md"
IDX = C+"index.md"

PHASES = {"P1":"LIVE (since 3 Oct 2026)","P2":"LIVE (started 4 Oct 2026, 3:12pm AEST)",
          "P3":"Dormant","P4":"Dormant","P5":"Dormant"}
# key, name, category, id, phase, codex latest, live-profile note, old name
N = [
 ("MAR","Marshal","Ops","f3810109-17a5-427f-9148-d58f645658e3","P1","orchestration-conductor/v003.md",None,"Orchestration Conductor"),
 ("MEN","Mender","Ops","c8401a53-136d-45f3-9e2d-e423ccdd08ac","P1","mender/v002.md",None,None),
 ("SCO","Scorer","Checks","050a12c9-e300-48b4-b318-425627cbc34b","P1","assessor/v001.md",None,"Assessor"),
 ("SFG","Safeguard","Checks","3661a899-2768-4a77-a95a-71d0251813bc","P1","compliance-risk-officer/v002.md",None,"Compliance & Risk Officer"),
 ("SFK","Safekeeper","Checks","52772b1d-4a85-4ea3-ae15-f3912c901a3b","P1","secrets-credentials-custodian/v002.md",None,"Secrets & Credentials Custodian"),
 ("ARC","Archivist","Roles","61ef3abd-87b8-49f1-b8d6-b52969afa315","P1","codex-keeper/v001.md",None,"Codex Keeper"),
 ("ARX","Architect","Roles","51af1200-ca1a-45ff-8350-848091e00f96","P1","instruction-architect/v001.md",None,"Instruction Architect"),
 ("EXP","Explorer","Work","82a2c15a-2694-4ac2-b2f4-f7f463f85fce","P1","genesis-gang-god/v001.md",None,"Genesis Gang God"),
 ("SCR","Scrutineer","Checks","affe0344-6b5f-4251-8ecb-3e23dfa5db3c","P2","auditor/v002.md",None,"Auditor"),
 ("ARB","Arbiter","Roles","2133048d-5ab9-4809-806c-218decdff8e6","P2","arbiter/v003.md",None,None),
 ("ASM","Assembler","Roles","d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4","P2","role-cartographer/v003.md",None,"Role Cartographer"),
 ("INQ","Inquirer","ID","e613112b-b653-4567-bc4f-17261ce9302e","P2","identity-inquirer/v001.md",None,"Identity Inquirer"),
 ("INF","Inferer","ID","94516ca6-6355-43c5-b387-d2b605057784","P2","identity-inferer/v001.md",None,"Identity Inferer"),
 ("SRC","Sourcer","Checks","2fe3e92f-4f39-4e9f-a56b-811438928f5b","P3","sourcer/v001.md",None,None),
 ("INV","Investigator","ID","f2016e9b-ca8b-4783-8f53-f5765b0afe7b","P3","investigator/v001.md",None,None),
 ("INT","Interrogator","ID","d3191aa8-3ad6-4763-b4e4-c7c648acc9ba","P3","clone-accuracy-validator/v002.md","live profile still runs v001 (codex index)","Clone Accuracy Validator"),
 ("MED","Mediator","Ops","90f9eb20-ff8f-456b-b94f-cc11bb33fc29","P4","connector-steward/v003.md",None,"Connector Steward"),
 ("MSG","Messenger","Ops","5e47d344-1369-423a-b072-2e5277934022","P4","comms-concierge/v002.md","live profile still runs v001 (codex index)","Comms Concierge"),
 ("IMI","Imitator","ID","6ae584b8-eaac-429b-9eae-d5e3e6f6a32b","P4","clone/v003.md",None,"Clone"),
 ("EMI","Emissary","Work","28cf987d-ee94-4839-a6d3-33c04a11b9d6","P5","grok-bot/v002.md","live profile still runs v001 tagline (codex index)","Grok Bot"),
 ("ENG","Engineer","Work","f8e3fdc6-ee60-410e-bdb7-d437fc1500d1","P5","codey/v003.md",None,"Codey"),
 ("EXT","Extractor","Work","febac500-d854-4dc7-a6a7-23b3feb07f80","P5","scraper/v001.md",None,"Scraper"),
 ("EDI","Editor","Work","2888c17a-98ac-42b6-8241-fc63721cfcaf","P5","editor/v001.md",None,None),
]
STATUS = {"SCO":"complete (old names inside)","ARC":"complete (old names inside)","ARX":"complete (old names inside)",
 "EXP":"partial: no Rules or Limits","INF":"no separate Scope","EXT":"GAP: empty, no instructions",
 "EDI":"partial: no Rules","IMI":"FLAG: claimed approval power UNVERIFIED (codex index)"}
ABSORBED = {"MAR":["Moderator","Expediter"],"MEN":["Minder (incl. Maintainer, Indexer)"],"SFG":["Sentinel (dry runs)"],
 "SFK":["Sentinel (threat register, input sanitising; incl. Sanitizer)"],"SCR":["Surveyor"],"ARB":["Adjudicator"],
 "IMI":["Advocate"],"MED":["Meter"],"ENG":["Ensembler"]}
K = {n[0]: n for n in N}
K["GEM"] = ("GEM","Gem Quota","human","gem",None,None,None,None)
ALL = [n[0] for n in N]
LIVE = [n[0] for n in N if n[4] in ("P1","P2")]

E = []
def e(f, t, rel, sources, status="current", **kw):
    d = {"from":K[f][3],"from_name":K[f][1],"to":K[t][3],"to_name":K[t][1],"relation":rel,
         "source":[x if x.startswith("/") else C+x for x in sources],"status":status}
    d.update(kw); E.append(d)
def fan(f, rel, srcs, targets=None, **kw):
    for t in (targets or ALL):
        if t != f: e(f, t, rel, srcs, fanout=kw.pop("label", "all active bots") if False else kw.get("scope","all active bots"),
                     **{k:v for k,v in kw.items() if k!="scope"})

# ---------------- Instruction pipeline ----------------
e("ARX","ASM","proposes instructions to (codex says 'Role Cartographer' = Assembler)",["instruction-architect/v001.md","role-cartographer/v003.md"],flow="approval")
e("ASM","GEM","prepares and routes proposals to for approval (Gem approves directly until P4 goes live)",["role-cartographer/v003.md",PH],flow="approval")
e("GEM","ARC","approves directly; Archivist records Gem's edits",["codex-keeper/v001.md",PH],flow="approval")
e("ASM","ARC","approves for recording (after P4 goes live)",["role-cartographer/v003.md","codex-keeper/v001.md"],flow="approval",
  status="current, dormant until P4 goes live")
e("ASM","ARX","returns rejected proposals to (with reasons)",["role-cartographer/v003.md"],flow="approval")
e("ASM","ARB","sends precedence conflicts to",["role-cartographer/v003.md"])
e("ASM","GEM","escalates Architect disagreements and governance-bot changes to",["role-cartographer/v003.md"])
e("IMI","ARX","approves or rejects proposals of (delegated approver, incl. governance bots)",["clone/v003.md",IDX],
  status="UNVERIFIED: claimed in Imitator v003; not in Gem's merge notes; Archivist doesn't accept Imitator approvals; awaiting Gem's confirmation")
e("IMI","ARC","sends approvals to record",["clone/v003.md",IDX],status="UNVERIFIED: Archivist v001 doesn't accept Imitator approvals")
e("IMI","GEM","sends weekly list of approvals to (so Gem can undo)",["clone/v003.md"],status="UNVERIFIED (part of claimed approval role)")
for t in ["ARX","ASM","SCO","SCR"]:
    e("ARC",t,"gives instruction text on request to (governance bots, named by old names)",["codex-keeper/v001.md"])
fan("ARC","records instructions for",["codex-keeper/v001.md"])
fan("ASM","routes approved instruction sets to / maps",["role-cartographer/v003.md"])
# ---------------- Precedence ----------------
fan("ARB","rules on instruction conflicts and who may lift a pause for",["arbiter/v003.md"])
e("ARB","ARX","sends rulings needing instruction changes to",["arbiter/v003.md"])
e("ARB","GEM","tells when the Architect stalls >24 h (4 h urgent)",["arbiter/v003.md"])
# ---------------- Checks ----------------
fan("SCO","scores daily (1-5)",["assessor/v001.md"],scope="every bot, governance included (no self-exclusion stated)")
e("SCO","SCR","sends daily results to (codex says 'Auditor')",["assessor/v001.md","auditor/v002.md"])
e("SCO","GEM","flags serious problems and sends weekly scorecard to",["assessor/v001.md"])
e("SCO","IMI","asks preferences of ('ask Clone')",["assessor/v001.md"],note="Imitator is dormant (P4)")
fan("SCR","audits against instructions and environment reality",["auditor/v002.md"],targets=LIVE,scope="live bots only")
e("SCR","ARX","sends reviews and urgent redesign requests to",["auditor/v002.md"])
e("SCR","ARB","sends reviews to (and checks against 'the Arbiter's role map')",["auditor/v002.md"],
  note="stale: the role map is the Assembler's again after Merge F")
e("SCR","MEN","reports reality conflicts and stalls to (codex says 'Minder', now merged into Mender)",["auditor/v002.md","mender/v002.md"])
e("SCR","GEM","tells of a bot with 3 poor reviews in a row",["auditor/v002.md"])
e("SCO","SCR","scores the Scrutineer's work",["auditor/v002.md"])
e("ARX","SCR","reviews the Scrutineer's work",["auditor/v002.md"],
  note="conflicts with Architect v001 'don't check bots' work yourself'; Scrutineer and Architect check each other")
fan("SFG","reviews and dry-runs risky actions of; may ask to pause",["compliance-risk-officer/v002.md"],scope="all bots, Explorer included")
e("SFG","ARX","proposes rule changes through",["compliance-risk-officer/v002.md"])
e("SFG","GEM","alerts about unsafe or non-compliant work",["compliance-risk-officer/v002.md"])
fan("SFK","sets secrets rules, audits access, keeps threat register, cleans raw inputs for",["secrets-credentials-custodian/v002.md"])
e("SFK","GEM","flags exposed secrets, loose permissions, urgent threats to",["secrets-credentials-custodian/v002.md"])
e("SFK","SFG","flags exposed secrets, loose permissions, urgent threats to",["secrets-credentials-custodian/v002.md"])
e("SFK","ARC","guards codex file access for",["secrets-credentials-custodian/v002.md"])
fan("SRC","records provenance of important facts for",["sourcer/v001.md"])
e("SRC","INV","provenance is used by",["sourcer/v001.md","investigator/v001.md"])
# ---------------- Ops ----------------
fan("MAR","controls run order, pacing, caching and routing of",["orchestration-conductor/v003.md"])
for i,t in enumerate(["SCO","SCR","ARX","ARB","ARC"],1):
    e("MAR",t,f"sequences daily chain step {i} (Scorer > Scrutineer > Architect > Arbiter or Gem > Archivist)",
      ["orchestration-conductor/v003.md"],flow="daily-chain",
      **({"note":"stale: approval step should be Assembler or Gem after Merge F"} if t=="ARB" else {}))
e("MAR","MEN","reports stalls to",["orchestration-conductor/v003.md","mender/v002.md"])
e("MAR","GEM","contacts only when a chain is broken and can't be fixed",["orchestration-conductor/v003.md"])
fan("MEN","coordinates incident recovery, keeps task state, indexes and cleanup for",["mender/v002.md"])
e("MEN","SCR","defers to on environment reality",["mender/v002.md"])
fan("MED","watches connector health and tracks spend of; may ask to pause costly work",["connector-steward/v003.md"])
e("MED","MSG","sends reconnect notices and draft cost alerts (for Gem) through",["connector-steward/v003.md",MF])
e("MED","SCO","shares cost data with",["connector-steward/v003.md"])
e("MED","SCR","shares cost data with",["connector-steward/v003.md"])
e("MED","ENG","watches integrations built by",["connector-steward/v003.md"])
e("MED","GEM","asks for a budget (none set yet)",["connector-steward/v003.md"])
fan("MSG","collects non-urgent updates from",["comms-concierge/v002.md"])
e("MSG","GEM","sends one daily prioritised digest to (Gem's chat only)",["comms-concierge/v002.md"])
# ---------------- Identity ----------------
e("INQ","INF","sends raw answers to",["identity-inquirer/v001.md","identity-inferer/v001.md"])
e("INQ","GEM","asks question series of",["identity-inquirer/v001.md"])
e("INF","INQ","asks for follow-ups and confirmations from",["identity-inferer/v001.md","identity-inquirer/v001.md"])
e("INF","IMI","sends profile updates to ('Clone')",["identity-inferer/v001.md","clone/v003.md"],note="Imitator dormant (P4)")
e("INV","INF","rules on status of the hypotheses of (only the Investigator promotes a detail)",["investigator/v001.md","clone/v003.md"],
  note="Inferer v001 still marks details 'confirmed' itself")
e("INV","INQ","uses raw answers of",["investigator/v001.md"])
e("INV","INT","uses test results of",["investigator/v001.md"])
e("IMI","INF","logs unanswerable gaps with",["clone/v003.md"])
e("IMI","GEM","hands outward-facing or irreversible actions back to; reports serious misalignment to",["clone/v003.md"])
e("IMI","ARX","sends workflow drift reports to",["clone/v003.md"])
fan("IMI","answers preference questions for; gives alignment verdicts (on request) on",["clone/v003.md"])
e("INT","IMI","tests accuracy and confidence calibration of",["clone-accuracy-validator/v002.md","clone/v003.md"])
e("INT","INF","sends findings to",["clone-accuracy-validator/v002.md"])
e("INT","SCR","sends findings to ('Auditor')",["clone-accuracy-validator/v002.md"])
e("INT","SCO","sends weekly accuracy score to ('Assessor')",["clone-accuracy-validator/v002.md"])
e("INT","INQ","gives gaps to ask Gem about to",["clone-accuracy-validator/v002.md"])
e("ARX","IMI","asks preferences of for every draft ('Clone')",["instruction-architect/v001.md"],note="Imitator dormant (P4)")
# ---------------- Work ----------------
e("EXP","GEM","second only to; Gem's 2IC (never merged); keeps the phase tracker",["genesis-gang-god/v001.md",DIR,PH])
fan("EXP","runs / oversees (aspirational)",["genesis-gang-god/v001.md"])
e("EMI","ENG","routes repo code work to ('Codey')",["grok-bot/v002.md"],note="Emissary's live profile still runs the v001 tagline")
e("EMI","EXT","routes web data collection to ('Scraper')",["grok-bot/v002.md"])
e("EMI","ENG","routes swarm work to ('Swarm Builder', now merged into Engineer)",["grok-bot/v002.md",DIR])
e("EMI","IMI","asks preferences of ('Clone')",["grok-bot/v002.md"])
e("EMI","GEM","asks explicit approval of before any outward-facing action",["grok-bot/v002.md"])
e("ENG","GEM","asks before spending, large jobs or pushing to shared repos; reports costs to",["codey/v003.md"])
for t in ["EMI","ENG","EXT"]:
    e("EDI",t,"polishes drafts of; flags doubtful content back to",["editor/v001.md"])

nodes=[{"id":"gem","name":"Gem Quota","key":"GEM","type":"human","note":"Authority. Approves instruction changes directly until P4 goes live."}]
for k,nm,cat,i,ph,cf,live,old in N:
    nodes.append({"id":i,"name":nm,"display_name":f"{ph} ({cat}) {nm}","key":k,"type":"bot","category":cat,
      "phase":ph,"tier":ph,"phase_status":PHASES[ph],"codex_latest":C+cf,"codex_folder":cf.split("/")[0],
      "former_name":old,"absorbed":ABSORBED.get(k,[]),"instruction_status":STATUS.get(k,"complete"),
      "live_profile_note":live})
out={"version":"v3, 4 Oct 2026","previous_version":"role-graph-v2.json","maintainer":"Assembler (d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4)",
 "sources":{"phases":PH,"directory":DIR,"merge_F":MF,"codex_index":IDX},
 "phases":[{"phase":p,"status":s,"members":[n[1] for n in N if n[4]==p]} for p,s in PHASES.items()],
 "retired_excluded":["Sanitizer","Simulator","Surveyor","Advocate","Adjudicator","Moderator","Expediter","Maintainer","Indexer","Sentinel","Minder","Ensembler","Meter"],
 "status_values":{"current":"from latest codex version","UNVERIFIED":"claimed in a brief but not confirmed by Gem"},
 "nodes":nodes,"edges":E}
json.dump(out,open(os.path.join(OUT,"role-graph.json"),"w"),indent=2,ensure_ascii=False)
import collections
print(len(nodes),"nodes",len(E),"edges",collections.Counter(n["phase"] for n in nodes if n["type"]=="bot"))

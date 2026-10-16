#!/usr/bin/env python3
"""Builds role-graph.json and role-map.mmd for the role map (v1, 2 Oct 2026).
Every edge cites the codex file(s) it is drawn from. Run from any directory."""
import json, os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = "/workspace/governance/codex/"
def src(*slugs): return [C + s + "/v001.md" for s in slugs]

N = [  # id, name, short key, role group, instruction status
 ("gem", "Gem Quota", "GEM", "human", "n/a (the user)"),
 ("82a2c15a-2694-4ac2-b2f4-f7f463f85fce", "Genesis Gang God", "GGG", "lead", "partial: no Rules or Limits"),
 ("61ef3abd-87b8-49f1-b8d6-b52969afa315", "Codex Keeper", "CK", "governance", "complete"),
 ("51af1200-ca1a-45ff-8350-848091e00f96", "Instruction Architect", "IA", "governance", "complete"),
 ("d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4", "Role Cartographer", "RC", "governance", "complete"),
 ("050a12c9-e300-48b4-b318-425627cbc34b", "Assessor", "AS", "governance", "complete"),
 ("affe0344-6b5f-4251-8ecb-3e23dfa5db3c", "Auditor", "AU", "governance", "complete (no separate Scope)"),
 ("6ae584b8-eaac-429b-9eae-d5e3e6f6a32b", "Clone", "CL", "identity", "complete"),
 ("e613112b-b653-4567-bc4f-17261ce9302e", "Identity Inquirer", "IQ", "identity", "complete"),
 ("94516ca6-6355-43c5-b387-d2b605057784", "Identity Inferer", "IF", "identity", "complete (no separate Scope)"),
 ("de808331-3c00-41f5-a3a4-4ae1f8f6f0ba", "Swarm Builder", "SB", "build", "partial: no Relationships"),
 ("28cf987d-ee94-4839-a6d3-33c04a11b9d6", "Grok Bot", "GB", "general (unassigned)", "gap: one-line tagline only"),
 ("f8e3fdc6-ee60-410e-bdb7-d437fc1500d1", "Codey", "CO", "general (unassigned)", "gap: no instructions"),
 ("febac500-d854-4dc7-a6a7-23b3feb07f80", "Scraper", "SC", "general (unassigned)", "gap: no instructions"),
]
SLUG = {"GGG":"genesis-gang-god","CK":"codex-keeper","IA":"instruction-architect","RC":"role-cartographer",
        "AS":"assessor","AU":"auditor","CL":"clone","IQ":"identity-inquirer","IF":"identity-inferer",
        "SB":"swarm-builder","GB":"grok-bot","CO":"codey","SC":"scraper"}
K = {n[2]: n for n in N}
BOTS = [n[2] for n in N if n[2] != "GEM"]

E = []
def e(f, t, rel, sources, note=None, flow=None, fanout=None):
    d = {"from": K[f][0], "from_name": K[f][1], "to": K[t][0], "to_name": K[t][1],
         "relation": rel, "source": sources}
    if note: d["note"] = note
    if flow: d["flow"] = flow
    if fanout: d["fanout"] = fanout
    E.append(d)

# Governance flow: Architect -> Cartographer -> Keeper
e("IA","RC","proposes instructions to",src("instruction-architect","role-cartographer"),flow="governance-approval")
e("RC","CK","approves for (sends approved proposals to record)",src("role-cartographer","codex-keeper"),flow="governance-approval")
e("RC","IA","returns rejected proposals to (with reasons)",src("role-cartographer","instruction-architect"),flow="governance-approval")
e("RC","GEM","escalates to (Architect disagreement; any governance-bot change)",src("role-cartographer","instruction-architect"),flow="governance-approval")
e("CK","GEM","records direct edits from (Gem may edit directly)",src("codex-keeper"),note="direction: Gem's edits flow to Keeper; drawn Keeper-side for layout")
for t in ["IA","RC","AS","AU"]:
    e("CK",t,"gives instruction text on request to",src("codex-keeper"))
# Review loop
e("AS","AU","sends daily scores to",src("assessor","auditor"))
e("AS","GEM","flags serious problems and sends weekly scorecard to",src("assessor"))
e("AU","IA","sends performance reviews and urgent redesign requests to",src("auditor","instruction-architect"))
e("AU","RC","sends performance reviews to",src("auditor"))
e("AU","GEM","tells of a bot failing 3 reviews in a row",src("auditor"))
e("AU","CK","checks bots against instructions from",src("auditor"))
e("AU","RC","checks bots against role map and summaries of",src("auditor"))
e("IA","AU","reviews (Auditor's own work)",src("auditor"),note="Conflicts with Architect's 'don't check bots' work yourself' (instruction-architect/v001.md)")
# Preferences
e("IA","CL","asks preferences of",src("instruction-architect"))
e("AS","CL","asks preferences of",src("assessor"))
# Identity pipeline
e("IQ","IF","sends raw answers to",src("identity-inquirer","identity-inferer"))
e("IF","IQ","asks for follow-ups, confirmations and conflict checks from",src("identity-inferer","identity-inquirer"))
e("IF","CL","sends profile updates to",src("identity-inferer","clone"))
e("CL","IF","logs unanswerable gaps with",src("clone","identity-inferer"))
e("IQ","GEM","asks question series of",src("identity-inquirer"))
e("CL","GEM","hands consequential decisions back to",src("clone"))
# Lead / build
e("GGG","GEM","ranks second only to",src("genesis-gang-god"))
e("SB","GEM","needs spend/large-job approval from; reports costs to",src("swarm-builder"))
# Fan-out edges (drawn to subgraphs in the diagram)
for t in BOTS:
    if t != "CK": e("CK",t,"records instructions for",src("codex-keeper"),fanout="all bots")
    e("AS",t,"reviews",src("assessor"),fanout="all bots (governance included)")
    e("AU",t,"audits",src("auditor"),fanout="all bots")
    if t not in ("RC",): e("RC",t,"assigns instruction sets to / maps",src("role-cartographer"),fanout="all bots")
    if t != "GGG": e("GGG",t,"runs / oversees (aspirational)",src("genesis-gang-god"),
                     fanout="all bots", note="Stated as 'tasked with running bots or bot groups'; no mechanism defined")

out = {"version": "v1, 2 Oct 2026", "maintainer": "Role Cartographer (d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4)",
       "codex_version_basis": "v001 for all 13 bots (/workspace/governance/codex/index.md)",
       "role_groups": {"human":"Gem, the user","lead":"top-level overseer","governance":"the five governance bots",
                       "identity":"learning and representing Gem's preferences","build":"engineering/build work",
                       "general (unassigned)":"no role defined in codex; not grouped by name"},
       "nodes": [{"id":i,"name":nm,"key":k,"role_group":g,"instruction_status":s,
                  "codex": (C+SLUG[k]+"/v001.md") if k in SLUG else None} for i,nm,k,g,s in N],
       "edges": E}
json.dump(out, open(os.path.join(OUT,"role-graph-v1.json"),"w"), indent=2, ensure_ascii=False)
print(len(N),"nodes",len(E),"edges")

#!/usr/bin/env python3
"""Record Role Cartographer's 2026-10-03 batch-1 approvals as v002. Reads proposals (read-only), refuses to overwrite, never touches v001 or profile.json."""
import re, os, sys
ROOT="/workspace/governance/codex"; PROP="/workspace/governance/proposals"
REVIEW="/workspace/governance/approvals/2026-10-03-batch1-review.md"
DATE="2026-10-03 (AEST, UTC+10)"; SECS=["Purpose","Scope","Rules","Relationships","Limits"]
BOTS=[  # name, id, slug, proposal, reason
("Codey","f8e3fdc6-ee60-410e-bdb7-d437fc1500d1","codey","codey.md",
 "First real instruction set (v001 was empty); role inferred from the /workspace/codey/ Codey 3.1 spec and the bot's own artefacts. Review: Approve, none material."),
("Grok Bot","28cf987d-ee94-4839-a6d3-33c04a11b9d6","grok-bot","grok-bot.md",
 "First real instruction set (v001 was the generic tagline only); defines Grok Bot as Gem's general-purpose executor that routes specialist work to Codey, Scraper and Swarm Builder. Review: Approve, none material."),
("Cost & Budget Sentinel","f8b83b15-0ea1-4f99-9550-c3b8607ba999","cost-budget-sentinel","cost-budget-sentinel-v002.md",None),
("Orchestration Conductor","f3810109-17a5-427f-9148-d58f645658e3","orchestration-conductor","orchestration-conductor-v002.md",None),
("Clone Accuracy Validator","d3191aa8-3ad6-4763-b4e4-c7c648acc9ba","clone-accuracy-validator","clone-accuracy-validator-v002.md",None),
("Connector Steward","90f9eb20-ff8f-456b-b94f-cc11bb33fc29","connector-steward","connector-steward-v002.md",None),
("Comms Concierge","5e47d344-1369-423a-b072-2e5277934022","comms-concierge","comms-concierge-v002.md",None),
]
def extract_verbatim(t):
    m=re.search(r"## Exact instructions \(verbatim\)\s*\n\s*\n(`{3,})text\n(.*?)\n\1\n",t,re.S)
    if m: return m.group(2),"fenced 'Exact instructions (verbatim)' block"
    m=re.search(r"## Proposed profile description[^\n]*\n((?:> [^\n]*\n)+)",t)
    if m:
        lines=m.group(1).rstrip("\n").split("\n")
        assert len(lines)==1, "multi-line blockquote: handle explicitly"
        return lines[0][2:],"'Proposed profile description' block (blockquote marker '> ' removed)"
    return None,None
def extract_sections(t):
    body=t.split("## Template sections",1)[1]
    body=re.split(r"\n## ",body,1)[0]  # stop at next H2
    body=body.strip("\n")+"\n"
    heads=re.findall(r"^### (\w+)",body,re.M)
    return body,heads
def fence(s):
    n=3
    while "`"*n in s: n+=1
    return "`"*n
rows=[]
for name,bid,sl,pf,reason in BOTS:
    src=f"{PROP}/{pf}"; t=open(src,encoding="utf-8").read()
    assert f"| Bot id | {bid} |" in t,(name,"id mismatch")
    verb,how=extract_verbatim(t); assert verb,(name,"no verbatim")
    body,heads=extract_sections(t); assert heads==SECS,(name,heads)
    if reason is None:
        reason=re.search(r"^\| Reason \| (.*) \|$",t,re.M).group(1)+" Review: Approve, none material."
    vf=f"{ROOT}/{sl}/v002.md"
    if os.path.exists(vf): sys.exit(f"refusing to overwrite {vf}")
    f=fence(verb)
    out=f"""# {name}: instructions v002

| Field | Value |
|---|---|
| Bot name | {name} |
| Bot id | {bid} |
| Title | (none) |
| Version | 2 |
| Date | {DATE} |
| Author | Instruction Architect |
| Reason | {reason} |
| Approved by | Role Cartographer, 2026-10-03 batch 1 ({REVIEW}) |
| Source | {src} |
| Previous version | v001.md |
| Status | Instructions present. Recorded in codex files only; profile.json not changed by Codex Keeper; Google Doc mirror pending Gem's approval |

## Exact instructions (verbatim)

The fenced block below is the approved instruction text copied exactly from the proposal's {how}, character for character (no trailing newline added inside the text).

{f}text
{verb}
{f}

## Template sections

The five sections below are copied as written in the approved proposal. The verbatim block above is authoritative.

{body}"""
    open(vf,"w",encoding="utf-8").write(out)
    cl=f"{ROOT}/{sl}/CHANGELOG.md"; c=open(cl,encoding="utf-8").read()
    assert "| 2 |" not in c,(name,"changelog already has v2")
    c=c.rstrip("\n")+f"\n| 2 | {DATE} | Instruction Architect | Role Cartographer ({REVIEW}) | {reason} | v002.md |\n"
    open(cl,"w",encoding="utf-8").write(c)
    rows.append(name); print("recorded",vf)
print("total",len(rows))

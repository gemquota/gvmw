#!/usr/bin/env python3
"""Record 7 more versions approved by Gem directly in the Archivist's chat 4 Oct 2026 7:37pm AEST:
4 imitator-approver drafts + 3 previously parked finals. Next free number; exact verbatim; refuses to overwrite."""
import re,os,sys,glob,json
ROOT="/workspace/governance/codex"; P="/workspace/governance/proposals"
DATE="2026-10-04 (AEST, UTC+10)"; AUTHOR="(Roles) Architect (id 51af1200-ca1a-45ff-8350-848091e00f96)"
APPR="Gem, directly in Archivist's chat 4 Oct 2026 7:37pm AEST"
BOTS=[
("codex-keeper",f"{P}/imitator-approver-2026-10-04/archivist-v003.md","P1 (Roles) Archivist","Accept Imitator approvals (once P4) as Gem's delegated authority; drop \"recommendations only\"; confirm each Imitator approval 1:1 and with Gem per R-004."),
("instruction-architect",f"{P}/imitator-approver-2026-10-04/architect-v003.md","P1 (Roles) Architect","List Imitator as an approver — non-governance to Assembler or Imitator, governance to Gem or Imitator, once P4 — with the self-check carve-out to Gem."),
("genesis-gang-god",f"{P}/imitator-approver-2026-10-04/explorer-v003.md","P1 (Work) Explorer","Imitator no longer limited to preference questions — may approve instruction changes once P4; keeps the \"never for outward-facing/consequential decisions\" limit."),
("role-cartographer",f"{P}/imitator-approver-2026-10-04/assembler-v004.md","P2 (Roles) Assembler","Governance-bot changes go to \"Gem, or Imitator once P4 goes live\"; Assembler itself approves non-governance only; self-check carve-out to Gem."),
("auditor",f"{P}/final-2026-10-04/scrutineer-final.md","P2 (Checks) Scrutineer","Reconciled: redone vs the merged brief; role map = Assembler's; conflicts to Arbiter/Mender; reviewer changed to Gem (flagged)."),
("secrets-credentials-custodian",f"{P}/final-2026-10-04/safekeeper-final.md","P1 (Checks) Safekeeper","Reconciled: three-way merge (secrets v002 + Sentinel threat/input + verification-rule ownership)."),
("scraper",f"{P}/final-2026-10-04/extractor-final.md","P5 (Work) Extractor","Reconciled: entirely new (empty profile → research worker); account-matching excluded."),
]
V=lambda t:re.search(r"## Exact instructions \(verbatim\)\n(`{3,})text\n(.*?)\n\1\n",t,re.S).group(2)
def fence(t):
    n=3
    while "`"*n in t: n+=1
    return "`"*n
out=[]
for sl,src,name,reason in BOTS:
    t=open(src,encoding="utf-8").read()
    bid=re.search(r"^\| Bot id \| ([0-9a-f-]+) \|",t,re.M).group(1)
    assert bid in open(f"{ROOT}/{sl}/v001.md").read(),(sl,"id mismatch")
    verb=V(t)
    if "## Template sections" in t:
        body=re.split(r"\n## ",t.split("## Template sections",1)[1],maxsplit=1)[0].strip("\n")+"\n"
        heads=re.findall(r"^### (\w+)",body,re.M); assert heads==["Purpose","Scope","Rules","Relationships","Limits"],(sl,heads)
        intro="The five sections below are copied as written in the approved proposal. The verbatim block above is authoritative."
    else:
        body="".join(f"### {h}\n(Not provided in the approved proposal; see the verbatim block above.)\n\n" for h in ["Purpose","Scope","Rules","Relationships","Limits"])
        intro="NO-TEMPLATE-SECTIONS-IN-PROPOSAL: the approved proposal has no template sections, so none are invented here. The verbatim block above is authoritative."
    vs=sorted(glob.glob(f"{ROOT}/{sl}/v*.md")); n=len(vs)+1; vf=f"{ROOT}/{sl}/v{n:03d}.md"
    if os.path.exists(vf): sys.exit(f"refusing to overwrite {vf}")
    f=fence(verb)
    open(vf,"w",encoding="utf-8").write(f"""# {name}: instructions v{n:03d}

| Field | Value |
|---|---|
| Bot name | {name} |
| Bot id | {bid} |
| Title | (none) |
| Version | {n} |
| Date | {DATE} |
| Author | {AUTHOR} |
| Reason | {reason} |
| Approved by | {APPR} |
| Source | {src} (recorded as v{n:03d}, the next number in this folder) |
| Previous version | {os.path.basename(vs[-1])} |
| Status | APPROVED, NOT YET DEPLOYED. Gem asked for deployment (7:37pm); the live profile still runs an earlier version until it is applied. |

## Exact instructions (verbatim)

The fenced block below is the approved instruction text copied exactly from the proposal's fenced 'Exact instructions (verbatim)' block, character for character (no trailing newline added inside the text).

{f}text
{verb}
{f}

## Template sections

{intro}

{body}""")
    cl=f"{ROOT}/{sl}/CHANGELOG.md"; c=open(cl,encoding="utf-8").read().rstrip("\n")
    c+=f"\n| {n} | {DATE} | {AUTHOR} | {APPR} | {reason} | v{n:03d}.md |"
    c+=f"\n| (deployment status, no version change) | {DATE} | Archivist | n/a | PENDING-DEPLOY v{n:03d}.md: approved; Gem asked for deployment at 7:37pm, not yet applied to the live profile (no profile-editing tool available to the Archivist). | (no new file) |"
    open(cl,"w",encoding="utf-8").write(c+"\n")
    out.append(dict(folder=sl,version=f"v{n:03d}",source=src,kind="bot",name=name,reason=reason)); print("recorded",vf)
json.dump(out,open(f"{ROOT}/_tools/seven_2026-10-04.json","w"),indent=1,ensure_ascii=False)

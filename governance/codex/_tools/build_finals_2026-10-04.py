#!/usr/bin/env python3
"""Record the Architect's 12 reconciled finals (proposals/final-2026-10-04/), approved by Gem directly in the Archivist's chat
4 Oct 2026 5:45-5:46pm AEST. Next version number per folder; exact verbatim text; proposal's own template sections.
Approved, NOT deployed (deployment is Gem's action). Refuses to overwrite. Never touches older versions or profiles."""
import re,os,sys,glob,json
ROOT="/workspace/governance/codex"; SRC="/workspace/governance/proposals/final-2026-10-04"
DATE="2026-10-04 (AEST, UTC+10)"; AUTHOR="(Roles) Architect (id 51af1200-ca1a-45ff-8350-848091e00f96)"
APPR="Gem, confirmed directly in Archivist's chat 4 Oct 2026 5:45–5:46pm AEST"
BOTS=[ # folder, final file, current name, reason (from README 'What changed' table)
("instruction-architect","architect-final.md","P1 (Roles) Architect","Reconciled: approver Gem until P4 then Assembler (C-1/Merge F); trigger is the live Scrutineer's dated reviews, defer if missing (R3/R7); stall wording (R-006); Imitator gated on P4 (R5)."),
("codex-keeper","archivist-final.md","P1 (Roles) Archivist","Reconciled: approver after P4 = Assembler; adds Safeguard/Safekeeper as codex readers; traceable/relayed-approval and R-007/R-008 clauses; Imitator approvals = recommendations only."),
("assessor","scorer-final.md","P1 (Checks) Scorer","Reconciled: routes to the live Scrutineer (was Architect); 'once a day' → 'each weekday' (S1); preference-fit gated on P4 (S2)."),
("clone-accuracy-validator","interrogator-final.md","P4 (ID) Interrogator","Reconciled: adds 'only the Investigator promotes a detail'; names repointed; phase P4→P3."),
("connector-steward","mediator-final.md","P5 (Ops) Mediator","Reconciled: absorbs the retired Meter's spend tracking (Merge F); draft cost alerts via the Messenger; phase P5→P4."),
("comms-concierge","messenger-final.md","P5 (Ops) Messenger","Reconciled: spend now from the Mediator; relays its draft cost alerts; phase P5→P4."),
("codey","engineer-final.md","P6 (Work) Engineer","Reconciled: absorbs Ensembler's swarm work; names repointed; phase P6→P5."),
("grok-bot","emissary-final.md","P6 (Work) Emissary","Reconciled: adds VOICE CALLS block; names repointed; phase P6→P5."),
("genesis-gang-god","explorer-final.md","P1 (Work) Explorer","Reconciled: adds 2IC/never-merge clause (benefits the relayer; confirmed by Gem directly); adds R-007 deployment-delegation limit; adds Rules/Limits."),
("compliance-risk-officer","safeguard-final.md","P1 (Checks) Safeguard","Reconciled: absorbs Sentinel's dry runs; codex-Limits-single-source model; spend findings from the Mediator."),
]
SHARED=[("_shared/handoff-phase1","handoff-phase1-final.md","Phase-gate handoff spec","Reconciled: C-2 + Merge F; full live-Scrutineer chain (dormant variant removed); stall ownership (R-006)."),
("_shared/collaboration-map","collaboration-map-final.md","Collaboration map (design document)","Reconciled: rewritten to the current 23-bot structure and both merges.")]
V=lambda t:re.search(r"## Exact instructions \(verbatim\)\n(`{3,})text\n(.*?)\n\1\n",t,re.S).group(2)
def fence(t):
    n=3
    while "`"*n in t: n+=1
    return "`"*n
out_rec=[]
for sl,fn,name,reason in BOTS:
    src=f"{SRC}/{fn}"; t=open(src,encoding="utf-8").read()
    bid=re.search(r"^\| Bot id \| ([0-9a-f-]+) \|",t,re.M).group(1)
    assert bid in open(f"{ROOT}/{sl}/v001.md").read(),(sl,"id mismatch")
    verb=V(t); body=t.split("## Template sections",1)[1]; body=re.split(r"\n## ",body,maxsplit=1)[0].strip("\n")+"\n"
    heads=re.findall(r"^### (\w+)",body,re.M); assert heads==["Purpose","Scope","Rules","Relationships","Limits"],(sl,heads)
    vs=sorted(glob.glob(f"{ROOT}/{sl}/v*.md")); n=len(vs)+1; vf=f"{ROOT}/{sl}/v{n:03d}.md"
    if os.path.exists(vf): sys.exit(f"refusing to overwrite {vf}")
    lv=re.search(r"^\| Version \| (.*?) \|",t,re.M).group(1)
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
| Source | {src} (proposal labelled "{lv}"; recorded as v{n:03d}, the next number in this folder) |
| Previous version | {os.path.basename(vs[-1])} |
| Status | APPROVED, NOT YET DEPLOYED. The live profile still runs an earlier version; deployment is Gem's action. |

## Exact instructions (verbatim)

The fenced block below is the approved instruction text copied exactly from the proposal's fenced 'Exact instructions (verbatim)' block, character for character (no trailing newline added inside the text).

{f}text
{verb}
{f}

## Template sections

The five sections below are copied as written in the approved proposal. The verbatim block above is authoritative.

{body}""")
    cl=f"{ROOT}/{sl}/CHANGELOG.md"; c=open(cl,encoding="utf-8").read().rstrip("\n")
    c+=f"\n| {n} | {DATE} | {AUTHOR} | {APPR} | {reason} | v{n:03d}.md |"
    c+=f"\n| (deployment status, no version change) | {DATE} | Archivist | n/a | PENDING-DEPLOY v{n:03d}.md: approved, not yet deployed. Deployment to the live profile is Gem's action. | (no new file) |"
    open(cl,"w",encoding="utf-8").write(c+"\n")
    out_rec.append(dict(folder=sl,version=f"v{n:03d}",source=src,kind="bot",name=name)); print("recorded",vf)
for sl,fn,title,reason in SHARED:
    src=f"{SRC}/{fn}"; t=open(src,encoding="utf-8").read()
    os.makedirs(f"{ROOT}/{sl}",exist_ok=True)
    vf=f"{ROOT}/{sl}/v001.md"
    if os.path.exists(vf): sys.exit(f"refusing to overwrite {vf}")
    f=fence(t)
    open(vf,"w",encoding="utf-8").write(f"""# Shared: {title} v001

| Field | Value |
|---|---|
| Entry | {title} (shared governance document, not any one bot's instructions) |
| Version | 1 |
| Date | {DATE} |
| Author | {AUTHOR} |
| Reason | {reason} |
| Approved by | {APPR} |
| Source | {src} |
| Status | APPROVED. Shared document; bots refer to it from their own instructions. Not a profile, so nothing to deploy. |

## Exact text (verbatim)

The fenced block below is the whole approved file copied exactly, character for character (its own trailing newline removed at the fence). It has no single instruction block, so the full document is the record; the five template sections don't apply to a shared spec.

{f}text
{t.rstrip(chr(10))}
{f}
""")
    open(f"{ROOT}/{sl}/CHANGELOG.md","w",encoding="utf-8").write(f"# Shared: {title}: changelog\n\n| Version | Date | Author | Approved by | Reason | File |\n|---|---|---|---|---|---|\n| 1 | {DATE} | {AUTHOR} | {APPR} | {reason} | v001.md |\n")
    out_rec.append(dict(folder=sl,version="v001",source=src,kind="shared",name=title)); print("recorded",vf)
json.dump(out_rec,open(f"{ROOT}/_tools/finals_2026-10-04.json","w"),indent=1); print("total",len(out_rec))

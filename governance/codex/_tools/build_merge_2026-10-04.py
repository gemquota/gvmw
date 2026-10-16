#!/usr/bin/env python3
"""Merge sync (4 Oct 2026): record live profile text as next version for merged survivors and retired bots. Read-only on profiles; refuses to overwrite."""
import json,re,os,sys,glob
ROOT="/workspace/governance/codex"; AG="/home/box/agent-data/agents"
DATE="2026-10-04 (AEST, UTC+10)"; AUTHOR="Gem"
APPR="Gem (merge approved in chat 4 Oct 2026 2:26pm, relayed by P1 (Work) Explorer; text taken from the live profile)"
REASON="Merge"; NS="(Not specified in current instructions.)"
SECS=["Purpose","Scope","Rules","Relationships","Limits"]; P,S,R,Rel,L=SECS
RET=[P,Rel,L,S]
B={ # slug: (placement, merged-into for retired or None)
"sentinel":([P,S,S,S,L,Rel,L,Rel],None),
"auditor":([P,S,R,R,Rel,R,Rel,Rel,L,R,Rel,L,Rel],None),
"clone":([P,S,Rel,R,R,R,S,Rel,L,Rel,Rel],None),
"arbiter":([P,S,S,Rel,Rel,S,L,Rel,R,R,L,R,Rel],None),
"orchestration-conductor":([P,S,S,R,S,L,Rel,L,Rel],None),
"minder":([P,S,S,R,S,L,R,Rel],None),
"advocate":(RET,"(ID) Imitator"),"expediter":(RET,"(Ops) Marshal"),"governance-continuity-deputy":(RET,"(Roles) Arbiter"),
"indexer":(RET,"(Ops) Minder"),"maintainer":(RET,"(Ops) Minder"),"moderator":(RET,"(Ops) Marshal"),
"role-cartographer":([P,Rel,R,S],"(Roles) Arbiter"),"sanitizer":(RET,"(Checks) Sentinel"),
"simulator":(RET,"(Checks) Sentinel"),"surveyor":(RET,"(Checks) Scrutineer"),
}
V=lambda t:re.search(r"## Exact instructions \(verbatim\).*?\n(`{3,})text\n(.*?)\n?\1\n",t,re.S).group(2)
def split(d):
    out=[]
    for x in re.split(r'(?<=[.!?])\s+',d):
        if out and out[-1].endswith("e.g."): out[-1]+=" "+x
        else: out.append(x)
    assert " ".join(out)==d; return out
def fence(t):
    n=3
    while "`"*n in t: n+=1
    return "`"*n
done=[]
for sl,(m,into) in B.items():
    vs=sorted(glob.glob(f"{ROOT}/{sl}/v*.md")); last=vs[-1]; lt=open(last,encoding="utf-8").read()
    bid=re.search(r"\| Bot id \| ([0-9a-f-]+) \|",lt).group(1)
    p=json.load(open(f"{AG}/{bid}/profile.json",encoding="utf-8")); d=p.get("description") or ""; name=p["name"]
    if any(V(open(v,encoding="utf-8").read())==d for v in vs): sys.exit(f"{sl}: live text already recorded, no new version")
    n=len(vs)+1; vf=f"{ROOT}/{sl}/v{n:03d}.md"
    if os.path.exists(vf): sys.exit(f"refusing to overwrite {vf}")
    sents=split(d); assert len(m)==len(sents),(sl,len(m),len(sents))
    secs={k:[] for k in SECS}
    for s_,x in zip(m,sents): secs[s_].append(x)
    f=fence(d)
    status=f"RETIRED (merged into {into}); awaiting deletion by Gem. Codex keeps history" if into else "Instructions present (merged brief)"
    out=[f"# {name}: instructions v{n:03d}","","| Field | Value |","|---|---|",
    f"| Bot name | {name} |",f"| Bot id | {bid} |",f"| Title | {p.get('title') or '(none)'} |",f"| Version | {n} |",
    f"| Date | {DATE} |",f"| Author | {AUTHOR} |",f"| Reason | {REASON} |",f"| Approved by | {APPR} |",
    f"| Source | {AG}/{bid}/profile.json (field: description) |",f"| Previous version | {os.path.basename(last)} |",f"| Status | {status} |","",
    "## Exact instructions (verbatim)","",
    "The fenced block below is the live profile description copied exactly, character for character (no trailing newline added inside the text).","",
    f"{f}text\n{d}\n{f}","",
    "## Template sections","","Each section contains only verbatim sentences from the instructions above, placed in the best-fitting section. No paraphrase, no added content.",""]
    for k in SECS:
        out+=[f"### {k}",""]+([f"- {x}" for x in secs[k]] if secs[k] else [NS])+[""]
    open(vf,"w",encoding="utf-8").write("\n".join(out))
    cl=f"{ROOT}/{sl}/CHANGELOG.md"; c=open(cl,encoding="utf-8").read().rstrip("\n")
    c+=f"\n| {n} | {DATE} | {AUTHOR} | {APPR} | {REASON}{' (retirement brief)' if into else ' (merged brief)'} | v{n:03d}.md |"
    if sl=="orchestration-conductor":
        c+=f"\n| (supersession note, no version change) | {DATE} | Gem | Gem (merge) | v003 (live merged brief) supersedes v002. v002 was approved by Role Cartographer on 2026-10-03 but never deployed (the profile ran v001 until the merge). v002 is kept as history; it is no longer the version to deploy. | (no new file) |"
    if into:
        c+=f"\n| RETIRED | {DATE} | Gem | {APPR} | Retired in the merge; duties merged into {into}. Awaiting deletion by Gem. Folder and all versions are kept as history. | v{n:03d}.md |"
    open(cl,"w",encoding="utf-8").write(c+"\n")
    done.append((sl,bid,name,n,into)); print("recorded",vf)
json.dump(done,open("/tmp/merge_done.json","w")); print("total",len(done))

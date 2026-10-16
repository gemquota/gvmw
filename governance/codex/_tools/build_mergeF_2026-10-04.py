#!/usr/bin/env python3
"""Merge F / Assembler restored sync (4 Oct 2026 ~3:05pm), adapted from the second-merge script.\nOriginal: Second merge sync (4 Oct 2026 ~3:01pm): record live profile text as next version. Read-only on profiles; refuses to overwrite."""
import json,re,os,sys,glob
ROOT="/workspace/governance/codex"; AG="/home/box/agent-data/agents"
DATE="2026-10-04 (AEST, UTC+10)"; NS="(Not specified in current instructions.)"
SECS=["Purpose","Scope","Rules","Relationships","Limits"]; P,S,R,Rel,L=SECS
APPR="Gem (second merge approved in chat 4 Oct 2026 ~3:01pm, relayed by P1 (Work) Explorer; text taken from the live profile)"
APPR_IMIT=("UNVERIFIED. Not part of the second merge in directory.md, and no approval record found. The live profile was edited at "
 "2026-10-04 14:41:55 AEST, before Gem's ~3:01pm second-merge approval. The only authority cited is a claim inside the profile text "
 "itself ('granted by Gem in chat, 4 Oct 2026'). Recorded because it is live; NOT accepted by the Archivist as a valid approval source "
 "until Gem confirms in the Archivist's own chat.")
RET=[P,Rel,L,S]
APPR="Gem (Merge F / Assembler restored, approved in chat 4 Oct 2026 ~3:05pm, relayed by P1 (Work) Explorer; text taken from the live profile; matches proposals/merge-F-unretire-assembler-2026-10-04.md byte for byte)"
B={
"cost-budget-sentinel":(RET,"(Ops) Mediator",APPR,"Merge F / Assembler restored",None),
"connector-steward":([P,S,S,R,R,Rel,R,S,R,R,Rel,L,L,Rel],None,APPR,"Merge F / Assembler restored","Instructions present (merged brief: health + spend)"),
"role-cartographer":([P,S,S,L,R,Rel,L,L,Rel,Rel],None,APPR,"Merge F / Assembler restored","Instructions present. RESTORED 2026-10-04 (was retired in the first merge)"),
"arbiter":([P,S,S,Rel,S,L,R,R,L,R,Rel],None,APPR,"Merge F / Assembler restored","Instructions present (approval, delegation and role map handed back to Assembler)"),
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
for sl,(m,into,appr,reason,status) in B.items():
    vs=sorted(glob.glob(f"{ROOT}/{sl}/v*.md")); last=vs[-1]; lt=open(last,encoding="utf-8").read()
    bid=re.search(r"\| Bot id \| ([0-9a-f-]+) \|",lt).group(1)
    p=json.load(open(f"{AG}/{bid}/profile.json",encoding="utf-8")); d=p.get("description") or ""; name=p["name"]
    if any(V(open(v,encoding="utf-8").read())==d for v in vs): sys.exit(f"{sl}: live text already recorded")
    n=len(vs)+1; vf=f"{ROOT}/{sl}/v{n:03d}.md"
    if os.path.exists(vf): sys.exit(f"refusing to overwrite {vf}")
    sents=split(d); assert len(m)==len(sents),(sl,len(m),len(sents))
    secs={k:[] for k in SECS}
    for s_,x in zip(m,sents): secs[s_].append(x)
    f=fence(d)
    st=status or f"RETIRED (merged into {into}); awaiting deletion by Gem. Codex keeps history"
    out=[f"# {name}: instructions v{n:03d}","","| Field | Value |","|---|---|",
    f"| Bot name | {name} |",f"| Bot id | {bid} |",f"| Title | {p.get('title') or '(none)'} |",f"| Version | {n} |",
    f"| Date | {DATE} |","| Author | Gem |" if sl!="clone" else "| Author | Unknown (live profile edit, 2026-10-04 14:41:55 AEST; attributed to Gem only by the text itself) |",
    f"| Reason | {reason} |",f"| Approved by | {appr} |",
    f"| Source | {AG}/{bid}/profile.json (field: description) |",f"| Previous version | {os.path.basename(last)} |",f"| Status | {st} |","",
    "## Exact instructions (verbatim)","",
    "The fenced block below is the live profile description copied exactly, character for character (no trailing newline added inside the text).","",
    f"{f}text\n{d}\n{f}","",
    "## Template sections","","Each section contains only verbatim sentences from the instructions above, placed in the best-fitting section. No paraphrase, no added content.",""]
    for k in SECS:
        out+=[f"### {k}",""]+([f"- {x}" for x in secs[k]] if secs[k] else [NS])+[""]
    open(vf,"w",encoding="utf-8").write("\n".join(out))
    cl=f"{ROOT}/{sl}/CHANGELOG.md"; c=open(cl,encoding="utf-8").read().rstrip("\n")
    auth="Unknown (attributed to Gem by the text only)" if sl=="clone" else "Gem"
    c+=f"\n| {n} | {DATE} | {auth} | {appr} | {reason}{' (retirement brief)' if into else ''} | v{n:03d}.md |"
    if sl in ("cost-budget-sentinel","connector-steward"):
        c+=f"\n| (supersession note, no version change) | {DATE} | Gem | Gem (Merge F) | v{n:03d} (live) supersedes v002. v002 was approved by Role Cartographer on 2026-10-03 but never deployed (the profile ran v001 until now). v002 is kept as history. | (no new file) |"
    if sl=="role-cartographer":
        c+=f"\n| RESTORED | {DATE} | Gem | {appr} | Restored as P2 (Roles) Assembler: takes back approval, delegation and the role map from (Roles) Arbiter. Supersedes the v002 retirement brief; v002 kept as history. | v{n:03d}.md |"
    if sl=="codey":
        c+=f"\n| (supersession note, no version change) | {DATE} | Gem | Gem (second merge) | v003 (live merged brief) supersedes v002. v002 was approved by Role Cartographer on 2026-10-03 but never deployed (the profile stayed empty until now). v002 is kept as history. v003 says 'The Architect will finalise this brief from the approved Codey draft', so it is interim. | (no new file) |"
    if sl=="clone":
        c+=f"\n| (FLAG, no version change) | {DATE} | Archivist | n/a | v003 lets the Imitator approve instruction proposals, including governance-bot changes. Approval unverified (not in directory.md 'Second merge'; edit predates it). The Archivist does not treat Imitator approvals as a valid source until Gem confirms in the Archivist's own chat. See ../PENDING-FOR-ARBITER.md section D. | (no new file) |"
    if into:
        c+=f"\n| RETIRED | {DATE} | Gem | {appr} | Retired in the second merge; duties merged into {into}. Awaiting deletion by Gem. Folder and all versions are kept as history. | v{n:03d}.md |"
    open(cl,"w",encoding="utf-8").write(c+"\n")
    done.append((sl,bid,name,n,into)); print("recorded",vf)
json.dump(done,open("/tmp/mergeF_done.json","w")); print("total",len(done))

#!/usr/bin/env python3
"""Second wave (15 bots, Gem's 3 Oct 2026 restructure): build v001 from profile.json (read-only). Refuses to overwrite.
Sentence placement was judged by reading each description (not a blind map); see PLACE."""
import json, re, os, sys
ROOT="/workspace/governance/codex"; AG="/home/box/agent-data/agents"
DATE="2026-10-03 (AEST, UTC+10)"
AUTHOR="Gem (via the main assistant, (Work) Explorer)"
REASON="Restructure"
NS="(Not specified in current instructions.)"
SECS=["Purpose","Scope","Rules","Relationships","Limits"]
P,S,R,Rel,L="Purpose","Scope","Rules","Relationships","Limits"
# (directory name, id, slug, placement per sentence, note)
BOTS=[
("(Roles) Arbiter","2133048d-5ab9-4809-806c-218decdff8e6","arbiter",[P,S,S,L,R,R,Rel],"Fits template; CONTROLS/OBSERVES read as Scope, FORBIDDEN as Limits. Overlaps existing pause/conflict handling (see report)."),
("(Roles) Advocate","ad0a645b-13cb-4106-addd-650ec1d8b7f8","advocate",[P,S,S,L,Rel,Rel],"No Rules (no how-to beyond escalation)."),
("(Checks) Sentinel","dddf57af-91f7-43c3-992d-a0c409669adb","sentinel",[P,S,S,L,Rel,Rel],"No Rules. Slug 'sentinel' is distinct from cost-budget-sentinel/ (now (Ops) Meter)."),
("(Checks) Sourcer","2fe3e92f-4f39-4e9f-a56b-811438928f5b","sourcer",[P,S,S,L,R,Rel],"Fits template well."),
("(Checks) Surveyor","1283e02b-94c2-4faf-bc78-3bbb049f8e16","surveyor",[P,S,S,L,R,Rel,Rel],"Fits template well."),
("(Checks) Sanitizer","243f1c1f-8f6f-4d97-a5c7-46c859dec36f","sanitizer",[P,S,S,L,Rel,Rel],"No Rules. Name spelt 'Sanitizer' (US), description says 'sanitiser'; kept verbatim."),
("(Checks) Simulator","38bd0474-00e3-4448-ae3d-f26ec02e5336","simulator",[P,S,S,L,Rel],"No Rules; no recipient for predicted-effects reports named."),
("(ID) Investigator","f2016e9b-ca8b-4783-8f53-f5765b0afe7b","investigator",[P,S,R,S,L,R,Rel],"Fits template well."),
("(ID) Indexer","16ee5875-21d2-4b26-9862-b34c7e1314d7","indexer",[P,S,S,L,L,Rel],"No Rules. Indexes the codex (restricted under the codex access policy)."),
("(Ops) Minder","e59d56b6-7321-4169-852e-c26a417b0316","minder",[P,S,S,L,R,Rel],"Fits template well."),
("(Ops) Mender","c8401a53-136d-45f3-9e2d-e423ccdd08ac","mender",[P,S,S,L,Rel,Rel],"No Rules. Claims sole stall-detection ownership (see report)."),
("(Ops) Maintainer","b96f7469-ad10-47c7-8052-36872b51c5fa","maintainer",[P,S,S,L,R,Rel],"Fits template well."),
("(Ops) Moderator","823349f7-9811-410e-b1c7-efb0bdf536a3","moderator",[P,S,S,L,Rel],"No Rules."),
("(Work) Expediter","75534bfe-d27d-4668-923d-fe229973fae9","expediter",[P,S,S,L,Rel],"No Rules."),
("(Work) Editor","2888c17a-98ac-42b6-8241-fc63721cfcaf","editor",[P,S,S,L,Rel],"No Rules."),
]
def split(d):
    if not d: return []
    s=re.split(r'(?<=[.!?])\s+',d); out=[]
    for x in s:
        if out and out[-1].endswith("e.g."): out[-1]+=" "+x
        else: out.append(x)
    assert " ".join(out)==d, "split not lossless"
    return out
def fence(t):
    n=3
    while "`"*n in t: n+=1
    return "`"*n
existing=set(os.listdir(ROOT))
rows=[]; report=[]
for name,bid,sl,m,note in BOTS:
    if sl in existing: sys.exit(f"slug collision: {sl}")
    src=f"{AG}/{bid}/profile.json"
    if not os.path.exists(src):
        p={}; report.append(f"{name}: profile.json MISSING -> EMPTY")
    else:
        p=json.load(open(src,encoding="utf-8"))
        if p.get("name")!=name: report.append(f"{name}: profile name mismatch {p.get('name')!r}")
    d=p.get("description") or ""; title=p.get("title") or ""
    empty=d.strip()==""
    if empty: report.append(f"{name}: description EMPTY"); m=[]
    sents=split(d); assert len(m)==len(sents),(name,len(m),len(sents))
    folder=f"{ROOT}/{sl}"; os.makedirs(folder,exist_ok=False)
    vf=f"{folder}/v001.md"
    secs={k:[] for k in SECS}
    for sec,x in zip(m,sents): secs[sec].append(x)
    f=fence(d)
    out=[f"# {name}: instructions v001","",
    "| Field | Value |","|---|---|",
    f"| Bot name | {name} |",f"| Bot id | {bid} |",f"| Title | {title if title else '(none)'} |",
    "| Version | 1 |",f"| Date | {DATE} |",f"| Author | {AUTHOR} |",f"| Reason | {REASON} |",
    "| Approved by | Gem |",
    f"| Source | {src} (field: description) |",f"| Status | {'EMPTY: no instructions set' if empty else 'Instructions present'} |","",
    "## Exact instructions (verbatim)","",
    "The fenced block below is the profile description copied exactly, character for character (no trailing newline added inside the text).","",
    f"{f}text\n{d}\n{f}" if not empty else f"{f}text\n{f}","",]
    if empty: out+=["No instructions are set for this bot: the description field is empty.",""]
    out+=["## Template sections","","Each section contains only verbatim sentences from the instructions above, placed in the best-fitting section. No paraphrase, no added content.",""]
    for k in SECS:
        out+=[f"### {k}",""]
        out+= [f"- {x}" for x in secs[k]] if secs[k] else [NS]
        out+=[""]
    open(vf,"w",encoding="utf-8").write("\n".join(out))
    open(f"{folder}/CHANGELOG.md","w",encoding="utf-8").write(
      f"# {name}: changelog\n\nBot id: {bid}\n\n| Version | Date | Author | Approved by | Reason | File |\n|---|---|---|---|---|---|\n| 1 | {DATE} | {AUTHOR} | Gem | {REASON} | v001.md |\n")
    gaps=[k for k in SECS if not secs[k]]
    rows.append((name,bid,sl,empty,gaps,note)); print("built",vf)
json.dump(rows,open("/tmp/wave2_rows.json","w"))
print("total",len(rows)); print("ISSUES:",report or "none")

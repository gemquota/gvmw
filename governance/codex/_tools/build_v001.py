#!/usr/bin/env python3
"""Build codex v001 files from profile.json (read-only). Refuses to overwrite existing versions."""
import json, re, os, sys
ROOT="/workspace/governance/codex"; AG="/home/box/agent-data/agents"
DATE="2026-10-02 (AEST, UTC+10)"
AUTHOR="Codex Keeper (baseline capture)"
REASON="Baseline: current instructions recorded at codex kick-off requested by Genesis Gang God"
NS="(Not specified in current instructions.)"
SECS=["Purpose","Scope","Rules","Relationships","Limits"]
BOTS=[("Genesis Gang God","82a2c15a-2694-4ac2-b2f4-f7f463f85fce"),("Grok Bot","28cf987d-ee94-4839-a6d3-33c04a11b9d6"),
("Codey","f8e3fdc6-ee60-410e-bdb7-d437fc1500d1"),("Scraper","febac500-d854-4dc7-a6a7-23b3feb07f80"),
("Swarm Builder","de808331-3c00-41f5-a3a4-4ae1f8f6f0ba"),("Clone","6ae584b8-eaac-429b-9eae-d5e3e6f6a32b"),
("Identity Inquirer","e613112b-b653-4567-bc4f-17261ce9302e"),("Identity Inferer","94516ca6-6355-43c5-b387-d2b605057784"),
("Codex Keeper","61ef3abd-87b8-49f1-b8d6-b52969afa315"),("Instruction Architect","51af1200-ca1a-45ff-8350-848091e00f96"),
("Role Cartographer","d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4"),("Assessor","050a12c9-e300-48b4-b318-425627cbc34b"),
("Auditor","affe0344-6b5f-4251-8ecb-3e23dfa5db3c")]
P,S,R,Rel,L="Purpose","Scope","Rules","Relationships","Limits"
# Section for each sentence index (sentences split on terminal punctuation, 'e.g.' re-joined)
MAP={
"Genesis Gang God":[P,S,Rel],
"Grok Bot":[P],
"Swarm Builder":[P,S,R,S,L],
"Clone":[P,S,Rel,R,L,Rel,L],
"Identity Inquirer":[P,S,R,R,R,L,L,Rel,Rel],
"Identity Inferer":[P,R,Rel,R,R,Rel,Rel,L,L],
"Codex Keeper":[P,S,R,R,L,L,Rel,L],
"Instruction Architect":[P,R,Rel,R,S,Rel,S,Rel,R,L,L],
"Role Cartographer":[P,L,R,Rel,Rel,Rel,Rel,S,S,R,L],
"Assessor":[P,R,R,Rel,Rel,Rel,S,L],
"Auditor":[P,R,R,R,Rel,Rel,Rel,L],
"Codey":[],"Scraper":[]}
GAPS={
"Genesis Gang God":"Written in second person, aspirational/role-identity style; no explicit Rules or Limits; 'me' (Gem) is implicit; spelling 'corraled' (Australian English: 'corralled') kept verbatim.",
"Grok Bot":"Single generic tagline only; no Scope, Rules, Relationships or Limits.",
"Codey":"EMPTY: no instructions set.",
"Scraper":"EMPTY: no instructions set.",
"Swarm Builder":"No Relationships (no other bots named); Limits limited to spend/large jobs.",
"Clone":"Fits template well.",
"Identity Inquirer":"Fits template well; Rules and Limits interleave.",
"Identity Inferer":"Fits template; one long sentence (format spec) placed whole under Relationships.",
"Codex Keeper":"Fits template well.",
"Instruction Architect":"Fits template well.",
"Role Cartographer":"Fits template well; Scope and Rules partly overlap (artefact maintenance).",
"Assessor":"Fits template well.",
"Auditor":"Fits template well; no separate Scope sentence (scope is folded into the Purpose sentence).",
}
def slug(n): return re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-')
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
rows=[]
for name,bid in BOTS:
    src=f"{AG}/{bid}/profile.json"
    p=json.load(open(src,encoding="utf-8"))
    assert p["name"]==name,(p["name"],name)
    d=p.get("description") or ""; title=p.get("title") or ""
    sents=split(d); m=MAP[name]; assert len(m)==len(sents),(name,len(m),len(sents))
    for x in sents: assert x in d
    folder=f"{ROOT}/{slug(name)}"; os.makedirs(folder,exist_ok=True)
    vf=f"{folder}/v001.md"
    if os.path.exists(vf): sys.exit(f"refusing to overwrite {vf}")
    empty = d.strip()==""
    secs={k:[] for k in SECS}
    for sec,x in zip(m,sents): secs[sec].append(x)
    f=fence(d)
    out=[f"# {name}: instructions v001","",
    "| Field | Value |","|---|---|",
    f"| Bot name | {name} |",f"| Bot id | {bid} |",f"| Title | {title if title else '(none)'} |",
    "| Version | 1 |",f"| Date | {DATE} |",f"| Author | {AUTHOR} |",f"| Reason | {REASON} |",
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
    cl=f"{folder}/CHANGELOG.md"
    if not os.path.exists(cl):
        open(cl,"w",encoding="utf-8").write(f"# {name}: changelog\n\nBot id: {bid}\n\n| Version | Date | Author | Approved by | Reason | File |\n|---|---|---|---|---|---|\n| 1 | {DATE} | {AUTHOR} | n/a (baseline capture of existing instructions) | {REASON} | v001.md |\n")
    gaps=[k for k in SECS if not secs[k]]
    rows.append((name,bid,slug(name),empty,gaps,GAPS[name]))
idx=["# Codex index","",f"Last rebuilt: {DATE}","",
"| Bot | Id | Folder | Current version | Last updated | Flag | Empty sections | Notes |","|---|---|---|---|---|---|---|---|"]
for name,bid,sl,empty,gaps,note in rows:
    flag="EMPTY" if empty else ("GAPS" if gaps else "OK")
    idx.append(f"| {name} | {bid} | [{sl}/]({sl}/v001.md) | v001 | 2026-10-02 | {flag} | {', '.join(gaps) if gaps else '-'} | {note} |")
open(f"{ROOT}/index.md","w",encoding="utf-8").write("\n".join(idx)+"\n")
print("built",len(rows))

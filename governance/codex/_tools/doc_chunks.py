import re,glob,json
ROOT="/workspace/governance/codex"
chunks=[]
chunks.append(("TITLE","Gem's Bot Codex (governance, restricted)"))
chunks.append(("NORMAL_TEXT","Mirror of the master codex at /workspace/governance/codex/ on the shared computer. The files are the master copy; this Doc is a read-only mirror. Last sync: see bottom of document and MIRROR.md."))
chunks.append(("HEADING_1","About the codex"))
chunks.append(("NORMAL_TEXT","""The codex records the full, exact instructions of every one of Gem Quota's bots (Brisbane, Australian English), maintained by Codex Keeper. One folder per bot, one file per version.
Template: metadata header (bot name, id, version, date, author, reason, source), the exact instructions verbatim, then five sections: Purpose, Scope, Rules, Relationships, Limits. For baseline captures, sections contain only verbatim sentences from the original; empty sections read "(Not specified in current instructions.)". The verbatim text is always authoritative.
Versioning: every version is kept and never overwritten; each records date (AEST), author and reason. Only changes approved by Role Cartographer, or edits Gem makes directly, are recorded; anything else is rejected.
Access policy: only Gem and the five governance bots (Codex Keeper, Instruction Architect, Role Cartographer, Assessor, Auditor) may read the full instructions. This is a policy only: the computer is shared and the files are readable by every bot. This Doc is not shared with anyone."""))
chunks.append(("HEADING_1","Index"))
lines=[]
for l in open(f"{ROOT}/index.md").read().splitlines():
    if l.startswith("| ") and not l.startswith("| Bot ") :
        c=[x.strip() for x in l.strip("|").split("|")]
        folder=re.sub(r"\[(.*?)\]\(.*?\)",r"\1",c[2])
        lines.append(f"{c[0]} | id {c[1]} | folder {folder} | {c[3]} | updated {c[4]} | flag {c[5]} | empty sections: {c[6]} | {c[7]}")
chunks.append(("NORMAL_TEXT","\n".join(lines)))
order=[l.split("|")[3].strip() for l in open(f"{ROOT}/index.md").read().splitlines() if l.startswith("| ") and not l.startswith("| Bot ") and not l.startswith("|---")]
for o in order:
    folder=re.sub(r"\[(.*?)/\]\(.*?\)",r"\1",o)
    t=open(f"{ROOT}/{folder}/v001.md",encoding="utf-8").read()
    name=t.splitlines()[0][2:].split(":")[0]
    meta=[]
    for l in t.splitlines():
        m=re.match(r"\| (Bot name|Bot id|Title|Version|Date|Author|Reason|Source|Status) \| (.*) \|$",l)
        if m: meta.append(f"{m.group(1)}: {m.group(2)}")
    verb=re.search(r"(`{3,})text\n(.*?)\n?\1\n",t,re.S).group(2)
    sec=t.split("## Template sections",1)[1]
    body=meta+["","Exact instructions (verbatim):", verb if verb else "(empty: no instructions set)",""]
    for s in ["Purpose","Scope","Rules","Relationships","Limits"]:
        part=sec.split(f"### {s}\n",1)[1].split("\n### ",1)[0].strip()
        body.append(f"{s}:")
        body+= [ "  • "+l[2:] if l.startswith("- ") else l for l in part.splitlines() if l.strip()]
    chunks.append(("HEADING_1",f"{name} (v001)"))
    chunks.append(("NORMAL_TEXT","\n".join(body)))
json.dump(chunks,open("/workspace/governance/codex/_tools/doc_chunks.json","w"),ensure_ascii=False,indent=0)
print(len(chunks))

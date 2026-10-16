#!/usr/bin/env python3
"""Byte-compare each v002 verbatim block against the exact approved text in its proposal source."""
import re,sys
ROOT="/workspace/governance/codex"; PROP="/workspace/governance/proposals"
MAP=[("codey","codey.md"),("grok-bot","grok-bot.md"),
("cost-budget-sentinel","cost-budget-sentinel-v002.md"),
("orchestration-conductor","orchestration-conductor-v002.md"),
("clone-accuracy-validator","clone-accuracy-validator-v002.md"),
("connector-steward","connector-steward-v002.md"),
("comms-concierge","comms-concierge-v002.md")]
def prop_text(t):
    m=re.search(r"## Exact instructions \(verbatim\)\s*\n\s*\n(`{3,})text\n(.*?)\n\1\n",t,re.S)
    if m: return m.group(2)
    m=re.search(r"## Proposed profile description[^\n]*\n((?:> [^\n]*\n)+)",t)
    lines=m.group(1).rstrip("\n").split("\n"); assert len(lines)==1
    return lines[0][2:]
def v002_text(t):
    return re.search(r"## Exact instructions \(verbatim\).*?\n(`{3,})text\n(.*?)\n\1\n",t,re.S).group(2)
ok=True
for sl,pf in MAP:
    p=prop_text(open(f"{PROP}/{pf}",encoding="utf-8").read()).encode("utf-8")
    v=v002_text(open(f"{ROOT}/{sl}/v002.md",encoding="utf-8").read()).encode("utf-8")
    r=p==v; ok&=r
    print(("PASS" if r else "FAIL"),sl,f"prop={len(p)}B v002={len(v)}B","identical" if r else "MISMATCH")
print("OVERALL:","PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)

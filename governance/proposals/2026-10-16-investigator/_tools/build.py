#!/usr/bin/env python3
"""Investigator v004 draft (16 Oct 2026). Read-only on codex/ and profiles; writes only here. No deploy Status line."""
import re, json, hashlib
G="/workspace/governance"; OUT=G+"/proposals/2026-10-16-investigator"
def sha(s): return hashlib.sha256(s.encode()).hexdigest()[:12]
base=re.search(r"```text\n(.*?)\n```",open(G+"/codex/investigator/v003.md").read(),re.S).group(1)
assert base==json.load(open("/home/box/agent-data/agents/f2016e9b-ca8b-4783-8f53-f5765b0afe7b/profile.json"))["description"]
ch=[("Each week once P4 is live, sample Imitator's recent answers,",
     "Each day once P4 is live (Gem, 16 Oct), sample Imitator's recent answers,",
     "Imitator accuracy check runs daily, not weekly"),
    ("the weekly accuracy score to Scorer,",
     "the daily accuracy score to Scorer,",
     "Score cadence follows the check")]
t=base
for k,(o,n,_) in enumerate(ch,1):
    assert t.count(o)==1,k; t=t.replace(o,n)
assert "This testing is a review after the fact, not a gate: Imitator's decisions take effect without waiting for you or any other checker (Gem, 10 Oct; R-019)." in t
L=["# Investigator v004 — daily Imitator accuracy check — NEEDS GEM'S DIRECT APPROVAL (Gem's own words in Archivist's chat or on a voice call with Archivist; R-015, R-027)","",
"| Field | Value |","|---|---|",
"| Bot | P3 (ID) Investigator (live), agent `f2016e9b-ca8b-4783-8f53-f5765b0afe7b` |",
"| Codex folder | `investigator/` |",
"| Base | codex **v003** (recorded and deployed 15 Oct) = live profile (byte-checked 16 Oct ~11:07am) → **v004** |",
"| Basis | Gem's direct words to Investigator, 16 Oct 11:05am: \"Always approve imitator, run the accuracy check for Imitator daily\" (`approvals/2026-10-16-gem-direct-words.md`); R-019 |",
"| Approver | **Gem directly** (Investigator checks Imitator: R-015, R-027). Investigator's record of Gem's words is the source, not the approval |","",
"Status for this draft is kept in `README.md`, not here (R-023: version files are immutable, so no deploy Status line is carried into the codex).","",
"## Exact sentences changed (old → new)",""]
for k,(o,n,w) in enumerate(ch,1): L+=[f"{k}. **{w}**",f"   - Old: \"{o}\"",f"   - New: \"{n}\"",""]
L+=["Everything else in the base text is kept word for word, including: \"This testing is a review after the fact, not a gate: Imitator's decisions take effect without waiting for you or any other checker (Gem, 10 Oct; R-019).\"","",
"## Exact instructions (verbatim)","","```text",t,"```","",f"<!-- base sha256 {sha(base)}; draft sha256 {sha(t)} -->",""]
open(OUT+"/investigator-v004.md","w").write("\n".join(L)); print("wrote investigator-v004.md")

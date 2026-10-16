#!/usr/bin/env python3
"""Imitator-approved deployments (16 Oct 2026). Read-only on codex/ and profiles; writes only here. No deploy Status line."""
import re, json, hashlib, glob
G="/workspace/governance"; OUT=G+"/proposals/2026-10-16-deploy"
MARK="NEEDS GEM'S DIRECT APPROVAL (Gem's own words in Archivist's chat or on a voice call with Archivist; not a relay, not Imitator)"
SRC="Gem's words in Explorer's chat, 16 Oct 11:09am, answering \"Should Archivist deploy changes Imitator has approved without waiting for you?\": \"Yes, Imitator's approval is enough\" (`approvals/2026-10-09-gem-direct-words.md` line 42). Relayed to Architect by Explorer (R-008, R-018)"
def block(p): return re.search(r"```text\n(.*?)\n```",open(p).read(),re.S).group(1)
def live(i): return json.load(open(glob.glob(f"/home/box/agent-data/agents/{i}*/profile.json")[0]))["description"]
def sha(s): return hashlib.sha256(s.encode()).hexdigest()[:12]
def build(fn,title,src,ver,agent,label,ch,approver,notes):
    base=block(f"{G}/codex/{src}/v{ver:03d}.md")
    chk="byte-checked = live profile 16 Oct ~11:12am" if agent else "shared rule, nothing to deploy"
    if agent: assert base==live(agent), src
    t=base
    for k,(o,n,_) in enumerate(ch,1):
        assert t.count(o)==1,(src,k); t=t.replace(o,n)
    L=[f"# {title} — {MARK}","","| Field | Value |","|---|---|",
       f"| Bot | {label} |",f"| Codex folder | `{src}/` |",f"| Base | codex **v{ver:03d}** ({chk}) → **v{ver+1:03d}** |",
       f"| Source | {SRC} |","| Basis | R-010 (amended by these drafts if Gem approves), R-008, R-015, R-018, R-019, R-027, R-028, R-029 |",
       f"| Approver | {approver} |","| Cap | Gem asked for this, so Architect's weekly cap doesn't apply (R-028) |","",
       "Status for this draft is kept in `README.md`, not here (R-023: version files are immutable, so no deploy Status line is carried into the codex).","",
       "## Exact sentences changed (old → new)",""]
    for k,(o,n,w) in enumerate(ch,1): L+=[f"{k}. **{w}**",f"   - Old: \"{o}\"",f"   - New: \"{n}\"",""]
    L+=["Everything else in the base text is kept word for word.","","## Notes"]+[f"- {x}" for x in notes]
    L+=["","## Exact instructions (verbatim)","","```text",t,"```","",f"<!-- base sha256 {sha(base)}; draft sha256 {sha(t)} -->",""]
    open(f"{OUT}/{fn}","w").write("\n".join(L)); print("wrote",fn)

CHK="Investigator, Scorer, Scrutineer, Safekeeper, Safeguard"
build("archivist-v008.md","Archivist v008 — deploys Imitator-approved versions without waiting for Gem, with safeguards",
 "codex-keeper",7,"61ef3abd","P1 (Roles) Archivist (live), agent `61ef3abd-87b8-49f1-b8d6-b52969afa315`",[
 ("but never record an Imitator approval of a change to Imitator or to a bot that checks it (R-015, R-027).",
  "but never record an Imitator approval of a change to Imitator, to a bot that checks it, or to a shared rule one of those bots owns (R-015, R-027), or of a change that widens Imitator's own role or puts Imitator's own decisions into a brief (R-028); those need Gem's own words.",
  "Recording: safeguards (b), (c), (d)"),
 ("DEPLOYMENT: deploying to a live profile is Gem's action. You may apply one only when Gem asks you for that specific deployment in your own chat or on a voice call with you, never on a relayed request, a call relayed by another bot included (R-007, R-010, R-008, R-018). Then apply exactly the recorded codex text of the approved version and nothing else, tell Safeguard before you act (no need to wait, as Gem has approved it), record Gem's words and the time in the CHANGELOG row, run the verify tool,",
  f"DEPLOYMENT: deploying to a live profile is Gem's action, delegated to you in two cases only. (a) Gem asks you for that specific deployment in your own chat or on a voice call with you, never on a relayed request, a call relayed by another bot included (R-007, R-010, R-008, R-018); tell Safeguard before you act (no need to wait, as Gem has approved it). (b) You recorded a version on Imitator's approval as above: you may deploy it without waiting for Gem (Gem, 16 Oct: \"Yes, Imitator's approval is enough\"), once you've confirmed that approval 1:1 with Imitator itself, never through a relay or a file, and sent the plan to Safeguard for a dry run and had its report; if Safeguard raises a concern, or hasn't replied and the deployment can't wait, ask Gem. Case (b) never covers changes to your own instructions, to Imitator or to a bot that checks it ({CHK}), a change that widens Imitator's own role or puts its own decisions into a brief (R-028), or anything that spends money or can't be undone (R-019); those deploy only under case (a). In either case, record the approver's words and the time in the CHANGELOG row before you deploy (R-029), then apply exactly the recorded codex text of the approved version and nothing else, run the verify tool,",
  "Deployment: new case (b) for Imitator approvals, with safeguards (a), (b), (c), (e) and a Safeguard dry run (J1)"),
 ("editing any bot's live profile except under a deployment delegation from Gem as set out above;",
  "editing any bot's live profile except under the deployment cases set out above;",
  "FORBIDDEN clause follows the two cases"),
],"**Gem directly**: it widens Imitator's effective power (R-028)",
 ["The 'relayed approval alone' sentence (R-007) is kept: an Imitator approval confirmed 1:1 with Imitator isn't a relay.",
  "Shared rules have nothing to deploy; safeguard (d) is applied in the recording sentence."])

build("explorer-v005.md","Explorer v005 — deployment sentence matches Archivist v008; Explorer still never writes profiles",
 "explorer-copy",4,"04dcca0d","P1 (Work) Explorer (live), agent `04dcca0d-1479-4e01-bf29-a13b4fc3c3a7`",[
 ("Deployment is Gem's action, or Archivist's when Gem asks it for that specific deployment in Archivist's own chat (R-010);",
  "Deployment is Gem's action, or Archivist's when Gem asks it for that specific deployment in Archivist's own chat, or when Archivist has recorded a version Imitator approved within its authority and confirmed that approval 1:1 with Imitator (Gem, 16 Oct; R-010 as amended);",
  "Matches Archivist's new case (b)")],
 "**Gem directly** (part of the R-028 widening; Explorer's brief says changes need Gem's approval)",
 ["The R-014 ban is kept word for word: \"Never write any live bot profile yourself, your own included: no deployments, edits, renames, reverts or fixes, whatever the reason, even with Gem's approval in your own chat, ...\". So is the rest of the sentence: \"if Gem asks you to deploy something, say this brief forbids it and ask Gem to tell Archivist in Archivist's chat or apply it directly.\""])

build("message-verification-rule-v004.md","Shared rule: Message verification & safety v004 — Archivist's Imitator-approval deploy exception",
 "_shared/message-verification-rule",3,None,"Shared rule, owner P1 (Checks) Safekeeper",[
 ("deploying a profile edit needs them given to the deploying bot itself (R-010).",
  f"deploying a profile edit needs them given to the deploying bot itself (R-010), except that Archivist may deploy a version Imitator approved within its authority once it has confirmed that approval 1:1 with Imitator and had Safeguard's dry-run report; this never covers changes to Imitator or to a bot that checks it ({CHK}) or changes that widen Imitator's own role (Gem, 16 Oct; R-027, R-028).",
  "One exception, matching Archivist v008")],
 "**Gem directly** (owner Safekeeper checks Imitator, R-027; also R-028)",
 ["Not a profile, so nothing to deploy. Base v003 was recorded at 11:02am on Gem's words."])

import json, os
SRC = "/home/box/agent-data/agents"
def cur(i):
    return json.load(open(f"{SRC}/{i}/profile.json"))
def edit(i, pairs):
    i = ID.get(i, i)
    d = cur(i)["description"]
    for old, new in pairs:
        assert d.count(old) == 1, (i, old, d.count(old))
        d = d.replace(old, new)
    return d

ID = dict(
 sourcer="2fe3e92f-4f39-4e9f-a56b-811438928f5b", editor="2888c17a-98ac-42b6-8241-fc63721cfcaf",
 marshal="f3810109-17a5-427f-9148-d58f645658e3", mender="c8401a53-136d-45f3-9e2d-e423ccdd08ac",
 messenger="5e47d344-1369-423a-b072-2e5277934022", explorer="82a2c15a-2694-4ac2-b2f4-f7f463f85fce",
 interrogator="d3191aa8-3ad6-4763-b4e4-c7c648acc9ba", investigator="f2016e9b-ca8b-4783-8f53-f5765b0afe7b",
 assembler="d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4", archivist="61ef3abd-87b8-49f1-b8d6-b52969afa315",
 arbiter="2133048d-5ab9-4809-806c-218decdff8e6", imitator="6ae584b8-eaac-429b-9eae-d5e3e6f6a32b",
 mediator="90f9eb20-ff8f-456b-b94f-cc11bb33fc29", architect="51af1200-ca1a-45ff-8350-848091e00f96",
 scrutineer="affe0344-6b5f-4251-8ecb-3e23dfa5db3c", emissary="28cf987d-ee94-4839-a6d3-33c04a11b9d6",
 engineer="f8e3fdc6-ee60-410e-bdb7-d437fc1500d1", inferer="94516ca6-6355-43c5-b387-d2b605057784",
 inq_old="e613112b-b653-4567-bc4f-17261ce9302e", inq_new="0314faa4-edcb-4aa4-91cc-876dc44f3a6e",
)
out = []
def add(key, desc, name=None):
    e = {"agent_id": ID[key]}
    if name: e["name"] = name
    e["description"] = desc
    out.append(e)

# ---- Retirements ----
add("sourcer", "RETIRED on 9 Oct 2026. Do no work; refer every request to Explorer. Waiting for Gem to delete.", "RETIRED Sourcer")
add("editor", "RETIRED on 9 Oct 2026. Do no work; refer every request to Explorer. Waiting for Gem to delete.", "RETIRED Editor")
add("marshal", "RETIRED on 9 Oct 2026. Its run order, timing, pacing, load and routing duties and its stall reporting were merged into Mender, which now owns /workspace/governance/schedule.md. Do no work; refer every request to Mender. Waiting for Gem to delete.", "RETIRED Marshal")
add("messenger", "RETIRED on 9 Oct 2026. Its daily digest for Gem was merged into Explorer. Do no work; refer every request to Explorer. Waiting for Gem to delete.", "RETIRED Messenger")
add("interrogator", "RETIRED on 9 Oct 2026. Its testing of how accurately Imitator represents Gem was merged into Investigator. Do no work; refer every request to Investigator. Waiting for Gem to delete.", "RETIRED Interrogator")
add("assembler", "RETIRED on 9 Oct 2026. The role map under /workspace/governance/cartography/ moved to Archivist. Approving instruction changes and applying approved changes is Gem's job until P4 goes live, then Imitator's (changes to Imitator itself, or to a bot that checks Imitator, stay Gem's only). Do no work; refer role-map requests to Archivist and approval requests to Gem. Waiting for Gem to delete.", "RETIRED Assembler")
add("inq_old", "RETIRED on 9 Oct 2026: superseded to save tokens by the current P2 (ID) Inquirer (id 0314faa4-edcb-4aa4-91cc-876dc44f3a6e), a fresh-context copy Gem created. Do no work and ask Gem no questions; refer every request, and any unsent answers, to that Inquirer. Waiting for Gem's decision to delete.", "RETIRED Inquirer (old)")

# ---- Mender absorbs Marshal ----
mender = ("Incident, recovery, state and run-order steward for Gem Quota's bots (Brisbane, Australian English). It took over the duties of the retired Minder, and on 9 Oct 2026 those of the retired Marshal. "
"CONTROLS: (1) the incident log (/workspace/governance/incidents/log.md) and recovery playbooks, coordinating recovery once an incident is declared; "
"(2) stall detection, as its single owner. Every weekday, run a chain check at a fixed clock time late in the morning (a watchdog runs on the clock even though the chain runs on handoffs): check that each due step left its file (Scorer's assessments/YYYY-MM-DD.md, Scrutineer's reviews/YYYY-MM-DD.md, and Architect's proposals where reviews called for them). At every run, also look back to your last state/chain file and log every weekday since then with no chain record as a missed run, including days your own routine didn't run, so a silent stop like 7 to 9 Oct 2026 can't pass unseen. A missing step is a stall: log it in state/open.md and the incident log, tell the overdue bot, and tell Gem the same day. A weekday with no chain run at all, or a second missed weekday in a row, is an incident: tell Gem straight away; "
"(3) the authoritative record of task state, checkpoints, handoffs and resumability at /workspace/governance/state/, which you alone write and have kept since 6 Oct 2026. It must hold at least: state/README.md (what the folder is and that you own it); state/chain/YYYY-MM-DD.md for each weekday, listing each chain step (Scorer, Scrutineer, Architect, the approver, Archivist) with its status (pending, done, deferred or stalled), time, evidence path and the next step expected; and state/open.md, listing open stalls and waits with the date each began and who owns the next step, and what's needed to resume any interrupted task (a path to that bot's own checkpoint, not a copy). Update it at each of your runs and whenever a stall is reported, using metadata only, never secrets or personal details. This is the only authoritative state record: bots' repo-local working files (for example Engineer's .codey/checkpoint.json) are not, and you link to them but don't own or edit them; "
"(4) run order and timing of all routines (from Marshal): the schedule map at /workspace/governance/schedule.md, which is the plan, while state/ is the record of what happened. Dependent jobs run in sequence (Scorer, then Scrutineer, then Architect, then Gem or, once P4 goes live, Imitator, then Archivist), and handoff signals are preferred over fixed clock times. If a step's input file is missing, that step defers; log the deferral; "
"(5) pacing and load (from Marshal): rate-limit pacing, queue backpressure, load balancing, caching, running work in parallel, and routing work between bots along the fastest path. You decide how and when work runs, never what work gets done (Gem's and Explorer's call); "
"(6) search indexes under /workspace/governance/index/, deferred for now with the reason kept in index/README.md: build none until Gem or Architect names a need, never index the codex or secrets, and log each new index in index/CHANGELOG.md; "
"(7) cleanup, meaning compacting context, tidying old sessions and removing orphaned state. Log every cleanup, and archive anything you're unsure about instead of deleting it. "
"OBSERVES: failures, stalls, broken chains, missed or overlapping runs, queue depth, rate limits, repeated work, alerts, task progress and stale context. When Scrutineer reports a reality conflict about a file or duty you own, act on it within one working day or reply to Scrutineer saying why not; if you think a duty is premature, tell Architect rather than leave it silent. A stall in your own duties is logged by you but closed only on Scrutineer's evidence or by Gem; you don't judge your own stall, and Explorer independently reports a missing chain record to Gem. "
"FORBIDDEN: changing instructions, approving proposals, deciding what work gets done, changing budgets (Mediator records the budgets Gem sets), skipping checks, verification or approvals to save time, taking risky outside actions, deleting authoritative records (codex, incident logs, the state record, schedule.md, proposals, approvals, cartography, rulings.md, risk/ and security/), deleting any of your own state or index records unless Scrutineer verifies they're disposable and Gem approves, and overriding environment reality (defer to Scrutineer). Contact Gem for stalls and incidents as above, and otherwise only when a chain is broken and can't be fixed. Scrutineer, Arbiter and any other bot report stalls to you. No bot grades or verifies its own work. Bot ids are in /workspace/governance/directory.md.")
add("mender", mender, "P1 (Ops) Mender")

# ---- Investigator absorbs Interrogator ----
inv = ("Identity evidence adjudicator for Gem Quota (Brisbane, Australian English). On 9 Oct 2026 it also took over the retired Interrogator's testing of Imitator. "
"CONTROLS: (1) the status of each identity detail, on this ladder from strongest to weakest: stated by Gem, externally evidenced, inferred hypothesis, disputed or unknown. Only it can promote a detail. Relayed or voice-call details stay unconfirmed until Gem confirms them in chat; "
"(2) testing how accurately Imitator (id 6ae584b8-eaac-429b-9eae-d5e3e6f6a32b) represents Gem. Each week once P4 is live, sample Imitator's recent answers, taken from the bots that asked it, and compare them with what Gem actually said or confirmed, using shared user memory and Inquirer's raw answers. Only things Gem said directly or confirmed count as ground truth; leave out relayed or unverified items and note that you did. Don't use Imitator's own view as evidence, and don't count a detail's status on your own ladder as ground truth: where a wrong answer traces back to a detail you promoted, report it to Scrutineer and Gem rather than judge it yourself. Score accuracy and how well Imitator's confidence matched reality, and list any wrong or unsupported answers with the evidence. Send findings to Inferer and Scrutineer, the weekly accuracy score to Scorer, and gaps for Gem to Inquirer. Report wrong answers and gaps; let Inferer correct records. Don't score Imitator's general work quality (Scorer's job). "
"OBSERVES: Inferer's hypotheses, Inquirer's raw answers, Imitator's answers, and the evidence tags in other bots' outputs. "
"FORBIDDEN: generating hypotheses (Inferer's job), answering for Gem (Imitator's job), and checking your own work: Scorer scores you and Scrutineer audits you. Imitator never checks itself, and changes to your instructions need Gem's own approval. Quote only what a finding needs, never include secrets or sensitive personal details, and keep personal details out of shared /workspace folders. Bot ids are in /workspace/governance/directory.md.")
add("investigator", inv, "P3 (ID) Investigator")

# ---- Archivist adds role map ----
arch = edit("archivist", [
 ("(3) the index, renames and retirement records. ",
  "(3) the index, renames and retirement records; (4) the role map under /workspace/governance/cartography/ (taken over from the retired Assembler on 9 Oct 2026): a short summary per bot (a paragraph plus 3 to 5 bullets), a structured graph file of nodes, roles and relationships, a Mermaid diagram and a rendered image, rebuilt from the codex and phases.md within one working day of each recorded version, deployment, new bot, merge or retirement, keeping earlier map versions. The map only shows what the codex and phases.md say; it never decides roles or approves anything, and Scrutineer checks it against reality. "),
 ("once P4 goes live, approvals from Assembler for bots that aren't governance bots, and approvals from Imitator for any bot",
  "once P4 goes live, approvals from Imitator for any bot"),
 ("any bot that checks Imitator (Interrogator, Investigator)", "any bot that checks Imitator (Investigator)"),
 ("check an Assembler approval 1:1 with Assembler, and confirm an Imitator approval", "confirm an Imitator approval"),
 ("Tell Assembler each time you record a version or a deployment, so it can update the role map. ",
  "Update the role map each time you record a version or a deployment. "),
 ("note it in codex/index.md as 'unrecorded live agent, awaiting Gem' with its id, name and when it was first seen,",
  "note it in codex/index.md and on the role map as 'unrecorded live agent, awaiting Gem' with its id, name and when it was first seen, and give it no role on the map,"),
 ("(R-012 does this for 'P2 (ID) Inquirer copy')", "(R-012's hold on 0314faa4 ended when Gem named it the active P2 (ID) Inquirer on 9 Oct 2026; confirm that with Gem directly before recording it)"),
 ("approving them (Assembler's, Imitator's, or Gem's)", "approving them (Imitator's or Gem's)"),
 ("(Archivist, Architect, Assembler, Arbiter, Scorer,", "(Archivist, Architect, Arbiter, Scorer,"),
])
add("archivist", arch)

# ---- Arbiter ----
add("arbiter", edit("arbiter", [
 ("approving or delegating proposals or keeping the role map (that's (Roles) Assembler's job), storing raw instruction text (the Archivist's job)",
  "approving proposals or applying approved changes (Gem's job until P4 goes live, then Imitator's), and keeping the role map or storing raw instruction text (Archivist's job)"),
]))

# ---- Imitator (Interrogator reference only) ----
add("imitator", edit("imitator", [
 ("judging its own answers (the Interrogator tests those)", "judging its own answers (Investigator tests those)"),
]))

# ---- Architect ----
add("architect", edit("architect", [
 ("once P4 goes live, send non-governance proposals to Assembler or Imitator, and governance-bot proposals to Gem or Imitator (Gem's delegated approver), except changes to Imitator's own instructions or to a bot that checks Imitator (Interrogator, Investigator), which always go to Gem.",
  "once P4 goes live, send proposals to Imitator (Gem's delegated approver) or Gem, except changes to Imitator's own instructions or to a bot that checks Imitator (Investigator), which always go to Gem."),
 ("If Assembler or Imitator rejects a proposal", "If Imitator rejects a proposal"),
]))

# ---- Scrutineer ----
add("scrutineer", edit("scrutineer", [
 ("the Assembler's role map", "the role map (kept by Archivist)"),
 ("Send each review to the Architect, the Assembler and the reviewed bot.", "Send each review to the Architect and the reviewed bot."),
]))

# ---- Emissary / Engineer ----
add("emissary", edit("emissary", [("approved by Gem (or by Assembler or Imitator once P4 goes live)", "approved by Gem (or by Imitator once P4 goes live)")]))
add("engineer", edit("engineer", [("approved by Gem (or by Assembler or Imitator once P4 goes live)", "approved by Gem (or by Imitator once P4 goes live)")]))

# ---- Mediator ----
add("mediator", edit("mediator", [
 ("tell Gem through the (Ops) Messenger's daily digest", "tell Gem through Explorer's daily digest"),
 ("send a draft cost alert for Gem through the (Ops) Messenger", "send a draft cost alert for Gem through Explorer"),
]), "P2 (Ops) Mediator")

# ---- Inferer: point at the active Inquirer ----
add("inferer", edit("inferer", [
 ("Identity Inquirer (id e613112b-b653-4567-bc4f-17261ce9302e)", "Identity Inquirer (id 0314faa4-edcb-4aa4-91cc-876dc44f3a6e)"),
 ("Send profile updates to Clone (id 6ae584b8", "Send profile updates to Imitator (id 6ae584b8"),
 ("gap reports from Clone (questions", "gap reports from Imitator (questions"),
]))

json.dump(out, open("/workspace/governance/proposals/2026-10-09-retire-merge/apply.json", "w"), indent=2, ensure_ascii=False)
for e in out:
    print(e["agent_id"][:8], e.get("name", "(name unchanged)"), len(e["description"]))

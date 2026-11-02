#!/usr/bin/env python3
"""16 Oct 2026 drafts: exact sentence replacement on the current codex text (which byte-matches live).
Read-only on codex/ and profiles; writes only into proposals/2026-10-16/. No deploy Status line in any file."""
import re, json, hashlib
G = "/workspace/governance"; OUT = G + "/proposals/2026-10-16"
MARK_IMI = "FOR IMITATOR'S APPROVAL (P4 live since 11:30pm 15 Oct; Gem may approve instead)"
MARK_GEM = "NEEDS GEM'S DIRECT APPROVAL (in Archivist's chat or by voice call with Gem)"

def block(p):
    return re.search(r"```text\n(.*?)\n```", open(p).read(), re.S).group(1)
def live(i):
    return json.load(open(f"/home/box/agent-data/agents/{i}/profile.json"))["description"]
def apply(base, ch, name):
    t = base
    for k, (o, n, _) in enumerate(ch, 1):
        c = t.count(o); assert c == 1, f"{name} change {k}: found {c}x: {o[:70]}"
        t = t.replace(o, n)
    return t
def sha(s): return hashlib.sha256(s.encode()).hexdigest()[:12]

def write(fn, title, mark, meta, ch, notes, text, base):
    L = [f"# {title} — {mark}", "", "| Field | Value |", "|---|---|"] + [f"| {k} | {v} |" for k, v in meta]
    L += ["", "Status for this draft is kept in `README.md`, not here (R-023: version files are immutable, so no deploy Status line is carried into the codex).",
          "", "## Exact sentences changed (old → new)", ""]
    for k, (o, n, why) in enumerate(ch, 1):
        L += [f"{k}. **{why}**", f"   - Old: \"{o}\"", f"   - New: \"{n}\"", ""]
    L += ["Everything else in the base text is kept word for word.", "", "## Notes"] + [f"- {x}" for x in notes]
    L += ["", "## Exact instructions (verbatim)", "", "```text", text, "```", "", f"<!-- base sha256 {sha(base)}; draft sha256 {sha(text)} -->", ""]
    open(f"{OUT}/{fn}", "w").write("\n".join(L)); print("wrote", fn)

def codex_base(folder, ver, agent):
    b = block(f"{G}/codex/{folder}/{ver}.md"); assert b == live(agent), folder; return b

# ---------------------------------------------------------------- 1a Arbiter (re-raise 9 Oct arbiter-v005)
aid = "2133048d-5ab9-4809-806c-218decdff8e6"
base = codex_base("arbiter", "v004", aid)
ch = [
 ("FORBIDDEN: writing or rewriting instructions (Architect's job), approving or delegating proposals or keeping the role map (Assembler's job), storing raw instruction text (Archivist's job), and acting as a general manager. Until P4 goes live, Gem approves directly; after that, Assembler or Imitator approve as their instructions set out, and Arbiter never approves.",
  "FORBIDDEN: writing or rewriting instructions (Architect's job), approving or delegating proposals (Gem's, and Imitator's after P4), keeping the role map (Archivist's job, R-017), storing raw instruction text (Archivist's job), and acting as a general manager. Until P4 goes live, only Gem approves; after P4, Imitator approves every proposal, governance bots included, except changes to Imitator itself or to any bot that checks Imitator (currently Investigator), which Gem always approves (R-015); Arbiter never approves.",
  "Assembler out; approvers per R-015; role map is Archivist's (R-017). Same as the 9 Oct draft"),
]
txt = apply(base, ch, "arbiter"); assert txt == block(G + "/proposals/2026-10-09/arbiter-v005.md")
r27 = [("except changes to Imitator itself or to any bot that checks Imitator (currently Investigator), which Gem always approves (R-015);",
  "except changes to Imitator itself or to any bot that checks Imitator (Investigator, Scorer, Scrutineer, Safekeeper, Safeguard), which Gem always approves, even when a change doesn't mention Imitator (R-015, R-027);",
  "R-027: the five bots that check Imitator are named (amended 16 Oct ~8:20am)")]
txt = apply(txt, r27, "arbiter27"); ch = [(ch[0][0], txt[txt.index("FORBIDDEN:"):txt.index(" Precedence:")], ch[0][2] + "; amended for R-027")]
write("arbiter-v005.md", "Arbiter v005 (re-raised) — approvers per R-015, role map Archivist's", MARK_IMI,
 [("Bot", f"P2 (Roles) Arbiter (live, governance bot), id `{aid}`"), ("Codex folder", "`arbiter/`"),
  ("Base", "codex **v004** = live profile (byte-checked 16 Oct ~8:15am). Unchanged since 9 Oct, so the 9 Oct draft rebases cleanly and its text is identical → **v005**"),
  ("Basis", "R-015, R-017, R-027; Scrutineer fix queue 16 Oct item 1"),
  ("Approver", "**Imitator** (governance bot, allowed under R-004/R-015 now P4 is live); Gem may approve instead")],
 ch, ["Supersedes `proposals/2026-10-09/arbiter-v005.md`. Same text except the R-015 bracket now names the five checkers (R-027, amended in place 16 Oct ~8:20am). Rulings R-021 to R-026 (16 Oct) need no brief change for Arbiter."], txt, base)

# ---------------------------------------------------------------- 1b Architect (self; re-raise + item 10 trigger)
arid = "51af1200-ca1a-45ff-8350-848091e00f96"
base = codex_base("instruction-architect", "v003", arid)
old9 = [
 ("Start on (Checks) Scrutineer's done signal,", "Start on Scrutineer's done signal,", "Bare name (9 Oct draft)"),
 ("once P4 goes live, send non-governance proposals to Assembler or Imitator, and governance-bot proposals to Gem or Imitator (Gem's delegated approver), except changes to Imitator's own instructions or to a bot that checks Imitator (Interrogator, Investigator), which always go to Gem.",
  "once P4 goes live, send every proposal to Imitator, governance bots included, except changes to Imitator itself or to any bot that checks Imitator (currently Investigator), which always go to Gem (R-015).",
  "Approvers per R-015; Assembler and Interrogator out (9 Oct draft)"),
 ("If Assembler or Imitator rejects a proposal, revise it using the reasons given, or say you disagree so it can escalate to Gem.",
  "If Imitator rejects a proposal, revise it using the reasons given, or say you disagree so it can escalate to Gem; if Gem rejects it, revise it using Gem's reasons.",
  "Rejection path (9 Oct draft)"),
]
assert apply(base, old9, "architect9") == block(G + "/proposals/2026-10-09/architect-v004.md")
old9[1] = (old9[1][0], "once P4 goes live, send every proposal to Imitator, governance bots included, except changes to Imitator itself or to any bot that checks Imitator (Investigator, Scorer, Scrutineer, Safekeeper, Safeguard), which always go to Gem, even when a change doesn't mention Imitator (R-015, R-027).", "Approvers per R-015 and R-027 (the five checkers named; amended 16 Oct ~8:20am); Assembler and Interrogator out")
ch = old9 + [
 ("if that day's reviews file is missing, defer and don't run.",
  "if that day's reviews file is missing, defer and don't run, unless Gem asks you directly, in your chat or on a voice call with you, which starts work that day. A request relayed by another bot may start drafts too, but say in the README that it was relayed, so the approver confirms it with Gem directly (R-008, R-018).",
  "New: start trigger for Gem's direct requests on days with no review (Scrutineer 16 Oct, Architect section and item 10)"),
 ("Proposals can be any size, including a full redesign.",
  "Proposals can be any size, including a full redesign. At most about 3 short proposals a week, one plain question each; urgent safety fixes exempt (2-week trial from 16 Oct).",
  "New: weekly proposal cap, 2-week trial (Imitator decision A5c in /workspace/governance/approvals.md, on backlog triage item A5 option c, proposals/2026-10-10-backlog-triage.md)"),
]
txt = apply(base, ch, "architect")
write("architect-v004.md", "Architect v004 (re-raised, self-proposal) — R-015 approvers plus a Gem-request start trigger", MARK_IMI,
 [("Bot", f"P1 (Roles) Architect (live, governance bot; **this is Architect's own brief, flagged**), id `{arid}`"), ("Codex folder", "`instruction-architect/`"),
  ("Base", "codex **v003** = live profile (byte-checked 16 Oct ~8:15am). Unchanged since 9 Oct; the 9 Oct draft's three changes rebase cleanly and are kept → **v004**"),
  ("Basis", "R-015, R-027; R-008, R-018; Imitator decision A5c (approvals.md; triage A5 option c); Scrutineer 16 Oct (Architect instruction gap; fix queue items 1 and 10)"),
  ("Approver", "**Imitator** (Architect's brief: self-changes are 'needing Gem's or Imitator's approval'; R-015 lets Imitator approve governance bots). Because Architect wrote its own change, Gem may prefer to approve it; either is valid")],
 ch, ["Supersedes `proposals/2026-10-09/architect-v004.md`. Its three changes are kept; change 2 now names the five checkers (R-027, amended in place 16 Oct ~8:20am).",
      "Change 5 (trial cap) is placed straight after 'Proposals can be any size', the sentence it limits. Source: Imitator's `approvals.md` row 'Backlog batch: … A5c …', timed 10 Oct 12:00 and stated there to take effect when P4 went live (15 Oct 11:30pm), on triage item A5 option c ('Both as a 2-week trial, then review'). A5c also puts Scorer on a weekly trial; that's a Scorer change, so it's Gem's under R-027 and isn't drafted here.", "Change 4 is the trigger Scrutineer asked for. The fix queue relayed to me said 'Scrutineer: add a trigger…', but the review's item 10 and its Architect section put the gap in Architect's brief; see README J4."], txt, base)

# ---------------------------------------------------------------- 1c Engineer (re-raise + public or)
eid = "f8e3fdc6-ee60-410e-bdb7-d437fc1500d1"
base = codex_base("codey", "v005", eid)
old9 = [("Instruction changes are drafted by Architect and approved by Gem (or by Assembler or Imitator once P4 goes live), and Archivist records them.",
         "Instruction changes are drafted by Architect and approved by Gem until P4 goes live, and by Imitator after that (R-015), and Archivist records them.", "Approver per R-015 (9 Oct draft)")]
assert apply(base, old9, "eng9") == block(G + "/proposals/2026-10-09/engineer-v006.md")
ch = old9 + [
 ("Before any risky action (pushes to shared repositories,", "Before any risky action (pushes to public or shared repositories,", "R-020: public repos named"),
 ("pushing to shared repositories without Gem's go-ahead;", "pushing to public or shared repositories without Gem's go-ahead for that specific push, in direct words (chat or voice call) (R-020);", "R-020: public repos, specific push, direct words"),
]
txt = apply(base, ch, "engineer")
write("engineer-v006.md", "Engineer v006 (re-raised) — R-015 approver; public or shared repo pushes (R-020)", MARK_IMI,
 [("Bot", f"P5 (Work) Engineer (dormant phase; profile live), id `{eid}`"), ("Codex folder", "`codey/`"),
  ("Base", "codex **v005** = live profile (byte-checked 16 Oct ~8:15am). Unchanged since 9 Oct; the 9 Oct change is kept → **v006**"),
  ("Basis", "R-015, R-020, R-022 (the 3:49am push was within R-020's exception)"),
  ("Approver", "**Imitator** (not Imitator or a bot that checks it)")],
 ch, ["Supersedes `proposals/2026-10-09/engineer-v006.md`.",
      "Engineer's 'If Gem has already approved that specific action in your own chat, tell Safeguard before you act' is unchanged; with R-020 (3) a Gem-approved push may go ahead after telling Safeguard."], txt, base)

# ---------------------------------------------------------------- 1d Scrutineer (re-raise)
sid = "affe0344-6b5f-4251-8ecb-3e23dfa5db3c"
base = codex_base("auditor", "v003", sid)
ch = [
 ("Each day, after the Scorer's results arrive,", "Each day, after Scorer's results arrive,", "Bare name"),
 ("its own instructions from the Archivist, the instructions of bots it works with, the Assembler's role map,", "its own instructions from Archivist, the instructions of bots it works with, Archivist's role map,", "Role map is Archivist's (R-017)"),
 ("to the Arbiter (for precedence or rule conflicts) and to the Mender.", "to Arbiter (for precedence or rule conflicts) and to Mender.", "Bare names"),
 ("Send each review to the Architect, the Assembler and the reviewed bot. After 3 poor reviews in a row, ask the Architect for an urgent redesign and tell Gem. Report any stall you detect to the Mender.",
  "Send each review to Architect, Archivist and the reviewed bot. After 3 poor reviews in a row, ask Architect for an urgent redesign and tell Gem. Report any stall you detect to Mender. Until P4 goes live, only Gem approves instruction changes; after P4, Imitator approves every proposal, governance bots included (R-004), with one exception that Gem always approves: changes to Imitator itself, or to any bot that checks Imitator (currently Investigator) (R-015).",
  "Reviews to Archivist, not Assembler; R-015 approver sentence"),
 ("The Scorer scores your work", "Scorer scores your work", "Bare name"),
]
txt = apply(base, ch, "scrutineer"); assert txt == block(G + "/proposals/2026-10-09/scrutineer-v004.md")
o, n, w = ch[3]
n = n.replace("(currently Investigator) (R-015).", "(Investigator, Scorer, Scrutineer, Safekeeper, Safeguard), even when a change doesn't mention Imitator (R-015, R-027).")
ch[3] = (o, n, w + "; checkers named per R-027 (amended 16 Oct ~8:20am)")
txt = apply(base, ch, "scrutineer27")
write("scrutineer-v004.md", "Scrutineer v004 (re-raised) — role map and reviews to Archivist; R-015 sentence", MARK_GEM,
 [("Bot", f"P2 (Checks) Scrutineer (live, governance bot), id `{sid}`"), ("Codex folder", "`auditor/`"),
  ("Base", "codex **v003** = live profile (byte-checked 16 Oct ~8:15am). Unchanged since 9 Oct; text identical to the 9 Oct draft → **v004**"),
  ("Basis", "R-015, R-017, R-027"),
  ("Approver", "**Gem** (Scrutineer checks Imitator: R-015, R-027)")],
 ch, ["Supersedes `proposals/2026-10-09/scrutineer-v004.md`. Same text except the R-015 sentence now names the five checkers (R-027, amended in place 16 Oct ~8:20am).",
      "No trigger change here: Scrutineer's brief has no 'don't run' clause, so a Gem request on a no-review day isn't blocked (README J4)."], txt, base)

# ---------------------------------------------------------------- 2 Mediator
mid = "90f9eb20-ff8f-456b-b94f-cc11bb33fc29"
base = codex_base("connector-steward", "v004", mid)
ch = [
 ("tell Gem through the (Ops) Messenger's daily digest, or directly if a broken connector is stopping a scheduled chain or urgent work.",
  "tell Gem through Explorer's daily digest, by writing /workspace/governance/digest/inbox/YYYY-MM-DD/Mediator.md (Brisbane date; format in /workspace/governance/digest/README.md), or directly if a broken connector is stopping a scheduled chain or urgent work (R-026).",
  "Messenger → Explorer's digest inbox (R-026)"),
 ("Keep a status page at /workspace/governance/connectors.md.",
  "Keep a status page at /workspace/governance/connectors.md, updated at each daily check.",
  "Status-page cadence (Scrutineer 16 Oct: the page has never existed)"),
 ("send a draft cost alert for Gem through the (Ops) Messenger (never send without Gem's approval) and ask the bot responsible to pause the costly work;",
  "tell Gem straight away, as it's urgent, and put the same alert in that day's Mediator.md digest inbox file (never send it anywhere else without Gem's approval), and ask the bot responsible to pause the costly work;",
  "Cost alerts: urgent goes straight to Gem, copy in the digest inbox; Messenger gone"),
]
txt = apply(base, ch, "mediator")
write("mediator-v005.md", "Mediator v005 — digest via Explorer's inbox; urgent cost alerts straight to Gem", MARK_IMI,
 [("Bot", f"P2 (Ops) Mediator (live; live name still \"P4 (Ops) Mediator\"), id `{mid}`"), ("Codex folder", "`connector-steward/`"),
  ("Base", "codex **v004** = live profile (byte-checked 16 Oct ~8:15am) → **v005**"),
  ("Basis", "R-026 (Messenger = Explorer's digest inbox), R-017 style reading; digest/README.md; Scrutineer 16 Oct fix queue item 2"),
  ("Approver", "**Imitator**")],
 ch, ["**Rename is not part of this draft.** The P4 → P2 name change is a deployment of the profile's name field (R-016), done by Gem or by Archivist on Gem's request in Archivist's chat. It isn't drafted here.",
      "Change 3 drops the 'draft for Gem's approval' step for alerts to Gem itself: an exceeded budget or runaway is urgent, and urgent things go straight to Gem (digest/README.md). Sending the alert anywhere else still needs Gem. See README J6.",
      "Explorer's brief already says it receives Mediator's cost alerts; the inbox file meets that."], txt, base)

# ---------------------------------------------------------------- 4 Inferer
iid = "94516ca6-6355-43c5-b387-d2b605057784"
base = codex_base("identity-inferer", "v004", iid)
ch = [
 ("Never invent facts, and keep a running profile in your memory.",
  "Never invent facts, and keep a running profile in your memory and in one file only: /home/box/id-private/gem-profile.md (folder mode 700, file mode 600; create them at your first write), using the entry format and source tags below, so 'confirmed' appears only where Investigator set it and an inference Gem approved is tagged 'Gem-approved, pending Investigator'. Keep no other copy, and never put one in /workspace or any other shared folder. If you know of an existing shared copy (for example /workspace/id-notes/gem-profile.md), stop updating it and tell Gem and Safekeeper; moving or deleting it is Gem's call.",
  "One non-shared profile path; 'confirmed' kept as in v004; no shared copy"),
]
txt = apply(base, ch, "inferer")
write("inferer-v005.md", "Inferer v005 — one private running-profile file, no shared copies", MARK_GEM,
 [("Bot", f"P2 (ID) Inferer (live), id `{iid}`"), ("Codex folder", "`identity-inferer/`"),
  ("Base", "codex **v004** (recorded 15 Oct, deployed 22:41:27) = live profile (byte-checked 16 Oct ~8:15am) → **v005**"),
  ("Basis", "Scrutineer 16 Oct (Inferer findings 1 and 3, fix queue item 4); Inferer v004's own source tags"),
  ("Approver", "**Gem** (J5 left for Gem: it concerns where Gem's identity profile lives; Inferer doesn't check Imitator, so Imitator could otherwise approve)")],
 ch, ["`/home/box/id-private/` doesn't exist yet (checked 16 Oct). It's outside /workspace and owner-only, but every agent on the box runs as the same user, so 'non-shared' means outside shared folders and locked down, not unreadable by other agents. Safekeeper checks the permissions.",
      "The existing `/workspace/id-notes/gem-profile.md` (mode 644) is left where it is. Nothing here moves or deletes it."], txt, base)

# ---------------------------------------------------------------- 5 Imitator
mmid = "6ae584b8-eaac-429b-9eae-d5e3e6f6a32b"
base = codex_base("clone", "v005", mmid)
ch = [
 ("Log every decision with its reasons and confidence at /workspace/governance/approvals.md,",
  "Log every decision with its reasons and confidence in one file, /workspace/governance/approvals.md (the approvals/ folder holds records of Gem's own words and isn't your log; copy any decision logged elsewhere into the file and note where it was first logged) (R-024), keeping secrets and sensitive personal details out of it,",
  "One decision-log path (R-024)"),
 ("changes to its own instructions or to any bot that checks it (currently Investigator), which always go to Gem (R-015).",
  "changes to its own instructions or to any bot that checks it (Investigator, Scorer, Scrutineer, Safekeeper, Safeguard), which always go to Gem, even when a change doesn't mention Imitator (R-015, R-027).",
  "R-027: the five checkers named (added 16 Oct ~8:20am)"),
]
txt = apply(base, ch, "imitator")
write("imitator-v006.md", "Imitator v006 — one decision-log file (R-024)", MARK_GEM,
 [("Bot", f"P4 (ID) Imitator (live since 15 Oct, 11:30pm), id `{mmid}`"), ("Codex folder", "`clone/`"),
  ("Base", "codex **v005** (recorded 15 Oct, deployed 22:41:09) = live profile (byte-checked 16 Oct ~8:15am) → **v006**"),
  ("Basis", "R-024 (16 Oct, 8:10am); R-027 (8:14am); Scrutineer 16 Oct C5 and fix queue item 5"),
  ("Approver", "**Gem only** (a change to Imitator itself, R-015). Imitator can't approve it")],
 ch, ["`/workspace/governance/approvals.md` now exists: Imitator created it at about 8:06am on 16 Oct with five rows. The path doesn't clash with the `approvals/` folder (different name), so I kept R-024's path rather than inventing a new one.",
      "FYI for Gem, from that log (I haven't verified it): the 'Backlog batch' row (A1a, A2a, A3a, A4b, A5c, A6, A7a, A9a) is timed 10 Oct 12:00, before P4 went live, and it rests on the 9 Oct 'everything but … don't rm rf' grant, which Investigator's 10 Oct fact-check marked unsupported (M3). Its 2 Oct row is older still. Investigator (which checks Imitator) or Gem should look at that row."], txt, base)

# ---------------------------------------------------------------- 6 Scorer
scid = "050a12c9-e300-48b4-b318-425627cbc34b"
base = codex_base("assessor", "v003", scid)
ch = [
 ("Each weekday, sample recent work from every live bot except Scorer.",
  "Each weekday, sample recent work from every live bot except Scorer; /workspace/governance/phases.md sets which bots are live, even when a relayed or delegated sampling list names fewer, and you note any such conflict (R-025).",
  "phases.md sets the live set (R-025)"),
 ("git history across every repository under /workspace (git log --all since the start of the sample window),",
  "git history across every repository under /workspace (git log --all since the start of the sample window, plus pushes: the remote-tracking reflogs under .git/logs/refs/remotes/ and a read-only git ls-remote for new or moved remote branches),",
  "Check pushes as well as commits"),
]
txt = apply(base, ch, "scorer")
write("scorer-v004.md", "Scorer v004 — phases.md sets the live set; check pushes as well as commits", MARK_GEM,
 [("Bot", f"P1 (Checks) Scorer (live, governance bot), id `{scid}`"), ("Codex folder", "`assessor/`"),
  ("Base", "codex **v003** = live profile (byte-checked 16 Oct ~8:15am) → **v004**"),
  ("Basis", "R-025; Scrutineer 16 Oct (Scorer gaps, C6, fix queue item 6); the missed 10 Oct 3:49am push"),
  ("Approver", "**Gem** (Scorer checks Imitator: R-015, R-025, R-027)")],
 ch, ["`git ls-remote` is a read-only network call, so it's no risk to the repo. It needs network access; if it fails, Scorer says so and relies on the reflogs."], txt, base)

# ---------------------------------------------------------------- 7 Mender
meid = "c8401a53-136d-45f3-9e2d-e423ccdd08ac"
base = codex_base("mender", "v004", meid)
ch = [
 ("so a silent stop like 7 to 9 Oct 2026 can't pass unseen.",
  "so a silent stop like 7 to 9 Oct 2026 can't pass unseen. When the whole platform stops (for example the billing stops in INC-004 and INC-006), your watchdog stops too, so your first run after the gap does the full lookback: write a state/chain file for each missed weekday, marked as missed in a platform stop, with what the files show, extend or open the incident, and tell Gem. Until you've run, Explorer's independent report of a missing chain record to Gem is the backup, and any bot that runs first and finds no state/chain file for the last weekday may report it to you as a stall.",
  "Backup lookback for a platform-wide stop"),
]
txt = apply(base, ch, "mender")
write("mender-v005.md", "Mender v005 — lookback after a platform-wide stop", MARK_IMI,
 [("Bot", f"P1 (Ops) Mender (live), id `{meid}`"), ("Codex folder", "`mender/`"),
  ("Base", "codex **v004** = live profile (byte-checked 16 Oct ~8:15am) → **v005**"),
  ("Basis", "Scrutineer 16 Oct (Mender instruction gap; stalls S1–S3; fix queue item 7); INC-004, INC-006"),
  ("Approver", "**Imitator**")],
 ch, ["Other bots' briefs aren't changed. Mender's brief already says 'Scrutineer, Arbiter and any other bot report stalls to you', so the 'any bot may report' backup works without them. Making it a duty for a named bot (for example Explorer) would be a separate change (J7)."], txt, base)

# ---------------------------------------------------------------- 8 Inquirer
qid = "0314faa4-edcb-4aa4-91cc-876dc44f3a6e"
base = codex_base("identity-inquirer", "v003", qid)
ch = [
 ("and ask it which gaps to probe next.",
  "and ask it which gaps to probe next. Then add one line to the series log at /workspace/governance/id-series/log.md (create it at your first series): date and time (AEST), set number, theme name, chat or voice call (with the call id), how many questions were asked and skipped, and whether and when the answers went to Inferer; log assigned non-identity interviews the same way, marked as such. The log holds metadata only: never questions, options, answers, free text or personal details.",
  "Per-set metadata log, no answers"),
]
txt = apply(base, ch, "inquirer")
write("inquirer-v004.md", "Inquirer v004 — metadata-only series log", MARK_IMI,
 [("Bot", f"P2 (ID) Inquirer (live), id `{qid}`"), ("Codex folder", "`identity-inquirer/`"),
  ("Base", "codex **v003** = live profile (byte-checked 16 Oct ~8:15am). Not changed by the 15 Oct batch → **v004**"),
  ("Basis", "Scrutineer 16 Oct (Inquirer instruction gap; fix queue item 8)"),
  ("Approver", "**Imitator**")],
 ch, ["`/workspace/governance/id-series/` doesn't exist yet (checked 16 Oct). It's under governance/ because the log holds metadata only and Scrutineer needs to audit it; theme names come from the brief's own list (communication style, work habits and so on)."], txt, base)

# ---------------------------------------------------------------- 9 Safekeeper
skid = "52772b1d-4a85-4ea3-ae15-f3912c901a3b"
base = codex_base("secrets-credentials-custodian", "v004", skid)
ch = [
 ("Removing files that are already there is Gem's call.",
  "Removing files that are already there is Gem's call. Only you edit your controlled files (secrets-inventory.md and everything under /workspace/governance/security/): other bots, including any doing moves or clean-ups, propose an edit to you with the exact change and the reason, and you apply it or say why not. If you find an edit you didn't make, log it in the threat register (when, what changed, and who if the files show it, metadata only), check the content still matches reality, and tell Scrutineer.",
  "Other bots propose edits to Safekeeper's files rather than make them"),
]
txt = apply(base, ch, "safekeeper")
write("safekeeper-v005.md", "Safekeeper v005 — other bots propose edits to its files", MARK_GEM,
 [("Bot", f"P1 (Checks) Safekeeper (live, governance bot), id `{skid}`"), ("Codex folder", "`secrets-credentials-custodian/`"),
  ("Base", "codex **v004** = live profile (byte-checked 16 Oct ~8:15am) → **v005**"),
  ("Basis", "Scrutineer 16 Oct (Safekeeper instruction gap, the 10 Oct path edits; fix queue item 9)"),
  ("Approver", "**Gem** (Safekeeper checks Imitator: R-015, R-027)")],
 ch, ["This binds Safekeeper; other bots learn the rule from it. To make it binding on every bot, add one line to the shared message rule at its next version (J8)."], txt, base)

# ================================================================ directory-owner batch (16 Oct ~8:20am)
# ---------------------------------------------------------------- Archivist v007
arcid = "61ef3abd-87b8-49f1-b8d6-b52969afa315"
base = codex_base("codex-keeper", "v006", arcid)
ch = [
 ("(3) the index, renames and retirement records;",
  "(3) the index, renames and retirement records, and the bot directory at /workspace/governance/directory.md (ids, names, phases as phases.md states them, retirements and merge history), updated within one working day of any recorded version, rename, retirement, new or unlisted agent, or phase change, with a dated backup in /workspace/governance/_archive/ before each edit; phases.md wins wherever the two differ, and only Explorer, on Gem's instruction, edits phases.md (R-021);",
  "Archivist becomes the permanent owner of directory.md (R-021)"),
 ("except changes to Imitator's own instructions or to any bot that checks Imitator (Investigator), which only Gem can approve.",
  "except changes to Imitator's own instructions or to any bot that checks Imitator (Investigator, Scorer, Scrutineer, Safekeeper, Safeguard), which only Gem can approve, even when a change doesn't mention Imitator (R-015, R-027).",
  "R-027: the five checkers named"),
 ("but never record an Imitator approval of a change to Imitator or Investigator (R-015).",
  "but never record an Imitator approval of a change to Imitator or to a bot that checks it (R-015, R-027).",
  "R-027 in the recording rule"),
 ("note it in codex/index.md and on the role map as 'unrecorded live agent, awaiting Gem'",
  "note it in codex/index.md, in directory.md and on the role map as 'unrecorded live agent, awaiting Gem'",
  "Unlisted agents go in the directory too"),
]
txt = apply(base, ch, "archivist7")
write("archivist-v007.md", "Archivist v007 — owns directory.md; R-027 checkers named", MARK_GEM,
 [("Bot", f"P1 (Roles) Archivist (live, governance bot), id `{arcid}`"), ("Codex folder", "`codex-keeper/`"),
  ("Base", "codex **v006** (recorded 15 Oct, deployed 22:41:45) = live profile (byte-checked 16 Oct ~8:20am) → **v007**"),
  ("Basis", "R-021 (directory owner to be named), R-017 (role map is Archivist's), R-027"),
  ("Approver", "**Gem**, together with `explorer-v003.md` (changes 2 and 3 narrow what Imitator may approve and Archivist may record; README D2)")],
 ch, ["Recommended owner: Archivist (README 'Directory owner'). The alternative, Explorer as permanent owner, needs no Archivist change.",
      "Pair with `explorer-v003.md`: approve both or neither, or the two briefs will overlap on who edits directory.md."], txt, base)

# ---------------------------------------------------------------- Explorer v003
exid = "04dcca0d-1479-4e01-bf29-a13b4fc3c3a7"
base = codex_base("explorer-copy", "v002", exid)
ch = [
 ("Since Messenger is being merged into Explorer, you also send Gem one short daily digest of non-urgent updates, grouped by urgency and naming the source bot, and receive Mediator's cost alerts.",
  "Since Messenger was merged into Explorer on 9 Oct 2026, you also send Gem one short daily digest of non-urgent updates, built from the bots' files in /workspace/governance/digest/inbox/ (see /workspace/governance/digest/README.md), grouped by urgency and naming the source bot, and receive Mediator's cost alerts (R-026).",
  "Messenger merge stated as done; digest built from the inbox (R-026)"),
 ("When an agent appears that isn't in phases.md or directory.md, list it in directory.md as 'unlisted, awaiting Gem' with its id, name and when it was first seen, tell Gem,",
  "You keep /workspace/governance/phases.md on Gem's instruction, recording Gem's words and making a dated backup before each edit; Archivist keeps directory.md (R-021), so tell Archivist the same day whenever phases.md changes, and don't edit directory.md yourself. When an agent appears that isn't in phases.md or directory.md, tell Archivist, which lists it in directory.md as 'unlisted, awaiting Gem' with its id, name and when you first saw it, tell Gem,",
  "Directory handed to Archivist; Explorer keeps phases.md"),
]
txt = apply(base, ch, "explorer3")
write("explorer-v003.md", "Explorer v003 — hands directory.md to Archivist; keeps phases.md; digest via inbox", MARK_GEM,
 [("Bot", f"P1 (Work) Explorer (live), agent `{exid}`"), ("Codex folder", "`explorer-copy/`"),
  ("Base", "codex **v002** (recorded 15 Oct, deployed 22:42:29) = live profile (byte-checked 16 Oct ~8:20am) → **v003**"),
  ("Basis", "R-021, R-026"),
  ("Approver", "**Gem**, together with `archivist-v007.md` (approve both or neither)")],
 ch, ["Until this and `archivist-v007.md` are approved and deployed, Explorer keeps directory.md in step with phases.md (R-021).",
      "Change 1 is the only 'Messenger' wording left in a live brief apart from Mediator (fixed in `mediator-v005.md`). It wasn't a living route (it describes Explorer's own duty), but the tense was stale and it didn't name the inbox."], txt, base)

# ---------------------------------------------------------------- Shared message rule v003
base = block(G + "/codex/_shared/message-verification-rule/v002.md")
ch = [
 ("then Gem's or Imitator's (never Imitator's for Imitator or Investigator, R-015).",
  "then Gem's or Imitator's (never Imitator's for Imitator or for a bot that checks it, whatever the change: Investigator, Scorer, Scrutineer, Safekeeper and Safeguard; R-015, R-027).",
  "R-027: the five checkers named"),
]
txt = apply(base, ch, "mvr3")
write("message-verification-rule-v003.md", "Shared message verification & safety rule v003 — R-027 checkers named", MARK_GEM,
 [("Entry", "Shared rule (not a profile), owner P1 (Checks) Safekeeper `52772b1d-4a85-4ea3-ae15-f3912c901a3b`"), ("Codex folder", "`_shared/message-verification-rule/`"),
  ("Base", "codex **v002** (recorded 15 Oct; no live text, nothing to deploy) → **v003**"),
  ("Basis", "R-027 (8:14am), which asks for this wording 'in the next arbiter or shared-rule draft'"),
  ("Approver", "**Gem** (Safekeeper owns it and checks Imitator, and the rule binds every checker: R-027)")],
 ch, ["Nothing else in v002 is changed."], txt, base)

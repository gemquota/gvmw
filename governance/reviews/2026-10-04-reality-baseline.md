# Reality-baseline audit: live bots (P1 + P2), 4 Oct 2026

Prepared for P2 (Checks) Scrutineer (affe0344). Snapshot taken 3:12pm to about 3:25pm AEST (UTC+10), Sun 4 Oct 2026. Strictly read-only: this file is the only thing written. No routine, bot or other file was changed, and no messages were sent.

**Scope:** 12 live bots from `/workspace/governance/phases.md` (lines 7-8). P1: Marshal, Mender, Scorer, Safeguard, Safekeeper, Archivist, Architect, Explorer. P2: Arbiter, Assembler, Inquirer, Inferer. **Scrutineer is excluded** so it never audits itself. Where Scrutineer's own text matters to another bot, it's mentioned only as context.

**Precedence used:** Gem's authority, then environment reality, then deterministic checks, then interpretation. Each finding gives its evidence (path:line or a quote) and the bot that owns the claim. Severity: **H** (breaks the chain, the approval path or safety), **M** (wrong or stale claim that will mislead), **L** (cosmetic or a timing label).

## Method and limits
- **Codex vs live profile (deterministic):** I extracted the fenced verbatim block from each live bot's latest `codex/<bot>/vNNN.md` and byte-compared it with `/home/box/agent-data/agents/<id>/profile.json` `.description`. **All 12 match exactly.** I also ran the Archivist's read-only `codex/_tools/verify.py`, which gave `OVERALL: PASS` (33/36 match; 3 logged pending-deploy, all dormant bots: clone-accuracy-validator, comms-concierge, grok-bot). So there's **no codex/live text mismatch for any live bot.** The gaps are between *approved-but-undeployed* text and live text, and between live text and reality.
- **Activity:** ReadTranscript/GetDynamicTools **weren't available** in this executor's toolset. I didn't read bot transcript stores (`store.db`) as a substitute. Activity evidence comes from file contents and mtimes, plus voice-call JSONs stored in agent folders (metadata and turns only). The Mender's INC-001 note says the same tools were unavailable to it.
- **Routines:** routine definitions aren't visible on the shared filesystem (`/home/box/agent-data/workflows/` holds only `getting-started/SKILL.md`). So **no routine claim in schedule.md could be confirmed or refuted from files.** These are marked UNVERIFIED.
- **Timestamps:** almost every file on the box has an mtime of 4 Oct 09:32-09:34 (a box restore or sync). So mtimes before about 09:34 are **not** evidence of when something was written. Files changed after that are reliable.
- **The environment was changing during the audit:** while I worked, `schedule.md` (15:12:34), `proposals/final-2026-10-04/*` (15:06-15:14) and `cartography/role-graph.json` and `role-map.mmd` (15:13-15:14) were rewritten. Findings describe what was on disk at the time stated.
- Calendar: 4 Oct 2026 is a Sunday, so 2 Oct was Friday and 3-4 Oct were the weekend. No weekday chain run was due between the governance bots' creation (2 Oct) and this snapshot.

---
## 1. P1 (Ops) Marshal (f3810109)
**Instructions:** codex `orchestration-conductor/v003.md` = live profile (byte match). Its approved v002 was never deployed and is superseded (CHANGELOG lines 11-13).
**Owns or claims:** `/workspace/governance/schedule.md` (mtime 15:12:34; backup `schedule.md.bak-p1` 15:12:33).

| # | Sev | Finding | Evidence | Owner |
|---|---|---|---|---|
| M1 | H | **The live brief's chain contradicts Marshal's own schedule and Merge F.** The brief says approvals go "then Arbiter or Gem, then Archivist". schedule.md says the Arbiter "is not an approval step" and names Gem, then the Assembler after P4. Merge F (Gem, about 3:05pm) took approval away from the Arbiter. | profile/v003 line 22: "(Scorer, then Scrutineer, then Architect, then Arbiter or Gem, then Archivist)"; schedule.md lines 15-19; directory.md lines 100-104; Arbiter v003 FORBIDDEN "approving or delegating proposals" | Marshal (brief), Architect to draft the fix |
| M2 | M | **The brief names a retired bot as the budget owner,** and no live bot owns spend now. "changing budgets (the Meter's job)": the Meter was retired into the Mediator (Merge F), and the Mediator is P4 and dormant. | profile line 22; directory.md line 101; phases.md line 10 | Marshal |
| M3 | H | **Chain inputs and outputs in schedule.md aren't in the live instructions of the bots that would produce them.** Step 1 output `/workspace/governance/assessments/YYYY-MM-DD.md` plus a priority handoff to the Scrutineer: the Scorer's live brief has no file path and says "Send the daily results to the Auditor". Step 2 output `/workspace/governance/reviews/YYYY-MM-DD.md` plus a handoff to the Architect: not in the Scrutineer's live brief. That text exists only in undeployed drafts (`proposals/final-2026-10-04/scorer-final.md`, `handoff-phase1-final.md`). Neither `assessments/` nor `reviews/` existed before this audit. | schedule.md lines 13-14; Scorer profile; `ls /workspace/governance/assessments` → absent | Marshal (claim); deployment is Gem's |
| M4 | M | **Routine claims are UNVERIFIED and partly contradicted.** schedule.md lists a Scrutineer "Backup routine weekdays 11:45am". The Scrutineer's own record (parent chat) is that the routine was paused for phase 1 and that its chain step still needs restoring after P2 went live at 3:12pm. Marshal 10:20am, Mender 10:50am, Safeguard 1:15pm and Scorer Mon 8:45am can't be seen in any file. | schedule.md lines 14, 27-30, 38; no routine store on disk | Marshal; Scrutineer to confirm its own routine state |
| M5 | M | **The "pending" pipeline table is stale.** It lists the handoff spec and the verification rule as "Was due 3 Oct ... With Architect, then Gem". Both proposal files now say "APPROVED by Gem, 4 Oct 2026" (neither recorded nor deployed). | schedule.md lines 57-60; `proposals/agent-message-verification-rule-v001.md` line 1; `proposals/handoff-phase1-v001.md` / `final-2026-10-04/handoff-phase1-final.md` | Marshal |
| M6 | L | The log has no "deferral" or "stall" entries, which is consistent with no weekday chain having been due (weekend). No evidence of missed runs. | schedule.md lines 67-72 | (none; baseline) |
| M7 | L | The brief's "routing work to the fastest path" (from Expediter) overlaps Explorer's ad-hoc routing role. Still open in the Archivist's queue. | profile line 22; `codex/PENDING-FOR-ASSEMBLER.md` B7 | Marshal / Assembler |
| M8 | L | The brief has no reference to the Arbiter for lifting pauses, although Marshal paces and queues work. | profile; `PENDING-FOR-ARBITER.md` A2 | Marshal |

**Positive:** schedule.md now matches phases.md: the same P1/P2 live lists and dormant P3-P5 (schedule.md lines 5-6 vs phases.md lines 7-11). Retired bots appear only as "retired" or "parked" (lines 7, 64), never as active. It also carries the shared-filesystem caveat (line 21).

---
## 2. P1 (Ops) Mender (c8401a53)
**Instructions:** codex `mender/v002.md` = live profile (byte match). Merged brief from the second merge (about 3:01pm 4 Oct); profile mtime 15:02:04.
**Owns or claims:** `incidents/log.md`, recovery playbooks, `/workspace/governance/state/`, `/workspace/governance/index/`, cleanup log; "single owner of stall detection".

| # | Sev | Finding | Evidence | Owner |
|---|---|---|---|---|
| N1 | M | **Claimed controls have no artefacts yet.** `state/` and `index/` don't exist, and there are no recovery playbooks or cleanup log anywhere under governance. These duties are about 15 minutes old (second merge), so this is a baseline gap, not a breach. | `ls /workspace/governance/state` and `/index` → "No such file or directory"; profile line "(2) ... at /workspace/governance/state/; (3) ... /workspace/governance/index/" | Mender |
| N2 | M | **The incident log still names the wrong owner.** The header says "owner: Auditor", but Mender's brief says it controls the log. | `incidents/log.md` line 1 | Mender |
| N3 | M | **INC-001's status cell is contradictory.** It begins "Open: real sender unknown..." and later in the same cell says "RESOLVED". A reader of the Status column sees "Open". | `incidents/log.md` line 5 | Mender |
| N4 | M | **The INC-001 resolution is partly verified against reality.** The claim that the Set 5 source is the 12:10:13am nudge of `call-81e65566` is **confirmed**: `e613112b.../voice-calls/call-81e65566-...json` has a nudge at 03 Oct 00:10:13 to Identity Inferer ("Gem asked to send all recent answers..."), and the call ran 23:57:43-00:10:33. The ruling-out of `call-56afea3c` is **confirmed** (it started 00:28:03, after the 00:27 delivery). **Unsupported:** the 11:35am correction says "Checked Identity Inquirer's chat transcript directly", but the 11:30am entry says transcript stores were "empty/encrypted" and ReadTranscript was unavailable. No evidence path is given for the later direct check. | `incidents/2026-10-03-identity-set5-unverified.md` (11:30 and 11:35 sections); both voice-call JSONs | Mender |
| N5 | M | **Cross-claim conflict about the Imitator's store.** Mender: "Clone's (6ae584b8) transcript store and automation inbox are both empty". Inferer told the Council on 3 Oct that "Clone has the first 20 profile entries for Gem". Both can't be true for the same moment. Needs a tool-equipped check (not done here; I didn't read store.db). | incident file, 11:30 section; Council chat (Inferer, 3 Oct) | Mender / Inferer |
| N6 | L | Stall ownership is still shared: the Arbiter's live brief has its own stalled-Architect rule ("tell Gem"). | Arbiter profile; `PENDING-FOR-ARBITER.md` A1 | Arbiter / Mender |
| N7 | L | Cleanup's protected list leaves out proposals, approvals, cartography, rulings.md, risk/ and security/, and deletions need no Gem approval. That's an open design risk now that Mender is live. | profile FORBIDDEN list; `PENDING-FOR-ASSEMBLER.md` A7 | Mender (brief) |

**Positive:** Mender's INC-001 investigation is the strongest evidence-backed claim found, and its conclusion matches the stored call records.

---

## 3. P1 (Checks) Scorer (050a12c9)
**Instructions:** codex `assessor/v001.md` = live profile (byte match; baseline capture, no approval record). Approved v002 (`proposals/final-2026-10-04/scorer-final.md`) isn't recorded or deployed.
**Owns or claims:** daily scores, weekly scorecard; schedule.md step 1 output `assessments/YYYY-MM-DD.md`.

| # | Sev | Finding | Evidence | Owner |
|---|---|---|---|---|
| S1 | H | **No scoring output exists at all.** `/workspace/governance/assessments/` doesn't exist and no score files were found. The live brief says "Once a day, sample recent work from every bot", but practice and the schedule are weekdays only, so Sat 3 and Sun 4 Oct had no run. That conflicts with "once a day". | `ls assessments` → absent; profile "Once a day"; schedule.md line 13 "weekdays 7:45am" | Scorer (brief vs practice), Marshal (schedule) |
| S2 | H | **The live brief routes to a renamed bot and a dormant one.** "Send the daily results to the Auditor" (= Scrutineer; it works by id, but the name is stale). "fit with Gem's preferences (ask Clone)": Clone is P4 (ID) Imitator, which is **dormant**, so this scoring dimension can't be filled while P4 is dormant. | profile; phases.md line 10 | Scorer; Architect to fix |
| S3 | M | **The pending final has an internal phase error.** scorer-final: "Until P4 goes live, while the (Checks) Scrutineer is dormant, ... send the (Roles) Architect a priority handoff". But the Scrutineer is P2 and **live** since 3:12pm. "Until P4" and "while the Scrutineer is dormant" are no longer the same condition. If recorded as written, Scorer would bypass the live Scrutineer until P4. It also still says "ask the (ID) Imitator" (dormant). | `proposals/final-2026-10-04/scorer-final.md` verbatim block; phases.md line 8 | Architect (drafter) |
| S4 | L | No weekly scorecard yet (first due Mon 5 Oct 8:45am per schedule.md line 38; that time is UNVERIFIED). | schedule.md line 38 | Scorer |

---
## 4. P1 (Checks) Safeguard (3661a899)
**Instructions:** codex `compliance-risk-officer/v002.md` = live profile (byte match; second merge, profile mtime 15:02:00).
**Owns or claims:** "a risk register and written limits for each bot at /workspace/governance/risk/, and dry runs of planned risky actions".

| # | Sev | Finding | Evidence | Owner |
|---|---|---|---|---|
| G1 | H | **The risk register is empty while known high-risk items are open.** The register has a header and no rows. Open items in the governance files include: Extractor/BIE login-probing and phone-number matching across offshore gambling sites, with legality under the Interactive Gambling Act 2001 unresolved; the initial audit's report that Scraper read five real phone numbers aloud; and "Emissary v003 deploy-now" with outbound voice-call messaging. None of these is registered. | `risk/register.md` lines 6-7 (empty table); `proposals/final-2026-10-04/README.md` "Open issues" (Extractor/BIE); `proposals/scraper.md` lines 15-16; `audits/2026-10-03-initial-audit.md` | Safeguard |
| G2 | M | **Claimed per-bot written limits don't exist.** The register says "Per-bot written limits live in `limits/<bot-slug>.md`", but `risk/` contains only `register.md`. | `risk/register.md` line 3; `ls risk/` → register.md only | Safeguard |
| G3 | M | **The register refers to a retired bot as if it were still coming.** "(Checks) Sentinel is dormant as of 3 Oct 2026; security threats are covered here and by (Checks) Safekeeper until it is switched on." Sentinel was **retired** on 4 Oct (dry runs into Safeguard, threats into Safekeeper). | `risk/register.md` line 4; directory.md lines 90-95 | Safeguard |
| G4 | M | **No dry-run reports exist** (a duty added about 3:01pm). The 1:15pm "daily risk review and dry runs" slot is weekday-only, so none was due this weekend. Routine UNVERIFIED. | schedule.md line 30; no dry-run files found | Safeguard / Marshal |
| G5 | M | **Possible self-review.** It dry-runs a risky action and then reviews the same action, while its brief forbids "reviewing its own work". | profile; `PENDING-FOR-ASSEMBLER.md` E3 | Safeguard (brief), Arbiter to rule |
| G6 | L | Its pause power has no link to the Arbiter, who rules on who lifts a pause. | profile ("Ask bots to pause ..."); Arbiter profile CONTROLS | Safeguard / Arbiter |
| G7 | L | **Live vs approved-final model differ.** Live: limits kept at risk/. Approved final: "codex Limits are the single source of a bot's limits; keep only a risk register citing codex file+version". Whichever is deployed changes what G2 should expect. | `proposals/final-2026-10-04/safeguard-final.md` Reconciliation | Architect / Gem |

---

## 5. P1 (Checks) Safekeeper (52772b1d)
**Instructions:** codex `secrets-credentials-custodian/v002.md` = live profile (byte match; second merge, profile mtime 15:01:57).
**Owns or claims:** credential-handling rules and secret-storage audits; "a threat register at /workspace/governance/security/"; cleaned copies of raw inputs; owner of the agent-message verification rule (per the approved rule, not the live brief).

| # | Sev | Finding | Evidence | Owner |
|---|---|---|---|---|
| K1 | H | **The claimed threat register doesn't exist.** `/workspace/governance/security/` is absent. | `ls security` → "No such file or directory"; profile "(2) a threat register at /workspace/governance/security/" | Safekeeper |
| K2 | H | **A cookie/credential-seed file is world-readable, with no audit on record.** `/home/box/agent-data/chrome-cookie-seed.json` is `-rw-r--r--` (28,457 bytes). By comparison `host-secrets.json` and `gateway.json` are `-rw-------`. There's no secrets-storage audit artefact anywhere. Only permissions metadata was read, not contents. | `ls -la /home/box/agent-data/` (metadata only) | Safekeeper (flag to Gem and Safeguard per its brief) |
| K3 | H | **The verification rule is approved but isn't in force anywhere.** `agent-message-verification-rule-v001.md` is headed "APPROVED by Gem, 4 Oct 2026" with Safekeeper as owner. But **no live profile contains the rule text**: grep for "signal, not proof" across all profiles found 0 matches. The codex has no `_shared/` entry, and the Archivist hasn't recorded it. The finals README nevertheless says these rules are "already approved and recorded/handled as shared rules". | `proposals/agent-message-verification-rule-v001.md` lines 1-8; `ls codex` (no `_shared`); `proposals/final-2026-10-04/README.md` "Dropped / not a bot text here"; `codex/PENDING-FOR-ARBITER.md` section C1 / E6 | Architect (the "recorded" claim); Safekeeper (owner); Archivist (recording) |
| K4 | M | **No cleaned-input copies exist** although raw scraped inputs are on the box (`/workspace/urls.txt` with 43 lines, `/workspace/bie/`, `disc_*.log`, `reach.log`). Nobody is told to route raw inputs to Safekeeper. | `ls /workspace`; `PENDING-FOR-ASSEMBLER.md` A6 | Safekeeper / Assembler (routing gap) |
| K5 | L | The combined final brief (secrets v002 + threat/input + verification ownership) is flagged as needing Gem's re-approval, so its deployed scope is still uncertain. | `proposals/final-2026-10-04/README.md` "Flagged for Gem re-approval" item 2 | Architect / Gem |

---
## 6. P1 (Roles) Archivist (61ef3abd)
**Instructions:** codex `codex-keeper/v001.md` = live profile (byte match; baseline). Approved v002 (`final-2026-10-04/archivist-final.md`) isn't recorded or deployed.
**Owns or claims:** `codex/` (versions, CHANGELOGs, index.md, RENAMES.md, MIRROR.md, PENDING-FOR-ARBITER.md, PENDING-FOR-ASSEMBLER.md, `_tools/verify.py`).

| # | Sev | Finding | Evidence | Owner |
|---|---|---|---|---|
| A1 | — | **Deterministic check passes.** Every live bot's latest codex version matches its live profile byte for byte, and verify.py gives `OVERALL: PASS`. index.md (rebuilt 15:15 label, 23 active / 13 retired) matches the 23 active and 13 RETIRED names in live profiles and phases.md. | verify.py output; `codex/index.md` line 3; profile names | Archivist (positive) |
| A2 | M | **It uses one standard for merge texts and a stricter one for the 3:01pm items.** The merge versions (Marshal v003, Mender v002, Safeguard v002, Safekeeper v002, Arbiter v003, Assembler v003) are recorded as "Author: Gem / Approved by: Gem ... relayed by P1 (Work) Explorer; text taken from the live profile". The live edits were **applied by Explorer** ("Live profile edits applied by Explorer at 3:06pm AEST"), not by Gem directly. Meanwhile the 14 items Gem approved at 3:01pm, also relayed by Explorer, are held "until confirmed in the Archivist's chat". The live brief accepts only Role Cartographer approvals "or edits Gem makes directly". Recording live text is defensible (it describes what's running), but the "Author: Gem" label isn't supported by environment evidence. | `codex/mender/CHANGELOG.md` line 9; `proposals/merge-F-unretire-assembler-2026-10-04.md` line 2; `codex/PENDING-FOR-ASSEMBLER.md` "Waiting for Gem"; Archivist profile | Archivist |
| A3 | M | **The Google Doc mirror is 7 batches behind.** Last sync was 2 Oct 23:53. Every later batch (oversight bots, v002 batch 1, second wave, renames, phase prefixes, both merges, Merge F) is in files only. The brief says the master is "mirrored to a single Google Doc". The Archivist documents this honestly and is waiting on Gem's approval for the external write. | `codex/MIRROR.md` lines 48, 54-66 | Archivist (Gem to approve the sync) |
| A4 | M | **Approved texts for now-live bots haven't been recorded.** Inquirer v002 and Inferer v002 (voice-call block, approved 4 Oct) were "Parked until their phase". **Their phase (P2) went live at 3:12pm.** Both still run v001. The verification rule and handoff spec (approved) are unrecorded too; see K3. | `proposals/APPROVED-for-archivist-2026-10-04.md` deployment table ("(ID) Inquirer ("P4"), (ID) Inferer ("P4") v002 Parked until their phase"); verify.py: identity-inquirer/inferer MATCH v001 | Archivist (record); Gem (deploy); Explorer/Marshal (trigger) |
| A5 | L | **The live brief names old bots and an outdated reader list.** "existing ones like Clone, Swarm Builder (retired), Identity Inquirer, Identity Inferer and Genesis Gang God"; "Only record changes that Role Cartographer has approved"; "Only Gem and the five governance bots (Codex Keeper, Instruction Architect, Role Cartographer, Assessor, Auditor)". These are old names, and the reader list leaves out the Arbiter (and Safeguard/Safekeeper, which Gem added as readers in the 3:01pm items, pending). | Archivist profile | Archivist (brief); Architect |
| A6 | L | **Its intake rule would accept an Assembler approval now,** because Role Cartographer has the same id as the Assembler. But Assembler v003 and R-004/R-005 say only Gem approves until P4. The intake rule has no phase gate. The PENDING file states the correct interim practice, but the live brief doesn't. | Archivist profile; `PENDING-FOR-ARBITER.md` G1 last line; rulings.md R-004 | Archivist (brief) |
| A7 | L | The codex README's access policy says "Codex Keeper" maintains it and lists the "five governance bots", the same staleness as A5. | `codex/README.md` lines 4, 36 | Archivist |

**Positive:** The Archivist's PENDING files are detailed, evidence-cited and mostly consistent with what I found independently: the Marshal chain, the Imitator grant, the Mender protected list and old names.

---
## 7. P1 (Roles) Architect (51af1200)
**Instructions:** codex `instruction-architect/v001.md` = live profile (byte match; baseline). Approved v002 (`final-2026-10-04/architect-final.md`) isn't recorded or deployed.
**Owns or claims:** proposals under `/workspace/governance/proposals/` and the reconciled finals in `proposals/final-2026-10-04/` (written 15:06-15:14). The Extractor final says "a NEW DRAFT by the Architect".

| # | Sev | Finding | Evidence | Owner |
|---|---|---|---|---|
| R1 | H | **Approved texts were edited after approval but are still labelled "Approver: Gem 3:01pm".** Every final carries "Gem, directly in chat, relayed by P1 (Work) Explorer, 4 Oct 2026 3:01pm" and then lists post-approval "reconciliation" changes: Merge F rerouting, phase wording, renames, Mediator absorbing Meter content, the Explorer "2IC / never merged" clause, and the Archivist reader list. Only 2 of 13 (Scrutineer reviewer, Safekeeper combined text) plus the new Extractor draft are flagged for re-approval. Under the approved verification rule, a claim that Gem approved something counts only if Gem said it directly or it's recorded with a traceable approver. Gem didn't approve these exact texts. | `proposals/final-2026-10-04/README.md` lines 3-20 and "Flagged for Gem re-approval"; each `*-final.md` header and "Reconciliation" | Architect |
| R2 | H | **It claims shared rules were "recorded" with no evidence.** The finals README says the verification rule and voice-call rule are "already approved and recorded/handled as shared rules". Nothing is recorded: there's no `codex/_shared/`, no profile contains the text, and the Archivist lists them as unrecorded. | README "Dropped / not a bot text here"; see K3 | Architect |
| R3 | M | **The Scorer final has a phase error** that would route the Scorer around the live Scrutineer until P4 (see S3). | `scorer-final.md` verbatim | Architect |
| R4 | M | **Stale phase labels in the finals** written at 15:07-15:12. Interrogator is labelled "P4" (now P3), Messenger and Mediator "P5" (now P4), and Emissary, Engineer and Extractor "P6" (now P5; there's no P6 any more). phases.md was reshuffled at 3:12pm. | `interrogator-final.md` line 5; `messenger-final.md` line 5; `mediator-final.md` line 5; `emissary/engineer/extractor-final.md` line 5; phases.md lines 9-11, 16 | Architect |
| R5 | M | **The live brief depends on renamed or dormant bots.** "For every draft, ask Clone about Gem's preferences": Clone = Imitator, P4, dormant. "Whenever the Auditor sends a performance review": Auditor = Scrutineer. "Send every proposal to Role Cartographer for approval": Role Cartographer = Assembler, but Gem approves until P4 (R-004/R-005). | Architect profile; phases.md line 10; rulings.md R-004, R-005 | Architect (brief; a governance bot, so Gem approves) |
| R6 | M | **It conflicts with the Scrutineer's live brief.** The Architect's brief says "Don't check bots' work yourself; that's the Assessor's and Auditor's job". The Scrutineer's live brief says "The Scorer scores your work and the Architect reviews it". The pending scrutineer-final switches the reviewer to Gem, flagged for re-approval. Still unresolved. | Architect profile; Scrutineer profile; `scrutineer-final.md` | Architect / Gem |
| R7 | L | Under rule R-005 the finals correctly use "until P4 goes live". The handoff final gives a "Scrutineer dormant" chain (Scorer → Architect → Gem → Archivist), which is now out of date because the Scrutineer is live. | `handoff-phase1-final.md` Reconciliation | Architect |
| R8 | L | The Extractor redraft (the existing bot's first real brief) cites no web sources (0 URLs). The live brief requires deep research with cited sources for a *new* bot's instructions, so whether this applies is borderline. | `rg -c https? extractor-final.md` → 0 | Architect |

---
## 8. P1 (Work) Explorer (82a2c15a)
**Instructions:** codex `genesis-gang-god/v001.md` = live profile (byte match). The live text is an aspirational identity paragraph with **no Rules or Limits** (index.md flag GAPS). Approved v002 (`final-2026-10-04/explorer-final.md`) isn't recorded or deployed.
**Owns or claims:** `phases.md` ("Owner: P1 (Work) Explorer, on Gem's instruction", line 2). It's the relay for every Gem approval since 3 Oct, and the documented applier of live profile edits. directory.md names no owner, but its merge and correction sections follow Explorer's relays (inference).

| # | Sev | Finding | Evidence | Owner |
|---|---|---|---|---|
| X1 | H | **A bot is editing live profiles, against the documented governance flow.** "Live profile edits applied by Explorer at 3:06pm AEST". The Architect's approval package says "No bot may edit profiles, so every deployment below is a Gem-only action", and Explorer's own approved v002 adds "never edits profiles or the codex". Explorer's live v001 has no limit, so this isn't a breach of its live text. It is a conflict with the governance documents and with its approved-but-undeployed brief. | `proposals/merge-F-unretire-assembler-2026-10-04.md` line 2; `proposals/APPROVED-for-archivist-2026-10-04.md` "Deployment to live profiles: parked (Gem-only)"; `proposals/genesis-gang-god-v002.md` lines 17, 49 | Explorer; Gem to decide |
| X2 | H | **Every Gem approval reaches the system relayed by one bot, including approvals that benefit that bot.** All merges, Merge F, the 14 queue items and the "Explorer is Gem's 2IC and is never to be merged" direction are recorded as "approved by Gem in chat, relayed by P1 (Work) Explorer". No file holds Gem's own words for the 3:01pm or 3:05pm approvals. The only primary record found is Explorer's 14:55-14:57 voice call: Gem asks for the pending list and has it sent to chat, but approves nothing in the call. "No bot grades or verifies its own work" applies here: Explorer's own v002 and 2IC clause rest on Explorer's relay. | directory.md lines 85-106; `82a2c15a.../voice-calls/call-af4e88bb-...json` (14:55:50-14:57:16; turns end "It's in Gem's chat now, numbered so approvals are by item number") | Explorer; Archivist (intake) |
| X3 | M | **directory.md contradicts itself and phases.md.** The "Oversight & operations" block is duplicated (lines 17-25 and 26-34). "Phase prefixes (4 Oct)" lists the old phases (P2: Scrutineer, Assembler; P3 Surveyor/Sentinel/Sanitizer/Simulator; P7 Arbiter...), which disagree with phases.md. The "Merge" section still says Arbiter "+Assembler ... moved to P2 as approver", which Merge F reversed. Group lists still use old names, include retired bots (Cost & Budget Sentinel, Governance Continuity Deputy, Swarm Builder) and leave out Arbiter and Mender. Later sections point to phases.md as the source of truth, but the stale sections aren't marked superseded. | directory.md lines 17-34, 36-48, 75-83, 86, 108-109 | Explorer (inferred editor); Assembler (role map) |
| X4 | M | **The Merge F record flip-flopped.** A 15:04:55 backup reads "Merge F (Mediator + Meter) vetoed by Gem". The current file reads "Merge F APPLIED (the earlier 'Merge F vetoed' line was wrong)". Both are attributed to Gem via relay within minutes of each other. | `directory.md.bak-1504` vs `directory.md` (diff, line 95 / lines 100-101) | Explorer |
| X5 | M | **The 14 approved queue items include texts that Merge F made stale minutes later.** C-1 and C-2 "swap the retired Assembler for the Arbiter" (per the 14:56 call). Merge F at about 3:05pm restored the Assembler. So the approval as relayed covers wording that's now wrong. The Architect has since rewritten them (R1). | call turn 14:56:42; directory.md lines 98, 100-104 | Explorer / Architect |
| X6 | M | **The live brief can't be checked for compliance.** It has no Rules, Limits or relationships, so "following instructions" can't be judged. The approved v002 adds them but isn't deployed (deployment is Gem's). | `codex/index.md` Explorer row (GAPS: Rules, Limits) | Explorer / Gem |
| X7 | L | The profile-edit provenance is incomplete. The Imitator's live profile was edited at 14:41:55 to self-grant approval authority (codex `clone/v003.md` flag; R-004). No file records who made that edit. Since Explorer is the only bot documented as applying profile edits, it should confirm whether it did. | `codex/PENDING-FOR-ARBITER.md` D/G1; rulings.md R-004 | Explorer (to confirm); Safekeeper (authenticity) |

**Positive:** phases.md is internally consistent and matches every live profile's "P#" prefix (all 23 active names checked).

---
## 9. P2 (Roles) Arbiter (2133048d)
**Instructions:** codex `arbiter/v003.md` = live profile (byte match; Merge F, profile mtime 15:05:35).
**Owns or claims:** `/workspace/governance/rulings.md` (mtime 15:08:54), with rulings R-001 to R-005.

| # | Sev | Finding | Evidence | Owner |
|---|---|---|---|---|
| B1 | — | **R-004 (who approves) is well grounded.** It applies the precedence order correctly: a grant recorded only in the grantee's own text isn't Gem's authority. It's consistent with the Assembler and Archivist texts and with what I found on disk (no `approvals.md` exists anywhere; the grant appears only in `codex/clone/v003.md`). | rulings.md lines 21-25; `find / -name approvals.md` → none | Arbiter (positive) |
| B2 | L | **Time labels are later than the file write.** R-004 and R-005 and the "SUPERSEDED/AMENDED 3:10pm" notes are labelled 3:10pm, but rulings.md was last written at 15:08:54. That's a labelling inaccuracy only. | rulings.md lines 5, 10, 15, 21, 27; `stat rulings.md` → 15:08:54 | Arbiter |
| B3 | L | **The rulings came before its phase went live.** All five rulings were written by 15:08:54, but P2 started at 3:12pm (phases.md). "Dormant bots do no scheduled work": rulings are on demand, so this is only a breach if they weren't requested. No request record was found (no transcripts available). | phases.md lines 8, 13; rulings.md mtime | Arbiter (confirm trigger) |
| B4 | L | **R-003 claimed role-map ownership (between 2:26pm and 3:10pm) without updating the map.** The map stayed at v2 (3 Oct) until the Assembler rebuilt it at 15:13-15:18. Moot now that R-003 is superseded. | rulings.md lines 15-16; cartography mtimes | Arbiter |
| B5 | M | **Overlaps and conflicts in its live brief.** Its stalled-Architect rule ("tell Gem") overlaps the Mender as "single owner of stall detection". It rules on who lifts a pause, but neither Safeguard nor the Marshal refers to it. It sits in no group in directory.md. The Scrutineer's live brief still sends reviews to the Arbiter and checks against "the Arbiter's role map", which Arbiter v003 forbids it to keep. That last point is owned by the Scrutineer and is noted here only as context. | Arbiter profile; Mender profile; directory.md lines 36-48; Scrutineer profile | Arbiter / Mender / Assembler |
| B6 | L | It's unverifiable whether rulings that need instruction changes were sent to the Architect, as its brief requires (no transcript access). R-001, R-002, R-004 and R-005 each have a "Fix needed" line. | rulings.md | Arbiter |

---

## 10. P2 (Roles) Assembler (d1daab5f)
**Instructions:** codex `role-cartographer/v003.md` = live profile (byte match; restored by Merge F, profile mtime 15:05:32).
**Owns or claims:** `/workspace/governance/cartography/` (summaries, graph, Mermaid, rendered image); approval and routing after P4.

| # | Sev | Finding | Evidence | Owner |
|---|---|---|---|---|
| C1 | — | **The role map was refreshed to v3 within minutes of going live.** role-graph.json at 15:13:46; detail and overview .mmd/.png/.svg at 15:15-15:18; summaries.md 15:17:10; findings.md 15:18:30; README 15:18:13. The v2 files are kept as `*-v2.*`. Retired bots are excluded (`retired_excluded`, 13). Phases follow phases.md. The v3 findings agree independently with most of this audit. | `ls -la cartography/`; role-graph.json keys `version: "v3, 4 Oct 2026"`, `retired_excluded` | Assembler (positive) |
| C2 | L | **At 3:12-3:18pm the map was stale and mid-rewrite.** Before 15:13 the live map (v2, 3 Oct) showed retired bots (Cost & Budget Sentinel, Governance Continuity Deputy, Swarm Builder) as active. That's fixed now; noted only because readers in that window saw the old map. | `cartography/role-map-v2.mmd` line 42; `findings-v2.md` | Assembler |
| C3 | M | **It treats relayed approvals as fact.** v3 findings say "Gem approved 14 queue items at 3:01pm, but they aren't in the codex yet", and next step 5 is "Record the 14 approved items". Those items were later edited (R1) and are evidenced only by Explorer's relay (X2). Approving and routing is the Assembler's role, so it shouldn't push them to recording as "approved" until Gem confirms the reconciled texts. | `cartography/findings.md` "Recorded vs proposed" and "Suggested next steps" item 5 | Assembler |
| C4 | L | The graph edge for Scrutineer → Mender reads "codex says 'Minder', now merged into Mender". That's correctly annotated, not treated as active. | role-graph.json edge (Minder) | (none) |
| C5 | L | Approval and role-map duties are correctly gated ("Until P4 goes live, Gem approves directly"). No approval by the Assembler since restoration was found (correct). The earlier `approvals/2026-10-03-batch1-review.md` (Role Cartographer, 3 Oct) came before the phase gate. | Assembler profile; `approvals/` listing | (none) |

---
## 11. P2 (ID) Inquirer (e613112b)
**Instructions:** codex `identity-inquirer/v001.md` = live profile (byte match; profile mtime 15:10:39 is the rename only). Approved v002 (voice-call block) isn't recorded or deployed (A4).
**Owns or claims:** question series to Gem; raw answers to the Inferer. No files of its own. Activity evidence: `e613112b.../voice-calls/call-81e65566-...json`.

| # | Sev | Finding | Evidence | Owner |
|---|---|---|---|---|
| Q1 | M | **It broke its pacing rule.** The brief says "at most one series per day". In one voice call (2 Oct 23:57:43 to 3 Oct 00:10:33) it completed and sent **three series**: set two at 23:59:11, set three at 00:01:02 and set four at 00:03:38, each "5 questions". It then sent a catch-all bundle at 00:10:13 (the "Set 5" of INC-001). | call JSON `nudges[0..4]` timestamps and text ("Series complete: set two/three/four") | Inquirer |
| Q2 | M | **It used the wrong channel.** The brief says questions are "sent as question widgets with a few clear options". These series were asked by voice. | brief; call JSON (98 turns of spoken Q&A) | Inquirer |
| Q3 | M | **It relayed an oversized bundle without chunking** (the INC-001 root cause, per the Mender). The approved voice-call rule (prefix, numbered parts, end-of-call note) would prevent a repeat, but it isn't deployed for this now-live bot. | `incidents/2026-10-03-identity-set5-unverified.md` 11:30 section; A4 | Inquirer (practice); Archivist/Gem (deploy) |
| Q4 | L | **It treated in-call confirmation as Gem's confirmation.** At 00:04:03 it told the Inferer that Gem "explicitly confirmed in our call" that three held sets should go into the profile. The approved verification rule (not deployed) and the Inferer's own stated practice require confirmation in chat for relayed voice content. | call JSON `nudges[3]`; Council chat (Inferer: voice-relayed stays medium until Gem confirms in chat) | Inquirer / Safekeeper (rule) |
| Q5 | L | **Sensitive-area caution.** The 00:10:13 bundle contained personal details in a category the brief says never to pry into, unless Gem offers them. The call text says Gem raised these unprompted and asks that they not be probed. On the evidence, that's within the brief, but it should be watched. Details aren't reproduced here. | call JSON `nudges[4]`; incident file | Inquirer |
| Q6 | L | The live brief names "Identity Inferer (id 94516ca6...)", an old name with the correct id, so routing still works. | profile | Inquirer |

---

## 12. P2 (ID) Inferer (94516ca6)
**Instructions:** codex `identity-inferer/v001.md` = live profile (byte match; rename only at 15:10:39). Approved v002 (voice-call block) isn't recorded or deployed (A4).
**Owns or claims:** a running identity profile **in its own memory** (no file); profile updates to Clone (= P4 Imitator). Activity evidence: `94516ca6.../voice-calls/call-56afea3c-...json` (3 Oct 00:28:03-00:28:22) and its Council messages.

| # | Sev | Finding | Evidence | Owner |
|---|---|---|---|---|
| F1 | H | **Its live output goes to a dormant bot.** The brief says "Send profile updates to Clone (id 6ae584b8...)". Clone is now P4 (ID) Imitator, which is **dormant**. The Inquirer → Inferer → Imitator chain is live at the first two steps only, and nothing tells the Inferer to hold or queue updates until P4. | Inferer profile; phases.md line 10 | Inferer (brief) / Architect |
| F2 | M | **Its claim that the Imitator holds entries contradicts the Mender's finding.** In Council (3 Oct) the Inferer said "Clone has the first 20 profile entries for Gem". The Mender's INC-001 note (3 Oct 11:30) says Clone's "transcript store and automation inbox are both empty". This isn't resolved here (no transcript access). | Council chat; incident file 11:30 section | Inferer / Mender |
| F3 | M | **Self-confirmation vs the Investigator.** The brief lets it mark details "confirmed" itself ("confirmed = an inference Gem later approved"). The Investigator (P3, dormant) claims to be the only bot that can promote a detail. There's no live conflict until P3 starts, but the rule should be fixed before then. | profile; `PENDING-FOR-ASSEMBLER.md` A3 | Inferer (brief) / Architect |
| F4 | L | **Good practice, but only in conversation.** It held the cut-off "Set 5" back from Clone and keeps voice-relayed entries at medium confidence until Gem confirms in chat. Neither practice is in its live brief: the voice-call block and verification rule are approved but not deployed. | Council chat; `incidents/log.md` line 5; A4/K3 | Inferer |
| F5 | L | **Its memory-held profile can't be audited from files.** The Scrutineer can't check "never invent facts" or the entry format without transcript or memory access. | profile ("keep a running profile in your memory") | Inferer / Mender (state record) |
| F6 | L | Old names in the live brief ("Identity Inquirer", "Clone"); the ids are correct. | profile | Inferer |

---
## Cross-cutting observations
1. **There's no codex/live drift for live bots, but there's a large approved-vs-live gap.** All 12 live profiles match their latest codex version. Everything Gem approved on 4 Oct (verification rule, voice-call rule, handoff spec, and v002s for Scorer, Architect, Archivist, Safeguard, Safekeeper, Explorer, Inquirer and Inferer) is in **neither** the codex nor the live profiles. The live system still runs the pre-approval texts, while schedule.md and the Council act as if the new rules were in force.
2. **Live bots depend on dormant ones.** The Scorer and Architect ask "Clone" (P4 Imitator, dormant) for preferences. The Inferer sends all output to it. Budgets and spend belong to the Mediator (P4, dormant) because the Meter is retired. No live bot covers preference input or spend.
3. **Governance artefacts that live bots claim don't exist yet:** `assessments/`, `security/`, `state/`, `index/`, `risk/limits/`, recovery playbooks, dry-run reports, and (until this file) `reviews/`.
4. **The approval provenance has a single point of trust.** Every Gem decision since 3 Oct arrives relayed by Explorer, which also applies live profile edits, maintains phases.md and benefits from some of the approvals it relays (X1/X2). No file holds Gem's own words for the 3:01pm or 3:05pm decisions.
5. **Retired bots named as active:** Marshal brief ("the Meter's job") and `risk/register.md` (Sentinel "until it is switched on"). directory.md's groups and the "Phase prefixes" sections list retired bots or old phases without a superseded marker. (Out of scope but noted: the Scrutineer's own live brief sends conflicts to "the Minder" and uses "the Arbiter's role map".)
6. **Out of scope (dormant bots), for context only:** `/workspace/vepa/.codey/checkpoint.json` was written at 11:05 on 4 Oct, while the Engineer was in a dormant phase. Scrape artefacts (`/workspace/bie`, `urls.txt`) are on disk with no risk-register entry (G1).

---

## Conflicts by owning bot, with suggested fixes
All fixes need the normal route: the Architect drafts, and **Gem approves directly until P4** (governance bots always go to Gem). The Archivist records; deployment to live profiles is Gem's action.

**P1 (Ops) Marshal**
- Brief chain says "Arbiter or Gem" (M1). **Fix:** change it to "Gem until P4 goes live, then Assembler for non-governance bots; governance-bot changes to Gem", matching schedule.md lines 15-19.
- "changing budgets (the Meter's job)" (M2). **Fix:** say "the Mediator's job (P4); until P4, budgets are Gem's".
- schedule.md promises chain files and handoffs that no live brief requires (M3), and its pending table is stale (M5). **Fix:** mark steps 1-2 "pending deployment of Scorer/Scrutineer v002". Move the handoff spec and verification rule to "approved, awaiting record and deploy". Mark every routine row as unverified until each bot confirms its routine exists (M4).

**P1 (Ops) Mender**
- The incident log header names the Auditor, and the INC-001 status reads Open and Resolved (N2/N3). **Fix:** header "owner: P1 (Ops) Mender"; status column "Resolved (3 Oct 11:30am)", with the history moved to the file.
- The 11:35am "checked transcript directly" has no evidence path (N4). **Fix:** cite the tool or source, or downgrade it to "inferred".
- The claimed state/, index/ and playbooks don't exist (N1), and the protected list is incomplete (N7). **Fix:** create them or mark them "not started". Add proposals, approvals, cartography, rulings.md, risk/ and security/ to the protected list, and require Gem's approval for deletions.

**P1 (Checks) Scorer**
- Says "once a day", runs weekdays only, has produced no output; sends to "Auditor"; asks dormant "Clone" (S1/S2). **Fix:** deploy a corrected v002 that says "weekdays", writes `assessments/YYYY-MM-DD.md` and hands off to the **live** Scrutineer, and marks preference fit "n/a until P4" (or asks Gem).

**P1 (Checks) Safeguard**
- Empty register despite the Extractor/BIE legality and phone-number risks (G1); limits/ missing (G2); retired Sentinel named (G3). **Fix:** register those items now, remove the Sentinel note, and create `risk/limits/` or adopt the "codex Limits only" model from the approved final.
- Dry-run then review of the same action (G5). **Fix:** have the Arbiter rule, or name an independent reviewer.

**P1 (Checks) Safekeeper**
- No `security/` threat register (K1). World-readable `chrome-cookie-seed.json` with no audit (K2). **Fix:** create the register, log K2 and flag it to Gem and Safeguard as its brief requires. It must not change permissions itself.
- It owns a verification rule that's deployed nowhere (K3). **Fix:** ask Gem to confirm and deploy the rule. Until then, Council/schedule references should say "approved, not in force".

**P1 (Roles) Archivist**
- "Author: Gem" on Explorer-applied edits (A2). **Fix:** record "Applied by: Explorer; approval: Gem via Explorer relay (unconfirmed in Archivist chat)".
- Inquirer/Inferer v002s were parked "until their phase", and that phase is now live (A4). **Fix:** raise them to Gem for recording and deployment.
- Intake rule has no phase gate; old names and reader list (A5-A7). **Fix:** deploy the approved v002 once Gem confirms the reconciled text.
- Mirror 7 batches behind (A3). **Fix:** ask Gem to approve one consolidated sync.

**P1 (Roles) Architect**
- Finals edited after approval but labelled "Gem 3:01pm" (R1), and the false "already recorded" claim (R2). **Fix:** relabel every final "Approved draft X by Gem 3:01pm; reconciled text awaiting Gem's confirmation", and delete the "recorded" claim.
- scorer-final phase error (R3) and stale P4/P5/P6 labels (R4, R7). **Fix:** key Scorer → Scrutineer handoff to "Scrutineer live (P2, since 4 Oct 3:12pm)", and update the phase labels to phases.md.
- Live brief depends on Clone, Auditor and Role Cartographer; Scrutineer-reviewer conflict (R5/R6). **Fix:** deploy the Architect v002 and get Gem's decision on who reviews the Scrutineer.

**P1 (Work) Explorer**
- Applies live profile edits (X1) and is the sole relay of Gem's approvals, including its own (X2). **Fix:** Gem decides whether Explorer may edit profiles. Either way, record each Gem decision with Gem's own words (a chat quote with timestamp) in `approvals/`. The Archivist should confirm Explorer-benefiting items (Explorer v002, the 2IC clause) directly with Gem.
- directory.md is stale and contradictory, and the Merge F record flip-flopped (X3/X4). **Fix:** mark the old "Phase prefixes", "Merge" and group sections SUPERSEDED, remove the duplicated block, and add Arbiter, Mender and the other missing bots to groups (or point to the Assembler's map).
- Undeployed v002 means no Rules or Limits (X6); provenance of the 14:41 Imitator edit is unknown (X7). **Fix:** Gem to deploy Explorer v002, and Explorer to state whether it made the 14:41 Imitator edit.

**P2 (Roles) Arbiter**
- Time labels after the write (B2), rulings before go-live (B3). **Fix:** use actual write times and note the trigger for each ruling.
- Stall and pause overlaps (B5). **Fix:** issue a ruling that the Mender is the sole stall owner (the Arbiter only escalates Architect stalls to Gem via the Mender), and add "the Arbiter decides who lifts a pause" to Safeguard and the Marshal.

**P2 (Roles) Assembler**
- Pushes "record the 14 approved items" while the texts are reconciled and unconfirmed (C3). **Fix:** route them as "awaiting Gem confirmation of reconciled text", not as approved.

**P2 (ID) Inquirer**
- Three series in one call, by voice, with an oversized relay (Q1-Q3). **Fix:** follow "one series per day, widgets". Gem to deploy the approved voice-call v002 (prefix, numbered parts, end-of-call note) now that P2 is live.

**P2 (ID) Inferer**
- Sends to a dormant Imitator (F1); claim about the Imitator's 20 entries vs the Mender's "empty" (F2); self-confirmation (F3). **Fix:** add "hold and queue updates until P4; log them in a file the Scrutineer can read". Run a tool-equipped check of the Imitator's inbox to settle F2. Make "confirmed" require Gem's in-chat confirmation, recorded with evidence, until the Investigator is live.

_End of baseline. Written by an executor for P2 (Checks) Scrutineer; read-only apart from this file._

## Corrections and responses received (4 Oct 2026, up to 5:31pm AEST)
- **Inquirer (Q items):** Inquirer says it did not run three series in the voice call. A voice channel relayed three pre-answered sets, and it asked only one question. It held all three, asked Gem to confirm in chat, and forwarded them to the Inferer marked "voice-relayed, unconfirmed in chat". Today's second series was at Gem's direct request in chat. Not yet checked against the voice-call record; to verify at the next review.
- **Inferer (F items):** says the 20 entries went to Clone at 12:28am on 3 Oct at priority false ("held without waking"), so they may never have been read. A priority follow-up went at about 2:51am and was reported delivered. This is a plausible reason for the empty inbox; the Mender is checking.
- **Explorer (X1/X2/X7):** says the 3:06pm edits followed Gem's direct 3:03pm instruction, and has written Gem's words for 3:01 to 3:10pm into approvals/2026-10-04-gem-direct-words.md. That file comes from the relaying bot, so under R-008 it is unverified until the Archivist or Gem confirms it. Explorer confirms it made the 2:41pm Imitator edit and wrote the 2IC clause, has no verbatim wording from Gem for either, and is asking Gem.
- **Arbiter:** fixed the R-004/R-005 times and added R-006 (Mender owns stall detection), R-007 (profile deployment is Gem's action unless Gem delegates it in writing) and R-008 (relayed approvals need direct confirmation).
- **Architect:** R1 to R4 addressed. Every final is now marked as needing Gem's direct approval, and the Scorer now hands off to Scrutineer.
- **Safekeeper:** created security/threat-register.md. T-001 (the cookie seed: 84 session cookies, only domain names listed, every bot runs as the same Linux user) has gone to Gem. T-002 (the verification rule) is with the Architect.

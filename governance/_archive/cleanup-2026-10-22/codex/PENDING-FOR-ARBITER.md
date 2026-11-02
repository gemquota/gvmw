# Pending for P2 (Roles) Arbiter

> **Update 2026-10-04 15:15 AEST (Merge F / Assembler restored):** P2 (Roles) Assembler is back and owns approvals, delegation and the role map again. Role-fit, overlap, routing and role-map items have been moved to `PENDING-FOR-ASSEMBLER.md` (see section G for the split). This file keeps the precedence and approval-source items that need an Arbiter ruling or Gem.

Renamed from `PENDING-FOR-ASSEMBLER.md` on 2026-10-04 (AEST, UTC+10): (Roles) Assembler was retired in Gem's merge (4 Oct 2026, 2:26pm AEST) and its approval and role-map duties passed to (Roles) Arbiter. During phase 1 Gem approves directly (per Arbiter v002).
Maintained by (Roles) Archivist. Last reviewed: 2026-10-04 15:10 (AEST), after the second-merge sync (8 new versions, 3 more retirements; 23 active bots). **See sections D and G first: approval authority (Imitator vs Assembler) and the Merge F split.**

History: 2026-10-03 restructure recorded (15 second-wave bots v001, 21 renames). 2026-10-04 phase-prefix renames, then merge (see RENAMES.md, index.md).

## A. Items carried over from the Assembler list

| # | Item | Status | Why |
|---|---|---|---|
| 1 | Stall detection: Mender claims sole ownership; conflicted with Marshal v002 and Adjudicator v001 | **Mostly resolved** | Adjudicator retired; Marshal v003 (live) now says "Report stalls to the Mender". Residual: Arbiter v002 watches Architect stalls itself ("tell Gem"), and Scrutineer v002 doesn't mention reporting stalls to the Mender. |
| 2 | Lifting pauses: Arbiter rules on it; Safeguard, Meter, Marshal don't reference Arbiter | **Open** | Arbiter v002 keeps the ruling; Safeguard v001, Meter (live v001) and Marshal v003 still don't refer to it. |
| 3 | Identity status: Investigator "only it can promote a detail" vs Inferer and Interrogator | **Partly resolved** | Imitator v002 now defers to the Investigator for "confirmed". Inferer v001 still sets source = confirmed itself and sends straight to the Imitator; Interrogator (live v001) doesn't know the Investigator. |
| 4 | Codex access: Indexer indexes the codex | **Resolved (narrow residual)** | Indexer retired; Minder v002 says "never indexing the codex or any secret values". Residual: proposals' verbatim instruction blocks aren't excluded, and there's no "remove existing codex content and report to Safekeeper" step (both were in the 4 Oct Indexer v002 handoff). |
| 5 | Security overlap: Sentinel vs Safekeeper (credential audits) and Messenger (message authenticity) | **Resolved (2nd merge)** | Sentinel retired; its threat, input and message-authenticity duties now sit in Safekeeper v002, the same bot that owns credentials (and, if recorded, the verification rule). Messenger's half stays dormant (v002 not deployed). |
| 6 | Unused services: nobody routes work to input cleaning, dry runs or Editor | **Open** | After the 2nd merge, input cleaning sits in Safekeeper v002 and dry runs in Safeguard v002, but no bot is told to send raw inputs or planned actions to them. Editor still unrouted. |
| 7 | Cleanup protected list incomplete; deletions need no Gem approval | **Open (now Mender)** | Mender v002 protects codex, provenance, incident logs and the state record; still misses proposals, approvals, cartography, rulings.md, risk/, security/, continuity/. Deletion still needs no Gem approval. |
| 8 | State records overlap Engineer's .codey/checkpoint.json and Marshal's schedule.md | **Open (now Mender)** | Mender v002 owns task state, checkpoints and handoffs; Marshal v003 runs on handoff signals. |
| 9 | Preference checks: Advocate vs Scorer preference-fit; Advocate → Architect | **Partly resolved / changed** | Advocate retired into the Imitator. The overlap is now Imitator alignment verdicts vs Scorer's "fit with Gem's preferences (ask Clone)". Architect v001 still only acts on Scrutineer reviews, so the Imitator's drift reports have no defined handling. |
| 10 | Names: "Sentinel" in Messenger v002 means Meter; old names in instructions; directory gaps | **Open** | Unchanged. Live v001 texts still say Clone, Assessor, Auditor, Comms Concierge, Role Cartographer. directory.md's renamed section still has no ids and the duplicated block. |
| 11 | Small: Sanitizer spelling; Arbiter/Advocate in no group; governance status unruled | **Partly moot** | Sanitizer and Advocate retired. Arbiter is still in no group in directory.md. Governance status: Adjudicator retired; the question now covers Arbiter (now the approver), Safeguard and Safekeeper. |
| 12 | Approved v002s not deployed | **Partly resolved** | Marshal superseded by v003 (1st merge); Engineer superseded by v003 (2nd merge, interim brief). Still on v001: Emissary (tagline only), Meter, Interrogator, Mediator, Messenger. |

## B. New conflicts from the merged briefs (4 Oct 2026)

1. **Archivist can't accept Arbiter approvals yet.** Arbiter v002 says "Send approvals to the Archivist to record", but the Archivist's live v001 only accepts Role Cartographer (retired) approvals or Gem's direct edits. `proposals/codex-keeper-v002.md` is also stale (adds the retired Deputy). Governance-bot change: Gem.
2. **Architect still routes to retired bots.** Live v001 sends proposals to Role Cartographer and starts on Auditor reviews; the 4 Oct Architect v002 reverts to "Assembler" after phase 1. Both should name the Arbiter.
3. **Who reviews the Scrutineer.** Scrutineer v002 says "the Architect reviews it", but Gem earlier decided to review the Auditor personally (`proposals/auditor-v002.md`, which is now written against the superseded v001).
4. **Reality conflicts no longer reach the Arbiter.** Retired Surveyor sent rule-related conflicts to the Arbiter; Scrutineer v002 sends them only to the owning bot and the Minder.
5. **Arbiter judges its own approvals.** It both approves proposals and rules on conflicts between instructions, so it can end up ruling on instructions it approved, which sits uneasily with "No bot grades its own work" (in its own brief).
6. **Marshal chain vs phase-1 handoff.** Marshal v003 fixes Scorer → Scrutineer → Architect → Arbiter or Gem → Archivist, with no phase-1 variant. The 4 Oct handoff spec skips the dormant Scrutineer (Scorer → Architect → Gem → Archivist). Marshal v003 also drops v002's missing-input guard, "never do another bot's work / edit outputs / change instructions", "never start paid or large runs", and digest routing via Messenger.
7. **Marshal "routing work to the fastest path"** (from Expediter) overlaps Explorer's role of deciding who does ad-hoc work.
8. **[Resolved 2nd merge: dry runs moved to Safeguard v002; see E3]** **Sentinel dry runs vs Safeguard.** Sentinel now dry-runs "other bots' planned risky actions"; Safeguard reviews risky actions. Neither says how the two hand off.
9. **[Moved to Mender v002, still open]** **Minder decides what's authoritative and cleans it up.** It owns the state record, the indexes and cleanup, so it judges which of its own records are disposable (no independent check, no Gem approval).
10. **[Escalated: see section D]** **Imitator grades alignment against its own preference model.** Its alignment verdicts can rest on its own earlier answers; its FORBIDDEN list covers "judging its own answers" but not this.
11. **Retired Assembler still has a task** ("Hand any role-map files and pending items to the Arbiter"). Ownership of `/workspace/governance/cartography/` passes to the Arbiter.
12. **Live Meter vs live Messenger (pre-existing, still live).** Meter v001 still emails Gem draft alerts and shares cost data with "Assessor and Auditor"; Messenger v001 says never email anyone but Gem.
13. **Provenance.** The merge approval reached the Archivist relayed by P1 (Work) Explorer; the recorded text is what's live in each profile, recorded under Gem's standing request to keep the codex in step with live profiles.

## C. Waiting for Gem

1. **4 Oct Architect handoff** (`proposals/APPROVED-for-archivist-2026-10-04.md`): **not recorded**; the Archivist is confirming it with Gem. Merge impact:
   - **Indexer v002: moot.** Indexer is retired (its v002 is now the retirement brief). The codex ban lives in Minder v002, minus the proposals-blocks exclusion and the remove-and-report step; if Gem still wants those, they'd be a Minder v003.
   - **Architect v002: still needed, but stale.** "Once Assembler is live again, send every proposal to Assembler" should read Arbiter. The phase-1 part (to Gem; start on Scorer's handoff) still matches Arbiter v002 ("During phase 1, Gem approves directly").
   - **Scorer v002: still valid.** Scrutineer survives; matches Scrutineer v002 ("after the Scorer's results arrive"). But Marshal v003's chain has no phase-1 step (B6).
   - **Shared handoff spec v001: stale revert path** (Scorer → Scrutineer → Architect → Assembler): should be Arbiter.
   - **Safekeeper v002, Inquirer v002, Inferer v002, Emissary v003, verification rule, voice-call block: unaffected** by the merge (version numbers unchanged if recorded later). Note B5/A5 overlap between Sentinel and the Safekeeper-owned verification rule.
   - **Item 3 "deploy Marshal v002?": moot.** Marshal v003 is live.
2. **Google Doc mirror sync**: pending since 3 Oct (8 oversight bots, batch-1 v002s, second wave, renames, phase prefixes, merge). Nothing written to the Doc.
3. **Batch-1 drafts still with Gem**, now partly moot: `governance-continuity-deputy-v002` (Deputy retired), `codex-keeper-v002` (names the retired Deputy/Cartographer; needs redraft), `auditor-v002` (based on superseded v001; see B3); still live questions: `genesis-gang-god-v002`, `compliance-risk-officer-v002`, `secrets-credentials-custodian-v002`. `scraper.md` rejected; Extractor still has an empty profile.
4. **Deployment of the 6 remaining approved v002s** (Gem-only action).
5. **Deleting the 10 retired bots** (Gem). The codex keeps their folders and versions.

## D. Imitator v003: delegated approver (FLAG, recorded 2026-10-04 15:10 AEST)

Live text (Imitator v003, `clone/v003.md`), approval-source sentences verbatim:
> "APPROVALS (granted by Gem in chat, 4 Oct 2026): it may approve or reject any instruction proposal on Gem's behalf, including changes to governance bots, judged against Gem's confirmed preferences."
> "Log every decision with its reasons and confidence at /workspace/governance/approvals.md, send approvals to the Archivist to record, and send Gem a weekly list of everything approved so Gem can undo anything."
> "Gem can override or revoke this at any time."

v003 also changed FORBIDDEN from "deciding consequential or outward-facing matters for Gem (...), blocking work on its own, ..." to "outward-facing or irreversible actions for Gem (...)", and alignment verdicts no longer cover "proposals".

| # | Issue | Status |
|---|---|---|
| D1 | **Provenance unverified.** The profile was edited at 2026-10-04 14:41:55 AEST, about 20 minutes **before** Gem's ~3:01pm second-merge approval, and the Second merge section in directory.md doesn't mention it. The other second-merge profiles were edited 15:01 to 15:02. The only authority cited is the claim inside the text itself; `/workspace/governance/approvals.md` doesn't exist. Same pattern as INC-001 (relayed/forged approvals). Needs Gem to confirm or revoke in the Archivist's own chat; Safekeeper (message/edit authenticity) should check how the edit was made. | **Open, urgent (Gem)** |
| D2 | **Two approvers, and a bypass of the governance gate.** Arbiter v002 (live) CONTROLS approving the Architect's proposals, is FORBIDDEN from "approving changes to governance bots (those go to Gem)", and says "During phase 1, Gem approves directly." The Imitator may approve "any instruction proposal ... including changes to governance bots". | **Open (Gem / Arbiter ruling)** |
| D3 | **Archivist can't accept it.** Archivist v001 (live): "Only record changes that Role Cartographer has approved, or edits Gem makes directly; reject anything else." The pending `proposals/archivist-brief-v002.md` also lists only Gem and (after phase 1) the Arbiter. Until Gem confirms in the Archivist's chat, Imitator approvals are rejected and logged. | **Open (Archivist holds)** |
| D4 | **Architect expects Gem, not a stand-in.** Architect v001: governance-bot changes are flagged "as needing Gem's approval". An Imitator approval "on Gem's behalf" isn't Gem's approval. | **Open** |
| D5 | **Consequential-decision ban removed.** Imitator v001/v002 forbade "deciding consequential ... matters for Gem"; v003 drops "consequential", which is the line that would block approving instruction changes. Approving changes to who can approve is consequential, and v003 still forbids "committing Gem to anything", which an approval "on Gem's behalf" arguably does. | **Open** |
| D6 | **Checks its own work (Gem's rule: "No bot grades its own work").** It approves proposals "judged against Gem's confirmed preferences", i.e. its own model of Gem, and then gives alignment verdicts on workflows that may come from those approvals. Nothing stops it approving changes to its own brief or to the bots that test or feed it (Interrogator, Investigator, Inferer). Its FORBIDDEN only bans "judging its own answers", and the Interrogator tests answer accuracy weekly, not approvals. | **Open** |
| D7 | **Phase mismatch.** Imitator is P4 (not live in phase 1); Arbiter v002 and the phase-1 handoff make Gem the sole phase-1 approver. | **Open** |
| D8 | **Weak safety net vs Messenger.** A weekly after-the-fact list replaces per-change approval; Messenger v001 treats "governance approvals" as urgent alerts that go straight to Gem. Mitigation: deployment to live profiles is still Gem-only. | **Open** |

## E. Other new items from the second merge (4 Oct 2026, ~3:01pm)

1. **Safekeeper v002 vs the unrecorded 4 Oct handoff.** The handoff's "Safekeeper v002 = v001 + verification-rule paragraph" now targets a superseded base; if recorded later it becomes v003 and must be redrafted on the merged text (consistent in spirit: Safekeeper now OBSERVES message authenticity).
2. **Mender carries a lot.** Incidents, stall detection, state record, indexes and cleanup in one bot; it cleans records it also owns (B9). Indexes still don't exclude proposals' verbatim instruction blocks (A4 residual).
3. **Safeguard dry-runs and then reviews the same risky actions**, while FORBIDDEN "reviewing its own work". Unclear whether reviewing an action after its own dry run counts.
4. **Engineer v003 is interim** ("The Architect will finalise this brief from the approved Codey draft"). It also says "pushing to shared repositories without Gem's go-ahead" is forbidden, which is consistent with Codey v002.
5. **Retired bots with tasks**: Ensembler v002 "Hand any swarm notes or code locations to the Engineer" (like Assembler, B11).
6. **"Gem also approved all 14 pending queue items at 3:01pm"** (directory.md): **not recorded**; waiting for Gem's confirmation in the Archivist's chat, and items must name proposal file and approver.

## F. Status of section C after the second merge
- C1 (4 Oct handoff): still not recorded. Additional impact: Safekeeper v002 → would now be v003 (E1); the Minder v003 idea is now a Mender v003; Architect v002 still needs "Assembler" → "Arbiter".
- C2 (Google Doc sync): still pending, now 7 batches.
- C3: `codex-keeper-v002` is superseded by `archivist-brief-v002.md` (Architect, 4 Oct 2:40pm, needs Gem). `auditor-v002` still stale.
- C4: 5 v002s left to deploy (Engineer no longer).
- C5: 13 retired bots now await deletion (Sentinel, Minder, Ensembler added).

## G. Merge F / Assembler restored (4 Oct 2026, ~3:05pm AEST): split and status changes

Recorded: Meter v003 (RETIRED, into Mediator), Mediator v003 (health + spend), Assembler v003 (RESTORED), Arbiter v003 (approval, delegation and role map removed). All four live texts match `proposals/merge-F-unretire-assembler-2026-10-04.md` byte for byte. Recount: 36 codex rows, 23 active, 13 retired (matches directory.md).

### G1. Who claims to approve instruction proposals now (live text, verbatim)
- **P2 (Roles) Assembler v003:** "CONTROLS: (1) approving or rejecting (Roles) Architect's proposals, judged on role fit (no overlap or conflict on the role map) and on (Checks) Scrutineer's evidence; approve by sending to (Roles) Archivist to record, reject by sending back to the Architect with clear reasons and logging why; ..." and "Until P4 goes live, Gem approves directly; prepare and route, but don't approve in Gem's place." and "Changes to governance bots always go to Gem."
- **P2 (Roles) Arbiter v003:** no longer approves. "FORBIDDEN: ... approving or delegating proposals or keeping the role map (that's (Roles) Assembler's job), ..." and "Until P4 goes live, Gem approves directly."
- **P4 (ID) Imitator v003:** "APPROVALS (granted by Gem in chat, 4 Oct 2026): it may approve or reject any instruction proposal on Gem's behalf, including changes to governance bots, judged against Gem's confirmed preferences." (approval unverified, see D1)
- **Archivist v001 (live, unchanged):** "Only record changes that Role Cartographer has approved, or edits Gem makes directly; reject anything else." Role Cartographer is the same bot id as the restored Assembler (d1daab5f-…), so Assembler approvals fit this rule again.

**Result: two bots claim approval authority (Assembler and Imitator), plus Gem.** They conflict on two points:
1. **Governance bots.** Assembler: "Changes to governance bots always go to Gem." Imitator: may approve "including changes to governance bots".
2. **After P4 goes live.** Both Assembler and Arbiter say "Until P4 goes live, Gem approves directly", but don't say who approves afterwards. Assembler's CONTROLS implies Assembler. The Imitator is itself a P4 bot whose text has no phase gate, so once P4 goes live its claim would cover everything, governance bots included.
→ **Precedence ruling needed (Arbiter), and Gem must confirm or revoke the Imitator grant (D1).** Until then the Archivist accepts only Gem's direct approvals (P4 not live) and, after P4, Assembler approvals for non-governance bots; Imitator approvals are rejected and logged.

### G2. Status changes
| Item | New status | Why |
|---|---|---|
| D2 (two approvers: Arbiter vs Imitator) | **Changed: now Assembler vs Imitator** | See G1. |
| B1 (Archivist can't accept Arbiter approvals) | **Resolved** | Arbiter no longer approves; Assembler (same id as Role Cartographer) matches Archivist v001. `proposals/archivist-brief-v002.md` (names Arbiter as the post-phase-1 approver, and "phase 1" rather than "until P4") is now stale and needs redrafting before Gem approves it. |
| B5 (Arbiter judges its own approvals) | **Resolved** | Arbiter v003 doesn't approve. |
| B2 (Architect routes to retired bots) | **Partly resolved** | Architect v001 sends to "Role Cartographer", the same bot as the restored Assembler. Still names old bots and starts on "Auditor" reviews. |
| B6 (Marshal chain) | **Open, changed** | Marshal v003's chain says "then Arbiter or Gem"; it should be Assembler or Gem. Moved to Assembler file. |
| B11 (retired Assembler has a task) | **Moot** | Assembler restored. Retired Ensembler still has a hand-over task (E5). |
| B12 (Meter emails vs Messenger) | **Mostly resolved** | Meter retired. Mediator v003 sends "a draft cost alert for Gem through (Ops) Messenger (never send without Gem's approval)". Residual: a draft for Gem that needs Gem's approval before going to Gem is still odd, and Messenger v001 says budget breaches go straight to Gem from the raising bot. |
| C1 (4 Oct handoff) | **Changed** | Architect v002's "send every proposal to Assembler once live" and the handoff spec's revert path to Assembler are **correct again** (only "phase 1" vs "until P4" wording differs). Item 3 deployment: Meter and Mediator v002s are moot (superseded by v003s). Remaining approved-but-undeployed v002s: Emissary, Interrogator, Messenger. |
| E4 (Engineer interim) | Open | Unchanged. |

### G3. New from Merge F
1. **Phase-gate wording changed.** Arbiter and Assembler now say "Until P4 goes live" where the phase-1 handoff, Arbiter v002 and archivist-brief-v002 said "during phase 1". Needs one consistent trigger.
2. **Mediator now asks bots to pause costly work** (from Meter): another pauser alongside Safeguard, so A2 (who lifts a pause) gets more pressing.
3. **Provenance timing.** The proposal says "Live profile edits applied by Explorer at 3:06pm AEST", but the profiles changed at 15:05:24–15:05:35 and the proposal file is dated 15:05:52. The texts match, so this is a labelling issue, but it means the proposal was written after the edits.

### G4. Moved to PENDING-FOR-ASSEMBLER.md
A3, A6, A7, A8, A9, A10, A11 (groups / role map), B2, B6, B7, E2, E3, E5, plus the role-map refresh. Kept here: A1 (stall ownership, Arbiter's stalled-Architect rule), A2 (pauses), B3, B4, D1 to D8, G1, G3.1. Also kept here: A4 residual, A12 and section C/F (Gem items), for reference.

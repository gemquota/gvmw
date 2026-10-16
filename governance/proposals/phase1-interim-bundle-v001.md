# Phase-1 interim bundle v001 (APPROVED by Gem, 4 Oct 2026, whole bundle)

| Field | Value |
|---|---|
| Drafted by | (Roles) Architect, 3 Oct 2026, 11:40am (AEST, UTC+10) |
| Approver | **Gem** (every item touches governance roles or the codex access policy, and (Roles) Assembler is dormant in phase 1) |
| Approved by | Approved by Gem directly, 4 Oct 2026 (AEST, UTC+10). Phase 1: (Roles) Assembler dormant, so Gem approved in place of Assembler. |
| After approval | (Roles) Archivist records items 1 and 2 as new versions. Item 3 needs no recording (already recorded); deployment is parked (see below). |
| Changelog | 3 Oct 2026, 11:40am: drafted. 4 Oct 2026: Gem approved; deployment note added to item 3. 4 Oct 2026, 2:35pm: **Correction C-1 (needs Gem):** after the merge, Assembler is replaced by (Roles) Arbiter in item 1; item 2 (Indexer) withdrawn; item 3 updated for Marshal v003. |
| Note | (Roles) Assembler was **retired** in Gem's merge (4 Oct 2026, 2:26pm); its approval duties passed to (Roles) Arbiter. Earlier lines saying "dormant" are kept as written at the time. |

## Item 1: Interim approval flow (Architect and Scorer)

During phase 1: **Scorer → Architect → Gem (approval) → Archivist (records).** After phase 1, approvals route through **(Roles) Arbiter** (corrected from Assembler, which is retired; see C-1 below). It matches `handoff-phase1-v001.md`.

### (Roles) Architect (51af1200…), instruction-architect v001 → v002
| | Sentence |
|---|---|
| **Before** | "Send every proposal to Role Cartographer for approval, never to Codex Keeper directly." |
| **After (approved 4 Oct, superseded by C-1)** | ~~"During phase 1, while (Roles) Assembler is dormant, send every proposal to Gem for approval; once Assembler is live again, send every proposal to Assembler instead; never send proposals to (Roles) Archivist directly."~~ |
| **After (C-1, needs Gem)** | "During phase 1, send every proposal to Gem for approval; after phase 1, send every proposal to (Roles) Arbiter for approval, except changes to governance bots, which always go to Gem; never send proposals to (Roles) Archivist directly." |

Linked trigger change, needed so the Architect still has a starting point while Scrutineer is dormant:
| | Sentence |
|---|---|
| **Before** | "Whenever the Auditor sends a performance review, propose improvements as a complete rewritten instruction set using the template sections Purpose, Scope, Rules, Relationships and Limits." |
| **After** | "During phase 1, start on (Checks) Scorer's priority handoff and only if today's dated assessment file exists, otherwise defer; once (Checks) Scrutineer is live, start whenever it sends a performance review. Either way, propose improvements as a complete rewritten instruction set using the template sections Purpose, Scope, Rules, Relationships and Limits." |

### Correction C-1 to the Architect v002 text
**Correction C-1, 4 Oct 2026 (after Gem's merge at 2:26pm): NEEDS GEM'S APPROVAL.** This is a governance-bot change, so the Arbiter can't approve it (Arbiter v002 FORBIDDEN; ruling R-002).

| # | Before (in the approved Architect v002) | After (C-1) |
|---|---|---|
| 1 | "During phase 1, while (Roles) Assembler is dormant, send every proposal to Gem for approval; once Assembler is live again, send every proposal to Assembler instead; never send proposals to (Roles) Archivist directly." | "During phase 1, send every proposal to Gem for approval; after phase 1, send every proposal to (Roles) Arbiter for approval, except changes to governance bots, which always go to Gem; never send proposals to (Roles) Archivist directly." |
| 2 | "If Role Cartographer rejects a proposal, revise it using the reasons given, or say you disagree so it can escalate to Gem." (unchanged from v001) | "If (Roles) Arbiter rejects a proposal, revise it using the reasons given, or say you disagree so it can escalate to Gem." |

Phase 1 stays **Gem-direct**, which matches Arbiter v002: "During phase 1, Gem approves directly". The trigger sentence (Scorer's handoff in phase 1, Scrutineer's reviews later) is unchanged. Other old names left in Architect v001 ("Auditor", "Assessor", "Clone", "the five governance bots") aren't routing. R-002 already reads them as Scrutineer, Scorer and so on, and they're left for the Architect's next full rewrite.

### (Checks) Scorer (050a12c9…), assessor v001 → v002
| | Sentence |
|---|---|
| **Before** | "Send the daily results to the Auditor." |
| **After** | "During phase 1, while (Checks) Scrutineer is dormant, write the daily results to /workspace/governance/assessments/YYYY-MM-DD.md and send (Roles) Architect a priority handoff with the file path; once Scrutineer is live again, send that handoff to Scrutineer instead." |

(Scorer v002 is unaffected by the merge: Scrutineer survives.)

Everything else in both instruction sets is unchanged. Both are governance roles, so Gem's approval is required either way.

## Item 2: WITHDRAWN (4 Oct 2026 merge)

~~Amend (ID) Indexer's brief to exclude the codex from all indexes.~~ **Withdrawn:** (ID) Indexer was retired in Gem's 4 Oct merge, and its duties passed to (Ops) Minder. **The core rule is kept:** Minder v002 CONTROLS (2) already says it keeps the search indexes "never indexing the codex or any secret values". So nothing is recorded for the Indexer.

Two refinements from the withdrawn item are **not** in Minder v002 and would need a Minder v003 if Gem still wants them (see the questions for Gem below):
- also excluding the verbatim instruction blocks in `/workspace/governance/proposals/`;
- "if any codex content is already in an index, remove it and report that to (Checks) Safekeeper."

## Item 3: Getting the approved v002s onto the live bots

**Correction to the premise:** these seven v002s are **already recorded** by the Archivist. Each has a `v002.md` and a CHANGELOG row approved by Role Cartographer in batch 1 (`approvals/2026-10-03-batch1-review.md`). What's missing is **deployment**: `codex/_tools/verify.py` reports each live profile as "still = v001: approved version not yet deployed". So no new recording is needed. The open step is getting each v002's verbatim text onto the bot's live profile. The Archivist's instructions only cover recording, and no bot is allowed to edit profiles.

| Bot (new name) | Old name / folder | Bot id | Recorded | Proposal file |
|---|---|---|---|---|
| (Work) Engineer | Codey / `codey/` | f8e3fdc6-ee60-410e-bdb7-d437fc1500d1 | v002 ✔ | `proposals/codey.md` |
| (Work) Emissary | Grok Bot / `grok-bot/` | 28cf987d-ee94-4839-a6d3-33c04a11b9d6 | v002 ✔ | `proposals/grok-bot.md` |
| (Ops) Meter | Cost & Budget Sentinel / `cost-budget-sentinel/` | f8b83b15-0ea1-4f99-9550-c3b8607ba999 | v002 ✔ | `proposals/cost-budget-sentinel-v002.md` |
| (Ops) Marshal | Orchestration Conductor / `orchestration-conductor/` | f3810109-17a5-427f-9148-d58f645658e3 | v002 ✔ | `proposals/orchestration-conductor-v002.md` |
| (ID) Interrogator | Clone Accuracy Validator / `clone-accuracy-validator/` | d3191aa8-3ad6-4763-b4e4-c7c648acc9ba | v002 ✔ | `proposals/clone-accuracy-validator-v002.md` |
| (Ops) Mediator | Connector Steward / `connector-steward/` | 90f9eb20-ff8f-456b-b94f-cc11bb33fc29 | v002 ✔ | `proposals/connector-steward-v002.md` |
| (Ops) Messenger | Comms Concierge / `comms-concierge/` | 5e47d344-1369-423a-b072-2e5277934022 | v002 ✔ | `proposals/comms-concierge-v002.md` |

**Asks for Gem:**
1. Confirm these seven should go live (they were approved under the old flow, before the renames and phase 1).
2. Decide who applies them: Gem directly, or a named bot given one-off permission to update these seven profiles with the exact recorded text.
3. Note that the v002 texts use the **old names** (Codey, Comms Concierge, Role Cartographer and so on) and assume the old 13-bot setup. For example, Marshal v002 has the Governance Continuity Deputy using its due times, and Messenger v002's urgent list predates Mender, Safeguard and the other new names. Options: (a) deploy as they are now and refresh the names in a v003, or (b) the Architect redrafts v003s with phase-1 names first. **Recommended: (a)**, because the rules are still right and it stops these bots running on the weaker v001.

### Deployment status (4 Oct 2026, after Gem's approval)
- **Deploying approved versions to live profiles is parked.** Most of these bots are dormant non-P1 bots in phase 1, and deployment is **a Gem-only action**: no bot may edit profiles, the Archivist included. Recording in the codex is not deployment.
- **The one P1 exception is (Work) Emissary, at v003.** v003 is v002 plus the VOICE CALLS block from `voice-call-messaging-v001.md`. Deploy v003 straight away rather than v002, so the profile changes only once. Gem does this.
- ⚠ **Check for Gem:** the live profile names Emissary "P6 (Work) Emissary", and `schedule.md` doesn't list Emissary among the live phase-1 bots.
- **Update after the merge:** Marshal v002 is moot. Marshal's merged **v003 is live** (recorded by the Archivist). So the open deployments are Engineer, Emissary, Meter, Interrogator, Mediator and Messenger (still v001).
- Everyone else in the table above stays on v001 until their phase wakes them up. At that point Gem deploys the latest recorded version (refreshing names in a v003 where useful, as in option (a)).

## Approval summary
| Item | Change | Approved |
|---|---|---|
| 1 | Architect v002 and Scorer v002: phase-1 flow via Gem, then the Arbiter after phase 1 | Gem, 4 Oct 2026; **C-1 correction (Assembler → Arbiter) needs Gem** |
| 2 | ~~Indexer v002~~: withdrawn (Indexer retired; Minder v002 already bans indexing the codex) | n/a |
| 3 | 7 v002s already recorded. Deployment parked (Gem-only); Emissary v003 is the exception | Gem (approved 4 Oct; deployment is Gem's own action) |

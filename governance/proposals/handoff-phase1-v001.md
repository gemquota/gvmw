# Phase-1 handoff spec v001 (APPROVED by Gem, 4 Oct 2026)

| Field | Value |
|---|---|
| Drafted by | (Roles) Architect (51af1200-ca1a-45ff-8350-848091e00f96) |
| Date | 3 Oct 2026, 11:30am (AEST, UTC+10) |
| Replaces | The pending "Handoff changes for Assessor/Auditor" item in `schedule.md` (written for the old Assessor → Auditor → Architect chain) |
| Based on | `/workspace/governance/schedule.md` (phase 1, set up by (Ops) Marshal, 3 Oct 11:20am) |
| Approved by | Approved by Gem directly, 4 Oct 2026 (AEST, UTC+10). Phase 1: (Roles) Assembler dormant, so Gem approved in place of Assembler. |
| Status | Approved. For (Roles) Archivist to record; (Ops) Marshal to reflect in `schedule.md`. |
| Changelog | 3 Oct 2026, 11:30am: drafted. 4 Oct 2026: Gem approved. 4 Oct 2026, 2:35pm: **Correction C-2 (needs Gem):** retired Assembler → (Roles) Arbiter as the approver after phase 1 (ruling R-002). |

## The chain (weekdays)

```
(Checks) Scorer ──priority handoff + file path──▶ (Roles) Architect ──proposals──▶ approver ──approved──▶ (Roles) Archivist
   7:45am                                          starts on the handoff          Gem (phase 1)          records vNNN
                                                                                  Arbiter (after phase 1)
          (Ops) Marshal 10:20am check ──deferrals / stalls──▶ (Ops) Mender 10:50am
```

(Checks) Scrutineer's audit step is **skipped** while Scrutineer is dormant.

## Step by step

### 1. (Checks) Scorer
- **CONTROLS:** today's assessment file, `/workspace/governance/assessments/YYYY-MM-DD.md` (Brisbane date).
- **OBSERVES:** recent work from the live phase-1 bots.
- **Runs:** its own routine, weekdays at 7:45am.
- **Hands off:** once the file is written, it sends (Roles) Architect a **priority message containing the full file path**. While Scrutineer is dormant it sends nothing to Scrutineer.
- **FORBIDDEN:** changing other bots' work or instructions, and backdating or overwriting an earlier day's file.

### 2. (Roles) Architect
- **Starts on:** the Scorer's handoff, **not a clock time**.
- **Input check:** it runs only if the file at the handoff path **exists and carries today's Brisbane date** (in both the file name and the heading). A dated file is a signal, not proof of who wrote it. If anything looks wrong (a missing handoff, a file without a handoff, the wrong date, an unexpected sender), it checks 1:1 with the Scorer before acting, as set out in `agent-message-verification-rule-v001.md`.
- **If the input is missing or wrong:** it **defers** and doesn't run without input. The deferral is picked up at (Ops) Marshal's 10:20am check: the Marshal logs it in `schedule.md` and reports the stall to (Ops) Mender, the single owner of stall detection. The Architect doesn't chase the Scorer on a timer itself.
- **CONTROLS:** proposals in `/workspace/governance/proposals/`.
- **Hands off:** proposals, if any, go to the approver.
  - **Phase 1:** Gem, directly (Arbiter v002: "During phase 1, Gem approves directly").
  - **After phase 1:** (Roles) Arbiter.
  - Either way, anything touching a governance bot goes to **Gem** (the Arbiter can't approve governance-bot changes).
- **FORBIDDEN:** recording in the codex, approving its own proposals, checking bots' work itself, and running on a clock time without the handoff.

### 3. Approval
- The approver approves, or rejects with reasons. Rejections go back to the Architect to revise, or the Architect says it disagrees and the matter goes to Gem.

### 4. (Roles) Archivist
- **Starts on:** an approval (from Gem in phase 1, or (Roles) Arbiter after phase 1, governance bots always from Gem) or a direct edit from Gem.
- **CONTROLS:** `/workspace/governance/codex/<bot>/vNNN.md` and each bot's CHANGELOG.
- **FORBIDDEN:** recording anything without a valid approval.

### Checks around the chain
- **(Ops) Marshal, 10:20am:** checks that today's assessment file exists, that the handoff happened and that the Architect ran or deferred. It updates `schedule.md`, logs deferrals and reports stalls to Mender.
- **(Ops) Mender, 10:50am:** owns stall detection and recovery. It logs to `/workspace/governance/incidents/log.md` and tells the owners of the stalled step.

## When Scrutineer comes live (reverting to the full chain)

The chain becomes **Scorer → Scrutineer → Architect**:
1. The Scorer's priority handoff (with the file path) goes to **(Checks) Scrutineer** instead of the Architect.
2. Scrutineer starts on that handoff (not its parked 11:45am fallback), writes its reviews, then sends the Architect a priority handoff with the review path(s).
3. The Architect starts on **Scrutineer's** handoff. Its input check becomes: today's reviews exist (with today's assessment file behind them). The rest of its rules stay the same.
4. The Marshal's 10:20am check moves to after Scrutineer's expected finish. The Marshal sets the new time when it switches Scrutineer on.
5. Before switching on, the parked 11:45am Scrutineer fallback routine is either removed or turned into a guard that defers when there's no handoff.
6. Approvals: after phase 1 the full chain is **Scorer → Scrutineer → Architect → Arbiter → Archivist**, with governance-bot changes going to Gem. (Phase 1 ending and Scrutineer coming live may happen at different times. The approver follows the phase; the Scrutineer step follows Scrutineer.)

Switching back is a change to the Scorer's, Scrutineer's and Architect's instructions, so it goes through the normal flow and needs Gem's approval (all three are governance roles).

## What changed from the earlier draft, and why
- **Old chain Assessor → Auditor → Architect, now Scorer → Architect.** Phase 1 keeps only 8 bots live, and Scrutineer (the Auditor) is dormant. Leaving it in the chain would stall every day.
- **The Architect starts on a handoff, not reviews.** v001 of the Architect's instructions triggers "whenever the Auditor sends a performance review". In phase 1 that never happens, so the trigger becomes the Scorer's handoff (the instruction text change is in the interim bundle).
- **An explicit "today's file must exist" check, with defer-and-log.** This fixes the audit's finding that a downstream run could fire on a fixed clock time with no input.
- **One stall owner.** Deferrals go via the Marshal to Mender (Mender v001 says it's the single owner of stall detection). This drops the earlier draft's idea of the Governance Continuity Deputy (now Adjudicator) timing stalls itself, which overlapped with Mender.
- **Approver in phase 1 is Gem.** Assembler was dormant, so proposals would otherwise have queued forever. *(C-2: Assembler has since been retired; the approver after phase 1 is (Roles) Arbiter. See `codex/PENDING-FOR-ARBITER.md` C1 and ruling R-002.)*
- **Trust check on the handoff.** The computer is shared and the "Set 5" message on 3 Oct shows messages can't be taken at face value. The Architect follows the verification rule.

## Correction C-2 (4 Oct 2026, 2:35pm): NEEDS GEM'S APPROVAL
Governance change (the approval route of the Architect and Archivist), so Gem approves, not the Arbiter (R-002).

| # | Where | Before | After |
|---|---|---|---|
| 1 | Chain diagram | `Assembler (later)` | `Arbiter (after phase 1)` |
| 2 | §2 Hands off | "**Phase 1:** Gem, because (Roles) Assembler is dormant (pending Gem's approval of the interim bundle)." / "**Once Assembler is live:** (Roles) Assembler." / "Either way, anything touching a governance bot is **flagged for Gem**." | "**Phase 1:** Gem, directly (Arbiter v002: "During phase 1, Gem approves directly")." / "**After phase 1:** (Roles) Arbiter." / "Either way, anything touching a governance bot goes to **Gem** (the Arbiter can't approve governance-bot changes)." |
| 3 | §4 Archivist, Starts on | "an approval (from Gem in phase 1, or Assembler later) or a direct edit from Gem." | "an approval (from Gem in phase 1, or (Roles) Arbiter after phase 1, governance bots always from Gem) or a direct edit from Gem." |
| 4 | Revert section | (no approver step) | New step 6: full chain **Scorer → Scrutineer → Architect → Arbiter → Archivist**, governance-bot changes to Gem; the approver follows the phase, the Scrutineer step follows Scrutineer. |
| 5 | "What changed" note | "Assembler is dormant, so proposals would otherwise queue forever (see `codex/PENDING-FOR-ASSEMBLER.md`)." | Same, plus: "Assembler has since been retired; the approver after phase 1 is (Roles) Arbiter." |

**Not changed here:** Marshal v003's live chain (Scorer → Scrutineer → Architect → Arbiter or Gem → Archivist) has no phase-1 variant that skips the dormant Scrutineer (PENDING-FOR-ARBITER B6). That's a Marshal change, so it's listed as a question for Gem rather than fixed here.

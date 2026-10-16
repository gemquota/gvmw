# Phase-gate handoff spec — final v001 (shared; live-Scrutineer chain)

| Field | Value |
|---|---|
| Record as | `codex/_shared/handoff-phase1/v001.md` (a shared governance document, not any one bot's instructions) |
| Approver | Approved in principle by Gem, 3:01pm 4 Oct 2026 (relayed by P1 (Work) Explorer; relay unverified per R-008). C-2, Merge F and the live-Scrutineer chain are reconciliations beyond the approved draft. |
| Status | **Reconciled text NEEDS GEM'S DIRECT APPROVAL** |
| Sources merged | `handoff-phase1-v001.md`, correction C-2, `merge-F-unretire-assembler-2026-10-04.md`, rulings R-002/R-005/R-006, `schedule.md`, Scrutineer baseline R3/R7/M1-M5 |

## Reconciliation (what changed, and why)
- **Live Scrutineer (R3/R7):** the Scrutineer is live (P2, since 4 Oct 3:12pm), so the chain is the **full chain now** — the "Scrutineer dormant" variant (Scorer → Architect) is removed.
- **Merge F / R-005:** the approver is Gem **until P4 goes live**, then the restored **(Roles) Assembler** for non-governance bots; governance-bot changes always to Gem; the Arbiter is **not** an approval step.
- **R-006 (stall ownership):** the **(Ops) Mender** owns detecting and logging every stall (the Architect's included); the Marshal and the Arbiter report stalls to the Mender, and the Arbiter escalates an overdue Architect stall to Gem. No bot drafts in the Architect's place.
- Matches `schedule.md` (steps 1–5) as written on 4 Oct 3:11pm.

## The chain (weekdays)
```
Scorer --assessments/YYYY-MM-DD.md + path--> Scrutineer --reviews/YYYY-MM-DD.md + path--> Architect --proposal--> approver --approved--> Archivist (records vNNN)
  approver = Gem until P4 goes live; the (Roles) Assembler after P4 (non-governance only); governance-bot changes always to Gem.
  The (Roles) Arbiter rules only on precedence conflicts and is not an approval step.
  Marshal 10:20am chain check --deferrals/stalls--> Mender (owns stall detection) 10:50am
```

## Step by step
1. **(Checks) Scorer** (weekdays) writes `/workspace/governance/assessments/YYYY-MM-DD.md` (Brisbane date) and sends the **Scrutineer** a priority handoff with the full path.
2. **(Checks) Scrutineer** starts on that handoff, writes `/workspace/governance/reviews/YYYY-MM-DD.md`, and sends the **Architect** a priority handoff with the review path. Its 11:45am backup run skips if today's reviews exist and tells the Marshal if the Scorer's file is missing.
3. **(Roles) Architect** starts on the Scrutineer's done signal (not a clock time). It runs only if today's dated reviews file exists; if anything is off (missing handoff, wrong date, unexpected sender) it checks 1:1 with the Scrutineer per the message-verification rule. If the input is missing/wrong it **defers**; the Marshal's 10:20am check logs it and reports the stall to the **Mender**. Proposals go to the approver: **Gem until P4 goes live, the Assembler after P4; governance-bot changes always to Gem.**
4. **Approval.** The approver approves, or rejects with reasons back to the Architect (which revises or escalates its disagreement to Gem).
5. **(Roles) Archivist** records on a valid approval (Gem until P4; the Assembler after P4; governance bots always from Gem; a relayed approval counts only after direct confirmation with Gem, R-008) or a direct Gem edit.

## Stalls (R-006)
The **Mender** owns detecting and logging every stall. The Marshal reports chain deferrals/stalls to the Mender; the Arbiter, when it sees an Architect stall past its threshold (24h, or 4h for urgent), reports the stall to the Mender and escalates to Gem. No bot drafts in the Architect's place.

## Note for Gem (Marshal, M1/M3)
The live **Marshal v003** chain still reads "then Arbiter or Gem, then Archivist" and names the retired Meter as budget owner. Under Merge F the post-P4 approver is the **Assembler** and the Arbiter is not an approval step (as `schedule.md` already states). Marshal v003 needs a matching instruction update — that is a **Marshal change** for the Architect to draft and Gem to approve, not fixed in this spec.

# (Ops) Mender — delta (stall ownership, R-006) — NEEDS GEM'S DIRECT APPROVAL

| Field | Value |
|---|---|
| Bot | P1 (Ops) Mender |
| Bot id | c8401a53-136d-45f3-9e2d-e423ccdd08ac |
| Codex folder | `mender/` (current live: v002 merged brief) |
| Scope of this delta | One clarification from ruling **R-006** (stall ownership). The Mender has no full reconciled final in this batch; this is a short delta for the Architect to fold into a Mender v003 when Gem asks. |
| Approver | **NEEDS GEM'S DIRECT APPROVAL** (governance/ops change; Gem approves until P4) |

## Change (R-006)
The Mender's live v002 already says it is "the single owner of stall detection" and that "the Marshal and Scrutineer report stalls to it". R-006 adds the Arbiter and the Architect explicitly:
- The **Mender owns detecting and logging every stall, the Architect's included.**
- The **Marshal and the Arbiter report stalls to the Mender.** The Arbiter escalates an overdue **Architect** stall to Gem; it never drafts in the Architect's place.
- Suggested sentence to add to the FORBIDDEN/relationships area: "The Marshal, the Scrutineer and the Arbiter report stalls to you; you detect and log every stall, including the Architect's, and coordinate recovery; you never approve or draft instructions."

## Out of this delta (other bots / Gem)
- Mender baseline gaps N1–N7 (missing `state/`, `index/`, playbooks; `incidents/log.md` owner still "Auditor"; INC-001 Open/Resolved contradiction; incomplete protected list) are the **Mender's own** fixes, not the Architect's.

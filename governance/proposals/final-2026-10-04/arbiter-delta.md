# (Roles) Arbiter — delta (stall ownership, R-006) — NEEDS GEM'S DIRECT APPROVAL

| Field | Value |
|---|---|
| Bot | P2 (Roles) Arbiter |
| Bot id | 2133048d-5ab9-4809-806c-218decdff8e6 |
| Codex folder | `arbiter/` (current live: v003, Merge F) |
| Scope of this delta | One clarification from ruling **R-006**. The Arbiter's live v003 is otherwise current (precedence rulings only; no approvals). This is a short delta for a future v004. |
| Approver | **NEEDS GEM'S DIRECT APPROVAL** (governance bot; Gem approves) |

## Change (R-006)
Arbiter v003 says "If (Roles) Architect stalls for more than 24 hours (4 for urgent items), tell Gem." R-006 keeps this but makes the Mender the stall owner:
- When the Arbiter sees an Architect stall past the threshold, it **reports the stall to the (Ops) Mender and escalates to Gem**; the **Mender owns stall detection**. The Arbiter **never drafts in the Architect's place.**
- Suggested wording: "If the (Roles) Architect stalls past 24 hours (4 for urgent items), report the stall to the (Ops) Mender, which owns stall detection, and escalate to Gem; never draft in the Architect's place."

## Note
Arbiter self-review concern (Scrutineer B5 / earlier B5) is **largely resolved**: under Merge F the Arbiter no longer approves anything, so it cannot rule on instructions it approved. Residual items (pause-lifting link from Safeguard/Marshal; Arbiter in no group) are the owning bots' / Gem's.

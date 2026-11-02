# Imitator-approver follow-ups — 2026-10-04 — NEEDS GEM'S DIRECT APPROVAL

Style: bare bot names, Australian English, plain.

## Why
Archivist recorded the 12 Architect finals (Gem confirmed directly in Archivist's chat 4 Oct 5:45–5:46pm AEST). Gem also confirmed directly to Archivist (Arbiter ruling **R-004 update, 5:44pm**) that **Imitator may approve instruction changes on Gem's behalf, governance bots included.** These follow-ups update the approver-side bots so the codex stops treating Imitator approvals as "recommendations only / unverified". Every file is based on the **recorded** codex text, with the **correct next version number**, and is **NEEDS GEM'S DIRECT APPROVAL** (all are governance bots or benefit the drafter).

## Two reconciliations baked into every file
- **Phase gate (Gem's 2:55pm direction).** Gem approves directly until P4; proposals route to Imitator only **once P4 goes live**. Imitator is currently **dormant**. Wording used everywhere: **"Gem, or Imitator once P4 goes live".**
- **No self-checking carve-out (Gem's principle).** Imitator must **never** approve changes to its own instructions, or to Interrogator, Investigator or any bot that checks Imitator — those go to Gem. Added everywhere the exception appears; flagged as a judgement call for Gem (carve-out scope).

## Files and versions
| File | Bot | Recorded now | This proposal | One-line summary |
|---|---|---|---|---|
| `archivist-v003.md` | P1 (Roles) Archivist | `codex-keeper` v002 | **v003** | Accept Imitator approvals (once P4) as Gem's delegated authority; drop "recommendations only"; confirm each Imitator approval 1:1 and with Gem per R-004. |
| `architect-v003.md` | P1 (Roles) Architect | `instruction-architect` v002 | **v003** | List Imitator as an approver — non-governance to Assembler or Imitator, governance to Gem or Imitator, once P4 — with the self-check carve-out to Gem. |
| `explorer-v003.md` | P1 (Work) Explorer | `genesis-gang-god` v002 | **v003** | Imitator no longer limited to preference questions — may approve instruction changes once P4; keeps the "never for outward-facing/consequential decisions" limit. |
| `assembler-v004.md` | P2 (Roles) Assembler | `role-cartographer` v003 | **v004** | Governance-bot changes go to "Gem, or Imitator once P4 goes live"; Assembler itself approves non-governance only; self-check carve-out to Gem. |

Imitator (`clone` v003) already carries the delegated APPROVALS grant, now confirmed — no Imitator v-next is part of this task.

## Also updated (outside this folder)
- `../rolemap-v3-fixes-2026-10-04/fix-05-imitator-approval.md` — marked the grant **CONFIRMED** (R-004 update), with phase gate and carve-out.
- `../rolemap-v3-fixes-2026-10-04/roles-pipeline.md` — step 3 and the "until P4" variant now route governance-bot changes to "Gem, or Imitator once P4" with the carve-out.
- `../final-2026-10-04/safeguard-final.md` — fixed the two stale **Meter** references in the reconciliation note/Relationships (→ **Mediator**, Meter retired into Mediator per Merge F). The verbatim block already said Mediator.

## Judgement calls for Gem
1. **Self-check carve-out scope.** Which bots count as "checking Imitator"? At minimum Interrogator (tests Imitator's answers) and Investigator (confirms profile details Imitator relies on). Any change to Imitator, Interrogator or Investigator routes to Gem, never Imitator. Confirm the list.
2. **Phase-gated routing.** Confirm Imitator approves only once P4 goes live; Gem approves directly until then (Imitator currently dormant).
3. **Holder-benefits tension.** Imitator approving changes that benefit Imitator sits against "no bot grades its own work"; the carve-out plus Interrogator sampling (fix-01/02) and the weekly undo list to Gem are the mitigations — confirm that's enough.

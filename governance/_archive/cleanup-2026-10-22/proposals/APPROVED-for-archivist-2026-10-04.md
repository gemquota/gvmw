# Approved for (Roles) Archivist to record: 4 Oct 2026 (updated 2:40pm after the merge)

> **Update, 4 Oct 2026, 2:40pm:** Gem's merge (2:26pm) retired Assembler and Indexer. Changes to this handoff: the Architect v002 and the shared handoff spec are **on hold** until Gem approves corrections C-1/C-2 (Assembler → Arbiter); then record the corrected text. Indexer v002 is **withdrawn**. The new `archivist-brief-v002.md` (replacing the superseded `codex-keeper-v002.md`) is **pending Gem**. Marshal's deployment item is moot (v003 live). Everything else stands.

| Field | Value |
|---|---|
| To | (Roles) Archivist (61ef3abd-87b8-49f1-b8d6-b52969afa315) |
| From | (Roles) Architect (51af1200-ca1a-45ff-8350-848091e00f96) |
| Approving authority | **Gem, directly**, 4 Oct 2026 (AEST, UTC+10). Phase 1: (Roles) Assembler is dormant, so Gem approved in its place (`phase1-interim-bundle-v001.md`, item 1). Record "Approved by: Gem (direct), 4 Oct 2026" in each CHANGELOG row. |
| Verification | The Archivist verifies this file 1:1 with the claimed sender before recording, per `agent-message-verification-rule-v001.md` (governance-bot changes are high-consequence). This file was prepared by an Architect executor and relayed by the Architect, so the Archivist confirms Gem's approval with the Architect, or with Gem in chat, before recording. |
| Scope | Recording only. **No bot may edit live profiles; deployment is Gem's own action.** |

## 1. `phase1-interim-bundle-v001.md` (approved)

**Record:**
| Bot | Folder | New version | Text to record |
|---|---|---|---|
| (Roles) Architect | `instruction-architect/` | **v002: ON HOLD** | Record **only after Gem approves correction C-1**, using the C-1 text: v001 with three sentence swaps (approval to Gem in phase 1, then **Arbiter**, governance bots always to Gem; rejections from the **Arbiter**; trigger on the Scorer's handoff in phase 1, then Scrutineer). Don't record the earlier "Assembler" wording. |
| (Checks) Scorer | `assessor/` | **v002** | v001 with the one "Before → After" sentence swap in item 1 (results file plus priority handoff to the Architect in phase 1, then to Scrutineer). |
| ~~(ID) Indexer~~ | `indexer/` | **WITHDRAWN** | Indexer retired in the merge; don't record. (Ops) Minder v002 already carries "never indexing the codex". |

**Don't record:** item 3. The seven v002s (Engineer, Emissary, Meter, Marshal, Interrogator, Mediator, Messenger) are already recorded. Item 3 only changes their deployment status.

## 2. `handoff-phase1-v001.md` (approved)

**Record (ON HOLD until Gem approves correction C-2; then record the corrected text):** the spec as a shared governance document, for example `codex/_shared/handoff-phase1/v001.md`. It's the chain spec (Scorer → Architect → Gem → Archivist, reverting to Scorer → Scrutineer → Architect → **Arbiter** → Archivist after phase 1, per C-2) and isn't any one bot's instructions. The per-bot sentence changes it needs are the Architect and Scorer v002s in section 1, so nothing extra goes into bot folders.

**Not the Archivist's job:** (Ops) Marshal updates `schedule.md` to match. The "Handoff changes for Assessor/Auditor" pending item is now superseded by this spec.

## 3. `agent-message-verification-rule-v001.md` (approved)

**Record:**
- The rule (its verbatim block, including the voice-call line and the slot-only line added 4 Oct) as a shared rule, for example `codex/_shared/agent-message-verification-rule/v001.md`. Every bot's Limits refer to it, so there's no copy in each bot's folder (codex as single source).
- **(Checks) Safekeeper `secrets-credentials-custodian/` v002** = v001 verbatim, plus the "(Checks) Safekeeper's brief for this rule" (its CONTROLS / OBSERVES / FORBIDDEN / Reports to) appended as a final paragraph. This makes Safekeeper the rule's owner. Note: the unapproved `secrets-credentials-custodian-v002.md` draft from 3 Oct is **not** part of this; it's still pending.

## 4. `voice-call-messaging-v001.md` (approved, with Gem's two decisions folded in)

Gem's decisions are both in the text:
- Phone numbers are referred to only by slot (U1 to U5).
- The VOICE CALLS block auto-applies to any bot that starts taking voice calls later.

**Record** (use each bot's "After (exact)" text in the proposal):
| Bot | Folder | New version | Basis |
|---|---|---|---|
| (ID) Inquirer | `identity-inquirer/` | **v002** | v001 plus the VOICE CALLS block (with Inquirer's numbered-sets extras) |
| (ID) Inferer | `identity-inferer/` | **v002** | v001 plus the VOICE CALLS block |
| (Work) Emissary | `grok-bot/` | **v003** | recorded v002 plus the VOICE CALLS block |

**Parked, don't record yet:** **(Work) Extractor** (`scraper/`). Its "After" text folds the block into `proposals/scraper.md`, which isn't approved: batch-1 review "Reject as worded / needs Gem", and the codex is still the empty v001. Record Extractor's first version, with the block, only once Gem approves an Extractor instruction set. Gem's approval of the voice-call proposal covers the block, not scraper.md.

**Standing instruction (auto-apply):** when evidence shows another bot taking voice calls (a `voice-calls/` record, or the bot or Gem saying so), record that bot's next version as its current text plus the VOICE CALLS block with its own name in the prefix. Cite `voice-call-messaging-v001.md` (Gem, 4 Oct 2026) as the approval, and tell the Architect.

## 5. `archivist-brief-v002.md` (PENDING GEM, not approved yet)

Replaces the **superseded** `codex-keeper-v002.md`, so don't record that one. Once Gem approves it, record it as `codex-keeper/` **v002**. It makes the Arbiter (after phase 1) and Gem (always in phase 1, and for governance bots) the valid approval sources. Until then, the Archivist's live v001 accepts only Gem in practice, which matches phase 1 (ruling R-001).

## Deployment to live profiles: parked (Gem-only)

Recording in the codex isn't deployment. **No bot may edit profiles, so every deployment below is a Gem-only action.** Per Gem's instruction, deployment of approved versions is **parked** for the dormant non-P1 bots, with **one P1 exception: (Work) Emissary v003**, which Gem deploys directly once it's recorded. It skips v002, so the profile changes only once.

| Bot (live profile label) | Version to deploy | Status |
|---|---|---|
| (Work) Emissary ("P6") | v003 | **Deploy now (Gem)**: the stated exception |
| (ID) Inquirer ("P4"), (ID) Inferer ("P4") | v002 | Parked until their phase (Indexer retired) |
| Engineer, Meter, Interrogator, Mediator, Messenger | v002 (already recorded) | Parked until their phase (Marshal moot: v003 live) |
| ⚠ (Roles) Architect ("P1"), (Checks) Scorer ("P1"), (Checks) Safekeeper ("P1"), and (Roles) Archivist ("P1", once its v002 is approved) | v002 | **Gem to confirm.** These are *live* P1 bots, so the phase-1 flow, the verification-rule ownership and the Archivist's new approval sources only take effect once Gem deploys them. (Marshal is moot: its merged v003 is live.) Emissary's profile is labelled P6, not P1. |

## Summary for the Archivist
| # | Proposal | Approved | Record now | Parked |
|---|---|---|---|---|
| 1 | phase1-interim-bundle-v001.md | Gem, 4 Oct 2026 (C-1 pending Gem) | Scorer v002 now; Architect v002 after C-1 | Indexer withdrawn; item 3 deployment (Gem-only) |
| 2 | handoff-phase1-v001.md | Gem, 4 Oct 2026 (C-2 pending Gem) | Shared spec v001 after C-2 | `schedule.md` update (Marshal) |
| 3 | agent-message-verification-rule-v001.md | Gem, 4 Oct 2026 | Shared rule v001; Safekeeper v002 | Deployment (Gem-only) |
| 4 | voice-call-messaging-v001.md | Gem, 4 Oct 2026 | Inquirer v002, Inferer v002, Emissary v003 | Extractor (scraper.md not approved); deployment except Emissary |
| 5 | archivist-brief-v002.md | **Pending Gem** | codex-keeper v002 once approved | Deployment (Gem-only) |

# Proposals for 9 Oct 2026 — NEEDS GEM'S DIRECT APPROVAL

| File | Bot | Version | Approver | Status |
|---|---|---|---|---|
| `inferer-v003.md` | P2 (ID) Inferer (`94516ca6`) | v002 → v003 | Gem, directly (until P4 goes live); then Archivist records | Draft. NEEDS GEM'S DIRECT APPROVAL. Not deployed. Matches the R-012 update (9:25am; interim withdrawn); Archivist records only after Gem confirms in Archivist's own chat (R-008) |
| `inquirer-v003.md` | P2 (ID) Inquirer, active agent `0314faa4` (codex folder `identity-inquirer/`, keyed to old `e613112b`) | v002 → v003 | Gem, directly (until P4 goes live); then Archivist records | Draft. NEEDS GEM'S DIRECT APPROVAL. Not deployed. Matches the R-012 update; same R-008 caveat; Archivist decides folder keying with Gem |
| `explorer-v002.md` | P1 (Work) Explorer, agent `04dcca0d` (codex folder `explorer-copy/`) | v001 → v002 | Gem, directly, until P4 goes live; Imitator once P4 is live (R-014). Gem should confirm directly, as it removes deployment power | Draft. NEEDS GEM'S DIRECT APPROVAL. Not deployed. Hard ban on writing any live profile, its own included (R-014); deployment stays with Gem or Archivist (R-010) |
| `scrutineer-v004.md` | P2 (Checks) Scrutineer (`affe0344`, codex folder `auditor/`) | v003 → v004 | Gem, directly, until P4 goes live; Imitator once P4 is live. Governance bot, so Gem confirms directly | Draft. NEEDS GEM'S DIRECT APPROVAL. Not deployed. Role map and review recipient: Assembler → Archivist (R-017); adds one R-015 sentence on who approves (A1 ruled 9:35am) |
| `arbiter-v005.md` | P2 (Roles) Arbiter (`2133048d`, folder `arbiter/`) | v004 → v005 | Gem, directly (governance bot) | Draft. NEEDS GEM'S DIRECT APPROVAL. Not deployed. Approvals per R-015; role map is Archivist's (R-017) |
| `architect-v004.md` | P1 (Roles) Architect (`51af1200`, folder `instruction-architect/`) | v003 → v004 | Gem, directly (governance bot; self-proposal, flagged) | Draft. NEEDS GEM'S DIRECT APPROVAL. Not deployed. After P4 every proposal goes to Imitator, except Imitator or Investigator changes, which go to Gem; Interrogator dropped (retired) |
| `engineer-v006.md` | P5 (Work) Engineer (`f8e3fdc6`, folder `codey/`) | v005 → v006 | Gem, directly | Draft. NEEDS GEM'S DIRECT APPROVAL. Not deployed. "Assembler or Imitator" → Imitator after P4 (R-015) |
| `emissary-v005.md` | P5 (Work) Emissary (`28cf987d`, folder `grok-bot/`) | v004 → v005 | Gem, directly | Draft. NEEDS GEM'S DIRECT APPROVAL. Not deployed. "Assembler or Imitator" → Imitator after P4 (R-015) |

Superseded: `2026-10-06/inferer-v002.md` and `2026-10-06/inquirer-v002.md` (both recorded as codex v002 and deployed on 9 Oct), and their 2026-10-05 forerunners. Approve both v003s together. Nothing was deleted, deployed or recorded.

Inferer's switch to Inquirer `0314faa4` is **already covered by `inferer-v003.md`**. It matches the R-012 update (9:25am) and R-014, so its instruction text is unchanged; only a dated note was added to it and to `inquirer-v003.md`.

## Assembler sweep (R-015, R-017), 9 Oct about 9:45am
I searched the latest recorded version in every `codex/` folder, and today's drafts here, for Assembler named as a living approver or role-map owner. Historical changelogs and "retired" mentions were ignored.

| Brief (latest recorded) | Finding | Action |
|---|---|---|
| Arbiter `arbiter/v004` | "Assembler or Imitator approve"; role map "(Assembler's job)" | `arbiter-v005.md` |
| Architect `instruction-architect/v003` | non-governance proposals "to Assembler or Imitator"; "If Assembler or Imitator rejects"; checker list still names retired Interrogator | `architect-v004.md` |
| Engineer `codey/v005` | "approved by Gem (or by Assembler or Imitator once P4 goes live)" | `engineer-v006.md` |
| Emissary `grok-bot/v004` | same sentence as Engineer | `emissary-v005.md` |
| Scrutineer `auditor/v003` | "the Assembler's role map"; reviews sent to Assembler | already covered by today's `scrutineer-v004.md`; no amendment needed |
| Archivist `codex-keeper/v005` | role map "taken over from the retired Assembler" (retired mention only) | none |
| Old Explorer `genesis-gang-god/v004` | "Assembler or Imitator"; "Assembler marks it on the role map" | none. Agent `82a2c15a` has no folder now and isn't live; the active Explorer is `04dcca0d` (`explorer-copy/`). Its pending `explorer-v002.md` doesn't mention Assembler |
| Drafts in this folder | `inquirer-v003.md` and `scrutineer-v004.md` mention Assembler only in their notes; no instruction text names it | none |

All four new drafts are built on recorded text that byte-matches the live profiles. Each cites R-015, and only Gem approves them until P4 goes live.


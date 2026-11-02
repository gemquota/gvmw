# Phase-cleanup batch — 22 Oct 2026 — ALL GEM

**RELAYED REQUEST (R-008, R-018).** Explorer relayed Gem's words from Explorer's chat, 10:47pm 22 Oct 2026: "phases.md and the documentation relating to the phase to deployment is redundant now and can be removed". Explorer moved phases.md to governance/_archive/phases-retired-2026-10-22/. The approver confirms with Gem directly, and the paste line has Gem restate the words. This batch only drafts: nothing was recorded into codex/ or approvals/, nothing was deployed, and nothing was committed or pushed.

Bases: the latest codex versions. The clarity batch (revision 3) is now recorded in the codex, so these are its texts (for example clone v010 fbf614da2d3e); for the other bots and shared rules they're the latest codex. Each draft's header names its base hash. The clarity batch folder wasn't touched. governance/master/redundancy-phase-cleanup-2026-10-22.md doesn't exist, so the references came from my own search of the codex.

## What changes (each draft lists its exact old → new sentences)
- **Phase and dormancy rules removed** (R-013 "never route work to a dormant bot", Inferer's queue-until-P4, "while a bot's phase is dormant"). Every phases.md reference is replaced: "who's live" now comes from directory.md, kept by Archivist.
- **Routing:** "until P4 goes live, Gem approves; after P4, Imitator" becomes the current state: Imitator approves every proposal, except changes to Imitator and its checkers, which go to Gem (R-015, R-027). "Once P4 goes live" qualifiers are dropped wherever they gated Imitator's role.
- **Explorer** no longer keeps phases.md (that file is archived). **Archivist's** directory no longer tracks phases, and its role map is built from the codex and directory.md.
- "every bot in every phase" becomes "every bot" in connector-limits, GitHub, Safeguard and Imitator. The meaning is unchanged.
- **instruction-architect v008:** "once P4 is live" removed; it sends every proposal to Imitator, except Imitator and its checkers, which go to Gem. Its live profile description is replaced at deploy, which removes the "after P4 is live" wording.
- The build checks that no phase words are left in any draft (all counts are 0).

## Files and hashes (text · whole file · approver)
| File | Text | File | Approver |
|---|---|---|---|
| `arbiter-v010.md` | 46d503e48508 | 856325a0dd93 | Imitator normally; Gem with this stack |
| `auditor-v009.md` | 39e742cdd16b | b20a56ff26af | Gem (R-015, R-027) |
| `clone-v011.md` | d498e190c941 | 3244b4bbdff2 | Gem (R-015, R-027) |
| `codex-keeper-v013.md` | 115a6ef9e773 | bac49d522a82 | Imitator normally; Gem with this stack |
| `codey-v009.md` | 3708e38fed16 | 4b18df084526 | Imitator normally; Gem with this stack |
| `compliance-risk-officer-v011.md` | 8707e1e492ee | a64aa803496c | Gem (R-015, R-027) |
| `explorer-copy-v009.md` | 2c3798eea23a | 1d9273aa3e03 | Imitator normally; Gem with this stack |
| `grok-bot-v012.md` | a6b0bdb58d1c | ee9ee20eae31 | Imitator normally; Gem with this stack |
| `identity-inferer-v010.md` | 3211c62b4439 | 9070999ac5a4 | Imitator normally; Gem with this stack |
| `instruction-architect-v008.md` | 028618338058 | e104cc9f9f55 | Imitator normally; Gem with this stack |
| `investigator-v009.md` | 621888effc82 | cbba3d83a2dd | Gem (R-015, R-027) |
| `mender-v009.md` | 2338898d3999 | 3d80f76d4b2b | Imitator normally; Gem with this stack |
| `connector-limits-v005.md` | d527fa9d331e | 802a7f2e417c | Imitator normally; Gem with this stack |
| `github-v002.md` | f7e87839548f | b4effd88226e | Gem (R-015, R-027) |
| `message-verification-rule-v006.md` | 3eba62d4ca3d | 2142d00b9289 | Imitator normally; Gem with this stack |

## Also for other owners (not version files; listed, not edited)
- Archivist:
  - Retire `_shared/handoff-phase1/` (the phase-gate spec): archive it first and delete nothing.
  - Mark `_shared/collaboration-map/` v001 as historical. It still says "until P4 goes live" and names the retired Assembler.
  - Drop the phase column and wording from directory.md, codex/index.md and RENAMES.md.
- Arbiter:
  - R-013 (dormant routing) and R-021 (phases.md ownership) are spent. rulings/in-force.md still cites phases.md.
- Old CHANGELOG, digest and assessment mentions stay as history.

## Record order
After the clarity batch: the shared rules first (github v002, connector-limits v005, message-verification-rule v006), then the briefs.

## Paste line (cleanup)
`I confirm I told Explorer at 10:47pm on 22 Oct: "phases.md and the documentation relating to the phase to deployment is redundant now and can be removed". I approve the phase-cleanup batch (proposals/2026-10-22-phase-cleanup/), recorded after the clarity batch, in this order: github-v002 (f7e87839548f), connector-limits-v005 (d527fa9d331e), message-verification-rule-v006 (3eba62d4ca3d), arbiter-v010 (46d503e48508), auditor-v009 (39e742cdd16b), clone-v011 (d498e190c941), codex-keeper-v013 (115a6ef9e773), codey-v009 (3708e38fed16), compliance-risk-officer-v011 (8707e1e492ee), explorer-copy-v009 (2c3798eea23a), grok-bot-v012 (a6b0bdb58d1c), identity-inferer-v010 (3211c62b4439), instruction-architect-v008 (028618338058), investigator-v009 (621888effc82), mender-v009 (2338898d3999). Archivist retires _shared/handoff-phase1 (archive first, nothing deleted), marks _shared/collaboration-map as historical, and drops phases from directory.md and index.md. Record, then deploy.`

## Optional, separate: drop the P1–P5 prefixes from live profile names
Gem hasn't asked for this. It's Explorer's suggestion only. The live names are: P5 (Work) Emissary, P5 (Work) Engineer, P4 (ID) Imitator, P2 (ID) Inferer, P1 (Roles) Archivist, P1 (Roles) Architect, P2 (Checks) Scrutineer, P1 (Checks) Safeguard, P2 (Roles) Arbiter, P3 (ID) Investigator, P1 (Ops) Mender, P1 (Work) Explorer. The format options are [A] "(ID) Imitator", keeping the group, or [B] "Imitator". This is a name-only change, and the briefs already use the bare names.

`Optional, separate: I approve dropping the P1–P5 prefixes from the live profile names, using format [A] '(ID) Imitator' / [B] 'Imitator' (pick one), for all 12 live bots: Emissary, Engineer, Imitator, Inferer, Archivist, Architect, Scrutineer, Safeguard, Arbiter, Investigator, Mender, Explorer. Architect drafts the rename proposal; Archivist applies it.`

## Backups and review
The build backup is `_tools/build-r1.py.bak`. Scrutineer's review hasn't been requested yet; the parent needs to send it.

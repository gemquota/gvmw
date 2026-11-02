# Phase-cleanup batch — 22 Oct 2026 — ALL GEM

**RELAYED REQUEST (R-008, R-018).** Explorer relayed Gem's words from Explorer's chat, 10:47pm 22 Oct 2026: "phases.md and the documentation relating to the phase to deployment is redundant now and can be removed". Explorer moved phases.md to governance/_archive/phases-retired-2026-10-22/. The approver confirms with Gem directly, and the paste line has Gem restate the words. This batch only drafts: nothing was recorded into codex/ or approvals/, nothing was deployed, and nothing was committed or pushed.

Bases: the latest codex versions. The clarity batch (revision 3) is now recorded in the codex, so these are its texts (for example clone v010 fbf614da2d3e); for the other bots and shared rules they're the latest codex. Each draft's header names its base hash. The clarity batch folder wasn't touched. governance/master/redundancy-phase-cleanup-2026-10-22.md doesn't exist, so the references came from my own search of the codex.

## What changes (each draft lists its exact old → new sentences)
- **Phase and dormancy rules removed** (R-013 "never route work to a dormant bot", Inferer's queue-until-P4, "while a bot's phase is dormant"). Every phases.md reference is replaced: "who's live" now comes from directory.md, kept by Archivist.
- **Routing:** "until P4 goes live, Gem approves; after P4, Imitator" becomes the current state: Imitator approves every proposal, except changes to Imitator and its checkers, which go to Gem (R-015, R-027). "Once P4 goes live" qualifiers are dropped wherever they gated Imitator's role.
- **Explorer** no longer keeps phases.md (that file is archived). **Archivist's** directory no longer tracks phases, and its role map is built from the codex and directory.md.
- "every bot in every phase" becomes "every bot" in connector-limits, GitHub, Safeguard and Imitator. The meaning is unchanged.
- **instruction-architect v008:** "once P4 is live" removed; it sends every proposal to Imitator, except Imitator and its checkers, which go to Gem. Its live profile description is replaced at deploy, which removes the "after P4 is live" wording.
- The build counts the phase words left in each draft. The only ones left are the citation wording "no phase gate, R-055" and "phases retired, R-055".

## Files and hashes (text · whole file · approver)
| File | Text | File | Approver |
|---|---|---|---|
| `arbiter-v010.md` | 4fdacf4b19cd | 221ce6314fca | Imitator normally; Gem with this stack |
| `auditor-v009.md` | 49d52aa0b490 | 54538a8dcedd | Gem (R-015, R-027) |
| `clone-v011.md` | 2224e55c7479 | ea1a3cf0a4b3 | Gem (R-015, R-027) |
| `codex-keeper-v013.md` | acc983688554 | 590bb901ece5 | Imitator normally; Gem with this stack |
| `codey-v009.md` | 637602051587 | faff649f6ab8 | Imitator normally; Gem with this stack |
| `compliance-risk-officer-v011.md` | 39137e16f1cb | 26ed435e95e2 | Gem (R-015, R-027) |
| `explorer-copy-v009.md` | 0907098ed588 | 34e9b63be0f0 | Imitator normally; Gem with this stack |
| `grok-bot-v012.md` | 139df59223ce | 2d64a5efed38 | Imitator normally; Gem with this stack |
| `identity-inferer-v010.md` | 35c50eb35a9b | 39568326b025 | Imitator normally; Gem with this stack |
| `instruction-architect-v008.md` | 0656bfcd4aaf | 8f7a6f041033 | Imitator normally; Gem with this stack |
| `investigator-v009.md` | 42419cb504ec | a4611ea6b570 | Gem (R-015, R-027) |
| `mender-v009.md` | 1d77682bba5f | a46f236be681 | Imitator normally; Gem with this stack |
| `connector-limits-v005.md` | 73574e5639cb | 52a49ef4b359 | Imitator normally; Gem with this stack |
| `github-v002.md` | 55a582bc5940 | 53efe002e98e | Gem (R-015, R-027) |
| `message-verification-rule-v006.md` | da3b1cf66fb3 | dddcfeeb0e89 | Imitator normally; Gem with this stack |

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
`I confirm I told Explorer at 10:47pm on 22 Oct: "phases.md and the documentation relating to the phase to deployment is redundant now and can be removed" (Arbiter's R-055). I approve the phase-cleanup batch revision 2 (proposals/2026-10-22-phase-cleanup/), recorded after the clarity batch, in this order: github-v002 (55a582bc5940), connector-limits-v005 (73574e5639cb), message-verification-rule-v006 (da3b1cf66fb3), arbiter-v010 (4fdacf4b19cd), auditor-v009 (49d52aa0b490), clone-v011 (2224e55c7479), codex-keeper-v013 (acc983688554), codey-v009 (637602051587), compliance-risk-officer-v011 (39137e16f1cb), explorer-copy-v009 (0907098ed588), grok-bot-v012 (139df59223ce), identity-inferer-v010 (35c50eb35a9b), instruction-architect-v008 (0656bfcd4aaf), investigator-v009 (42419cb504ec), mender-v009 (1d77682bba5f). Archivist then: retires _shared/handoff-phase1 (archive first, nothing deleted); marks _shared/collaboration-map as historical; cleans directory.md (the phases.md citation and the 'P1: live' headings, so it lists live and retired bots per R-055), index.md and RENAMES.md. Arbiter has retired R-021 and amended R-013 and R-025 (R-055). Record, then deploy.`

## Optional, separate: drop the P1–P5 prefixes from live profile names
Gem hasn't asked for this. It's Explorer's suggestion only. The live names are: P5 (Work) Emissary, P5 (Work) Engineer, P4 (ID) Imitator, P2 (ID) Inferer, P1 (Roles) Archivist, P1 (Roles) Architect, P2 (Checks) Scrutineer, P1 (Checks) Safeguard, P2 (Roles) Arbiter, P3 (ID) Investigator, P1 (Ops) Mender, P1 (Work) Explorer. The format options are [A] "(ID) Imitator", keeping the group, or [B] "Imitator". This is a name-only change, and the briefs already use the bare names.

`Optional, separate: I approve dropping the P1–P5 prefixes from the live profile names, using format [A] '(ID) Imitator' / [B] 'Imitator' (pick one), for all 12 live bots: Emissary, Engineer, Imitator, Inferer, Archivist, Architect, Scrutineer, Safeguard, Arbiter, Investigator, Mender, Explorer. Architect drafts the rename proposal; Archivist applies it.`

## Backups and review
The build backup is `_tools/build-r1.py.bak`. Scrutineer's review hasn't been requested yet; the parent needs to send it.

## Revision 2 (Scrutineer's CONDITIONAL review: reviews/2026-10-22-phase-cleanup-review.md; Arbiter's R-055)
- **R-055 (Arbiter, 10:52pm 22 Oct; from Gem's 10:47pm words, which Arbiter checked in Explorer's transcript)** is cited wherever a draft drops a phase or dormancy rule:
  - R-021 is retired: directory.md is the only source for which bots are live. explorer-copy no longer cites R-021, and codex-keeper's "phases.md wins" clause is replaced with the R-055 rule.
  - R-013 is amended: Gem may chat with any bot, a retired bot gets no scheduled or bot-routed work, and Safeguard reviews all bots. Each "dormant" rule becomes "never route work to a retired bot (R-013 as amended by R-055)", and the remaining R-013 citations read "R-013 as amended by R-055".
  - R-025 is amended: Scrutineer samples the live bots in directory.md (auditor).
  - Arbiter has done the R-021 and R-013 step that the review asked for (R-055).
- **R-054 citation:** R-054 states that it "changes no rule" and only consolidates. Its row 3 restates R-015 and R-027 and extends them ("including changes to whether a checker exists"). So each routing sentence cites both: "(R-015, R-027; restated and extended by R-054 row 3: …)".
- **Checker lists:** every draft that I changed now uses the same list, "Investigator, Scorer, Scrutineer, Safekeeper, Safeguard". Scorer and Safekeeper retire only once the redesign is verified, so trimming the lists is **deliberately deferred to that retirement step**. Some untouched clauses keep their base wording; for example, auditor's base clause notes that Scorer and Safekeeper are merged in.
- **Full old → new sentences:** every draft's change list now shows whole sentences, including clone, explorer-copy and grok-bot.
- **Slightly outside the phase scope (announced):** Arbiter's "every proposal" became "every instruction proposal" (revision 1). Inferer's new sentence ("if you still hold a queue from before Imitator went live, send it in numbered parts first") adds a one-off transitional step.
- The paste line asks Archivist to clean directory.md (the phases.md citation and the "P1: live" headings), index.md and RENAMES.md, and notes R-055.
- Revision 1 files are in `_r1/`. The build backups are `_tools/build-r1.py.bak` and `_tools/build-r2.py.bak`.

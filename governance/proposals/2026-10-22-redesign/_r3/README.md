# Redesign batch — 22 Oct 2026 (R-051) — ALL GEM-ONLY

Source: R-051 and gem-answers-inquirer-2026-10-22.md. Gem's 14 answers were **relayed via Inquirer** (8:08–8:13pm AEST). Arbiter verified them in Inquirer's transcript, but under R-008 Gem confirms them directly before anything is recorded. Gem's words, exactly: "Engineer fully free, no per-push checks" · "Yes, create a free healthchecks.io account" · "Google Drive" · "Not now" · "No, leave it as is" · "No, keep allowing it" · "Advisory only for big or irreversible decisions" · "Start stage 1 (token inventory) now" · "Yes" (action hash) · "Yes, using free storage like Google Drive" · "Later" · "Yes" (11 checks) · all four merges approved, lifting the 4 Oct veto · "No, free options only".

Nothing has been written to codex/ or approvals/, no profiles were edited, nothing was deployed and no tokens were read. Builder: `_tools/build.py` (it reads the latest codex as its base).

## Hashes (file · text · whole file), revision 3
```
mender-v007.md a4fdbd11b16b c81642f2c919
scrutineer-v007.md b15dc0bf90ba ac6d38914be3
safeguard-v009.md b71d644b5161 6e1ac4c57356
inferer-v008.md ca342fc6cfc9 25f47e6067b7
emissary-v010.md f0371f2dd775 e3d0e805a87a
investigator-v007.md 15de2afd1c8e 109a2ec07214
archivist-v011.md 7a08e3b058d6 197ef75c954f
deterministic-checks-v001.md 0e93d5ae1a6a e4cea617fa6e
approval-objects-v001.md 1c2852679768 aa9a7fdcb4d2
resilience-v001.md 91c0da0bb06f 059fe27b555c
```

## Supersession (unrecorded drafts that are replaced, not recorded)
- redundancy: scorer-v005, scrutineer-v005, safeguard-v007, investigator-v005, archivist-v009 (rebased here: same version numbers, new text)
- r044-r047: emissary-v008 (its R-049 posting lines live in connector-limits v003 rule 1)
- GitHub 5c: mender-v006, mediator-v007, scorer-v006, scrutineer-v006, safeguard-v008, safekeeper-v006, inquirer-v005, inferer-v007, emissary-v009, extractor-v007, investigator-v006, archivist-v010
- gvmw per-push words in connector-limits v003 rule 14 and github-v001: superseded by R-051 (no per-push checks). Both need a rebase pass before recording (a follow-up, not done here).
- Kept as they are: redundancy imitator-v007; r044 imitator-v008 and arbiter-v007; GitHub github-v001 (rebase first), engineer-v008, imitator-v009, explorer-v007, architect-v006, arbiter-v008, message-verification-rule-v005.

## Record order
1. Redundancy leftovers that survive (imitator-v007) → 2. r044-r047 (imitator-v008, arbiter-v007) → 3. connector-limits v003, rebased: rule 14 to R-051, rule 1/Apify naming Emissary, Drive writes allowed for the resilience rule → 4. GitHub 5c survivors (after a STACK rebase) → 5. this batch.

## Migration order
1. Gem creates the free healthchecks.io account and names a private Drive folder.
2. Archivist archives Mediator, Scorer, Safekeeper, Inquirer and Extractor (folders, CHANGELOGs and notes to _archive/ and Drive; counts and hashes checked).
3. Record the shared rules: resilience, approval-objects (shadow mode), deterministic-checks.
4. Deploy the survivors: Safeguard v009 and Scrutineer v007 first, so the checkers are up; then Mender v007, Inferer v008, Emissary v010, Investigator v007, Archivist v011. Scrutineer checks each deploy hash except its own: Safeguard checks Scrutineer v007's deploy, and Scrutineer checks Safeguard v009's.
5. Retire the five merged agents only after step 4 has been verified. Don't delete them.
6. A week of shadow approval objects, then make them required for deploys.

## Open / TODO
- Imitator's advisory scope: a TODO pending Arbiter's question to Gem (interim per R-051; veto stands).
- gvmw: free per R-051; also pending Gem's answer on the user's card.
- Deletion gate (Not now), data classes and BIE wall (Later), gvmw privacy check (No).

## Gem paste line (one)
> Gem, in Archivist's chat: "I confirm my 14 answers in Inquirer's chat tonight (R-051), and I approve the redesign batch, recorded after GitHub revision 5d: Mender v007 (a4fdbd11b16b), Scrutineer v007 (b15dc0bf90ba), Safeguard v009 (b71d644b5161), Inferer v008 (ca342fc6cfc9), Emissary v010 (f0371f2dd775), Investigator v007 (15de2afd1c8e), Archivist v011 (7a08e3b058d6), deterministic-checks v001 (0e93d5ae1a6a), approval-objects v001 (1c2852679768), resilience v001 (91c0da0bb06f), with the archive-first migration order and retiring Mediator, Scorer, Safekeeper, Inquirer and Extractor after verification."

## Update after Scrutineer's frozen re-check
- Record order step 4 is now GitHub revision 5d, survivors only (its README has the paste line). connector-limits v003 is revision 7: the daily sync is on, gvmw checks are none per R-051, and Gem's card answer is pending.
- Gap: the merged briefs here are built on the latest codex, so they don't yet carry the superseded GitHub drafts' GitHub-rule pointer lines. Rebase them onto github-v001 before recording. The version numbers also collide with unrecorded drafts (safeguard-v008, inferer-v007, mender-v006), so retire the superseded files' numbers when recording.

## Revision 2 (8:20pm, rebased; frozen)
- Rebased onto github-v001: each merged brief's annex is now the GitHub 5d drafts (which stack on codex, redundancy and r044), so their GitHub pointer lines carry over.
- Version numbers bumped above every unrecorded draft: Mender v007, Scrutineer v007, Safeguard v009, Inferer v008, Emissary v010, Investigator v007, Archivist v011. Superseded drafts keep their numbers unused.
- Because the annexes now come from the GitHub 5d drafts, GitHub 5d must be recorded first (survivors only), then this batch; the superseded 5d texts are recorded only as annex text inside these briefs.
- resilience v001 now points to connector-limits v003 revision 8 (Drive carve-out in rule 3; Emissary runs Apify).
- r044-r047 emissary-v008 is no longer recorded separately; its text is inside Emissary v010's annex.
- The old gap note above is resolved. Revision 1 files are in `_r1/`, and the build backup is `_tools/build-r1.py.bak`.

## Revision 3 (8:26pm; Investigator's and Scrutineer's reviews; frozen)
- B1: scrutineer-v007's header now names the codex base, auditor v004 (542ade104e4b) and assessor v004 (10e0324f805d).
- D2/D5: the annex sentences that referred to Scorer, or had Scrutineer reviewing itself, are amended and marked [R-051] (scrutineer-v007, mender-v007); every other line stays word for word.
- D3: Scrutineer's scope adds auditing checks 1 and 10.
- R1: scrutineer-v007's reviewer is now Safeguard only.
- Check 6 and migration step 4: Safeguard and Scrutineer check each other's deploys.
- Mender: the bot responsible pauses a cost, and only Arbiter lifts a pause.
- NAMES note in every brief's Relationships, and in connector-limits v003 LIMITS: a retired bot's name means the bot it merged into. github-v001 and engineer-v008 rely on that note and weren't edited.

## Unused version numbers (not a gap in the chain; Archivist records the jump)
- mender v006 · auditor (Scrutineer) v005, v006 · assessor (Scorer) v005, v006 (retired) · compliance-risk-officer (Safeguard) v007, v008 · secrets-credentials-custodian (Safekeeper) v006 (retired) · identity-inferer v007 · identity-inquirer v005 (retired) · grok-bot (Emissary) v008, v009 · scraper (Extractor) v007 (retired) · connector-steward (Mediator) v007 (retired) · investigator v005, v006 · codex-keeper (Archivist) v009, v010.

## Risk notes
- D1: scoring and auditing now sit in one bot and one run. The only independent check is Safeguard's after-the-fact audit, plus Gem. This is a real reduction in checking (Investigator's review).
- R2: imitator-v008's veto over every Arbiter ruling could have reached R-015, R-027 and R-028. imitator-v008 and v009 now exclude them (Gem, 8:25pm in Investigator's chat, "I guess", relayed by Investigator). Gem restates it in the r044 paste line.
- Mender: one bot tracks cost pauses and recovery; Arbiter alone lifts pauses.

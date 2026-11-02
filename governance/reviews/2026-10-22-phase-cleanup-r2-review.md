# Scrutineer review: phase-cleanup batch, revision 2

Reviewed 22 Oct 2026, about 11:00pm AEST (UTC+10). Read-only; this file is the only write. Prior review: reviews/2026-10-22-phase-cleanup-review.md (CONDITIONAL).

**Verdict: CONDITIONAL**

## Integrity (9)
- README sha256 first 12 = 667255941a56 (confirmed).
- All 15 text hashes (fenced text, trailing newline stripped) and file hashes recomputed: they match the README table and _tools/hashes.txt. The 4th column of hashes.txt (phase-word count) went from 0 in _r1 to 0–2; that matches the "Phase words left on purpose" lines.
- Bases (7): every header base hash equals the fenced-text hash of that codex version, and that version is still the highest in its folder after the clarity deploy (arbiter v009, auditor v008, clone v010 fbf614da2d3e, codex-keeper v012, codey v008, CRO v010, connector-limits v004, explorer-copy v008, github v001, grok-bot v011, identity-inferer v009, instruction-architect v007, investigator v008, mender v008, MVR v005). PASS.

## (1) R-055
- In rulings.md:428, quoted: "### R-055 (2026-10-22 22:52 AEST) Phase records retired. Source: Gem's own words, typed at 10:47pm AEST in Explorer's chat (t80u): 'phases.md and the documentation relating to the phase to deployment is redundant now and can be removed'. I checked them in Explorer's transcript. … R-021 is retired. directory.md is now the only source for which bots are live or retired, and Archivist keeps it. R-025 is amended. … R-013 is amended. Gem may chat with any bot. A retired bot gets no scheduled or bot-routed work. Safeguard review applies to all bots. The dormancy clauses are spent, because every phase is live."
- Also in rulings/in-force.md:76 (and R-013/R-025 marked "amended by R-055" at :42 and :46) and in rulings/annex-history.md:81. in-force.md no longer cites phases.md. PASS.
- Basis: Gem's words were typed in Explorer's chat. Arbiter read them in Explorer's transcript, so it is better than a bare relay, but Gem didn't speak to Arbiter or the approver. approvals/ has no record of the 10:47pm words. Under R-008 this is still relay-grade until Gem restates the words (the paste line does this).
- R-055 is cited at every dropped phase or dormancy rule in the 15 drafts. PASS.

## (2) R-021 / R-013 wording
- explorer-copy no longer cites R-021 ("Archivist keeps directory.md, the only source for which bots are live (R-055)"). No fenced text cites R-021.
- The dormancy rules now read "never route work to a retired bot (R-013 as amended by R-055)" (codey, explorer-copy, grok-bot ×2). The other R-013 citations read "R-013 as amended by R-055" (clone, CRO). PASS.
- Note: grok-bot v012 now has two retired-bot routing sentences, one replacing each old dormancy sentence. That's redundant but consistent.

## (3) R-054 row 3
- Row 3 (rulings/R-054-approval-authority.md:13) covers (a) any change to Imitator; (b) any change to its checkers "including changes to whether a checker exists"; and (c) any proposal that widens Imitator's role. The "changes no rule" statement is in R-054's preamble (line 3) and rulings.md:422, not in row 3 itself.
- Routing sentences cite "(R-015, R-027; restated and extended by R-054 row 3: …)". The word "extended" sits uneasily with R-054's own "changes no rule". This is a wording issue, not a routing error.

## (4) Checker lists
- The README records the deferral (Revision 2, "Checker lists": "deliberately deferred to that retirement step"). Confirmed.
- Changed sentences in arbiter, clone, codex-keeper, instruction-architect, MVR use the full five-bot list. codey, grok-bot, explorer-copy, mender say "Imitator and its checkers" without naming them, which is acceptable.
- Fact (auditor, own brief, no verdict): auditor v009's changed routing sentence keeps "Investigator, Scrutineer, Safeguard; Scorer and Safekeeper are merged into them [R-051]". It isn't the five-bot list, but the README describes it as base wording.

## (5) Change lists / out-of-scope edits
- Every draft's change list now uses whole sentences. Every base→draft sentence change maps to an announced OLD→NEW pair. No unannounced changes were found.
- The lists are layered: the r1 pair is followed by an r2 pair whose OLD is the r1 text, not the base. Examples: clone DECISIONS, auditor, codex-keeper CONTROLS, instruction-architect, MVR. Applying them in order gives the draft, but a reader comparing a single pair against the base will see a mismatch. This is cosmetic.
- Both out-of-scope edits are announced: arbiter "every instruction proposal" and inferer's queue-to-Imitator sentence.

## (6) clone v011 "There is no phase gate any more, so these powers apply now (R-055)."
- It replaces "Until P4 goes live it decides and approves nothing… (R-013)". R-021 and R-025 record P4 as live since 11:30pm on 15 Oct, so the gate had already lifted and Imitator's powers don't widen in substance. The sentence states the current position.
- It is still a change to Imitator, so only Gem can approve it (R-015, R-027, R-054 row 3(a)). The README and the header route it to Gem. PASS on routing.

## (8) Paste line
- It includes the Archivist cleanup of directory.md, index.md and RENAMES.md, and "Arbiter has retired R-021 and amended R-013 and R-025 (R-055)". PASS.
- Stale or incomplete: directory.md was already partly cleaned at 10:54:24pm (phase grouping removed), so asking for the "'P1: live' headings" is out of date. directory.md:20 still says "Explorer still keeps phases.md … this file follows it (R-021)", and codex/index.md:7 still cites phases.md. These are Archivist items; the paste line should name the line-20 owner clause.

## (9) Diff vs _r1 / phase words
- r1→r2 fenced changes in all 15 files: R-055 citations, R-054 row-3 citations, full checker lists (arbiter restored Scorer and Safekeeper), "as amended by R-055", new retired-routing sentences (explorer-copy, grok-bot, codey), the clone "no phase gate" sentence, the codex-keeper directory-only clause, and CRO's "since your review applies to all bots". All are announced in the change lists or the README Revision 2 section. No unannounced changes.
- Phase words left in fenced text: "no phase gate, R-055" and "phases retired, R-055" as citations, plus clone's sentence. Two profile names remain: codex-keeper "active P2 (ID) Inquirer" and instruction-architect "'P4 (Ops) Mediator'". These are names, not rules, but README line 13 ("the only ones left are the citation wording") isn't exact. No phases.md, dormant or "until/once P4" wording remains in any fenced text.

## Observation (outside this batch)
directory.md:109 records that the retired bots' agent folders were deleted, with the writer unknown and no approval on record. This is outside this batch and is noted for Gem and Arbiter.

## Conditions
1. Gem restates the 10:47pm words directly (the paste line), because R-055 rests on Gem's words in Explorer's chat, checked from a transcript (R-008).
2. Correct the directory.md item in the paste line: the headings are already gone. Name the directory.md:20 "Explorer still keeps phases.md … (R-021)" clause and codex/index.md:7.
3. Correct README line 13 to mention the remaining P# profile names (cosmetic).
4. Optional: reword "restated and extended" to fit R-054's "changes no rule", and flatten the layered change lists to base→final pairs.

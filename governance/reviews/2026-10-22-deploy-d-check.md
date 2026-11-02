# Scrutineer deploy check D: GitHub revision 5h (t72u item 4), 22 Oct 2026, about 9:45pm AEST

This check was read-only. Hashes are the SHA-256 of the fenced text, first 12 hex characters. All times are AEST (UTC+10). The manifest is codex/_tools/deploy_manifest_2026-10-22d.json, with 7 entries.

| # | Check | Verdict |
|---|---|---|
| 1 | Live text byte-equal to the draft, codex and manifest | **PASS** |
| 2 | R-035 order | **PASS** |
| 3 | Only the five profiles changed | **PASS** |
| 4 | Gem's approval names 5h and every hash | **PASS** |
| 5 | CHANGELOGs, index and directory | **PASS** |
| 6 | verify.py and verify_shared.py | **PASS** |
| 7 | 5h is the same set passed in final-check-2 | **PASS** |
| 8 | The 12 GitHub drafts left out on purpose | **PASS** |
| 9 | imitator-v009 chain; Arbiter v008 approval | **PASS** |
| 10 | Apify gap | **Open, safe** (unchanged) |

## Evidence
1. **Byte-equality.** For each entry, the live description (or the codex file, for shared rules), the frozen draft's fenced text, the codex version file and the manifest `text` are all byte-equal.

   | Entry | Chars | Hash |
   |---|---|---|
   | _shared/github v001 | 13528 | 3c5c3995a886 |
   | _shared/message-verification-rule v005 | 3827 | c78245bcf145 |
   | Engineer (f8e3fdc6, codey v008) | 8101 | e48cde917489 |
   | Imitator (6ae584b8, clone v009) | 7083 | c92d31926a18 |
   | Explorer (04dcca0d, explorer-copy v007) | 8415 | a98d235b093a |
   | Architect (51af1200, instruction-architect v006) | 2515 | c2e149404e57 |
   | Arbiter (2133048d, arbiter v008) | 2390 | 8a9498236d52 |

2. **R-035.** Each profile was written after its version file: Engineer +63 seconds, Imitator +80, Explorer +100, Architect +106 and Arbiter +112.
3. **Only five profiles.** Only these five profile.json files changed after 9:37pm. verify.py found every live agent equal to its latest codex version.
4. **Approval.** approvals/2026-10-22-gem-direct-words.md, t72u 9:27pm, item 4 (Gem's own words in Archivist's chat):
   > "I approve GitHub batch revision 5h, after the redundancy, r044-r047 and connector-limits v003 batches: github-v001 (3c5c3995a886), engineer-v008 (e48cde917489), imitator-v009 (c92d31926a18), explorer-v007 (a98d235b093a), architect-v006 (c2e149404e57), arbiter-v008 (8a9498236d52), message-verification-rule-v005 (c78245bcf145) — record and deploy, github-v001 first; the other twelve are replaced by the redesign batch."

   The approval names 5h and all 7 hashes. github-v001 was deployed first, as asked: it is the first manifest entry. Because these are Gem's own words, the changes to Imitator (v009) and the Arbiter v008 addition to Imitator's role are Gem-approved (R-015, R-027).
5. **Records.**
   - Every CHANGELOG has a row citing t72u item 4: _shared/github, _shared/message-verification-rule, codey, clone, explorer-copy, instruction-architect and arbiter.
   - index.md shows codey v008 (:9), clone v009 (:12), instruction-architect v006 (:16), arbiter v008 (:28), explorer-copy v007 (:44), message-verification v005 (:64) and GitHub v001 (:66).
   - **directory.md is fixed:** Emissary grok-bot v007 (:34) and Extractor scraper v006 (:36). The five deployed bots show their new versions (:17, :18, :22, :31 and :35).
6. **Scripts.** Neither script writes anything. verify.py printed "OVERALL: PASS". verify_shared.py printed "SHARED: 12 version files, 12 match … OVERALL: PASS", including "_shared/github/v001.md == github-v001.md (13528 chars, 3c5c3995a886)" and "message-verification-rule/v005.md (3827 chars, c78245bcf145)".
7. **What 5h is.**
   - 5h is Architect's 8:36–8:37pm refreeze (github/README.md:334, "Revision 5h (8:36pm; frozen)"). That is exactly the state I checked in final-check-2, with PASTE-LINES still 75820b4ab8a6.
   - All 7 deployed hashes equal the ones in final-check-2. **Nothing changed after final-check-2.**
   - **Architect v006 (c2e149404e57):** the same hash was in the "rest PASS" group of reviews/2026-10-22-github-r5-review.md and has been unchanged since.
   - **Explorer v007 (a98d235b093a):** it failed the r5 review at d81785c494c4 (finding 4: "a public or shared push still needs Gem's own words to Engineer"). A word diff of d81785c494c4 against a98d235b093a shows two changes:
     - (a) The backup rule now follows R-049: "verified off-computer backup, checked by a bot other than you … before deleting code, notes, configs or bot instructions; scrapes, data, logs and scratch files need none, and mass wipes are never allowed".
     - (b) Finding 4 is fixed: "… relay; Engineer acts under the GitHub rule (R-045)".
     - Nothing else changed. Both changes are correct under R-045 and R-049.
   - Arbiter v008 and Imitator v009 were passed in the r3 review chain and in final-check-2 at these hashes.
8. **The other twelve drafts.** They were left out on purpose, not by mistake.
   - PASTE-LINES §4 is titled "GitHub revision 5h, survivors only".
   - Gem's item 4 says "the other twelve are replaced by the redesign batch". These are:
     - safeguard-v008, safekeeper-v006 and scrutineer-v006, which become Safeguard v009 and Scrutineer v007
     - scorer-v006, which is replaced by Scrutineer v007
     - emissary-v009 and extractor-v007, which become Emissary v010
     - mediator-v007 and mender-v006, which become Mender v007
     - investigator-v006, which becomes Investigator v007
     - inquirer-v005 and inferer-v007, which become Inferer v008
     - archivist-v010, which becomes Archivist v011
   - Each redesign draft carries the matching GitHub text word for word as an annex (redesign README; final-check-2 confirmed safeguard).
   - **Interim note:** until item 5 is deployed, those bots run their older codex versions without the GitHub pointer lines. github-v001 is now the shared rule, and their briefs already follow the shared rules. Engineer is the only GitHub writer, and the others only read, so this is safe.
9. **Chains.**
   - imitator-v009's base is d877b6d0b31f, which matches live clone v008 (deploy C).
   - Its header still says "codex v006 (latest …)", which is out of date. Gem approved it by text hash, so this is cosmetic only.
   - Arbiter v008 stacks on 3d031639639f, the live v007.
10. **Apify gap.**
   - connector-limits/CHANGELOG.md:11 now records deploy C's finding as a "Factual note only; no routing rule is added or implied". That is accurate.
   - The gap is unchanged. v003 names Emissary as the Apify runner and Mender for spend, but the live briefs are still Emissary grok-bot v007 (which sends scraping back to Explorer), Extractor scraper v006 and Mediator.
   - It is still safe. It fails closed, because every Apify run is spending and needs Gem's direct words. It closes when item 5 is deployed.

## Overall: PASS
GitHub 5h is deployed correctly. Next in the record order is item 5 (the redesign), which also closes the Apify gap.

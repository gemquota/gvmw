# Scrutineer deploy check C: imitator-v008, arbiter-v007 and connector-limits v003 A, 22 Oct 2026, about 9:40pm AEST

This check is read-only. Each hash is the SHA-256 of the fenced text, first 12 hex characters. All times are AEST (UTC+10). Manifest: codex/_tools/deploy_manifest_2026-10-22c.json, which has 3 entries.

| # | Check | Verdict |
|---|---|---|
| 1 | Live text byte-equal to the draft and the codex | **PASS** |
| 2 | Manifest matches | **PASS** |
| 3 | R-035 order | **PASS** |
| 4 | Only these two profiles changed | **PASS** |
| 5 | Gem's approval recorded with the hashes and Variant A | **PASS** |
| 6 | CHANGELOGs and index updated | **PASS** |
| 7 | verify.py and verify_shared.py | **PASS** |
| 8 | v003 A recorded as a shared rule, v002 superseded | **PASS** |
| 9 | imitator-v008 wording, and v009's chain | **PASS** |
| 10 | Apify gap | **Safe in the meantime** (gap stays open until item 5) |

## Evidence
1. **Live text.** Both live descriptions are byte-equal to the frozen draft's fenced text and to the codex version file.

   | Bot | Live description | Draft | Codex |
   |---|---|---|---|
   | Imitator (6ae584b8…) | 6261 chars, d877b6d0b31f | r044-veto/imitator-v008.md | codex/clone/v008.md |
   | Arbiter (2133048d…) | 2076 chars, 3d031639639f | r044-veto/arbiter-v007.md | codex/arbiter/v007.md |

2. **Manifest.**
   - The two profile entries match on agent id, folder, version, character count and full sha256, and each `text` is byte-equal to the live description.
   - The third entry (kind shared, `_shared/connector-limits` v003, variant A, 23658 chars, sha256 806a6fa315cb52133d88…) is byte-equal to codex/_shared/connector-limits/v003.md and to the draft.
3. **R-035 order.** The version files were written before the profiles.
   - Written at 21:34:28.99: codex/clone/v008.md, codex/arbiter/v007.md and _shared/connector-limits/v003.md.
   - Profiles: Imitator at 21:35:38.93, Arbiter at 21:35:45.25.
   - The CHANGELOGs and index followed at 21:36:18.
4. **Only these two changed.** Only those two profile.json files changed after 9:31pm. verify.py shows 17 of 17 live agents matching their latest codex version; the other 20 are retired bots whose profiles are gone.
5. **Gem's approval.**
   - Where it's recorded: approvals/2026-10-22-gem-direct-words.md:26 records "Gem, in Archivist's chat (t72u), 9:27pm 22 Oct 2026".
   - Item 2 ends: "I approve r044-r047: imitator-v008 (d877b6d0b31f) and arbiter-v007 (3d031639639f), after the redundancy batch — record and deploy with connector-limits v003." Both hashes are named. Gem's own words also restate "R-015, R-027 and R-028, and any ruling applying them, can't be vetoed" and the R-051 advisory-only interim. Only Gem approves changes to Imitator (R-015, R-027), and that is met.
   - Item 3 (Variant A) reads: "I approve connector-limits v003 variant A (proposals/2026-10-22-gvmw/connector-limits-v003.md, text hash 806a6fa315cb)". It also restates the 8:32pm gvmw words, which closes the restate condition from final-check.
   - The note added at 9:29:07pm (:47) reads: Gem picked "Variant A (keep gvmw as it is)" at 9:28pm (t72s401); "Variants B and C are **not approved**".
   - Info: the same message relays "Engineer reports the GitHub dead-man check is live and its test run passed". That's Engineer's claim, unverified, and outside this check.
6. **CHANGELOGs and index.**
   - codex/clone/CHANGELOG.md and codex/arbiter/CHANGELOG.md each have a pending-deploy row and a DEPLOYED row, both citing t72u item 2.
   - index.md:12 lists clone v008 as OK (LIVE) at 21:35:38, and :28 lists arbiter v007 as OK (LIVE) at 21:35:45.
   - index.md:65 lists Connector limits at v003, 2026-10-22, citing t72u item 3 and t72s401.
   - _shared/connector-limits/CHANGELOG.md:9 has row 3, "text 806a6fa315cb … base v002 (d4fbfa8f391f)", and a status row saying it's IN EFFECT from about 9:35:49pm.
7. **Verify scripts.** Neither script writes anything (0 write calls).
   - verify.py: "OVERALL: PASS" (17/37 strict matches; the rest are deleted profiles).
   - verify_shared.py: "MATCH _shared/connector-limits/v003.md == connector-limits-v003.md (23658 chars, text sha256 806a6fa315cb, file hash ok)", 10/10 match, "OVERALL: PASS".
8. **v003 A in effect.** It's recorded at codex/_shared/connector-limits/v003.md, the highest version.
   - Every live brief says "follow the shared connector limits … (highest version)", so v002 is superseded automatically.
   - v002.md stays as history. The CHANGELOG records base v002.
9. **imitator-v008 live text.**
   - It contains "R-015, R-027 and R-028, and any ruling applying them, can't be vetoed (… R-052)".
   - It also contains the R-051 interim: "…your 8:04pm grants are advisory only for retiring or merging bots, making a project public, deletions that need a backup and anything irreversible; you recommend and Gem decides."
   - imitator-v009:7 chains on d877b6d0b31f. Its text hash is still c92d31926a18.
   - Advisory: v009's header still says "codex v006 (latest…)". It should say v008 (live). That changes the file hash only.

## 10. Live inconsistency: the Apify, Extractor and Mediator gap (until item 5)
Live v003 A conflicts with the live briefs in several places:
- **Who runs Apify.** v003 rule 17 (:39) says "Emissary runs Apify actors in its collection lane … and Mender (with Mediator's duties) runs the spend check". :42 says "Emissary runs Apify (Extractor folded into Emissary, R-051…)".
  - Live Emissary (grok-bot v007) still says "Extractor only collects and scrapes the data" and sends "web data collection or scraping … back to Explorer". So Emissary has a rule power that its own brief tells it not to use.
- **Extractor's live brief conflicts.** Live Extractor (scraper v006) is still "web data-collection and scraping worker … builds, runs and maintains scrapers", and it follows the shared connector limits at the highest version, which is now v003.
  - v003 says Emissary runs Apify, and its NAMES line (:43) says "Extractor means Emissary". Extractor can't read that as being about itself while it still exists, so this is a real conflict for Apify runs.
- **The spend check.** v003 assigns it to Mender. Live Mediator (connector-steward v006) still tracks spend and isn't retired. The pointer "Mediator means Mender" assumes a merge that hasn't happened yet.
- **Advisory:** directory.md:34 and :36 still list grok-bot v006 and scraper v005; the codex has v007 and v006. Update directory.md.

**Is it safe in the meantime? Yes, because both conflicts fail closed.**
- Every Apify actor run costs money (v003:39), and spending without asking is $0 (R-051; spending is forbidden in every brief). So no bot may run an Apify actor without Gem's words for that run, whichever bot it is.
- Emissary's brief routes scraping to Explorer. Under v003, Extractor isn't the named Apify runner. So the likely outcome is that no Apify runs happen, which is safe.
- The only risk is duplication: both Mediator and Mender may track spend. That's harmless, because tracking only reads.
- Non-Apify scraping is unchanged: Extractor still does it, as before.

**Fix.** Until the redesign (item 5: emissary-v010, mender-v007 and the archive-first Extractor and Mediator retirements) is deployed, Explorer should route any Apify job to Gem, who names the runner. Better still, deploy item 5 next. Archivist could add a one-line interim note to connector-limits/CHANGELOG.md: "Until emissary-v010 is live, Extractor keeps its collection lane; no Apify run without Gem's words." That is Gem's or Archivist's call.

## Overall: PASS
The deploy is correct and recorded. The Apify, Extractor and Mediator gap is open but safe, and it closes when item 5 is deployed. The remaining order is GitHub 5h (item 4), then the redesign (item 5).

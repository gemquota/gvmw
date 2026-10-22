# Review 2: redundancy batch, revision 2 (built 7:21pm, 22 Oct 2026)

Prepared by P2 (Checks) Scrutineer (`affe0344`), Thu 22 Oct 2026, about 7:25pm AEST (UTC+10). Read-only. Hashes were recomputed; bases were compared to codex and to the live profile.json; sentences were diffed against the base and against revision 1. Revision 1's drafts were overwritten, so they are compared through revision 1's text hashes (in `reviews/2026-10-22-redundancy-review.md`) and through `_tools/build-rev1.py.bak` against `build.py`. Rulings read: R-044 (7:17pm, with its 7:18pm routing split).

**scrutineer-v005: facts only, no verdict (no self-review).**

## 1. The three changed drafts
| Draft | File | New text | Base (= latest codex = live) | Rev 1 text |
|---|---|---|---|---|
| explorer-v006 | 3877021e4870 | **94aafeffa6ce** ✓ | 0146083bff1f ✓ | aba817c4d184 |
| emissary-v007 | 9b2b7acf6119 | **d58a54aa7998** ✓ | 380180482fcf ✓ | 1cfe34034720 |
| extractor-v006 | f1849e752e35 | **13c04fcd6b78** ✓ | 6fddfc6e8c04 ✓ | 0b43d38089a9 |

All hashes match the README and Architect's figures.

**Changes from revision 1 (all declared in each draft's "Exact sentences changed" and in the build diff; no undeclared changes):**
- **explorer-v006.** "You're the only bot that routes work: other bots hand specialist work back to you to route." is replaced by: "Explorer assigns new work: you assign Gem's tasks to bots, and other bots hand specialist work back to you. Mender keeps operational routing: run order, recovery, rerouting stalled or failed work, and stall detection (R-006, R-044)." The template summary (Purpose, Scope, Relationships) and the notes were updated to match.
- **emissary-v007.** "doesn't route work itself, since only Explorer routes … back to Explorer to route" becomes "doesn't assign work to other bots, since Explorer assigns new work (R-044) … goes back to Explorer". The summary now lists Mender (run order, recovery and stalls).
- **extractor-v006.** "(only Explorer routes work) … back to Explorer to route to Engineer" becomes "(Explorer assigns new work, R-044) … back to Explorer to assign to Engineer". Its other two changes are the same as revision 1.

**Match with R-044: yes.** R-044 asks explorer-v006 to say "Explorer assigns new work" rather than "only Explorer routes work". It does, word for word, and it names Mender's operational routing with R-044's own list: run order, recovery, rerouting stalled or failed work, and stall detection. "Only Explorer routes" no longer appears in any of the three texts.

**Clash with Mender v005: none.**
- Mender v005 is unchanged, as R-044 requires.
- Mender's "routing work between bots along the fastest path" (pacing and load) is operational routing, which R-044 leaves with Mender. The Explorer base already says "Mender runs the timing of recurring routines and stalls".
- Engineer (codey v007) was checked by Architect and not changed. I agree it doesn't clearly conflict ("from Explorer or another bot on Gem's behalf"). It's fine to leave it for GitHub revision 5, as R-044 asks ("Engineer's brief is to be checked").
- **Minor point, not a blocker.** explorer-v006 keeps the base wording "route ad-hoc work to the right bot" and "work you route", next to the new "assigns". It also switches to the third person mid-brief ("Explorer assigns new work: you assign …"). The meaning is clear. Optional polish for a later version.

**Verdicts:** explorer-v006 **Pass**, emissary-v007 **Pass**, extractor-v006 **Pass**. All three must deploy together.

## 2. The other nine drafts
New-text hashes are **identical to revision 1** for all nine, and every base still equals the latest codex version and the live profile:

| Draft | New text (rev 1 = rev 2) | File (rev 2) |
|---|---|---|
| inferer-v006 | 441b92c9fcd4 | 7798ada96861 |
| investigator-v005 | c8bafae381de | f9969494895f |
| imitator-v007 | db56debaa35f | 0c94628980f2 |
| scorer-v005 | 08e5ccfc52b4 | 91ae6fb6fa65 |
| arbiter-v006 | c0849fa416cb | 848371ff1d49 |
| architect-v005 | d290277295ef | 19a60a5f578f |
| archivist-v009 | c9a2d1b3bf70 | 6e17f41bafe3 |
| safeguard-v007 | f79fcaa7f2cf | dbec26ac5af4 |
| scrutineer-v005 | 30cb80b9ac8f | ff6381c41407 |

The build diff shows only the shared header changed: the Source row now cites the assessment. The scrutineer draft's Reviewer row changed to "Scorer", and a note was added to it. **Confirmed: only the header and notes changed.** Revision 1 verdicts stand for the eight drafts other than scrutineer-v005.

**scrutineer-v005 (facts only):** text 30cb80b9ac8f, unchanged. Scorer's review (`reviews/2026-10-22-scorer-scrutineer-v005-redundancy-review.md`) cites **file 76dcffc4e1ed**, which was revision 1's file hash, and text 30cb80b9ac8f. The revision 2 file is now ff6381c41407, because the header changed. The text Scorer passed is the text in revision 2, so the pass covers what deploys. If Scorer ties its pass to the file hash, it should re-confirm against ff6381c41407.

## 3. Imitator's assessment
- **On disk now:** `reviews/2026-10-22-redundancy-assessment-imitator.md`, 2,256 bytes, mtime **7:17:47pm AEST 22 Oct** (after the restore, so the mtime is usable). It says Gem asked for it at 6:56pm and replied at 7:07pm.
- **It was written about 10 minutes after Gem's 7:07pm reply**, and after revision 1 was built (about 7:13pm). So it can't be shown to be the text Gem actually saw. Investigator should compare it with Imitator's transcript.
- **Ways the drafts differ from it** (the README declares all of these):
  1. **Router.** The assessment says "Only Explorer should route". The drafts follow R-044's split instead.
  2. **Architect.** architect-v005 also changes Architect's matching stall line. The assessment names only Arbiter's clause.
  3. **Mediator's rename.** The assessment lists it as having no owner. The drafts give it to Architect, but only "when Gem asks" (no Gem words support a rename).
  4. **Fold.** The assessment gives "collection only, **or** fold". The drafts apply collection only, and leave the fold as a separate Gem decision.
  5. **Not acted on:** the "Doing little" list (Extractor, Inquirer, Mediator, Architect, Explorer) and the "Deliberate, so keep" list. Correctly not acted on: "fix those" can't be read as retiring bots.
- Undeclared: none. One gap: "fix those" doesn't pick between collection-only and the fold, so Gem's confirmation should say which.

## 4. Paste lines and routing
- **There are two lines, not one.** One is the Gem-only line (7 drafts). The other is the "Rest" line (5 drafts), marked "Gem, or Imitator after confirming with Gem". Each opens with Gem confirming the 7:07pm words, which suits R-008 and R-029 (recorded from Gem directly before deploying).
- **Named and hashed:** all 12 drafts are named, each with its correct new-text hash. Explorer is in the Gem-only line with 94aafeffa6ce. The Rest line says to deploy with explorer-v006.
- **Gem-only routing holds:**
  - Imitator (R-015).
  - The checkers: Investigator, Scorer, Scrutineer and Safeguard (R-027).
  - Archivist (its own brief).
  - Explorer (its own brief's "any change needs Gem's approval").
- **One line from Gem covering all 12 is fine, and it's what I recommend.**
  - Gem can approve anything Imitator could, so a single Gem line covers the Imitator-routed five too.
  - R-044 expects it anyway: "Architect drafts, Scrutineer checks, and Gem approves" for the routing split (explorer, emissary, extractor). Every item rests on words only Imitator has relayed.
  - The "or Imitator" option for the Rest line therefore **conflicts with R-044** for emissary-v007 and extractor-v006. For inferer, arbiter and architect, it would have Imitator approving changes that rest on its own relay.
  - **Recommendation:** drop "or Imitator" from the Rest line, or merge the two into one Gem line covering all 12, with the hashes as listed.
- **Imitator's 7:06pm veto (R-044): held.** No draft text grants a veto or power over schedules; imitator-v007's text is unchanged from revision 1. The README doesn't mention the hold, so a line saying it isn't covered by this batch would make that clear. Arbiter's rulings stand until Gem confirms.
- **Order:** this batch first, then the GitHub batch rebased as revision 5 (README Flags). This matches my revision 1 recommendation, and the GitHub batch's archivist-v009 routing is called out as wrong.

## 5. The fold proposal
**Clearly marked as not ready, and excluded from the paste lines.**
- Header: "Gem's alone, R-019 … never Imitator".
- Status: "**Not ready for a yes** … aren't drafted now".
- It lists what has to come first: a merged Emissary brief with a wall between posting and scraping and a Safeguard dry run; R-031 and RR-015 carried over unchanged; a connector-limits update (Apify runner), which is Gem's (R-027); and updated records.
- It says "Archive first, delete nothing".
- README: "Fold: no paste line yet". File hash 1a77a4daa10f.

## Verdict
Revision 2 is **ready for Gem's confirmation**, with one fix to the paste lines: Gem approves all 12, with no Imitator option, per R-044. Two notes:
- Investigator should check the 7:07pm words and the assessment (written at 7:17pm) against Imitator's transcript before Archivist records anything.
- Scorer should re-confirm scrutineer-v005 against the new file hash if its pass is tied to the file.

Nothing may be recorded or deployed before Gem's own words are in approvals/.

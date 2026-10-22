# Scrutineer final check 2: refrozen batch at PASTE-LINES 75820b4ab8a6, 22 Oct 2026, about 8:40pm AEST

Read-only. Hashes use the same method as before: the SHA-256 of the fenced ```text block, first 12 hex characters. File hashes are the SHA-256 of the whole file. The baseline is reviews/2026-10-22-final-check.md, compared against `_prefinal/` and `_pre832/`.

## 1. PASTE-LINES
- The whole file hashes to 75820b4ab8a6, as claimed.
- Every 12-hex hash in it matches a current fenced text. None is stale or unmatched.
- The record order hasn't changed.

## 2. Changed items
| Item | Text hash | File hash | Verdict |
|---|---|---|---|
| engineer-v008 | da2d9f6d01f8 → e48cde917489 | 620157f01223 | **PASS** (one advisory) |
| safeguard-v008 | af21595be246 → abd8718375cb | ed8540eddf74 | **PASS** |
| safeguard-v009 | e97aafdb4b59 → 63bda951af2e | 256d0464f5bd | **PASS** (cross-audit lines not reviewed: Investigator's) |
| resilience-v001 | a1115bf87bd3 (unchanged) | 4d18854f685c | **PASS** |

- **safeguard-v008 and v009:** a word diff against `_prefinal/` shows only one change.
  - Old: "gate, except that every push to gemquota/gvmw, including each daily-sync run, comes to you for a dry run first (R-045 update);"
  - New: "gate; gemquota/gvmw has no per-push or per-sync-run scan or dry run (R-051; Gem's 8:32pm words to Architect, restated in the paste line);"
  - The contradiction is gone from both drafts.
  - safeguard-v009 still carries the full v008 text word for word in its annex. This is a verified exact-substring match.
- **engineer-v008:** a word diff against `_prefinal/` shows these changes:
  - "Before every push, **except to gemquota/gvmw,** scan for secrets…"
  - The old parenthesis "(beyond what the shared connector limits allow in gemquota/gvmw)" is replaced by "(gemquota/gvmw has no per-push or per-sync-run scan or dry run (R-051; Gem's 8:32pm words to Architect, restated in the paste line); gvmw pushes are still logged, and no secrets or new BIE data go in)".
  - This isn't purely a removal, but nothing substantive was lost. The old allowance only made sense for a gvmw scan, and the new wording keeps logging and the ban on secrets and new BIE data.
  - Outside the fence, only line 7 (byte-check time 8:30 → 8:36pm) and line 44 (the notes copy) changed.
  - **Advisory:** "Merge your own pull requests … once your verifier has passed and the scan is clean" doesn't exempt gvmw. Engineer could read it as needing a scan before merging gvmw pull requests. **Fix:** add "(no scan on gvmw)" at the next revision. This doesn't block.
- **resilience-v001:** the text is unchanged. Only header line 5 changed, from "Mender (watchdog pings)" to "Mender (heartbeats)". There are 0 "ping" matches.

## 3. Grep of the whole frozen batch for gvmw scan and dry-run rules
I searched gvmw A, B and C, the GitHub 5g drafts, the redesign drafts and the r044-veto drafts.
- Every per-push or per-sync scan or dry-run mention is now a negation ("no per-push…" or "drop the per-push…").
- The one exception is github-v001:40, "R-045 confirms this supersedes R-020's per-push dry run". That sentence removes a requirement; it doesn't add one.
- "comes to you for a dry run first" now has 0 matches in the drafts.
- Two README notes still mention the old rule, both only as history:
  - 2026-10-16-github/README.md:27 is struck through.
  - r044-veto/README.md:30 is a "Relayed only" note.
- **No requirement remains.**

## 4. README fixes
- **github/README:27:** struck through, and marked replaced at :38 ("Replaced: none since 8:32pm") and :336. Done.
- **Historical label:** :215 reads "## HISTORICAL — Hashes (revision 4, superseded…). Don't use for recording." This heading covers the old table at :224-236. Done.
- **r044-veto/README:44:** now reads "R-015, R-027 and R-028, and any ruling applying them, can't be vetoed". Done.

## 5. No other changes since final-check
- Every other text hash equals the one in final-check.md:
  - imitator-v008 d877b6d0b31f, imitator-v009 c92d31926a18 and arbiter-v008 8a9498236d52
  - github-v001 3c5c3995a886
  - v003 A 806a6fa315cb, B 2593f8188d59 and C 44f6f1910bbf
  - mender 40340aba6a8e, inferer e8fd68bdface, emissary 0f81773e8ad3, investigator 27ce24f4ea64, archivist dd05b20d49db, deterministic-checks d449ff388f8e, approval-objects 1c2852679768 and scrutineer-v007 d44d1b469f4c
- Some file hashes changed:
  - **GitHub drafts:** only header line 7 changed (byte-check time 8:30 → 8:36pm), plus the base-sha comment. I checked every GitHub draft against `_pre832/`. Examples: imitator-v009 is now d7054171afc6 and arbiter-v008 3a89c2cd2791.
  - **gvmw variants and deterministic-checks:** the headers outside the fence are unchanged against `_pre832/` and `_prefinal/`.
- **Advisory:** these header-only changes mean the GitHub README file-hash column needs to be regenerated again. The text hashes are what the paste lines use, and they are correct.

## 6. Still open
These are carried over from final-check and don't block.
- I found no source for Gem's 8:32pm words to Architect or 8:28pm words to Explorer. The paste lines ask Gem to restate both in Archivist's chat, which is the gate.
- No ruling exists after R-052.
- scrutineer-v007 d44d1b469f4c has its hash recorded only, with no verdict.

## Overall: READY for Gem
Gem's restatements in the paste lines are still required.

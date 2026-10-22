# Scrutineer review: refrozen batch (redesign revision 3, connector-limits v003 revision 9, imitator-v008/v009), 22 Oct 2026, about 8:35pm AEST

Read-only. Hashes are the SHA-256 of the fenced ```text block, first 12 hex characters. File hashes are the SHA-256 of the whole file. Times are AEST (UTC+10). Checked against R-051 and R-052 (rulings.md, the last two sections) and against my revision 2 review (reviews/2026-10-22-redesign-r2-review.md).

## 0. Hash tables
- **PASTE-LINES.md:** whole-file hash 9499872ef2c8, as claimed. Every 12-hex hash in it matches a current fenced text: the redundancy, r044, v003 rev 9, GitHub 5d and redesign rev 3 texts.
- **redesign/README.md:9-18:** all 10 text and file hashes match.
- **gvmw/README.md:104-106:** A 95debfabcf6d/4de9ca4031a3, B e264a37a37ca/65c26a0005ac, C 6369ac61aca4/d8351340e089. All match.
- **r044-veto/README.md:36:** imitator-v008 6163b07dd78b/40f0f3d4a3c7 matches. arbiter-v007 is unchanged (3d031639639f).
- **F1 (GitHub README file-hash column is stale):** 15 rows in 2026-10-16-github/README.md list old *file* hashes. Examples:
  - imitator-v009 at :51 lists 5aad70f7f044; actual da8cf883293b.
  - arbiter-v008 lists aa6a956663ba; actual f36db73a9489.

  Also affected: safekeeper, explorer, emissary-v009, extractor, mediator, mender, architect, scorer, scrutineer, investigator, inquirer, inferer and archivist. All *text* hashes, which are what the paste lines use, are correct. Only the file headers changed, so this doesn't block recording. **Fix:** regenerate the file column.

## 1. Redesign revision 3 (proposals/2026-10-22-redesign/)
**Revision 2 fixes:**
- **Self-check of Scrutineer's deploy: fixed.** deterministic-checks-v001:25 now says "Safeguard checks Scrutineer's deploys, and Scrutineer checks Safeguard's", and README.md:35 says the same.
- **Who pauses for cost: fixed.** mender-v007:22 says "For runaway cost, the bot responsible for the spend pauses it at once and tells you; you track it, and only Arbiter lifts a pause (R-051)". This agrees with the carried-over mediator text at :30.
- **Pointer to merged bots: fixed.** mender-v007:23 says "NAMES: a retired bot's name in any brief or shared rule means the bot it merged into (Mediator = Mender, Scorer = Scrutineer, Safekeeper = Safeguard, Inquirer = Inferer, Extractor = Emissary; R-051)". The same pointer is in every merged brief, deterministic-checks and archivist.
- **Unused version numbers: only partly fixed (F2).** scrutineer-v007:5 notes "unrecorded v005–v006 skipped". Six headers still name unrecorded versions as the base, with no "unused" note:
  - mender-v007:5 "mender/ v006 → v007" (codex has v005)
  - safeguard-v009:5 "v008 → v009" (codex v006)
  - inferer-v008:5 "v007 → v008" (codex v006)
  - emissary-v010:5 "v009 → v010" (codex v007)
  - investigator-v007:5 "v006 → v007" (codex v004)
  - archivist-v011:5 "v010 → v011" (codex v008)

  The README explains it, so this is advisory. **Fix:** use scrutineer-v007's wording in all six.
- **Investigator's D5 fix: done.** mender-v007:27 now reads "Scrutineer's assessments/YYYY-MM-DD…", "(Scrutineer scores and reviews, Architect, the approver, Archivist [R-051])" and "Scrutineer (scores, then reviews [R-051])". A word diff against mender-v006 (c726aaac1ab3) shows these [R-051] edits are the only changes.
  - Info: mender-v007:30 (the carried-over mediator text) still says "Share cost data with the (Checks) Scorer and (Checks) Scrutineer". The NAMES pointer at :23 covers it.

**Nothing lost:** every other carried-over text is still verbatim:
- mediator-v007 345b94138142
- safeguard-v008 2aabcb9d416a and safekeeper-v006 63f17cc83cca
- inferer-v007 65660cac2123 and inquirer-v005 caf7cce419da
- emissary-v009 db12061dc422 and extractor-v007 3a5554d96379
- investigator-v006 c14cca83ac11
- archivist-v010 f7c447d262e0

**Approver:** all are Gem-only (:1 and :8 of each file). No new contradictions with R-044 to R-052 were found.

| Draft | Text / file | Verdict |
|---|---|---|
| mender-v007 | a4fdbd11b16b / c81642f2c919 | **PASS** (F2 advisory) |
| safeguard-v009 | b71d644b5161 / 6e1ac4c57356 | **PASS** (F2 advisory) |
| inferer-v008 | ca342fc6cfc9 / 25f47e6067b7 | **PASS** (F2 advisory) |
| emissary-v010 | f0371f2dd775 / e3d0e805a87a | **PASS** (F2 advisory) |
| investigator-v007 | 15de2afd1c8e / 109a2ec07214 | **PASS** (F2 advisory) |
| archivist-v011 | 7a08e3b058d6 / 197ef75c954f | **PASS** (F2 advisory) |
| deterministic-checks-v001 | 0e93d5ae1a6a / e4cea617fa6e | **PASS** |
| approval-objects-v001 | 1c2852679768 / aa9a7fdcb4d2 (unchanged) | **PASS** |
| resilience-v001 | 91c0da0bb06f / 059fe27b555c (unchanged) | **PASS** |
| scrutineer-v007 | b15dc0bf90ba / ac6d38914be3 | **No verdict.** Safeguard checks it. Hashes recorded only |

## 2. connector-limits v003 revision 9 (proposals/2026-10-22-gvmw/)
- **Fixed.** A:49 and B/C:50 now read: "Emissary runs Apify actors in its collection lane, under its brief, and Mender (with Mediator's duties) runs the spend check (Gem's answers in Inquirer's chat at 8:09, 8:12 and 8:13pm, relayed via Inquirer, R-051, R-008…)".
- "Extractor runs" and "Mediator's spend" appear 0 times in each variant.
- The auto-sync fix from revision 8 is still in place.

| Variant | Text / file | Verdict |
|---|---|---|
| A | 95debfabcf6d / 4de9ca4031a3 | **PASS** |
| B | e264a37a37ca / 65c26a0005ac | **PASS** |
| C | 6369ac61aca4 / d8351340e089 | **PASS** |

## 3. imitator-v008 and imitator-v009
- **Hashes:** v008 6163b07dd78b / 40f0f3d4a3c7 (claimed 6163b07dd78b). v009 279abd886724 / da8cf883293b (claimed 279abd886724).
- **R-051:** done. imitator-v008:19 and :40 (and v009:34) carry "INTERIM (R-051; … "Advisory only for big or irreversible decisions"): until Gem answers on scope, your 8:04pm grants are advisory only for retiring or merging bots, making a project public, deletions that need a backup and anything irreversible; you recommend and Gem decides."
- **R-052 pass/fail test: FAIL.** The exact phrase "and any ruling applying them" appears in **neither** draft (0 matches). The veto exclusion reads, at imitator-v008:19 and :40 and imitator-v009:34: "R-015, R-027 and R-028 can't be vetoed (Gem, 8:25pm in Investigator's chat, "I guess", relayed by Investigator; Gem restates it in the paste line, R-008)."
  - R-052 rules that the veto "doesn't reach R-015, R-027 or R-028, **or any ruling applying them**". Without that phrase, Imitator could veto a later ruling that applies R-015, R-027 or R-028 to Imitator, which is the self-interest gap R-052 closes.
  - **Fix:** "R-015, R-027 and R-028, and any ruling applying them, can't be vetoed (…; R-052)." Then re-hash v008, rebuild v009 and update both READMEs and PASTE-LINES.
- **Chain:** v009 chains correctly onto the new v008. GitHub README.md:51 gives the base as 6163b07dd78b. A word diff of v009 against v008 shows only the revision 5 GitHub additions: the R-020 Engineer exception, "never commit… On GitHub you read…", and the gist, deletion and visibility list.

| Draft | Verdict |
|---|---|
| imitator-v008 | **FAIL** (R-052 phrase missing) |
| imitator-v009 | **FAIL** (inherits it) |

## 4. Record order and paste-line hashes
- **Order unchanged, chains OK:**
  1. imitator-v007 db56debaa35f
  2. imitator-v008 6163b07dd78b, then arbiter-v007 3d031639639f
  3. v003 rev 9
  4. GitHub 5d: github-v001 7a1c70ebd117, engineer-v008 dda5eeb9977d, imitator-v009 279abd886724 (on 6163b07dd78b), explorer-v007 a98d235b093a, architect-v006 c2e149404e57, arbiter-v008 8a9498236d52 (on 3d031639639f), message-verification-rule-v005 c78245bcf145
  5. redesign rev 3
- Every paste-line hash matches its file.
- **Result: PASS on order and hashes.** Recording is still blocked by the imitator FAIL in §3. Fixing it will change hashes in §2 and §4 of PASTE-LINES.

## 5. approvals.md row 26
- **Confirmed.** approvals.md:26 now reads: "…so the schedule power is live. Each change must be flagged in the digest. Imitator doesn't change the schedules of Investigator, Scorer, Scrutineer, Safekeeper or Safeguard without Gem's words for that change (R-046, R-048). | Investigator 20:00 |"
- Against the backup /workspace/backups/approvals-20261022-2024.md, only row 26 changed, plus one appended row (:32, 20:25, Gem's "I guess" to Investigator).

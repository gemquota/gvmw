# Review: connector-limits v003 (gvmw exception), proposals/2026-10-22-gvmw (revision 2)

Reviewer: Scrutineer (independent, read-only), Thursday 22 Oct 2026, about 6:54pm AEST (UTC+10).

**How this was checked:**
- **Hashes:** `sha256sum` for files. Text hashes come from the content of the one text block, with no trailing newline.
- **Rules:** compared line by line against the text block of codex v002.
- **Git:** read-only, using the local clone `/workspace/_repo-sync/gvmw.tmp`. It's clean, and its HEAD equals the remote.
- **Remote:** `git ls-remote` with no credentials, plus unauthenticated public GitHub API GETs.
- **Not done:** I read no file content from the identity notes, and nothing from /home/box/id-private or any Sensitive context section.
- **File times:** the proposal files date from after 6:39pm, so they're reliable (INC-008).

## Verdict: READY WITH FIXES (all three variants)
The hashes, the base and the diffs are clean, and Gem's quotes are exact. Four drafting fixes are needed before Gem sees it (section 7). The main one is that the exception and the paste lines don't name Gem's own identity notes, which are public in gvmw.

## 1. Hashes and diffs

| File | Expected | Found | Result |
|---|---|---|---|
| A (default), file / text | e162aaf4431f / 998c679c9e1c | e162aaf4431f… / 998c679c9e1c | MATCH |
| B, file / text | 715065eb5f4b / b5b971e5c294 | 715065eb5f4b… / b5b971e5c294 | MATCH |
| C, file / text | 22531b2f19c7 / 5afd3f141029 | 22531b2f19c7… / 5afd3f141029 | MATCH |
| Base: codex v002.md | text d4fbfa8f391f | file c290e699516b (unchanged since 16 Oct), text d4fbfa8f391f | MATCH |

**Each variant against v002, rule by rule:**
- **A:** the header line ("v002" becomes "v003") and rules 6, 14, 15 and 18. Every other line is byte-identical.
- **B and C:** the header line and rules 6 and 14. Rules 15 and 18 are identical to v002.
- **Every change is an insertion,** and all are declared in the README table. There are **no undeclared changes.**
  - Rule 6 adds: "The only exception is gemquota/gvmw under rule 14's gvmw exception; it doesn't cover posting, publishing or scheduling through postiz, Zapier, n8n, Notion, Todoist, Supabase, Obsidian, Gmail, X or any other channel."
  - Rule 14 adds the gvmw exception paragraph. It pins commit 4f43fc9ae82e…, includes the R-031 sentence and the no-roll-forward line, and gives the review date of 22 Nov with Safeguard as owner.
  - Rule 15 (A only) adds: ", except third-party contact details already in gemquota/gvmw under rule 14's gvmw exception".
  - Rule 18 (A only) adds: " (rule 14's gvmw exception covers only contact details already in gemquota/gvmw)".

**The variants differ only where declared:**
- **A against B:** only rule 14's scope clause changes, to "…including its governance/ folder and its BIE and gambling data, but not third-party contact details: those are removed from the public copy or moved to a private repo, on Gem's direct words and a Safeguard dry run (rules 13 and 14), and they stay in the git history until Gem decides on a history rewrite". B also drops A's rule 15 and 18 insertions.
- **A against C:** the same, with governance/ also dropped from the scope.

## 2. Gem's quotes

**Lines 61 to 63 of `approvals/2026-10-16-gem-direct-words.md`** (mtime 6:48:37pm, which is reliable) match the README character for character:
- **Line 61,** 6:45pm, Mediator's chat: "No, I made gemquota/gvmw public on purpose, leave it"
- **Line 62,** 6:47pm, Mediator's chat (t33u): "Change the rule"
- **Line 63,** 6:48pm, to Safeguard: "Leave gvmw public as it is, I accept the risks"

**Line 63 has no "Recorded by" heading of its own.** It sits under Mediator's 6:46pm section. R-042 (6:49pm) confirms it as Gem's own words in Safeguard's chat, and that's the authority it rests on. Archivist may want to give it a proper heading.

**Is "Gem's 6:48pm stated preference" recorded? Yes, but only as a preference about the repo's state, not as a choice of variant A.** "Leave gvmw public as it is" fits A, which keeps everything as of 4f43fc9. It doesn't choose between A, B and C by name. The README says as much ("They cover the repo's current state, not this rule text"), and the paste lines require Gem to name a variant, so this is handled correctly.

**Do A's rules 15 and 18 go beyond Gem's words?**
- **Rule 15: within what Gem said.** Safeguard's card listed "third-party contact details", and Gem accepted the risks "as it is". But "already in gemquota/gvmw" isn't pinned to 4f43fc9 in the rule's own words. It relies on the cross-reference to rule 14. **Fix: add "as of commit 4f43fc9".**
- **Rule 18: slightly beyond, and ambiguous.** Nothing on disk shows that any contact details in gvmw came from X. The parenthetical can be read as an exception for personal data drawn from X, which Gem never discussed. **Fix:** either drop the parenthetical, or reword it so it grants nothing. For example: "Nothing from X is covered by rule 14's gvmw exception."
- **governance/:** line 63 says the card listed it "later". From disk, I can't tell whether governance/ was on the card before Gem answered.
  - **A** names governance/ in its paste line, so Gem's approval of A settles this explicitly. Good.
  - **B** keeps governance/ public as well, and its paste line names it too.

## 3. Pinning to commit 4f43fc9

**Remote state, from `git ls-remote https://github.com/gemquota/gvmw.git` at about 6:53pm:**
- HEAD and refs/heads/main both point to **4f43fc9ae82eb1beaf63bf4ea33fcd699aae5adf**.
- There's only one branch, with no tags and no releases (API).
- has_pages is false, forks_count is 0, and visibility is public.
- created_at is 2026-10-16 05:58:52Z (3:58:52pm AEST); pushed_at is 2026-10-22 08:42:26Z (6:42:26pm AEST).
- gemquota's only public gist is from 31 July and unrelated.

**History:** 35 commits, strictly linear (`rev-list --count` equals `--first-parent --count`, both 35).
- e21adc3: the snapshot of 16 Oct, 3:54pm AEST.
- **33 commits, e82af0c to 5b6581c,** made on **18 Oct, 5:19:34am to 9:30:51am AEST**.
  - Authored and committed as "gemquota <gemquota@gmail.com>", and linked to the gemquota login.
  - Which bot or person made them is still unknown (R-040, R-041 item 6).
  - **They touch only medb-research/:** 33 files, 5,170 insertions.
- 4f43fc9: 22 Oct, 6:42:24pm AEST, "Sync workspace changes since 16 Oct (add/modify only…)".
  - Mostly governance/: 59 files in cartography, 15 in _archive, 8 in codex, and a few others.
  - Also 2 vepa files.

**Coverage:**
- **The 33 commits and the current HEAD are covered.** All of them are ancestors of 4f43fc9, and 4f43fc9 is HEAD now.
- **Nothing in gvmw falls outside the pinned exception today:** no other ref, tag, release, Pages site or fork.
- **Two caveats:**
  1. The rule pins content "as of" 4f43fc9, which includes all earlier history. Variants B and C leave the removed items in the history, which the text says plainly ("stay in the git history").
  2. Pinning legitimises the *content* of 4f43fc9. It doesn't settle whether pushing it was a breach (R-043: Engineer's claimed 6:41pm words aren't verified). Nor does it settle who made the repo public (R-040, R-042). v003 should say so, so the approval isn't read as clearing those questions.

## 4. Is "approval counts as R-031 permission" explicit enough?
**Not quite.**
- **R-031 needs Gem's words naming the file and the destination.** v003 says "the bonus_terms source files", which is a category, not a list of files. At 4f43fc9 the matching files are:
  - `bie_tools/bonus_terms_AU.csv`, `bie_tools/bonus_terms_AU.xlsx` and `bie_tools/pstats/bonus_terms_AU.*`: rows, anomalies, dups, meta and summary JSON, plus `k_bonus_terms_au.py`;
  - `bie_deliverables/reports/bonus_terms_AU.csv` and `.xlsx`;
  - the bonus-site reports in `bie/` and `bie_deliverables/scraper/`.
  In total there are 325 paths under bie*/.
- **`bonus_scores_AU.xlsx` itself is not in gvmw** at 4f43fc9: no path matches "score" outside governance/. R-042 already states that R-031 still applies to it.
- **R-042 has already lifted the R-031 hold for files already committed to gvmw.** That rests on Gem's 6:48pm words. v003's sentence repeats this rather than creating it, so it should cite R-042.

**Fix:** replace the sentence with:

> "For this repo only, Gem's approval also counts as the R-031 permission (as in R-042) for the bonus_terms and BIE files already in it at 4f43fc9: everything under bie/, bie_deliverables/ and bie_tools/, including the bonus_terms_AU files. bonus_scores_AU.xlsx isn't in the repo, and R-031 still applies to it and to every other destination."

The paste lines should say "bonus_terms and BIE files at 4f43fc9 (my R-031 permission)".

## 5. Conflicts with the rulings, the review owner, and future pushes
- **R-036 (Gem's words for each push to a public repo): no conflict.** v002 rule 14's sentence "Until the shared GitHub rule is recorded, any GitHub push… needs Gem's direct words naming it and a Safeguard dry run" stays. The exception adds a scan, a dry run and a read-back.
  - Wording risk: "every sync push gets a Safeguard dry run first" could be read as making the dry run enough on its own.
  - **Fix:** add "and Gem's words as rule 14 and R-036 require; a dry run is never a go-ahead".
- **R-037 (Vercel):** no overlap. Rule 2 is unchanged.
- **R-039 (Mediator's repos stay private under DayneK):** no conflict. gvmw is gemquota's, and R-042 governs it.
- **R-040:** matches. Rule 14 carries the read-back by the pushing bot, confirmation by a second bot, the Safekeeper scan of every push and the auto-sync pause.
- **R-041:** point 2 has been superseded by R-042, and v003 is consistent with R-042.
- **R-042:**
  - **Matches** on current contents only, no new content, no other destination, and automatic pushes paused until Gem's words cover pushes to a public repo.
  - **Gap:** R-042's "any file not already in gvmw" covers *all* new content. v003's no-roll-forward line covers only "new BIE, gambling or third-party contact content".
- **R-043:** pinning covers the content but should say it doesn't settle the breach question (section 3).
- **github-v001** (still a draft) bars BIE data from every repo. It's listed in the follow-ups, and its revision 5 needs the same exception. Good.
- **The 22 Nov review has an owner:** "Safeguard reviews this exception by 22 Nov 2026 and puts it back to Gem." It doesn't say what happens if Gem hasn't answered. **Suggest:** "it stays as is until Gem decides", so the exception doesn't lapse unnoticed and set off false breach reports.
- **Does rule 6 still bar future pushes?**
  - **Yes, for BIE and gambling content:** rule 6's ban still covers every channel, with the one pinned exception, and new BIE content needs Gem's fresh words.
  - **Not for other content:** new governance/ files, new identity notes or other personal data about Gem would be held back only by rule 14's per-push words and the dry run, not by any content rule. Example: `id-investigator/imitator-accuracy-2026-10-22.md` exists on the box but isn't in gvmw yet, so the next sync would add it.

## 6. The identity-notes gap
**Gem's identity notes in gvmw at 4f43fc9** (names only):
- `id-investigator/factcheck-2026-10-10.md`
- `id-notes/projects-map-2026-10-10.md`

Neither was changed after e21adc3: their only commit is the 16 Oct snapshot. Also public, under governance/, are Gem's recorded words (`governance/approvals/*-gem-direct-words.md` and three `_archive` backups) and `governance/approvals.md`.

**Gem's words:**
- **16 Oct, 3:47pm:** "Include both" (BIE data and the identity notes) was for a repo then meant to be **private**.
- **16 Oct, 3:57pm:** "private gemquota/gvmw".
- **22 Oct, 6:48pm:** "as it is" covers the current state, under R-042. That arguably includes the identity notes.

But Safeguard's card, as recorded, listed gambling data, contacts and "later" governance/. **It didn't list the identity notes**, and no paste line names them.

**Which rule should cover them:**
- **Rule 14's exception, not rule 6.** Rule 6 is about posting and gambling content.
- **What to add:** name the identity notes in the scope, as "Gem's own identity notes in id-investigator/ and id-notes/ at 4f43fc9", and extend no-roll-forward to them. Any new identity notes or other personal data about Gem would then need Gem's fresh words and a dry run.
- **Then** each paste line should say whether the identity notes stay public, so Gem decides it knowingly.
- **This isn't optional:** they're Gem's personal data, now in a public repo, and not named in any approval.

## 7. Ready for Gem? Not yet. Fixes needed, in all three variants
1. **Identity notes:** name them in rule 14's scope and paste lines, and extend no-roll-forward to them and to all new content, matching R-042 (section 6).
2. **R-031:** name the files and folders, cite R-042, and say bonus_scores_AU.xlsx is excluded (section 4).
3. **Rules 15 and 18 (A only):** pin rule 15 to 4f43fc9. Drop rule 18's parenthetical, or make it plainly grant nothing.
4. **Variants B and C:** say whether Gem's approval of the variant is itself the "direct words" for removing the content, so only the dry run remains, and who does it (Engineer, per follow-up 2). Also say how the content stands until it's removed. Without the exception for contacts, they're in breach of rule 15 until then.

Smaller fixes:

5. Add the R-036 phrase to the sync sentence: Gem's words for each push, and "a dry run is never a go-ahead".
6. Say v003 doesn't settle R-043's breach question or who made the repo public.
7. Say what happens after 22 Nov if Gem hasn't answered.
8. Give line 63 of the approvals file its own "Recorded by" heading (Archivist's job, not Architect's).

# Re-review 2: connector-limits v003 (gvmw exception), revision 2

Reviewer: Scrutineer (independent, read-only), Thursday 22 Oct 2026, about 6:58pm AEST (UTC+10).

How I checked it:
- Hashes: `sha256sum` for files; text hashes computed in memory (the content of the text block, with no trailing newline).
- Revision 1 was rebuilt in memory from `_tools/build-r2.py.bak`, with every write redirected to memory, so nothing was written. It reproduced the revision 1 text hashes 998c679c9e1c, b5b971e5c294 and 5afd3f141029.
- The revision 2 files were written at 6:55:46pm, after the restore, so their times are reliable.

## Verdict: READY for Gem, all three variants
- All four fixes and all three smaller points are applied.
- One wording update is recommended now that R-043 is final (section 4).
- I also recommend one safeguard for the contacts listed as a category in B and C (section 3).
- Neither blocks Gem.

## 1. Hashes, base and diff

| File | Expected | Found | Result |
|---|---|---|---|
| A, file / text | 19f8b999b0b8 / 2405e7b493f8 | 19f8b999b0b8… / 2405e7b493f8 | MATCH |
| B, file / text | 5dcb15141cc6 / c1a93deacf1f | 5dcb15141cc6… / c1a93deacf1f | MATCH |
| C, file / text | b0c4062f151d / 26d877e80a94 | b0c4062f151d… / 26d877e80a94 | MATCH |
| Base: codex v002.md text | d4fbfa8f391f | d4fbfa8f391f (file c290e699516b, unchanged) | MATCH |

Against v002:
- **A** changes the header line and rules 6, 14 and 15. Rule 18 is now byte-identical to v002.
- **B and C** change the header line and rules 6 and 14.

Against revision 1:
- **A** changes rules 14, 15 and 18 (18 goes back to v002's text).
- **B and C** change rule 14 only.
- **Outside the text:** a Notes line now says "…rules 6 and 14 and 15" instead of "…15 and 18". A new Notes line says "v003 doesn't settle R-043 or who made the repo public. Line 63 of the approvals file has no "Recorded by" heading…". The B and C Notes lines are reworded.
- **No undeclared changes.** Rule 6 is unchanged since revision 1.
- The variants still differ only in rule 14's scope clause and B and C's removal sentence, plus A's rule 15 insertion.

## 2. The four fixes and three smaller points

| # | Item | Status | New text (A unless stated) |
|---|---|---|---|
| 1 | Identity notes in scope, and no rolling forward of any new content | **FIXED** | "…and Gem's own identity notes id-investigator/factcheck-2026-10-10.md and id-notes/projects-map-2026-10-10.md." Also: "the exposure of Gem's own identity notes; that's Gem's own call". And: "any new content, of any kind, including any new identity notes or other personal data about Gem, needs fresh direct words from Gem and a Safeguard dry run (R-042)." All three paste lines name both files ("my identity notes id-investigator/factcheck-2026-10-10.md and id-notes/projects-map-2026-10-10.md") |
| 2 | R-031: name the files, cite R-042, exclude bonus_scores | **FIXED** | "For this repo only, Gem's approval also counts as the R-031 permission (as in R-042) for the bonus_terms and BIE files already in it at 4f43fc9: everything under bie/, bie_deliverables/ and bie_tools/, including the bonus_terms_AU files. bonus_scores_AU.xlsx isn't in the repo and isn't covered; R-031 still applies to it and to every other destination." The paste lines say "(my R-031 permission; not bonus_scores_AU.xlsx)" |
| 3 | Rule 15 pinned; rule 18 neutralised (A) | **FIXED** | Rule 15: "…except third-party contact details already in gemquota/gvmw as of commit 4f43fc9, under rule 14's gvmw exception". Rule 18: the bracket is removed, and the rule is byte-identical to v002 |
| 4 | B and C: approval counts as the words for removal; status until removed | **FIXED** | B: "Gem's approval of this rule counts as Gem's direct words to remove the third-party contact details from the repo's current tree only; a history rewrite needs separate words from Gem, and until then they remain in the git history. Engineer removes them, after making a backup first (a private copy on the box), a secret scan and a Safeguard dry run. Until they're removed, they stay as they are and nothing is added to them." C says the same about "the third-party contact details and the governance/ folder". The paste lines say "remove … from the current tree (backup, scan and dry run first; no history rewrite)" |
| a | R-036: Gem's words for each push, and a dry run is never a go-ahead | **FIXED** | "every push needs Gem's words for that push as this rule and R-036 require, and a Safeguard dry run first; a dry run is never a go-ahead." The auto-sync sentence now reads "…until Gem's words cover automatic pushes to the public repo (R-040, R-042)" |
| b | Doesn't settle R-043 or who made the repo public | **FIXED**, but now out of date (section 4) | "This exception doesn't settle R-043 (whether the 4f43fc9 push was a breach) or who made the repo public." |
| c | What happens after 22 Nov | **FIXED** | "If Gem hasn't decided by then, the exception stays in force and nothing is removed automatically, and Safeguard raises it with Gem in Explorer's daily digest until Gem decides." |

## 3. Contacts named as a category in B and C: acceptable, with one safeguard
**Why it's acceptable:**
- The removal is from the current tree only, a backup goes on the box first, and the history keeps everything, so it can be undone.
- Engineer does the removal after a secret scan and a Safeguard dry run. Rule 13's backup-first step is met.
- Gem's approval of B or C names the category and the repo, so it's direct words for that item.
- Nothing is added in the meantime.

**The risk:** without a list of paths, a removal could miss files or take too much. For example, a BIE file that also holds contact columns would then be both "BIE data, kept" and "contacts, removed".

**Recommended safeguard** (one sentence in B and C, or a condition on the dry run):
- Safeguard's dry run lists the exact paths, plus any file that mixes BIE data with contact details.
- That list is saved on the box before removal.
- Any mixed or unclear file goes to Gem before it's removed.

This is a recommendation, not a block.

## 4. R-043 is final: is v003 consistent?
**The ruling** (rulings.md line 345, mtime 6:55:06pm): "R-043 final (6:55pm): Gem confirmed in Arbiter's chat at 6:54pm: "Yes, I told Engineer to sync gvmw both ways at 6:41pm". The 4f43fc9 push had Gem's words, so it's not a breach of R-036. What remains is two process gaps for Engineer: no Safeguard dry run or notice (R-020), and no visibility read-back… Automatic recurring pushes to the now-public repo still wait on Gem's answer to Arbiter's card, and every push needs a Safeguard dry run first and a read-back after."

Gem's words are recorded at `approvals/2026-10-16-gem-direct-words.md` line 64 ("22 Oct 2026 6:54pm AEST, Gem's own words in Arbiter's chat (widget)"), and they match exactly.

**Consistency:**
- **There's no contradiction.** v003's pin to 4f43fc9, its pause on automatic pushes, the per-push dry run and the read-back by a second bot all match R-043 final.
- **v003 is a little stricter.** It needs Gem's words for every push, where R-043 says "A sync Gem asks for is covered". That's the same thing when Gem asks for each sync, and the stricter reading wins anyway. Fine.
- **One sentence is out of date.** "This exception doesn't settle R-043 (whether the 4f43fc9 push was a breach)" is still literally true, but it reads as if the question were still open. The README (line 16) repeats it. Suggested wording: "R-043 (final) settled the 4f43fc9 push: Gem's words covered it, leaving two process gaps for Engineer. This exception doesn't settle who made the repo public."
- **If the text changes, the hashes and paste lines change too.** Gem must approve the new hash. If Architect would rather not rebuild, the current text is acceptable as it stands.

## 5. Ready for Gem?
**Yes, all three variants are ready.** These are recommended but optional:
1. Update the R-043 sentence (section 4).
2. Add the path-list safeguard for B and C (section 3).

If either is applied, the hashes and paste lines must be rebuilt before Gem pastes.

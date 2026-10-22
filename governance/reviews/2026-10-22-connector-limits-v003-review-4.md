# Re-review 4: connector-limits v003, revision 4

Reviewer: Scrutineer (independent, read-only), Thursday 22 Oct 2026, about 7:19pm AEST (UTC+10).

**Method:**
- **Hashes:** `sha256sum` for files. Text hashes come from the text block's content, with no trailing newline.
- **Revision 3:** rebuilt in memory from `_tools/build-rev3.py.bak`, with writes redirected to memory. It reproduced 47fe3f8dcbc1, e6490c18768f and 970ee0c7df6a.
- **File times:** the revision 4 files were written at 7:17:07pm, after the restore, so the times are reliable.

## Verdict: READY for Gem (all three variants)
- Every review-3 item and both review-2 optional edits are applied.
- One improvement is recommended: snapshot the list of "people Gem already shares with" (section 4). It doesn't block.

## 1. Hashes, base and diff

| Variant | File | Text (expected / found) | Result |
|---|---|---|---|
| A | bc4bba386c16… | 64666a8425b1 / 64666a8425b1 | MATCH |
| B | 34e217fca5c4… | 8784cf5d103b / 8784cf5d103b | MATCH |
| C | 38337ec51a9f… | 3af413fa153b / 3af413fa153b | MATCH |
| Base v002 | c290e699516b, unchanged | d4fbfa8f391f | MATCH |

**Against revision 3:**
- **A** changes rules 9, 11 and 14, and LIMITS.
- **B and C** change the same, and their rule 14 also gets the path-list sentence from review 2.
- **Notes:**
  - The amendment line now ends "…in rules 9 and 11 and LIMITS".
  - The rules 9, 11 and LIMITS line is rewritten.
  - The R-043 line is updated.
- **All of these are declared by Architect. No undeclared changes.**

**Against v002:**
- **A** changes the header line and rules 6, 9, 11, 14 and 15, and LIMITS.
- **B and C** change the header line and rules 6, 9, 11 and 14, and LIMITS.

**Variants:** B and C still differ from A only in rules 14 and 15. Rules 9 and 11 and LIMITS are identical in all three.

## 2. Review-3 items and the review-2 optional edits

| Item | Status | New text |
|---|---|---|
| Rule 11, Mem0 only | **FIXED** | "Emissary and Explorer may add Mem0 memories once Mem0 works (it doesn't yet: no key) (Gem's direct words, 22 Oct 2026); this doesn't cover Notion's memories or any other memory store. No other bot adds memories, and no bot changes or deletes them without Gem's direct words." |
| Rule 11, purpose requirement dropped | **NOTED** | Notes: "v002's need for Gem to name what each writer is for is dropped, as Gem named only the writers" |
| Rule 9, who and how | **FIXED** | "Explorer may share a Notion page or Todoist task that is its own with people Gem already shares with in that workspace… Publishing to the web, inviting or sharing with anyone new, and assigning a task to anyone other than Gem keep the gate above." |
| Rule 9, dry run | **FIXED** | "…without per-item words from Gem but with a Safeguard dry run for each share." |
| Rule 9, own items | **FIXED** | "Explorer keeps a log on the box, like rule 16's, of the id and time of each page or task it creates and of each share (what, with whom, when); only items logged as Explorer's count as its own." |
| LIMITS conflict | **FIXED** | "The one named carve-out: Explorer's sharing under rule 9, on Gem's direct words to Architect at 7:10pm on 22 Oct 2026, "Yes, Emissary and Explorer can write to Mem0 and Explorer can share Notion/Todoist; add it to v003", needs no per-item words from Gem; it still needs a Safeguard dry run for each share." The quote matches README line 19 exactly |
| Recording Gem's 7:10pm words | **HANDLED** (section 5) | Every paste line opens: "I confirm I told Architect at 7:10pm on 22 Oct: 'Yes, Emissary and Explorer can write to Mem0 and Explorer can share Notion/Todoist; add it to v003'." |
| Review 2, optional edit 1: R-043 | **APPLIED** | "R-043 (final) settled the 4f43fc9 push: Gem's words covered it, leaving two process gaps for Engineer. This exception doesn't settle who made the repo public." |
| Review 2, optional edit 2: B and C path list | **APPLIED** | "Before anything is removed, Safeguard's dry run lists the exact paths to be removed, saved on the box, and any file that mixes BIE data with contact details goes to Gem before it's touched." |

Note on rule 9: revision 3's "it created for work Gem asked for" is now "that is its own" (meaning logged as Explorer's). Nothing is lost. Rule 9 already lets Explorer create items only "for work Gem asked for in Gem's direct words", so every item it logs as its own is already Gem-requested work.

## 3. Why have a LIMITS carve-out if the dry run is kept? Does it waive anything Gem didn't say?
- **It isn't a dry-run waiver,** so "this rule has no dry-run waivers" stays true.
- **What it changes is the line "it never replaces Gem's approval".**
  - Without the carve-out, each share could be read as still needing Gem's approval for that item.
  - LIMITS also says "A dry run is never a go-ahead". Without the carve-out, it could look as if the dry run were standing in as the go-ahead.
- **The carve-out makes clear that the go-ahead is Gem's standing 7:10pm words.** The dry run remains only a check, and "If Safeguard raises a concern or hasn't replied, stop and ask Gem" still applies.
- **What it waives:** only per-item words for Explorer's own items shared with existing people.
- **Is that within what Gem said?** Yes. A blanket "Explorer can share Notion/Todoist" can't reasonably mean "with your words for each item", since that's what v002 already allowed.
- **Nothing else is waived.** Publishing, new people, task assignments and other bots all keep v002's gate.
- **The carve-out isn't strictly necessary,** but it's sound and removes an apparent contradiction. **Acceptable.**

## 4. Can "people Gem already shares with in that workspace" be checked?
**Partly.** There's a read-only source for each service:
- **Notion:** workspace members and page permissions (for example, the connector's user listing and page sharing data).
- **Todoist:** each project's collaborators (`find-project-collaborators`).

Safeguard can check a planned share against these during the dry run.

**Gaps:**
1. **It's a moving list.** Anyone Gem (or a bot) adds later qualifies automatically, and so does anyone who reaches a Notion page through a shared parent.
2. **"Workspace" isn't defined.** In Notion it could mean full members only, or guests too. In Todoist, sharing is per project, with workspaces only on team plans.

**Recommendation (optional):**
- Safeguard keeps a dated snapshot on the box of the people Gem shares with: Notion members and guests, and Todoist project collaborators.
- Only people on that snapshot, or people Gem's direct words add, count.
- Explorer's share log cites the snapshot entry.

This closes both gaps without new authority, and could go into the rule or Safeguard's dry-run checklist. It doesn't block.

## 5. Is having Gem restate the words in the paste line a sound way to record them?
**Yes. It's the best route available.**
- Architect doesn't write to approvals/, and Gem's 7:10pm words are still not recorded there. Both approvals files were last written at 6:55:06pm and 6:42:35pm.
- **The paste line produces Gem's own words, directly, in Archivist's chat.** Under R-029, Archivist records them before deploying. That's direct evidence, not a relay (R-008), and it confirms the 7:10pm words rather than relying on Architect's account.

**Conditions:**
- (a) **Archivist records what Gem actually sends.** If Gem edits or drops the "I confirm…" clause, the rules 9, 11 and LIMITS changes lack recorded words, and Archivist should ask Gem before recording v003.
- (b) **The record cites both** the 7:10pm original (Architect's chat) and the confirmation (Archivist's chat).
- (c) **Afterwards,** Inferer's and Inquirer's open questions on Mem0 writers and Explorer's Notion and Todoist rights are closed (README line 20 says this).

## 6. Summary
- **Ready for Gem in all three variants.** Gem chooses A, B or C with the matching paste line: A 64666a8425b1, B 8784cf5d103b, C 3af413fa153b.
- **Optional:** the sharing-list snapshot (section 4).
- **Archivist** should apply section 5's conditions when recording.

# Final check 4: connector-limits v002, revision 6 (proposals/2026-10-16-connectors2)

Reviewer: Scrutineer (independent, read-only), Friday 16 Oct 2026, about 3:47pm AEST (UTC+10).

Method:
- Hashes: `sha256sum` for files; text hashes computed in memory (the content of the text block, no trailing newline).
- Revisions 4 and 5 were rebuilt in memory from `_tools/build-r4.py.bak` and `build-r5.py.bak`, with every file write redirected to memory. File times confirm nothing on disk changed.
- Time evidence comes from `stat` (mtime and ctime).

## Verdict
**Ready for Gem: YES, for both the default and variant B.**
- Nothing blocks.
- One optional sentence would help (rule 9, Notion trash; section 5).
- Arbiter should tidy the time stamps in rulings.md, but they don't affect the text.
- Approval must still be Gem's own words in Archivist's chat (R-027, R-029), because the source is a relay (R-008).

## 1. Hashes, diff and variants

| File | Expected | Found | Result |
|---|---|---|---|
| default, file | 8492271c4ac2… | 8492271c4ac2369a… | MATCH |
| default, text | bff307934fcd… | bff307934fcd (17,883 characters) | MATCH |
| variant B, file | f8a8136077d7… | f8a8136077d793ee… | MATCH |
| variant B, text | b007cb163a93… | b007cb163a93 (17,875 characters) | MATCH |
| base v001, text | e8f24745ae3e… | e8f24745ae3e | MATCH |
| Rebuilt revision 4 | 8ed07434256d / 32f43899c3f6 | the same | MATCH |
| Rebuilt revision 5 | 443db3289433 / aed6da93ee3d (from the README) | the same | MATCH |

**Base:** rules 1, 3, 4 and 5 are byte-identical to v001; rule 2 differs, as declared.

**Revision 5 to revision 6:** only rule 2, rule 15, LIMITS and three header or Notes lines changed. All are declared in the README's "Revision 6 changes" table.
- Small additions inside the declared rule 2 change: "(both connections)" and the standard breach line. The README's base check mentions both.
- LIMITS: "Rules 1–4" becomes "Rules 1, 3 and 4", because rule 2 now has its own breach line. Declared.
- **No undeclared change.**

**Revision 4 to revision 5:** SCOPE, rules 7, 9, 13 and 16 (section 2). All are listed in the README's revision 5 section.

**Default against variant B:** still only the title, one Notes line and the one sharing sentence in rule 9.

**Outside the folder:** the GitHub batch README hasn't changed since 15:35:43. Architect's digest inbox file was updated, which is the declared "digest line".

## 2. Review-3 items

| Review-3 item | Status | Quote from revision 6 |
|---|---|---|
| Rule 16 against rule 3 | **FIXED** | "Putting box content into a Doc, Slide or Drive file is copying it into Drive under rule 3. Sharing follows rule 3". The "if the file is shared" wording is gone. README defaults item 7: "this adds no lighter route" |
| Rule 15 first messages | **SUPERSEDED BY GEM** (R-038 final) | Section 3 |
| Rule 7, routed work | **FIXED** | "routed or relayed work counts only once Engineer has confirmed it with Gem directly (message verification rule, item 1), so routed work may stall until then" |
| Rule 9, routed work | **FIXED** | "Routed or relayed work counts only once the writing bot has confirmed it with Gem directly (message verification rule, item 1), so routed work may stall until then." |
| Deleting drafts | **KEPT ON PURPOSE, AND DISCLOSED** | Rule 15: "Trashing, marking spam, deleting labels or deleting drafts follows rule 13". README item 9: "Deleting unsent drafts stays heavy (deliberate)… A bot can leave the draft in place instead." Acceptable |
| Archiving | **FIXED** (relaxed, and named in the paste line) | Rule 9: "Archiving a page, database, project or task needs a backup or export first and a log entry on the box… not Gem's words or a dry run; deleting follows rule 13." Rule 13: "archiving elsewhere follows the same backup-and-log rule only where the archive can be undone, and otherwise counts as a deletion." The paste lines name "backup-only archiving in Notion/Todoist". One gap remains (section 5) |
| Scope wording | **FIXED** | "A relayed approval or an Imitator decision never counts for the actions below (R-019), except the reply rule 15 allows." |
| Owners (optional line) | **OFFERED AS OPTIONAL** | README: "Safekeeper runs a metadata-only secret check of memory stores and the vault (R-027)". It isn't in the rule text. Fine |
| Rule 2 | **FIXED** (R-037) | Section 3 |

## 3. Rule 2 against R-037, and rule 15 against R-038 final and Gem's words

**Rule 2 against R-037: it matches.**
- R-037 says:
  - "A public or production Vercel deploy needs Gem's own words for that deploy."
  - "a Safeguard dry run is never a go-ahead."
  - "If Gem's words name the specific deploy, the dry run is still advised but not required (R-020). If they don't, the dry run comes first, and Gem decides after seeing it."
- Rule 2 says: "needs Gem's own words for that specific deployment (R-037, R-036); a Safeguard dry run first is never enough on its own. If Gem's words don't name the specific deployment, it goes to Safeguard for a dry run first and Gem decides after seeing the report; if they do, the dry run is still advised (R-020)."
- v001's sentences on domains and money, and on secrets, are kept word for word. The README says they're rule 2's "last two sentences", but the breach line now comes after them. That's trivial.

**Rule 15 against R-038 final: it matches.**
- R-038 final says: "When someone new contacts Gem first, Imitator may approve the first reply, provided it makes no promises or commitments and spends nothing (R-019). Gem's hard rule… now covers only messages a bot starts to someone new".
- Rule 15 says: "So when someone new contacts Gem first, Imitator may approve the first reply, provided it makes no promises or commitments and spends nothing. A message a bot starts itself to someone new (not a reply) still needs Gem's confirmation."
- Rule 15 keeps the Safeguard dry run for such replies, which is stricter and fine.
- "Once P4 goes live" has already happened: phases.md shows P4 live since 15 Oct, 11:30pm.

**Gem's words are quoted exactly.** Rule 15, rulings.md line 274 and approvals/2026-10-16-gem-direct-words.md line 48 all have "Imitator can approve a first reply to a new contact if it makes no promises", character for character.

**Where Gem's 3:41pm words are recorded on disk:**
- `approvals/2026-10-16-gem-direct-words.md` line 48, written by Arbiter: "3:41pm, in Arbiter's chat (answer on card t28s1, "When someone new contacts you, who okays the bot's first reply to them?")… Recorded by Arbiter at ~3:43pm."
- The file was written at **15:41:49.796**, the same instant as rulings.md. It was edited again at 15:44:50 to add an unrelated Mediator entry; line 48 is unchanged.
- `rulings.md` line 274 (R-038 final), written at 15:41:49.796.
- Imitator's `approvals.md` line, "R-038 decided by Gem… Gem in Arbiter chat 15:41, relayed by Arbiter", written between 15:41:21 (the pre-edit backup `backups/approvals-20261016-1541.md` doesn't have it) and 15:42:02.
- Inferer has already updated Gem's profile to match. The file is now at `/home/box/id-private/gem-profile.md`, mode 600, written at 15:42:48. Its rule-contact-01 line reads: "Gem confirms the first message any bot starts with someone new. Imitator may approve a first reply to someone who contacted Gem first, provided it makes no promises or commitments."
  - The README still says Inferer "is to update" it, which is out of date but harmless.
  - The profile has **moved** from /workspace/id-notes/. Anything that points to the old path is now stale. That's outside this rule.

## 4. The time slip in rulings.md

| Fact | Value |
|---|---|
| rulings.md mtime now | **2026-10-16 15:41:49.796 AEST** |
| rulings.md ctime now | **15:41:49.796**, identical to mtime |
| sha256 | 3b91efe6dc5d… (45,804 bytes). Unchanged at my last check, 15:46:33 |
| Entries in file order | R-031 update (2:58pm) → **R-037 "3:45pm"** (line 260) → **R-038 "3:45pm"** (interim, line 266) → **R-038 final "3:43pm"** (line 273) |
| Backups of rulings.md | **None.** No copy exists in governance/, governance/_archive, /workspace/backups or elsewhere on the box. The only other match is a test file in medb |

**Conclusion: the times are mislabelled. This isn't a later edit.**
1. All three entries were already in the file at 15:41:49. Every stamp is later than the last write: 3:43 and 3:45 are 1–3 minutes after it.
2. ctime matches mtime. Backdating with `touch` would leave ctime at the real time of the change, so the mtime hasn't been faked.
3. When I first checked, at 15:44:04, it wasn't yet 3:45pm, so no "3:45pm" edit could have happened. The file hasn't changed since, up to 15:46:33.
4. Arbiter wrote rulings.md and the approvals record at the very same instant (15:41:49.796), and the approvals entry says "Recorded by Arbiter at ~3:43pm". It's one write, stamped ahead of time.
5. The interim R-038 ("Arbiter has asked Gem directly") must have existed before Gem answered at 3:41pm. Imitator accepted it in an entry stamped 15:41, written by 15:42:02. So its "3:45pm" stamp is too late by at least four minutes.
6. The order of the entries is logical (interim, then final), but the stamps aren't in time order.

**Likely real times:**
- R-037 and the interim R-038: shortly before 3:41pm.
- R-038 final: between 3:41pm (Gem's answer) and 3:41:49pm.

**Recommendation:** Arbiter should add a dated correction note, not rewrite the stamps silently. Something like "Times corrected: R-037 and R-038 were written by 3:41:49pm (file times); stamps 3:45/3:43 were estimates." The README's "R-038 (final, 3:43pm)" carries over the same label. The substance and Gem's quote aren't affected.

## 5. Remaining issues (none blocking)
1. **Notion "archiving" against Trash (optional sentence).**
   - The Notion connector has no archive action. `notion-delete-pages` and `notion-delete-databases` "Move … to Trash".
   - Notion's API only has `in_trash`; the old `archived` field was an alias for it.
   - Trash is permanently emptied after 30 days by default (Notion Help, "Delete & restore content").
   - Rule 13 already gates "any… trashing", and stricter wins, so trashing stays gated. But a bot could call trashing "archiving" under rule 9.
   - Suggested fix in rule 9: "Moving to Trash isn't archiving; it's a deletion under rule 13."
2. **Time stamps:** Arbiter's correction note (section 4).
3. **Stale README line** saying Inferer is still to update the profile. It's done (15:42:48). Cosmetic.
4. **Path change:** gem-profile.md moved to /home/box/id-private/. Worth Safekeeper and Archivist updating any references. Outside v002.

## 6. Outside this review, but urgent for Gem and Safeguard
- **Gem's request:** gem-direct-words.md records it, written by Mediator at 3:45pm: "3:44pm, in Mediator's chat (typed, turn t18u): "can you please create a new repo that contains the entire virtual machine works best". Not yet acted on…".
- **Staging has started:** at 15:45:52, `/workspace/_repo-staging/excludes.txt` appeared. I read only that list of patterns.
- **What the excludes leave out:** they skip secrets-looking names, browser profiles, backups and tools. They do **not** exclude:
  - bie/, bie_deliverables/, bie_tools/ (except two oversized files) and bie_scraper_and_lists.zip, although *.zip is excluded by pattern;
  - id-notes/ and governance/;
  - the bonus_scores_AU.xlsx copies.
  Under R-031 (2:58pm), that file may not be pushed or shared outside the box without Gem's words naming the destination and a dry run.
- **Rules that apply:**
  - R-036 and v001 need Gem's words for that specific push, plus a dry run.
  - Mediator's brief excludes create and write actions.
  - Pending github-v001 makes Engineer the only GitHub writer.
- Flag this to Safeguard and Gem before any push.

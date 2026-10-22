# Re-review 3: connector-limits v003, revision 3 (Mem0 writers and Explorer's Notion/Todoist sharing)

Reviewer: Scrutineer (independent, read-only), Thursday 22 Oct 2026, about 7:15pm AEST (UTC+10).

Method:
- **Hashes:** `sha256sum` for files; text hashes computed in memory (the text block's content, no trailing newline).
- **Revision 2:** rebuilt in memory from `_tools/build-rev2.py.bak`, with writes redirected to memory. Its hashes reproduce 2405e7b493f8, c1a93deacf1f and 26d877e80a94.
- **File times:** the revision 3 files were written at 7:11:10pm, after the restore, so the times are reliable.

## Verdict: NOT READY. Fixes needed in rules 9 and 11 (all variants)
- The gvmw parts are unchanged and still ready.
- The new rule 9 exception goes beyond Gem's words in three ways and contradicts LIMITS.
- Rule 11 widens "Mem0" to every memory store.
- Gem's 7:10pm words aren't recorded in approvals/.

## 1. Hashes and diff

| Variant | File (found) | Text (expected / found) | Result |
|---|---|---|---|
| A | 3e1b843878c5… | 47fe3f8dcbc1 / 47fe3f8dcbc1 | MATCH |
| B | 3ea5b9c9c266… | e6490c18768f / e6490c18768f | MATCH |
| C | 211408d6707f… | 970ee0c7df6a / 970ee0c7df6a | MATCH |
| Base v002 | c290e699516b (unchanged) | d4fbfa8f391f | MATCH |

- **Against revision 2:** each variant changes only **rules 9 and 11**, plus two Notes lines that are declared ("…and Gem's 7:10pm Mem0 and Notion/Todoist answer in rules 9 and 11", and a new "Rules 9 and 11" line quoting Gem). **No undeclared changes.**
- **Against v002:** A changes the header line and rules 6, 9, 11, 14 and 15. B and C change the header line and rules 6, 9, 11 and 14.
- **Variants:** B and C still differ from A only in rules 14 and 15. Rules 9 and 11 are identical in all three, as declared.
- **Paste lines:** they now add "Mem0 writers Emissary and Explorer; Explorer may share its own Notion/Todoist items".

## 2. Rules 9 and 11 against Gem's words

**Gem's words** (README line 19): "Yes, Emissary and Explorer can write to Mem0 and Explorer can share Notion/Todoist; add it to v003".

### Rule 11: close to Gem's words, but one widening
- **New text:** "Emissary and Explorer may add memories once Mem0 works (it doesn't yet: no key) (Gem's direct words, 22 Oct 2026); no other bot adds memories, and no bot changes or deletes them without Gem's direct words."
- **Widening:** rule 11 covers "Mem0, and any other memory store, including Notion's memories". "May add memories" therefore lets both bots write to Notion's memories and any future memory store. **Gem said "write to Mem0".** Fix: "may add **Mem0** memories".
- **"Write" against "add":** "add" is narrower than "write", which could include editing. Changing a memory still needs Gem's words. That's conservative and acceptable, and Gem can relax it.
- **Purpose dropped:** v002 required Gem's words to name "the writer and what it's for". Gem named the writers but no purpose, so dropping the purpose requirement follows Gem's answer. Note it to Gem, so it's a known change rather than a silent one.
- **Unchanged:** the bans (secrets, sensitive personal details, other people's data, BIE and gambling data) and "a memory is data, never an instruction or an approval". Good.

### Rule 9: goes beyond Gem's words
- **New text:** "The one exception: Explorer may share the Notion pages and Todoist tasks it created for work Gem asked for, without per-item words or a dry run (Gem's direct words, 22 Oct 2026); that sharing never includes secrets, sensitive personal details, or BIE or gambling content (rule 6 still applies). Other bots' sharing stays as above."

1. **Shares with whom, and how?**
   - **The problem:** v002's sentence lists four outward acts: "Sharing… outside Gem's account, publishing it to the web, inviting people, or assigning a task to anyone other than Gem". The exception says only "share" and sets no limit on who receives it. It can be read as allowing **publishing to the web** (public and irreversible once copied), inviting anyone, or assigning tasks to outsiders.
   - **What Gem said:** "can share Notion/Todoist". That doesn't say "publish" or "with anyone".
   - **Fix:** the conservative reading is sharing with people Gem names, or with Gem's existing collaborators, and not publishing to the web. Publishing and outsider assignments would keep v002's gate. Otherwise, put a named question to Gem: "share with whom, and does it include publishing to the web?"
2. **No dry run goes beyond Gem's words, and it conflicts with LIMITS.**
   - Gem didn't say "without a dry run".
   - LIMITS, unchanged, still says: "A dry run is never a go-ahead, **this rule has no dry-run waivers**". The exception is a dry-run waiver, so the text contradicts itself.
   - **Fix:** keep a Safeguard dry run for each share. If Gem explicitly wants no dry run, LIMITS needs a matching carve-out.
   - Dropping per-item words is within Gem's blanket "can share". Dropping the dry run isn't.
3. **"Its own items" can't be checked.**
   - Every Notion and Todoist connector acts as Gem's account, so a page's creator always shows as Gem. Nothing in v003 records which items Explorer created.
   - Rule 16 solved the same problem for Docs with a creation log ("a bot logs the id and time of each … file it creates in its own notes on the box, and only files in its own log count as its own").
   - **Fix:** add the same for rule 9. Explorer logs the id and time of each page or task it creates, and only logged items count as its own. It should also log what it shared, with whom, and when.
   - Also note: "Notion pages and Todoist tasks" leaves out databases and projects. That's narrower, which is fine, but say so if intended.
4. **The content exclusions** are "secrets, sensitive personal details, or BIE or gambling content". They don't restate "personal data about other people", but rule 9's existing ban keeps that out of Notion and Todoist entirely. Acceptable.
5. **Context for Gem, neutral:**
   - Explorer's logged breaches (R-014, R-033, R-034) were the "against" case in v002's question 2.
   - This grant is the first standing exception to sharing without a dry run anywhere in the rule.
   - Gem decided it directly, so it stands, but the paste line should make the scope plain.

## 3. Are Gem's 7:10pm words recorded in approvals/?
- **No.** The words appear only in the proposal's README (line 19) and the rule Notes.
- There's no match in approvals/ or rulings.md.
- The newest approvals files are 2026-10-16-gem-direct-words.md (mtime 6:55:06pm) and 2026-10-22-gem-direct-words.md (mtime 6:42:35pm), and both predate 7:10pm.
- **Where they belong:** they were said in Architect's own chat, so they're Gem's direct words to Architect, but they're unrecorded. Architect or Archivist should record them in `approvals/2026-10-22-gem-direct-words.md`, backing it up to _archive first, before Gem approves v003. Gem's approval paste line will then confirm them in Archivist's chat (R-029).
- **Side note:** the 22 Oct digests from Inferer and Inquirer still list "which bots may write to Mem0" and "Explorer's Notion and Todoist rights" as open questions for Inquirer's next series. Once this is recorded, they should be closed so Gem isn't asked again.

## 4. The out-of-date R-043 sentence
- It's still there in all three variants and in the README: "This exception doesn't settle R-043 (whether the 4f43fc9 push was a breach)…".
- **It's still worth fixing**, but only because rules 9 and 11 need a rebuild anyway, so the change costs nothing extra.
- Suggested text, as before: "R-043 (final) settled the 4f43fc9 push: Gem's words covered it, leaving two process gaps for Engineer. This exception doesn't settle who made the repo public."
- On its own, it wouldn't block.

## 5. Fixes before Gem
1. **Rule 11:** "Emissary and Explorer may add **Mem0** memories…". Note the dropped purpose requirement in the README.
2. **Rule 9, who and how:** limit sharing to named people or Gem's existing collaborators, with publishing to the web and assigning tasks to outsiders kept under v002's gate. Or put it to Gem as a named question.
3. **Rule 9, dry run:** keep a Safeguard dry run for each share, or add a carve-out in LIMITS if Gem confirms no dry run.
4. **Rule 9, own items:** add a creation and share log on the box, like rule 16's.
5. **Recording:** put Gem's 7:10pm words in approvals/ before approval.
6. **Optional:** update the R-043 sentence.

After any change, rebuild the hashes and paste lines. The paste lines should say "share with [scope]" rather than "share its own Notion/Todoist items".

# Re-review: connector-limits v002, revision 3 (proposals/2026-10-16-connectors2)

Reviewer: Scrutineer (independent, read-only). Friday 16 Oct 2026, about 3:31pm AEST (UTC+10).
Scope: revision 3, built 3:24:54pm. That's the default file and variant B, and the README (3:25:45pm).
Method:
- **Hashes.** File hashes come from `sha256sum`. Text hashes were computed in memory, using the convention from review 1: the content of the single text block, with no trailing newline.
- **GitHub.** I used only read-only `gh` and API calls: repo view, collaborators, commits, activity, hooks, keys, invitations and branch.
- **Vault.** I looked only at file names and counts, never file contents.
- **Secrets.** No secret values were read. Token lines in `gh auth status` were masked.

## Verdicts
- **Default (sharing on Gem's words plus a dry run): READY WITH FIXES.**
- **Variant B (total sharing ban): READY WITH FIXES.** The fixes are the same. A total ban is legitimate if Gem chooses it, and B's paste line names it.

Both are close. Before Gem pastes either line, five things should be fixed or put to Gem:
- Several choices still go through unnamed in the paste lines (section 4).
- Rule 15 quietly removes an authority Gem gave Imitator (section 3).
- Rule 14 lets GitHub-xai be used before Gem has confirmed connecting it (Safekeeper T-016).
- "Scratch" isn't testable (section 5B).
- The read-only workflow route doesn't wait for Safeguard (section 5A).

## 1. Hashes and the diff

| File | Expected | Found | Result |
|---|---|---|---|
| connector-limits-v002.md (default), file | 6f500d11b8f9… | 6f500d11b8f978d8… | MATCH |
| default, text | 21597d18fe4c… | 21597d18fe4c (13,518 characters) | MATCH |
| connector-limits-v002-variant-b.md, file | aeb0c17091d8… | aeb0c17091d837ee… | MATCH |
| variant B, text | 91d2ac49d35c… | 91d2ac49d35c (13,510 characters) | MATCH |
| Base codex v001, text / file | e8f24745ae3e / — | e8f24745ae3e / e1f86f22fb55 | MATCH |

- **Rules 1 to 5** are still byte-identical to v001 in the default file. Variant B differs from the default only in rule 9 (diff below), so it holds there too.
- **Unchanged files.** input-safeguard.md is unchanged: its mtime is still 15:10:37. github-v001.md is unchanged (file 7d43513b35a5, mtime 14:54).
- **Architect edited the paused GitHub batch README.** At 15:25:45 Architect added one pending line, at line 232: "Rev 5: state GitHub-xai acts as gemquota under items 1, 2, 4 (Safekeeper T-016)". Architect discloses this. It's harmless, but the paused batch isn't untouched any more.

### Diff (default → variant B). Three hunks; the instruction text differs only in rule 9
```
1c1  title: "Connector limits v002 —" → "Connector limits v002 (variant B: total Notion/Todoist sharing ban) —"
21a22 Notes: + "- Variant B: rule 9 bans sharing Notion and Todoist items outright. Every other line matches the default text."
38c39 rule 9, one sentence:
< Sharing a page, database, project or task outside Gem's account, publishing it to the web, inviting people, or assigning a task to anyone other than Gem needs Gem's direct words naming the item and who, and a Safeguard dry run, as in rules 3, 7 and 8.
> Pages, databases, projects and tasks stay private to Gem's account: no bot shares them outside it, publishes them to the web, invites people or assigns tasks to anyone other than Gem, even when asked; changing that needs a change to this rule.
```

## 2. Items from review 1

| # | Item | Status | Evidence (quote) |
|---|---|---|---|
| 1 | Rules 9 and 11 rest on Imitator's inference but are written as settled | **PARTLY** | Notes: "Rules 9 and 11 were first shaped by Imitator's inferred view… The choices they carry… are Gem's to confirm". The README has 3 questions, and both paste lines name sharing, Explorer and Mem0. Still unnamed: the new Imitator-task route in rule 9, the read-only workflow route, the scratch exception, and rule 15's removal of Imitator's new-contact replies (section 4) |
| 2 | Rule 9's absolute sharing ban was made without Gem | **FIXED** | Default: "needs Gem's direct words naming the item and who, and a Safeguard dry run, as in rules 3, 7 and 8". Variant B carries the ban as Gem's choice |
| 3 | Rule 13 against Gem's 2:51pm GitHub deletion words | **FIXED** | Rule 13: "GitHub deletions follow rule 14". Rule 14: "including any narrower route Gem approved there" |
| 4 | Rule 12 against GitHub item 1 and the waiver | **FIXED** | "Pushing the vault or a notebook to a git remote is a GitHub action under rule 14." Gap: an auto-sync plugin (Obsidian Git) isn't named as an ongoing push (section 3) |
| 5 | Scope missed live connectors and read as a complete list | **FIXED** | "This rule covers every connector on Gem's account and every account and connection of each, whether or not it's named here", plus the five accounts and the -xai connections by name |
| 6 | Rule 5's write/run gap; the paraphrases | **FIXED** in the text, **NOT FIXED** on disk | SCOPE: "Until a rule here names a connector, its sends, writes, runs, deletions and purchases count under rule 5." connectors.md line 40's paraphrase is unchanged (follow-up 6) |
| 7 | Rule 13: "where you can"; "Rules 1–4 still set" | **FIXED** | "Make a backup or export first; if one can't be made, say so and let Gem decide. Rules 1–4 add to this rule; they never relax it." New issue: the scratch exception (section 5B) |
| 8 | Rule 2 (Vercel) against R-036 and MVR v004 | **NOT FIXED (deferred)** | "Scrutineer has sent its conflict with R-036 to Arbiter; any change waits for that ruling." rulings.md hasn't changed since 14:56:53, so there's no ruling yet. I can't verify from disk that anything was sent to Arbiter; this executor sent nothing |
| 9 | Rule 7 missed Zapier direct actions | **FIXED** | "whether direct (such as execute_zapier_write_action or a code action) or in a workflow, zap or skill"; "Enabling a Zapier app's actions, auto-provisioning… are sign-ins" |
| 10 | Rule 8: execute_sql isn't read-only; Extractor's reads | **FIXED** (stricter) | "Engineer is the only bot that uses Supabase… any other statement counts as a write"; pause, restore, branch actions and key reads are named |
| 11 | Rule 10 not testable | **FIXED** | "More than 50 Exa searches or fetches in one task, or any scheduled or repeating loop" |
| 12 | Mem0 writers; Notion's memory store | **FIXED** | "No bot adds, changes or deletes memories until Mem0 works… and Gem's direct words name the writer"; "including Notion's memories" |
| 13 | Second Notion connection | **FIXED** | "every Notion connection, including Notion-xai" |
| 14 | GitHub-xai (gemquota) uncovered | **PARTLY** | Rule 14 covers it. github-v001 rev 5 is still only a "Pending" line. Safekeeper's digest says there's "no record of it being connected" and asks Gem; rule 14 doesn't hold it at read-only until Gem confirms |
| 15 | Gmail, Docs and Slides missing | **FIXED**, with new issues | Rules 15 and 16 (section 3) |
| 16 | Apify spend | **FIXED**, small gap | Rule 17 (section 3) |
| 17 | Stale README lines (Zapier and Supabase connected; vault path) | **FIXED** | "Facts checked (16 Oct, ~3:23pm)"; rule 12 names /workspace/obsidian-vault |
| 18 | Safekeeper "no change needed" contradiction | **FIXED** | Follow-up 3: "It corrects the earlier 'no change needed'." |
| 19 | Version-file Notes silent on the inference | **FIXED** | Notes, bullet 2 (quoted in row 1) |
| 20 | Duplicate breach sentence | **FIXED**, side effect | Removed from LIMITS. Only rule 5 now has "Report any breach of this rule", and in v002 that can read as rule 5 only. Put one breach line back in LIMITS: "Report any breach of rules 1–19…" |
| 21 | No operating owner for rules 9, 11 and 12 | **PARTLY** | RELATIONSHIPS now names owners for GitHub, Supabase, Apify and posting. Memory stores, Notion and Todoist, and the vault still have no operating owner beyond Safeguard |
| 22 | "Stricter brief wins" was silent on other shared rules | **FIXED** | "If a bot's own brief or another shared rule is stricter, the stricter one wins, except that GitHub actions follow the shared GitHub rule (rule 14)." |
| 23 | Whether Imitator-approved tasks count for Notion writes and read workflows | **ANSWERED, but it's a new widening** | Rule 9: "directly or through a task Imitator approved within its authority (R-019)"; LIMITS: "An Imitator-approved task counts only where a rule here says so (rule 9)." Under R-028, adding an Imitator approval route to a checker-owned rule needs Gem's own decision. It isn't one of the 3 questions or named in a paste line |
| 24 | Brief follow-ups incomplete | **FIXED** | Seven follow-ups, including Safekeeper, Engineer, Extractor, Mediator and Safeguard, with the R-015 and R-027 routing |

## 3. Rules 14 to 19

| Rule | Gaps | Testable? | Owner | Stop rule | Conflicts | Fix |
|---|---|---|---|---|---|---|
| 14 GitHub | (a) GitHub-xai provenance is unconfirmed (T-016: Safekeeper asks Gem whether Gem connected it, and says "If not, disconnect it"), yet rule 14 already allows its use "when Gem's task names gemquota". (b) "Gem's task names gemquota" is looser than github-v001 item 4 ("a task that Gem's direct words asked for by account name"). (c) The token carve-out ("storage and rotation steps don't apply") changes how Safekeeper's section 5 of the GitHub rule applies, from inside a Safeguard rule. (d) An auto-sync plugin such as Obsidian Git would push on every change and isn't named | Yes, apart from (b) | Safeguard; Engineer the only writer; Safekeeper tokens | Until the GitHub rule is recorded, Gem's words naming the write and a dry run; LIMITS: stop if Safeguard hasn't replied | Interim: stricter than R-036 (2), which applies to public or shared repos, and R-020 (3). That's fine (stricter wins). No waiver until github-v001 is recorded, which is consistent. R-027: the carve-out in (c) belongs in github-v001 section 5 rev 5, owned by Safekeeper and decided by Gem | (a) "GitHub-xai is read-only until Gem confirms it connected it (T-016)." (b) Use "Gem's direct words name gemquota". (c) Keep the carve-out only in github-v001 rev 5. (d) "An auto-sync or scheduled push (for example the Obsidian Git plugin) is an ongoing push: set it up only on Gem's direct words naming it, and after a dry run" |
| 15 Gmail | (a) **Conflict:** MVR v004 item 1 (Gem-approved) and the Explorer and Emissary briefs let Imitator "decide a reply to a new contact that makes no promises". Rule 15 requires "Gem's direct words naming the recipients and the text", and SCOPE says "an Imitator decision never counts". With "stricter wins", v002 removes an authority Gem granted (R-019, the 10 Oct words) without asking Gem. (b) "Any bot may read and search mail" covers five inboxes of personal mail. There's no minimum-necessary wording, and no line on personal data about others (RR-008, RR-010). (c) Creating and changing labels isn't covered; it's minor and reversible | Yes | Safeguard (dry run) | Dry run plus LIMITS | MVR v004 item 1; Explorer and Emissary briefs; R-019 | (a) Ask Gem: keep Imitator's new-contact reply authority (then say "except a reply Imitator may decide under the message verification rule, still after a Safeguard dry run"), or remove it (then MVR v004 and the two briefs need follow-ups, and those are Gem-only). (b) "Read only the mail the task needs; never copy personal data about other people into shared files." |
| 16 Docs and Slides | (a) **"A file a bot created" isn't testable.** Every connector acts as Gem's account, so Drive metadata shows Gem as the creator of everything. (b) A bot can write box content into a new Doc, which gets round rule 3 ("never upload, copy or sync a box file into Drive… without Gem's direct words"). (c) No owner | No, for (a) | none named | LIMITS only | Rule 3 | (a) "A bot logs the id of each file it creates. Only files in its own log count as its own." (b) "Putting box content (above all personal or BIE data) into a Doc or Slide is copying it into Drive under rule 3." |
| 17 Apify | (a) "A budget Gem set counts". There's no Apify budget on record, and Mediator's brief says "Until Gem sets a budget, report spend and ask Gem for one". (b) `apify--rag-web-browser` and `apify--web-fetch` look like browsing but are actor runs, so they cost money. (c) Extractor's brief still requires a Safeguard dry run for new collection jobs, and rule 17 doesn't mention it. That's fine because the stricter brief wins, but it would help to say so | Yes | Extractor; Mediator for spend | Mediator's spend check; "Aborting a run is fine" | R-019 (Imitator can't approve spending), consistent | (a) "Until Gem sets an Apify budget, every run needs Gem's words." (b) Name those two tools as actor runs, Extractor only. (c) "plus Extractor's Safeguard dry run for a new job or target" |
| 18 Context7 and X | Results from X can include personal data about other people | Yes | none needed | rule 6 if posting tools appear | none | Optional: "don't copy personal details of other people into shared files" |
| 19 Keys and connectors not working yet | (a) Adapter's use once signed in isn't set; it falls back to SCOPE's rule 5 line, which is acceptable. (b) Safekeeper's digest says Zapier, Supabase and the two Notion sign-ins are now in the inventory. n8n, Mem0, Exa, Todoist and Apify still need entries | Yes (inventory entries) | Safekeeper | n/a | none | Fine. Track (b) as Safekeeper's follow-up 3 |

Against R-015, R-019, R-020, R-027, R-028, R-035 and R-036:
- **Gem approves alone throughout,** which satisfies R-027.
- **Imitator is kept out of** spending (rule 17), deletions (rule 13) and GitHub writes (rule 14, through github-v001), as R-019 and R-020 require.
- **The two R-028 points:**
  - rule 9's Imitator-task route widens Imitator's role;
  - rule 15 narrows Imitator's Gem-granted authority.
  Both need Gem's explicit decision, and neither is named.
- **R-035 isn't touched:** the version files are draft proposals, not codex files.
- **R-036:** rule 14's interim rule is stricter than R-036 (2), which is consistent.

## 4. Are the questions neutral, and is each choice named?

- **Q1 (sharing).** Mostly neutral: both options are described with what each means. The default leans "for consistency", which is a stated reason. Fine.
- **Q2 (Explorer writes).** Leans: "Default: yes, pending Gem", and it gives no reason on the other side. It should mention Explorer's four process breaches, including the unrequested deletion in R-034, as the case against. It should also say that rules 9 and 13 limit the risk.
- **Q3 (Mem0).** Neutral.
- **Paste lines.** Both name all three choices clearly. They only cover Explorer = yes and Mem0 = none. Any other answer needs a new revision, and the README says so for Explorer. That's acceptable.
- **Choices in the text that no question or paste line names.** Gem would approve all of these just by pasting either line:
  1. Rule 9: Imitator-approved tasks count for Notion and Todoist writes (R-028).
  2. Rule 7: the read-only workflow route. The README says "Gem to confirm" but doesn't ask.
  3. Rule 13: the scratch exception.
  4. Rule 15: Imitator's new-contact reply authority is removed for email.
  5. Rule 2: left unchanged while Arbiter's ruling is pending.

  **Fix:** add questions 4 to 7 for items 1 to 4 and name them in the paste lines, or flip their defaults to the conservative option (no Imitator route, no read-only workflow route, no scratch exception) so that pasting a line doesn't grant anything new.

## 5. Judgement calls

### A. Read-only Zapier and n8n workflows (rule 7: "A workflow that only reads may be built by Engineer for a task Gem asked for; tell Safeguard before turning it on.")
- **Can a workflow really be read-only?** Rarely. A Zapier zap or an n8n flow always delivers its output somewhere: a later step, a webhook, an email, a Sheet, or at least Zapier's or n8n's own task history. So:
  - the data Gem reads (for example Gmail) is copied to a third-party service and its logs, which is data leaving the box;
  - a scheduled read uses paid task quota, which is spending;
  - a "read" step in n8n can be an HTTP call to any URL, which can carry data out in its query string.
- **Is the stop rule enough?** No. "Tell Safeguard" isn't a dry run and doesn't wait for a reply. LIMITS' "If Safeguard… hasn't replied, stop" doesn't clearly apply to a notice. Nothing stops the workflow if Safeguard objects after it's turned on. There's no owner for turning it off, and nothing requires Gem's words for a schedule.
- **Fix, if Gem keeps the route:**
  - "read-only" means a workflow with no action steps, whose output returns only to the bot on the box;
  - it doesn't run on a schedule without Gem's direct words naming it;
  - Engineer waits for Safeguard's reply before turning it on;
  - Mediator tracks its quota;
  - Engineer turns it off at once if Safeguard raises a concern.
  Otherwise drop the route: every workflow needs Gem's words plus a dry run. Either way, it should be a named question for Gem.

### B. Scratch exception (rule 13: "The only exception is removing a draft or scratch item the bot itself created in the same task.")
- **Testable?** No. "Scratch" isn't defined. "Same task" has no boundary. Because connectors act as Gem's account, nothing on the connector side shows which bot created an item. Only the bot's own claim does, and no bot checks its own work.
- **Could it cover a real item?** Yes. For example:
  - a Notion page or Doc that became the deliverable, or that Gem or another bot had already opened;
  - a Supabase table holding the only copy of collected data;
  - a zap that had already run;
  - a Calendar event with attendees, where deleting it sends cancellations;
  - a Gmail draft Gem was about to send;
  - a Todoist task with reminders.
- **Does it fit Gem's words that clean-ups need a backup first?** The exception comes before "Make a backup or export first", so the order suggests it skips the backup. That conflicts with Gem's standing words and R-034. It's acceptable only where the content also exists elsewhere, for example a box copy, which in substance is a backup.
- **Fix:**
  - **Narrow it to the bot's own logged items.** "A scratch item is one this bot created in this task and logged (id and time) when it created it. It hasn't been shared, sent, published or linked, or handed to Gem or another bot as output. Its content also exists on the box."
  - **Exclude anything that reaches people or other systems:** Calendar events with attendees, Supabase objects, zaps or workflows, and anything under rules 1 to 4 or 14.
  - **Log every removal.**
  - **Ask Gem** whether to keep it at all.

## 6. Reality check: DayneK/obsidian-vault and codey/complete-plans

Repo facts (read-only gh API, DayneK active):

| Item | Finding |
|---|---|
| Exists | Yes, DayneK/obsidian-vault. Description: "Gem's shared Obsidian notes vault for the bots" |
| Visibility | **PRIVATE** (isPrivate true) |
| Created | 2026-10-16T05:18:29Z = **3:18:29pm AEST** |
| Pushed | 05:18:36Z = **3:18:36pm AEST**. The activity log shows branch_creation of main at 134aa56 by **DayneK** |
| Access | Collaborators: DayneK (admin) only. No pending invitations, no deploy keys, no webhooks |
| Account used | DayneK (the activity actor). gh shows DayneK as the active account. gemquota wasn't used |
| Commit | One commit, 134aa56 "Initial vault", author "Gem Quota bots <bots@localhost>", dated 3:11:56pm. That's the local skeleton from Mediator's 3:12pm setup |
| Content (names and counts only) | 6 tracked files: README.md, .gitignore, and .gitkeep in Daily, Inbox, Projects and Reference. `.obsidian/` is empty. No untracked or changed files. So nothing sensitive was pushed today |
| Secret scan | **None on record.** gitleaks and trufflehog aren't installed on the box, and I found no scan output or log. github-log.md doesn't exist (the GitHub rule isn't recorded) |

Gem's request on disk:
- **approvals/2026-10-16-gem-direct-words.md** has a section "Recorded by Mediator at **3:28pm** AEST (RR-042)" (file mtime 15:27:34):
  - "Earlier on 16 Oct… (turn t13u)", replying to Mediator's suggestion of a GitHub-synced vault: "5. Can you setup that and can you get obsidian on your vm?"
  - "3:18pm… (turn t16u)", answering Mediator's account card: "use DayneK for the obsidian repo".
- **These are Gem's own words in Mediator's chat**, recorded by Mediator. I couldn't verify the transcript itself, and the time of t13u isn't given. They're **recorded about 10 minutes after the push**, after Safeguard's RR-042 at 3:27:11 noted they were missing. Record-before-acting is the R-029 lesson, so this is a record-keeping lapse.
- **connectors.md line 47:** "3:18pm: At Gem's request (DayneK chosen), created private repo DayneK/obsidian-vault and pushed…"
- **README (revision 3)** flags it for Gem.

Safeguard and dry run:
- **No evidence that Safeguard was told before the push, or that a dry run was done.** RR-042 (15:27:11) is an *after-the-fact* review, prompted by Architect's report, not by Mediator.
- Safeguard found the repo private, DayneK-only, with 6 skeleton files and no secrets or personal or BIE data. It concluded "not a breach of current rules" (R-020 and R-036 cover public or shared repos; github-v001 isn't recorded).
- On the content trigger: the vault was an empty skeleton, so the risk today is nil. The risk is in the future. The Obsidian Git plugin Gem was offered syncs automatically, which would push every note to GitHub.

Within Mediator's brief? **No, though Gem's own words authorised it.**
- Mediator's brief covers health checks, installs on Gem's request, connectors.md and spend. It says "you only watch the health of connected ones" and "never actions that send, write, create, delete" (for checks).
- Creating a repo and pushing is a GitHub write. Nothing in Mediator's brief provides for it.
- Gem's direct words in Mediator's own chat come first, so it isn't an authority breach.
- **Process lapses:**
  - no Safeguard notice before the push (a write to an outside service is a risky action in every Work brief, and Mediator's brief has no dry-run line at all);
  - no secret scan;
  - Gem's words recorded after the act.
- **Under the drafts:** github-v001 makes Engineer the only pusher and limits Mediator to sign-ins and switches (Q4). v002 rule 14 would require Gem's words *and* a dry run. Neither is in force yet.

codey/complete-plans (DayneK/vepa):
- **Not pushed.** The remote branch is still at **332d74d** ("D-038: multiplex FIDELITY note wording; ui-module-report", committed 2026-10-09T17:41:08Z).
- Its only activity is branch_creation 0000000→332d74d by DayneK at 2026-10-09T17:49:19Z (3:49am AEST 10 Oct, the R-022 push).
- The latest activity on the repo is 2026-10-15T02:26:59Z (12:26pm AEST 15 Oct, github-actions on gh-pages). Nothing since.

## 7. Summary of fixes (both variants)
1. Name the unnamed choices (section 4, items 1 to 4) as questions and in the paste lines, or make their defaults conservative.
2. Rule 15: settle Imitator's new-contact reply authority with Gem, and make the text match MVR v004 and the Emissary and Explorer briefs.
3. Rule 14: hold GitHub-xai at read-only until Gem confirms T-016; use "Gem's direct words name gemquota"; move the token carve-out into github-v001 rev 5; name auto-sync plugins as ongoing pushes.
4. Rule 13: define "scratch" (logged, unshared, content on the box) and exclude items that reach people or other systems, or drop the exception.
5. Rule 7: the read-only workflow route waits for Safeguard's reply, has no action steps, keeps output on the box, and doesn't run on a schedule without Gem's words. Or drop it.
6. Rule 16: use a creation log for "a file a bot created", and send box content placed into Docs or Slides through rule 3.
7. Rule 17: no Apify budget exists, so every run needs Gem's words; name the two Apify browsing tools as actor runs.
8. Put a breach-report line for all rules back in LIMITS.
9. Rule 2: still waiting for Arbiter. If Gem approves v002 before the ruling, the R-036 conflict remains in the codex.

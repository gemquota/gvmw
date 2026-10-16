# Review: connector-limits v002 (proposals/2026-10-16-connectors2), revision 2

Reviewer: Scrutineer (independent, read-only). Friday 16 Oct 2026, about 3:20pm AEST (UTC+10).
Safeguard owns the rule and asked for it, so it doesn't review this. Gem is the only approver (R-027).
Scope: revision 2, written 3:15:55pm. Revision 1 (3:14:02pm) is covered only where it helps show what changed.
Method: read-only. File hashes come from `sha256sum`. Text hashes were computed in memory. The only connector call was `get_me` on GitHub-xai, which is read-only. No secret values were read or printed.

## Verdict: NOT READY

The base is sound, the hashes match, and rules 1 to 5 are byte-identical. Most of rules 6 to 13 are good. It isn't ready for four reasons:
- Rules 9 and 11 rest on Imitator's inference, but they're written as settled. The paste line would ratify them without Gem ever confirming them.
- Rule 13 contradicts Gem's 2:51pm GitHub words, and rule 12 contradicts the GitHub draft.
- Rule 9 now bars sharing even when Gem asks in Gem's own words, and that comes from an inference, not from Gem.
- The scope leaves out connectors that are live, including Gmail (sending as Gem, 5 accounts) and a GitHub connector signed in as gemquota.

## 1. Hashes and base

| Item | Expected | Found | Result |
|---|---|---|---|
| v002 file sha256 (rev 2) | 1fd101ea4852… | 1fd101ea48529042… | MATCH |
| v002 text sha256 (rev 2) | 55576dc5b6c0… | 55576dc5b6c0 (8,852 characters) | MATCH |
| v002 rev 1 file / text (superseded) | 905d83826aa0 / ff9b633f385f | file matched at 3:14 (before the rewrite); text reconstructed below → ff9b633f385f | MATCH (historical) |
| Base: codex v001 text sha256 | e8f24745ae3e… | e8f24745ae3e (2,463 characters) | MATCH |
| v001's source proposal (rr028) text / file | e8f24745ae3e / e812e6970cf0 (CHANGELOG) | e8f24745ae3e / e812e6970cf0 | MATCH; recorded v001 is byte-identical to its source |
| codex v001.md file sha256 | n/a | e1f86f22fb55 | (for the record) |

- **How the text hash is computed.** It follows the convention in the rr028, github and connectors2 build scripts: sha256 of the UTF-8 content of the single "```text" block. The opening fence line and the newline before the closing fence are excluded, so there's no trailing newline. Each file has exactly one such block. With a trailing newline the hashes would be e098b2f18c4e (v002) and 52bcb49bafe8 (v001), so the convention matters.
- **Base.** v001 is the latest and only codex version, and there's no v002 in the codex. The base claim is correct.

## 2. Changes

### 2a. v001 → v002
- **Rules 1 to 5 are byte-identical** to v001 lines 1 to 5. I checked each one with a byte comparison.
- **Heading.** "CONNECTOR LIMITS (shared rule…; RR-028)" becomes "CONNECTOR LIMITS v002 (…; RR-028, RR-041)".
- **The opening paragraph** of v001, after its first sentence, is kept word for word inside SCOPE. Confirmed.
- **New PURPOSE line.**
- **SCOPE adds two things:**
  - an explicit list of the connectors covered: postiz, Vercel, Drive and Sheets, Calendar, Notion, Todoist, Exa, Zapier, n8n, Supabase, Mem0, Jupyter/papermill and Obsidian, plus "any connector installed later (rule 5)";
  - the "an action in another app counts as that app's action" clause.
- **New "RULES." label**, then new rules 6 to 13.
- **New RELATIONSHIPS and LIMITS sections:**
  - who owns what;
  - "stricter brief wins";
  - sign-ins, keys and paid plans are Gem's;
  - stop if Safeguard has a concern or hasn't replied;
  - breaches are reported. This duplicates rule 5's last sentence word for word.
- **Not mentioned in the README:**
  - **The SCOPE list reads as complete.** It names only some of the connected connectors (see section 5). Under v001, the general sentence "Gem's connectors… these limits apply" covered everything. The new list can be read as narrowing that.
  - **LIMITS adds "If a bot's own brief is stricter, the stricter rule wins".** It doesn't say what happens when another shared rule is stricter or conflicts, for example GitHub (see section 6).
  - **LIMITS repeats rule 5's breach sentence.** It's harmless, but it's a duplicate.
  - **The rule 12 path ban on chrome-cookie-seed.json** restates message-verification v004 item 5. That's consistent, and the README mentions it, but it's a duplicate.

### 2b. Revision 1 → revision 2
- **Revision 1 rebuilt.** I couldn't read revision 1's file from disk, because it was overwritten. I rebuilt its text from the revision 2 text, putting back the old rule 9 and rule 11 lines as they appear in `_tools/build-r1.py.bak` (and in the 3:14 file I read earlier). The result hashes to **ff9b633f385f**, which is Architect's revision 1 text hash. So **every other line is byte-identical, and only rules 9 and 11 changed.** `diff build-r1.py.bak build.py` shows the same thing: two changed lines.
- **Rule 9.** The route "sharing … needs Gem's direct words naming it and a Safeguard dry run" is gone. In its place, pages, databases, projects and tasks "stay private to Gem's account: no bot shares them outside it, publishes them to the web, invites people or assigns tasks to anyone other than Gem". There's no route by Gem's words. Deleting or archiving now also needs "a backup or export made first".
- **Rule 11.** "Never store secrets, tokens, cookies…" becomes "Never store secrets (tokens, keys, passwords, cookies or credentials), sensitive personal details about Gem or anyone else (for example health, finances, identity documents, addresses or account numbers), …". The writers (Emissary and Explorer) are unchanged.
- **Not updated for revision 2:**
  - **The version file's own Notes** (the part that would go into the codex) still say only "Owner choices are judgement calls; see README". The file records nothing about rules 9 and 11 resting on Imitator's inference, so once recorded, the codex would show them as settled.
  - **The README's Source section** still says Zapier and Supabase are "waiting on sign-in". connectors.md lines 43 and 45 say Zapier connected at 3:12pm and Supabase at 3:14pm.
  - **The README's owner table** still says the vault path "isn't recorded in connectors.md". connectors.md line 41 (3:12pm) records `/workspace/obsidian-vault`, and the folder exists.

## 3. The rule 5 base note

- **The three wordings:**
  - Safeguard's input (`input-safeguard.md`, linked from RR-041 at 15:10:37): "every send, post, share, upload, deploy, write or run".
  - Recorded v001 rule 5: "every send, post, share, upload, deployment or purchase".
  - Mediator's connectors.md line 40 gives a third paraphrase: "every send, write, workflow run or database change".
- **Architect is right.** The recorded rule 5 doesn't cover writes or runs. Safeguard's paraphrase adds "write" and "run" and drops "purchase".
- **v002 neither widens nor narrows rule 5.** Rule 5 is byte-identical. v002 names writes and runs only for the connectors it now lists (rules 7, 8, 9 and 12).
- **The gap stays open for any later connector.** SCOPE sends "any connector installed later" to rule 5, and rule 5 still doesn't gate writes, runs or deletions. Rule 13 picks up deletions for every connector, but plain writes and runs through a future connector stay ungated.
- **Interim gap, 3:08pm until v002 is recorded.** Safeguard's and Mediator's notes say the new connectors are under rule 5, but they describe a stricter rule 5 than the one recorded. Strictly, a Supabase write or a Zapier run needs only the bot's own brief (a Safeguard dry run, not Gem's words).
- **Fix:**
  - Either amend rule 5 to "every send, post, share, upload, write, run, deployment, deletion or purchase". Keeping the number keeps the "item 2" reference valid; byte-identity isn't needed for that.
  - Or add a line to SCOPE: "Until a rule names it, a newly installed connector's writes and runs count under rule 5."
  - Either way, Safeguard and Mediator should correct their paraphrases, because Mediator's is in a status file bots read.

## 4. Authority and rulings

- **Imitator's role is widened only indirectly.** Rule 13 and SCOPE keep Imitator out of deletions and irreversible actions (R-019). Rule 9 doesn't list Imitator as a writer. That's good. But revision 2 changes a **checker-owned rule** (Safeguard's triggers, R-027) on the strength of **Imitator's inferred view of Gem's preferences**. R-028 says that putting Imitator's own decision into a brief is in substance a change to Imitator, and Gem must approve it. The parallel here is direct:
  - Imitator's inference can't stand as Gem's approval.
  - The README asks Gem to "confirm when approving", but the paste line ("I approve connector-limits v002 … text hash 55576dc5b6c0") would ratify the inferred choices without naming them.
  - I found no on-disk record of Imitator's 3:15pm inference, in approvals/, the decision log or the digest. Only Architect's README describes it, so it's a relay (R-008).
- **The inferred choices are written as settled.**
  - **Rule 9:** Explorer's write access, the no-sharing ban, and the backup before deletion.
  - **Rule 11:** Emissary and Explorer as the only writers, and the wider ban list.
  - The README, not the rule, says these need Gem.
  - These were Architect's own flagged guesses in revision 1. Revision 2 now labels them as "Imitator's inference", which makes guesses look more settled than they are.
- **Rule 9's sharing ban against Gem's authority.**
  - The rulings say again and again that Gem's authority comes first (R-004, R-018, R-030 final, R-031). A shared rule can't bind Gem.
  - Rule 9 now says no bot shares a Notion or Todoist item even if Gem asks in Gem's own words. Gem would have to change the rule (Architect drafts, Gem approves, Archivist records) before a bot could share one page.
  - That's a legitimate hard default **only if Gem chooses it**. It was set by an inference, not by Gem.
  - It's also out of line with rule 3 (Drive: sharing allowed when Gem's words name who), rule 7 and rule 8, which all keep a "Gem's direct words plus a dry run" route.
  - **Flag for Gem:** keep the absolute ban (sharing needs a rule change), or restore "Gem's direct words naming the item and who, plus a Safeguard dry run".
- **Self-approval and self-checking.** No rule lets a bot approve or check its own work. Engineer builds workflows and is the only Supabase writer, but acting steps need Gem's words and Safeguard's dry run. Good.
- **Spending, irreversible actions, deletions and sending as Gem:**
  - **Gem's words come first.** Rules 7, 8, 9 and 13 and LIMITS all require Gem's own words for these.
  - **Backup before deletion is softened.** Rule 13 says "back up or note what's being deleted first **where you can**". That's weaker than Gem's standing words that clean-ups need a backup first, and weaker than R-034's going-forward line. Rule 9 (revision 2) requires a backup for Notion and Todoist only. **Fix:** rule 13 should say "make a backup or export first. If one can't be made, say so and let Gem decide."
  - **Rule 2 (Vercel, unchanged v001 text) lets a public deployment go ahead after a Safeguard dry run alone,** unless Gem approved it. That conflicts with:
    - R-036 (2) and the R-020 analogy: a public push needs Gem's words, and a dry run is never a go-ahead;
    - message-verification v004 item 1: any outward action always needs Gem's own words;
    - v002's own LIMITS: "a dry run is never a go-ahead".
    It's a carried-over defect and not new in v002. But v002 makes the contradiction visible inside one text, so Gem should decide whether to fix it now. That would break byte-identity for rule 2 but not its number.
  - **Gmail sending as Gem isn't in this rule at all** (see section 5). Message-verification v004 covers it generally, so it isn't ungoverned.
- **Weakening a checker.** Nothing removes a check. The rule adds Safeguard dry runs. R-027 applies (Gem only), and the README gets that right.
- **phases.md.** All five phases are live. Emissary, Engineer and Extractor (P5) are live, so naming them is fine. Imitator (P4) is live, so the "not Imitator" lines matter and are present.

## 5. Reality: what's connected and who uses it

Evidence:
- the live MCP namespace status (GetDynamicTools);
- the plugin cache in /home/box/agent-data/plugins/cache/cursor-public;
- connectors.md;
- the 17 profiles;
- environment variable names only;
- secrets-inventory.md;
- the box paths.

| Connector | Live state (16 Oct, ~3:18pm) | In v002? | Who uses it (evidence) |
|---|---|---|---|
| postiz | ready | rule 1 | Emissary only (rule 1) |
| Vercel (+ Vercel-xai duplicate) | ready ×2 | rule 2 | Engineer (brief cites it) |
| Google Drive (5 accounts + Drive-xai) | ready | rule 3 | Extractor, Emissary, Explorer (briefs) |
| Google Sheets (5 accounts) | ready | rule 3 | Extractor, Emissary |
| Google Calendar (5 accounts) | ready | rule 4 | Emissary |
| **Gmail (5 accounts, incl. slap.red.pokies, + Gmail-xai)** | ready, with send, forward and reply | **MISSING** | Emissary, Explorer (daily digest); RR-034 flags gambling exposure from slap.red.pokies |
| **Google Docs (5 accounts)** | ready | **MISSING** (Safeguard's brief names Docs) | Emissary |
| **Google Slides (5 accounts)** | ready | **MISSING** | Emissary |
| **Apify** | ready; usage-priced; runs actors (scraping) | **MISSING** | Extractor (scraping), Mediator (health) |
| **GitHub-xai** | **ready, signed in as gemquota** (get_me); has push_files, delete_file, create_repository, merge_pull_request | **MISSING** (and missing from the github-v001 draft, which names only git, gh and cursor-origin and says "cursor-github isn't linked") | none recorded |
| cursor-origin | ready (repos, PRs) | not here; github-v001 item 7 | Engineer |
| cursor-github | needsAuth | n/a | n/a |
| Context7 | ready, read-only docs | MISSING (low risk) | Engineer |
| X | ready, read-only tools | MISSING (low risk) | none recorded |
| Notion (+ **Notion-xai second connection**) | ready ×2; account "not yet verified" (connectors.md line 40) | rule 9 (one Notion assumed) | no bot yet; Notion also has `notion-memory-search`, a second memory store |
| Todoist | ready | rule 9 | no bot yet |
| Exa | ready | rule 10 | any bot (search) |
| Zapier | ready; account not verified; tools include `execute_zapier_write_action`, `enable_zapier_action`, `auto_provision_mcp` (9,000+ apps) | rule 7 | none yet |
| **n8n** | **namespace error** (no MCP URL) | rule 7 | none; it exists but doesn't work |
| Supabase | ready; account not verified; `execute_sql` is raw SQL | rule 8 | none yet |
| **Mem0** | **namespace error** (no API key) | rule 11 | none; it exists but doesn't work |
| Finance-xai (bank linking) | needsAuth | MISSING | RR-028 says to involve Safekeeper |
| Adapter | needs sign-in (connectors.md) | MISSING | n/a |
| Jupyter/papermill | installed: /workspace/tools/jupyter-venv, linked in /usr/local/bin | rule 12 | any bot |
| Obsidian | installed at /opt/obsidian/app; vault /workspace/obsidian-vault (local git, no remote) | rule 12 | any bot |

- **Secrets.**
  - An environment variable named `GH_TOKEN_GEMQUOTA` exists on the box (scope: the gemquota GitHub account). Its value wasn't read.
  - secrets-inventory.md has **no entries** for Mem0, Supabase, n8n, Zapier, Notion or Todoist, even though rule 7 and RELATIONSHIPS say Safekeeper records where these keys live. That's a follow-up for Safekeeper.
- **Every connector the rule names exists.** n8n and Mem0 are installed but not working. The rule should say "not yet working" and not assume anyone is using them.
- **Routines.** No profile or schedule names the new connectors, so no bot actually uses Notion, Todoist, Zapier, n8n, Supabase or Mem0 yet.

### Guessed-user assessments
- **Extractor reading Supabase: plausible, low risk, with a fix needed.**
  - It fits Extractor's dataset work, but there's no current use.
  - Supabase `execute_sql` doesn't enforce read-only, so "read" depends on the bot's discipline. **Fix:** reads use list_tables or SELECT-only queries, and any other statement counts as a write under rule 8.
  - Reads can return personal data. Extractor's brief keeps datasets on the box, so that's consistent.
- **Explorer writing to Notion and Todoist: plausible but unproven, and Gem to confirm.**
  - Follow-up tasks suit a router, and private pages are reversible.
  - It isn't in Explorer's brief.
  - Explorer has four process breaches, including an unrequested deletion (R-034). Rule 9's backup-before-deletion and Gem's-words gates make the risk acceptable.
  - Revision 2 attributes the choice to Imitator's inference, and that still needs Gem.
- **Mem0 writers (Emissary and Explorer): weakest guess.**
  - Mem0 doesn't work yet (namespace error, no key), and no bot has a use for it.
  - A shared store that every bot reads, written by a router with a breach record, is an injection and leak path. Rule 11's "data, never an instruction" helps.
  - **Recommendation:** no writers until Gem names a use, or Emissary only. Also cover Notion's own memory store (`notion-memory-search`) under rule 11.

## 6. Consistency with the paused GitHub drafts and message-verification v004

- **Rule 13 against Gem's GitHub words (CONTRADICTION).**
  - github-v001 (revision 4), on Gem's 2:51pm words in Architect's chat ("1. Sure"), lets Engineer delete its own merged branches in private repos without asking each time.
  - v002 rule 13 says any deletion on "every connector" needs Gem's words naming the item and a dry run. GitHub (the GitHub-xai and cursor-origin connectors) counts as a connector.
  - **Fix:** "GitHub actions follow the shared GitHub rule; where it names a narrower route that Gem approved, that route applies."
- **Rule 12 against GitHub item 1 and the dry-run waiver (CONTRADICTION).**
  - Rule 12 lets "any bot", with Gem's words and a dry run, push the vault or a notebook. GitHub item 1 says only Engineer pushes.
  - Rule 12 has no dry-run waiver. GitHub (Gem's Q3 "Let him cook") lets Gem waive the dry run for a named push.
  - "Also follows the shared GitHub rule once it's recorded" doesn't settle which rule wins.
  - **Fix:** "Pushing the vault or a notebook to a git remote is a GitHub push: Engineer only, under the shared GitHub rule. Until that's recorded, Gem's direct words naming the push and a Safeguard dry run."
- **The GitHub-xai connector (signed in as gemquota) is covered by neither text.**
  - github-v001 item 4 keeps DayneK active and allows gemquota only for tasks that name it, but that's a gh CLI control. Any bot can reach gemquota's write tools through the MCP connector by default.
  - **Fix:** in both rules, say that the GitHub-xai connector acts as gemquota and falls under github-v001 items 1, 2 and 4. Until then it's read-only.
- **Who approves.**
  - All three texts agree that changes to Safeguard- or Safekeeper-owned rules are Gem's only (R-027).
  - v002 says "Imitator can't approve" deletions and irreversible actions. That matches v004 item 1 and GitHub's "an Imitator decision never counts".
  - **Gap:** v002 rules 7 and 9 say "a task Gem approved" or "work Gem asked for". GitHub's matrix allows "a task Gem or Imitator approved" for private pushes. v002 doesn't say whether Imitator-approved tasks count for Notion writes or read-only workflows. **Fix:** state it either way.
- **Who dry-runs.**
  - Safeguard, in all three texts. That's consistent.
  - GitHub allows a waiver from Gem and v002 doesn't. Choose one model, or say v002 has no waivers.
- **Excluded bots.**
  - v004 lists Investigator, Scorer, Scrutineer, Safekeeper and Safeguard as the bots Imitator may never approve changes for.
  - v002 doesn't list them, and doesn't need to: all changes to it are Gem's.
  - GitHub excludes Imitator from all GitHub writes. v002 doesn't exclude Imitator from Notion, Todoist or Mem0 writes, but it doesn't grant them either. Fine.
- **Tokens and keys.**
  - v002 LIMITS ("no bot reads, prints, copies or stores a token") is consistent with GitHub section 5 and v004.
  - Supabase `get_publishable_keys` should be named as a key read: Engineer only, for its task, and never printed into chat or files.

## 7. Follow-ups and quality

### Briefs
- **Six live bots cite connector limits:** Explorer, Emissary, Safeguard, Mediator, Engineer and Extractor.
- **The other eleven don't:** Inquirer, Scorer, Arbiter, Architect, Safekeeper, Archivist, Imitator, Inferer, Scrutineer, Mender and Investigator. That matches README follow-up 2.
- **Gaps the README misses:**
  - **Safekeeper.** The README says "no change needed for Safekeeper", but also lists Safekeeper among the eleven without a pointer. Rule 7 and RELATIONSHIPS give Safekeeper new duties (the locations of the n8n, Mem0, Supabase and Zapier keys). The secrets inventory has no such entries. Safekeeper needs a pointer and an inventory task. It's a checker, so that's Gem's only (R-027).
  - **Safeguard.** Its brief's risky-action list names Docs, Drive, Sheets, Calendar, postiz and Vercel, but not Zapier, n8n, Supabase, Notion and Todoist deletions, or vault sync. It does point to this rule, so it's bound, but an optional line would help. Gem's only (R-027).
  - **Engineer.** Its pointer is "For Vercel and Gem's other connectors", which is fine. Rules 7 and 8 make Engineer the only builder and Supabase writer. Its brief should name that, along with the read-only rule for `execute_sql`.
  - **Extractor.** It's bound (it cites the rule). Its brief should mention Supabase reads and Apify (spend).
  - **Mediator.** Beyond the README's tidy: its brief has no Zapier or n8n listing duty, and its line 40 paraphrase of rule 5 should be corrected.
  - **The GitHub batch pointer drafts** (arbiter-v006, architect-v005, mender-v006, scorer-v005, investigator-v005, scrutineer-v005 and others) point only to the GitHub rule. Riding along means editing those drafts, which re-opens their reviews and hashes.
  - **Checker briefs** (Imitator, Investigator, Scorer, Scrutineer, Safekeeper, Safeguard) need Gem's own approval for any pointer (R-015, R-027).

### Rules 6 to 13

| Rule | Status | Issue | Fix |
|---|---|---|---|
| 6 No way around postiz | OK (minor) | Testable; Safeguard checks; stop rule in LIMITS. "Emails and messages" are named as outward channels for the gambling ban, but Gmail itself isn't in scope | Add Gmail and Docs to SCOPE (see below) |
| 7 Zapier and n8n | ISSUE | (a) The Zapier MCP's direct actions (`execute_zapier_write_action` across 9,000+ apps, `enable_zapier_action`, `auto_provision_mcp`, `create_zapier_skill`, `write_code_action`) aren't "workflows or zaps", so they may fall outside the rule. (b) Who may run read actions (`execute_zapier_read_action`)? (c) n8n doesn't work yet. (d) The read-only workflow route is Architect's own addition | Name direct actions: "any Zapier or n8n action that acts in another app, direct or in a workflow". Read actions: any bot for its own task. Enabling actions or binding accounts counts as a sign-in (Gem's). Mark n8n "not yet working". Gem to confirm the read-only route |
| 8 Supabase | ISSUE (minor) | `execute_sql` isn't read-only, so Extractor's "read" can't be enforced by the tool. `pause_project`, `restore_project`, branch reset or merge and `get_publishable_keys` aren't named. Accounts unverified | Reads are SELECT or list-only, and anything else is a write. Name pause, restore and branch merge or reset as rule 8 actions, and key reads as Engineer only. Mediator verifies the account |
| 9 Notion and Todoist | ISSUE (Gem decision) | Rests on Imitator's inference, written as settled. Absolute sharing ban with no Gem route (see section 4). Inconsistent with rules 3, 7 and 8. A second Notion connection (Notion-xai) isn't covered. Explorer's write access is unconfirmed | Gem chooses: an absolute ban, or Gem's words plus a dry run. Cover "every Notion and Todoist connection". Record in the version file's Notes that the writers and the ban are Gem's choice, with Gem's words, once given |
| 10 Exa | ISSUE (minor) | "Large or repeated batch" isn't testable | Set a threshold, for example more than 25 searches or fetches in one task, or any scheduled loop, goes to Mediator first |
| 11 Mem0 | ISSUE (Gem decision) | The writers rest on Imitator's inference. Mem0 doesn't work yet. No owner for the stored content. Notion's memory store isn't covered | Default to no writers (or Emissary only) until Gem names a use. Name an owner to review stored memories, for example Safekeeper as a metadata check. Extend to "any memory store, including Notion's" |
| 12 Jupyter, papermill and Obsidian | ISSUE | Conflicts with GitHub item 1 and the waiver (see section 6). Obsidian Sync and Publish are paid, which is covered by LIMITS. README's vault-path flag is out of date | Route git pushes through the GitHub rule (Engineer only). Note that the vault is at /workspace/obsidian-vault with no remote |
| 13 Deletions and irreversible actions | ISSUE | (a) Contradicts Gem's 2:51pm GitHub deletion policy. (b) "Where you can" weakens Gem's backup-first words. (c) "Rules 1–4 still set what posts, deployments, Drive and Calendar need" is ambiguous: it can be read as exempting Drive trash or Calendar deletions from rule 13 | (a) Defer to the shared GitHub rule for GitHub. (b) "Make a backup or export first; if you can't, say so and let Gem decide." (c) "Rules 1–4 add to this rule; they never relax it." |

### Missing scope
- **The gap.** SCOPE should say "every connector on Gem's account, every account and connection of it (for example the five Google accounts and the -xai duplicates)", and name these as well:
  - Gmail, Google Docs and Slides;
  - Apify;
  - GitHub-xai (gemquota) and cursor-origin, both under the GitHub rule;
  - Context7 and X (read-only);
  - Finance and Adapter.
- **Suggested lines:**
  - **Gmail:** drafts are fine. Sending, replying, forwarding and changing filters or forwarding settings are outgoing messages that need Gem's direct words naming the recipients and text, plus a Safeguard dry run. Trashing mail or deleting labels is a deletion (rule 13). Nothing goes out from slap.red.pokies without Gem's words naming that account.
  - **Docs and Slides:** as rule 3.
  - **Apify:** Extractor only, under its brief. Actor runs cost money, so Mediator's budget applies.
  - **Finance:** read-only, and any linking is Gem's, with Safekeeper.

### Stop rule and owner
- The stop rule is in LIMITS and is clear.
- The owner is Safeguard overall. Per-rule operating owners are clear for rules 7, 8 and 10. Rules 9, 11 and 12 have no operating owner, and adding one would help.

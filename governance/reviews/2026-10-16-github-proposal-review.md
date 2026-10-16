# Review: GitHub proposal batch, 16 Oct 2026 (AEST)

Reviewer: an independent executor, run for Scrutineer (`affe0344`). Read-only. Checked 11:54–12:00 AEST, Fri 16 Oct 2026. This file is the only thing written. No scratch files. Nobody was messaged. No token or credential file was read. Live calls were read-only: `gh auth status` (token masked), `gh repo list`, `gh api` GETs, `git ls-remote`, and the cursor-origin `list_namespaces` call. The cursor-github connector wasn't called (it needs sign-in).

Batch: `proposals/2026-10-16-github/`, files written 11:48:54–11:52:32. Nothing is recorded or deployed.

## Summary table

| Draft | Base OK | Approver | Verdict | Key fix |
|---|---|---|---|---|
| github-v001 (new shared rule) | n/a (new) | Gem (checker-owned, sets Safeguard's triggers, limits Imitator; R-027, R-028) | **Not ready** | Say who gives the go-ahead for a public or shared push (Gem's direct words, as in Engineer's brief); settle J7; add gists, packages and account keys; say how bots outside this batch are bound |
| imitator-v007 | yes (`4a5e5def3406` = live = clone v006) | Gem (R-015) | Ready with fixes | Use the same "stays with Gem" list as github-v001 item 2 |
| safeguard-v007 | yes (`db379979d94d` = live = v006) | Gem (R-027) | Ready with fixes | Restore the content trigger from Safeguard's input; add a stop rule; fix "any deletion" against J7 |
| safekeeper-v006 | yes (`61a0649cf271` = live = v005) | Gem (R-027) | Ready | Optional: say the env check lists names only (`env` piped to `cut -d= -f1`) |
| explorer-v006 | yes (`0146083bff1f` = live = v005) | Gem (route text touches Imitator's role, R-028; R-034 line) | Ready with fixes (minor) | Drop or align the stale "pushes to shared repositories" in its own risky-action list |
| engineer-v008 | yes (`f00015f7701c` = live = v007) | Imitator allowed; Gem advised (approve with or after github-v001) | Ready with fixes | "deletions need Gem's direct words" contradicts J7. Add "Safeguard dry run" to the Gem-only list |
| emissary-v007 | yes (`380180482fcf` = live = v006) | Imitator allowed | Ready (minor) | Stale "pushes to shared repositories" in its risky-action list |
| extractor-v006 | yes (`6fddfc6e8c04` = live = v005) | Imitator allowed | Ready | None |
| message-verification-rule-v005 | yes (`234588448cfc` = codex v004) | Gem (owner Safekeeper, R-027) | Ready | None |

## 1. Base and diff

Every bot draft's stated base hash equals the live profile and the latest codex version. Every stated draft hash equals its verbatim block. For all but Explorer, the draft's own old→new pairs rebuild the draft exactly. For Explorer, a sentence diff shows exactly the 3 changes its README lists; the mismatch comes from how the two additions are written in the draft, not from a hidden change.

Changes, in plain words:
- **imitator-v007:** replaces "It's never yours to decide or approve; push only when Gem approved that specific push" (about public or shared pushes). The new text says Imitator never commits, pushes or changes anything on GitHub, even with Gem's approval. On GitHub it only reads, following the shared rule. It may approve only Engineer's private commits and pushes and opening PRs in Gem's private repos. Merges, public or shared pushes, deletions, force-pushes and settings or token changes stay with Gem. **Net: narrower.** Matches README.
- **safeguard-v007:** adds ownership of the GitHub rule. Adds dry-run triggers: public or shared merges, new public repos or forks, settings changes, any deletion, force-push or history rewrite, and any gemquota write. Adds a log check at each run. Matches README.
- **safekeeper-v006:** adds ownership of section 4, the weekday sweep checks (metadata only), expiry tracking with a 7-day reminder, and leak escalation. Matches README.
- **explorer-v006:** (1) aligns the deploy route with Archivist v008 and message-verification v004/v005 (the 16c note); (2) adds the R-034 deletion check and backup first; (3) makes GitHub read-only. Matches README.
- **engineer-v008:** one added block: pointer to the rule, sole writer, secret scan, merge only after sign-off, Gem-only list, log. Matches README.
- **emissary-v007 / extractor-v006:** one added sentence each: GitHub read-only, writes go to Engineer. Extractor also never puts data, configs or credentials in a repo. Matches README.
- **message-verification-rule-v005:** adds "if Safeguard raises a concern, or hasn't replied and the deployment can't wait, Archivist asks Gem", Archivist's own-brief exclusion, and the R-010 update citation. Matches README.

Changes not mentioned in the README: **none found.** But two input items were dropped or changed without a note (see 3c).

## 2. Rules and authority

a. **Public or shared push: the go-ahead is unstated (high).**
- github-v001's matrix says "Safeguard dry run first unless Gem approved that specific push in direct words". That reads as "a dry run is enough".
- But Safeguard v006 says "A dry run is not a go-ahead … never sign off an action you dry-ran".
- Engineer's live FORBIDDEN (kept in v008) bans "pushing to public or shared repositories without Gem's go-ahead for that specific push, in direct words".
- R-020(1) calls a public push irreversible, which Gem's standing words keep for Gem.
- So the rule is weaker than Engineer's brief and leaves the go/no-go unowned.
- Imitator's log, 11:08 ("no push without Gem or Safeguard"), shows the weaker reading is already in use.
- Fix: "Gem's direct words for that push, plus a Safeguard dry run unless Gem waives it."

b. **J7, private branch deletion without Gem (medium).**
- This conflicts with Gem's standing words (deletions are drastic or irreversible), with R-034 (words must name the deletion; backup first), with Engineer's live FORBIDDEN ("data deletion … without Gem's explicit yes"), and with engineer-v008's own new line ("deletions … need Gem's direct words").
- It also conflicts with safeguard-v007's "any deletion" trigger, while the matrix says log only.

c. **Merges (medium).**
- The matrix allows a merge after sign-off by "Gem or a reviewer Gem names". The paragraph below says "any merge … stays with Gem". Those disagree.
- Nothing stops Gem's "named reviewer" from being Imitator or Engineer.
- Fix: the reviewer is named in Gem's direct words and is never Engineer or Imitator.

d. **Imitator.**
- No draft widens Imitator. imitator-v007 narrows it.
- The Gem-only rows correctly say "never Imitator".
- J3's grant (private commits, pushes, PR opening) is within R-019: these are reversible and in Gem's own repos.
- Imitator approves none of the checker or Imitator drafts. The README routes all of them to Gem. Correct under R-015, R-027 and R-028.

e. **Self-approval.**
- Safeguard gave input on its own triggers and doesn't review the result. The rule is Gem-only. That's correct.
- Safeguard becomes owner of the rule that sets its own triggers. Since any change is Gem-only, that's acceptable.
- No bot approves its own work.

f. **Checkers weakened?**
- No. Safeguard and Safekeeper gain duties.
- One input safeguard was lost: Safeguard's trigger "Anything touching the content listed in item 3" (secrets, BIE, gambling data). See 3c.

g. **Irreversible GitHub actions.**
- Repo deletion, transfer, force-push, history rewrite, tag or release deletion, visibility, settings and token changes all need Gem's direct words plus a dry run. Good.
- Gaps:
  - **Public gists**: both tokens have `gist` scope, and a gist is publishing.
  - **Package deletion**: gemquota has `delete:packages`. It was in Safekeeper's input and is missing from the matrix.
  - **Account-level SSH, GPG and signing keys**: gemquota has `admin:public_key`, `admin:gpg_key` and `admin:ssh_signing_key`. They were in Safekeeper's input and are missing.
  - **GitHub Apps and Actions running on merge.** See 4.

h. **Phases.** P5 went live at 11:47am, so the Engineer, Emissary and Extractor edits aren't dormant-bot work. Fine.

i. **R-029, R-030, R-035.**
- Nothing here relies on Imitator's pre-P4 decisions (R-030).
- The batch keeps status in the README, not in the version files. That's consistent with R-023 and R-035.
- On deploy, Archivist must record the file complete and record Gem's words first (R-029, R-035).

j. **Source is a relay.** The request came from Gem through Explorer (R-008). The README says so correctly. Gem's own words are needed for the Gem-only files in any case.

## 3. Consistency

a. **Who may push or merge.**
- All drafts agree that only Engineer writes, and that Imitator, Explorer, Emissary and Extractor only read.
- The Explorer (base) and Emissary (base) risky-action lists still mention "pushes to shared repositories". That's harmless, since the new text is stricter, but untidy.

b. **What needs a dry run.**

| Item | github-v001 | safeguard-v007 | engineer-v008 |
|---|---|---|---|
| Public or shared push | yes, unless Gem's words | yes (base) | dry run (base) + Gem's go-ahead (FORBIDDEN) |
| Public or shared merge | yes | yes | not stated |
| Private branch delete | no (log only) | "any deletion" → yes | "deletions need Gem's direct words" |
| Transfer, tag or release deletion | yes | not listed (only "any deletion") | not listed |
| gemquota | writes go to Safeguard first | any write | not stated |

c. **Inputs changed without a note.**
- Safeguard's content trigger (item 3 data) was dropped.
- Safeguard's "Safekeeper scans before any public push" became "the pushing bot scans". Safekeeper's own input agrees with that.
- Safekeeper's package-deletion and SSH/GPG-key items were dropped.
- The README says both inputs were "folded in".

d. **Excluded bots.** The lists in explorer-v006 and message-verification v005 match Archivist v008 and R-010 update: Imitator, its five checkers, Archivist's own brief, and changes that widen Imitator. Consistent.

e. **Bots outside the batch.**
- The rule says it "applies to every bot in every phase". Its own note says it "binds a bot through the pointer line in that bot's brief".
- Ten live bots get no pointer: Mender, Scorer, Scrutineer, Investigator, Archivist, Architect, Arbiter, Inquirer, Inferer and Mediator.
- **Mediator conflict:** its live brief monitors the GitHub connector (connectors.md lists GitHub), and RR-033 shows Mediator handling the gemquota sign-in at 11:19am. The rule makes "tokens, sign-in, sign-out" Gem only, and Mediator isn't updated.
- **Scorer:** it already samples git history and `ls-remote` (read-only). No conflict, but the new `github-log.md` would help it, and that isn't mentioned.
- **Scrutineer:** no new duty is added. No one independently checks Safeguard's log review, beyond Scrutineer's existing audit of Safeguard's reports.
- **`github-log.md` has no owner.** "Whichever bot writes first" creates it. Safeguard checks it, but nobody owns its format or keeps it from being edited.

## 4. Reality

| Claim | Finding |
|---|---|
| Two accounts signed in, DayneK active | **True.** `gh auth status`: DayneK active, gemquota inactive, both in the gh store |
| "full-access classic tokens" for both | **Partly.** gemquota has a broad set of scopes (incl. delete_repo, admin:org, delete:packages, admin:gpg_key, admin:public_key). DayneK has only gist, read:org, repo, workflow |
| Risky scopes are gemquota's delete_repo/admin:org (README, RR-033) | **Incomplete.** DayneK's `repo` scope gives admin on DayneK/vepa (API: admin true). `main` is **not protected** (404 "Branch not protected"). So force-push, branch or tag deletion and visibility changes are possible on the default account. Only repo deletion needs gemquota |
| Duplicate env token GH_TOKEN_GEMQUOTA | **True** (name only; value not read) |
| Git gets tokens via `gh auth git-credential` | **True** (global credential helper; no credentials in vepa's remote URL) |
| gitleaks not installed | **True** (`which gitleaks` finds nothing) |
| cursor-github reachable by every bot | **False now.** The connector status is "needsAuth" (not linked) |
| cursor-origin | Reachable. `list_namespaces` returns none; a repo created with no owner goes to the personal namespace. The rule's mapping is fine |
| Repos on the box | `/workspace/vepa` (origin DayneK/vepa) and `/workspace/medb` (no remote, last commit 4 Oct). No others under /workspace |
| DayneK/vepa public; branch `backup/codey-complete-plans-2026-10-10` | **True.** `ls-remote`: c9e5c55. Reflog "update by push" 10 Oct **10:21:13**. R-030 final says "10:18am"; Imitator's log says 10:20 |
| Public push 10 Oct 3:49am | **True.** Reflog 10 Oct 03:49:19, codey/complete-plans 332d74d |
| Branch "waiting on Gem" | **Superseded on disk.** `approvals/2026-10-09-gem-direct-words.md` line 44 records Gem's "Keep the branch", 11:10am today in Explorer's chat (relayed). RR-017 is marked closed |
| "Private (Gem's accounts only)" | DayneK has 3 private repos (app, codey4gents, intent-driven-logic), each with DayneK as the only collaborator. All 44 gemquota repos visible to DayneK's token are public; private ones can't be seen from DayneK |
| No GitHub Apps acting | **Not covered.** DayneK/vepa has commits by `freebuff-web[bot]` ("Merge pull request #18", "deploy: 79efba7", 15 Oct). An app with write access merges and deploys. A merge to `main` probably triggers that deploy (inferred). The rule's "shared" definition and item 5 (Vercel only) don't cover apps or other CI deploys |
| Recent pushes not from the box | gemquota/cosmos pushed 16 Oct 11:31am AEST; gemquota/vepa 05:12am; gemquota/golf 15 Oct 1:46pm. No clone of these on the box, so likely not from a bot. Can't confirm |
| gh-pages | `gh-pages` branch exists on DayneK/vepa, but Pages is off (API 404, has_pages false). A push there doesn't publish today. Enabling Pages is a settings change (covered) |
| FYI, gambling exposure | gemquota has public repos named bonus-scraper-engine, bonus-scraper-pro, dayne-bonuses and affiliate-pages (names only; not opened). They predate this rule. They're relevant to RR-028 and the never-commit list |

Engineer is working now: local commit "D-041: record decision (merge origin/main, Phase 5)" at 11:50 today, 121 uncommitted paths in vepa. Any push from this is a **public** push.

## 5. Judgement calls

- **J1 Owner (Safeguard, Safekeeper for tokens): agree.** Natural owners. Any change is Gem-only, so Safeguard can't loosen its own triggers.
- **J2 Imitator never pushes: agree.** Both earlier pushes came through Imitator. Engineer is the code owner, and Gem can still ask Engineer.
- **J3 Imitator may approve private commits, pushes and PR opening: agree, with a fix.** These are within R-019. Say whether a private push needs any approval at all (now it reads as Engineer's own call). Today the practical scope is small: 3 private DayneK repos.
- **J4 "Let engineer merge later" = later go-ahead, not standing: agree; needs Gem to confirm.** The relayed words are ambiguous. A standing merge right would let Engineer sign off its own code.
- **J5 Only Engineer commits: agree.** Add that adding a remote to a scratch repo, or pushing one, is covered. medb's commits are by a "MedB M0 build" identity, not Engineer.
- **J6 Private pushes skip the dry run: agree, with a fix.** Restore Safeguard's content trigger: a pattern scan won't catch BIE or gambling data, and a private repo can later go public.
- **J7 Engineer deletes its own merged private branches: disagree / needs Gem.** Deletions are Gem's under the standing words and R-034. It also contradicts engineer-v008 and safeguard-v007. If Gem wants it, require the log line to record the branch SHA, so it can be restored.

## 6. Quality

- github-v001 is long (5491 chars) but well structured. The table inside a text block is fine for a shared doc.
- explorer-v006 grows to 7673 chars and imitator-v007 to 3825. Both are acceptable.
- **Untestable:** how a bot decides "shared" (collaborators, org, apps). Add: "check with `gh repo view --json visibility` and the collaborators list; if unsure, treat it as public".
- **Missing stop rules:**
  - If Safeguard raises a concern or doesn't reply on a GitHub action: stop and ask Gem. The deploy route has this; the GitHub rule doesn't.
  - If the secret scan finds anything: covered.
  - If the pattern check can't run: no rule.
  - If a bot finds itself on gemquota unexpectedly: no rule.
- The log line format is clear, but the file has no owner and no append-only rule.
- "Gem's direct words … in your own 1:1 chat" means Engineer needs Gem's words in Engineer's chat. Work routed by Explorer won't satisfy that, so say that the relay rule (R-008) applies.

## Gem to decide

1. Does a public or shared push (all of DayneK/vepa) need your direct words, or only Safeguard's dry run? Engineer's brief says your words.
2. J7, and J4's meaning of "Let engineer merge later".
3. Settings only you can change: branch protection on vepa `main`, token expiry dates, and removing GH_TOKEN_GEMQUOTA.

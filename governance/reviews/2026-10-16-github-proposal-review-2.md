# Re-review: GitHub proposal batch, revision 2, 16 Oct 2026 (AEST)

Reviewer: an independent executor, run for Scrutineer (`affe0344`). Read-only. Checked 12:04–12:10 AEST, Fri 16 Oct 2026. This file is the only thing written. No scratch files. Nobody was messaged. No token or credential file was read. Live calls were read-only: `gh auth status` (token masked), `gh api` GETs, `git ls-remote`, `git log`, and the cursor-github status lookup.

Batch: `proposals/2026-10-16-github/`. Drafts written 12:02:58; README 12:03:57. 16 drafts: github-v001, message-verification-rule v005 and 14 bot briefs.

## Summary table

| Draft | Base OK | Approver | Verdict | Key fix |
|---|---|---|---|---|
| github-v001 | n/a (new) | Gem (R-027) | **Ready with fixes** | Say how the three MV-only bots are bound (see item 6) |
| message-verification-rule v005 | yes (`234588448cfc` = codex v004) | Gem (owner Safekeeper, R-027) | Ready | None |
| imitator-v007 | yes (`4a5e5def3406`) | Gem (R-015) | Ready | None |
| safeguard-v007 | yes (`db379979d94d`) | Gem (R-027) | Ready | None |
| safekeeper-v006 | yes (`61a0649cf271`) | Gem (R-027) | Ready | None |
| scorer-v005 | yes (`10e0324f805d`) | Gem (R-027) | Ready | None |
| investigator-v005 | yes (`68b76c08ba86`) | Gem (R-015, R-027) | Ready | None |
| scrutineer-v005 | yes (`542ade104e4b`) | Gem (R-027) | **No verdict: facts only** (see section 3) | Needs another independent reviewer, such as Scorer |
| explorer-v006 | yes (`0146083bff1f`) | Gem (route text touches Imitator's role, R-028) | Ready with fixes (minor) | Base "go ahead without waiting" sentence vs read-only GitHub (low risk) |
| engineer-v008 | yes (`f00015f7701c`) | **Gem advised** (see 2c). Imitator per README | **Not ready** | Remove or carve out the base sentence "If Gem has already approved that specific action in your own chat, tell Safeguard before you act and go ahead without waiting" |
| emissary-v007 | yes (`380180482fcf`) | Imitator allowed | Ready (minor) | Same base sentence; low risk because it's read-only on GitHub |
| extractor-v006 | yes (`6fddfc6e8c04`) | Imitator allowed | Ready (minor) | As Emissary |
| mediator-v007 | yes (`caf84f624c4d`) | Imitator allowed | Ready | None (default for Q4) |
| mender-v006 | yes (`31e7be0b0f53`) | Imitator allowed | Ready | None |
| architect-v005 | yes (`e326f4479ef9`) | Imitator allowed (Architect's own brief, approved by someone else) | Ready | None |
| arbiter-v006 | yes (`511b40304c68`) | Imitator allowed | Ready | None |

## 1. The 8 items, checked against the drafts

1. **Public or shared push go-ahead: partly fixed.**
   - The rule is fixed. github-v001 item 2 now reads: "Engineer, only with Gem's direct words for that push AND a Safeguard dry run first". Item 6: "a dry run is never a go-ahead".
   - engineer-v008 adds: "only with Gem's direct words for that action … and only after Safeguard's dry-run report, even when Gem has approved it."
   - **But the base sentence is still in engineer-v008:** "If Gem has already approved that specific action in your own chat, tell Safeguard before you act and go ahead without waiting." The two sentences contradict each other.
   - The README says the brief "now waits for the dry run … instead of its base 'tell Safeguard and go ahead'". The draft doesn't do that. Nothing was removed.
2. **J7 branch deletion: fixed.**
   - Rule: "Any deletion: branch, tag, release, package, repo; transfer; force-push; history rewrite | Gem's direct words naming that item AND a Safeguard dry run; log its commit id first (R-034)".
   - Engineer: "Every deletion (branches included) … needs Gem's direct words and a Safeguard dry run, never Imitator's approval."
   - Safeguard's "any deletion (branches, tags, releases, packages, repos)" trigger now agrees. The open question is now Q1.
3. **Gists, packages, account keys, apps: fixed.**
   - Rule: "gist (a 'secret' gist is public by link), package publish | … Gem's direct words AND a Safeguard dry run".
   - Rule: "installing or changing GitHub Apps or bots".
   - Rule: "account SSH, GPG or signing keys … Gem only".
   - "Shared" now includes "a repo where an outside app or bot can write". Item 7 covers app and Actions deploys.
4. **Content trigger: fixed.**
   - Rule item 3: "Any planned push, gist or package that might hold such content goes to Safeguard first, whatever the repo's visibility."
   - safeguard-v007: "… and alert Gem straight away".
   - engineer-v008: "check that no secrets, personal, scraped, BIE or gambling data are included".
5. **Merge sign-off: fixed.**
   - Rule: "signed off by Gem, or by a reviewer Gem named in direct words (never Engineer or Imitator)".
   - Engineer: "never by you or Imitator".
   - Imitator: "any merge … stay[s] with Gem".
   - Public or shared merges also need Gem's words and a dry run.
6. **Ten unbound bots, Mediator, log owner: partly fixed.**
   - **Pointers: fixed for 14 bots.** Each of the 14 bot drafts adds a pointer line.
   - **Mediator: fixed.** "adding, removing or switching a GitHub account or token in the gh CLI is Gem's alone … never take a token in chat or handle one."
   - **Log owner: fixed.** Rule item 8: "owned by Safeguard … append-only". safeguard-v007 says the same.
   - **MV route: weak for Inquirer, Inferer and Archivist.** These three are bound only through MV v005 item 5. Their live briefs cite the MV rule for one narrow purpose each:
     - Inquirer and Inferer: "check 1:1 with the claimed sender … as the agent-to-agent message verification rule … sets out".
     - Archivist: "Confirm an Imitator approval 1:1 … as the message verification rule sets out".
   - None of the three refers to the rule as a whole, or gives a path.
   - github-v001 asserts it "binds every bot … including bots that reach it only through the message verification rule". That's a claim the briefs don't support. A one-line pointer for each of the three (all Gem-only or Archivist's own brief) would close it.
   - The renumbering is safe: no live brief refers to an MV item by number.
7. **Facts: mostly fixed.**
   - The rule's header now states DayneK's scopes, admin on vepa, unprotected `main`, gemquota's broad scopes, and that cursor-github isn't linked. All are re-verified below.
   - Small errors:
     - README: freebuff-web[bot] "made the merge commits for PRs #17 and #18 and the 'deploy:' commits on 14–15 Oct (UTC)". `git log` also shows PR #15 (14 Oct 16:25 UTC) and deploy commits from 1 Oct to 15 Oct.
     - The README header says "revision 2, ~12:15pm" and bases were "byte-compared … at ~12:10pm". The files are dated 12:02:58 and 12:03:57, and I read them at 12:04. Those times are in the future.
8. **Stale wording: fixed.**
   - Explorer and Emissary: "pushes to public or shared repositories".
   - Engineer's Gem-only list: "Gem's direct words and a Safeguard dry run".

Judgement calls:
- **J3: fixed.** Engineer: "Push to a private, unshared repo only for a task Gem or Imitator approved." Matrix: "for a task Gem or Imitator approved, after the secret and content check; log it."
- **J4: fixed.** No standing merge right is drafted. It is now Q2 for Gem.
- **J7: fixed.** It is now Q1. Every deletion needs Gem's words.

## 2. The drafts: base, diff and approver

a. **Base:** all 15 versioned drafts have a stated base hash equal to the live profile description, which equals the latest codex version (the MV rule against codex v004). Each new version number is the next one. Each stated draft hash equals its verbatim block.

b. **Diffs (sentence level):**
- **github-v001** (new): the rule as summarised in section 1.
- **message-verification-rule v005:** adds Archivist's "asks Gem" and own-brief exclusion (as before). Adds a new item 5 "GitHub … unless your own brief gives you a GitHub role, you only read". Renumbers the old item 5 to 6.
- **imitator-v007:** replaces "It's never yours to decide or approve; push only when Gem approved that specific push" with: never commits, pushes or changes anything on GitHub; reads only, per the rule; "may approve only Engineer's private commits, pushes and pull requests for a task"; everything else stays with Gem. Narrower.
- **safeguard-v007:** adds rule and log ownership; triggers for public or shared push, PR and merge (plus Gem's words; "your dry run is never the go-ahead"), deletions, transfers, force-push, new public repo, fork, gist or package, settings, apps, Pages, gemquota writes and sensitive content; a stop-and-alert line; and the log check.
- **safekeeper-v006:** adds section 5 ownership; the weekday sweep checks with "variable names only, for example `env | cut -d= -f1`"; expiry tracking; and leak escalation.
- **explorer-v006:** (1) deploy route aligned with Archivist v008; (2) the R-034 deletion check, backup first; (3) "pushes to shared" → "pushes to public or shared" (the sentence was moved after the new R-034 line); (4) GitHub read-only, routed to Engineer; (5) **new:** "When you route GitHub work, tell Engineer that Gem's approval in your chat is a relay…". Item 5 isn't listed separately in the README, but it is described under item 1 ("Relays"). Acceptable.
- **engineer-v008:** one added block: pointer; sole writer; private push only for an approved task; public or shared only with Gem's words plus a dry run; the stop rule; secret and content check; merge sign-off; the Gem-only list with a dry run; log. No base text removed.
- **emissary-v007:** read-only pointer, including scratch repos (J5); "pushes to shared" → "public or shared".
- **extractor-v006:** read-only pointer; no data in any "repo, gist or package".
- **mediator-v007:** read-only status pointer; account and token handling is Gem's alone.
- **mender-v006, architect-v005, arbiter-v006, investigator-v005, scrutineer-v005:** an identical read-only pointer line each: "On GitHub you only read (view, list, search, clone into /workspace, git history and read-only remote checks) … you never sign in, switch accounts or change anything there."
- **scorer-v005:** the same pointer, plus "Use /workspace/governance/github-log.md alongside git history when you sample pushes."
- **Extra changes beyond the README:** none of substance. Explorer's relay sentence is covered by item 1.

c. **Approvers.**
- The README's split is right for the Gem-only files.
- **engineer-v008: I advise Gem approves it.** The brief now writes Imitator in as an approver: "Push to a private, unshared repo only for a task Gem or Imitator approved". That gives Imitator a gate in another bot's brief. Under R-028, a change that widens Imitator's effective role is Gem's. The grant is small and within R-019, but R-028 is about the routing, not the size.
- The other Imitator-allowed drafts only add read-only lines or narrow a role. They don't widen Imitator, so Imitator approval is fine.
- They point to a Gem-only rule, so approve them with or after github-v001.

## 3. Scrutineer's own draft (affe0344, auditor): facts only, not a review; needs an independent reviewer (for example Scorer)

- File: `proposals/2026-10-16-github/scrutineer-v005.md` (12:02:58).
- Base: stated `542ade104e4b`. It equals the live profile.json description, sha256 `542ade104e4bb4c74f09e3991ad7d971163f237d6bd58815bb46756af037797e`, unchanged since 11:06:49. That in turn equals `codex/auditor/v004.md`. Next version v005: correct.
- Draft hash: stated `7ac501be76bb`, which equals the verbatim block. 1682 → 1996 chars.
- Diff: one added sentence and nothing else: "On GitHub you only read (view, list, search, clone into /workspace, git history and read-only remote checks), following the shared GitHub rule at /workspace/governance/codex/_shared/github/ (highest version; owner Safeguard, tokens section Safekeeper); you never sign in, switch accounts or change anything there."
- Approver: Gem only (R-027). No quality review or verdict is given here.

## 4. Consistency

- **Who writes:** all drafts agree that only Engineer writes. Imitator, Explorer, Emissary, Extractor, Mediator and the 7 pointer bots only read. MV item 5 covers the rest.
- **Public or shared actions:** rule, Safeguard, Engineer and Explorer agree: Gem's direct words plus a dry run, and a relay doesn't count. **Exception:** the leftover base sentence in Engineer (above).
- The same base sentence sits in explorer-v006, emissary-v007 and extractor-v006 ("If Gem has already approved that specific action … go ahead without waiting"). These bots can't write to GitHub, so there's no live conflict there. But the sentence still lists "pushes to public or shared repositories" as a risky action they might take, which is now impossible for them. That's untidy, not a conflict.
- **Deletions:** rule, Engineer, Safeguard and Imitator agree.
- **Merges:** rule, Engineer and Imitator agree.
- **Excluded bots:** Explorer v006 and MV v005 match Archivist v008 and the R-010 update.
- **Tokens and accounts:** rule items 4 and 5, Safekeeper, Mediator and Safeguard (gemquota writes) agree. Section numbering: the rule and Safekeeper both say section 5.
- **Log:** rule item 8 and Safeguard agree. Scorer reads it.
- **Dry-run waiver (Q3):** the rule allows none. If Gem says yes to Q3, the rule, Safeguard, Engineer and Explorer will all need the same edit.
- **New duties for bots outside the drafts:** none. All 17 live bots now have a draft or an MV citation (14 pointers + Inquirer, Inferer, Archivist via MV). The MV route is weak (item 6).

## 5. GitHub facts (read-only, 12:06 AEST)

| Claim | Result |
|---|---|
| DayneK token has admin on DayneK/vepa | **Confirmed.** `gh api repos/DayneK/vepa`: permissions admin, maintain, push, triage and pull all true; visibility public |
| `main` has no branch protection | **Confirmed.** `branches/main`: protected false; `branches/main/protection`: 404 "Branch not protected" |
| Collaborators on vepa | DayneK only |
| Pages | has_pages false |
| DayneK scopes gist, read:org, repo, workflow; gemquota broad (delete_repo, admin:org, delete:packages, admin:gpg_key, admin:public_key, admin:ssh_signing_key, …) | **Confirmed** (`gh auth status`, masked) |
| cursor-github not linked | **Confirmed** (status needsAuth) |
| freebuff-web[bot] merges and deploys | **Confirmed, and wider than stated.** PRs #15, #17 and #18 merged, plus "deploy:" commits from 1 Oct to 15 Oct (UTC). The installed-app check (`/installation`) can't be read with a user token (401) |
| Pushes 10 Oct 03:49:19 and 10:21:13 | **Confirmed** earlier from the reflog. Remote heads are unchanged: codey/complete-plans 332d74d, backup c9e5c55, main 79efba7 |
| "Keep the branch" recorded | On disk (approvals/2026-10-09-gem-direct-words.md line 44; relayed by Explorer) |

Live activity: Engineer committed "Merge origin/main … into codey/complete-plans (D-041)" locally at 12:04:47. Nothing has been pushed (the remote is still at 332d74d). Any push of this branch is a public push. Under the current live Engineer brief, it needs Gem's direct words for that push.

## Remaining issues (priority)

1. **engineer-v008 contradicts itself:** "go ahead without waiting" stays beside "only after Safeguard's dry-run report, even when Gem has approved it". The README says it was replaced; it wasn't.
2. **The three MV-only bots are weakly bound.** Inquirer, Inferer and Archivist cite the MV rule for one narrow purpose each. Add a one-line pointer each.
3. **engineer-v008 should go to Gem,** because it writes Imitator in as approver of private-push tasks (R-028).
4. Leftover base sentence in Explorer, Emissary and Extractor (low).
5. README facts and times: freebuff covers more than PRs #17 and #18 (#15 too, deploys since 1 Oct). "~12:15pm" and "~12:10pm" are in the future.

## Gem to decide

- Q1 (merged-branch deletion), Q2 ("Let engineer merge later"), Q3 (dry-run waiver), Q4 (Mediator sign-ins).
- Q5 settings: branch protection on vepa `main`, token expiry, removing GH_TOKEN_GEMQUOTA, secret scanning.
- Approving all the Gem-only drafts, plus engineer-v008 once fixed.

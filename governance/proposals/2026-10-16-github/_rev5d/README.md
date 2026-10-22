# GitHub rules: drafts, 16 Oct 2026 (revision 5, 22 Oct)

Revision 4's drafts were written at 2:54:22pm (file times from `stat`); this README was updated just after. Revision 3's drafts were written at 12:09:47. Revision 2's drafts were written at 12:02:58 and its README at 12:03:57; the "~12:15pm" and "~12:10pm" times revision 2 gave were wrong.

These are drafts only. Nothing is recorded in codex/, no profile is edited, no bot has been messaged, and no token or credential file was read; only `gh auth status` was run, with the token masked. Revision 2 fixed every item in Scrutineer's review (`reviews/2026-10-16-github-proposal-review.md`). Revision 3 fixes the re-review (`reviews/2026-10-16-github-proposal-review-2.md`). See "Revision 3 changes". Revision 4 applies Gem's answers to Q1–Q4 (see "Gem's direct words to Architect" and "Revision 4 changes"). The first build is kept at `_tools/build-r1.py.bak`.

## Revision 5 (22 Oct 2026, about 8:10pm AEST): supersedes the revision 4 hashes and paste lines below
- **Gem's 7:52pm words.** Gem told Architect directly in chat, 7:52pm 22 Oct, choosing the option that explicitly said **"no per-push approval or Safeguard check"** for Engineer on GitHub. These are Gem's direct words to Architect; they're in Architect's chat log, not on disk. **Archivist still has to record them** in approvals/ from Gem directly (R-029), so each paste line below opens with Gem restating them.
- **What reading (b) changes:**
  - github-v001 item 2: Engineer pushes, creates branches, opens pull requests and merges, on private or public repos, with no per-push words from Gem and no Safeguard dry run. It still does its own secret and content scan, and it logs each action. Safeguard reviews from the log afterwards, never as a gate.
  - **Not covered** (unchanged, Gem's direct words and a dry run): a pull request to a repo Gem doesn't own (an outgoing message); a push or merge that triggers a production or public deployment (connector limits, item 7); every other deletion, force-push and history rewrite; new public repos, gists and packages; visibility, settings, collaborators and apps; accounts and tokens. If "fully free" was meant to reach these too, Gem says so.
  - Engineer, Safeguard and Imitator drafts match. Their R-020 sentences now except Engineer's pushes and merges.
- **The other pending items:**
  - Every clashing draft is rebased (stacked) on the redundancy batch, and Imitator and Arbiter also on the r044-veto batch (`proposals/2026-10-22-r044-veto/`). Six redundancy drafts are already recorded (inferer v006, arbiter v006, architect v005, emissary v007, extractor v006, explorer v006), so those use the codex as their base. The other six stack on unapproved drafts; if Gem declines one, that GitHub draft is rebased on the codex.
  - **Record order:** the redundancy batch, then r044-veto, then this batch.
  - **Other items applied:**
    - GitHub-xai acts as gemquota under items 1, 2 and 4, and its platform-held token falls outside section 5's storage and rotation steps (T-016).
    - R-039 is restated for gemquota, and Mediator's one-off repo tasks are in the rule and in mediator-v007.
    - The Mediator sign-in hand-over (Q4).
    - Recurring syncs are a new item 9; the vault is a new item 10 (RR-042), with Engineer as its only writer unless Gem names another.
    - The gvmw content exception points to connector-limits v003.
    - Engineer's base exception is widened to "any GitHub action the shared GitHub rule sends to Safeguard".
    - Engineer gets the R-044 wording.
    - archivist-v010 goes to Gem.
- **Revision 5a (about 8:15pm), fixing Scrutineer's review (`reviews/2026-10-22-github-r5-review.md`):**
  - **R-020/R-036 tension superseded by R-045** (7:56pm). R-045 rules that Gem's words (7:19pm in Inquirer's chat, 7:52pm in Architect's chat) supersede R-036 and R-020's per-push dry run for Engineer on GitHub. The drafts now cite R-045.
  - **gvmw exception (R-045 update):** Gem's 7:55pm words to Engineer, "Turn it on now, with a scan and dry run each push", bind for gvmw. So every gvmw push, each daily-sync run included, needs a secret scan and a Safeguard dry run. This is now in github-v001 (items 2 and 9), safeguard-v008 and engineer-v008. It also settles the v003 tension for gvmw: a scan and a dry run for each push.
  - **explorer-v007:** "a public or shared push still needs Gem's own words to Engineer" is removed. It now reads "Engineer acts under the shared GitHub rule (R-045)".
  - **imitator-v009:** inherits the fixed imitator-v008. Imitator may change other bots' schedules but not its checkers' schedules without Gem's words (R-045, R-046).
  - **arbiter-v008 moves to Gem only.** Its base arbiter-v007 gives Imitator a veto (R-028).
  - The revision 5 files are kept in `_rev5a/`, and the build in `_tools/build-r5a.py.bak`.
- **Reviews:** Scorer must re-check scrutineer-v006, since its PASS was on the old text. Scrutineer reviews the rest.

- **Revision 5b (about 8:20pm), for R-047 and R-048:**
  - github-v001 item 2, engineer-v008 and safeguard-v008 now carry the named-projects grant. Engineer may make VEPA, Codey, swarm, SLAP.RED/Golf and MedB public after Safekeeper's scan (a secret blocks) and Safeguard's one-time dry run (it informs and doesn't block). MedB's data/ is out unless Gem names it, and SLAP.RED/Golf's gambling and BIE material is out until the rule 6 change.
  - emissary-v009 stacks on r044-r047's emissary-v008.
  - imitator-v009 and arbiter-v008 are re-stacked.
  - gvmw keeps a scan and a dry run for each push.
  - **The whole batch now goes to Gem (R-027).** The revision 5a files are in `_rev5b/`.

- **Revision 5c (8:20pm, frozen), for R-049:**
  - explorer-v007's deletion line now needs a verified off-computer backup, checked by another bot, only for code, notes, configs and bot instructions. Mass wipes are never allowed. Source: Gem's words in Inquirer's chat at 8:07pm, verified by Arbiter.
  - imitator-v009 and emissary-v009 are re-stacked on the r044-r047 revision 4 drafts.
  - The revision 5b files are in `_rev5c/`.

### Hashes (revision 5c)
| Draft | Base text | New text | File | Approver |
|---|---|---|---|---|
| github-v001 | - | 7a1c70ebd117 | 1e89b34edde7 | Gem |
| engineer-v008 | f00015f7701c | dda5eeb9977d | 7a96b726ecf0 | Gem |
| imitator-v009 | d6325ee0c6a8 | 26914191a8c3 | 5aad70f7f044 | Gem |
| safeguard-v008 | f79fcaa7f2cf | 2aabcb9d416a | e735c056f593 | Gem |
| safekeeper-v006 | 61a0649cf271 | 63f17cc83cca | 16da327822d5 | Gem |
| explorer-v007 | 94aafeffa6ce | a98d235b093a | 051f20c9e68b | Gem |
| emissary-v009 | 1f4a1ffa2d25 | db12061dc422 | 8e41473bd091 | Gem |
| extractor-v007 | 13c04fcd6b78 | 3a5554d96379 | 819b45bfa114 | Gem |
| mediator-v007 | caf84f624c4d | 345b94138142 | 7e9816c7ce6b | Gem |
| mender-v006 | 31e7be0b0f53 | c726aaac1ab3 | 66b111600444 | Gem |
| architect-v006 | d290277295ef | c2e149404e57 | 832b6144afa6 | Gem |
| arbiter-v008 | 3d031639639f | 8a9498236d52 | aa6a956663ba | Gem |
| scorer-v006 | 08e5ccfc52b4 | aea931e86d5f | 335b9f0d3729 | Gem |
| scrutineer-v006 | 30cb80b9ac8f | e4813a3f42b7 | 67357670924e | Gem |
| investigator-v006 | c8bafae381de | c14cca83ac11 | f9013fafc284 | Gem |
| message-verification-rule-v005 | 234588448cfc | c78245bcf145 | 7b7fd32c1f97 | Gem |
| inquirer-v005 | a0469f4a9700 | caf7cce419da | 11598175fbf1 | Gem |
| inferer-v007 | 441b92c9fcd4 | 65660cac2123 | 07a69900b7f6 | Gem |
| archivist-v010 | c9a2d1b3bf70 | f7c447d262e0 | 8bbad9c29613 | Gem |

### Paste line (revision 5c, Gem only)
- `I confirm I told Architect directly in chat at 7:52pm on 22 Oct that Engineer is fully free on GitHub, with no per-push approval or Safeguard check, and that the gemquota/gvmw daily sync is on (my 7:55pm words), with gvmw per-push checks as my card answer says (none per R-051 until then). I approve GitHub batch revision 5c, recorded after the redundancy and r044-r047 batches: github-v001 (7a1c70ebd117), engineer-v008 (dda5eeb9977d), imitator-v009 (26914191a8c3), safeguard-v008 (2aabcb9d416a), safekeeper-v006 (63f17cc83cca), explorer-v007 (a98d235b093a), emissary-v009 (db12061dc422), extractor-v007 (3a5554d96379), mediator-v007 (345b94138142), mender-v006 (c726aaac1ab3), architect-v006 (c2e149404e57), arbiter-v008 (8a9498236d52), scorer-v006 (aea931e86d5f), scrutineer-v006 (e4813a3f42b7), investigator-v006 (c14cca83ac11), message-verification-rule-v005 (c78245bcf145), inquirer-v005 (caf7cce419da), inferer-v007 (65660cac2123), archivist-v010 (f7c447d262e0) — record and deploy, github-v001 first.`

## Source: relayed by Explorer
- **Gem in Explorer's chat, 11:46am 16 Oct** (`approvals/2026-10-16-gem-direct-words.md` line 34): "stay signed in to DayneK and gemquota using the full access classic tokens, add rules to governance on what bots are allowed to do what with GitHub."
- **This reached Architect as a relay from Explorer** (R-008, R-018). The approver confirms with Gem directly. The same message's "Approve all drafts" is relayed too, so it doesn't approve these drafts.
- **P5 went live at 11:47am.**
- Gem asked for this, so Architect's weekly cap doesn't apply.
- **Inputs:** `input-safeguard.md` and `input-safekeeper.md` are both folded in. Neither is missing.

## Gem's direct words to Architect (2:51pm, 16 Oct)
- **Gem in Architect's own chat, 2:51pm 16 Oct**, answering Q1–Q4 below: "1. Sure. 2. Meh just let him cook. 3. Let him cook. 4. Yes."
- These are Gem's direct words to Architect. **They approve the policy, not the draft text.** Each Gem-only draft still needs Gem's own words to Archivist (in Archivist's chat or on a call) before it's recorded and deployed (R-029).
- How each answer was read, narrowly:
  - **Q1 "Sure":** Engineer may delete its own merged branches in private, unshared repos without asking each time, after logging each branch's commit id. Every other deletion is unchanged.
  - **Q2 "let him cook":** Engineer may merge its own pull requests in private, unshared repos without a sign-off each time, after its fresh-context verifier passes, the secret and content scan is clean, and a log line. Public or shared merges still need Gem's words and a dry run (unless waived). Anyone else's pull requests still need a sign-off.
  - **Q3 "Let him cook":** Gem may waive the Safeguard dry run for one specific push or merge, in direct words naming it. Without a waiver the dry run applies. Waivers are logged with Gem's quote.
  - **Q4 "Yes":** Mediator may add or switch GitHub sign-ins when Gem asks it directly. It never reads, prints or stores a token outside the gh store, and it tells Safekeeper the same day.

**Flag: Q2 relaxes the "no bot verifies its own work" principle.** Engineer merges its own private pull requests without a separate sign-off. That rests on Gem's explicit words. What stays: the fresh-context verifier (its brief requires it before a merge), the scan, the log, and Scrutineer's audit. Safeguard checks the log.

**Token advice (Safekeeper):** tokens shouldn't be pasted into chat. Mediator's draft therefore uses only the browser sign-in that Gem completes on GitHub (`gh auth login --web`) or `gh auth switch`. A token pasted into chat isn't used; it's treated as a suspected leak, and Gem replaces it. *Judgement call:* if Gem wants Mediator to accept a pasted token, that's a further change, and Safekeeper should give its view first.

## Deploy order (every pointer draft)
**Every draft in this batch that points to the GitHub rule deploys only with or after `github-v001.md` is recorded in the codex.** That's every bot draft and message verification v005. `codex/_shared/github/` doesn't exist yet, so a pointer deployed first would point at a missing rule. This was Scorer's condition for scrutineer-v005 (`reviews/2026-10-16-scrutineer-v005-review.md`), applied to the whole batch. Each draft's header carries it as "Deploy order".

## Independent review of Scrutineer's own draft
Scrutineer can't review its own brief, so Scorer reviewed scrutineer-v005 at about 12:10pm. Result: **PASS**, on the deploy-order condition above. The draft text is unchanged in revision 3 (sha256 7ac501be76bb, the hash Scorer checked). It's Gem-only (R-015, R-027).

## Revision 3 changes
| # | Re-review item | Change |
|---|---|---|
| 1 | engineer-v008's base sentence "tell Safeguard before you act and go ahead without waiting" contradicts the dry run | That sentence now ends: "except for GitHub actions on public or shared repos and any deletion, which always wait for Safeguard's report as the shared GitHub rule sets out". The same tidy is made in Explorer, Emissary and Extractor: "this never covers GitHub writes or deletions, which you don't make yourself". |
| 2 | Inquirer, Inferer and Archivist only weakly bound through the message verification rule | New one-line read-only pointers: `inquirer-v005`, `inferer-v006`, `archivist-v009`. Each is based on the latest codex version and byte-checked against live. Archivist's line doesn't touch its deploy route, so Imitator may approve it. But it's Archivist's own brief, so it deploys only on Gem's request (Archivist v008 case a). The message verification item 5 stays as a backstop. |
| 3 | engineer-v008 should go to Gem | Now Gem-only: it names Imitator as an approver of private-push tasks in another bot's brief, which widens Imitator's effective role (R-028). |
| 4 | Facts and times | freebuff-web[bot] and Scrutineer's 12:06 API checks are corrected in "Facts checked". Timestamps now come from `stat` (see the top). |

## Revision 4 changes
| Gem's answer | Drafts changed | Change |
|---|---|---|
| Q1 | github-v001, engineer-v008, safeguard-v007 | New matrix row: Engineer's own merged branch in a private, unshared repo, deleted without asking, commit id logged first. Engineer's "every deletion" line becomes "every other deletion". Safeguard's deletion trigger excludes these and checks their log lines. |
| Q2 | github-v001, engineer-v008 | Merge row: Engineer merges its own private PRs after the verifier, scan and log; anyone else's PRs still need a sign-off; public or shared merges need Gem's words and a dry run. Engineer's sign-off line now reads "doesn't sign off its own code … One exception, on Gem's explicit words". |
| Q3 | github-v001, engineer-v008, safeguard-v007 | New "Dry-run waiver" paragraph: one named push or merge, logged with Gem's quote first. A waiver never covers deletions, settings, account rows, or a push that might contain secrets or restricted data. Engineer's dry-run sentences and Safeguard's triggers and log check reflect it. Log lines carry the waiver quote. |
| Q4 | github-v001, mediator-v007, safekeeper-v006 | Matrix row split: adding or switching an account is Gem's, or Mediator's on Gem's direct request; tokens, sign-out, keys and the cursor-github link stay Gem-only. Browser sign-in only; log the action and tell Safekeeper the same day. Item 4: a switch with a log line isn't "unexpected". Safekeeper records Mediator's notices. |
| Routing | mediator-v007 | Moves to **Gem**: it grants a sign-in power that the shared rule keeps out of Imitator's reach (R-019, R-027). |

Engineer's approver: Imitator still appears in engineer-v008, as an approver of private-push tasks, and as never a merge sign-off. So it stays **Gem** (R-028). It also carries Gem's new merge, deletion and waiver policy.

Unchanged texts: the other 13 drafts' instruction texts are identical to revision 3; only the build time in their headers changed. scrutineer-v005's text is still 7ac501be76bb, the hash Scorer passed.

## Questions for Gem (Q1–Q4 answered at 2:51pm; Q5 still open)
1. **Q1, deleting branches.** Every deletion needs your direct words for now. Should Engineer be allowed to delete its own merged branches in private repos without asking each time? If yes, it logs each branch's commit id first, so the branch can be restored.
2. **Q2, "Let engineer merge later".** Is this a go-ahead for later, with each merge still needing your sign-off, or someone you name, of that change? Or do you want Engineer to merge on its own? Merging on its own would mean Engineer signs off its own code, which its brief forbids.
3. **Q3, skipping the dry run.** A public or shared push now needs your words and a Safeguard dry run. Do you want to be able to say "no dry run" for a specific push?
4. **Q4, Mediator and sign-ins.** At 11:19am Mediator added gemquota to the gh CLI from a token you gave it. Under the rule, adding or switching GitHub accounts is yours alone. Should Mediator be allowed to do this on your direct request? The default is no, and tokens shouldn't be pasted into chat.
5. **Q5, settings only you can change:**
   - branch protection on DayneK/vepa `main`, which has none;
   - expiry dates on both tokens;
   - removing the duplicate `GH_TOKEN_GEMQUOTA` copy;
   - GitHub secret scanning and push protection.

## Changes for each of Scrutineer's items (revision 2)
The items 2, 6 and J4 rows below are from before Gem's 2:51pm answers. Revision 4 replaces them where they differ.

| # | Scrutineer item | Change |
|---|---|---|
| 1 | Public or shared push go-ahead unstated | **Rule:** a public or shared push, PR or merge needs Gem's direct words **and** a Safeguard dry run. **Shared:** if you're unsure whether a repo is shared, treat it as public, and check with `gh repo view --json visibility` and the collaborators list. **Stop rule:** if Safeguard has a concern or hasn't replied, stop and ask Gem. **Relays:** work routed by another bot doesn't give Engineer Gem's words. **Engineer's brief:** it now waits for the dry run even when Gem has approved, instead of its base "tell Safeguard and go ahead". |
| 2 | J7, Engineer deleting branches on its own | Removed. Every deletion (branches, tags, releases, packages, repos), force-push and history rewrite needs Gem's direct words naming the item, a Safeguard dry run, and the commit id logged first (R-034, R-019). Whether to allow merged-branch deletion in private repos is now Q1. |
| 3 | Gists, packages, account keys, apps | Added to the matrix. **Gists and package publishing:** public (a "secret" gist is public by link), so Gem's words and a dry run. **Package deletion:** a deletion. **Account SSH, GPG and signing keys:** Gem only. **GitHub Apps and bots:** installing or changing them is a settings change. **Repos an outside app can write to:** count as shared. **Deploys:** a merge that triggers an app or Actions deploy counts as a public deployment. **freebuff-web[bot]:** see "Facts checked" for the corrected history. |
| 4 | Content trigger dropped | Restored in item 3: never push or publish secrets, configs, personal data, or scraped, BIE, gambling, casino or pokies data to any repo, gist or package, public or private. Anything that might hold such content goes to Safeguard first. **safeguard-v007** gets a stop rule: if a planned action would put that content on GitHub, or a public or shared action lacks Gem's words, it asks the bot to stop and alerts Gem. |
| 5 | Merge sign-off inconsistent | One rule. The change is signed off by Gem, or by a reviewer Gem named in direct words, never Engineer or Imitator. Public or shared merges also need Gem's direct words for that merge and a dry run. Imitator may approve no merge. The same wording is in the rule, the Engineer brief and the Imitator brief. |
| 6 | Ten bots unbound; Mediator; log owner | See "How every bot is bound" and "Log owner" below. Mediator's sign-in conflict is fixed in `mediator-v007` (and is Q4). |
| 7 | Facts | Fixed in the rule and this README. See "Facts checked". |
| 8 | Stale wording | Explorer and Emissary: "pushes to shared repositories" becomes "pushes to public or shared repositories". engineer-v008: the Gem-only list now says "Gem's direct words and a Safeguard dry run". |
| J3 | Do private pushes need approval? | Yes, a task approval. Engineer pushes to a private, unshared repo only for a task Gem or Imitator approved, after the secret and content check, then logs it. No dry run. |
| J4 | "Let engineer merge later" | Now Q2. No standing merge right is drafted. |
| Other | Stop rules Scrutineer listed as missing | **Scan can't run:** don't push. **Unexpectedly on gemquota:** switch back, do nothing else, log it, tell Safekeeper. **Env check:** names only. **Log:** append-only. |

## How every bot is bound
No shared rule is cited by every brief. The message verification rule is cited by name in 6 briefs: Emissary, Extractor, Inquirer, Inferer, Archivist and Safekeeper. Connector limits is cited by 6 (Engineer, Emissary, Extractor, Explorer, Mediator and Safeguard). So the binding works in two layers:
- **Message verification v005** gets a new item 5, "GitHub": every bot follows the GitHub rule, and reads only unless its brief gives it a GitHub role. This reaches Archivist, Inquirer and Inferer. The cookie-seed item becomes item 6; no brief refers to it by number.
- **Every other bot gets a one-line pointer in its own brief:**
  - The 7 with real GitHub roles or risk: Engineer, Imitator, Safeguard, Safekeeper, Explorer, Emissary and Extractor.
  - The 7 that cite neither shared rule: Mediator, Mender, Architect, Arbiter, Scorer, Scrutineer and Investigator.
  - The read-only pointer allows reading, git history and read-only remote checks, which is what Scorer and Scrutineer already do. It bars signing in, switching accounts and any change.
- **Scorer's pointer** also tells it to use the GitHub log.

Result (revision 3): all 17 live bots carry their own pointer line. Inquirer, Inferer and Archivist got theirs in revision 3, because their briefs cite the message verification rule only for one narrow purpose each. The message verification rule's item 5 is a backstop.

## Log owner
**Default:** Safeguard owns `/workspace/governance/github-log.md`. It sets the format and checks the log at each scheduled run against git history and the remotes. Every bot that makes a write appends one line; in practice that's Engineer. The log is append-only, never edited and never holds secrets.

**Why:**
- The log exists so Safeguard can find writes that didn't come to it first.
- The writer can't own the record of its own actions, because no bot verifies its own work.
- Scrutineer already audits Safeguard's reviews, so the check is itself checked.

**Alternative:** Engineer owns the log and Safeguard checks it. That's weaker, because Engineer would own the record of its own writes.

## Facts checked
| Fact | Checked how | Result |
|---|---|---|
| DayneK active; scopes gist, read:org, repo, workflow | `gh auth status` (token masked), ~12:05pm | Verified. Not "full access" |
| gemquota: broad scopes, including delete_repo, admin:org, delete:packages, admin:gpg_key, admin:public_key, admin:ssh_signing_key, admin:org_hook, admin:repo_hook | `gh auth status` | Verified. Broad, but the rule doesn't call it "full access" |
| DayneK's token has admin on vepa; `main` has no branch protection | Scrutineer's read-only `gh api` GETs at 12:06 (re-review section 5) | **Confirmed by Scrutineer.** Permissions admin, maintain, push, triage and pull are all true; `main` protected false (protection: 404). Collaborators: DayneK only. Pages off. Architect didn't call the API itself |
| cursor-github isn't linked | Tool status: "needsAuth" (not connected) | Verified |
| Gem said "Keep the branch" at 11:10am, so the backup branch isn't pending | `approvals/2026-10-09-gem-direct-words.md` line 44; RR-017 closed | Verified on disk (relayed by Explorer) |
| Backup branch push at 10:21:13 on 10 Oct | `/workspace/vepa` remote reflog: `c9e5c55 … 2026-10-10 10:21:13 +1000: update by push` | Verified. R-030 final says 10:18am and Imitator's log says 10:20; the reflog wins |
| codey/complete-plans push at 03:49:19 on 10 Oct | remote reflog `332d74d` | Verified |
| freebuff-web[bot] merges and deploys on vepa | `git log --author=freebuff` | Verified (see the correction row below). That a merge triggers the deploy is inferred |
| freebuff-web[bot] history (correction) | `/workspace/vepa` `git log --all --author=freebuff` | Verified. 25 "deploy:" commits (12 Sep–15 Oct, UTC), 13 PR merges (#4–#13, #15, #17, #18; 20 Sep–15 Oct), and 3 code or docs commits of its own (19 Sep, 10 Oct). So it writes code as well as merging and deploying |
| Mediator handled the gemquota sign-in at 11:19am | `connectors.md` line 35, RR-033 | Verified on disk |
| GH_TOKEN_GEMQUOTA exists; gitleaks isn't installed | Scrutineer | Not re-checked (name only). I didn't list the environment |

## Files and approvers
Every bot base is that bot's latest codex version, byte-compared against its live profile when the drafts were built at 2:54:22pm. All matched, and none had a newer codex version.

| File | Base → new | Approver |
|---|---|---|
| `github-v001.md` | new `_shared/github/` | **Gem** (checker-owned, R-027) |
| `message-verification-rule-v005.md` | _shared v004 → v005 | **Gem** (owner Safekeeper, R-027) |
| `imitator-v007.md` | clone v006 → v007 | **Gem** (R-015) |
| `safeguard-v007.md` | compliance-risk-officer v006 → v007 | **Gem** (R-027) |
| `safekeeper-v006.md` | secrets-credentials-custodian v005 → v006 | **Gem** (R-027) |
| `scorer-v005.md` | assessor v004 → v005 | **Gem** (R-027) |
| `scrutineer-v005.md` | auditor v004 → v005 | **Gem** (R-027). Scorer: PASS, on the deploy-order condition |
| `investigator-v005.md` | investigator v004 → v005 | **Gem** (R-015, R-027) |
| `engineer-v008.md` | codey v007 → v008 | **Gem** (R-028: names Imitator as a private-push approver) |
| `explorer-v006.md` | explorer-copy v005 → v006 | **Gem** (Explorer's brief; R-034) |
| `mediator-v007.md` | connector-steward v006 → v007 | **Gem** (sign-ins on Gem's request, R-019, R-027) |
| `emissary-v007.md` | grok-bot v006 → v007 | Imitator (Gem may) |
| `extractor-v006.md` | scraper v005 → v006 | Imitator (Gem may) |
| `mender-v006.md` | mender v005 → v006 | Imitator (Gem may) |
| `architect-v005.md` | instruction-architect v004 → v005 | Imitator (Gem may). Architect's own brief, approved by someone else |
| `arbiter-v006.md` | arbiter v005 → v006 | Imitator (Gem may) |
| `inquirer-v005.md` | identity-inquirer v004 → v005 | Imitator (Gem may) |
| `inferer-v006.md` | identity-inferer v005 → v006 | Imitator (Gem may) |
| `archivist-v009.md` | codex-keeper v008 → v009 | Imitator (Gem may). Own brief, so it deploys only on Gem's request |

**Order and routing:**
- **Gem directly (11):** github-v001, message verification v005, Imitator, Safeguard, Safekeeper, Scorer, Scrutineer, Investigator, Explorer, Engineer and Mediator.
- **Imitator, or Gem (8):** Emissary, Extractor, Mender, Architect, Arbiter, Inquirer, Inferer and Archivist.
- All of them deploy only with or after github-v001 (see "Deploy order").
- If Imitator approves them, Archivist may deploy them under the R-010 update: a 1:1 confirmation with Imitator and a Safeguard dry run.
- imitator-v007 narrows Imitator. engineer-v008 gives Imitator a small gate (private-push tasks), so it's Gem's (R-028). None of the 8 Imitator-approvable drafts widens Imitator.

## Hashes (revision 4, superseded; drafts kept in `_rev4/`)
The file hash covers the whole draft file. The text hash covers only the verbatim fenced instructions, which is what gets recorded and deployed.

| File | File hash | Text hash |
|---|---|---|
| `arbiter-v006.md` | 3bce25e391ea | 8f7cbde98e08 |
| `architect-v005.md` | 2cd87ddbee04 | 59e70088bf08 |
| `archivist-v009.md` | c2c82efa4970 | ba2b1bffe723 |
| `emissary-v007.md` | 2e5d749cacae | 3e382764d584 |
| `engineer-v008.md` | d31300baedf8 | 5993e0a14618 |
| `explorer-v006.md` | f2107aebdf4c | bccaf550b8f5 |
| `extractor-v006.md` | 4a166cd1f59d | a1f873eca6f1 |
| `github-v001.md` | 7d43513b35a5 | 6a7dfc5cf997 |
| `imitator-v007.md` | ce60389e0a2d | cd63beadaf5b |
| `inferer-v006.md` | 28c2ad9030f5 | 73526e90ac9e |
| `inquirer-v005.md` | 004fec7ff0b3 | caf7cce419da |
| `investigator-v005.md` | c8f276d95f66 | 45b626cf2470 |
| `mediator-v007.md` | 80bf2ea59287 | 017c80c21b59 |
| `mender-v006.md` | e38a52f00282 | c726aaac1ab3 |
| `message-verification-rule-v005.md` | 7b7fd32c1f97 | c78245bcf145 |
| `safeguard-v007.md` | a38d458b8abd | ab095be8ab46 |
| `safekeeper-v006.md` | 7d253bb38699 | 63f17cc83cca |
| `scorer-v005.md` | 3d632a7a0f88 | 6342ea59d915 |
| `scrutineer-v005.md` | a1d7068adf5a | 7ac501be76bb |

## Owner of the shared rule (J1, unchanged)
Safeguard owns the rule and its log. Safekeeper owns section 5 (tokens). Any change is Gem-only (R-027).
- Engineer can't own it: it's the bot the rule limits most, and its brief forbids setting its own governance rules.
- Imitator can't own it, because the rule limits Imitator.

## Matrix summary (in full in github-v001, item 2)
**Visibility:** "shared" means another collaborator, any organisation repo, or an outside app that can write. It counts as public. If in doubt, a repo is public.

**Who can act:**
- **Any bot:** read, list, search, clone.
- **Engineer only:** commits, pushes, branches, opening pull requests and merging.
- **Imitator:** reads only, and never pushes.

**Rules by action:**
- **Private pushes and PRs:** need a task approved by Gem or Imitator, a secret and content check, and a log line.
- **Public or shared pushes, PRs and merges:** Gem's direct words **and** a Safeguard dry run, unless Gem waives the dry run for that one action in direct words (logged).
- **Merges in private repos:** Engineer's own PRs after the verifier, scan and log. Anyone else's need sign-off by Gem or a reviewer Gem names, never Engineer or Imitator.
- **Engineer's own merged private branches:** deleted without asking, commit id logged first.
- **Other deletions, transfers, force-pushes, history rewrites:** Gem's words naming the item, a dry run, and the commit id logged first. Never waivable.
- **New public repos, forks, gists and package publishing:** Gem's words and a dry run.
- **Visibility, settings, collaborators, hooks, keys, workflows, Actions, Pages and apps:** Gem's words and a dry run.
- **Adding or switching a sign-in:** Gem, or Mediator on Gem's direct request (browser sign-in only, logged, Safekeeper told the same day).
- **Tokens, sign-out, account keys and the cursor-github link:** Gem only.

**Content:** no secrets, personal data, or scraped, BIE or gambling data in any repo.

**Accounts:** DayneK is the default. gemquota is used only when Gem names it, and the bot switches back afterwards.

**Stop rules:**
- Safeguard has a concern or no reply: ask Gem.
- The scan finds something or can't run: don't push.
- A step would go beyond what Gem's words named: stop.

## Judgement calls (defaults)
- **J1. Owner:** Safeguard, with Safekeeper owning the tokens section (above).
- **J2. Imitator never pushes,** even with Gem's approval.
- **J3. Private pushes:** need a task approved by Gem or Imitator, plus the scan and a log line. No dry run.
- **J4. Merges:** Gem's Q2 answer, drafted narrowly (own private PRs only).
- **J5. Only Engineer commits.** Adding a remote to a scratch repo, or pushing one, counts.
- **J6. Log:** Safeguard owns it, and writers append.
- **J7. Deletions:** Gem's Q1 answer (own merged private branches only).

## Actions for named owners (drafted, not done)
1. **Gem:**
   - Remove `GH_TOKEN_GEMQUOTA` once gh works for gemquota.
   - Set token expiry dates, at most 90 days.
   - Consider branch protection on vepa `main`.
   - Turn on secret scanning and push protection.
2. **Engineer:** install gitleaks after telling Safeguard, once v008 is approved.
3. **Safekeeper:** add token expiry rows (no values) to the inventory. Move the tokens to 1Password once Gem connects it.
4. **Safeguard:** create `github-log.md`. Consider seeding it with the 10 Oct vepa pushes (03:49:19 and 10:21:13).

## FYI
- **Public repos on gemquota:** Scrutineer found repos named bonus-scraper-engine, bonus-scraper-pro, dayne-bonuses and affiliate-pages (names only). They predate this rule but are relevant to RR-028.
- **"Make the spreadsheet public":** relayed through Explorer at 11:46am. If it means the BIE sheet, Safeguard should dry-run it first (R-031, connector limits item 3).

## Pending (revision 5): all applied in revision 5 (see the top), except Gem's vault-writer question, which now defaults to Engineer only
- Rebase every draft on the redundancy batch (proposals/2026-10-22-redundancy/, recorded first): 12 bots clash on version and base. Redo hashes; Scorer re-checks scrutineer-v005. Route archivist-v009 to Gem only. engineer-v008: consider 'Explorer assigns new work' (R-044) in place of 'from Explorer or another bot on Gem's behalf'.
- Rev 5: state GitHub-xai acts as gemquota under items 1, 2, 4 (Safekeeper T-016)
- Rev 5, Safekeeper section 5: GitHub-xai's token is held by the platform, so section 5's storage and rotation steps don't apply to it; revoking it means disconnecting it, which is Gem's call (Safekeeper T-016; moved here from connector-limits v002 revision 4).
- Rev 5, vault (Safeguard RR-042): DayneK/obsidian-vault is private, with 6 skeleton files and no breach.
- Rev 5, vault (Safeguard RR-042): a synced vault never holds secrets, personal data about other people, or BIE or gambling data.
- Rev 5, vault (Safeguard RR-042): making the vault public or adding collaborators needs Gem's direct words plus a Safeguard dry run.
- Rev 5, vault, question for Gem (Safeguard RR-042): who may push to the vault? Engineer as the only writer, or Mediator for the vault only.
- Rev 5, gvmw (connector-limits v003 draft, 22 Oct): github-v001 bars BIE and gambling data from any repo; add the same narrow gvmw exception (gemquota/gvmw only, content as of commit 4f43fc9), or rule 14's deference undoes v003.
- Rev 5 (Scrutineer, reviews/2026-10-22.md): cover recurring syncs under R-036. A recurring auto-sync publishes new content on every run, so state what Gem's words must name for it, above all for a public repo (R-040, R-041).
- Rev 5 (Scrutineer, reviews/2026-10-22.md): restate R-039 for gemquota.
- Rev 5, R-039: Mediator may do one-off repo tasks Gem gives it directly; routine repo work is Engineer's.
- Rev 5 (Scrutineer, review-3): widen Engineer's exception to "any GitHub action the shared GitHub rule sends to Safeguard".
- Rev 5 (Scrutineer, review-3): route archivist-v009 to Gem.
- Rev 5, Q4: Mediator signs in only after Gem authorises it, then hands over to Safekeeper.

## Revision 5d (after Scrutineer's frozen re-check)
- gvmw lines (github-v001 items 2 and 9, engineer-v008, safeguard-v008): the daily sync is on (Gem 7:55pm); per-push/per-run checks follow the gvmw rule: none per R-051, Gem's card pending (both stated).
- safeguard-v008 F4: 'whose every push' rewritten unambiguously.
- R-050 per-project holds cited in github-v001 and engineer-v008.
- `_rev5c/` now holds the real frozen 5c files (the old 5b snapshot moved to `_rev5c-was-5b-snapshot/`). Build backup `_tools/build-r5c.py.bak`.
- Note: the redesign batch supersedes several of these drafts (see 2026-10-22-redesign/README.md).

### Paste line (revision 5d, survivors only, if the redesign batch is approved)
- `I confirm I told Architect directly in chat at 7:52pm on 22 Oct that Engineer is fully free on GitHub, with no per-push approval or Safeguard check, and that the gemquota/gvmw daily sync is on (my 7:55pm words), with gvmw per-push checks as my card answer says (none per R-051 until then). I approve GitHub batch revision 5d, after the redundancy, r044-r047 and connector-limits v003 batches: github-v001 (7a1c70ebd117), engineer-v008 (dda5eeb9977d), imitator-v009 (26914191a8c3), explorer-v007 (a98d235b093a), architect-v006 (c2e149404e57), arbiter-v008 (8a9498236d52), message-verification-rule-v005 (c78245bcf145) — record and deploy, github-v001 first; the other twelve are replaced by the redesign batch.`

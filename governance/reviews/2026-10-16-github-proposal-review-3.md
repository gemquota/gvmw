# Re-check: GitHub proposal batch, revision 3, 16 Oct 2026 (AEST)

Reviewer: an independent executor, run for Scrutineer (`affe0344`). Read-only. Checked 2:53–2:57pm AEST, Fri 16 Oct 2026. This file is the only thing written. No scratch files. Nobody was messaged. No token or credential file was read. Live calls were read-only: `git ls-remote`, `git log`, `git reflog`, `git status` in `/workspace/vepa`.

## Important: the batch moved to revision 4 during this check

- At 2:53pm the drafts were revision 3 (written 12:09:47, README 12:10:22). I hashed all 19 drafts then.
- At 2:54:22pm Architect rewrote every draft as **revision 4** (README 2:54:56pm; revision 3's build kept as `_tools/build-r3.py.bak`). Revision 4 applies Gem's answers to Q1–Q4, which the README says Gem gave in Architect's chat at 2:51pm.
- Revision 4 changed the instruction text of **5 drafts**: github-v001, engineer-v008, safeguard-v007, safekeeper-v006 and mediator-v007. The other 14 are byte-identical to revision 3. (The README says "the other 13"; it's 14.)
- This report checks revision 3, as asked. **Revision 4's 5 changed texts haven't been reviewed by anyone.**
- Gem's 2:51pm words to Architect ("1. Sure. 2. Meh just let him cook. 3. Let him cook. 4. Yes.") are **not on disk** in `approvals/` or `risk/register.md`. They're only in the README.

## 1. The 4 items (revision 3 drafts)

1. **Engineer's "go ahead without waiting": fixed, with a small gap.**
   - engineer-v008 (rev 3, also in `build-r3.py.bak`): "If Gem has already approved that specific action in your own chat, tell Safeguard before you act and go ahead without waiting, except for GitHub actions on public or shared repos and any deletion, which always wait for Safeguard's report as the shared GitHub rule sets out."
   - Explorer, Emissary and Extractor now add: "this never covers GitHub writes or deletions, which you don't make yourself (shared GitHub rule)."
   - Gap (low–medium): the exception names only "public or shared repos and any deletion". It doesn't cover the other rows the rule sends to Safeguard on a private repo: visibility (private to public), settings, collaborators, apps, a new public repo, a gist or a package. Another Engineer sentence still says these need "Gem's direct words and a Safeguard dry run". So the conflict is much smaller, but it isn't gone. Fix: "except for any GitHub action the shared GitHub rule sends to Safeguard".
2. **Pointers for Inquirer, Inferer and Archivist: fixed.**
   - Each adds one sentence and nothing else: "On GitHub you only read (view, list, search, clone into /workspace, git history and read-only remote checks), following the shared GitHub rule at /workspace/governance/codex/_shared/github/ (highest version; …".
   - inquirer-v005 4406 → 4720 chars; inferer-v006 4693 → 5007; archivist-v009 7076 → 7390 (+314 each, same as the other pointer bots).
   - Minor: archivist-v009 is listed "Imitator (Gem may)". Archivist v008 case (b) excludes Archivist's own instructions, so it can deploy only on Gem's request. In practice it's Gem's. Simpler to route it to Gem.
3. **engineer-v008 to Gem: fixed.** Header: "NEEDS GEM'S DIRECT APPROVAL". README: "Now Gem-only: it names Imitator as an approver of private-push tasks … (R-028)".
4. **README freebuff facts and times: fixed.**
   - "25 'deploy:' commits (12 Sep–15 Oct, UTC), 13 PR merges (#4–#13, #15, #17, #18; 20 Sep–15 Oct), and 3 code or docs commits of its own (19 Sep, 10 Oct)". I re-counted with `git log --all --author=freebuff`: 25, 13 (#4–#13, #15, #17, #18) and 3. Correct.
   - The README's file times now match `stat` (drafts 12:09:47).
   - Residual time slip: Scorer's review file was created at **12:09:00**, but it says "Reviewed … at about 12:10pm" and "as of 12:10pm". The README repeats "about 12:10pm". Small, but it's the same kind of future-dated time. Also, R-036 is headed "2:55pm", but rulings.md was last written at 2:53:39pm when I read it.

## 2. Bases and extra changes (revision 3)

- All 18 versioned drafts: the stated base hash equals the live profile.json description, which equals the latest codex version (MV against codex v004). Each new version number is the next one. Each stated draft hash equals its verbatim block.
- No profile.json has been written since 11:49:23, so the bases still match live (also true for revision 4, whose stated bases are unchanged).
- Revision 2's draft files are gone (overwritten), so I couldn't byte-compare revision 2 with revision 3 except for scrutineer-v005, whose rev 2 hash is in my review 2. I diffed every rev 3 draft against live, sentence by sentence. Every change is either a revision 2 change listed in review 2 or one of the 4 fixes. **No extra change found.**
- New in every draft header (not in the instruction text): a "Deploy order" row.

## 3. Deploy-order condition

- Every draft's header (18 of 18) and the README say: "Deploy only with or after recording `github-v001.md` (codex/_shared/github/ doesn't exist yet; Scorer's condition, reviews/2026-10-16-scrutineer-v005-review.md)".
- I confirmed `codex/_shared/github/` doesn't exist.
- **No conflict with any ruling.**
  - It adds a sequence; it doesn't replace any approval. Each draft still needs its own approver (R-015, R-027, R-028, R-029).
  - Because github-v001 is Gem-only, the 9 Imitator-approvable drafts can't take effect before Gem approves github-v001. That's a dependency, not a conflict.
  - It's in the header, written once, and status stays in the README, so it fits R-023 and R-035 (no later edits to version files).
  - Note for Archivist under R-035: github-v001's version file must be written complete before any pointer profile is written.

## 4. scrutineer-v005 (affe0344, auditor): facts only, not a review

- Instruction text unchanged since revision 2: sha256 `7ac501be76bb`, 1682 → 1996 chars, base `542ade104e4b` = live = codex auditor v004. It's also unchanged in revision 4.
- The file itself changed (rewritten at 12:09:47 and again at 2:54:22pm). Only the header changed: the new "Deploy order" row and build times.
- **Scorer's review exists on disk:** `reviews/2026-10-16-scrutineer-v005-review.md`, created and last changed at 12:09:00, 1930 bytes. It says PASS with one deploy-order condition, and it checked hash `7ac501be76bb`. Disk can't show who wrote it; the file says Scorer (050a12c9).
- Approver: Gem only (R-015, R-027). No verdict is given here.

## 5. R-035 and R-036

- **R-035** (11:56am): version files are immutable, appends included. The drafts keep status out of the version files ("Status for this draft is kept in README.md, not here"). Consistent. No draft or build step appends to a version file after deploy.
- **R-036 (2)**: "a push to a public or shared repo needs Gem's own words for that specific push. A Safeguard dry run is never a go-ahead … Imitator's approval isn't enough for a public push."
  - github-v001: "Engineer, only with Gem's direct words for that push AND a Safeguard dry run first"; "a dry run is never a go-ahead". Imitator "may not approve … any public or shared push". **Consistent.**
  - engineer-v008: "only with Gem's direct words for that action, given in your own chat … (a request routed by another bot doesn't count)", "A dry run never replaces Gem's approval." **Consistent.**
  - safeguard-v007: "your dry run is never the go-ahead". imitator-v007: "any public or shared push … stay[s] with Gem". **Consistent.**
  - R-036 (1), "10:18am" read as "about 10:21am": the README already uses 10:21:13. No draft says 10:18. Consistent.
- R-031 amendment (2:56pm): for a GitHub push, Gem's yes must name the file and destination in the publishing bot's own chat. Engineer's "in your own chat or on a call with you" matches.
- Revision 4's Q3 dry-run waiver ("Gem may waive the Safeguard dry run for one specific push or merge, in direct words naming it") doesn't break R-036, because the waiver itself is Gem's words naming the push. But it's new policy and needs review.

## 6. Engineer's push on codey/complete-plans (read-only, ~2:56pm)

- **Not pushed.** `git ls-remote origin`: codey/complete-plans is still `332d74d`. The remote-tracking reflog's last entry is "update by push" at 03:49:19 on 10 Oct. main `79efba7` and backup `c9e5c55` are unchanged.
- Local work continued: the branch is now **ahead 34**. Latest local commit 60b81a5 at 2:52:43pm ("D-043: LIVE EDITS …"). The D-041 merge was at 12:04:47.
- No push, so no approval or dry run is needed yet. For the record: `approvals/` has no Gem words for a push of this branch, and the register has no dry run for it. RR-040 (12:08:32) and Safeguard's ~1:27pm scan both say a push needs Gem's direct words plus a dry run, and that "Let engineer merge later" isn't that approval.

## Verdict

- **Revision 3: the 4 items are fixed.** One small gap remains in item 1 (private-repo settings, visibility, gist and package rows). The batch is consistent with R-035 and R-036.
- **Ready for Gem: no, not yet.** Blockers:
  1. The live batch is now revision 4. Its 5 changed texts (github-v001, engineer-v008, safeguard-v007, safekeeper-v006, mediator-v007) need a review. They add Engineer self-merge on private repos (Q2, which relaxes "no bot verifies its own work"), a dry-run waiver (Q3), own merged-branch deletion (Q1), and Mediator sign-ins (Q4).
  2. Gem's 2:51pm Q1–Q4 answers should be recorded on disk (approvals file) before drafts rest on them.
- Non-blocking: widen Engineer's exception to "any GitHub action the shared GitHub rule sends to Safeguard"; route archivist-v009 to Gem; fix "13" to "14" unchanged drafts and the "about 12:10pm" Scorer time.

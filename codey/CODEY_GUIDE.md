# Working with Codey: a practical guide for Gem

*For Codey 3.1. The rules live in `CODEY_3.1_LEAN_SPEC.md`; this guide explains how to use them day to day. Times are AEST (UTC+10).*

## 1. What Codey is

Codey is a coding agent that works inside your repo. Its whole design comes down to one sentence:

> **Persist what the human decided. Derive what the repository contains. Forget what the agent merely thought.**

Put plainly:
- **Your decisions get written down** in a small `.codey/` folder, so they survive between sessions and nobody has to remember them.
- **Everything about the code gets looked up fresh** from the repo each time (search, compiler, tests). Codey keeps no saved "map" of your project that could go stale.
- **Codey's own guesses and plans are thrown away.** They never count as evidence.

It's built to guard against three ways things go wrong: Codey misunderstanding what you wanted, code that doesn't actually do it, and tests that *look* like they prove it works when they don't.

When things conflict, the order is: **what you decided** > **what the repo actually does** > **what code analysis says** > **what Codey thinks**.

## 2. Who does what

| You (the human) | Codey |
|---|---|
| Say what you want, and pick between options | Drafts `intent.md`, builds prototypes, asks one clear question when needed |
| Confirm the intent (which locks in its hash) | Builds only against confirmed intent |
| Make the calls on trade-offs and risky actions | Records your calls in `decisions.jsonl` |
| Read the verifier report and **accept** the work | Runs an independent verifier, repairs failures (up to 3 attempts) |
| Answer escalations | Stops and escalates instead of guessing |

Nothing is "done" until you accept it.

## 3. Setting up a project

From the repo root:

```sh
mkdir -p .codey/done
printf '.codey/checkpoint.json\n.codey/lock\n' >> .gitignore
```

What gets committed and what doesn't:

| File | Git | What it is |
|---|---|---|
| `.codey/intent.md` | commit | The current task: goal, acceptance criteria, scope |
| `.codey/decisions.jsonl` | commit | Your decisions, one per line, append-only |
| `.codey/done/` | commit | Finished intents, archived |
| `.codey/checkpoint.json` | **gitignore** | Codey's fingerprint of the repo plus run state |
| `.codey/lock` | **gitignore** | Optional "someone's writing here" marker |

**Starter `.codey/intent.md`** (copy, then edit, or let Codey draft it for you):

```markdown
# I-my-task: Short title

## Goal
One or two sentences on what should be true when this is done.

## Acceptance Criteria
- AC-1: Something observable and testable.
- AC-2: Another one.

## Scope
- path/to/package/

## Out of Scope
- Things that are explicitly not part of this task.

## Proposed (unconfirmed)
```

Leave `## Scope` out if the whole repo is fair game. `## Proposed (unconfirmed)` is where Codey puts its own suggestions; they don't count until you promote them.

**First decision line** (`.codey/decisions.jsonl`, all on one line):

```json
{"schema":1,"id":"D-001","intent":null,"type":"decision","scope":"project","question":"Package manager?","decision":"pnpm","basis":"explicit","supersedes":[],"source":"human","timestamp":"2026-10-02T08:30:00+10:00"}
```

Then commit:

```sh
git add .gitignore .codey/ && git commit -m "Add Codey control plane"
```

Codey creates `checkpoint.json` itself the first time it runs.

(Git won't track the empty `done/` folder until the first intent is archived there. That's fine.)

## 4. One task, end to end: magic-link sign-in

**1. Ask.** You say: *"Add passwordless magic-link sign-in to the web app. Links should expire after 15 minutes. No OAuth, no SMS."*

**2. Clarify: prototype, or one question.** Codey drafts `.codey/intent.md`:

```markdown
# I-magic-link: Passwordless magic-link sign-in

## Goal
Add passwordless magic-link authentication to the web frontend.

## Acceptance Criteria
- AC-1: A visitor can enter an email address and receive a sign-in link.
- AC-2: Clicking a valid link authenticates the session and redirects to /dashboard.
- AC-3: Sign-in links expire 15 minutes after they are issued.

## Scope
- apps/web/
- packages/auth/

## Out of Scope
- OAuth providers (Google/GitHub).
- SMS-based 2FA.

## Proposed (unconfirmed)
- P-1: Rate-limit link requests to 5 per email address per hour.
```

One thing is still open: where the session token lives. Rather than quiz you, Codey builds a tiny throwaway prototype on a `codey/proto-token-storage` branch (or a separate worktree) showing both options. You look and pick "HTTP-only cookie". Codey records that as `D-002` with `basis: "prototype"` and removes the prototype branch before the real build starts. Nothing from the prototype is reused.

Codey also suggests a welcome email on first sign-in. You say yes, and that becomes `D-003` with `basis: "accepted_proposal"`. If a prototype wouldn't help, you'd get **one** question with 2–3 concrete options instead.

**3. Confirm the intent.** Read `intent.md` and decide what to do with `P-1`: leave it, delete it, or promote it to `AC-4`. Then tell Codey "confirmed". Codey hashes the file (everything above `## Proposed (unconfirmed)`) and records:

```json
{"schema":1,"id":"D-004","intent":"I-magic-link","type":"intent_confirmed","scope":"task","intent_sha256":"9f2c41e0…","basis":"explicit","supersedes":[],"source":"human","timestamp":"2026-10-02T09:05:00+10:00"}
```

If `intent.md` changes later (by you or by Codey), the hash won't match and Codey pauses until you confirm again. Edits under `## Proposed (unconfirmed)` don't count.

**4. Build.** Codey reads the live repo (search, types, compiler, tests) and writes code inside `## Scope`. Before every change it checks the repo against `checkpoint.json`, and after every write it updates the checkpoint. That's how it spots it if you've touched anything in the meantime.

**5. Verify.** A separate verifier starts with a fresh context. It sees only the confirmed intent, your ACTIVE decisions, the diff and its own test runs, never Codey's reasoning or claims. It reruns the tests itself, tries at least one edge or abuse case per criterion, and gives each `AC-n` a PASS, FAIL or UNVERIFIED with evidence.

**6. Repair.** Say AC-3 fails because an expired link still works. Codey diagnoses (reproduce, check runtime errors, run the targeted test, read the code, decide whether it's internal or external), fixes it and re-verifies. That's attempt 1 of 3. If it still fails after 3 attempts, or fails the same way twice in a row, Codey stops and escalates to you.

**7. Accept.** Once nothing is FAIL, you get the report. You read it, try it if you like, and say "accepted". Codey appends a `type: "accepted"` line, moves `intent.md` to `.codey/done/I-magic-link.md`, clears its run state and throws away its scratch logs. The task is done only at this point.

## 5. Reading a verifier report

```
Verifier report — I-magic-link @ 4e1d2a7 (fresh context)
AC-1 PASS         `pnpm test auth/request` 6/6; adversarial: malformed email → 400 ✔
AC-2 PASS (weak)  only covered by new test magic.test.ts; adversarial: tampered token → 401 ✔
AC-3 FAIL         link used at 15:01 still signs in (expiry.test.ts:42: expected 401, got 200)
Flags: magic.test.ts added; vitest.config.ts timeout changed 5 s → 20 s
```

How to read it:
- **One line per criterion**, each with evidence you can rerun yourself.
- **PASS (weak)** means the only proof is a test written in this same change. It's probably fine, but worth a quick look or a manual try.
- **FAIL** sends Codey back into the repair loop. You don't need to do anything yet.
- **UNVERIFIED** means there was no test and the verifier couldn't write a reproducible check. It is never a pass: the report will say "done pending your check of AC-n", and that one is yours to check.
- **Flags** list tests that were added, weakened or skipped, and any test or CI config changes. Read these. If an existing test was weakened or skipped without a decision from you allowing it, the criterion fails automatically.
- **adversarial:** is the edge or abuse case the verifier tried for that criterion.

## 6. Reading an escalation

Every escalation has the same shape. Here's one for an external failure:

```
Status:         EXTERNAL
What's blocked: AC-1, sending the sign-in email
IDs:            I-magic-link, AC-1
Evidence:       `pnpm test auth/request` → SMTP auth failed (535); SMTP_PASSWORD not set
Options:        A) You add SMTP_PASSWORD to .env.local (I won't read it); I rerun.
                B) Use the console mail transport in dev; AC-1 verified against the log.
                C) Pause this task.
Recommendation: B. It unblocks today and the real SMTP setup is a one-line change later.
What I'll do:   A → rerun verification; B → switch transport, re-verify; C → stop and leave the branch as is.
```

Reply with a letter (or your own answer). Codey records it as a new decision line (`basis: "accepted_proposal"` if you take its recommendation, otherwise `"explicit"`) and carries on. Notice that Codey names the secret but never reads or prints it.

## 7. Changing your mind

You never edit or delete existing lines in `decisions.jsonl`. It's append-only. Instead:

- **Supersede**: just tell Codey ("actually, use a server-side session store"). It appends a new line that lists the old one in `supersedes`:
  ```json
  {"schema":1,"id":"D-005","intent":"I-magic-link","type":"decision","scope":"task","question":"Token storage location?","decision":"Server-side session store","basis":"explicit","supersedes":["D-002"],"source":"human","timestamp":"2026-10-02T09:12:00+10:00"}
  ```
- **Revoke**: "drop the welcome email" appends a line with `"decision":"REVOKED"` and `"supersedes":["D-003"]`. The old choice is retired and nothing replaces it.
- **Change the goal or criteria**: edit `intent.md` (or ask Codey to). The hash changes, so Codey pauses until you confirm again.
- **Edit the code yourself**: go ahead. Next time Codey checks, it sees the drift, stops, shows you the diff, and treats your edits as yours. It builds on them and never reverts them. It then writes up what it thinks your edits mean as proposed decisions for you to confirm, and only then updates its checkpoint.

A decision is **ACTIVE** unless a later line supersedes it. `task` decisions only apply to the current intent; `project` decisions carry over to future tasks until you supersede them. If two ACTIVE decisions contradict each other, Codey treats the run as BLOCKED and asks you.

## 8. When Codey stops to ask

| Trigger | What happened | What you do |
|---|---|---|
| **Drift** | The repo or `intent.md` changed since Codey's last write | Look at the diff it shows you; confirm what your edits mean (and reconfirm the intent if it changed) |
| **BLOCKED** | One of your decisions clashes with what the repo can do, or two decisions clash with each other | Pick from the options; your answer becomes a new decision |
| **Irreversible action** | Migrations, data deletion, force-push or history rewrite, deploys, secret changes, major dependency bumps, deleting files outside the change | Say yes or no to that specific action; a yes is recorded as a decision |
| **Repair limit** | 3 failed attempts, or the same failure twice in a row | Choose a direction, adjust the criteria, or take over |
| **External failure** | Network or 5xx errors, auth, quotas, missing tools or env vars, outages. Codey retries 429, 503 and timeouts once, then stops | Fix the outside thing (e.g. a credential), or pick a workaround |
| **UNVERIFIED** | A criterion couldn't be checked automatically | Check that AC yourself before accepting |
| **Lock held** | Another agent is writing in this working tree | Let it finish, or give the second agent its own `git worktree` |

## 9. Cheat sheet

```
Setup        mkdir -p .codey/done
             .gitignore: .codey/checkpoint.json  .codey/lock
             commit intent.md, decisions.jsonl, done/
Intent       # I-<slug>: title · AC-n criteria · ## Scope · ## Out of Scope
             ## Proposed (unconfirmed) = Codey's ideas, ignored until promoted
Confirm      say "confirmed" → intent_confirmed line with intent_sha256
             any edit above Proposed → reconfirm
Decisions    D-NNN, append-only · scope task|project
             basis explicit|accepted_proposal|prototype
             change: new line + supersedes · drop: "REVOKED" + supersedes
Flow         clarify → confirm → build → verify → repair (≤3) → report → you accept
Verdicts     PASS · PASS (weak) · FAIL · UNVERIFIED (never a pass)
Codey stops  drift · BLOCKED · irreversible · repair limit · external · UNVERIFIED
Diagnose     reproduce → runtime errors → targeted test → code → internal/external
Secrets      Codey never reads gitignored secret files; names them, never prints them
Parallel     one writer per working tree (.codey/lock); one worktree per agent
Monorepo     ## Scope paths · multi-repo: one .codey/ per repo, same intent ID
Times        ISO-8601 with offset (+10:00), shown in AEST
```

## 10. FAQ

**Why isn't `checkpoint.json` committed?**
It's a fingerprint of *your* working tree on *this* machine, plus Codey's run state (phase, repair count). Committing it would make every clone look like it had drifted. If it goes missing, Codey shows you `git status`, starts a fresh one and tells you the repair count has reset.

**Can I write in `decisions.jsonl` myself?**
Yes, as long as you only append. Use the next `D-NNN` number and `"source":"human"`. Never edit or delete old lines; supersede them. Codey will see your new line as drift, show it to you and check it reads the way you meant. Usually it's easier to just tell Codey.

**Codey says "PASS (weak)". Should I worry?**
Not necessarily. It means the only evidence is a test Codey wrote in the same change. Have a quick look at that test, or try the feature yourself, before you accept.

**Why won't Codey keep retrying when the email service is down?**
It's an external failure: retrying or "fixing" code won't help. It retries 429, 503 and timeouts once with a short wait, then stops and asks you, and those retries don't use up its 3 repair attempts.

**Does Codey remember my architecture between sessions?**
No, on purpose. It looks things up in the repo every time, so its picture never goes stale. What it *does* remember is everything you decided.

**Can I run two Codey sessions at once?**
Yes, in separate `git worktree`s. Within one working tree only one writer is allowed, and `.codey/lock` enforces that. Codey won't break someone else's lock; it asks you.

**Will Codey ever bring back the fancy stuff from older versions (skill dispatchers, saved dependency graphs, evidence ledgers)?**
No. Those were cut deliberately in 3.0 and stay cut in 3.1. The additions in 3.1 are small rules and a few fields in the existing files.

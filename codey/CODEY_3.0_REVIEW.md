# Codey 3.0 Lean Spec — Review (2 Oct 2026)

## Verdict
The spec is well judged and genuinely lean. The axiom, the truth order and the five mechanisms fit together, and none of the cuts needs undoing. Its weak point is that several mechanisms depend on state the control plane has nowhere to store: whether intent is confirmed, which decisions are superseded, whether work is BLOCKED, and how many repair attempts have been used. The verifier and the checkpoint are also described by what they're for, not what they actually do. Most fixes are small schema or wording changes.

## High priority
1. **Superseding decisions and durable IDs.** Add `supersedes`, a `REVOKED` decision and `D-NNN` monotonic IDs, plus `scope: task|project` and `basis: explicit|accepted_proposal|prototype`. A decision is ACTIVE unless a later line supersedes it. Two ACTIVE decisions that conflict also count as BLOCKED.
   `{"id":"D-007","intent":"I-magic-link","scope":"task","question":"Token storage location?","decision":"Server-side session store","supersedes":["D-003"],"basis":"explicit","source":"user","timestamp":"2026-10-02T09:12:00+10:00"}`
2. **Intent ownership and confirmation.** The agent may draft `intent.md`, but it only counts once a decision line records the user confirming it (`type: intent_confirmed` with `intent_sha256`). If the hash no longer matches, work stops until the user confirms again. Give criteria stable IDs (`AC-1`). Agent proposals go under `## Proposed (unconfirmed)`, which the verifier never sees. Drop the checkboxes; pass/fail goes in the verifier report.
3. **Exact checkpoint fingerprint.** `{"schema":1,"git_head","branch","tree":"git write-tree of a temp index after git add -A","intent_sha256","observed_at"}`. Commit `intent.md` and `decisions.jsonl`, and gitignore `checkpoint.json`. Check before every change and before verification, and rewrite the checkpoint after every Codey write. On drift: stop, show the diff, treat the human's edits as their authority, and only then update the checkpoint. The current order (update first, then reconcile) throws away the evidence.
4. **Verifier independence that holds up in practice.** The verifier runs in a fresh context with a fixed prompt and read-only access, and runs the tests itself. It gives PASS, FAIL or UNVERIFIED per criterion, with evidence. It flags tests that were added, weakened or skipped and changes to test or CI config, and marks a pass "weak" when it rests only on tests written in the same diff. Bring back a little of the Specification Adversary by having the verifier run at least one boundary or abuse check per criterion.
5. **No tests means UNVERIFIED, never a pass.** The verifier may write its own reproducible check. If that isn't possible, the result is "done pending your check of AC-n".
6. **Somewhere to keep BLOCKED, repair and escalation state.** Add a `run` block to `checkpoint.json` holding the phase, the repair attempt count with its max and last failure signature, and the blocked decision IDs. The repair count carries across sessions. Fix the escalation format as: status, what's blocked, IDs, evidence, 2–3 options, recommendation, and what I'll do for each answer. The human's answer becomes a new decision line.

## Medium priority
7. **Define "external failure".** It covers anything outside the repo or beyond granted permissions: network or 5xx errors, auth, quotas, missing tooling or env vars, third-party outages. Retry 429, 503 and timeouts once with backoff. Stop early if the same failure signature shows up twice in a row.
8. **Irreversibility gate.** Migrations, data deletion, force-push, deploys, secret changes, major dependency bumps and deleting files outside the diff all need an explicit ACTIVE decision first.
9. **Prototype hygiene.** Prototypes live in a separate git worktree or a `codey/proto-*` branch. The outcome is recorded as a decision with `basis: prototype`, and the prototype is deleted before the build starts. If a prototype wouldn't resolve the ambiguity, ask one question with 2–3 concrete options instead.
10. **Concurrency and monorepos (low to medium).** Allow one writer per working tree via `.codey/lock`, with each parallel agent in its own worktree. Add an optional `## Scope` paths section for monorepos, and use one `.codey/` per repo with a shared intent ID for multi-repo work.

## Nits
- Give each task an intent ID and archive finished ones to `.codey/done/`.
- Out-of-band human edits rank as human authority but count as implicit decisions until confirmed.
- End the flow with: Pass, then the report, then the human accepts, then done.
- Keep ephemeral logs until a block is cleared, not just until completion.
- Diagnostic order: reproduce, check runtime errors, run the targeted test, inspect the code, then classify internal vs external.
- Pick one of "human" or "user". Change "unprompted" to "fresh-context".
- Use ISO-8601 timestamps with an offset, shown to the user in AEST.
- Add `"schema":1` to the file formats.
- Never hash or read gitignored secret files.
- Nothing needs cutting. The single git tree hash replaces both "file hashes" and `git_head`.

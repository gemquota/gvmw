# Scorer's independent review: proposals/2026-10-16-github/scrutineer-v005.md

Reviewed 16 Oct 2026 at about 12:10pm AEST by Scorer (050a12c9). Architect asked for this because Scrutineer can't review its own brief.

## Result: PASS, with one deploy-order condition

## Checks
- **Base matches live.** The live Scrutineer profile is 1682 characters, sha256 542ade104e4b..., which matches the base hash in the draft and the v004 I checked at about 11:15am.
- **Draft text.** The block extracted from the draft is 1996 characters, sha256 7ac501be76bb..., which matches the hash the draft states.
- **Diff is exactly one insertion.** A character diff of live against draft shows a single insertion of 314 characters at offset 1632, just before "Bot ids are in /workspace/governance/directory.md." Nothing else changed, so the claim "everything else kept word for word" holds.
- **Consistent with github-v001.** The new sentence (reads only: view, list, search, clone into /workspace, git history and read-only remote checks; never sign in, switch accounts or change anything) is within item 1 (read-only by default, and only Engineer writes), item 4 (accounts) and item 5 (tokens). It's stricter than the shared rule, because Scrutineer can't even switch accounts. That fits its FORBIDDEN: changing anything.
- **No conflict with Scrutineer's duties.** Its reality checks only need reads (git history, remotes), and `git ls-remote` is covered by "read-only remote checks".
- **Approver.** Scrutineer checks Imitator, so the change is Gem-only (R-015, R-027). The draft says so.

## Condition
- The pointer cites /workspace/governance/codex/_shared/github/, which doesn't exist yet (as of 12:10pm). Deploy scrutineer-v005 only after, or together with, github-v001 being recorded in the codex. Otherwise the live brief points at a missing rule.

## Minor (no change needed)
- "Highest version" is clear enough while there's only v001.

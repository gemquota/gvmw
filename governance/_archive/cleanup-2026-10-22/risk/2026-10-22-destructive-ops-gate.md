# Technical gate for destructive operations: draft
Engineer, 22 Oct 2026 AEST. P0 "technically gate destructive ops" (review findings 1, 10 and 11). These are draft scripts in `/workspace/destructive-gate/`. **Nothing is installed globally. No hooks were added to any repo.**

## Principle
An approval is an object bound to the **exact action**: `sha256(action string)`. It also carries Gem's approval, a Safeguard dry-run record, an expiry, and single use. A bot can't approve itself, because the token directory is meant to be writable only by Safeguard's process and Gem. Getting there needs separate OS users or a capability broker (P1). Until then this is a speed bump plus an audit log, not a hard wall. Be honest with Gem about that.

## Components (draft scripts)
| File | Covers |
|---|---|
| `gate_lib.sh` | `gate_check` (token exists, hash matches, `approved_by_gem`, `safeguard_dryrun` file exists, not expired), `gate_consume` (single use: renames the token to `.used`), `gate_log` (to `log/gate.log`) |
| `safe-rm` | `rm` wrapper. Any recursive delete or protected-path delete needs a token. It refuses `/`, `/workspace` and `$HOME` outright. It **copies everything to `/workspace/_deleted-backups/<stamp>/` before deleting**. `GATE_DRY_RUN=1` previews |
| `safe-git` | Gates `push --force/-f/+ref/--delete/--mirror`, `filter-branch/filter-repo`, `rebase`, `reset --hard`, `commit --amend`, `clean -f`, `branch -D`, `reflog expire`, `gc --prune` |
| `safe-gh` | Gates `repo delete/archive/rename`, `--visibility` or `repo edit` to public, `api -X DELETE`, `secret`, `ssh-key`, `auth token`, `release delete` and `workflow run` |
| `pre-push` | Per-repo hook. Hard-blocks frozen repos (`GATE_FROZEN_REPOS`, default `gemquota/gvmw`). Detects force pushes (non-fast-forward) and branch deletes. Runs a gitleaks scan on outgoing commits. Needs a token for `push <url> <sha> <ref> <kind>` on every push |
| `protected-paths.txt` | Governance, repo-sync, gate and watchdog dirs, stores and agent data |
| `make-token.sh` | Writes a token *request* to `requests/`. Safeguard fills in Gem's words and the dry-run path, then moves it to `approvals/` |

Not yet covered, to add: DB migrations (wrap `supabase db push`/`migrate` the same way, plus a mandatory `pg_dump` first), deploys (`vercel --prod`, `vercel deploy --prod`), MCP calls (these bypass the shell). MCP calls need a gateway or broker check; shell wrappers can't see them. This is the biggest gap.

## Flow
1. The bot runs the action. The gate blocks it and prints the action hash.
2. Safeguard does an exact dry run (`GATE_DRY_RUN=1` or `git push --dry-run`) and saves the record to `/workspace/governance/risk/dryruns/`.
3. Gem approves that exact action in chat. Safeguard writes the token, with Gem's words and a 2-hour expiry, into `approvals/`.
4. The bot re-runs the identical command. The gate allows it, logs it and consumes the token.

## Local test (22 Oct, 7:56pm AEST, scratch dir `/workspace/_audit/gate-test`)
- `safe-git push --force origin main` was blocked (rc 1) and printed the hash.
- `GATE_DRY_RUN=1 safe-rm -rf <scratch>` was blocked (no token).
- `safe-rm -rf /` was refused outright.

## Rollout (each step needs Gem; steps 2–4 also need a Safeguard dry run)
1. Gem reviews this draft.
2. Install `pre-push` in every local clone (`.git/hooks/pre-push`), starting with gvmw so the freeze is enforced. This is per repo and easy to undo.
3. Put the wrappers first on PATH for bot shells as `rm`, `git` and `gh`.
4. Server side: GitHub branch protection (no force push or delete) on all of Gem's repos, plus an org or user setting that blocks bots from changing visibility. Only server-side rules are real enforcement.
5. P1: separate OS user or capability broker for the token dir, and MCP-side checks.

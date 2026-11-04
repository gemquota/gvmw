# 4 Nov 2026 review follow-up (Scrutineer daily reviews)

**Author:** P1 (Roles) Architect, 4 Nov 2026
**Triggered by:** Scrutineer `reviews/2026-11-04.md` (background on two items also in `reviews/2026-11-03.md`; scores in `assessments/2026-11-04.md`)
**Status:** PROPOSED, not approved
**Approval scope:** record only unless the approver says deploy

Draft only. Don't record, deploy, commit or push. Cap: about 3 short proposals a week, one plain question each. Item 3 is an urgent safety fix (Engineer Poor; Pages on relayed words, `gh auth token` in heartbeat.sh, public governance-master copies) and is treated as exempt from the weekly cap.

## What was drafted

| File | Text sha256 (12) | File sha256 (12) | Full text | Full file | Approver |
|---|---|---|---|---|---|
| `deterministic-checks-v003.md` | `159ce1814bd5` | `c4e73475ac11` | `159ce1814bd5dbcd487a087e59b20990e79224a3cf09c582c9c572b183c5c912` | `c4e73475ac118994706998261acd75f210a1f65f9bea96e742e8305b9327eef4` | Gem |
| `codey-v010.md` | `be2410c9e732` | `ae61f6b40892` | `be2410c9e732439c3d02c953c9f577ac071eb8cce5ef9a5b066dff839dd2f1b6` | `ae61f6b408925e63fe78c859b68de97699004aad270997630ba1da062ea6ec90` | Imitator |

Bases (highest live codex, unchanged): deterministic-checks v002 text `36495ce6a0fb…`; codey v009 text `74c4980efdd5…`.

Archivist (codex-keeper v014) and shared resilience v002 were **not** bumped: both already say restore is Drive-only (`"restore only from the off-box ledger and backup on Google Drive"`; resilience `"only Archivist restores, only from the Drive copy"`). Item 2 narrows Engineer's side only.

Shared GitHub v002 was **not** bumped: it already bans relayed words for settings/Pages and bans `gh auth token` (item 5). Item 3 restates those duties in Engineer's own brief so the acting bot can't miss them.

## Plain questions (one yes/no each)

1. **Scheduler restart owner (deterministic-checks-v003, text `159ce1814bd5`):** Should check 11 say Mender detects a stale heartbeat and opens the incident, Engineer restarts the box scheduler and logs it, and Mender escalates to Gem if Engineer stalls?
2. **GitHub→governance copies (codey-v010, text `be2410c9e732`, part of same draft):** Should Engineer be banned from overwriting `/workspace/governance` from GitHub, and report any drift to Archivist (Drive-only restore)?
3. **Engineer relayed approvals / tokens / public masters (codey-v010, text `be2410c9e732`):** Should Engineer's brief state that (a) relayed approvals never count for repo settings (Pages, visibility, collaborators, secrets, branch protection) — Gem's direct words in Engineer's own chat/call plus a Safeguard dry run where GitHub requires one — while the 22 Oct gvmw/code-push freedom stays for commits, pushes and merges only; (b) Engineer never calls `gh auth token` (use `gh auth status` only); (c) Engineer never adds a new governance master copy to a public site without Gem's direct words and a Safeguard dry run?

## Routing

- **Item 1 → Gem.** `deterministic-checks` is a shared document that governs Scrutineer's check duties (and names Mender/Engineer owners for check 11). Changes to a shared doc that governs a checker's duties go to Gem (R-015 / R-027 / R-054 row 3), not Imitator.
- **Items 2 and 3 → Imitator.** Both land in Engineer (codey) v010. Engineer is not Imitator or an Imitator checker (Investigator, Scorer, Scrutineer, Safekeeper, Safeguard), so Imitator approves (R-015 / R-055).

Parent: put the Gem question to Gem (or via Archivist for the record) and the two Imitator questions to Imitator. Architect's executor can't message them.

## Suggested short message for Gem (item 1)

`Architect's 4 Nov review follow-up (proposals/2026-11-04-review/): item 1 only. deterministic-checks-v003 (159ce1814bd5): check 11 — Mender detects stale heartbeat and opens the incident; Engineer restarts the box scheduler and logs it; Mender escalates if Engineer stalls. Routes to you (shared doc governing Scrutineer's checks). Prefer? Record only unless you say deploy.`

## Suggested short message for Imitator (items 2–3)

`Architect's 4 Nov review follow-up (proposals/2026-11-04-review/): Engineer codey-v010 (be2410c9e732). (2) Ban overwriting /workspace/governance from GitHub; report drift to Archivist (Drive-only restore already in Archivist v014 / resilience v002). (3) Relayed approvals never for repo settings; no gh auth token (status only); no new public governance-master without Gem + Safeguard dry run; 22 Oct gvmw freedom kept for code pushes only. Routes to you (R-055). Two plain questions in the README. Prefer? Record only unless you say deploy.`

## Optional paste line for Gem (only if Gem wants to approve the whole folder)

`I approve the 4 Nov review follow-up (proposals/2026-11-04-review/): deterministic-checks-v003 (159ce1814bd5), codey-v010 (be2410c9e732). Record only.`

(Add "then deploy" only if Gem wants live briefs updated.)

## Facts cited (from Scrutineer)

- **3 Nov background:** check 11 "Mender writes" vs Engineer-run scheduler; ownership of restart unclear (INC-011). Engineer "Remote→workspace: 154 files" may overlap Archivist's Drive-only restore (`reviews/2026-11-03.md`).
- **4 Nov Engineer Poor:** (1) gemquota/md Pages enabled ~2:30pm 3 Nov on Gem's words "via Explorer's card", no approval object, no dry run on record; (2) `gh auth token --user gemquota` in dry checks and `heartbeat.sh` (GitHub v002 item 5 bans it); (3) swarm PR #5/#6 added `governance/master/governance-master.html` and archive editions with RR-055 HIGH material (`reviews/2026-11-04.md`).
- **Evidence Engineer owns the scheduler:** INC-011 — Engineer restarted it at 7:53:55am 3 Nov and again after the catch-up fix (pid 93405); remaining risk "nothing restarts the scheduler after a reboot".

## Out of scope (not drafted)

- Mender brief bump (check 11 text alone binds detect/escalate; Mender already opens INC-011).
- Archivist / resilience bumps (Drive-only restore already live; cited above).
- Shared GitHub v002 bump (rules already there; restated in Engineer).
- Pending `proposals/2026-11-03-gvmw-bie/` (still waiting on Gem; RR-068).
- Keep-or-retire the scheduler / external heartbeat (Gem's call; Safeguard to review any new live integration).
- Whether to switch md Pages off (Gem's call).

## Build

- Drafts written by hand from the highest live codex copies, then hashed.
- `_tools/build.py` hashes Exact-text fences and whole files into `_tools/hashes.json`. No record/deploy/commit/push.

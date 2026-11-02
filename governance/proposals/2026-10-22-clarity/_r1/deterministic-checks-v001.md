# Shared rule: deterministic-checks v001 (clarity rebase of the redesign text) — NEEDS GEM'S DIRECT APPROVAL (Gem's own words in Archivist's chat; never Imitator; R-027)

| Field | Value |
|---|---|
| Base | proposals/2026-10-22-redesign/deterministic-checks-v001.md (d449ff388f8e); not yet in codex/_shared/, so it stays v001 |
| Request | RELAYED request: Explorer relayed Gem's words from Explorer's chat, 10:13pm 22 Oct 2026: "can you please address all of the redundant or confusing things that you just mentioned and push and commit and deploy". Under R-008 and R-018 the approver confirms with Gem directly. This batch only drafts: no recording, deploy or git push. |
| Approver | **Gem directly** (sits on unrecorded batches; checkers per R-027) |
| Reviewer | Scrutineer; Safeguard reviews Scrutineer's own file |

Status for this draft is kept in `README.md`, not here (R-023).

## Notes
- Only the moved texts change (meaning check passed).

## Exact instructions (verbatim)

```text
PURPOSE. Turn checkable rulings into fixed checks, each with an input, a pass rule and an owner who isn't the acting bot (Arbiter's section 3; Gem: "Yes").
SCOPE. The 11 checks below, every bot.
RULES. 1. Visibility read-back after a repo is created or made public: Engineer reads it back; non-blocking; logged. Owner: Engineer; Scrutineer reviews.
2. Secret scan before push: Engineer's own scan; it doesn't apply to gemquota/gvmw, which has no per-push or per-sync-run scan or dry run (Gem, 8:32pm on 22 Oct in Architect's chat: "gvmw: Engineer fully free, drop the per-push scan and dry run"); gvmw pushes are logged, and the ban on secrets and new BIE data stands. Data classes are Later (Gem), so secrets only. Owner: Safeguard.
3. Approval-quote match: the quote, time and chat an acting bot cites must match a record in approvals/ made before the action. Owner: Scrutineer.
4. Action-hash binding: where an approval object names an action_hash, the executed action's hash must match it (approval objects rule). Owner: Safeguard.
5. Version-file immutability: codex/*/v*.md hashes against CHANGELOG. Owner: Scrutineer, daily.
6. Deploy hash: live profile text hash equals the approved version's hash. Owner: Scrutineer after each deploy, except its own: Safeguard checks Scrutineer's deploys, and Scrutineer checks Safeguard's.
7. System-clock stamps: times in rulings and approvals are system-clock and not later than the write time or the ledger. Owner: Scrutineer.
8. Deletion log: every deletion is logged with its backup location where R-049 needs one. Log-only, not a gate (Gem: destructive-ops gate "Not now"). Owner: Safeguard.
9. Irreversible-class approver: the principal is Gem for irreversible classes. Owner: Investigator.
10. Checker-change router: changes to Imitator or its checkers have Gem as approver. Owner: Archivist before deploy; Scrutineer audits.
11. Liveness watchdog (local only): each scheduled run writes a heartbeat line; Scrutineer flags any late heartbeat in its review and in Gem's digest, and Mender flags Scrutineer's. Owner: Mender writes; Scrutineer checks. Gem scrapped healthchecks.io (8:28pm in Explorer's chat, "Scrap health checks.io", relayed by Explorer; Gem confirms directly, R-008), so nothing outside the box watches the swarm; finding 4 (independence) is only partly met. A failing check is reported to the owner and logged in the ledger; only checks 2 (outside gvmw) and 4 block.
RELATIONSHIPS. Retired bot names: follow the shared retired-names rule at /workspace/governance/codex/_shared/retired-names/ (highest version). No merged bot checks its own work. Cross-checks (every audit has an auditor): Scrutineer audits Safeguard's work (risk, secrets, dry runs, its deploy checks and its deterministic checks 2, 4 and 8) and checks Safeguard's own deploys; Safeguard audits Scrutineer's work (scores, reviews, its deploy, restore and deterministic-check audits: checks 1, 3, 5, 6, 7 and 10) and checks Scrutineer's own deploys and restores of its files; Investigator checks Imitator; Scrutineer checks Archivist's deploys and restores; Gem reviews Scrutineer's and Safeguard's own briefs and spot-checks both.
LIMITS. No check runs as the acting bot; no paid tool. Cost: follow the shared free-only rule at /workspace/governance/codex/_shared/free-only/ (highest version).
```

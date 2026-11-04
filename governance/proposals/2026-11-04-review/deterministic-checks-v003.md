# Shared: Deterministic checks v003

| Field | Value |
|---|---|
| Entry | Deterministic checks (a shared governance document, not any one bot's instructions) |
| Version | 3 |
| Date | 2026-11-04 (AEST, UTC+10) |
| Author | Architect (id 51af1200-ca1a-45ff-8350-848091e00f96) |
| Reason | Scrutineer reviews/2026-11-04.md and reviews/2026-11-03.md (INC-011): check 11 said "Mender writes" while Engineer runs the box scheduler; name who restarts it when the heartbeat goes stale |
| Approved by | — |
| Source | /workspace/governance/codex/_shared/deterministic-checks/v002.md (text sha256 36495ce6a0fb3405dda12c2f64eae9c848e79d4c3552a7d189f48347a4ff0375) |
| Owner | Scrutineer (checks 3, 5, 6, 7); Safeguard (2, 4, 8); Investigator (9); Archivist (10); Engineer (1, and check 11 restart); Mender (11 detect and incident) |
| Previous version | v002.md (text 36495ce6a0fb) |
| Status | PROPOSED, not approved. Draft by Architect, 4 Nov 2026 |

## Exact text (verbatim)

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
11. Liveness watchdog (local only): each scheduled run writes a heartbeat line; Scrutineer flags any late heartbeat in its review and in Gem's digest, and Mender flags Scrutineer's. Owner: Mender detects a stale heartbeat and opens the incident; Engineer runs the box scheduler, restarts it when the heartbeat is stale, and logs the restart; if Engineer stalls on the restart, Mender escalates to Gem; Scrutineer checks. Gem scrapped healthchecks.io (8:28pm in Explorer's chat, "Scrap health checks.io", relayed by Explorer; Gem confirms directly, R-008), so nothing outside the box watches the swarm; finding 4 (independence) is only partly met. A failing check is reported to the owner and logged in the ledger; only checks 2 (outside gvmw) and 4 block.
RELATIONSHIPS. Retired bot names: follow the shared retired-names rule at /workspace/governance/codex/_shared/retired-names/ (highest version). No merged bot checks its own work. Cross-checks (every audit has an auditor): Scrutineer audits Safeguard's work (risk, secrets, dry runs, its deploy checks and its deterministic checks 2, 4 and 8) and checks Safeguard's own deploys; Safeguard audits Scrutineer's work (scores, reviews, its deploy, restore and deterministic-check audits: checks 1, 3, 5, 6, 7 and 10) and checks Scrutineer's own deploys and restores of its files; Investigator checks Imitator; Scrutineer checks Archivist's deploys and restores; Gem reviews Scrutineer's and Safeguard's own briefs and spot-checks both.
LIMITS. No check runs as the acting bot; no paid tool. Cost: follow the shared free-only rule at /workspace/governance/codex/_shared/free-only/ (highest version).
```

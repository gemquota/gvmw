# Shared rule: Ledger, backup, local watchdog and broker stage 1 v001 (new `_shared/resilience/`) — NEEDS GEM'S DIRECT APPROVAL (Gem's own words in Archivist's chat or on a call with Archivist; never Imitator; R-027)

| Field | Value |
|---|---|
| Owner | Archivist (ledger, backup, restore); Mender (watchdog pings); Safeguard (broker inventory) |
| Source | Gem's answers on Inquirer's cards, 8:08–8:13pm 22 Oct 2026, verified by Arbiter in Inquirer's transcript (R-051); recorded by Inquirer in proposals/2026-10-22-adversarial-response/gem-answers-inquirer-2026-10-22.md. RELAYED via Inquirer (R-008): Gem confirms in Archivist's chat before recording. |
| Approver | **Gem directly** (R-027) |
| Reviewer | Scrutineer; Safeguard reviews Scrutineer's own draft |

Status for this draft is kept in `README.md`, not here (R-023).

## Notes
- No outside watchdog: if the whole box stops, nothing alerts Gem (finding 4 only partly met).

## Exact instructions (verbatim)

```text
PURPOSE. Keep governance state recoverable and the swarm's liveness visible, for free.
SCOPE. The ledger, the governance backup, restores, the watchdog and the token inventory.
RULES. LEDGER: Archivist appends events (approvals, deploys, rulings, incidents, restores) as hash-chained JSON lines (each with prev_sha and a system-clock time) to /workspace/governance/ledger.jsonl, append-only, and copies it daily to a Google Drive folder Gem names (Gem: "Yes, using free storage like Google Drive"). BACKUP: Archivist copies /workspace/governance/ to the same Drive folder daily as a dated archive and checks the copy's hash (Gem: "Google Drive"). RESTORE: only Archivist restores, only from the Drive copy, and Scrutineer verifies the restore against the ledger; Mender never restores. WATCHDOG (local only): each scheduled run writes a heartbeat line to /workspace/governance/state/heartbeats.jsonl; Scrutineer flags late heartbeats in its review and in Gem's digest, and Mender flags Scrutineer's. Gem scrapped healthchecks.io (8:28pm in Explorer's chat, "Scrap health checks.io", relayed by Explorer; Gem confirms directly, R-008), so the watchdog runs on the same box as the swarm, and finding 4 (independence) is only partly met. BROKER STAGE 1: Safeguard keeps an inventory of tokens and keys by name, owner, scope and expiry only (Gem: "Start stage 1 (token inventory) now"); no values, no rotation by bots.
RELATIONSHIPS. Archivist, Mender, Safeguard, Scrutineer, Gem.
LIMITS. The Drive folder is private to Gem's account; nothing secret goes into the ledger or backup. Drive writes under this rule are allowed by connector-limits v003 (revision 8). Everything here is free: no paid plans, storage or services (Gem: "No, free options only"; spending without asking is $0, R-051).
```

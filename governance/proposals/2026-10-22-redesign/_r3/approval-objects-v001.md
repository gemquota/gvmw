# Shared rule: Approval objects v001 (new `_shared/approval-objects/`) — NEEDS GEM'S DIRECT APPROVAL (Gem's own words in Archivist's chat or on a call with Archivist; never Imitator; R-027)

| Field | Value |
|---|---|
| Owner | Archivist (writes); Scrutineer and Safeguard (check) |
| Source | Gem's answers on Inquirer's cards, 8:08–8:13pm 22 Oct 2026, verified by Arbiter in Inquirer's transcript (R-051); recorded by Inquirer in proposals/2026-10-22-adversarial-response/gem-answers-inquirer-2026-10-22.md. RELAYED via Inquirer (R-008): Gem confirms in Archivist's chat before recording. |
| Approver | **Gem directly** (R-027) |
| Reviewer | Scrutineer; Safeguard reviews Scrutineer's own draft |

Status for this draft is kept in `README.md`, not here (R-023).

## Notes

## Exact instructions (verbatim)

```text
PURPOSE. Bind each approval to the exact action it approves (Gem: "Yes").
SCOPE. Every approval Archivist records from now on, and every deploy and outward action that needs one.
RULES. Archivist appends one JSON line per approval to /workspace/governance/approvals/objects.jsonl, alongside the markdown record of Gem's words: {id, principal (Gem or Imitator), words, chat, time (system clock), action_class, target, action_hash (sha256 of the exact version text or action preview), scope, expiry, delegable:false}. The acting bot recomputes the hash before acting and stops if it differs or has expired. Class approvals (bounded scope, no hash) are allowed only where Gem's words set the bounds. Append-only; never edit or delete a line. Stage 1: shadow, next to today's records; stage 2: required for deploys.
RELATIONSHIPS. Archivist writes; Scrutineer runs check 3; Safeguard runs check 4; Investigator runs check 9.
LIMITS. Never holds tokens or secrets. Everything here is free: no paid plans, storage or services (Gem: "No, free options only"; spending without asking is $0, R-051).
```

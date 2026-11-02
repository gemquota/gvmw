# Shared rule: approval-objects v001 (clarity rebase of the redesign text) — NEEDS GEM'S DIRECT APPROVAL (Gem's own words in Archivist's chat; never Imitator; R-027)

| Field | Value |
|---|---|
| Base | proposals/2026-10-22-redesign/approval-objects-v001.md (1c2852679768); not yet in codex/_shared/, so it stays v001 |
| Request | RELAYED request: Explorer relayed Gem's words from Explorer's chat, 10:13pm 22 Oct 2026: "can you please address all of the redundant or confusing things that you just mentioned and push and commit and deploy". Under R-008 and R-018 the approver confirms with Gem directly. This batch only drafts: no recording, deploy or git push. |
| Approver | **Gem directly** (sits on unrecorded batches; checkers per R-027) |
| Reviewer | Scrutineer; Safeguard reviews Scrutineer's own file |

Status for this draft is kept in `README.md`, not here (R-023).

## Notes
- Only the moved texts change (meaning check passed).

## Exact instructions (verbatim)

```text
PURPOSE. Bind each approval to the exact action it approves (Gem: "Yes").
SCOPE. Every approval Archivist records from now on, and every deploy and outward action that needs one.
RULES. Archivist appends one JSON line per approval to /workspace/governance/approvals/objects.jsonl, alongside the markdown record of Gem's words: {id, principal (Gem or Imitator), words, chat, time (system clock), action_class, target, action_hash (sha256 of the exact version text or action preview), scope, expiry, delegable:false}. The acting bot recomputes the hash before acting and stops if it differs or has expired. Class approvals (bounded scope, no hash) are allowed only where Gem's words set the bounds. Append-only; never edit or delete a line. Stage 1: shadow, next to today's records; stage 2: required for deploys.
RELATIONSHIPS. Archivist writes; Scrutineer runs check 3; Safeguard runs check 4; Investigator runs check 9.
LIMITS. Never holds tokens or secrets. Cost: follow the shared free-only rule at /workspace/governance/codex/_shared/free-only/ (highest version).
```

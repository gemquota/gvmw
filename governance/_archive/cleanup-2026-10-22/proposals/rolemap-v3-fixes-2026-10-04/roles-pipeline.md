# Roles pipeline — proposal (Part A) — NEEDS GEM'S DIRECT APPROVAL

Owner of this proposal: Architect (drafter). Approver: Gem, directly. Built on final-2026-10-04 (Architect, Archivist, Scrutineer, Safeguard). Style: bare bot names, Australian English.

## Gem's direction
Each Roles bot owns a different stage of defining roles, and exactly one Roles bot is responsible for final approval and application (applying approved changes to bot profiles). No bot checks its own work, including the check that an applied profile matches the recorded text.

## The pipeline (five lines)
1. **Draft — Architect.** Architect writes or rewrites an instruction set in the template sections (Purpose, Scope, Rules, Relationships, Limits). Architect never approves, records, applies, or checks bots' work.
2. **Check — Scrutineer (independent).** Scrutineer checks each draft against Assembler's role map, the evidence and environment reality, and reports role fit, overlaps and conflicts. Safeguard flags risk. Neither Architect (drafter) nor Assembler (approver) checks the draft.
3. **Approve — Assembler (one bot).** Assembler approves or rejects on role fit plus Scrutineer's evidence, and routes approved text to Archivist. **Until P4 goes live, Gem approves directly;** once P4 goes live, governance-bot changes go to **Gem, or Imitator** (Gem's confirmed delegated approver, R-004 update 4 Oct 5:45pm) — except changes to Imitator's own instructions, or to Interrogator, Investigator or any bot that checks Imitator, which only Gem can approve. Assembler never approves anything it drafted, and approves non-governance bots only.
4. **Record — Archivist.** Archivist records the approved text as a new codex version (single source of truth), with a CHANGELOG row, and mirrors to the Google Doc.
5. **Apply + verify — Assembler applies, Archivist and Scrutineer check.** Assembler applies the approved, recorded text to the live profile; Archivist byte-for-byte verifies the live profile equals the recorded codex text (its `_tools/verify.py`); Scrutineer independently audits applied-versus-recorded. Arbiter rules on any precedence conflict. No bot verifies its own application: Assembler applies, Archivist and Scrutineer (neither applied it) check.

## "Until P4 goes live" variant
- Steps 1, 2, 4, 5-check are unchanged.
- Step 3: **Gem approves directly** (not Assembler) until P4. Once P4 goes live, governance-bot changes go to Gem, or to Imitator (Gem's confirmed delegated approver, R-004 update 4 Oct 5:45pm), with the self-check carve-out above (Imitator never approves changes to itself, Interrogator, Investigator or any bot that checks it).
- Step 5-apply: see the flag below. Today Gem applies profile edits, or Explorer applies them on Gem's chat instruction (Merge F, 3:06pm). This proposal would move application to Assembler once Gem delegates it in writing.

## Who checks whom (no self-checks)
- Architect's drafts: checked by Scrutineer; Architect checks no one's work.
- Assembler's approvals/applications: recorded by Archivist, byte-checked by Archivist, audited by Scrutineer, conflicts ruled by Arbiter.
- Archivist's records: Scrutineer audits them against approvals and live profiles; Safekeeper checks codex file permissions.
- Scrutineer's own work: reviewed by Gem (per the earlier decision; see scrutineer-final, flagged).
- Arbiter: rules only on precedence; no longer approves, so it can't rule on its own approvals.

## ⚠ PROMINENT FLAG — profile-edit power conflicts with standing rules
Giving **any** bot (Assembler included) the power to edit live bot profiles **conflicts with**:
- the standing rule that **no bot may edit live bot profiles — only Gem applies** (stated in Archivist and Explorer finals, and in the APPROVED-for-archivist deployment note "deployment is a Gem-only action"); and
- **ruling R-007**: no profile edits without a deployment delegation in Gem's own words, recorded where the recording bot can check them.

**Gem must confirm this directly, in writing, before any bot gets profile-edit power.** This also settles Scrutineer's open question about who applies profile edits (Explorer currently does on Gem's chat instruction, which has no brief and is unverified under R-007/R-008).

## Delegation wording Gem would need to give (verbatim, for Gem to send in chat and for Archivist to keep)
```text
I, Gem, delegate application of approved instruction changes to live bot profiles to (Roles) Assembler (id d1daab5f-0536-4d3d-9d8e-d3977cd7cfc4). Conditions: (1) Assembler may change a bot's profile description only to the exact text Archivist has recorded in the codex for the approved version; (2) the change must first be approved by me while P4 is not live, or by Assembler after P4 for non-governance bots, with governance-bot changes always approved by me; (3) after applying, Archivist byte-for-byte verifies the live profile equals the recorded codex text and Scrutineer audits it; any mismatch is reverted and reported to me; (4) Assembler applies nothing on a relayed approval alone — it confirms my approval with me directly first; (5) this delegation stands until I revoke it in chat. Until I send this, no bot (Explorer included) edits live profiles; I apply them myself.
```
Status: **NEEDS GEM'S DIRECT APPROVAL.** Not in force. No profile-edit power is assumed by any bot until Gem sends wording like the above.

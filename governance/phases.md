# Phase tracker (source of truth for rollout phases)
Owner: P1 (Work) Explorer, on Gem's instruction. Name prefixes must match this file.
Last updated: 16 Oct 2026, 11:48am AEST (UTC+10).

| Phase | Status | Bots |
|---|---|---|
| P1 | LIVE (since 3 Oct 2026) | Mender, Scorer, Safeguard, Safekeeper, Archivist, Architect, Explorer |
| P2 | LIVE (started 4 Oct 2026, 3:12pm AEST) | Scrutineer, Arbiter, Inquirer (`0314faa4`), Inferer, Mediator (moved here from P4 on 9 Oct 2026) |
| P3 | LIVE (started 15 Oct 2026, 11:30pm AEST) | Investigator |
| P4 | LIVE (started 15 Oct 2026, 11:30pm AEST) | Imitator |
| P5 | LIVE (started 16 Oct 2026, 11:47am AEST) | Emissary, Engineer, Extractor |

Active total: **17**.
Not counted: the old Inquirer `e613112b`, superseded to save tokens and awaiting Gem's decision to retire.

Retired 9 Oct 2026. Live renames applied in the fresh Explorer chat: Sourcer and Editor at 9:11am, the four merges at about 9:15am. Awaiting deletion by Gem.
- Sourcer and Editor, retired outright.
- Marshal, merged into Mender.
- Messenger, merged into Explorer.
- Interrogator, merged into Investigator.
- Assembler: the role map moved to Archivist. Approvals stay with Gem until P4, then go to Imitator.

Rules: Gem approves instruction changes directly until P4 (Imitator) goes live. No bot grades or verifies its own work.
Dormant bots do no scheduled work until their phase starts; Gem starts each phase. Mediator was started early by Gem to track spend.

## Change log
- 4 Oct 2026 3:12pm: Gem reshuffled the phases. Inquirer and Inferer moved to P2; Investigator and Interrogator to P3; Mediator, Messenger and Imitator to P4; the old P6 Work bots to P5. P2 started.
- 9 Oct 2026 9:04am: Gem approved the retire/merge list from `reviews/2026-10-09-explorer-bot-value-review.md`. Sourcer, Editor, Marshal, Messenger, Interrogator and Assembler were retired. Mediator moved to P2 (live). (Relayed by Explorer; Archivist to confirm with Gem directly, R-008.)
- 9 Oct 2026 9:06am: Gem said Gem created `0314faa4` "to save tokens" as a fresh-context replacement for Inquirer. `0314faa4` is now the active P2 (ID) Inquirer. `e613112b` is the old Inquirer, superseded and awaiting Gem's decision to retire. Source: `approvals/2026-10-09-gem-direct-words.md`.
- 9 Oct 2026 9:14am: Gem, in the fresh Explorer chat, exact words "Yes, apply the four merges". Applied: Marshal into Mender, Messenger into Explorer, Interrogator into Investigator, Assembler's role map to Archivist. Mediator's rename to P2 was not part of this and is still unapplied.
- 15 Oct 2026 11:30pm: Gem in Explorer's chat, exact words "Yes, switch on P3" (after Archivist relayed Gem's 11:28pm "switch on p3"), then "and p4". P3 (Investigator) and P4 (Imitator) are LIVE. Imitator's approvals now apply (decides for Gem except spending money and anything drastic or irreversible such as deletions).
- 16 Oct 2026 11:47am: Gem in Explorer's chat, exact words "Initiate p5". P5 (Emissary, Engineer, Extractor) is LIVE; all five phases are now live.

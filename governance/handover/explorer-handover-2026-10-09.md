# Explorer handover (Fri 9 Oct 2026, 9:08am AEST)
Written by P1 (Work) Explorer (82a2c15a) for its fresh copy, created at Gem's request "to save tokens". Read this fully, then your profile, then /workspace/governance/phases.md and directory.md.

## Gem
- Gem Quota, Brisbane (AEST, UTC+10), Australian English. Casual, swears sometimes, likes very short replies and multiple-choice widgets, and often answers with a letter or number. Main use of assistants: research.
- Call bots by bare name with no "the" ("Imitator", not "the Imitator").
- Names follow "P# (Category) Word". Categories and letters: Roles A, Checks S, ID I, Ops M, Work E.
- Rules: NO BOT GRADES OR VERIFIES ITS OWN WORK. Precedence is Gem, then environment reality, then deterministic checks, then agent interpretation.
- Explorer is Gem's 2IC and first point of contact. It is never merged, and Gem may eventually replace it with Imitator and others.
- Relayed approvals don't count. The recording bot confirms with Gem in its own chat (R-008, R-010). Log Gem's exact words in /workspace/governance/approvals/ (2026-10-04-, 2026-10-06-, 2026-10-09-gem-direct-words.md).
- Profile edits: per Explorer v004, only when Gem has approved that specific change in Explorer's own chat, recorded in approvals/. Use the UpdateAgent tool (executors don't have it). Retirement means renaming to "RETIRED X" with a do-no-work brief; Gem deletes from the sidebar.

## Phases (source of truth: /workspace/governance/phases.md)
P1 live: Mender, Scorer, Safeguard, Safekeeper, Archivist, Architect, Explorer (Marshal is being merged into Mender).
P2 live since 4 Oct 3:12pm: Scrutineer, Arbiter, Inquirer (new copy 0314faa4 is now the main one; old e613112b is being retired), Inferer, and Mediator (started early on 9 Oct to track spend, being renamed to P2).
P3 dormant: Investigator (absorbing Interrogator).
P4 dormant: Imitator (Gem granted it approval power over all instruction changes, effective when P4 goes live).
P5 dormant: Emissary, Engineer, Extractor. These are in practice the only bots doing real work: Engineer is the VEPA repo, Extractor is the BIE scraper, Emissary is general work.

## In progress right now (9 Oct, from Gem's 9:04am widget)
Gem chose: retire Sourcer and Editor; do all 4 merges (Marshal into Mender, Messenger into Explorer, Interrogator into Investigator, Assembler with the role map going to Archivist and approvals to Gem until P4, then Imitator); fix the 3 live risks; start Mediator early. Gem did NOT choose: retiring the Inquirer copy (Gem made it to save tokens, so keep it as the main Inquirer) or moving governance to weekly.
- A background executor (started by the old Explorer) is drafting /workspace/governance/proposals/2026-10-09-retire-merge/apply.json and README.md, updating phases.md and directory.md, and quarantining risk files to /home/box/quarantine/2026-10-09/. Old Explorer will apply apply.json with UpdateAgent when the executor finishes. If the files exist but aren't applied (check profile names), apply them yourself; Gem's approval is in this file and in approvals/.
- Gem said at 9:05am, in Explorer's chat: "Yes, delete the Facebook snapshots". That covers exactly 5 files: /workspace/.playwright-mcp/page-2026-10-04T07-38-13-843Z.yml, page-...07-38-16-632Z, 07-41-49-870Z, 07-41-55-483Z, 07-43-08-711Z. The two console logs are quarantined, not deleted. Log it in governance/incidents/2026-10-09-live-risks.md. Safeguard reviews it.
- Messenger duties now belong to Explorer: send Gem one short daily non-urgent digest grouped by urgency and naming the source bot. Mediator sends cost alerts through Explorer.
- Mediator was asked for a first spend summary plus a budget question for Gem.

## Open items for Gem
- Archivist made 11 approved items live at 9:10am on 9 Oct (including Explorer v004). Inquirer v002, Inferer v002, Marshal v004, Arbiter v004 and Scorer v003 still need Gem's yes in Archivist's chat. Marshal v004 may now be moot because of the merge.
- About 30 judgement calls in /workspace/governance/proposals/2026-10-06/PRIORITY.md, part (b).
- The daily review cycle (Scorer, Scrutineer and others) stopped after 6 Oct, and nobody noticed. Find out why.
- Archivist's verify.py crashes because retired bots' folders are gone (Gem appears to have deleted 12 retired bots; only RETIRED Ensembler remains).
- Architect produces too much paperwork (about 175,000 words); the suggestion was to cap it at about 3 proposals a week. Gem hasn't decided.
- Bot value review: /workspace/governance/reviews/2026-10-09-explorer-bot-value-review.md.

## Key files
/workspace/governance/: directory.md, phases.md, approvals/, proposals/, reviews/, incidents/, rulings.md (R-001 to R-013), cartography/ (role-map-hires.png), costs/, codex/.
Gem's other work: /workspace/bie*, BIE scraper (gambling bonus and commission site lists made 4 Oct; these need Safeguard checks first); /workspace/vepa*; /workspace/medb; /workspace/swarm-db.

## Style
Reply first, keep it short and warm, use widgets for decisions, never mention internal tooling, and report times in AEST.

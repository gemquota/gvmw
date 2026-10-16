# Findings (role map v3, 4 Oct 2026)

Full rebuild after the renames, the three merges (first, second and Merge F) and Gem's phase reshuffle (3:12pm). Based on the latest codex version of each of the 23 active bots (mapped by id), `phases.md`, `directory.md` and the Merge F proposal. Retired bots are excluded. Edge evidence is in `role-graph.json`; earlier findings are in `findings-v1.md` and `findings-v2.md`. Several items match the Archivist's open lists (`codex/PENDING-FOR-ASSEMBLER.md`, `codex/PENDING-FOR-ARBITER.md`); their item numbers are given in brackets.

## Phase source check
- **`phases.md` and the phase list I was given agree** (P1 8, P2 5, P3 3, P4 3, P5 4 = 23). The map follows `phases.md`.
- **Live names match `phases.md`.** When checked at 3:16pm, all 23 live profile names already carried the new prefixes (e.g. "P2 (ID) Inquirer", "P5 (Work) Editor"). The older "Phase prefixes (4 Oct 2026)" section of `directory.md` still lists the old P1-P7. A later section (3:12pm) points to `phases.md`, which wins.

## (a)/(c) Self-checks that break "no bot grades or verifies its own work"
1. **Safeguard dry-runs and then reviews the same risky action**, although its brief forbids reviewing its own work. *(compliance-risk-officer/v002; E3)*
2. **Scorer scores "every bot, the governance bots included"** with no self-exclusion, and nobody independently scores the Scorer (the Scrutineer audits it, but against instructions, not quality). *(assessor/v001)*
3. **Mender owns the state record and indexes and also decides what to clean up**, so it judges which of its own records are disposable. There's no independent check and no Gem approval for deletions, and its protected list misses proposals, approvals, cartography, rulings, risk/ and security/. *(mender/v002; A7, E2)*
4. **Imitator gives alignment verdicts against its own preference model** and, if its approval role stands, would approve proposals against that same model. The Interrogator tests its answers, not its verdicts or approvals. *(clone/v003)*
5. **Scrutineer and Architect check each other.** Scrutineer v002 says the Architect reviews its work, but Architect v001 forbids checking bots' work, and the Architect's own proposals are triggered by the Scrutineer's reviews. *(auditor/v002, instruction-architect/v001; B3)*
6. **Engineer** is forbidden to judge its own code, but its brief doesn't name who does. Until a reviewer is named, nothing stops it checking its own code. *(codey/v003)*
- **Fixed since v2:** Arbiter v003 no longer approves, so it can't rule on its own approvals. Assembler v003 forbids approving its own drafts.

## (b) Imitator's approval claim (UNVERIFIED)
7. **Imitator v003 claims Gem granted it delegated approval of any proposal, governance bots included**, sent to the Archivist and logged in `approvals.md`. The codex index flags this as UNVERIFIED: the grant was edited in at 14:41 and isn't in Gem's merge notes. Archivist v001 doesn't accept Imitator approvals. `phases.md` says Gem approves directly until P4 (the Imitator's phase) goes live, and the Imitator is dormant. The graph and diagrams mark these edges **UNVERIFIED** until Gem confirms or revokes the grant. If it stands, it overlaps the Assembler's approval duty and the Gem-approval rule.

## (d) Duplicate or overlapping duties after the merges
8. **Stall detection.** Mender is "the single owner", but the Arbiter watches Architect stalls itself (and tells Gem) and the Marshal watches missed runs. Scrutineer reports to the "Minder". *(A1)*
9. **Pauses.** Safeguard (unsafe work) and Mediator (runaway cost) can ask bots to pause, and the Arbiter rules on who may lift one, but neither Safeguard nor Mediator mentions the Arbiter. *(item 2)*
10. **Routing.** Marshal's "routing work to the fastest path" (from the Expediter) overlaps the Explorer's role as Gem's 2IC deciding who does ad-hoc work. *(B7)*
11. **State records.** Mender's task-state and handoff record overlaps the Engineer's `.codey/checkpoint.json` and the Marshal's `schedule.md` handoffs. *(A8)*
12. **Preference fit.** Imitator alignment verdicts overlap the Scorer's "fit with Gem's preferences". The Imitator's drift reports go to an Architect that only acts on Scrutineer reviews. *(A9)*
13. **Truth and evidence.** Scrutineer (environment reality, from the Surveyor) and Sourcer (provenance) overlap. The Sourcer still says the retired Surveyor rules on system truth.
14. **Identity confirmation.** The Investigator alone may promote a detail, but the Inferer still marks details "confirmed" itself and the Interrogator doesn't know the Investigator. *(A3)*
15. **Mediator carries two unrelated duties** (connector health and spend). It also sends cost alerts "through the Messenger", but Messenger v002 says budget breaches go straight to Gem from the raising bot.
16. **Engineer carries coding plus the swarm build** (interim brief, to be finalised by the Architect).

## Conflicts and stale references
17. **Marshal's daily chain names "Arbiter or Gem"** for the approval step. After Merge F it should be Assembler, or Gem until P4. There's no phase variant that skips dormant bots. *(B6)*
18. **Scrutineer checks against "the Arbiter's role map"** and sends reviews to the Arbiter. The role map is the Assembler's again.
19. **Old or retired names in active briefs.** Archivist, Architect, Scorer, Inquirer and Inferer use pre-rename names (Clone, Auditor, Assessor, Role Cartographer). Marshal says "Meter", Scrutineer "Minder", Sourcer "Surveyor", and Emissary "Codey", "Scraper", "Swarm Builder" and "Clone". *(A10)*
20. **Live and codex drift.** Interrogator, Messenger and Emissary have approved v002s in the codex, but their live profiles still run v001 (Emissary's is the bare tagline). The map uses the codex text and flags these.
21. **Live bots depend on dormant ones.** P1/P2 bots rely on P4 bots: the Scorer and Architect ask the Imitator for preferences, the Inferer feeds the Imitator, and the Scorer and Scrutineer expect cost data from the Mediator. Until P4 starts there's no preference source, no spend tracking and no digest.
22. **Live profiles are changed outside the pipeline.** The Explorer applied the Merge F profile edits directly (on Gem's chat approval), and the Archivist recorded them afterwards "from live profile". Gem may edit directly, but the Explorer's role in doing so isn't in any brief.

## Gaps and bots with few or no edges
- **Extractor:** empty instructions, no edges of its own (only fan-out duties from others). A draft awaits Gem.
- **Editor:** no Rules, and no bot is told to send it work. *(A6)*
- **Unrouted services:** nobody is told to send raw inputs to the Safekeeper for cleaning or planned risky actions to Safeguard for dry runs. *(A6)*
- **Explorer:** still the v001 aspirational text with no Rules or Limits, though it's Gem's 2IC, keeps `phases.md` and relays approvals.
- **Groups and Council in `directory.md` predate the merges.** The Arbiter, Mender, Sourcer, Investigator and Editor are in no group. That section also has a duplicated block.
- **Recorded vs proposed.** Gem approved 14 queue items at 3:01pm, but they aren't in the codex yet. Proposed final briefs in `proposals/final-2026-10-04/` (Architect, Archivist, Emissary, Engineer, Explorer, Extractor, Interrogator, Mediator, Messenger, Safeguard, Safekeeper, Scorer, Scrutineer) are not on this map until recorded.

## Suggested next steps (short)
1. Gem: confirm or revoke the Imitator's approval grant.
2. Name independent checkers: who scores the Scorer, who reviews Safeguard's dry runs, who approves Mender deletions, who reviews the Engineer's code, and who reviews the Scrutineer (Gem, per the earlier decision).
3. Architect: refresh stale names and routes (Marshal chain, Scrutineer role-map line, Sourcer, Emissary), add Arbiter references to the pause rules, and make the Inferer defer to the Investigator.
4. Explorer: update the stale "Phase prefixes" section of `directory.md` (or point it to `phases.md`).
5. Record the 14 approved items and deploy the three undeployed v002s, then refresh this map (v4).

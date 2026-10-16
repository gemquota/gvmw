# Fix list B2 — overlaps, one owner each — NEEDS GEM'S DIRECT APPROVAL

Style: bare bot names. Exact text to add or change per bot.

## Stall detection → Mender (R-006)
Already in mender-delta, arbiter-delta, architect-final and handoff-phase1-final. One owner: Mender detects and logs every stall, Architect's included. Marshal and Arbiter report stalls to Mender; Arbiter escalates an overdue Architect stall to Gem and never drafts in Architect's place. No new text beyond those files.

## Lifting pauses → Arbiter lifts; Safeguard and Mediator reference it
- **Safeguard (v-next on safeguard-final):** add "Safeguard can ask a bot to pause unsafe or non-compliant work, but only Arbiter rules on who may lift a pause; Safeguard refers pause-lift requests to Arbiter."
- **Mediator (v-next on mediator-final):** add "Mediator can ask a bot to pause on cost grounds, but only Arbiter rules on who may lift a pause; Mediator refers pause-lift requests to Arbiter."
- **Arbiter (add to arbiter-delta):** confirm "Arbiter rules on who may lift any pause, including pauses set by Safeguard (unsafe work) and Mediator (runaway cost)."

## Routing → Marshal (routines) vs Explorer (ad-hoc)
- **Marshal (fix in fix-03):** remove "routing work to the fastest path"; Marshal owns run order, pacing, caching and parallelism of routines, not who does ad-hoc work.
- **Explorer (explorer-final):** already owns ad-hoc work routing as Gem's 2IC. One owner each: Marshal = routine timing/throughput; Explorer = who does ad-hoc work.

## State records → Mender (authoritative) vs Engineer (repo-local) vs Marshal (schedule)
- **Mender (v-next):** add "Mender owns the authoritative record of task state, checkpoints and handoffs at /workspace/governance/state/. A bot's repo-local working files (for example Engineer's .codey/checkpoint.json) and Marshal's run schedule (schedule.md) are not the authoritative state record and Mender doesn't own them."
- No change needed to Engineer or Marshal beyond this boundary note.

## Preference fit → Imitator owns the model; Scorer consumes it
- **Scorer (scorer-final already):** "fit with Gem's preferences (ask Imitator once P4 is live; until then n/a)". Confirmed. Scorer keeps no preference model of its own.
- **Imitator:** owns the preference model and alignment verdicts; drift reports go to the responsible bot and to Architect. (Imitator dormant, P4.)

## Truth → Scrutineer (system/reality) vs Sourcer (provenance)
- **Sourcer (fix in fix-03):** replace "ruling on what's true (that's (Checks) Surveyor's job for the system ...)" with "ruling on what's true (that's Scrutineer's job for the system, and Investigator's for identity)". Sourcer owns the provenance ledger (where each fact came from), not truth.

## Identity confirmation → only Investigator promotes
- **Inferer (fix in fix-03, live P2):** Inferer must not mark a detail 'confirmed'. Exact change below in fix-03.
- **Interrogator (interrogator-final already):** "only Investigator can mark a detail confirmed" is in. Add (v-next): "Interrogator also samples Imitator's alignment verdicts, not only its answers."

## Messenger vs Mediator — one consistent cost-alert route
Problem (finding 15): Mediator sends cost alerts "through Messenger", but Messenger v002 says breaches go straight to Gem from the raising bot.
- **One rule:** cost-breach and runaway alerts are **drafted by Mediator and delivered to Gem by Messenger as urgent; Mediator never sends a cost alert without Gem's approval.**
- **Mediator (v-next on mediator-final):** keep "send a draft cost alert for Gem through Messenger (never send without Gem's approval)".
- **Messenger (v-next on messenger-final):** replace the clause that lumps "budget breaches and runaway spending (including Mediator's draft cost alerts)" under "urgent alerts go straight to Gem from the bot that raised them" with: "Urgent alerts go straight to Gem from the bot that raised them, except cost-breach and runaway-spend alerts, which Mediator drafts and Messenger delivers to Gem as urgent (Mediator never sends them without Gem's approval)."

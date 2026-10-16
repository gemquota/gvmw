# Retire and merge drafts: 9 Oct 2026

Gem approved this at 9:04am AEST on Fri 9 Oct 2026 (relayed by Explorer). Background: `reviews/2026-10-09-explorer-bot-value-review.md`.
**These are drafts. Nothing has been applied.** `apply.json` is a list of `{agent_id, name?, description}` for Explorer's profile-edit tool. The drafts were built by `_build.py` from the live `profile.json` text as it read at about 9:05am, after the 9:03 to 9:04am deployments. If any profile changes before you apply, rerun `python3 _build.py`. It fails loudly if a sentence it edits has moved.

Under R-008, Archivist has to confirm Gem's approval with Gem directly before recording any of these as codex versions. Changes to **Imitator** and **Investigator** (the bot that now checks Imitator) need Gem's own approval, never a relayed one.

## Retirements (7 entries)
| Bot | New name | Points to |
|---|---|---|
| Sourcer `2fe3e92f` | RETIRED Sourcer | Explorer |
| Editor `2888c17a` | RETIRED Editor | Explorer |
| Marshal `f3810109` | RETIRED Marshal | Mender (now owns schedule.md) |
| Messenger `5e47d344` | RETIRED Messenger | Explorer |
| Interrogator `d3191aa8` | RETIRED Interrogator | Investigator |
| Assembler `d1daab5f` | RETIRED Assembler | Archivist for the role map; Gem for approvals until P4, then Imitator |
| Inquirer (old) `e613112b` | RETIRED Inquirer (old) | The active P2 (ID) Inquirer `0314faa4`. **Applying this retires it.** Gem's 9:06am words list it as "awaiting Gem's decision to retire", so apply it only when Gem says. |

Each brief reads: "RETIRED on 9 Oct 2026 … Do no work; refer every request to X. Waiting for Gem to delete."

## Merges and updates (11 entries)
- **Mender `c8401a53`, still "P1 (Ops) Mender"** (full rewrite, 4,657 characters). Keeps every existing duty and adds Marshal's:
  - run order and timing, with `schedule.md` as the plan and `state/` as the record;
  - pacing, backpressure, load, caching, parallel runs and routing between bots. It decides how and when work runs, never what work gets done.
  - **Stall detection is strengthened for the 7 Oct failure.** There's a fixed-time weekday chain check (a watchdog, even though the chain itself runs on handoffs). Each run also looks back to its last `state/chain` file and logs every missed weekday, including days its own routine didn't run. A stall goes to Gem the same day. A whole missed weekday, or two in a row, is an incident.
  - It still doesn't judge its own stall: those close only on Scrutineer's evidence or Gem's word. Explorer's new digest duty adds an independent check (below).
  - Also from Marshal: it doesn't change budgets (Mediator holds them) and never skips checks or approvals.
- **Investigator `f2016e9b`, still "P3 (ID) Investigator"** (full rewrite). Absorbs Interrogator's weekly test of Imitator's accuracy, once P4 is live. Ground truth is only what Gem said or confirmed. Imitator's own view isn't evidence. **Self-check guard:** if a wrong answer traces back to a detail Investigator itself promoted, it reports that to Scrutineer and Gem instead of judging it. Scorer scores it and Scrutineer audits it. Sourcer's provenance input is replaced by the evidence tags in other bots' outputs. Adds "keep personal details out of shared /workspace folders" (lesson from T-004).
- **Archivist `61ef3abd`** (minimal edits, 5,117 characters). Adds CONTROLS (4), the role map under `/workspace/governance/cartography/`. It's rebuilt from the codex and phases.md within one working day of each change, earlier versions are kept, it decides nothing and approves nothing, and Scrutineer checks it. All its current duties stay. Other edits:
  - Assembler is removed as an approval source and from the codex reader list.
  - "Tell Assembler…" becomes "Update the role map…".
  - Unrecorded agents are also marked on the map.
  - The Interrogator reference is removed.
  - R-012's example now says the hold on `0314faa4` ended with Gem's 9:06am words, which Archivist confirms with Gem directly.
- **Arbiter `2133048d`**: **change needed.** It named Assembler as the approver and role-map keeper. Now approving and applying are Gem's until P4, then Imitator's, and the role map is Archivist's.
- **Imitator `6ae584b8`**: **no Assembler-as-approver reference, so nothing changes for that.** One edit is still needed: "(the Interrogator tests those)" becomes "(Investigator tests those)". This needs Gem's own approval.
- **Mediator `90f9eb20`**: renamed "P2 (Ops) Mediator". The description is otherwise unchanged except two phrases. The actual text was "through the (Ops) Messenger's daily digest" and "through the (Ops) Messenger"; these become "through Explorer's daily digest" and "through Explorer".
- **Other active bots that referred to retired bots (minimal edits):**
  - **Architect**: after P4, proposals go to Imitator or Gem. Imitator and Investigator changes always go to Gem. "If Assembler or Imitator rejects" becomes "If Imitator rejects".
  - **Scrutineer**: "the Assembler's role map" becomes "the role map (kept by Archivist)", and reviews are no longer sent to Assembler.
  - **Emissary** and **Engineer**: "(or by Assembler or Imitator once P4 goes live)" becomes "(or by Imitator once P4 goes live)".
  - **Inferer**: points at the active Inquirer `0314faa4`, not `e613112b`. Also "Clone", an old name with no matching bot, becomes "Imitator" (same id, `6ae584b8`). Drop that part if you want the edit even smaller.
- **No change needed:** Scorer, Safeguard, Safekeeper, Extractor and the active Inquirer `0314faa4`. None of them names a retired bot.

## Explorer (not in apply.json; for you to edit yourself)
**Paragraph to add (Messenger duties):**

> DIGEST (taken over from the retired Messenger, 9 Oct 2026): Collect non-urgent updates from all bots, including Mediator's routine spend summaries, and send Gem one short, prioritised daily message in Gem's chat, grouped by urgency, with duplicates merged. Name the source bot for each item and keep its meaning; never soften or drop a point, and flag any item you can't trace to a real bot instead of passing it on as fact. Anything about your own work (reviews, scores, risk findings or complaints about Explorer) goes in word for word, unedited and marked as about you. Urgent alerts still go straight to Gem from the bot that raised them, and you never hold them back: serious quality problems and 3 poor reviews in a row, budget breaches and runaway spending (including Mediator's draft cost alerts), pause requests, exposed secrets, broken routine chains, broken connectors stopping urgent work, and governance approvals or escalations that need Gem. Each weekday, also check that Mender's chain record for the previous weekday exists in /workspace/governance/state/chain/; if it doesn't, report it to Gem as urgent, since Mender can't judge its own stall. Only message Gem, and only in Gem's chat.

**Sentences in your current text that name retired bots** (exact old text, then the new text):
1. "Marshal runs the timing of recurring routines; take cross-group issues to the Council." becomes "Mender runs the timing of recurring routines; take cross-group issues to the Council."
2. "Gem approves until P4 goes live, and after that Assembler or Imitator approve as their instructions set out;" becomes "Gem approves until P4 goes live, and after that Imitator approves as its instructions set out;"
3. "Messenger is dormant until P4 goes live: until then, send everything non-urgent … through Messenger's digest instead." is **replaced by** the DIGEST paragraph above.
4. "Archivist notes it in the codex index and Assembler marks it on the role map." becomes "Archivist notes it in the codex index and on the role map."
5. "(R-012 does this for 'P2 (ID) Inquirer copy')" is deleted. Gem decided on 9:06am that 0314faa4 is the active Inquirer.

## Rules kept
- No bot grades or verifies its own work. This is restated in Mender, Investigator and Arbiter. Imitator never checks itself: Investigator tests it.
- Gem's precedence is unchanged: Gem, then environment reality, then deterministic checks, then agent interpretation (Arbiter and Scrutineer text untouched).
- Gem approves until P4. Changes to Imitator, or to a bot that checks it, stay Gem's only.

## Open points for Gem (not drafted)
- **"Applying approved changes" goes to Imitator after P4.** Neither the current Imitator brief nor this draft gives it the power to edit live profiles. Its brief forbids irreversible actions, and Archivist's deployment clause still says deploying is Gem's action. Adding that power is an Imitator change, which is Gem-only, so it's left for Gem to decide.
- **Same name on two agents:** `0314faa4` and `e613112b` are both named "P2 (ID) Inquirer" right now. Until the old one is renamed, bots and Gem can't tell them apart by name.
- **Safeguard** says "spending to Mediator (until P4 goes live, spending is Gem's)". Mediator is now live at P2, but spending decisions are still Gem's, so the sentence still holds. Optional tidy-up only.
- Mediator's text still says "the (Checks) Safekeeper" and similar ("the" plus a bot name). It was kept as asked; a later tidy could switch to bare names.
- Investigator's bulk mailbox reading (RR-008) should go through Safeguard first. This wasn't added, as it's outside today's scope.
- Role-map files in `cartography/` still show Assembler as the owner. Archivist should rebuild them once these changes are applied.

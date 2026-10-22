# r044-veto batch (22 Oct 2026): imitator-v008, arbiter-v007 — DRAFT, NEEDS GEM

- **Source:** R-044 and its 7:52pm update (rulings.md). Arbiter read Inquirer's transcript directly: Gem's own words in Inquirer's chat at 7:00pm, answering "If two bots disagree while you're away, what should Imitator do?" with option C "Pass it to Arbiter": "C and Imitator can veto if desired". They're not in approvals/ yet, so the paste line opens with Gem restating them and Archivist records them first (R-029).
- **Note:** the brief for this batch ("as messaged earlier") never reached Architect. This draft follows R-044 exactly. Check that it matches what you meant.
- **What changes (one sentence added to each):**
  - **Imitator:** while Gem is away, Arbiter rules on disputes and Imitator may veto a ruling, with three limits:
    - no veto on disputes about Imitator or its five checkers;
    - a veto never overrides Gem's words or a deterministic check;
    - each veto is logged with its reasons in rulings.md and flagged in the digest.
    
    **Schedules (R-046 update):** Imitator may change other bots' schedules or routines, flagging each change in its digest note. It may never change the schedules of Investigator, Scorer, Scrutineer, Safekeeper or Safeguard without Gem's words for that change. Investigator verified Gem's 7:06pm choice in Imitator's transcript.
  - **Arbiter:** the same rule from Arbiter's side, plus the checkers'-schedules limit, which Arbiter enforces (R-046).
- **Revision 2 (8:10pm):** fixes Scrutineer's review (`reviews/2026-10-22-r044-veto-review.md`): schedules wording per R-046, and R-045/R-046 cited. Revision 1 is kept in `_tools/*.r1.bak`.
  - **Default chosen:** a vetoed ruling doesn't take effect, and the dispute waits for Gem. R-044 doesn't say what happens after a veto, so Gem can choose otherwise.
- **Approver: Gem directly** for both. The change widens Imitator's role (R-028), and R-044 says Gem approves. Scrutineer reviews.
- **Bases:** stacked on the redundancy drafts. Imitator is on imitator-v007 (text db56debaa35f, Gem-only, not yet approved). Arbiter is on arbiter-v006 (text c0849fa416cb, recorded in the codex at 7:55pm, so it matches). If Gem declines imitator-v007, imitator-v008 is rebased on codex clone v006.
- **Record order:** the redundancy batch, then this batch, then GitHub revision 5 (whose imitator-v009 and arbiter-v008 stack on these).

| Draft | Base text | New text | File |
|---|---|---|---|
| imitator-v008 | db56debaa35f | 0f3acc7a3e67 | 842c9148c347 |
| arbiter-v007 | c0849fa416cb | 9c75e34a05cb | 38ae56219e67 |

**Paste line:** `I confirm I told Inquirer at 7:00pm on 22 Oct: "C and Imitator can veto if desired", and chose on Imitator's card at 7:06pm: "Yes, you can veto Arbiter in disputes and change bots' schedules (flagged in the digest)". I approve r044-veto: imitator-v008 (0f3acc7a3e67) and arbiter-v007 (9c75e34a05cb), after the redundancy batch — record and deploy.`

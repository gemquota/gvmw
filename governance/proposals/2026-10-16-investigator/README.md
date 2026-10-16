# Investigator v004 draft, 16 Oct 2026

**Status (16 Oct 2026, ~11:56am AEST, Archivist):** RECORDED and DEPLOYED. Gem approved in Archivist's chat at 11:48am ("I approve proposals/2026-10-16-investigator/investigator-v004.md. Record and deploy it."). Recorded as `codex/investigator/v004.md`; live at 11:49:23 AEST (manifest `codex/_tools/deploy_manifest_2026-10-16d.json`); awaiting Scrutineer's check.

Originally written as a draft only: nothing recorded in codex/, no profile edited and no bot messaged.

| File | Base (checked = live) | New | Approver | Status |
|---|---|---|---|---|
| `investigator-v004.md` | investigator v003 (byte-matches live) | v004 | **Gem directly** (R-015, R-027) | RECORDED and DEPLOYED: Gem approved in Archivist's chat 11:48am 16 Oct; recorded as codex/investigator/v004.md; live 11:49:23 AEST; awaiting Scrutineer's check |

## Change
- **Imitator accuracy check:** "Each week" becomes "Each day … (Gem, 16 Oct)".
- **Score sent to Scorer:** "weekly accuracy score" becomes "daily accuracy score".
- **Kept word for word:** the check stays a review after the fact that never blocks Imitator: "This testing is a review after the fact, not a gate: Imitator's decisions take effect without waiting for you or any other checker (Gem, 10 Oct; R-019)."
- **Nothing else changes.** The draft doesn't set a run time, because timings belong in Mender's schedule.

## Source
- Gem said this directly to Investigator at 11:05am on 16 Oct: "Always approve imitator, run the accuracy check for Imitator daily". Investigator recorded it in `approvals/2026-10-16-gem-direct-words.md`.
- For Investigator these are Gem's own words, not a relay. For a change to Investigator's brief, they are only the source. Investigator checks Imitator, so the change needs Gem's own approval given to Archivist, in Archivist's chat or on a voice call with Archivist (R-015, R-027, R-010). A relay, including Investigator's record, or an Imitator approval won't do.
- **Routine:** Investigator says its routine is already daily at 6:31am AEST and that it applied the daily check straight away. Nothing on disk confirms this:
  - Mender's `schedule.md` still lists Investigator as "Weekly, no time set on disk".
  - Until this draft is live, the brief says weekly and the practice is daily. Running the check more often than the brief says is harmless, because the check doesn't block anything.
  - Mender should update `schedule.md` once Gem approves.

## Judgement call: what "Always approve imitator" means
- **Default reading:** Investigator's checks never block or hold up Imitator's decisions. The brief already says this (R-019), so nothing is added, and the draft widens nothing beyond it.
- **Other readings, not drafted, for Gem to say if meant:**
  1. Investigator should give Imitator approval or a pass mark. That conflicts with Investigator's role: it scores accuracy against what Gem actually said, and no bot verifies its own work. A blanket pass would empty the check.
  2. Imitator's approvals should be treated as Gem's for everything. That would widen Imitator's authority past R-019, which excludes spending, deletions, public or shared pushes and other drastic or irreversible decisions. R-028 says a widening like this needs Gem's own confirmation.
  3. Investigator should approve Imitator's own instruction changes. R-015 and R-027 keep those with Gem.
- If Gem meant any of these, it needs a separate draft and Gem's explicit words to Archivist.

## Conflicts
- **Pending drafts:** none.
  - No draft in `proposals/2026-10-16/` or `proposals/2026-10-16-rr028/` changes Investigator.
  - None of them mentions the weekly accuracy check or the weekly score.
  - Gem approved both batches at 11:02–11:03am, before this draft.
- **Scorer:**
  - Scorer's brief (assessor v003, and scorer-v004, approved by Gem at 11:02am) doesn't fix how often Investigator's score arrives, so a daily score doesn't conflict.
  - A daily score will be noisier than a weekly one. Scorer may want to roll it up weekly, which is Scorer's call.
- **Architect's weekly cap:** this counts as one of about 3 short proposals this week. It isn't a safety fix, but Gem asked for it, and R-028 says the cap mustn't hold back a proposal Gem asks for.

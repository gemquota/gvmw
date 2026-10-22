# Redundancy batch (22 Oct 2026), revision 2: 12 brief changes + 1 optional fold

**RELAYED request (R-008).** Imitator relayed it at 7:07pm AEST, 22 Oct. Imitator says Gem replied in Imitator's chat to its redundancy assessment: "Yeah fix those and proceed as suggested". They answer **Imitator's assessment, now at `reviews/2026-10-22-redundancy-assessment-imitator.md`** (Gem asked for it at 6:56pm). **These words are not in approvals/** (searched 7:15pm for "fix those" and "proceed as suggested": no match). So each approver confirms with Gem directly, and Investigator can check Gem's words against Imitator's transcript. Imitator can't approve items in this batch that it relayed on Gem's behalf without that check, and can't approve its own brief or its checkers' briefs at all.

Revision 2 built at 7:21pm AEST by `_tools/build.py`, after Scrutineer's review (`reviews/2026-10-22-redundancy-review.md`) and R-044. Revision 1's build is kept as `_tools/build-rev1.py.bak`. Each base is the latest codex version, byte-checked against the bot's live profile. Each draft lists the exact sentences changed; the build checks every other sentence is kept word for word. Every draft also has the five template sections (Purpose, Scope, Rules, Relationships, Limits) as a summary; the verbatim text is what deploys.

## Revision 2 changes
- **R-044 (Arbiter, 7:18pm):** Explorer assigns new work (Gem's tasks to bots). Mender keeps operational routing: run order, recovery, rerouting stalled or failed work, and stall detection. explorer-v006 now says "Explorer assigns new work" instead of "only Explorer routes work". emissary-v007 and extractor-v006 match ("hands specialist work back to Explorer" kept). Mender v005 is unchanged.
- **Engineer (codey v007) checked, no draft:** "It takes coding and swarm tasks from Gem (and, once its phase is live, from Explorer or another bot on Gem's behalf…), never routes work to a dormant bot". "Another bot on Gem's behalf" sits loosely with "Explorer assigns new work", and "never routes work" is about not using dormant bots. It doesn't clearly conflict, so it's a note for the GitHub batch's revision 5 (engineer-v008), not a change here.
- **Routing:** explorer-v006 goes to Gem (confirmed in the Gem-only paste line). scrutineer-v005 is **reviewed by Scorer, not Scrutineer** (no self-review). The Extractor fold is **Gem's alone (R-019)**, and its proposal now lists what it needs first: a merged Emissary brief with a wall between posting and scraping, R-031 and RR-015 carried over, and a connector-limits update (Extractor is the named Apify runner). The merged brief isn't drafted.
- **Order:** this batch is recorded first. The GitHub batch is rebased on top as its revision 5 (added to its pending list).

## Drafts against Imitator's assessment
The five items match the assessment's harmful overlaps and "no owner" list, with these differences:
- **Item 2, the router:** the assessment says "Only Explorer should route". R-044 narrows this: Explorer assigns new work, and Mender keeps operational routing. The drafts follow R-044.
- **Item 4, Architect:** the assessment names only Arbiter's stall clause. architect-v005 also changes Architect's matching line, which cited Arbiter's escalation.
- **Item 5, Mediator's rename:** the assessment lists it as having no owner. Scrutineer's 22 Oct review found no Gem words asking for it, so architect-v005 makes Architect the owner only "when Gem asks".
- **The fold:** the assessment offers it as an alternative ("or fold it into Emissary after archiving it"). Here it's a separate yes/no for Gem, after collection-only is applied.
- **Not in the five items:** the assessment's "Doing little" list (Extractor, Inquirer, Mediator, Architect, Explorer) and its "Deliberate, so keep" list. Neither is acted on here. Inquirer's brief needs no change.

## What changes
| Item | Change | Drafts |
|---|---|---|
| 1 | One certainty vocabulary, word for word in all three ID briefs; "confirmed" defined on Investigator's ladder; every gap about Gem goes through Inferer only | inferer-v006, investigator-v005, imitator-v007 |
| 2 | Emissary owns research write-ups; Extractor collects and scrapes only; Explorer assigns new work and Emissary and Extractor hand specialist work back to it; Mender keeps operational routing (R-044) | emissary-v007, extractor-v006, explorer-v006 |
| 3 | Imitator out of grading (alignment verdicts dropped); Scorer's preference fit comes only from Gem's recorded words in approvals/ | imitator-v007, scorer-v005 |
| 4 | Arbiter's stall clause dropped (Mender owns stalls, R-006); Architect's matching line updated | arbiter-v006, architect-v005 |
| 5 | Owners: streaks.md → Scrutineer; standing approvals for recurring syncs → Safeguard; agent folders vs directory → Archivist; drafting Mediator's rename → Architect | scrutineer-v005, safeguard-v007, archivist-v009, architect-v005 |
| Optional | Fold Extractor into Emissary: Gem's alone (R-019), not ready until a walled merged brief and a connector-limits update are drafted | extractor-fold-proposal.md (separate yes/no) |

Inquirer's brief needs no change: it already takes its gaps only from Inferer. Mender's brief already owns stalls.

## Approvers
- **Gem directly (R-027):** investigator, imitator, scorer, scrutineer, safeguard (Imitator's checkers or Imitator itself), archivist (never on Imitator's approval), explorer (its own brief says Gem), and the fold (Gem's alone, R-019).
- **Reviewers:** Scrutineer for every draft except scrutineer-v005, which **Scorer** reviews (no self-review).
- Scrutineer recommends that inferer-v006 go to Gem along with the other two ID drafts, so the shared vocabulary lands at the same time. It's routed to Gem or Imitator here, but the rest paste line has Gem approving it too.
- **Imitator or Gem** (after a 1:1 check of Gem's words, a Safeguard dry run, within R-019): inferer, arbiter, architect, emissary, extractor.

## Hashes (sha256, first 12)
| Draft | Base text | New text | File |
|---|---|---|---|
| inferer-v006 | b348276a1f72 | 441b92c9fcd4 | 7798ada96861 |
| investigator-v005 | 68b76c08ba86 | c8bafae381de | f9969494895f |
| imitator-v007 | 4a5e5def3406 | db56debaa35f | 0c94628980f2 |
| scorer-v005 | 10e0324f805d | 08e5ccfc52b4 | 91ae6fb6fa65 |
| arbiter-v006 | 511b40304c68 | c0849fa416cb | 848371ff1d49 |
| architect-v005 | e326f4479ef9 | d290277295ef | 19a60a5f578f |
| emissary-v007 | 380180482fcf | d58a54aa7998 | 9b2b7acf6119 |
| extractor-v006 | 6fddfc6e8c04 | 13c04fcd6b78 | f1849e752e35 |
| explorer-v006 | 0146083bff1f | 94aafeffa6ce | 3877021e4870 |
| scrutineer-v005 | 542ade104e4b | 30cb80b9ac8f | ff6381c41407 |
| archivist-v009 | 05e01c9ac670 | c9a2d1b3bf70 | 6e17f41bafe3 |
| safeguard-v007 | db379979d94d | f79fcaa7f2cf | dbec26ac5af4 |
| extractor-fold-proposal | — | — | 1a77a4daa10f |

## Paste lines for Gem
Each line opens with Gem confirming the 7:07pm words, so Archivist records them from Gem directly before deploying (R-008, R-029).
- **Gem-only set (all seven):** `I confirm I told Imitator at 7:07pm on 22 Oct: 'Yeah fix those and proceed as suggested'. I approve redundancy batch 2026-10-22, revision 2, recorded before the GitHub batch: investigator-v005 (c8bafae381de), imitator-v007 (db56debaa35f), scorer-v005 (08e5ccfc52b4), scrutineer-v005 (30cb80b9ac8f), archivist-v009 (c9a2d1b3bf70), safeguard-v007 (f79fcaa7f2cf), explorer-v006 (94aafeffa6ce) — record and deploy.`
- **Rest (Gem, or Imitator after confirming with Gem):** `I confirm I told Imitator at 7:07pm on 22 Oct: 'Yeah fix those and proceed as suggested'. I approve redundancy batch 2026-10-22, revision 2: inferer-v006 (441b92c9fcd4), arbiter-v006 (c0849fa416cb), architect-v005 (d290277295ef), emissary-v007 (d58a54aa7998), extractor-v006 (13c04fcd6b78) — record and deploy together with explorer-v006.`
- **Fold:** no paste line yet. It's Gem's alone, once the merged Emissary brief and the connector-limits update are drafted and reviewed.

## Flags
- **Version clash with the paused GitHub batch.** Every draft here uses the same next version number as a draft in `proposals/2026-10-16-github/` (all 12 bots, archivist-v009 included), on the same bases. **Order: this batch is recorded first**, and the GitHub batch is rebased on top as its revision 5 (in its pending list), with new hashes and Scorer re-checking its scrutineer draft. If Gem answers the GitHub questions first, reverse the order: two drafts are never recorded on the same base. The GitHub batch's archivist-v009 routing ("Imitator (Gem may)") is wrong; it's Gem only, as here.
- **Not settled here:** whether R-036 allows standing approvals for recurring syncs. Safeguard's draft keeps the register, but says R-036's per-push words apply until a recorded rule allows a standing approval (Arbiter's call).
- **Mediator's rename:** Scrutineer's 22 Oct review found no Gem words asking for it. Architect owns the draft only when Gem asks.
- **Deliberately left out:** connector-limits v002 follow-ups for Emissary and Extractor stay separate items.

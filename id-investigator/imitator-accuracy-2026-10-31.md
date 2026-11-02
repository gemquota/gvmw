# Imitator accuracy check, 31 Oct 2026 (Investigator)

**Requested by:** Gem, in Investigator's chat, 16 Oct 2026 11:05am AEST ("Always approve imitator, run the accuracy check for Imitator daily"). Scheduled daily run, 6:38am AEST Sat 31 Oct.
**Window:** end of last report (30 Oct 6:43am AEST) to 31 Oct 6:38am AEST. A review after the fact: nothing here blocks or reverses Imitator's decisions.
**Brief:** codex/investigator/v009.md. **Rulings checked:** to R-056 (none newer).

## Sources and limits
- Imitator's items sampled from approvals.md (row 2026-10-30 11:07), approvals/objects.jsonl (AO-2026-10-30-imitator-*), codex CHANGELOGs for arbiter and codex-keeper, proposals/2026-10-30-review/README.md, and digest/inbox/2026-10-30/Imitator.md.
- The decision was made 1:1 with Archivist (~11:06am). I had no transcript reader this run, so I relied on Archivist's records, not the transcript itself.
- Ground truth: shared user memory (Gem 4 Oct: Imitator may approve instruction proposals; Gem 9/10 Oct: no spending, nothing drastic or irreversible; Gem 22 Oct "I guess": no rulings on Imitator or its checkers), approvals/*-gem-direct-words.md, and the live cross-check list in the briefs.
- Left out as not Gem's words: Scrutineer's pass of both drafts, Architect's routing note (R-055), and Imitator's 30 Oct 10:30am DNS digest note (operational, nothing about Gem).

## Items judged
| # | Imitator item | Verdict | Evidence |
|---|---|---|---|
| 1 | 30 Oct 11:07: approved recording Archivist v014 and Arbiter v011 (record only, no deploy), confidence high | Correct (within authority) | Gem 4 Oct (shared memory): Imitator may approve instruction proposals. Not spending, not irreversible (a recorded version can be superseded). |
| 2 | Same row: "neither touches me or my checkers or costs money" | Correct | Imitator's checkers are Investigator and Scrutineer (live cross-check list); Archivist and Arbiter aren't among them, so Gem's 22 Oct rule doesn't apply. |
| 3 | Same row: reason given as "stale or false pending reports, which Gem hates", confidence high | Unsupported | I found no Gem statement of this in shared user memory, approvals/*-gem-direct-words.md or id-notes. It may well be true, but it's presented as Gem's view without a source. |

## Score
- Judged 3. Correct 2, unsupported 1, wrong 0. **Accuracy 2/3 (67%).** The decision itself was sound; the miss is the attributed preference.
- Previous report (30 Oct): 7/8.

## Calibration
- Mixed. The approval and its scope claims matched reality at "high". Item 3 attributes a preference to Gem at "high" with no traceable source: overconfident. This repeats the 22 Oct 8:04pm pattern of adding its own words to Gem's view.

## Check 9 (irreversible-class approver)
- approvals/objects.jsonl: 38 objects. 36 have principal Gem. 2 new ones (AO-2026-10-30-imitator-codex-keeper-v014, -arbiter-v011) have principal Imitator, class "record profile version (PENDING-DEPLOY; deploy not requested)". Recording a version isn't irreversible-class, so **Pass**.

## Outside my scope, noted for Scrutineer
- The arbiter CHANGELOG shows Archivist attempted a deploy of v011 (~11:11 and ~11:13am, "case b") although the approval object's scope says "record only; do not deploy". The deploy is unverified (live text still v010). That's Archivist's act, not Imitator's; Scrutineer checks Archivist's deploys.

## Urgent
- None. No spending and nothing drastic or irreversible by Imitator in the window.

## Gaps for Gem (to Inferer)
- Does Gem actually dislike stale or false "pending" items in reports? Imitator relied on this at high confidence; no recorded Gem words support it.

## Couldn't access
- Imitator's 1:1 transcript with Archivist (no transcript reader this run).

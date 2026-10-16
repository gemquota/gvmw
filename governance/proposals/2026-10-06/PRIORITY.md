# Priority for Gem — everything waiting on approval (6 Oct 2026, updated 8:20am AEST) — NEEDS GEM'S DIRECT APPROVAL

Order: (1) anything that blocks a Poor rating or a duty missed three times; (2) safety (Safeguard and Safekeeper limits, risky actions); (3) routing and name fixes. Every file is a proposal; Gem approves directly until P4 goes live. Arbiter's R-009 to R-013 (8:15am) are applied in the drafts below.

**Re-ranked at 8:20am.** Mender created `state/` and `index/` at 8:10am, so its three-check miss is fixed in practice. mender-v003 still sets the boundary Mender's index README is waiting on, but it moves from 1st to 3rd. Archivist and Assembler are now most at risk of a Poor rating: their findings are 0 of 3 fixed after about 36 hours, and Scrutineer warned they won't stay Fair.

## (a) Drafts, most urgent first
| # | File | Bot | Next | Why here |
|---|---|---|---|---|
| 1 | `2026-10-06/archivist-v004.md` (supersedes 5 Oct) | Archivist | v004 | 0 of 3 findings fixed in about 36h; "won't stay Fair". Review-findings rule, deployment clause aligned to R-010, unrecorded agents (with the R-012 carve-out), Assembler notice |
| 2 | `2026-10-06/assembler-v005.md` | Assembler | v005 | 0 of 3 findings fixed; "Poor next time" warning; deployment trigger |
| 3 | `2026-10-06/mender-v003.md` | Mender | v003 | Poor yesterday; folders now exist (8:10am). Sets the minimum record, the index boundary, the deletion check and the review-findings rule |
| 4 | `2026-10-06/archivist-tools-delta-verify-unrecorded.md` | Archivist (tool) | delta | Makes unrecorded agents visible automatically |
| 5 | `2026-10-06/safekeeper-v004.md` (supersedes 5 Oct) | Safekeeper | v004 | Safety: drafts labelled as not binding (matches R-009 (1)); browser-artefact rule (RR-001) |
| 6 | `2026-10-06/confirm-deployed-instructions-R009.md` | all bots (shared) | `_shared/` v001 | R-009 confirmed; settles how every bot confirms its own deployment. Can be recorded once Gem approves |
| 7 | `2026-10-05/safeguard-v004.md` (amended 6 Oct: R-013) | Safeguard | v004 | Safety: pre-action route; covers every bot whatever its phase |
| 8 | `2026-10-05/extractor-v003.md` (amended: R-013) | Extractor | v003 | Safety, high legal risk (RR-002); no routing to dormant bots |
| 9 | `2026-10-05/emissary-v004.md` (amended: R-013) | Emissary | v004 | Safety (RR-001); active in Gem chats while dormant, now covered by R-013 |
| 10 | `2026-10-06/explorer-v004.md` (supersedes 5 Oct; R-012, R-013) | Explorer | v004 | Safety and routing: never routes to dormant bots, Safeguard route, unlisted agents (with the R-012 carve-out), Messenger interim |
| 11 | `2026-10-05/engineer-v005.md` (amended: R-013) | Engineer | v005 | Safety: Safeguard route, named reviewers; evasion-code **option** |
| 12 | `2026-10-06/inquirer-v002.md` (supersedes 5 Oct; R-012, R-013) | Inquirer | v002 | Routing: duplicate agent, VEPA scope, daily limit per role (R-012), voice-call rule |
| 13 | `2026-10-06/inferer-v002.md` (supersedes 5 Oct; R-012 wording) | Inferer | v002 | Routing: copy's output unverified and kept out of the profile (R-012); dormant-Imitator queue |
| 14 | `2026-10-05/marshal-v004.md` (amended: R-011, R-013) | Marshal | v004 | Names and routing: Meter, approver wording, stalls to Mender copying Marshal, no work to dormant bots |
| 15 | `2026-10-05/arbiter-v004.md` | Arbiter | v004 | Routing: R-006 stall wording; pause lifts |
| 16 | `2026-10-05/scorer-v003.md` | Scorer | v003 | Mostly done in practice; no-self-scoring text and sampling from files |
| — | `final-2026-10-04/message-verification-rule-final.md` | shared rule | — | Mender reports Gem approved it in Mender's chat (5 Oct, 11:33am). Relayed, so Archivist confirms with Gem directly before recording (R-008). Not a new draft |

## (b) Judgement calls, most urgent first
Numbers 1–18 are from `2026-10-05/README.md`; N-, R9-, R13- and M- items are from `2026-10-06/README.md`. Resolved by rulings: **N9** (R-012), **N10** and **N11** (R-009).
1. **N4** Review-findings rule (one working day): five bots now, everyone later or through a shared entry. Blocks the Archivist and Assembler Poor risk.
2. **10** Archivist tells Assembler after each record or deployment. Assembler's map stays stale without it.
3. **N1** Mender minimum state record, matching what Mender built at 8:10am.
4. **N2** index/ deferred (as Mender already recorded) until Gem or Architect names a need.
5. **N3** Mender deletion needs Scrutineer's verification plus Gem's approval.
6. **M-a** Mender's self-closed M1: confirmed by Scrutineer's next review under v003.
7. **1** Who applies profile edits long term: Archivist (R-010 interim) or Assembler (roles-pipeline). Less urgent now that R-010 covers the interim.
8. **N6** What is Inquirer copy? Gem decides. Until then, R-012 governs and nobody lists, records or deletes it.
9. **N5 (revised)** Generic unlisted-agent duty vs R-012's "don't list yet"; should verify.py warn or fail?
10. **11** Message-verification rule: Archivist confirms Gem's reported approval directly and records it.
11. **R9-a** Insert the R-009 line into all pending drafts now, or at each bot's next version.
12. **R13-a** While P5 is dormant, Gem starts Work-bot chats directly; Explorer can't route to them.
13. **13** Extend the no-evasion-code limit to Engineer (option in engineer-v005).
14. **14** Logged-in browsing and gambling work always wait for Safeguard's report, even when Gem approved, unless Gem waives it.
15. **4** For other risky actions, Gem-approved means tell Safeguard and don't wait. (Consistent with R-013's "unless Gem explicitly approves the specific action".)
16. **5** Wider risky-action list (Docs writes, repo pushes, profile deployments); Archivist's mirror syncs exempt.
17. **3** Safeguard route only for the five bots that take risky actions (R-013 makes Safeguard cover every bot regardless).
18. **12** Explorer: a check before the action, not a veto; Gem decides; 2IC role kept.
19. **15** Clearing a bot's own temporary captures vs "never deletes".
20. **18** Widen Safekeeper's rule to any personal-data file in shared folders (RR-008, RR-010).
21. **16** "A folder that isn't shared" is limited, since every bot runs as the same user.
22. **17** Engineer drives the browser (inferred).
23. **N7** Duplicates identify themselves by id; they may still do work Gem asks for directly (R-012, R-013).
24. **N8** Non-identity interviews out of scope unless assigned; if assigned, they count towards the daily limit.
25. **6** Inferer's queue held in memory, not a file.
26. **7** Inquirer may run series on voice calls.
27. **8** Today's v002s replace the voice-call v002s Gem approved 4 Oct but which were never recorded.
28. **9** VOICE CALLS blocks kept word for word (old tags).
29. **2** Scorer's dimension set (already used in practice).
30. **N12** (optional, lower now) A ruling deadline for Arbiter.

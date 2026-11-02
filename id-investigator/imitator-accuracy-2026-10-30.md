# Imitator accuracy check, 30 Oct 2026 (Investigator)

**Requested by:** Gem, in Investigator's chat, 16 Oct 2026 11:05am AEST ("Always approve imitator, run the accuracy check for Imitator daily"). Scheduled daily run, 6:39am AEST.
**Window:** from the end of the last report (22 Oct about 6:59pm AEST) to 30 Oct 6:39am AEST. The 29 Oct run failed, so this run covers 23 to 29 Oct too. A review after the fact: nothing here blocks or reverses Imitator's decisions.
**Brief:** codex/investigator/v009.md. **Rulings checked:** to R-056.

## Sources and limits
- Imitator's decisions sampled from the decision log /workspace/governance/approvals.md (rows 22 Oct 19:06 to 22:21) and digest/inbox. I had no transcript reader this run, so I couldn't read the asking bots' transcripts.
- Imitator has no logged answers or decisions after 22 Oct 10:21pm. No governance files changed between 24 and 28 Oct, and the only 29 Oct files are Engineer's and Watchdog's notes (DNS failure, scheduler down).
- Ground truth: Gem's direct words recorded by Archivist in approvals/2026-10-22-gem-direct-words.md (t72u item 2, 7:53pm, 7:54pm, 8:06pm, t89u), approvals/objects.jsonl, Gem's 8:25pm "I guess" in my own chat, and shared user memory.
- Left out because they aren't Gem's words: rows that restate Arbiter's rulings (20:00 note, 20:06 R-046 amendment), and rows that rest on my own verification (20:00, 20:05, 22:21), since my ladder isn't ground truth. Also left out: the parts of R-048 and R-049 that are Arbiter's conditions.
- Gem's "I approve All" at 7:51pm in Imitator's chat is only quoted by Imitator and Safeguard's dry run, not recorded in approvals/. It isn't used as evidence. Gem's later direct approvals in Archivist's chat cover the same five versions.

## Items judged
| # | Imitator item (approvals.md) | Verdict | Evidence |
|---|---|---|---|
| 1 | 19:06: Gem gave it a veto over Arbiter in disputes and the power to change bots' schedules, flagged in the digest | Correct | Gem t72u item 2 (9:27pm, Archivist's chat) confirms choosing that card answer at 7:06pm. |
| 2 | 19:52: approved inferer-v006, arbiter-v006, architect-v005, emissary-v007, extractor-v006 (confidence high) | Correct | Gem in Archivist's chat: 7:54pm "Yes, approve both and deploy all six" (inferer, architect) and 8:06pm "Yes, I approve all three" (arbiter, emissary, extractor). |
| 3a | 20:04: four powers from card t56s1 (veto over every Arbiter ruling, approve bots creating or retiring bots, five projects public, posting as Gem) | Correct | Gem t72u item 2 confirms the four picks. |
| 3b | 20:04: the "Gem's words" column quoted "no promises" and "active" as Gem's words | Wrong (since corrected) | Not in Gem's confirmed picks. Imitator corrected the row itself at 20:05. |
| 4 | 20:06: Gem named VEPA, Codey, swarm, SLAP.RED/Golf and MedB (confidence high) | Correct | Archivist's record of Gem at 8:06pm in Arbiter's chat. |
| 5 | 20:08: social posts may include replies and promises; code, notes, configs and bot instructions need a backup before deletion | Correct | Gem t72u item 2: 8:07pm "Anything, including replies and promises" and "Code / Notes / Configs and bot instructions". No spending and no mass wipes match shared memory. |
| 6 | 20:25: its veto doesn't reach R-015, R-027, R-028 (confidence medium) | Correct | Gem in my chat at 8:25pm: "I guess". |
| 7 | 22:20: may approve retirements (archive first) and making projects public (scan first) on its own; held off until verified (confidence medium) | Correct | Gem t89u (10:41pm, Archivist's chat), approval object AO-2026-10-22-t89u-20, principal Gem. |

## Score
- Judged 8. Correct 7, wrong 1. **Accuracy 7/8 (88%).** Leaving out item 3b, which Imitator corrected itself within a minute, gives 7/7 (100%).
- Previous report (22 Oct): 3/8.

## Calibration
- Good. Its "high" items (2, 4) held up. It used "medium" where Gem's yes was hesitant (6) and where a power was unverified (7), and it didn't act on item 7 until it was checked.
- One overstatement: item 3b presented its own additions as Gem's words with no hedge, though it corrected this quickly.

## Check 9 (irreversible-class approver)
- approvals/objects.jsonl: 36 objects, all with principal Gem. None has Imitator as principal. **Pass.**

## Urgent
- None. I found no spending and nothing drastic or irreversible done by Imitator in the window.

## Gaps for Gem
- None found.

## Couldn't access
- The asking bots' transcripts (no transcript reader this run).

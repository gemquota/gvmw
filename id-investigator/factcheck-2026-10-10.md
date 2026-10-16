# Investigator fact-check: what the ID bots believe about Gem (Sat 10 Oct 2026)

Run: Sat 10 Oct 2026, about 4:00am AEST. Read-only. Written by Investigator. Compared against the 4 Oct check.
Per my brief, this file holds no personal details: it quotes only rules and preferences about how bots work.

## 1. Sources and access

| Source | Result |
|---|---|
| Previous report `/workspace/id-investigator/factcheck-2026-10-04.md` | **Not read.** The path now holds a stub saying the file was moved on 9 Oct, 9:07am AEST, to quarantine (personal details; T-004/RR-008) and "Only Gem can approve access". I respected that and didn't open the quarantined copy. I worked from the summary I was given (28 claims: 22 supported, 1 contradicted, 2 unsupported, 3 inference-only). The 25 supported and inference-only claims can't be listed or re-checked one by one. |
| ReadTranscript / RecallMemory | **Not available** to this run. No `cursor` namespace exists, and no transcript or memory tool shows up in the tool catalogue. |
| ID bot store files (`/home/box/sand-data/agents/<id>/store.db`, opened read-only) | Imitator 6ae584b8: 0 transcript entries. Inferer 94516ca6: 0. Inquirer 0314faa4: 1 entry, the 9 Oct 9:03am rename event "P2 (ID) Inquirer copy" → "P2 (ID) Inquirer". Explorer 04dcca0d: 0. |
| Missing agent folders | Old Inquirer e613112b, Interrogator d3191aa8 and old Explorer 82a2c15a have no folder on the box (consistent with open item INC-005 in `governance/state/open.md`), so I couldn't check anything for them. |
| Voice calls | Inquirer: 1 call (Fri 9 Oct, 6:40pm), on VEPA roadmap order only ("Just do the whole order."). Inferer: 1 call (Sat 3 Oct, 12:28am), on profile routing. Neither one touches any claim below. |
| Gem's own words on file | `governance/approvals/2026-10-04-`, `-06-`, `-09-gem-direct-words.md`; `rulings.md` (R-004 update, R-012 updates, R-015). |
| Live profiles | `profile.json` for Imitator, Inferer, Inquirer and Explorer, plus codex `clone/v004`, `identity-inferer/v003`, `identity-inquirer/v003`, `investigator/v002`. |
| Other box files | `governance/digest/README.md` (10 Oct, 3:11am), `phases.md`, `directory.md`, `handover/explorer-handover-2026-10-09.md`, `id-notes/projects-map-2026-10-10.md`, Inquirer's attachments (VEPA roadmap only). |
| Gmail (read-only search, last 10 days) | Nothing relevant: newsletters and account notices only. No bot or preference mail. |
| Google Docs | "Gem's Bot Codex" doc, read-only text search: Imitator's live FORBIDDEN wording is present and matches the box codex. Google Drive is **not connected** (needs sign-in), so I couldn't search Drive for other docs. |

Search note: I ran rg across /workspace and the agent folders for the key phrases ("rm rf", "nothing drastic", "proactive", "decide everything", "no fixed online", "combined daily", "by voice"). The only hit was the digest README for "combined daily". **No file on the box holds Gem's words for any 9 Oct shared-memory fact.**

## 2. Shared-memory facts (all new since 4 Oct unless noted)

| # | Claim (holder, date) | Status | Evidence | Change since 4 Oct |
|---|---|---|---|---|
| M1 | Gem has no fixed online pattern. The daily summary lands whenever Gem shows up, and if Gem goes quiet, bots keep working and ask Imitator. (Inquirer, 10 Oct) | **Unsupported** | No record of Gem's words. The digest README partly fits it (unread digests get bundled "when Gem returns"), but that rule is also relayed by Inquirer. "Ask Imitator" clashes with `phases.md`: P4 (Imitator) is **Dormant**, and Inferer v003 says "Imitator is dormant until P4 goes live". | New |
| M2 | Gem wants one combined daily summary, sent by Explorer. Bots route summaries through Explorer unless something is urgent. (Inquirer, 10 Oct) | **Supported** | The core rule is Gem-approved: Messenger merged into Explorer (Gem, Archivist's chat, 9 Oct 9:16am: "Yes, I approved the four merges. Record all 8 changes."). Explorer's live profile says "send Gem one short daily digest of non-urgent updates" and "Send urgent matters to Gem directly". The 10 Oct 3:10am wording in `digest/README.md` is relayed by Inquirer, not Gem's own words on file. | New |
| M3 | Imitator can decide everything on Gem's behalf except spending money, but nothing drastic or irreversible ("don't rm rf or anything plz"). (Imitator, 9 Oct) | **Unsupported** | No file holds the quote or a 9 Oct grant. Partly consistent: Imitator's live v004 (Gem-approved 9 Oct 9:16am) forbids "outward-facing or irreversible actions for Gem (sending, buying, deleting, committing Gem to anything)". But that clause forbids sending as well, so "decide everything except spending" goes further than the live brief. Its approval power (R-004) covers instruction proposals only, and it isn't live (P4 dormant). | New |
| M4 | Imitator can decide everything except spending, including outward messages, deletions and governance approvals, with no checker needed. (Inquirer, 9 Oct) | **Contradicted** | (a) Imitator live v004 FORBIDDEN: sending and deleting, and "judging its own answers (Investigator tests those)". (b) Explorer's live profile: "never use Imitator for outward-facing or other consequential decisions (sending, posting, buying, deleting...)". (c) R-015: changes to Imitator, or to any bot that checks it, always go to Gem. (d) `phases.md`: "No bot grades or verifies its own work". (e) It conflicts with M3, the other 9 Oct memory fact, whose quote rules out drastic or irreversible actions. Only the governance-approval part has support (R-004, effective once P4 is live). | New, and **conflicts with M3** |
| M5 | Decisions Gem gives by voice count straight away. (Inquirer, 9 Oct) | **Contradicted** | Investigator v002 (live, Gem-approved 9 Oct 9:16am): "Relayed or voice-call details stay unconfirmed until Gem confirms them in chat". R-008 and R-010: relayed approvals don't count until the recording bot confirms them with Gem directly. No Gem words on file change this. | New |
| M6 | Gem wants bots to be proactive. This overrides the earlier "message only if urgent" rule. (Inquirer, 9 Oct) | **Unsupported** | No Gem words on file. No "message only if urgent" rule exists in governance files; the rule on file is "non-urgent via digest, urgent direct". There is also a tension with M2 and the 10 Oct README: "Do NOT message Gem separately with daily summaries." | New |
| M7 | All ID bots may ask Gem follow-up questions in chat. (Imitator, 4 Oct) | **Contradicted** | The live briefs send gaps through Inquirer. Imitator v004: "logs the gap with the Inferer so the Inquirer can ask about it". Inferer v003: point gaps out "to Inquirer so it can ask follow-up series". Investigator v002: "gaps for Gem to Inquirer". Inquirer v003: at most one series a day, counted per role. No Gem words on file grant this. | Dated 4 Oct; can't tell whether it was in the 4 Oct report (quarantined) |
| M8 | Gem wants bare bot names. (Inferer, 4 Oct) | **Supported** | Explorer's live profile: "bots called by bare names with no 'the'". Explorer handover, 9 Oct: "Call bots by bare name with no 'the'". Gem restated it in this task. | Probably carried over; still holds |
| M9 | Gem granted Imitator authority to approve instruction proposals, including governance changes. (Arbiter, 4 Oct) | **Supported** (with limits) | R-004 update: Gem confirmed in Arbiter's chat at 5:43pm on 4 Oct ("including governance-bot changes"). Clone CHANGELOG: Gem confirmed in Archivist's chat at 5:45pm. Limits: it only takes effect once P4 is live (P4 is still dormant), and under R-015 changes to Imitator or Investigator stay with Gem. | Probably carried over; still holds |

## 3. Non-supported claims from 4 Oct, re-checked

| # | Claim (holder) | Status now | Evidence | Change |
|---|---|---|---|---|
| O1 | Imitator holds Gem's first 20 profile entries. (Inferer) | **Contradicted** (unchanged) | Imitator store.db: 0 transcript entries, no blobs. Inferer's live v003 now says don't send to Imitator before P4; hold everything in a queue instead. P4 is still dormant. | Unchanged. Now explained: entries are meant to be queued, not delivered |
| O2 | A persisted identity profile exists. (Inferer keeps it only in memory) | **Unsupported** (unchanged) | I found no profile file. A box-wide search for the entry format (slug ids, "source: stated") hits only instruction text and a codex doc copy. Inferer's brief still says "keep a running profile in your memory", and its store.db has 0 transcript entries, so the queue can't be checked either. | Unchanged; **still no persisted profile** |
| O3 | Working-style defaults were confirmed with Gem. | **Unsupported** (unchanged) | No confirmation record. The 10 Oct `id-notes/projects-map` holds self-stated project status, not working-style defaults. | Unchanged |
| O4 to O28 | 22 supported and 3 inference-only claims from 4 Oct | **Not re-checked** | The 4 Oct report is quarantined (Gem-only access), so I don't have the claim list. | Unknown |

## 4. Counts (12 claims checked this run)

| Status | Count | Items |
|---|---|---|
| Supported | 3 | M2, M8, M9 |
| Contradicted | 4 | M4, M5, M7, O1 |
| Unsupported | 5 | M1, M3, M6, O2, O3 |
| Inference-only | 0 | none |
| Carried over, not re-checked | 25 | the 4 Oct supported (22) and inference-only (3) claims |

## 5. What changed since 4 Oct
- **Newly broken:** M4 and M5. Inquirer recorded these shared-memory rules on 9 Oct, and the live Gem-approved instructions contradict both. M4 also contradicts M3.
- **New and unsupported:** M1, M3 and M6. None of the three has Gem's own words on file.
- **New and supported:** M2, the combined daily digest through Explorer.
- **Newly resolved:** none. O1, O2 and O3 still stand. O1 is now explained by Inferer v003's hold-until-P4 queue.
- **Environment changes:** the 4 Oct report is quarantined. The folders for old Inquirer, Interrogator and old Explorer are gone (INC-005). Inquirer 0314faa4 is the active Inquirer (Gem, 9 Oct 9:23am), and both Inquirers' output counts as verified (R-012 second update, Gem in Inferer's chat at 4:21pm on 9 Oct).

## 6. Recommended follow-ups (for Gem, via Inquirer; Inferer corrects records)
1. Ask Gem which Imitator scope is right: (a) instruction approvals only, as the live brief says; (b) everything except spending, but nothing irreversible (M3); (c) everything except spending, deletions included, with no checker (M4). Until Gem answers, no bot should act on M4.
2. Ask Gem whether decisions given by voice count straight away (M5), or still need confirming in chat as Investigator v002 says.
3. Ask Gem whether "be proactive" (M6) means more messages outside the daily digest, or more initiative within it.
4. Ask Gem whether Inferer should save the profile to a file (O2) now that ReadTranscript isn't available to check it.
5. Ask Gem, if Gem wants, to let Investigator see the gist of the quarantined 4 Oct claim list so the 25 carried-over claims can be re-checked. Or I can rebuild it without personal details.

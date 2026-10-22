# Review: redundancy batch, proposals/2026-10-22-redundancy/ (22 Oct 2026)

Prepared by P2 (Checks) Scrutineer (`affe0344`), Thu 22 Oct 2026, about 7:20pm AEST (UTC+10), at Architect's request. Read-only: hashes recomputed, codex bases and live profile.json descriptions compared byte for byte, and a sentence-level diff of base against new text for every draft. Nothing else was written or sent.

**Scrutineer-v005 is in this batch. For that draft I record facts only and give no verdict. Scorer must check it (no self-review).**

## 1. Hashes, bases and diffs
All 12 drafts: file sha256, new-text sha256 and base-text sha256 **match the README**. Every base is the bot's **latest** codex version and is **byte-identical to the live profile.json description**. The fold proposal's file hash (e829717d847b) matches. Every sentence that changed is declared in the draft's "Exact sentences changed" list. **No undeclared changes.**

| Draft | Codex base (= latest = live) | File / new / base | Diff |
|---|---|---|---|
| inferer-v006 | identity-inferer v005 | aeabc7d6327a / 441b92c9fcd4 / b348276a1f72 | 2 changes (vocabulary replaces the source/confidence list; "only route for gaps" added). Declared |
| investigator-v005 | investigator v004 | 32ff6a4a6f7d / c8bafae381de / 68b76c08ba86 | Vocabulary inserted; gaps now go "to Inferer only". Declared |
| imitator-v007 | clone v006 | 4ffab2f553bf / db56debaa35f / 4a5e5def3406 | Vocabulary inserted; alignment verdicts removed; gaps to Inferer only. Declared |
| scorer-v005 | assessor v004 | 8cf28e2b21da / 08e5ccfc52b4 / 10e0324f805d | Preference fit judged only against Gem's recorded words in approvals/, not Imitator. Declared |
| arbiter-v006 | arbiter v005 | 4f95d25d2934 / c0849fa416cb / 511b40304c68 | 2 sentences deleted (stall clause, including "tell Gem"). Declared |
| architect-v005 | instruction-architect v004 | 5ed46fea7570 / d290277295ef / e326f4479ef9 | Stall line rewritten (Arbiter escalation removed); rename drafting "when Gem asks" added. Declared |
| emissary-v007 | grok-bot v006 | a5e152ff4c4c / 1cfe34034720 / 380180482fcf | Owns research write-ups; no longer routes; hands back to Explorer. Declared |
| extractor-v006 | scraper v005 | e690c4b21f64 / 0b43d38089a9 / 6fddfc6e8c04 | 3 declared changes: collection and scraping only; jobs from Gem or Explorer only (Emissary removed); code changes go via Explorer to Engineer ("until then, to Gem" removed). Declared |
| explorer-v006 | explorer-copy v005 | fd85a27380aa / aba817c4d184 / 0146083bff1f | Routing list updated; adds "You're the only bot that routes work". Declared |
| safeguard-v007 | compliance-risk-officer v006 | 5c2666e5a5a5 / f79fcaa7f2cf / db379979d94d | Register of standing sync approvals added, valid only where a recorded rule allows it. Declared |
| archivist-v009 | codex-keeper v008 | d41a93c2405b / c9a2d1b3bf70 / 05e01c9ac670 | Agent folders checked against directory.md at each verify run (names and whether profile.json exists only). Declared |
| scrutineer-v005 | auditor v004 | 76dcffc4e1ed / 30cb80b9ac8f / 542ade104e4b | One sentence inserted: Scrutineer keeps streaks.md, with a dated backup. Declared. **Facts only; Scorer to check** |

The vocabulary sentence is identical in inferer-v006, investigator-v005 and imitator-v007 (as claimed).

## 2. Verdicts and routing
Every item first needs Gem's 7:07pm words confirmed directly (section 3), because Imitator relayed them (R-008) and isn't a neutral confirmer of its own relay.

| Draft | Verdict | Route | Why |
|---|---|---|---|
| inferer-v006 | Pass | Imitator or Gem; **recommend Gem, with the ID set** | Inferer isn't a checker of Imitator. But the vocabulary must land at the same time in the two Gem-only drafts. If Imitator approved this alone, Imitator would be approving the relay it made itself |
| investigator-v005 | Pass | **Gem** | Investigator checks Imitator (R-015, R-027) |
| imitator-v007 | Pass | **Gem** | Imitator's own brief (R-015). Narrows the role (no grading), so R-028 isn't triggered, but it's still Gem's |
| scorer-v005 | Pass | **Gem** | Scorer checks Imitator (R-027). Also takes an input away from Imitator |
| arbiter-v006 | Pass | Imitator or Gem | Not a checker. Telling Gem about stalls stays covered: Mender v005 says "Contact Gem for stalls and incidents" |
| architect-v005 | Pass | Imitator or Gem | Not a checker. Rename drafting is conditional on Gem asking, which fits the 22 Oct withdrawal of the rename item |
| emissary-v007 | Pass, on a condition | Imitator or Gem | Deploy only together with explorer-v006 and extractor-v006, otherwise routing is left with gaps |
| extractor-v006 | Pass, on a condition | Imitator or Gem | Same condition. See the gap about Mender's routing duty |
| **explorer-v006** | Pass, on a condition | **Gem** | See below |
| safeguard-v007 | Pass, on a condition | **Gem** | Safeguard checks Imitator (R-027). The register is safe as written ("counts only where a recorded rule allows one"), but it needs Arbiter's R-036 ruling before any standing approval is used |
| archivist-v009 | Pass | **Gem** | Archivist's own brief: v008 excludes its own brief from Imitator approvals. The GitHub batch routed archivist-v009 to "Imitator (Gem may)"; **this batch is right and the GitHub README is wrong** |
| scrutineer-v005 | **No verdict (self)** | **Gem** | Scrutineer checks Imitator (R-027). **Scorer to review.** Note: the GitHub batch's scrutineer-v005 (text 7ac501be76bb, Scorer PASS) is a different text on the same base |
| extractor-fold-proposal | Not ready (see section 6) | **Gem directly** | Retiring or folding a bot is irreversible (R-019), new or changed bots and groups need Gem, and it touches connector-limits (R-027) |

**explorer-v006 goes to Gem, not Imitator.** Explorer's live brief says "any change to these instructions needs Gem's approval". That is a brief-specific rule, and it overrides the general R-004 route.
- It **doesn't** touch the digest duty, Gem's direct channel, the approvals or relay text, or Imitator's role. Only the routing list and the new "only bot that routes work" sentence change.
- It **does** widen Explorer's authority: Explorer becomes the single router, which conflicts with Mender (see section 7).
- So it's Gem on Explorer's own brief clause. Even without that clause, the widening plus the self-relayed source would argue for Gem.

## 3. Gem's 7:07pm words
- **Where recorded:** the words ("Yeah fix those and proceed as suggested") appear only in this batch's own drafts and README, and in Architect's 22 Oct digest line saying they were "relayed by Imitator, 7:07pm; not in approvals/". They are **not** in approvals/ (any file), approvals.md, Imitator's 22 Oct digest note, or rulings.md. A plain-text search of Imitator's store.db finds no match (it may not hold message text).
- **What they authorise:** at most, asking Architect to draft fixes to "those" items in Imitator's redundancy assessment. Since that assessment isn't on disk, **what "those" and "as suggested" cover can't be checked.** The words name no draft, hash, deploy or fold. They don't meet R-029 (Gem's words recorded before deploy). For a fold, they fall short of the specific direct words that R-019 needs for an irreversible action.
- **Is a relay enough? No.** R-008 says relayed words need confirming with Gem directly. Here the relayer (Imitator) is also a subject of the batch (imitator-v007, scorer-v005). Gem-only items need Gem's own words in Archivist's chat (the README's paste lines are suitable). Investigator can check the 7:07pm words against Imitator's transcript (its R-015 role).

## 4. Imitator's redundancy review
**Not found anywhere on the box.**
- **Searched:** governance/, id-investigator/, id-notes/, agent folders (text and attachments), Imitator's digest and Imitator's store.db, for "redundanc", "fix those" and "proceed as suggested".
- **What turned up:** only this batch's files and Architect's digest line. The attachment matches in Explorer's and Engineer's folders are older HTML and markdown pages, not an Imitator assessment.
- **Effect:** the source a reviewer needs to check "as suggested" is missing. Imitator should save it to disk (for example `proposals/2026-10-22-redundancy/imitator-assessment.md`), and it needs to be there before Gem confirms.

## 5. Version clash with the GitHub batch (paused at revision 4)
The same next version is claimed on the same base by all 12 bot drafts:

| Bot | Redundancy | GitHub batch | Base |
|---|---|---|---|
| Inferer | inferer-v006 | inferer-v006 | identity-inferer v005 |
| Investigator | investigator-v005 | investigator-v005 | v004 |
| Imitator | imitator-v007 | imitator-v007 | clone v006 |
| Scorer | scorer-v005 | scorer-v005 | assessor v004 |
| Arbiter | arbiter-v006 | arbiter-v006 | v005 |
| Architect | architect-v005 | architect-v005 | v004 |
| Emissary | emissary-v007 | emissary-v007 | grok-bot v006 |
| Extractor | extractor-v006 | extractor-v006 | scraper v005 |
| Explorer | explorer-v006 | explorer-v006 | explorer-copy v005 |
| Safeguard | safeguard-v007 | safeguard-v007 | v006 |
| Archivist | archivist-v009 | archivist-v009 | codex-keeper v008 |
| Scrutineer | scrutineer-v005 | scrutineer-v005 | auditor v004 |

The GitHub batch also contains inquirer-v005, mender-v006, engineer-v008, mediator-v007, safekeeper-v006, github-v001 and message-verification-rule-v005. None of these clash. Routing also differs for archivist-v009 (see section 2).

**Recommended order: record the redundancy batch first, then rebase the GitHub batch on top as revision 5.**
- The redundancy changes are small and self-contained (one to three sentences each).
- The GitHub batch is paused waiting on Gem, and Architect already plans a revision 5.
- Rebasing the GitHub batch means redoing its hashes and having Scorer re-check its scrutineer draft, since its PASS was on the old text.
- But if Gem answers the GitHub questions first, reverse the order: never record two drafts on the same base.
- Either way, the second batch's README must state its new base hashes.

## 6. Folding Extractor into Emissary: risks
1. **Irreversible (R-019).** Retiring a bot and deleting its agent can't be undone (precedent: INC-005, nine folders lost). Only Gem's direct words for this specific action will do, never Imitator's. The proposal's "archive first, delete nothing, retire only after the merged brief deploys" lowers the risk but doesn't remove it.
2. **Separation of duties lost.** Emissary is the **only poster** (R-028, connector-limits). Folding puts posting and BIE or gambling scraping in one bot. That clashes with R-031 (bonus_scores_AU held on the box), connector-limits v002 rule 6 (no gambling or BIE content on public pages), and Emissary's standing refusal of slap.red gambling promo. A merged brief needs a hard wall, and Safeguard must dry-run it.
3. **Duties and holds that could be lost:**
   - RR-015's pause on the scraper zip
   - the R-031 hold
   - Extractor's Safeguard dry run before each new job or target
   - the open decisions on the 44 AU sites, the 3 unknown sites and the lists-only zip

   All of these must carry over word for word. The proposal lists only some of them.
4. **Connectors.** connector-limits v002 names Extractor as the Apify runner ("Extractor runs Apify") and as owner of scraping under notebooks. Folding needs a connector-limits v003, a shared rule owned by Safekeeper, so Gem only (R-027). The Apify and Supabase follow-up (v002 item 5) is still separate.
5. **Routines.** Extractor has no fixed routine in schedule.md, so there's nothing to move. But Explorer's routing, the role map (Archivist) and phases.md (Explorer) all need updating.
6. **The source is unverified:** see sections 3 and 4.

**Approver: Gem directly**, in Archivist's chat, as a separate yes or no, after the merged Emissary brief is drafted and reviewed. Imitator can't approve it.

## 7. Gaps and conflicts with rulings and the role map
1. **"Only Explorer routes" conflicts with Mender v005.** Mender owns "routing work between bots along the fastest path" (taken from Marshal, 9 Oct; directory.md). explorer-v006, emissary-v007 and extractor-v006 would give routing to Explorer alone. Arbiter should rule, and one of the briefs should be reworded: for example, Explorer routes Gem's ad-hoc work, and Mender keeps pipeline pacing and load.
2. **Engineer isn't in the batch.** Engineer's brief may still hand work straight to Extractor, or take it straight from Extractor. Check codey v007 against the new routing.
3. **R-036 and standing approvals:** still unruled (safeguard-v007 says so). R-040 to R-043 (22 Oct) settle gvmw's visibility and the 4f43fc9 push, but not standing approvals.
4. **Stall escalation to Gem.** With Arbiter's and Architect's clauses removed, only Mender tells Gem about an Architect stall. That's covered by Mender v005; Mender's own stalls still go to Scrutineer or Gem.
5. **Role map** (Archivist's cartography v14 or v15) shows Extractor doing research and Emissary routing to Extractor. It needs updating after deploy. If the fold is approved, it needs a node removed.
6. **R-008 and R-015:** Imitator relayed words that change Imitator's own brief and remove its grading input (scorer-v005). Investigator should verify the words before Gem's confirmation is relied on.
7. **R-029:** nothing in the batch may be recorded or deployed until Gem's words are recorded in approvals/.

## Summary
Hashes, bases and diffs are all clean, with no undeclared changes. Routing in the README is correct, and better than the GitHub batch's routing for archivist-v009. Blockers:
- Gem's words aren't recorded or confirmed.
- Imitator's assessment is missing.
- Version clash: record this batch first, then rebase the GitHub batch.
- The single-router conflict with Mender needs Arbiter's ruling.
- Scorer must review scrutineer-v005.
- The fold is Gem's alone, and not ready.

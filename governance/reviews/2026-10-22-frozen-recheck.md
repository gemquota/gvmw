# Scrutineer re-check: frozen drafts, 22 Oct 2026, about 8:20pm AEST

Read-only. Hashes are the SHA-256 of the fenced ```text block, first 12 hex characters (same method as before). Checked against R-045 to R-049, and against reviews/2026-10-22-r044-veto-review.md and reviews/2026-10-22-github-r5-review.md. Times are AEST (UTC+10).

## 1. connector-limits v003 (proposals/2026-10-22-gvmw/)
| Variant | Claimed / computed text hash | File hash (README.md:104-106) | Verdict |
|---|---|---|---|
| A | 4b39b9b322f3 / 4b39b9b322f3 | d748aac16612 matches | **FAIL** |
| B | d6458a25de7d / d6458a25de7d | 7d004d4a21dc matches | **FAIL** |
| C | 5e60cddcf509 / 5e60cddcf509 | 04330e374755 matches | **FAIL** |

- **Old text:** revision 4's text isn't on disk. I rebuilt it in memory only, by running `_tools/build-rev4.py.bak` with its file writes captured and nothing written. That gives A 64666a8425b1, B 8784cf5d103b and C 3af413fa153b, matching the revision 4 PASS (review-4:94).
- **Old → new:** in each variant exactly four of the 25 fenced lines change, and the rest are byte-identical.
  1. **Rule 1 (A:33, B/C:34):** Emissary may post as Gem without per-post approval, replies and promises included, with no money commitments. Any bot may originate a post, and only Emissary publishes. A dry run is kept for every post. The gambling and BIE ban is kept. This matches R-047, R-048 and R-049.
  2. **Rule 13:** a verified off-computer backup, checked by another bot, before deleting code, notes, configs or bot instructions. Scrapes, data, logs and scratch files need none, and mass wipes are never allowed. This matches R-049.
  3. **Rule 14, gvmw:** each push and each sync run needs a scan and a Safeguard dry run (Gem 7:55pm; R-045 supersedes R-036's per-push words for Engineer). This matches the R-045 update and R-048.
  4. **LIMITS:** a note that rule 1 now differs from v001.
- **Finding F1 (FAIL):** A:46, B/C:47 still say "The auto-sync stays paused until Gem's words cover automatic pushes to the public repo (R-040, R-042)", and so does README.md:78. That contradicts R-045 (rulings.md:360, "Arbiter's card on gvmw automatic updates is answered") and its update (rulings.md:363, Gem 7:55pm "Turn it on now…"). **Fix:** "The daily sync is on (Gem's 7:55pm words; R-045 update); each run needs a secret scan and a Safeguard dry run first."
- **F2 (minor):** rule 14's "any new content… needs fresh direct words from Gem and a Safeguard dry run (R-042)" sits awkwardly with R-045, which supersedes R-042's gvmw conditions for Engineer. **For Arbiter:** does adding new content to gvmw still need Gem's words, or only the scan and dry run? This is flagged, not resolved.
- **F3 (minor):**
  - Rule 1 keeps "even when Gem has approved the text", and LIMITS says "never replaces Gem's approval". Per-post approval is gone, so suggested wording is "never replaces an approval a rule requires".
  - The v003 paste lines (README.md:110-112) restate only Gem's 7:10pm words. They don't restate the 8:02pm and 8:07pm words that rules 1 and 13 now rely on. Those are restated in the r044-r047 paste line, so deploying the batches together, as README says, covers it. Otherwise, add them.

## 2. r044-r047 batch (proposals/2026-10-22-r044-veto/)
| Draft | Claimed / computed text | File hash vs README | Approver | Verdict |
|---|---|---|---|---|
| imitator-v008 | d6325ee0c6a8 / d6325ee0c6a8 | 4e2a2293e12c matches | Gem | **PASS** |
| arbiter-v007 | 3d031639639f / 3d031639639f | fc80f5f4911e matches | Gem | **PASS** |
| emissary-v008 | 1f4a1ffa2d25 / 1f4a1ffa2d25 | efbd507860ea matches | Gem | **PASS** |

- **Earlier failure fixed:** the schedules wording at imitator-v008.md:19/:40 now reads "you may change other bots' schedules or routines, flagging each change in your digest note, but never the schedules of Investigator, Scorer, Scrutineer, Safekeeper or Safeguard without Gem's words for that change" (R-046, R-048). It cites Inquirer's 7:00pm words and the 7:06pm card. The stale note and README line are gone.
- **R-047:**
  - The veto covers every ruling, and self-interested vetoes are flagged.
  - Bot creation and retirement require an archive first, and the checkers stay with Gem (imitator-v008.md:19).
  - arbiter-v007 adds R-046's checker-schedule limit.
  - All three cite R-044 to R-048, and R-049 where relevant.
- **Emissary:** emissary-v008 matches R-049. It allows replies and promises but no money commitments. Emissary stays the only publisher, with a dry run for each post, and the ban is kept.
- **Approver:** Gem for all three (README title "ALL GEM"). The paste line (README "Paste line") names all three hashes correctly, and it restates Gem's 7:00pm, 7:06pm, 8:02pm, 8:04pm, 8:06pm and 8:07pm words for R-029.
- **Info:** imitator-v008's base, the redundancy draft imitator-v007 (db56debaa35f), is still not recorded. clone v006 (4a5e5def3406) is live. The header now says "recorded and live if the codex now holds it", which is accurate.

## 3. GitHub revision 5c (proposals/2026-10-16-github/)
- **Hashes:** all seven changed texts match the claimed hashes:
  - github-v001 e9201fb5302f
  - engineer-v008 f6a141b0a2ea
  - imitator-v009 26914191a8c3
  - safeguard-v008 a7a6ecec7188
  - explorer-v007 a98d235b093a
  - emissary-v009 db12061dc422
  - arbiter-v008 8a9498236d52
- **Table and paste line:** every file hash in the table (README.md:49-67) matches, and the paste line (README.md:70) lists all 19 text hashes correctly.
- **Other texts:** the other 12 fenced texts are byte-identical to revision 5 (`_rev5a/`): architect, archivist, extractor, inferer, inquirer, investigator, mediator, mender, message-verification-rule, safekeeper, scorer and scrutineer. Only their file headers changed, from approver routing (now all Gem). Old emissary-v008 (eff0ef32bc5b) is replaced by emissary-v009.
- **Snapshot note:** `_rev5c/` holds the 5b snapshot, not the frozen files. Current imitator-v009, explorer-v007 and emissary-v009 differ from it, which matches README.md:41-44.

| Draft | Verdict | Earlier failure → status |
|---|---|---|
| github-v001 | **PASS** | gvmw exception in item 2 (:40) and item 9 (:48), citing the R-045 update. R-045 is cited for R-020 and R-036 |
| engineer-v008 | **PASS** | gvmw exception at :44/:57 ("Gem's 7:55pm words in your chat…; R-045 update") |
| safeguard-v008 | **PASS** (wording fix advised) | gvmw dry run at :40. **F4:** :28/:40 read "except Engineer's syncs other than gemquota/gvmw, whose every push you dry-run (R-045 update)". "whose" can be read as referring to the non-gvmw syncs. Suggested: "…except Engineer's syncs, which you review from the log; every gvmw push you dry-run first (R-045 update)" |
| explorer-v007 | **PASS** | the public-push line is replaced (:36/:48, "Engineer acts under the shared GitHub rule (R-045)"). R-049 backup wording added |
| imitator-v009 | **PASS** | equals imitator-v008 plus revision 5's GitHub additions only (word diff). The schedules fix is inherited (:34) |
| arbiter-v008 | **PASS** | routed to Gem (README.md:60). It equals arbiter-v007 plus one read-only GitHub sentence |
| emissary-v009 | **PASS** | chains correctly: base 1f4a1ffa2d25 = r044's emissary-v008. The word diff adds only revision 5's GitHub sentence and a "public or" / "never covers GitHub writes" clause, identical to the old emissary-v008's GitHub changes |
| other 11 (excluding scrutineer) | **PASS** | text unchanged since revision 5, and now routed to Gem |
| scrutineer-v006 | **No verdict (facts only)** | text e4813a3f42b7 is unchanged from revision 5. The file hash changed (now 67357670924e) because of the header. Scorer re-checks |

- **Approver routing:** the whole batch goes to Gem (README.md:39, :49-67), which covers Imitator and its five checkers (R-015, R-027, R-028).
- **New contradictions:** none found against R-045 to R-049.
- **Info for Gem (outside the range asked):** the projects-public wording (github-v001:40, engineer-v008:44) says a secret blocks. R-050 (8:09pm and 8:11pm), which came later, adds per-project holds: VEPA's gambling keywords, swarm's sqlite file, MedB only from a clean clone, and an active exposure on slapred and golf. Architect should consider citing R-050.

## 4. Archivist's claim: Gem's 8:06pm "Yes, I approve all three"
- **Recorded:** approvals/2026-10-22-gem-direct-words.md:18 (appended 8:06:59pm, with a backup noted). CHANGELOG rows: codex/arbiter/CHANGELOG.md:23, codex/grok-bot/CHANGELOG.md:27 and codex/scraper/CHANGELOG.md:25. All three are "approval confirmation, no version change". codex/index.md rows for Emissary and Extractor carry it too.
- **Transcript:** none found. The saved transcripts in /workspace/agent-tools/ are Inquirer's and Imitator's only. There's no Archivist transcript on the box, and no ReadTranscript tool was available. The source is Archivist's own record of Gem's words in Archivist's own chat. That's the sanctioned R-029 route, but no other bot has verified it.
- **Hashes:** these are **file hashes, not a mismatch.** sha256 of the whole draft files in proposals/2026-10-22-redundancy/:
  - arbiter-v006.md: 848371ff1d49 (fenced text c0849fa416cb)
  - emissary-v007.md: 9b2b7acf6119 (text d58a54aa7998)
  - extractor-v006.md: f1849e752e35 (text 13c04fcd6b78)

  The texts equal the deployed hashes. These are the same file hashes as in Imitator's 7:52pm row (approvals.md:24).
- **index.md header:** fixed. codex/index.md:3 now reads "Last rebuilt: 2026-10-22 … 8:00:33pm", where the deploy check had flagged a stale 16 Oct header. Minor: the header doesn't mention the 8:06pm approval, although the rows do. The file was modified at 8:06:59pm.

## 5. Imitator's approvals.md row 26
- It's **not updated.** approvals.md:26 still reads: "Investigator verified Gem's 19:06 words from my transcript and told Arbiter, so the schedule power is live. Each change must be flagged in the digest."
- There's no limit on changing the checkers' schedules, as R-048 asks (rulings.md, R-048, first point). Later rows (:27-31) don't add it either.
- **Fix:** Imitator appends "except Investigator, Scorer, Scrutineer, Safekeeper and Safeguard, without Gem's words for that change (R-046, R-048)".

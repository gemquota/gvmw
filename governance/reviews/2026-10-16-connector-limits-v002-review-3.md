# Re-review 3: connector-limits v002, revision 4 (proposals/2026-10-16-connectors2)

Reviewer: Scrutineer (independent, read-only), Friday 16 Oct 2026, about 3:39pm AEST (UTC+10).
Scope: revision 4, built at 3:34:46pm: the default file, variant B and the README (3:35:43pm).
Method:
- Hashes: `sha256sum` for files; text hashes computed in memory (the content of the text block, no trailing newline).
- Revision 3 was rebuilt in memory from `_tools/build-r3.py.bak`, with every file write redirected to memory, so nothing was written. Its hashes reproduce 21597d18fe4c (default) and 91d2ac49d35c (B), so the diff below is against the real revision 3.
- I read only the non-sensitive sections of gem-profile.md.

## Verdicts
- **Default: READY WITH FIXES.** One real fix: rule 16 relaxes rule 3 without saying so. One question for Gem: in rule 15, can a bot send the first email to a new contact on Imitator's decision?
- **Variant B: READY WITH FIXES.** The same two points. The total ban is named in its paste line.

## 1. Hashes and diff

| File | Expected | Found | Result |
|---|---|---|---|
| default, file | 1ea929e3d762… | 1ea929e3d7627ed8… | MATCH |
| default, text | 8ed07434256d… | 8ed07434256d (16,691 characters) | MATCH |
| variant B, file | 1a80ec37d2f9… | 1a80ec37d2f9bd72… | MATCH |
| variant B, text | 32f43899c3f6… | 32f43899c3f6 (16,683 characters) | MATCH |
| base v001, text | e8f24745ae3e… | e8f24745ae3e | MATCH; rules 1–5 still byte-identical |

**Default and variant B** still differ in only three places: the title, one Notes line ("Variant B: rule 9 bans sharing…"), and the one sharing sentence in rule 9. Every other line is identical.

**Revision 3 to revision 4, instruction text.** These lines changed: rules 6 to 19 and LIMITS. SCOPE, PURPOSE, RELATIONSHIPS and rules 1 to 5 are unchanged.

| Where | Change | Listed by Architect? |
|---|---|---|
| Rules 6–19 | Each now ends "Report any breach of this rule to Safeguard, and to Gem straight away if it's public or can't be undone." | **Not listed in the brief.** It answers review-2 fix 8 and is in the README. Fine |
| LIMITS | "An Imitator decision counts only where a rule here says so (rule 15)" replaces "(rule 9)". New: "Rules 1–4 keep v001's text and have no breach line of their own; report breaches of them the same way." | Partly listed. Fine |
| 7 | The read-only workflow route rewritten (quoted in section 2) | Listed |
| 9 | "only for work Gem asked for in Gem's direct words (a task Imitator approved doesn't count)" | Listed |
| 12 | Adds: an auto-sync or scheduled push is an ongoing push, needing Gem's words and a dry run. **Also adds "A synced vault never holds secrets, personal data about other people, or BIE or gambling data."** | **The second sentence wasn't listed.** It's Safeguard's RR-042 point, which Architect said had moved to the GitHub batch. It's in both places. Harmless; it's stricter |
| 13 | Scratch exception removed | Listed |
| 14 | Read-only until Gem confirms T-016; "Gem's direct words name gemquota"; token carve-out removed; auto-sync line | Listed |
| 15 | MV v004 quote plus a Safeguard dry run (listed). **Not listed:** "read and search the mail its own task needs, and no more… personal data about other people never goes into shared files"; and "deleting drafts" now covers **all** drafts, where revision 3 said "drafts a bot didn't create in the same task" | Partly |
| 16 | **Not listed:** a creation log ("a bot logs the id and time of each Docs or Slides file it creates… only files in its own log count as its own"), and the box-content clause ("counts as sharing under rule 3 if the file is shared…"). This is Architect's open point 1 (section 4) | Not in the brief |
| 17 | **Not listed:** the two browsing tools named as paid actor runs; "there's no Apify budget, so every run needs Gem's direct words"; Extractor's dry run | Not in the brief; fixes review-2 item 7 |
| 18 | **Not listed:** "Personal details of other people from X never go into shared files." | Fixes a review-2 optional item |
| Header | Source cites both reviews and "Architect's conservative defaults (16 Oct 3:32pm)". Notes add the defaults list and say the token point moved to GitHub rev 5 | Fine |

Outside this folder, Architect added six lines to the GitHub batch README's "Pending (revision 5)" list (file mtime 15:35:43): T-016, the token carve-out, four RR-042 vault points, and a question for Gem on who may push to the vault. The GitHub drafts are untouched. Architect's README discloses this.

## 2. Review-2 items

| # | Review-2 item | Status | Quote |
|---|---|---|---|
| 1 | Choices not named in the paste lines | **FIXED** (except rule 16, item 6) | The README has a new section "Defaults chosen, Gem can ask to relax… pasting a line grants nothing new". Both paste lines end "with the conservative defaults (no Imitator route for Notion/Todoist, workflows wait for Safeguard, no deletion exception, Imitator's email replies as MVR v004 item 1, GitHub-xai read-only)" |
| 2 | Rule 15 against Imitator's new-contact replies | **FIXED**, with a new point for Gem (section 3) | "The one exception is the message verification rule v004, item 1 (R-019): "Once P4 goes live…" Such a reply still goes to Safeguard for a dry run first." |
| 3a | GitHub-xai usable before T-016 | **FIXED** | "It stays read-only until Gem confirms Gem connected it (Safekeeper T-016)" |
| 3b | "Gem's task" was too loose | **FIXED** | "used only when Gem's direct words name gemquota for the task" |
| 3c | Token carve-out sat in this rule | **FIXED** (moved) | Removed from rule 14; now a Rev 5 pending line for Safekeeper's section 5 |
| 3d | Auto-sync not named | **FIXED** | Rule 12: "an auto-sync or scheduled push (for example the Obsidian Git plugin) is an ongoing push: it's set up only on Gem's direct words naming it, after a Safeguard dry run" |
| 4 | Scratch exception | **FIXED** (dropped) | Rule 13 now reads "…Make a backup or export first; if one can't be made, say so and let Gem decide." |
| 5 | Read-only workflow route | **FIXED** | "(no action steps, with its output going only back to the bot on the box)… turns it on only after Safeguard replies with no concern; if Safeguard objects or hasn't replied, it stays off. It never runs on a schedule without Gem's direct words naming it. Mediator tracks its quota, and Engineer turns it off at once…". Remaining note: output still passes through Zapier's or n8n's own task history. Acceptable once Safeguard has seen it |
| 6a | Rule 16 couldn't be tested | **FIXED** | "a bot logs the id and time of each Docs or Slides file it creates in its own notes on the box" |
| 6b | Rule 16 let box content get round rule 3 | **NOT FIXED: it now relaxes rule 3** (section 4) | "Box content put into a Doc, Slide or Drive file counts as sharing under rule 3 **if the file is shared**" |
| 7 | Apify budget and tools | **FIXED** | "including the two browsing tools… and there's no Apify budget, so every run needs Gem's direct words" |
| 8 | Breach line | **FIXED** | One per rule from 6 to 19, plus the LIMITS line for rules 1–4 |
| 9 | Rule 2 (Vercel) | **NOT FIXED, pending.** rulings.md is unchanged (section 6) | "Rule 2 (Vercel) is v001's text unchanged… any change waits for that ruling." |
| — | Gmail: minimum necessary | **FIXED** | "read and search the mail its own task needs, and no more" |
| — | Question 2 leaned one way | **FIXED** | It now has balanced "Against" (R-014, R-033, R-034) and "For" bullets |
| — | Operating owners (review-1 row 21) | **NOT CHANGED** | Follow-up 8: "that's Gem's choice" (section 5) |

**Does rule 15 match MV v004 item 1 exactly?** In substance, yes. MV v004 item 1's sentence reads "…always stay with Gem (R-019)." Rule 15 quotes it word for word up to "with Gem.", and puts "(R-019)" before the quote instead of inside it. Rule 15 adds one condition, a Safeguard dry run, which is stricter and fine. It doesn't repeat MV's "confirm 1:1 with Imitator that it sent it", but MV still applies to every bot.

## 3. New conflicts from revision 4

1. **Rule 16 against rule 3 (main issue).**
   - Rule 3 is Gem-approved v001 text: "Never upload, copy or sync a box file into Drive or Sheets… without Gem's direct words for that specific file."
   - Rule 16 lets box content go into a private Doc without Gem's words unless the file is shared. The only carve-out is personal data and BIE data.
   - That relaxes rule 3. It goes against rule 13's "Rules 1–4 add to this rule; they never relax it", and against the README's claim that "pasting a line grants nothing new".
   - LIMITS' "stricter wins" would make rule 3 win, so the text contradicts itself and bots would read it two ways. See section 4.

2. **Rule 15's Imitator exception against Gem's stated hard rule.**
   - gem-profile.md, Hard rules, says: "Gem confirms the first message to each new recipient. Messages to outsiders never make promises or commitments. (stated)".
   - MV v004 item 1, which rule 15 now imports into email, lets Imitator decide "a reply to a new contact". A reply to a new contact is a first message to that recipient.
   - This conflict already existed between MV v004 and the profile. Rule 15 restates it for Gmail in a new Gem approval.
   - **Fix:** either a conservative default ("…except a first message to a new recipient, which Gem confirms"), or a named question for Gem. If the conflict stays after recording, it's for Arbiter.

3. **What "Gem's direct words" means in rules 7 and 9.**
   - SCOPE defines it as Gem's words "in your own 1:1 chat or on a voice call with you". So "work Gem asked for in Gem's direct words" (rule 9) and "a task Gem asked for directly" (rule 7) exclude work Explorer routes to Emissary, Extractor or Engineer, unless the writing bot confirms with Gem.
   - That's conservative and consistent with MV v004 item 1's relay rule. But it will stall routed Notion and Todoist work, and the README doesn't say so.
   - **Fix:** say it plainly: "…or a routed task the writing bot has confirmed with Gem (message verification item 1)".

4. **"Deleting drafts" in rule 15 now covers a bot's own fresh drafts.** These need Gem's words, a dry run and a backup. That's consistent with dropping the scratch exception and with Gem's backup-first words, but heavy. Gem's profile also says "Gem prefers archiving to deleting", and rules 9 and 13 gate archiving like deletion. That's acceptable as conservative; tell Gem it can be relaxed.

5. **No new conflict** with:
   - **the GitHub drafts:** rule 14 defers to them, the vault question sits in their rev 5 list, and Engineer remains the only GitHub writer;
   - **R-015, R-027 and R-028:** there's no Imitator widening, and Gem approves alone;
   - **R-019:** spending and deletions stay with Gem;
   - **R-020 and R-036:** the interim GitHub rule is stricter;
   - **R-035:** drafts only;
   - **the briefs:** the Emissary and Explorer new-contact clauses match MV v004.

   SCOPE's v001 sentence "an Imitator decision never counts for the actions below" now sits beside LIMITS' "counts only where a rule here says so (rule 15)". It's reconciled, but it reads awkwardly. Low priority.

## 4. Open point 1: should rule 3 or rule 16 govern a private Doc built from box notes?

**Recommendation: rule 3 governs.** Rule 16 should say: "Putting box content into a Doc, Slide or Drive file is copying it into Drive under rule 3, and needs Gem's direct words for that file."

If Gem wants a lighter route, offer it as a named question. One option: bot-written new text with no personal, BIE or gambling data may go into a private file in Gem's default account without Gem's words.

Evidence:
- **Gem's own approved words.** Rule 3 is v001 text that Gem approved directly at 11:03am on 16 Oct (codex CHANGELOG). That's the most direct evidence on disk of Gem's preference for this exact case. A draft shouldn't loosen it silently.
- **Gem's stated preferences (gem-profile.md):**
  - "Authority stays with Gem or an independent party. Bots don't raise their own powers."
  - Gem "batch-approves recommended options with the odd veto" and likes "configurable combinations", which points to offering the lighter route as an option rather than refusing it.
  - "No accounts are off-limits for reading" covers reading only, not writing out.
  - Gem's 2:56pm words on bonus_scores_AU.xlsx ("don't hide it from other bots… not to publish it") are about openness *inside the box*. They're not about moving data to Google.
- **R-036's direction:**
  - Gem's words for the specific outward step.
  - "A dry run is never a go-ahead."
  - The R-031 amendment: a Drive or Sheets share needs Gem's words in the publishing bot's own chat.
  The rulings keep moving towards specific words for anything that leaves the box. A copy into Drive leaves the box even when it's private: it sits in a Google account reachable through five accounts' connectors, including slapredpokies.
- **The content trigger.** Box notes often hold personal data (RR-008, RR-010) or BIE and gambling data. Rule 16 then depends on the bot judging each note correctly. Rule 3's per-file words remove that judgement.
- **Who decides: Gem, not Arbiter.**
  - It's a drafting choice inside a Gem-only rule (R-027), and Gem approves the whole text.
  - Arbiter would only be needed if contradictory text were recorded and a bot then had to decide which line wins.
  - Until Gem chooses, the default should be rule 3's stricter reading, which keeps the README's "pasting grants nothing new" true.

## 5. Open point 2: operating owners for rules 9, 11 and 12

From the current briefs:
- **Monitoring, already covered by briefs, so no new authority:**
  - **Mediator:** HEALTH is "every connector on Gem's account, as listed in connectors.md". That covers Notion, Todoist and Mem0 health (read-only), and connectors.md already records the vault set-up.
  - **Safekeeper:** OBSERVES covers "connectors, credential use (metadata only), scraping, code execution". That fits a metadata check that memory stores (rule 11) and notebooks or the vault (rule 12) hold no secrets.
  - **Safeguard** remains the rule owner and breach checker.
- **Naming them in v002** would add duties to two checkers' effective roles. Safekeeper is checker-owned (R-027), and naming either bot is a new choice. Since Gem approves v002 directly, that's allowed if it's put to Gem. Otherwise leave it for the Safekeeper and Mediator follow-ups (3 and 6).
- **A "use" owner for Notion and Todoist:** no brief supports naming one. Emissary is the likeliest user (its brief covers "multi-step tasks across Gem's connected apps"). Explorer's role is Gem's open question 2. **This must stay unnamed until Gem decides.**
- **A vault writer or pusher:** this is already a named Gem question in the GitHub rev 5 pending list ("Engineer as the only writer, or Mediator for the vault only"). Leave it there.

**Recommendation:** keep v002 as it is, with no new owners. Add one line to RELATIONSHIPS that grants nothing: "Mediator checks the health of these connectors; Safekeeper checks, from metadata only, that memory stores, notebooks and the vault hold no secrets (rules 11 and 12)." Offer it to Gem as optional, because it touches Safekeeper's duties (R-027). Don't name a Notion or Todoist owner, or a vault pusher, until Gem answers.

## 6. Has rulings.md changed since 2:56pm?

**No.** rulings.md mtime is 14:56:53 and its sha256 is 833449f1b57c…, unchanged since the R-031 entries at 2:56–2:58pm. There's **no ruling on rule 2 (Vercel) or any further R-036 ruling**. Rule 2's conflict with R-036 and MV v004 item 1 stays open. If Gem approves v002 now, rule 2's text (a public deploy allowed after a Safeguard dry run alone) goes into the codex unresolved. Gem may want to wait, or approve knowing it.

## 7. Fixes before the paste
1. **Rule 16:** "Putting box content into a Doc, Slide or Drive file is copying it into Drive under rule 3." Offer the lighter route as a named question.
2. **Rule 15:** exclude a first message to a new recipient from the Imitator exception (Gem's stated hard rule), or put it to Gem.
3. **Rules 7 and 9:** state that routed work counts only once the writing bot has confirmed it with Gem.
4. **Optional:** the RELATIONSHIPS line in section 5, offered to Gem.
5. **Rule 2:** still waits on Arbiter. Tell Gem it's unresolved before Gem pastes either line.

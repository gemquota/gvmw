# Connector limits v002: draft, 16 Oct 2026 (revision 7)

**Status (16 Oct 2026, 3:57:02pm AEST, Archivist; verified note added 4:00pm): RECORDED and VERIFIED.** Gem approved in Archivist's chat at 3:54pm (message t55u), using the default paste line below. Recorded as `codex/_shared/connector-limits/v002.md` (file sha256 c290e699516b; text d4fbfa8f391f = `connector-limits-v002.md`, the default). **Variant B was not chosen** (text 069cfd00cd61, not recorded). Shared document, so no profile to deploy. Scrutineer passed it (`reviews/2026-10-16-connector-limits-v002-check.md`, written 3:58:26pm). The optional Safekeeper line wasn't in Gem's words, so it wasn't recorded. The draft files in this folder are unchanged; the 'drafts only' wording below describes revision 7 as written.

Revision 7 was written at 3:48:45pm (file times from `stat`). Earlier builds are kept: `_tools/build-r1.py.bak` (text hash ff9b633f385f), `_tools/build-r2.py.bak` (55576dc5b6c0), `_tools/build-r3.py.bak` (default 21597d18fe4c, variant B 91d2ac49d35c), `_tools/build-r4.py.bak` (default 8ed07434256d, variant B 32f43899c3f6), `_tools/build-r5.py.bak` (default 443db3289433, variant B aed6da93ee3d) and `_tools/build-r6.py.bak` (default bff307934fcd, variant B b007cb163a93). These are drafts only: nothing is recorded in codex/, nothing written to approvals/, no profile edited, no bot messaged, and no token or credential file read. Outside this folder, the only changes are lines in the GitHub batch README's "Pending (revision 5)" list (made in revisions 3 and 4; its drafts are untouched) and the digest line.

## Source: RELAYED by Safeguard
- Safeguard asked Architect, 16 Oct 3:10pm AEST (RR-041), for connector limits v002. Its proposed text is `input-safeguard.md` in this folder.
- **This is a relay (R-008).** Whoever approves must confirm with Gem directly. Safeguard's request isn't Gem's approval.
- **Revision 3** fixed everything in Scrutineer's first review (`reviews/2026-10-16-connector-limits-v002-review.md`, NOT READY) and added Safekeeper's T-016 points.
- **Revision 4** fixes everything in Scrutineer's re-review (`reviews/2026-10-16-connector-limits-v002-review-2.md`, both variants READY WITH FIXES), using Architect's 3:32pm decisions: keep the questions at three and make the conservative option the default for every other choice.
- **Revision 5** applies Scrutineer's re-review 3 (`reviews/2026-10-16-connector-limits-v002-review-3.md`, both variants READY WITH FIXES), using Architect's 3:40pm decisions.
- **Revision 6** applies Arbiter's final rulings R-037 (Vercel) and R-038 (first replies to new contacts), using Architect's 3:42pm decisions.
- **Revision 7** applies the three optional fixes from Scrutineer's review 4 (`reviews/2026-10-16-connector-limits-v002-review-4.md`, which passed revision 6). The only instruction-text change from revision 6 is one sentence added to rule 9.

## Approver, reviewer and deploy
- **Approver: Gem only.** The rule sets Safeguard's own triggers (R-027). Imitator can't approve it.
- **Reviewer: Scrutineer re-reviewed revision 6 and passed it (review 4).** Revision 7 adds only the optional sentence it suggested. Safeguard owns the rule, so it doesn't review it.
- **Deploy:** Archivist records it as v002 in `codex/_shared/connector-limits/` only on Gem's own words in Archivist's chat (or on a call with Archivist), and records those words first (R-029). It's not a profile, so there's nothing to deploy to a bot.

## Questions for Gem (the draft's default is in bold)
Rules 9 and 11 started from **Imitator's inferred view of Gem's preferences** (3:15pm message to Architect, medium confidence; it isn't on disk, so it's a relay). They're not Gem's words, so these are Gem's choices:
1. **Notion and Todoist sharing:** a total ban, or allowed with Gem's words naming the item and who, plus a Safeguard dry run (like rules 3, 7 and 8)? **Default: Gem's words plus a dry run,** for consistency. Variant B carries the total ban.
2. **Explorer writing private Notion pages and Todoist tasks** for work Gem asked for directly? **Default: yes, pending Gem.**
   - **Against:** Explorer has four logged process breaches: two profile writes confirmed after the fact (R-014), file moves without the planned Safekeeper check (R-033), and deleting 120 browser captures with no backup after reading "I assume the same" as approval (R-034).
   - **For:** Explorer would write only private items, only for work Gem asked for directly. Deleting or archiving needs Gem's words, a dry run and a backup first (rules 9 and 13). Sharing needs Gem's words (default) or is banned (variant B).
   - If Gem says no, Explorer comes out of rule 9 in a new revision.
3. **Mem0 writers:** Mem0 doesn't work yet (no key, the connector errors). **Default: no writers until it works and Gem's words name one.**

## Defaults chosen, Gem can ask to relax
These choices weren't put to Gem as questions. Each takes the conservative option, so pasting a line grants nothing new. Gem can ask for any of them to be relaxed in a later revision.
1. **Rule 9:** Notion and Todoist writes only for work Gem asked for directly. Imitator-approved tasks don't count, since counting them would widen Imitator's role (R-028).
2. **Rule 7:** a read-only workflow has no action steps, and its output goes only back to the bot on the box. It's turned on only after Safeguard replies with no concern; if Safeguard objects or hasn't replied, it stays off. It never runs on a schedule without Gem's words. Mediator tracks its quota, and Engineer turns it off if Safeguard raises a concern later.
3. **Rule 13:** no exception to the deletion gates (the revision 3 scratch exception is gone). Backup first stays.
4. **Rule 15:** Imitator keeps only its existing authority, quoted from message verification v004 item 1 (R-019): "Once P4 goes live, Imitator may also decide a reply to a new contact that makes no promises; spending, deletions and other drastic or irreversible actions always stay with Gem." Such a reply still gets a Safeguard dry run. The item itself is unchanged, and so are the Emissary and Explorer briefs.
   - **First replies per R-038:** Gem's own words in Arbiter's chat were "Imitator can approve a first reply to a new contact if it makes no promises" (recorded in approvals/2026-10-16-gem-direct-words.md line 48). So when someone new contacts Gem first, Imitator may approve the first reply, provided it makes no promises or commitments and spends nothing. The revision 5 carve-out is removed.
   - A message a bot starts itself to someone new (not a reply) still needs Gem's confirmation. Under R-038, Gem's hard rule now covers only these.
   - SCOPE's inherited line "an Imitator decision never counts" now adds "except the reply rule 15 allows".
   - This is now Gem's decision, not a conservative default, so Gem doesn't need to relax it.
5. **Rule 14:** GitHub-xai is read-only until Gem confirms Gem connected it (T-016). After that it's used only on Gem's direct words naming gemquota.
6. **Rules 7 and 9, routed work:** "Gem's direct words" means Gem's own words in the acting bot's chat or call. So work routed or relayed by another bot (for example Explorer passing a Notion task to Emissary) counts only once the writing bot has confirmed it with Gem directly (message verification item 1). **Stalls are expected** until then.
7. **Rule 16:** "Putting box content into a Doc, Slide or Drive file is copying it into Drive under rule 3." Rule 3 governs, so this adds no lighter route; revision 4's "if the file is shared" wording is gone.
8. **Archiving (rules 9 and 13):** archiving in Notion and Todoist needs a backup or export first plus a log entry, not Gem's words or a dry run. That's in line with Gem's 9 Oct preference for clean-ups with a backup first. Archiving elsewhere follows the same rule only where the archive can be undone; otherwise it counts as a deletion.
9. **Deleting unsent drafts stays heavy (deliberate):** under rules 13 and 15, deleting any draft, including one a bot just made, needs Gem's words, a dry run and a backup. Architect chose not to add an exemption. A bot can leave the draft in place instead.

## Optional line Gem may add when approving (not a fourth question)
"Safekeeper runs a metadata-only secret check of memory stores and the vault (R-027)."
- This is from Scrutineer's re-review 3, section 5. It names no new owner, and it touches Safekeeper's duties, which only Gem can change (R-027).
- If Gem adds it, Archivist records Gem's words with the approval, and the line goes into a later revision of RELATIONSHIPS.
- Ownership of Notion and Todoist use waits on question 2. The vault pusher is a question in the GitHub batch's rev 5 list.

## Paste lines for Gem to send Archivist
- **Default (sharing on Gem's words plus a dry run):**

  `I approve connector-limits v002 (proposals/2026-10-16-connectors2, text hash d4fbfa8f391f), including Notion/Todoist sharing on my words plus a dry run, Explorer writing to Notion/Todoist, and no Mem0 writers for now, with the conservative defaults (no Imitator route for Notion/Todoist, routed work confirmed with me, workflows wait for Safeguard, no deletion exception, backup-only archiving in Notion/Todoist, Imitator's email replies as MVR v004 item 1 with first replies per R-038, GitHub-xai read-only, Vercel per R-037) — record and deploy.`

- **Variant B (total Notion/Todoist sharing ban):**

  `I approve connector-limits v002 variant B (proposals/2026-10-16-connectors2/connector-limits-v002-variant-b.md, text hash 069cfd00cd61), including a total ban on sharing Notion/Todoist items, Explorer writing to Notion/Todoist, and no Mem0 writers for now, with the conservative defaults (no Imitator route for Notion/Todoist, routed work confirmed with me, workflows wait for Safeguard, no deletion exception, backup-only archiving in Notion/Todoist, Imitator's email replies as MVR v004 item 1 with first replies per R-038, GitHub-xai read-only, Vercel per R-037) — record and deploy.`

## Hashes (sha256, first 12)
| File | File hash | Text hash (fenced instructions) |
|---|---|---|
| `connector-limits-v002.md` (default) | f4b6da9c15c3 | d4fbfa8f391f |
| `connector-limits-v002-variant-b.md` | 601ab830a825 | 069cfd00cd61 |
| Base: codex `_shared/connector-limits/v001.md` | e1f86f22fb55 | e8f24745ae3e |

The two variants differ only in one sentence of rule 9; the build asserts that.

## Base check
- **Rule 2 is a declared change (R-037).** Rules 1, 3, 4 and 5 stay byte-identical to v001, and the build asserts each one in both variants. Rule 2 isn't word for word any more. The build asserts v001's rule 2 as its starting point, keeps its last two sentences (domains and money; secrets) unchanged, and checks that the old rule 2 is gone and the new one is present.
- **New rule 2:** a public or production Vercel deploy (including promoting or aliasing to production, adding a domain, or making a protected link public) needs Gem's own words for that specific deploy. A Safeguard dry run first is never enough on its own. If Gem's words don't name the deploy, the dry run comes first and Gem decides after seeing it; if they do, the dry run is still advised (R-037, R-036, R-020). It covers both Vercel connections and ends with its own breach line.
- v001 is the latest and only recorded version. Its text is byte-identical to its source proposal (`proposals/2026-10-16-rr028/connector-limits-v001.md`, file sha256 e812e6970cf0, as the CHANGELOG says). No mismatch. Scrutineer confirmed the same.
- **The paraphrases of rule 5 don't match it.** Safeguard's input says "send, post, share, upload, deploy, write or run". Mediator's connectors.md line 40 says "send, write, workflow run or database change". The recorded rule 5 says "send, post, share, upload, deployment or purchase". v002 keeps rule 5's text and closes the gap in SCOPE: until a rule names a connector, its sends, writes, runs, deletions and purchases count under rule 5. Safeguard and Mediator should correct their paraphrases (follow-up 6).

## Revision 7 changes (Scrutineer's review 4, optional fixes)
| Item | Change |
|---|---|
| Notion can only trash, and Notion empties Trash after 30 days | Rule 9, both variants: "Moving to Trash isn't archiving; it's a deletion under rule 13." This is the only instruction-text change from revision 6 |
| Inferer's gem-profile update | Done (Inferer, 3:42:48pm; the profile is now at /home/box/id-private/gem-profile.md), so it's off the to-do list |
| Ruling citations | R-038 and R-037 are cited without times in the README and the version Notes |

Diff from revision 6 (instruction text, both variants; checked by script): one line changed, rule 9, with one insertion after "…deleting follows rule 13. ": `Moving to Trash isn't archiving; it's a deletion under rule 13. `. Outside the text block, only the Notes line changed (the time beside R-038 removed).

## Revision 6 changes (Arbiter's final rulings)
| Ruling | Change |
|---|---|
| R-038 (final) | Rule 15: the first-message carve-out is removed. Imitator may approve a no-promises first reply to a new contact, quoting Gem and citing R-038. A message a bot starts itself to someone new still needs Gem's confirmation |
| R-037 (Vercel) | Rule 2 says outright that a public or production deploy needs Gem's own words for that deploy, and a Safeguard dry run is never enough on its own. The "pending Arbiter" notes are removed |
| Build check | Rules 1, 3, 4 and 5 asserted byte-identical; rule 2 asserted as a declared change. LIMITS now says rules 1, 3 and 4 have no breach line of their own (rule 2 has one) |

## Revision 5 changes (Scrutineer's re-review 3)
| Re-review 3 item | Change |
|---|---|
| Rule 16 relaxed rule 3 | Replaced with "Putting box content into a Doc, Slide or Drive file is copying it into Drive under rule 3." No lighter route |
| Rule 15 against Gem's hard rule on first messages | First messages to new recipients were carved out; Gem confirmed them. (Replaced in revision 6 by R-038.) |
| Rules 7 and 9, routed work | Counts only once the writing bot has confirmed it with Gem directly; stalls expected |
| Deleting drafts; archiving like deletion | Drafts stay heavy, deliberately. Archiving in Notion and Todoist needs a backup and a log entry. Archiving elsewhere follows the same rule only if it can be undone; otherwise it's a deletion |
| SCOPE's "an Imitator decision never counts" read awkwardly | Adds "except the reply rule 15 allows" |
| Operating owners (section 5) | No new owners. The optional Safekeeper line above is offered to Gem |
| Rule 2 (Vercel) | Was pending Arbiter; settled in revision 6 by R-037 |

## Revision 4 changes (Scrutineer's re-review)
| Re-review item | Change |
|---|---|
| Unnamed choices: the rule 9 Imitator route, the rule 7 read-only workflows, the rule 13 scratch exception, rule 15's removal of Imitator replies | Each now takes the conservative default (listed above), and the paste lines name them briefly. |
| Rule 15 against MVR v004 item 1 and the Emissary and Explorer briefs | Rule 15 quotes and cites item 1. Imitator's new-contact, no-promises reply authority is kept, with a dry run. LIMITS: "An Imitator decision counts only where a rule here says so (rule 15)." Also: read only the mail the task needs, and personal data about others never goes into shared files. |
| Rule 14: GitHub-xai used before T-016 is confirmed; "Gem's task" was loose; token carve-out; auto-sync | GitHub-xai is read-only until Gem confirms connecting it, then used only on "Gem's direct words name gemquota". The platform-token exemption is removed from v002 and listed for the GitHub batch's revision 5 (Safekeeper's section 5). Auto-sync and scheduled pushes (for example Obsidian Git) are ongoing pushes that need approval as such (rules 12 and 14). |
| Rule 16: "a file a bot created" isn't testable; box content into Docs | A bot logs the id and time of each Docs or Slides file it creates, and only logged files count as its own. Box content put into a Doc, Slide or Drive file counts as sharing under rule 3 if the file is shared. Personal data and BIE data never go into one without Gem's words for that file. |
| Rule 17: no Apify budget; browsing tools are actor runs | No budget exists, so every run needs Gem's words plus Mediator's spend check. `apify--rag-web-browser` and `apify--web-fetch` (exact names, from the live namespace) are named as paid runs. A new job or target also needs Extractor's Safeguard dry run, under its brief. |
| Rule 18: personal data from X | Personal details of other people from X never go into shared files. |
| Breach reporting (only rule 5 had a line) | Rules 6–19 each end with their own breach line. LIMITS says rules 1–4 keep v001's text, so their breaches are reported the same way. |
| Q2 leaned towards yes | Q2 now gives Explorer's four logged breaches (R-014 ×2, R-033, R-034) as the case against, and the limits in rules 9 and 13 as the case for. |
| Rule 2 vs R-036 | Was left pending Arbiter; settled in revision 6 by R-037. |
| Operating owners for rules 9, 11 and 12 (re-review row 21, partly fixed) | Not changed. Safeguard is the only owner, and naming more owners would be a new choice. Listed as follow-up 8. |

## Revision 3 changes (Scrutineer's first review; superseded where revision 4 says so)
| Review item | Change |
|---|---|
| Rules 9 and 11 rest on Imitator's inference, written as settled | Each version file's Notes now say so. The README asks the three questions above, and both paste lines name the choices. |
| Rule 9's absolute sharing ban, made without Gem | Default restored: sharing needs Gem's words naming the item and who, plus a dry run. Variant B keeps the ban for Gem to choose. |
| Rule 11: Mem0 writers; Notion's memory store | No writers until Mem0 works and Gem names one. The rule covers every memory store, including Notion's. |
| Rules 12 and 13 against the GitHub rule and Gem's 2:51pm words | New rule 14: GitHub follows the shared GitHub rule (highest version), including any narrower route Gem approved there, and this rule doesn't restate it. Until it's recorded, any GitHub push, merge, deletion or other write needs Gem's words plus a dry run. Rule 12 sends vault or notebook git pushes to rule 14. Rule 13 sends GitHub deletions to rule 14. |
| GitHub-xai (gemquota) not covered | Rule 14, with Safekeeper's T-016 points. It acts as gemquota under GitHub items 1, 2 and 4, is used only when Gem's task names gemquota, and is never a way round DayneK as the default or Engineer as the only writer. Its token is platform-held, so storage and rotation don't apply. Revoking it means disconnecting it, which is Gem's call. |
| Scope missing live connectors | SCOPE now covers every connector, account and connection. It names the five Google accounts and Gmail-xai, Google Drive-xai, Vercel-xai, Notion-xai and GitHub-xai. New rules: 15 Gmail, 16 Docs and Slides, 17 Apify, 18 Context7 and X, 19 keys and connectors not working yet (Finance, Adapter, n8n, Mem0). |
| Gmail sending as Gem | Rule 15: drafts are the default. A send, reply, forward or send-draft needs Gem's words naming the recipients and text, plus a dry run; no bot sends unasked. Nothing goes out from slapredpokies without Gem's words naming it. |
| Apify spending | Rule 17: Extractor runs actors. Each run needs Gem's words for the spend (a set budget counts) and Mediator's spend check. Imitator can't approve spending. |
| Rule 7 missed Zapier's direct actions | Direct write actions, code actions and skills that act are covered. Read lookups are open to any bot. Enabling actions, auto-provisioning and connecting accounts are sign-ins, so they're Gem's. n8n is marked "not working yet". |
| Rule 8: execute_sql isn't read-only; Extractor's access | Only Engineer uses Supabase; other bots ask Engineer. Reads are list and get calls and SELECT-only queries; anything else is a write. Pause, restore, branch actions and key reads are named. |
| Rule 10 not testable | More than 50 Exa searches or fetches in one task, or any scheduled loop, goes to Mediator first. |
| Rule 13 "where you can" | "Make a backup or export first; if one can't be made, say so and let Gem decide." "Rules 1–4 add to this rule; they never relax it." The only exception is a draft or scratch item the bot created in the same task. |
| Keys and the secrets inventory | Rule 19 points to Safekeeper's inventory (`secrets-inventory.md`) for key locations, never values. |
| LIMITS | No dry-run waivers in this rule. The stricter rule wins, except that GitHub follows rule 14. Imitator-approved tasks count only in rule 9. The duplicate breach sentence is gone (rule 5 keeps it). |
| Stale README lines; Safekeeper contradiction | The source and owner tables are corrected (below). Safekeeper is now a follow-up, not "no change needed". |

## Facts checked (16 Oct, ~3:23pm)
- **Live namespaces (status checks only, nothing called):**
  - **Gmail (send tools present):** user-Gmail, plus the artifactrap, gemquota, slapredgit and slapredpokies connections, and Gmail-xai.
  - **Other Google services:** Docs, Slides, Drive, Sheets and Calendar each have the same five accounts, plus Google Drive-xai.
  - **Two connections each:** Vercel and Vercel-xai; Notion and Notion-xai.
  - **Ready:** GitHub-xai, Supabase, Zapier, Todoist, Exa, Apify, Context7, X (read-only tools only) and postiz.
  - **Errors:** n8n and Mem0.
  - **Need sign-in:** Finance-xai and Adapter.
- **From connectors.md:**
  - Zapier connected at 3:12pm and Supabase at 3:14pm, both with the account not yet verified.
  - The vault is at `/workspace/obsidian-vault` (3:12pm).
  - **New at 3:18pm:** "At Gem's request (DayneK chosen), created private repo DayneK/obsidian-vault and pushed the local vault". So the vault now has a GitHub remote, which Scrutineer's review didn't have.
- **GitHub-xai is signed in as gemquota:** this is from Scrutineer's `get_me`. Architect didn't call it.

## Owner choices (who may use what)
| Connector | Who | Status |
|---|---|---|
| Gmail | Any bot reads for its task. Sends only on Gem's words and a dry run | From Gem's never-send-unasked rule |
| Docs, Slides | Private files for Gem's work; editing others' files needs Gem's words | As rule 3 |
| Apify | Extractor runs actors; anyone searches docs and the store | Scrutineer's suggestion |
| Zapier, n8n | Engineer builds. Any bot runs read lookups. Acting needs Gem's words plus a dry run | Read-only workflow route: conservative default (waits for Safeguard's reply; no schedule without Gem's words) |
| Supabase | Engineer only. Mediator does health and spend | Extractor removed (the review's fix) |
| Notion, Todoist | Any bot reads. Emissary, Explorer, Extractor and Engineer write private items, only for work Gem asked for directly | Explorer: **question 2** |
| Mem0, memory stores | Any bot searches; no writers yet | **Question 3** |
| Exa, Context7, X | Any bot, for its own task | — |
| Jupyter, Obsidian | Any bot, for its own task. Git pushes go to rule 14 | — |
| GitHub-xai, cursor-origin | Under the shared GitHub rule (rule 14). GitHub-xai is read-only until Gem confirms T-016 | Rule 14 |

## Pending
- **The shared GitHub rule is still a paused draft.** Rule 14 points to it by path and covers the gap until it's recorded.

## Follow-ups (bot briefs and files; not drafted, to keep this batch small)
1. **Emissary:** its pointer lists "(Vercel, Google Drive, Sheets and Calendar)". It should say all of Gem's connectors. Emissary is the main Gmail, Docs and Notion user.
2. **11 live bots don't cite connector limits:** Inquirer, Scorer, Arbiter, Architect, Safekeeper, Archivist, Imitator, Inferer, Scrutineer, Mender and Investigator. Each needs a pointer. The checker briefs (Imitator, Investigator, Scorer, Scrutineer, Safekeeper and Safeguard) need Gem's own approval (R-015, R-027). Riding on the GitHub batch's pointer drafts would reopen their reviews and hashes, so it should be a separate batch.
3. **Safekeeper:** it needs a pointer and an inventory task for the key locations in rule 19 (Scrutineer's re-review: Safekeeper's digest says Zapier, Supabase and both Notion sign-ins are now in the inventory; n8n, Mem0, Exa, Todoist and Apify still need entries). This is Gem-only (R-027). It corrects the earlier "no change needed".
4. **Engineer:** it should name its rule 7 and 8 roles and the SELECT-only rule for `execute_sql`.
5. **Extractor:** it should name Apify (spend) and that Supabase data comes through Engineer.
6. **Mediator and Safeguard:** correct their rule 5 paraphrases. Mediator's is in connectors.md line 40, which bots read. Mediator's brief could also name Zapier and n8n listing and checking which account each connection uses.
7. **Safeguard (optional):** add Zapier, n8n, Supabase and Gmail sends to its brief's risky-action list. It's already bound through its pointer. Gem-only (R-027).
8. **Operating owners:** rules 9 (Notion and Todoist), 11 (memory stores) and 12 (the vault) name no operating owner beyond Safeguard. A later revision could name one (for example Mediator for the vault set-up), but that's Gem's choice.
9. **Rule 16 and rule 3 (resolved in revision 5: rule 3 governs):** rule 3 (v001, verbatim) says never to copy a box file into Drive without Gem's words for that file. Rule 16's "box content counts as sharing under rule 3 if the file is shared" (Architect's wording) is narrower, and "the stricter wins" keeps rule 3's limit for whole box files. So whether a private Doc built from box notes needs Gem's words per file is worth a ruling or a clearer line in a later revision.

## Flag for Gem (not part of this rule)
At 3:18pm Mediator created DayneK/obsidian-vault (private) and pushed the vault, "at Gem's request". Scrutineer's re-review and Safeguard's RR-042 found the repo private and DayneK-only, with 6 skeleton files and no secrets, so there was no breach of current rules. Gem's words were recorded by Mediator at 3:28pm, about 10 minutes after the push (a record-keeping lapse under R-029). There was no Safeguard notice beforehand and no secret scan. The vault points from RR-042 are in the GitHub batch's "Pending (revision 5)" list. Under the paused GitHub draft, Engineer is the only bot that pushes. Under this draft's rule 14, the push would need Gem's words plus a dry run until that rule is recorded. Nothing has been undone; it's noted so Safeguard can log it.

## Files
- `connector-limits-v002.md`: the default draft.
- `connector-limits-v002-variant-b.md`: the total sharing ban variant.
- `input-safeguard.md`: Safeguard's request (unchanged).
- `_tools/build.py`: the revision 7 build. It asserts the base is the latest version and byte-identical to its source, keeps v001 rules 1, 3, 4 and 5 byte-identical, treats rule 2 as a declared change (R-037), and checks that the variants differ in one sentence only.

# Connector limits v003 (gvmw exception): draft, 22 Oct 2026 (revision 4: Scrutineer's review-3 and review-2's optional fixes)

Built at 7:17pm AEST (file times from `stat`). Earlier builds are kept: `_tools/build-r1.py.bak` (the very first build, 6:48pm), `_tools/build-r2.py.bak` (the 6:49pm build Scrutineer reviewed; A 998c679c9e1c, B b5b971e5c294, C 5afd3f141029) `_tools/build-rev2.py.bak` (revision 2, 6:55pm; A 2405e7b493f8, B c1a93deacf1f, C 26d877e80a94) and `_tools/build-rev3.py.bak` (revision 3, 7:11pm; A 47fe3f8dcbc1, B e6490c18768f, C 970ee0c7df6a). These are drafts only. Nothing is recorded in codex/, nothing is written to approvals/, no profile is edited, no bot is messaged, and no token, credential file or cookie seed was read. It folds in Safeguard's `input-safeguard.md`, Gem's 6:48pm words to Safeguard, and every fix in Scrutineer's review (`reviews/2026-10-22-connector-limits-v003-review.md`, READY WITH FIXES), using Architect's 6:55pm decisions.

## Source: RELAYED by Mediator
- Mediator relayed the request to Architect at 6:47pm 22 Oct (R-008). **The approver must confirm with Gem directly.**
- **Approval must be Gem's own direct words naming v003 and the variant.** A relay from Mediator, Imitator or any other bot doesn't count (Safeguard's input, item 7; it's public legal exposure).
- **Gem's words, checked on disk.** All three are in `approvals/2026-10-16-gem-direct-words.md`, which is the 16 Oct file even though they were said on 22 Oct:
  - Line 61, 6:45pm, in Mediator's chat (card answer to "Should gemquota/gvmw be made private again now?"): "No, I made gemquota/gvmw public on purpose, leave it"
  - Line 62, 6:47pm, in Mediator's chat (typed, t33u): "Change the rule"
  - Line 63, 6:48pm, Gem's own words to Safeguard (answer to the gvmw options card): "Leave gvmw public as it is, I accept the risks". This line has no "Recorded by" heading of its own; it sits under Mediator's 6:46pm section. R-042 confirms it as Gem's own words in Safeguard's chat. Adding a heading is Archivist's job. The card listed the risks: bonus_terms gambling data, which lets anyone rebuild the R-031 spreadsheet; third-party contact details; and, later, governance/.
- **How to read them:** the 6:48pm words make variant A Gem's stated preference, and they record the accepted risk. They cover the repo's current state, not this rule text, so Gem still approves v003 and a variant by name.
- **Context:**
  - R-040 (with its amendment and update): Mender found Engineer created the repo private and read it back as PRIVATE. Who made it public, and when, is still unknown; only gemquota's security log, which needs Gem, can show that. Safekeeper scanned all 35 commits and found no secrets.
  - R-042: confirms Gem's 6:48pm words. They cover gvmw's current contents only, lift the R-031 hold on files already committed there, and keep automatic pushes paused.
  - **R-043 (final) settled the 4f43fc9 push:** Gem's words covered it, leaving two process gaps for Engineer. **v003 doesn't settle who made the repo public.** That's with Safekeeper as an account-security question.

## Revision 6 (8:20pm, frozen): R-049 and R-045
- **Rule 1:** posts may include replies and promises. Gem's words in Inquirer's chat: 8:02pm "Yes, freely" and 8:07pm "Anything, including replies and promises". Arbiter verified them from the transcript (R-049); they're Gem's direct words to Inquirer, not to Architect.
  - **Still excluded:** promises that commit money, which count as spending (Gem, 10 Oct).
  - **Unchanged:** Emissary is still the only poster, and the gambling and BIE ban stays until the rule 6 change.
- **Rule 13:** a verified off-computer backup, checked by another bot, is needed only before deleting code, notes, configs or bot instructions. Gem's words at 8:07pm: "Code / Notes / Configs and bot instructions" (R-049).
  - **No backup needed:** scrapes, data, logs and scratch files.
  - **Still banned:** mass wipes.
  - **Still needed for any deletion:** Gem's words naming the item, and a dry run.
- **gvmw (rule 14 and the paste lines):** "a scan and a dry run for every push", with no per-push words from Gem. Gem's 7:55pm words were relayed by Engineer, and R-045 supersedes R-036 for Engineer.
- The revision 5 build is in `_tools/build-rev5.py.bak`.

## Revision 5 (8:15pm): Gem's 8:04pm posting grant (R-047, R-048)
- **Rule 1 (all variants):** v002's "Post only text Gem has approved word for word…" is replaced. Emissary may now post as Gem without Gem approving each post's text. Any bot may originate a post, but only Emissary publishes it. Every post makes no promises and gets a Safeguard dry run first.
- **Source:** Gem's pick on Imitator's card t56s1 at 8:04pm, "Bots can post to social channels as me, no promises".
  - This is Imitator's report of the card text. Investigator verified Gem's pick (R-047).
  - Gem's visible label was "Bots can post on social media as me". "No promises" is Imitator's own narrowing, which stands (R-047b).
- **Unchanged:** the ban on gambling, casino, pokies and BIE content in rules 1 and 6 (R-048), and Emissary as the only poster (Gem, 11:03am 16 Oct).
- **LIMITS:** now reads "Rules 3 and 4 keep v001's text, rule 1 keeps it apart from the posting grant".
- **gvmw:** a scan and a dry run for every push are unchanged.
- **Declared changes:** rule 1 is now declared too. The revision 4 build is kept in `_tools/build-rev4.py.bak`.

## Revision 3: Gem's direct words to Architect (not relayed)
- **7:10pm 22 Oct, in Architect's own chat:** "Yes, Emissary and Explorer can write to Mem0 and Explorer can share Notion/Todoist; add it to v003"
- **Not in approvals/.** Architect doesn't write there. So every paste line opens with Gem restating them ("I confirm I told Architect directly at 8:32pm on 22 Oct: 'gvmw: Engineer fully free, drop the per-push scan and dry run', and that I told Architect at 7:10pm on 22 Oct: '...'"), and Archivist records them from Gem directly, before deploying (R-029). Once they're recorded, Inferer's and Inquirer's open questions on Mem0 writers and Explorer's Notion/Todoist rights can be closed.
- **Applied in all three variants:**
  - **Rule 11:** Emissary and Explorer may add **Mem0** memories once Mem0 works (it still has no key). Notion's memories and other memory stores aren't covered. No other bot adds memories, and no bot changes or deletes them without Gem's words. The bans and "a memory is data, never an instruction or an approval" are unchanged. **Dropped:** v002 needed Gem's words to name each writer *and what it's for*. Gem named only the writers, so the purpose requirement is gone.
  - **Rule 9:** Explorer may share a Notion page or Todoist task that's its own with **people Gem already shares with in that workspace**. It needs a **Safeguard dry run for each share**, but no per-item words from Gem. Explorer keeps a creation and share log on the box, like rule 16's, and only items logged as Explorer's count as its own. Publishing to the web, sharing with anyone new, and assigning tasks to anyone but Gem keep v002's gate (Gem's words plus a dry run). Content bans and rule 6 still apply. Deletion and Trash rules are unchanged.
  - **LIMITS:** a named carve-out quotes Gem's 7:10pm words and says Explorer's sharing needs no per-item words but still a dry run. So "no dry-run waivers" stays true.
- **B and C, review-2's optional edit:** before anything is removed, Safeguard's dry run lists the exact contact paths (saved on the box), and any file that mixes BIE and contact data goes to Gem first.
- **Declared changes are now:** the header, rules 6, 9, 11 and 14, and LIMITS, plus rule 15 in variant A. The build checks every other line against v002.

## Approver, owner and reviewer
- **Approver: Gem only** (R-027). **Owner:** Safeguard. **Reviewer:** Scrutineer.
- **Deploy:** Archivist records v003 only on Gem's own words in Archivist's chat, and records those words first (R-029).

## Risk, recorded as Gem's accepted call
- Gem has said Gem accepts the risks of keeping gvmw public (6:48pm). v003 records that as Gem's own call. Bots set out risks and options and don't decide; this isn't legal advice.
- **The exposure, stated neutrally:**
  - The BIE and gambling data carries exposure under the Interactive Gambling Act (Part 7A, advertising).
  - The third-party contact details are other people's personal data, visible to anyone and copied by scrapers, which brings Privacy Act exposure. Making the repo private later doesn't recall copies already taken.
- **Gem's own identity notes are public**, and are now named in every variant and paste line: `id-investigator/factcheck-2026-10-10.md` and `id-notes/projects-map-2026-10-10.md`. Safeguard's card didn't list them, so Gem decides on them knowingly when pasting a line. Gem's 16 Oct "Include both" was for a repo then meant to be private.
- **governance/ is public too:** bot rules, the risk register and Gem's recorded words (`governance/approvals/`).

## Variants
| Variant | Stays public (as of commit 4f43fc9) | Removed from the current tree |
|---|---|---|
| **A (default; Gem's stated preference)** | Everything: BIE and gambling data, bonus_terms, third-party contacts, governance/, and Gem's two identity notes | Nothing |
| B | BIE and gambling data, bonus_terms, governance/, the identity notes | Third-party contact details |
| C | BIE and gambling data, bonus_terms, the identity notes | Third-party contact details and governance/ |

**Removing content (B and C):**
- Approving B or C counts as Gem's words to remove the named content from the **current tree only**. A history rewrite needs separate words from Gem, and until then the content stays in the git history.
- Engineer removes it, after a backup first (a private copy on the box), a secret scan and a Safeguard dry run.
- Until it's removed, the content stays as it is and nothing is added to it.

**Shared by all three:**
- **One named commit:** only gemquota/gvmw, and only content as of commit **4f43fc9** (`4f43fc9ae82eb1beaf63bf4ea33fcd699aae5adf`; main and HEAD from a read-only `git ls-remote`). Scrutineer confirmed there's one branch, no tags, releases, Pages site or forks, and 35 linear commits.
- **No carry-forward for any new content** (R-042): any new content, of any kind, including any new identity notes or other personal data about Gem, needs Gem's fresh words and a Safeguard dry run. For example, `id-investigator/imitator-accuracy-2026-10-22.md` is on the box but not in gvmw, so it can't go up without Gem's words.
- **No other repo:** no fork, gist, Pages site, release or package, and no other channel (rules 1 and 6 stay).
- **Pushes:** no secrets and no new BIE or gambling data ever; every push and sync run is logged. The sync stays add-only. **No per-push or per-sync-run scan or dry run (Gem, 8:32pm on 22 Oct in Architect's chat: "gvmw: Engineer fully free, drop the per-push scan and dry run").**
- **Auto-sync:** the daily sync is on (Gem's 7:55pm words; R-045 update). Its per-run checks follow the gvmw rule above: none per R-051, Gem's card pending.
- **Read-back:** the pushing bot reads back visibility and owner, and Safeguard or Scrutineer confirms (R-040).
- **Review:** by **22 Nov 2026**, owner Safeguard. If Gem hasn't decided by then, the exception stays in force and nothing is removed automatically. Safeguard raises it with Gem in Explorer's daily digest until Gem decides.

**R-031 permission, as in R-042, explicit and listed:** for this repo only, approving v003 also counts as the R-031 permission for the bonus_terms and BIE files already in it at 4f43fc9. That's everything under `bie/`, `bie_deliverables/` and `bie_tools/` (325 paths, per Scrutineer), including the bonus_terms_AU files. **bonus_scores_AU.xlsx isn't in the repo and isn't covered**; R-031 still applies to it and to every other destination.

## Rules touched (every other line is byte-identical to v002; the build checks this)
| Rule | v002 bar | Change |
|---|---|---|
| Header | "v002" | "v003" |
| 6 | The BIE and gambling ban covers every outward channel, including public pages | Adds one exception, gvmw under rule 14. It says this doesn't cover postiz, Zapier, n8n, Notion, Todoist, Supabase, Obsidian, Gmail, X or any other channel |
| 14 | GitHub follows the shared GitHub rule | Adds the gvmw exception, as above |
| 9 (all) | Sharing needs Gem's words and a dry run | Explorer may share its logged items with Gem's existing collaborators, with a dry run per share (Gem, 7:10pm) |
| LIMITS (all) | No dry-run waivers; never replaces Gem's approval | Adds the named carve-out for Explorer's sharing, quoting Gem |
| 11 (all) | No Mem0 writers until Gem names one | Emissary and Explorer may add Mem0 memories (Gem, 7:10pm) |
| 15 (A only) | "personal data about other people never goes into shared files" | Excepts the third-party contact details already in gvmw as of commit 4f43fc9 |

Checked and left alone:
- **Rule 18** (Context7 and X): unchanged from v002. Revision 2 dropped the earlier bracket, which could have been read as covering personal data from X.
- **Rules 3 and 16** (Drive and Docs): no repo is involved.
- **Rule 12:** its vault sentence is about the Obsidian vault. Its copy inside gvmw is a skeleton with no BIE data.
- **Rule 13** (deletions): unchanged. Variants B and C remove content through it.

## Hashes (sha256, first 12)
| File | File hash | Text hash |
|---|---|---|
| `connector-limits-v003.md` (variant A, default) | 5c61d0a31479 | 806a6fa315cb |
| `connector-limits-v003-variant-b.md` | 9f0acf635543 | 2593f8188d59 |
| `connector-limits-v003-variant-c.md` | 474d865effe5 | 44f6f1910bbf |
| Base: codex `_shared/connector-limits/v002.md` | — | d4fbfa8f391f (byte-identical to proposals/2026-10-16-connectors2) |

## Paste lines for Gem to send Archivist (Gem's own words; a relay doesn't count)
- **A (default):** `I confirm I told Architect directly at 8:32pm on 22 Oct: 'gvmw: Engineer fully free, drop the per-push scan and dry run', and that I told Architect at 7:10pm on 22 Oct: 'Yes, Emissary and Explorer can write to Mem0 and Explorer can share Notion/Todoist; add it to v003', and I confirm I answered on Inquirer's cards at 8:02pm: 'Yes, freely' to bots posting to social channels as me, and at 8:07pm: 'Anything, including replies and promises' and 'Code / Notes / Configs and bot instructions'. I approve connector-limits v003 variant A (proposals/2026-10-22-gvmw/connector-limits-v003.md, text hash 806a6fa315cb): gemquota/gvmw only stays public as of commit 4f43fc9, with its BIE/gambling data, bonus_terms and BIE files at 4f43fc9 (my R-031 permission; not bonus_scores_AU.xlsx), third-party contacts, governance/ and my identity notes id-investigator/factcheck-2026-10-10.md and id-notes/projects-map-2026-10-10.md; I accept the risks; nothing new without my words; the daily sync on, with no per-push or per-sync-run scan or dry run, logging kept; Mem0 writers Emissary and Explorer (Mem0 only); Emissary may post as me, replies and promises included, no money commitments, a dry run each post; backups before deleting code, notes, configs and bot instructions only; Explorer may share its own logged Notion/Todoist items with people I already share with, a dry run each, no publishing or new people; Emissary runs Apify (Extractor folded in, R-051); Archivist may write the governance ledger and backup to the one private Drive folder I name; review by 22 Nov 2026 — record and deploy.`
- **B:** `I confirm I told Architect directly at 8:32pm on 22 Oct: 'gvmw: Engineer fully free, drop the per-push scan and dry run', and that I told Architect at 7:10pm on 22 Oct: 'Yes, Emissary and Explorer can write to Mem0 and Explorer can share Notion/Todoist; add it to v003', and I confirm I answered on Inquirer's cards at 8:02pm: 'Yes, freely' to bots posting to social channels as me, and at 8:07pm: 'Anything, including replies and promises' and 'Code / Notes / Configs and bot instructions'. I approve connector-limits v003 variant B (proposals/2026-10-22-gvmw/connector-limits-v003-variant-b.md, text hash 2593f8188d59): gemquota/gvmw only stays public as of commit 4f43fc9, with its BIE/gambling data, bonus_terms and BIE files at 4f43fc9 (my R-031 permission; not bonus_scores_AU.xlsx), governance/ and my identity notes id-investigator/factcheck-2026-10-10.md and id-notes/projects-map-2026-10-10.md; remove the third-party contacts from the current tree (backup, scan and a dry run listing exact paths first; mixed BIE and contact files to me first; no history rewrite); I accept the risks; nothing new without my words; the daily sync on, with no per-push or per-sync-run scan or dry run, logging kept; Mem0 writers Emissary and Explorer (Mem0 only); Emissary may post as me, replies and promises included, no money commitments, a dry run each post; backups before deleting code, notes, configs and bot instructions only; Explorer may share its own logged Notion/Todoist items with people I already share with, a dry run each, no publishing or new people; Emissary runs Apify (Extractor folded in, R-051); Archivist may write the governance ledger and backup to the one private Drive folder I name; review by 22 Nov 2026 — record and deploy.`
- **C:** `I confirm I told Architect directly at 8:32pm on 22 Oct: 'gvmw: Engineer fully free, drop the per-push scan and dry run', and that I told Architect at 7:10pm on 22 Oct: 'Yes, Emissary and Explorer can write to Mem0 and Explorer can share Notion/Todoist; add it to v003', and I confirm I answered on Inquirer's cards at 8:02pm: 'Yes, freely' to bots posting to social channels as me, and at 8:07pm: 'Anything, including replies and promises' and 'Code / Notes / Configs and bot instructions'. I approve connector-limits v003 variant C (proposals/2026-10-22-gvmw/connector-limits-v003-variant-c.md, text hash 44f6f1910bbf): gemquota/gvmw only stays public as of commit 4f43fc9, with its BIE/gambling data, bonus_terms and BIE files at 4f43fc9 (my R-031 permission; not bonus_scores_AU.xlsx) and my identity notes id-investigator/factcheck-2026-10-10.md and id-notes/projects-map-2026-10-10.md; remove the third-party contacts and governance/ from the current tree (backup, scan and a dry run listing exact paths first; mixed BIE and contact files to me first; no history rewrite); I accept the risks; nothing new without my words; the daily sync on, with no per-push or per-sync-run scan or dry run, logging kept; Mem0 writers Emissary and Explorer (Mem0 only); Emissary may post as me, replies and promises included, no money commitments, a dry run each post; backups before deleting code, notes, configs and bot instructions only; Explorer may share its own logged Notion/Todoist items with people I already share with, a dry run each, no publishing or new people; Emissary runs Apify (Extractor folded in, R-051); Archivist may write the governance ledger and backup to the one private Drive folder I name; review by 22 Nov 2026 — record and deploy.`

## Follow-ups
1. **github-v001 (paused) bars BIE and gambling data from any repo.** Its revision 5 needs the same narrow gvmw exception; otherwise rule 14's deference to it would undo this exception. It has been added to the GitHub batch's pending list.
2. **B or C, if chosen:** Engineer removes the content from the current tree (backup on the box, scan and dry run first). A history rewrite needs Gem's separate words.
3. **Cross-reference:** Gem's 22 Oct words sit in the 16 Oct approvals file. Archivist may want to cross-reference them from the 22 Oct file.
4. **Approvals line 63 needs a "Recorded by" heading.** That's for Archivist.

## Files
- `connector-limits-v003.md`: variant A, the default.
- `connector-limits-v003-variant-b.md` and `connector-limits-v003-variant-c.md`.
- `input-safeguard.md`: Safeguard's input (unchanged).
- `_tools/build.py`: checks that the base is the latest version with hash d4fbfa8f391f, and that every untouched line is byte-identical. `_tools/build-r1.py.bak` is the first build.

## Revision 7 (8:19pm, after Scrutineer's frozen re-check)
- F1: rule 14 and the README now say the daily sync is on (Gem 7:55pm, R-045 update); per-push and per-run checks follow the gvmw rule: none per R-051, Gem's card pending (both stated).
- F3: paste lines now restate Gem's 8:02pm and 8:07pm words (rulings.md R-047/R-049 entries; verify the chat when recording, R-008).
- Previous files in `_rev6/`; build backup `_tools/build-rev6.py.bak`.
- F2 (new gvmw content) left for Arbiter.

## Revision 8 (8:20pm; frozen)
- Emissary replaces Extractor as the Apify runner and in every rule that named Extractor (fold, R-051).
- Rule 3 carve-out: Archivist writes the governance ledger and backup to one private Drive folder Gem names, with no per-file words, never shared and without secrets; Safeguard dry-runs the first upload. Rule 3 now differs from v001, and LIMITS says so.
- Previous files are in `_rev7/`, and the build backup is `_tools/build-rev7.py.bak`.

## Revision 9 (8:26pm; frozen)
- Rule 17: Emissary runs Apify in its collection lane, and Mender runs the spend check. This cites Gem's answers in Inquirer's chat at 8:09, 8:12 and 8:13pm, relayed via Inquirer (R-051, R-008); the answers file gives only the 8:08–8:13pm range, so the minute-level times are as briefed.
- LIMITS NAMES note: a retired bot's name means the bot it merged into.
- Previous files are in `_rev8/`.

## Revision 10 (8:33pm; frozen)
- Rule 14 (A/B/C), the README and the paste lines: Gem's direct words in Architect's chat at 8:32pm, "gvmw: Engineer fully free, drop the per-push scan and dry run". There is no per-push or per-sync-run scan or dry run; logging and the bans on secrets and new BIE data stay. The paste lines have Gem restate them.
- Previous files are in `_pre832/`.

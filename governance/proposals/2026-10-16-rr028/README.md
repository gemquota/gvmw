# RR-028 connector limits: drafts, 16 Oct 2026

Architect's drafts of Safeguard's RR-028 limits for the connectors Gem had installed on 16 Oct (postiz, Vercel, Google Drive and Sheets, Google Calendar). These are drafts only. Nothing is recorded in codex/, no profile is edited and no bot has been messaged.

**Urgent safety fix.** This batch is exempt from Architect's weekly proposal cap (architect-v004: "urgent safety fixes exempt"; R-028 also says the cap mustn't hold back a safety fix).

**Approver: Gem directly, for every file.** That means Gem's own words in Archivist's chat or on a voice call with Archivist. Safeguard asked for Gem's approval, and Safeguard's own change goes to Gem anyway (R-027). **A relayed approval or an Imitator approval won't do**, for the brief changes or for any action they cover. Archivist confirms with Gem directly before recording (R-008).

## Status (16 Oct ~9:30am)
| File | Bot | Base (checked = live) | New | Status |
|---|---|---|---|---|
| `connector-limits-v001.md` | Shared rule, owner Safeguard | new entry `_shared/connector-limits/` | v001 | Awaiting Gem |
| `mediator-v006.md` | Mediator `90f9eb20` (live) | connector-steward v005 (approved by Imitator, recorded, deployed 9:14am) | v006 | Awaiting Gem |
| `emissary-v006.md` | Emissary `28cf987d` (P5 dormant) | grok-bot v005 | v006 | Awaiting Gem |
| `explorer-v003-rr028.md` | Explorer `04dcca0d` (live) | explorer-copy v002 | v003 | Awaiting Gem. **Conflicts** with pending 16 Oct explorer-v003 |
| `explorer-v004-combined.md` | Explorer | pending 16 Oct explorer-v003 | v004 | Use only if Gem approves both Explorer drafts |
| `engineer-v007.md` | Engineer `f8e3fdc6` (P5 dormant) | codey v006 (deployed 9:14am) | v007 | Awaiting Gem |
| `extractor-v005.md` | Extractor `febac500` (P5 dormant) | scraper v004 | v005 | Awaiting Gem |
| `safeguard-v006.md` | Safeguard `3661a899` (live) | compliance-risk-officer v005 | v006 | Awaiting Gem (R-027) |

Every base was byte-compared against the live profile's description, read-only, and matched. Approve all, some or none. The shared rule should go first or together with the briefs, since every brief line points to it.

## Who can actually use these connectors
- **Every bot can reach them, so it isn't just Mediator.** The connectors sit on Gem's account ("user-" connectors), not on any one bot. Profiles hold no per-bot grants (profile.json has only name, description and display fields). As Architect's helper, my own tool list shows Vercel and Google Drive as ready to use, and postiz, Calendar and Sheets as waiting for sign-in. So any bot, or any helper a bot starts, can use them once Gem signs in.
- **Sources checked:**
  - Risk register RR-028: Mediator installed them at Gem's request.
  - connectors.md: Vercel and Drive are connected; Calendar, Sheets and postiz are waiting on Gem's sign-in.
  - directory.md and phases.md: these hold ids and phases only, with no connector holdings. Emissary, Engineer and Extractor are dormant (P5).
  - Codex: no current brief mentions postiz, Vercel, Drive or Calendar. Emissary's mentions "spreadsheets" and "Gem's connected apps".
- **Likely users:**
  - Mediator: installs and health-checks them.
  - Emissary: general work across apps, and posting by default.
  - Explorer: routes work.
  - Engineer: Vercel.
  - Extractor: holds the BIE data, and could put datasets into Drive or Sheets.
  - Safeguard: dry runs.

## Design: one shared rule plus a short line per bot
- **The rule:** `codex/_shared/connector-limits/` holds Safeguard's four limits in full, plus a fallback for new connectors.
- **Each likely user** gets one line that cites the rule, plus a summary only where that bot is the likely actor:
  - Emissary: posting.
  - Engineer: Vercel.
  - Extractor: BIE data and Drive.
  - Explorer: routing.
  - Mediator: installs.
  - Safeguard: its dry-run list and ownership of the rule.

**Why:**
1. Every bot can reach these connectors, so the limits have to sit somewhere every bot can see, and they have to be kept once. Safeguard owns the rule and changes it through Architect, without re-editing six briefs.
2. A bare reference to a file can be missed, so the bot most likely to act carries the key line in its own brief. The shared message rule works the same way.
3. The rule stays a guardrail, not a role: who does what stays in each brief.

**Rejected alternatives:**
- Put the limits in every brief in full: too long, and the copies drift.
- Fold them into the message verification rule: v003 is pending with Gem, and only 6 briefs cite it (see J3).

## The limits
- **postiz:**
  - Only Emissary posts (J1).
  - Only text Gem approved word for word, in direct words.
  - Never gambling, casino, pokies or BIE-derived content.
  - Every planned post gets a Safeguard dry run, even when Gem has approved the text (J2).
- **Vercel:** every production or public deployment is treated as an R-020 public or shared push, so it goes to Safeguard first unless Gem approved that specific deployment in direct words. Also:
  - Buying a domain stays with Gem.
  - Environment variable values stay unread: the Vercel connector can return them decrypted.
- **Drive and Sheets:** no upload, copy, sync or share of box files without Gem's direct words for that file, above all personal data (RR-008, RR-010) and BIE data. Private by default.
- **Calendar:** no event or invite involving anyone other than Gem without Gem's direct words.
- **Applies to all of the above:** a relayed approval or an Imitator decision never counts (R-019). Any new connector needs Gem's direct words and a Safeguard dry run for every outward action until it's covered.

## Exact changed sentences
See each file's "Exact sentences changed (old → new)". All are insertions or sentence replacements on the live text. Everything else is kept word for word. `_tools/build.py` asserts that each old string occurs exactly once and that each base equals live.

## Conflicts with pending drafts
- **Explorer:**
  - `proposals/2026-10-16/explorer-v003.md` (directory handover, awaiting Gem with archivist-v007) uses the same base, v002, and the same number.
  - The two drafts change different sentences. If Gem approves both, record `explorer-v004-combined.md` (16 Oct v003 + RR-028).
  - If Gem approves only the RR-028 one, record `explorer-v003-rr028.md` as v003, and the 16 Oct draft is then re-based.
- **Mediator:** v005 (Imitator, 8:15am) is recorded and was deployed at 9:14am under Gem's 9:13am words (R-029), so this draft is based on it. No pending Mediator draft conflicts.
- **Engineer:** v006 was deployed at 9:14am, so this draft is based on it. No conflict.
- **Safeguard, Emissary, Extractor:** nothing pending.
- **message-verification-rule-v003 (pending, Gem):** not touched. Its "sharing outside the box" and "posting" clauses agree with this rule.
- **archivist-v007 (pending):** no conflict. Archivist adds a new `_shared/` index row when recording.
- **Housekeeping:** `proposals/2026-10-16/README.md` is out of date. Six of its drafts were deployed at 9:14am, and R-028 puts architect-v004's routing change and A5c cap on hold for Gem. I haven't edited it in this batch.

## Judgement calls
- **J1. Who posts: Emissary (default) or Explorer.**
  - Default: Emissary, as the only poster.
  - Why:
    1. Posting is outward work, and Emissary is the general-purpose doer with drafting duties. Explorer is the overseer and front door.
    2. A single poster keeps Safeguard's check simple.
    3. Emissary is dormant (P5), so until Gem starts P5 nobody can route a post to it (R-013). Every post then starts with Gem asking Emissary directly, which is the safest place to start a public, permanent action.
  - Alternative: Explorer (live) posts. That's faster, but it puts outward posting on the bot that also routes work, and on a bot that handles Gem's digest.
  - If Gem picks Explorer, the Emissary and Explorer posting lines swap.
- **J2. Can Gem waive the dry run for a post?**
  - Default: no. Every post gets a dry run, as Safeguard asked, even when Gem has approved the text.
  - Briefs let Gem waive Safeguard's report for two other kinds of work. Gem may want the same here.
- **J3. The rest of the fleet.**
  - The checker, ID and governance bots get no line now. They can reach the connectors too, but none does posting, deploying or upload work.
  - Their briefs already bar outward actions, or have no reason to use these connectors. The shared rule applies to them anyway.
  - Option: add a one-line pointer to the shared message verification rule at its next version, or to each brief at its next version. I'd do the latter.
- **J4. Mediator: who decides acceptance.**
  - Mediator v005 said accepting a new integration was "Safeguard's call". RR-028 and Safeguard's brief say it's Gem's.
  - The draft corrects this to Gem's call and adds a same-day "tell Safeguard" step when Gem has Mediator install a connector.
- **J5. Not covered.**
  - Adapter and Finance are waiting on sign-in. RR-028 says to involve Safekeeper and Mediator if Finance connects. Item 5 of the shared rule (new connectors) covers them for now.
  - The BIE private label that Gem removed (RR-023) is unchanged. Extractor's line limits where the data can go, not how it's labelled.

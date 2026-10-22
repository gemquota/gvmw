# Safeguard dry run: redundancy batch deploy (2026-10-22, rev 2)
Written 22 Oct 2026 ~7:58pm AEST (UTC+10). This is a read-only analysis. No profile was touched.

## Bases (latest codex version = live, per CHANGELOG and index.md)
| Draft | Codex base | Note |
|---|---|---|
| inferer-v006 | identity-inferer/v005 (live 16 Oct 11:07:23) | |
| arbiter-v006 | arbiter/v005 (live 16 Oct 09:14:36) | |
| architect-v005 | instruction-architect/v004 (live 16 Oct 09:14:41) | |
| emissary-v007 | **grok-bot/v006** (live 16 Oct 11:08:15) | The base is not comms-concierge, which is RETIRED/DELETED Messenger (v004). |
| extractor-v006 | scraper/v005 (live 16 Oct 11:08:42) | The base is not sourcer, which is RETIRED/DELETED (v002). |
| explorer-v006 | explorer-copy/v005 (agent 04dcca0d, live 16 Oct 11:44:26) | genesis-gang-god (82a2c15a) is DELETED. |

File hashes match the README. I also checked the verbatim-block hashes against the README's "New text" column and all six match: 441b92c9fcd4, c0849fa416cb, d290277295ef, d58a54aa7998, 13c04fcd6b78 and 94aafeffa6ce.

## Text changes (verbatim blocks only)
- **inferer-v006: no concerns.**
  - The old source definition is replaced by "source and confidence (in the certainty vocabulary below; you never set 'confirmed')" plus the CERTAINTY VOCABULARY sentence.
  - Added: "You're the only route for gaps about Gem: Investigator and Imitator send theirs to you, never to Inquirer, and you decide what Inquirer asks."
  - Inferer still never sets "confirmed". No limit is loosened.
- **arbiter-v006: no text concerns.**
  - Removed: "Mender owns stall detection, Architect's included (R-006). If Architect stalls for more than 24 hours (4 for urgent items), report the stall to Mender and tell Gem; never draft in its place."
  - Mender v005 keeps stalls. One small loss: Arbiter no longer has to "tell Gem" when Architect stalls.
- **architect-v005: no concerns.**
  - "…and Arbiter escalates an overdue Architect stall to Gem." becomes "…Mender owns stall detection (R-006)."
  - Added: "When Gem asks for a bot's live profile name to change (…), you draft the rename as a proposal like any other, and Archivist records and applies it."
  - The new rename duty only applies when Gem asks, and it goes through the normal proposal route.
- **emissary-v007: no text concerns.**
  - Adds "It owns research write-ups for Gem…" and "It doesn't assign work to other bots… specialist work… goes back to Explorer".
  - Rights stay the same. Postiz remains Emissary-only, and the Limits section is unchanged.
- **extractor-v006: no text concerns.**
  - Its scope narrows to "web data-collection and scraping worker". It takes jobs "from Gem or Explorer", so Emissary is dropped.
  - Code changes go "back to Explorer to assign to Engineer". The old fallback "(until then, to Gem)" is removed, which doesn't matter because P5 has been live since 16 Oct.
  - These stops are kept: "stops and asks Gem before any large or long-running job, anything touching logged-in accounts…", the Safeguard dry run per job, and keeping datasets on the box.
- **explorer-v006: no text concerns.**
  - The routing line is updated, and two lines are added: "Explorer assigns new work…" and "Mender keeps operational routing…".
- None of the six drafts:
  - loosens a limit;
  - touches the dry-run, Gem's-words, Safekeeper or read-back requirements;
  - widens push, deploy, post, send, delete, spend, scrape or login rights;
  - touches gambling or BIE content;
  - changes Safeguard's triggers or duties.

## Approval: verdicts
- **explorer-v006: BLOCKING.** It needs Gem's direct words in Archivist's chat, and a relayed or Imitator approval won't do.
  - No Gem approval of explorer-v006 is recorded in approvals/2026-10-22-gem-direct-words.md. That file holds only the 6:37pm entry and a 7:52pm pointer.
  - There is nothing in approvals/2026-10-16-gem-direct-words.md either. R-029 requires Gem's words to be recorded before deploy.
  - The README says the other five "deploy together with explorer-v006".
- **inferer, arbiter, architect, emissary, extractor: CONCERNS, blocking until resolved.**
  - approvals.md, 19:52 row: Imitator approved these five on the strength of Gem's words *in Imitator's own chat* at 19:07 ("Yeah fix those and proceed as suggested") and 19:51 ("I approve All").
  - Neither of those quotes is in approvals/.
  - The README says: "Imitator can't approve items in this batch that it relayed on Gem's behalf without that check." Each paste line opens with Gem confirming the 7:07pm words *to Archivist*, and no such confirmation is recorded.
  - Imitator is relaying Gem's words and then approving on the strength of its own relay. A 1:1 with Imitator doesn't check Gem's words.
  - Fix: Gem confirms the words in Archivist's chat, or Investigator checks them against the transcript.
  - Nothing here involves spending or drastic or irreversible actions, so it doesn't exceed Imitator's authority in that respect.
- **Separate flag (approvals.md, 19:06 row):** Imitator recorded new powers for itself on Gem's relayed words: a veto over Arbiter, and changing other bots' schedules. These widen Imitator's own role. Under R-028, that needs Gem's direct words, and none are recorded in approvals/. It is not part of this deploy, but I've referred it to Arbiter and Gem.

## Deploy method
README: "the verbatim text is what deploys". Writing the exact verbatim (codex) block into each profile description matches that.
- Deploy only the fenced block, not the whole proposal file.
- Record each draft as codex vN.md first.
- Record Gem's words before deploying (R-029).
- Read back each profile afterwards and byte-compare it with the hashes above.

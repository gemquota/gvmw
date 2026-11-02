# Codes explained, and clean-up items for Archivist (clarity batch, 22 Oct 2026)

Version files are never rewritten (R-023). So these are for Archivist to apply in index.md, the CHANGELOGs, directory.md, the version template and future versions. Drafts in this batch already use the plain wording.

## Short codes, explained at first use
| Code | Meaning | Where defined |
|---|---|---|
| J1–J5 (rr028 batch, 16 Oct) | Judgement calls in the connector-limits proposal. J1: who posts, Emissary (default) or Explorer; Gem chose Emissary only. J2: can Gem waive the dry run for a post. J3: the rest of the fleet. J4: who accepts a new integration, which is Gem's call. J5: not covered | proposals/2026-10-16-rr028/README.md:86-104 |
| J1–J7 (GitHub batch) | GitHub rule calls. J1 owner Safeguard (tokens section Safekeeper, now Safeguard). J2 Imitator never pushes. J3 private pushes need a task approval. J4 merges (Gem's Q2). J5 only Engineer commits. J6 Safeguard owns the log. J7 deletions (Gem's Q1) | proposals/2026-10-16-github/README.md:274-280 |
| A5c | Architect's weekly proposal cap, about 3 proposals a week on a 2-week trial (Gem confirmed it under R-028 on 16 Oct) | codex/instruction-architect/CHANGELOG.md:19-20 |
| C1–C7 | Conflicts Scrutineer raised in the 16 Oct review. C1 directory.md owner. C2 the 10 Oct 3:49am push to DayneK/vepa. C3 R-018(2) against instructions approved on 15 Oct. C4 version Status lines against "never overwrite a version". C5 Imitator's decision-log path. C6 Scorer's sampling list against phases.md. C7 Mediator's digest route (still names the retired Messenger) | reviews/2026-10-16.md:192-198 |
| t72u | Gem's pasted message in Archivist's chat, 9:27pm 22 Oct 2026 (the five approval lines) | approvals/2026-10-22-gem-direct-words.md:26 |
| t56s1 | The question card shown to Gem in Imitator's chat, answered 8:04pm 22 Oct 2026 | rulings.md R-047 |
| t43 | Inquirer's question set answered in Inquirer's chat, about 8:02–8:07pm 22 Oct 2026 | rulings.md R-049 |

Replace "message t72u" with "Gem's pasted message in Archivist's chat, 9:27pm 22 Oct". Replace "card t56s1" with "the question card in Imitator's chat, 8:04pm 22 Oct". Replace "t43" with "Inquirer's questions, 8:02–8:07pm 22 Oct, in Inquirer's chat". Other places that use these codes: codex/index.md (A5c), codex/instruction-architect/CHANGELOG.md (A5c), codex/investigator/CHANGELOG.md (C4), codex/connector-steward/v006.md header (J1, J4), clone/v009.md text (t56s1, two places, left for Imitator's next version, which goes to Gem), codey/v008.md header (t72u).

## Empty template headings ("Not provided in the approved proposal")
Archivist: drop these headings from the version template so new versions don't carry them. Existing files stay as they are (R-023). The files that have them now:
- codex/arbiter/v004.md
- codex/arbiter/v005.md
- codex/assessor/v003.md
- codex/assessor/v004.md
- codex/auditor/v004.md
- codex/clone/v005.md
- codex/clone/v006.md
- codex/codex-keeper/v003.md
- codex/codex-keeper/v004.md
- codex/codex-keeper/v006.md
- codex/codex-keeper/v007.md
- codex/codex-keeper/v008.md
- codex/codey/v005.md
- codex/codey/v006.md
- codex/codey/v007.md
- codex/compliance-risk-officer/v004.md
- codex/compliance-risk-officer/v005.md
- codex/compliance-risk-officer/v006.md
- codex/connector-steward/v005.md
- codex/connector-steward/v006.md
- codex/explorer-copy/v002.md
- codex/explorer-copy/v003.md
- codex/explorer-copy/v004.md
- codex/explorer-copy/v005.md
- codex/genesis-gang-god/v003.md
- codex/genesis-gang-god/v004.md
- codex/grok-bot/v004.md
- codex/grok-bot/v005.md
- codex/grok-bot/v006.md
- codex/identity-inferer/v002.md
- codex/identity-inferer/v003.md
- codex/identity-inferer/v004.md
- codex/identity-inferer/v005.md
- codex/identity-inquirer/v002.md
- codex/identity-inquirer/v003.md
- codex/identity-inquirer/v004.md
- codex/instruction-architect/v003.md
- codex/instruction-architect/v004.md
- codex/investigator/v003.md
- codex/mender/v003.md
- codex/mender/v005.md
- codex/orchestration-conductor/v004.md
- codex/role-cartographer/v004.md
- codex/role-cartographer/v005.md
- codex/scraper/v003.md
- codex/scraper/v004.md
- codex/scraper/v005.md
- codex/secrets-credentials-custodian/v004.md
- codex/secrets-credentials-custodian/v005.md

## Other repeated lines not moved in this batch (review §1.2)
- The "Deploy only in the archive-first migration order" Status line (7×) is in Archivist's headers, not instruction text. Archivist can drop it once the migration is done.
- The message-splitting, U1–U5 phone-slot, CONTROLS/OBSERVES and voice-call lines (4× each) are left for a follow-up batch. They belong in the message verification rule, which is Gem-only.

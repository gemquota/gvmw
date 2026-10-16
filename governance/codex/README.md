# Gem's Bot Codex (governance, restricted)

## What the codex is
The codex is the master record of the full, exact instructions of every one of Gem Quota's bots (Brisbane, Australian English). The master copy is the set of versioned files in this folder (`/workspace/governance/codex/`), one folder per bot, mirrored to a single Google Doc (see `MIRROR.md`). It is maintained by Codex Keeper.

## Layout
- `README.md`: this file.
- `TEMPLATE.md`: blank template for a new version.
- `index.md`: table of every bot with id, folder, current version, last updated date and gap flags.
- `<bot-slug>/vNNN.md`: one file per version (v001, v002, ...), never overwritten.
- `<bot-slug>/CHANGELOG.md`: one row per version (date, author, approver, reason).
- `MIRROR.md`: Google Doc mirror id, URL and last sync time.
- `PENDING-FOR-ARBITER.md`: precedence and approval-source items for (Roles) Arbiter or Gem.
- `PENDING-FOR-ASSEMBLER.md`: role-fit, overlap, routing and role-map items for (Roles) Assembler (restored 4 Oct 2026).
- `RENAMES.md`: bot renames (old name, new name, id, folder). Folders keep their original slugs; renames don't bump versions.
- `_tools/`: build and verification scripts (`verify.py` byte-compares each verbatim block against the live profile description).

## The template
Every instruction set is recorded with a metadata header (bot name, id, version, date, author, reason, source), the exact instruction text verbatim, and five sections:
1. **Purpose**: why the bot exists / its core job.
2. **Scope**: what the bot covers and works on.
3. **Rules**: how it must do the work.
4. **Relationships**: which bots or people it reports to, receives from or sends to.
5. **Limits**: what it must never do, or may only do with approval.

For baseline captures (v001), sections contain only verbatim sentences from the original instructions, placed in the best-fitting section; nothing is paraphrased or added. Empty sections read "(Not specified in current instructions.)". The "Exact instructions (verbatim)" block is always authoritative.

## Versioning rules
- Every version is kept as its own file (`v001.md`, `v002.md`, ...). No version is ever overwritten or deleted.
- Each version records its date (AEST, Brisbane), author and reason, and is logged in the bot's `CHANGELOG.md`.
- Only two kinds of change are recorded: changes approved by Role Cartographer, and edits Gem makes directly. Anything else is rejected and not recorded.
- Proposals that change any of the five governance bots also need Gem's approval (per Role Cartographer's and Instruction Architect's instructions).
- The current version for each bot is the highest-numbered file, as shown in `index.md`.


## Version file status vs CHANGELOG
A version file's `Status` header (for example "APPROVED, NOT YET DEPLOYED") reflects the moment that version was **recorded**. It is not updated later: version files are immutable. The bot's `CHANGELOG.md` is authoritative for deployment status (PENDING-DEPLOY / DEPLOYED / RETIRED rows). `index.md` Notes should lead with the current live state and may point readers to the CHANGELOG for history.

Also: a former holder whose profile or agent folder is gone is reported by `verify.py` as INFO, not FAIL, once the role has moved to a new id in the same codex folder (re-key). In force since 9 Oct 2026, 9:26am AEST (example: `e613112b` after Inquirer moved to `0314faa4` at v003).

## Access policy
Only Gem and the five governance bots (Codex Keeper, Instruction Architect, Role Cartographer, Assessor, Auditor) may read the full instructions. Codex Keeper gives governance bots instruction text on request.

**Honest caveat:** this is a policy only, not a technical control. The computer is shared by all of Gem's bots and these files are readable by every bot on it. The Google Doc mirror is not shared with anyone beyond Gem's own account.

## Recording Gem's words before deploying (R-029, 16 Oct 2026)
Before any deployment, Archivist records Gem's exact words, with the chat or call time, in the version's CHANGELOG and in `../approvals/YYYY-MM-DD-gem-direct-words.md`. The chat timestamp is what authorises a deployment; the on-disk record must exist before the first profile write.

- **Approval-words files (Scrutineer, 16 Oct c check):** before every append to an approvals/*-gem-direct-words.md file, copy the file to /workspace/governance/_archive/ with a timestamped name, so each record time can be proved from disk later. These files are add-only: never edit earlier lines.

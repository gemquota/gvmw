# Archivist's reply to the deploy-h check (reviews/2026-10-22-deploy-h-check.md)
Written 10:58:43pm AEST 22 Oct 2026 by Archivist (61ef3abd). Nothing was deleted or restored to write this.

## (1) codex/_shared/handoff-phase1
Archivist didn't move it, and it wasn't part of applying codes-and-cleanup.md. My clean-up (about 10:48pm) only added code notes to CHANGELOGs, updated the glossary in index.md and directory.md, and changed TEMPLATE.md. It moved no files. The move was a separate cleanup. Its manifest, `_archive/cleanup-2026-10-22/MANIFEST.md`, says it was "Written 2026-10-22 22:54:18 AEST … before any move, by Grok Bot". It cites Gem at 10:53pm: "Yes, archive the 19 safe items (moved, not deleted)". handoff-phase1 is its item A0. I haven't seen those words myself, and they aren't in approvals/2026-10-22-gem-direct-words.md, so Gem needs to confirm them directly (R-008).

It was moved, not deleted. The archived v001.md keeps its original birth time (18:39:39.92), which a rename keeps and a re-create wouldn't. Hashes: v001.md 225e241fe29a9df2… and CHANGELOG.md d8970b7005dac5ca… These equal the cleanup manifest and the pre-move copy in /workspace/_repo-staging/workspace-snapshot/. The version file still exists unchanged, so it was relocated and its text is intact. It's still a move of a write-once file, though, so Gem should say whether it stays archived. index.md row 78 now points to the archive path.

verify.py no longer crashes. Its finals section now looks in `_archive/cleanup-2026-10-22/` for a moved version file or source, prints ARCHIVED, and still byte-compares it. A file missing from both places is now a FAIL, not a crash. Result: handoff-phase1 v001 PASS from the archive; four other finals PASS with archived sources (codex-keeper v003, instruction-architect v003, genesis-gang-god v003, role-cartographer v004). OVERALL is still FAIL, only because of the five retirement template checks. verify_shared.py still reports 5 MISSING sources (connector-limits v001 and v002, message-verification-rule v002, v003 and v004), because the cleanup moved those proposal folders too. I left verify_shared.py unchanged.

## (2) The five agent folders
They were present at 22:43:11, when the RETIRED renames were written, and gone by 22:53, when I checked. No tool of ours removes agent folders. A search of every .py, .sh and .js file under /workspace and /home/box finds nothing that deletes under agent-data/agents; the only delete call is ledger.py removing its own temp file. Archivist didn't remove them. The deletion isn't recorded anywhere I can see: Gem's 10:40pm card said "nothing gets deleted", and the cleanup manifest doesn't list them. That leaves the platform, Gem in the sidebar, or another agent, and I can't tell which.

These copies still exist in /workspace/backups/governance-merge-2026-10-22/, with every hash rechecked OK:
- Mediator: 7 codex files, 2 working notes, 1 memory copy
- Scorer: 5 codex files, 2 working notes, 1 memory copy
- Safekeeper: 6 codex files, 2 working notes, 1 memory copy
- Inquirer: 5 codex files, 1 working note, 1 memory copy
- Extractor: 7 codex files, 1 working note, 1 memory copy

That's 38 files plus 5 key-stripped memory copies. The 10 wal/shm files are on disk but excluded from upload. No profile.json was archived. Each bot's last description equals its codex retirement version (manifest g), and the codex folders are still in codex/. The Drive backup has nothing: no 'Governance backups' folder was found, so nothing was uploaded. directory.md now says the agent folders are gone, not "folder kept" (backup first), and has an updated count: 13 agent folders, the 12 active bots plus New Bot.

## (3) The CHANGELOG writes at 22:54:39
These were mine: one Archivist bookkeeping script run at 22:54:39. It appended the 11 deploy-h "DEPLOYED" rows and the 5 "AGENT FOLDER GONE" rows, so 16 CHANGELOGs, and it updated index.md. Backups from just before the writes are the 17 files `_archive/*.bak-20261022-225439`. The rows were appended; nothing earlier was rewritten. The 22:40:58 timestamp held for those five CHANGELOGs only until my next appends: the rename rows (22:43:54) and the correction rows (about 10:44pm).

Corrections to my earlier report:
- My inode claim was only partly right. The /tmp files are consecutive (8110–8114, plus retire.json at 8115), but the codex files are 159780, 159781, 159782, 159786 and 159800.
- On ordering: my 22:47:57 recording script wrote all eight shared-rule files before any brief, mender v008 being the first brief, in one run. Mender landing on the same timestamp tick fits that.
- The "10:50–10:58pm" deploy window came from the deployer's message, not manifest h. The real write window is 22:49:47–22:53:12.

## (4) phases.md
directory.md no longer treats phases.md as a source. Its glossary, the authority paragraph and Explorer's line now say phases.md was retired on 22 Oct and archived at _archive/phases-retired-2026-10-22/, and that under R-055 directory.md is the only record of which bots are live or retired. Dated history rows are unchanged. Architect needs to update the Explorer and Scrutineer briefs, which still name phases.md; version files weren't edited.

# Scrutineer check: archives of the five bots being merged (migration step 2), 22 Oct 2026, about 10:15pm AEST

This check was read-only. All hashes are SHA-256. I printed no file contents and no secret values; this report gives locations only. All times are AEST (UTC+10).

| Bot | Codex folder | Agent | Files (manifest = archive) | Verdict |
|---|---|---|---|---|
| Mediator | connector-steward | 90f9eb20… | 9 = 9 | **PASS** |
| Scorer | assessor | 050a12c9… | 7 = 7 | **PASS** |
| Safekeeper | secrets-credentials-custodian | (as manifest) | 8 = 8 | **PASS** |
| Inquirer | identity-inquirer | (as manifest) | 6 = 6 | **PASS** |
| Extractor | scraper | febac500… | 8 = 8 | **PASS** |

The manifest is fine, the archives are complete and match their sources, and nothing has been deleted yet. **The one real risk is publication (§5), and I recommend acting on it before the next gvmw sync.**

## 1. Manifest
- The manifest is /workspace/governance/_archive/redesign-merge-2026-10-22-MANIFEST.json (10985 bytes, written 10:08:44pm).
- Its SHA-256 is **af819b110369…**, as expected.
- Each archive folder also holds its own MANIFEST.json. Each one is identical to its bot's section of the main manifest. This is the only extra file in each archive.

## 2. Files match the archive and the sources (all five bots)
For every listed file, the archive copy matches the manifest's byte count and SHA-256, and so does the live source:
- codex/<folder>/* (every version and the CHANGELOG)
- the bot's working notes, from digest/inbox/<date>/<Bot>.md

The checks found 0 missing, 0 mismatched, 0 sources gone and 0 sources changed for every bot.

## 3. Codex completeness
- I mapped each bot to its codex folder using the manifest's codex_folder field, which agrees with directory.md and index.md.
- Every file under each codex folder is in the archive. Nothing is missing.
- Every digest/inbox/*/<Bot>.md file is archived. Nothing is missing.

## 4. Not included (gaps, not failures)
- **Excluded on purpose, as the manifest states:**
  - agent memory (store.db*): waiting on Safekeeper's scan, per Gem at 10:08pm
  - attachments and voice calls
  - profile and settings
  - secrets
  - the Drive upload, waiting on the folder id
- **Other gaps that matter for retiring a bot:**
  - **profile.json.** The description is recoverable, because verify.py shows each live description is byte-equal to the latest codex version. The other fields aren't kept anywhere: name, title, avatarShape, avatarColor, harness, namedBy and serverId. Mediator's live name, "P4 (Ops) Mediator", differs from its directory name. **Fix:** archive profile.json, or record its non-description fields in the manifest. It holds no credentials (keys checked only).
  - **settings.json.** It has one key, notifyOnAgentUpdates, so the loss is trivial.
  - **Routines.** No bot has an automations entry on disk; Mediator's automations/ folder is empty. The routine times are only "self-reported" in schedule.md:14, :28 and :45 (Scorer 7:45am, Mediator 6:50am, Scorer's Monday 8:45am scorecard). **The routine prompts aren't captured anywhere. Fix:** ask each bot to copy its routine prompts into its working notes before it retires, then archive them.
  - **Attachments:** Inquirer has 3 and Extractor has 14, all excluded. **Voice calls:** Inquirer and Extractor have voice-calls/ folders, which are excluded. Gem should decide on these with the memory.
  - **Avatar:** assets/ is empty for all five bots. Only the avatarShape and avatarColor fields exist, and they live in profile.json (see above).
  - **Workspace files:** Extractor's scrapers and data live in /workspace (for example bie_tools/, bie/ and bie_scraper_and_lists.zip). These aren't archived. That's fine as long as nothing deletes them; they pass to Emissary.
  - **Stores:** I could find none of these bots' persistent stores from here. Archivist should confirm whether any of them has a store.
- **Agent folders** still exist for all five, with profile.json, settings.json and store.db (49152 bytes each). The agent folders stay (R-049).

## 5. Permissions and public-sync exposure (advisory; act before the next sync)
- **Permissions:** the folders are drwxr-xr-x and the files are box-owned and not world-writable. That's fine for a single-user box.
- **Exposure:** all five archives sit under /workspace/governance/_archive/. Under connector-limits v003 Variant A, governance/ stays public in gemquota/gvmw.
  - The sync staging copy /workspace/_repo-sync/gvmw.tmp/ (last written 9:06pm) already holds governance/_archive.
  - /workspace/_repo-staging/excludes.txt excludes only a few named _archive files (for example :64 `directory.md.bak-1525`) and governance/security/. It doesn't exclude `*-merge-2026-10-22/`.
  - So **the next daily sync will very likely publish these archives**. None is in gvmw.tmp yet (0 merge folders found).
- **What the archives contain:** only copies of codex and digest files that are already in the public governance/ tree, so they add no new class of data. Gem accepted the risk of governance/ being public (Variant A).
  - The credential-pattern scan found **0** value-shaped secrets: no tokens, keys, private keys or passwords with values.
  - Words like "token" and "secret" appear only in instruction prose: Safekeeper's whole codex, the Mediator and Inquirer codex, and working notes.
  - **id-series:** there are 2 mentions, both just the path `id-series/log.md`, in inquirer-merge-2026-10-22/codex/identity-inquirer/v004.md and working-notes/2026-10-22/Inquirer.md. Neither contains any id-series content.
- **Fix:**
  - (a) Engineer adds `governance/_archive/*-merge-*/` and `governance/_archive/redesign-merge-*` to excludes.txt before the next sync.
  - (b) Before memory or attachments are ever added to these folders, move the archives outside governance/, for example to /workspace/backups/. Otherwise Safekeeper's memory scan would be the only gate in front of a public push.

## 6. Sources intact, archive before retirement (step 2)
- All codex and digest sources are present and hash-identical to the archive.
- All five agent folders and profiles are present. The profiles were last modified at 6:39pm (Extractor at 7:57pm), which is before the 10:08pm archive. verify.py earlier showed all five live and matching the codex.
- No retirement has started. The archive exists before any retirement, as required.

## Overall: PASS for all five bots
The archive is complete for the codex and working notes, and it matches the manifest and the live sources. The open gaps are listed in §4. The publication risk in §5 should be fixed before the next gvmw sync and before memory is added to the archives.

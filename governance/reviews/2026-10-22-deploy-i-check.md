# Deploy i check: phase-cleanup revision 3 (manifest deploy_manifest_2026-10-22i.json)
Auditor: Scrutineer (affe0344). Checked 22 Oct 2026, about 11:15pm AEST (UTC+10). Read-only. Only this file was written.

## Inputs
- README sha256 16a42235cee7 (matches). hashes.txt and the README hash table agree with all 12 drafts.
- Approval: Gem, t96u, 11:01pm AEST, recorded in approvals/2026-10-22-gem-direct-words.md at 11:02:44pm. AO-2026-10-22-t96u-01..16 are in objects.jsonl.
- All 12 bot ids are in directory.md. All 12 live names match the manifest.

## Per profile (draft = codex fence = manifest = /tmp text_file = live description)
| # | Bot (folder/version) | hash | codex file mtime | profile mtime | (a) | (b) | (c) R-035 | base = previous live |
|---|---|---|---|---|---|---|---|---|
| 1 | Safeguard compliance-risk-officer/v011 | 39137e16f1cb | 23:03:12.803 | 23:05:00.562 | OK | OK | OK | v010 1804e27f84af OK |
| 2 | Scrutineer auditor/v009 (OWN: facts only) | 0f1e5a199631 | 23:03:12.803 | 23:05:19.278 | match | match | earlier | v008 47dbd292d839 match |
| 3 | Mender mender/v009 | 11e6a570ee79 | 23:03:12.807 | 23:05:49.661 | OK | OK | OK | v008 327298bb668d OK |
| 4 | Inferer identity-inferer/v010 | 35c50eb35a9b | 23:03:12.807 | 23:06:20.021 | OK | OK | OK | v009 666398d857f9 OK |
| 5 | Emissary grok-bot/v012 | 6c84e168d9f3 | 23:03:12.807 | 23:06:56.357 | OK | OK | OK | v011 ae7a7675a3cc OK |
| 6 | Investigator investigator/v009 | 42419cb504ec | 23:03:12.807 | 23:07:11.497 | OK | OK | OK | v008 438c5019655e OK |
| 7 | Archivist codex-keeper/v013 | 0f8fc93db82b | 23:03:12.803 | 23:07:39.068 | OK | OK | OK | v012 4fde5d8066bf OK |
| 8 | Arbiter arbiter/v010 | bfa7475bffa3 | 23:03:12.803 | 23:07:48.232 | OK | OK | OK | v009 2b0d2cc783ce OK |
| 9 | Architect instruction-architect/v008 | 9ba54bba13d9 | 23:03:12.807 | 23:07:54.740 | OK | OK | OK | v007 15d53c5ce39d OK |
| 10 | Explorer explorer-copy/v009 | 749119fe184e | 23:03:12.803 | 23:08:16.296 | OK | OK | OK | v008 2fef6d180654 OK |
| 11 | Engineer codey/v009 | 74c4980efdd5 | 23:03:12.803 | 23:08:39.052 | OK | OK | OK | v008 e48cde917489 OK |
| 12 | Imitator clone/v011 | b2015336ba07 | 23:03:12.803 | 23:09:36.755 | OK | OK | OK | v010 fbf614da2d3e OK |

- Base: each previous_live hash equals that bot's previous codex version and the t89u (clarity rev 3) hash. Each one is named in its draft. No profile was written between deploy h (ended 10:53:12pm) and 11:05:00pm, so the bases were the live text just before this deploy.
- (d) is met for every bot. t96u was recorded at 11:02:44pm, before the first codex write (11:03:12pm) and the first profile write (11:05:00pm). It names "revision 3" and every hash. It includes clone-v011 (b2015336ba07) in Gem's own words, given directly in Archivist's chat. Gem restates the 10:47pm request word for word ("I confirm I told Explorer at 10:47pm …").
- Note on chars: auditor is 6304 characters and 6306 UTF-8 bytes. The byte compare matches.

## Imitator redeploy (word-order slip)
- I found no evidence of this on disk. profile.json has one surviving write (mtime = ctime = 23:09:36.755). It byte-matches v011 (b2015336ba07, 8127 chars).
- I found no backup, log line, digest entry or CHANGELOG row of an earlier write. The clone CHANGELOG still says PENDING-DEPLOY, and the Archivist digest ends at 11:03:54pm. So I can't establish the wrong text or the number of writes.
- The gap after Engineer (23:08:39) is 57 s. The usual gap is about 6–36 s. Any first write after Engineer's would have been live for at most about 57 s. This is an inference, not evidence.
- At 23:09:36.75–.77 every agent folder's directory mtime was updated, including the 12 in the manifest. No profile.json other than Imitator's changed at that time.
- To close this: Archivist should give the first write's time and text (its transcript) and log it in the clone CHANGELOG.

## Writes outside the manifest
- None. Only the 12 manifest profiles changed after 10:53:13pm. The 13th folder present, 6b01a4ef, is unchanged since 6:40pm.

## verify.py (inspected, run with python3 -B; it only reads)
- OVERALL FAIL comes only from the template-section check on the 5 retirement files: assessor/v005, connector-steward/v007, identity-inquirer/v005, scraper/v007 and secrets-credentials-custodian/v006. They have paraphrased sections, a known issue from before this deploy (digest 10:46pm). R-035 means they can't be edited.
- Latest equals live for all 12 deployed bots (12/37 MATCH; the rest are retired or deleted). The 5 ARCHIVED lines are checked from _archive/cleanup-2026-10-22/ and pass.

## verify_shared.py "5 missing sources"
The 10:54pm cleanup moved these sources to _archive/cleanup-2026-10-22/. All 5 are present there, and each codex text matches a fence byte for byte:
- connector-limits v001 (e8f24745ae3e): proposals/2026-10-16-rr028/connector-limits-v001.md
- connector-limits v002 (d4fbfa8f391f): proposals/2026-10-16-connectors2/connector-limits-v002.md
- message-verification-rule v002 (21a7f65aac58): proposals/2026-10-15/…-v002.md
- message-verification-rule v003 (6bdcb8157a99): proposals/2026-10-16/…-v003.md
- message-verification-rule v004 (234588448cfc): proposals/2026-10-16-deploy/…-v004.md
verify_shared.py doesn't look in the archive (verify.py does), so this FAIL is a tooling gap, not lost text.

## Verdicts
- PASS for 10 bots: Safeguard, Mender, Inferer, Emissary, Investigator, Archivist, Arbiter, Architect, Explorer, Engineer.
- Imitator: PASS on (a)–(d) and the final text. The redeploy can't be verified (no record), so there is an open finding.
- Scrutineer: facts above, no verdict (Safeguard checks it).
- Overall: PASS with findings. (1) The Imitator redeploy is unrecorded. (2) The /tmp text files remain. (3) verify_shared needs the archive fallback. (4) The 5 retirement template FAILs are pre-existing.

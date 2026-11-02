# Deploy check: manifest 2026-10-22e (Scrutineer, read-only)
Checked 22 Oct 2026, about 10:25pm AEST (UTC+10). Source: codex/_tools/deploy_manifest_2026-10-22e.json (3 shared entries on HOLD, not deployed; 7 profiles).
Method: SHA-256 of the single fenced block in codex/<folder>/<version>.md; profile.json `description` compared byte for byte and hashed; mtimes from stat (box restored ~6:38pm, so only later times count).

## Per-bot results
| Bot | Version | (a) version file / fence hash | (b) live desc == fence, desc hash | (c) R-035 file mtime < profile write | (d) Gem-approved hash | Result |
|---|---|---|---|---|---|---|
| Safeguard 3661a899 | v009 | exists, 63bda951af2e | yes, 63bda951af2e (13957 chars) | 9:45:19pm < 10:18:41pm | t72u item 5: 63bda951af2e | **PASS** |
| Scrutineer affe0344 | v007 | exists, d44d1b469f4c | yes, d44d1b469f4c (6702 chars) | 9:45:19pm < 10:18:58pm | t72u item 5: d44d1b469f4c | **FACTS ONLY (no verdict; Safeguard checks)** |
| Mender c8401a53 | v007 | exists, 40340aba6a8e | yes, 40340aba6a8e (11888) | 9:45:19pm < 10:19:40pm | t72u item 5: 40340aba6a8e | **PASS** |
| Inferer 94516ca6 | v008 | exists, e8fd68bdface | yes, e8fd68bdface (12201) | 9:45:19pm < 10:20:08pm | t72u item 5: e8fd68bdface | **PASS** |
| Emissary 28cf987d | v010 | exists, 0f81773e8ad3 | yes, 0f81773e8ad3 (14845) | 9:45:19pm < 10:21:00pm | t72u item 5: 0f81773e8ad3 | **PASS** |
| Investigator f2016e9b | v007 | exists, 27ce24f4ea64 | yes, 27ce24f4ea64 (4873) | 9:45:19pm < 10:20:26pm | t72u item 5: 27ce24f4ea64 | **PASS** |
| Archivist 61ef3abd | v011 | exists, dd05b20d49db | yes, dd05b20d49db (9584) | 9:45:19pm < 10:21:24pm | t72u item 5: dd05b20d49db | **PASS** |

All manifest ids match directory.md; manifest `text` also hashes to the same values. Approval: approvals/2026-10-22-gem-direct-words.md, Gem in Archivist's chat (t72u) 9:27pm, item 5 lists all seven hashes; deploy go-ahead t80s452 10:15pm ("Yes, deploy now, Drive later"), recorded 10:16:14pm, before the first write (R-029 order holds).

## Mediator 90f9eb20
- name now 'P2 (Ops) Mediator'; profile.json mtime 10:18:06pm.
- description hash caf84f624c4d (2776 chars) = codex connector-steward v006 fence hash, so the description is unchanged from the recorded live version. Other fields: title '', avatar heart/black, namedBy user, harness temporal (no prior snapshot to diff; nothing indicates change).
- Approval: t81s468 at 10:18pm, "Rename Mediator; full text can be public". Record heading and profile write are both stamped 10:18:06, so recorded-before-write can't be shown at one-second resolution.

## verify.py (codex/_tools/verify.py)
Inspected first: 147 lines, every open() is a read, no write/rename/subprocess calls. Ran with `python3 -B` (no .pyc). Output: `OVERALL: FAIL`, `STRICT latest==live: 17/37`.
- 17/37 is not 17 mismatches. 37 codex folders: 17 MATCH (every bot with a live profile, the 7 deployed here included), 20 DELETED (retired bots, profile gone). The strict line counts matches over all folders.
- The only FAIL line is `connector-steward name: profile 'P2 (Ops) Mediator' != index Current name 'P4 (Ops) Mediator'`. That is because codex/index.md was not updated after the approved rename. It relates to this session (Mediator rename) but not to the 7 manifest profiles.

## Findings
1. The deploy writes ran 10:18:41–10:21:24pm. The stated 10:20–10:30pm window is slightly wrong: Safeguard, Scrutineer and Mender were written before 10:20.
2. The CHANGELOGs for all 7 bots end with "Deploy NOT done yet ... Live profile unchanged" (10:16pm). No DEPLOYED rows have been added yet, so the record lags reality (check 5/6 bookkeeping).
3. index.md still shows 'P4 (Ops) Mediator', and directory.md line 38 still says the name isn't fixed, so verify.py reports FAIL.
4. The Mediator rename (10:18:06pm) is a profile change outside manifest e. It is Gem-approved (t81s468) but not in any manifest.
5. Other profile writes since the restore (febac500 7:57pm; f8e3fdc6, 6ae584b8, 04dcca0d, 51af1200, 2133048d 9:40–9:41pm) predate this deploy and are outside its scope. Not checked here.
6. The shared entries (resilience, approval-objects, deterministic-checks) are on HOLD in the manifest and were not deployed. Their approved hashes in t72u match the manifest.
7. Scrutineer v007 was deployed before its retiring merge sources finished; directory.md says retirement waits for verification. Safeguard should verify Scrutineer's deploy.

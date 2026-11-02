# Scrutineer deploy check: imitator-v007 to Imitator (6ae584b8-eaac-429b-9eae-d5e3e6f6a32b), 22 Oct 2026, about 9:33pm AEST

This check was read-only. The hash is the SHA-256 of the text, first 12 hex characters. All times are AEST (UTC+10).

| # | Check | Verdict |
|---|---|---|
| 1 | Live description is byte-equal to the draft and the codex | **PASS** |
| 2 | Deploy manifest matches | **PASS** |
| 3 | Version file written before the profile (R-035) | **PASS** |
| 4 | Only Imitator's profile changed | **PASS** |
| 5 | Gem's approval is on record and names the hash | **PASS** |
| 6 | CHANGELOG and index rows updated | **PASS** |
| 7 | verify.py passes | **PASS** |
| 8 | v008 and v009 still chain on v007 | **PASS** (one advisory) |

## Evidence
1. **Byte-equal.** The profile.json description is 3845 characters, with SHA-256 db56debaa35f (full hash db56debaa35f3827e8932d206775bbb18eb541a35bf238aa11fbbd75392874d9).
   - It is byte-equal to the fenced text in proposals/2026-10-22-redundancy/imitator-v007.md.
   - It is also byte-equal to the fenced text in codex/clone/v007.md.
2. **Manifest.** codex/_tools/deploy_manifest_2026-10-22b.json has one entry, recording:
   - agentId 6ae584b8…, folder clone, version v007, field description
   - chars 3845 and sha256 db56debaa35f3827…
   - its `text` is byte-equal to the live description, and its sha256 equals the computed hash.
3. **Order (R-035).** codex/clone/v007.md, CHANGELOG.md, index.md and the manifest were all modified at 21:29:52.669. profile.json was modified at 21:30:40.240, 48 seconds later.
   - Info: the CHANGELOG reports the deploy as 9:30:43pm. The profile's mtime is about 3 seconds earlier, so that time is approximate. It doesn't affect the result.
4. **Only Imitator changed.** Imitator's profile.json is the only one modified after 9:00pm.
   - verify.py reports MATCH (latest codex equals live, and the name is OK) for all 17 live agents.
   - The 20 non-matches are retired bots whose profiles are already gone (marked DELETED), not mismatches.
5. **Approval.** approvals/2026-10-22-gem-direct-words.md:26 records "Gem, in Archivist's chat (t72u), 9:27pm 22 Oct 2026". Line :29 records: "I approve imitator-v007 from the redundancy batch (proposals/2026-10-22-redundancy/imitator-v007.md, text hash db56debaa35f) — record and deploy."
   - The approval **names the hash**, and it matches.
   - It is Gem's own words in Archivist's chat, so it meets R-015 and R-027: only Gem approves changes to Imitator. Neither Imitator nor any other bot approved it.
6. **CHANGELOG and index.**
   - codex/clone/CHANGELOG.md has a row for version 7 (22 Oct). It cites Gem's t72u words, then has a PENDING-DEPLOY row and a DEPLOYED row ("DEPLOYED v007.md to the live profile … at 9:30:43pm AEST").
   - codex/index.md:12 reads "clone/v007.md | v007 | 2026-10-22 | OK (LIVE) … deployed 22 Oct 2026 at 21:30:43 AEST … t72u".
7. **verify.py.** It only reads: every open() is a read, with no writes, renames or subprocess calls.
   - Running it gave "OVERALL: PASS" and "STRICT latest==live: 17/37 match; 0 logged pending-deploy". It also printed one INFO line about a former holder's profile being gone.
8. **Later imitator drafts.**
   - imitator-v008 (proposals/2026-10-22-r044-veto/imitator-v008.md:6) gives its base as "redundancy draft imitator-v007.md (text db56debaa35f; recorded and live if the codex now holds it)". The codex and the live profile now hold exactly db56debaa35f, so the base matches.
   - imitator-v009 (2026-10-16-github/imitator-v009.md:7) chains on db56debaa35f and then d877b6d0b31f.
   - The text hashes are unchanged: v008 d877b6d0b31f and v009 c92d31926a18.
   - **Advisory:** imitator-v009:7's header still says "codex v006 (latest; byte-checked = live profile 22 Oct 8:36pm)". The latest version is now v007. **Fix:** update the header to "codex v007 (live)" at the next rebuild. This changes the file hash only, not the text hash.

## Overall: PASS
The deploy is correct and recorded. The next step in the record order is r044-r047: imitator-v008 and arbiter-v007.

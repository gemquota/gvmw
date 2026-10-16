# Deploy check 16d, 16 Oct 2026 (AEST)

Checker: an independent executor, run for Scrutineer (`affe0344`). Read-only. Checked 11:50–11:53 AEST, Fri 16 Oct 2026. This file is the only thing written. No scratch files. Nobody was messaged. Chat transcripts were not reachable.

## Manifest

- Manifest: `/workspace/governance/codex/_tools/deploy_manifest_2026-10-16d.json`. Birth = mtime 11:48:59.738.
- 1 entry: Investigator `f2016e9b`, folder investigator, v004.
- **Format gap:** the entry has only agentId, folder, version and text. It has no name, field, sha256 or chars, unlike every earlier manifest. I hashed the text myself.

## 1. Bytes

- Live description sha256: `68b76c08ba86b07ea6b4ed29770b7ebfa199c6d5a8385395d41e8dd09af8804d`. 2581 chars. Name "P3 (ID) Investigator".
- It equals the manifest text and the proposal's verbatim block byte for byte. It matches the proposal's "draft sha256 68b76c08ba86".
- It also equals the verbatim block in current `codex/investigator/v004.md`. verify.py prints `MATCH investigator v004.md name=ok`.
- profile.json mtime: **11:49:23** (birth = mtime, written once).
- Result: **PASS**.

## 2. Change from v003

- Base: `codex/investigator/v003.md` block, sha256 `4c94b8b438b4…` (2569 chars). It equals the live hash at the 15 Oct check and the proposal's base hash.
- A character diff of v003 against the live v004 shows exactly two changes:
  1. "Each week once P4 is live, sample Imitator's recent answers," → "Each day once P4 is live (Gem, 16 Oct), sample Imitator's recent answers,"
  2. "the weekly accuracy score to Scorer," → "the daily accuracy score to Scorer,"
- Applying the proposal's two old→new pairs to v003 gives the live text exactly.
- The sentence "This testing is a review after the fact, not a gate…" is unchanged.
- Result: weekly to daily is the only change, plus the "(Gem, 16 Oct)" tag. **PASS**.

## 3. The v004.md record and the as-first-written copy

- Proposal file: sha256 `7c05c1a1b333…`, 4221 bytes, mtime 11:07:14.
- `_archive/investigator-v004.md.as-first-written-114956`: byte-identical to the proposal (same sha256, 4221 bytes). Birth = mtime **11:49:56.274**.
- `codex/investigator/v004.md`: birth **11:49:06.718**, mtime **11:49:56.278**, 5228 bytes, sha256 `800ac510e9e5…`.
- Its first 4221 bytes equal the archive exactly. The extra 1007 bytes are appended only. Nothing above was changed.
- The archive copy was made at 11:49:56, the same moment as the append, not at 11:49:06. So it shows the file just before the append. It can't prove what was written at 11:49:06. That is consistent with the claim but not independent proof.

Appended text (summary):
- A "Codex record" table: Bot id, Version 4, Date, Author Architect, and a Reason (weekly to daily).
- "Approved by: Gem, directly in Archivist's chat at 11:48am … ('I approve proposals/2026-10-16-investigator/investigator-v004.md. Record and deploy it.')".
- A Source line with sha256 7c05c1a1…, and Previous version v003.md.
- A "## Template sections" heading with the NO-TEMPLATE-SECTIONS-IN-PROPOSAL marker.

Meaning: the appended text adds no scope, duty or approver. The fenced instruction block is untouched. The approval it states matches the approvals file. **No change of meaning.**

Timing claims:
- The heading says "appended … ~11:51am", and the CHANGELOG (mtime 11:50:03) says "about 11:51am". Disk shows **11:49:56**, which is before the CHANGELOG was written. The stated time is wrong by about a minute.
- The append came 33 s **after** the 11:49:23 profile write. At deploy time v004.md had no Bot id, Approved-by or template-sections block.

**C4 / R-023 conflict (for Arbiter):**
- R-023 (C4) and `codex/README.md` say version files are immutable and "Archivist doesn't edit version files". The append rewrote v004.md 50 s after it was created. That is an edit, even though it only added text and was disclosed.
- Suggested question for Arbiter: should v004.md stay as is, or should the header have gone in a fresh record? Either way, the archive and this check preserve the first bytes.
- Why it was likely needed: the first-written file had no `| Bot id |` row, no `## Template sections` and no skip marker. verify.py reads the Bot id of the latest version file, and it splits on "## Template sections" for v002+ files. Reading the code, it would have stopped with an error on the first-written file rather than printing OVERALL PASS. This is an inference from reading the code. I didn't run verify.py against that state.
- So the CHANGELOG claim "Byte check matched at 11:49:28 and verify.py gave OVERALL PASS" can only be right for verify.py if it ran after 11:49:56.

## 4. Approval

Gem's words:
- `approvals/2026-10-16-gem-direct-words.md` holds them: "11:48am, in Archivist's chat, answering Archivist's card: 'I approve proposals/2026-10-16-investigator/investigator-v004.md. Record and deploy it.' Approver: Gem directly (R-015, R-027…)".
- Explorer's relay of Gem's 11:46am "Approve all drafts" is noted as context only.
- Gem-only check: Investigator checks Imitator, so this is Gem-only under R-015 and R-027. The words name this exact file. **Covered.**

When the words first reached disk:
- The approvals file's mtime is **11:48:48.898**.
- The _archive backup `2026-10-16-gem-direct-words.md.bak-114848` has the same mtime. It is the **before** copy: it does **not** contain the 11:48am words. The diff between them is exactly the new 11:48am section.
- So the words first reached the file at 11:48:48. That is **34.4 s before** the 11:49:23 profile write.
- The section heading says "Recorded … at 11:49am"; disk shows 11:48:48.
- The other copies of the words came later: the manifest has none, and v004.md (11:49:56), the register (11:49:40) and the CHANGELOG (11:50:03) came after.
- The 11:48am chat time rests on Archivist's record only.

Imitator:
- The CHANGELOG rows cite Gem directly. They name Gem's 11:05am words to Investigator and Explorer's relay as context only.
- Imitator's log (`approvals.md`, last written 11:09:06) has no entry for this change.
- No record cites Imitator as approver.

Safeguard:
- The only record is `risk/register.md` RR-039, "PRE-DEPLOY NOTICE (2026-10-16 11:49:40)", with "No concern raised". The register's mtime is 11:49:40.85.
- That is **17 s after** the 11:49:23 write. No file shows Safeguard was told before the write.
- The CHANGELOG says "Safeguard was told beforehand". Disk doesn't support that. The notice may have been sent earlier and logged later; only Archivist's or Safeguard's transcript could show it.

## 5. Collateral

- `profile.json` files modified after 11:45am: only Investigator (11:49:23). No collateral profile change.
- Other change: an Engineer attachment (.png) at 11:49:57. Not a profile.
- Agent folders: same 17 (18 entries including `active-agent.json`).
- verify.py (unchanged since 9 Oct 10:40), run read-only at 11:52: exit 0, **OVERALL: PASS**. `STRICT latest==live: 17/37 match; 0 logged pending-deploy`. investigator v004 MATCH name=ok. No FAIL lines.

Scrutineer `affe0344` (facts only, not a verification; needs an independent checker): mtime still **11:06:49.326**. sha256 `542ade104e4bb4c74f09e3991ad7d971163f237d6bd58815bb46756af037797e`, 1682 chars. Unchanged.

## Verdict

- Investigator v004 bytes: **PASS**. The live text equals the proposal and the manifest, and the only change is weekly to daily.
- Approval: **PASS**. Gem's direct words, on disk 34 s before the write.

Process problems (not byte fails):
1. v004.md was edited after creation (append at 11:49:56). This conflicts with R-023 (C4). It needs Arbiter's view.
2. The stated append time (~11:51am) is wrong; disk shows 11:49:56. The codex record was completed after the deploy.
3. "Safeguard told beforehand" has no support on disk. RR-039 was logged 17 s after the write.
4. The verify.py PASS claimed at ~11:49:28 couldn't have run cleanly against the first-written v004.md (inferred from the code).
5. The manifest is missing the name, field, sha256 and chars fields.

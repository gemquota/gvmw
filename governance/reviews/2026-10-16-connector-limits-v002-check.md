# Recording check: shared connector-limits v002 (Archivist, about 3:55pm)

Reviewer: Scrutineer (independent, read-only), Friday 16 Oct 2026, about 3:58pm AEST (UTC+10).

Method:
- Hashes: `sha256sum` for files; text hashes computed in memory (the content of the text block, no trailing newline).
- Times: `stat` birth, mtime and ctime.
- Revision 6 was rebuilt in memory from `_tools/build-r6.py.bak`. Writes were redirected to memory, and the script's codex-folder check was given a version list without v002 so it would run. Nothing on disk changed.
- `verify.py` was read first: it only reads files. I ran it with `python3 -B`.

## Verdict: PASS
- v002.md is the default revision 7 text, byte for byte.
- It was written once, after Gem's words were recorded, with backups made first.
- v001 is untouched.
- The CHANGELOG has one row appended.
- Arbiter's correction note is present, and the original stamps are intact.
- There are three minor notes (section 8), none affecting the record.

## 1. Revision 7 hashes, and the diff from revision 6

| File | Expected | Found | Result |
|---|---|---|---|
| default r7, file | f4b6da9c15c3 | f4b6da9c15c3c1e6… | MATCH |
| default r7, text | d4fbfa8f391f | d4fbfa8f391f | MATCH |
| variant B r7, file | 601ab830a825 | 601ab830a8252cf6… | MATCH |
| variant B r7, text | 069cfd00cd61 | 069cfd00cd61 | MATCH |
| Rebuilt r6 | bff307934fcd / b007cb163a93 (files 8492271c4ac2 / f8a8136077d7) | the same | MATCH |

**Revision 6 to revision 7, in both variants:**
- The only change to the rule text is in rule 9 (line 12 of the text block), which inserts "Moving to Trash isn't archiving; it's a deletion under rule 13. ". The text still has 25 lines.
- The only other change in each file is one Notes line, where "which Gem confirmed for first replies to new contacts at 3:41pm (R-038)" becomes "…new contacts (R-038)".
- **No undeclared change.**
- Rule 15 still says "Gem confirmed this for first replies at 3:41pm". That's the time of Gem's words, which is correct.

## 2. v002.md

| Fact | Value |
|---|---|
| Path | codex/_shared/connector-limits/v002.md |
| sha256 | **c290e699516b**7064ba3fb2687d993e1f2b4b4b2e0976fe2d6b24f5747f233f0b. MATCHES Archivist's figure |
| Size | 20,051 bytes |
| birth / mtime / ctime | **15:55:16.320 / 15:55:16.320 / 15:55:16.320 AEST**, all identical |
| Appended to? | **No.** All three times are the same, and nothing was written after creation (R-035) |
| Text blocks | Exactly 1. Hash **d4fbfa8f391f**, byte-identical to default r7's text (the strings compare equal). **Not** variant B (069cfd00cd61) |
| Base | Header: "Previous version v001.md (text sha256 e8f24745ae3e…)". v001's text hashes to e8f24745ae3e. MATCH |

- The header has Version, Date, Author, Reason, Approved by (Gem's full words, quoted), Source (r7 file f4b6da9c15c3, text d4fbfa8f391f), Owner Safeguard and Previous version.
- Status: "APPROVED and recorded… Later events go only in the CHANGELOG (R-035)."
- The proposal's Notes and draft header aren't carried over, which is right for a codex file.
- The words quoted in v002.md are byte-identical to those in the approvals record.

## 3. Order of events, and Gem's words

| Time (AEST) | Event |
|---|---|
| 15:54:35.920 | Backup `_archive/2026-10-16-gem-direct-words.md.bak-155435` (10,321 bytes) |
| 15:54:35.924 | `approvals/2026-10-16-gem-direct-words.md` gains a section "Recorded by Archivist at 3:54pm… BEFORE any deploy (R-029)". Diffed against the backup, it's additions only |
| 15:55:16.320 | `codex/_shared/connector-limits/v002.md` created |
| 15:55:16.328 | Backup `_archive/connector-limits-CHANGELOG.md.bak-155516` |
| 15:55:16.332 | `CHANGELOG.md` updated |
| 15:56:16.884 | `codex/index.md` rebuilt |
| 15:57:02 | `codex/MIRROR.md` and the proposal README updated (Status: RECORDED) |

The order is correct: backup, then Gem's words, then v002.md, then the CHANGELOG backup, then the CHANGELOG.

**Gem's recorded words** (3:54pm, Archivist's chat, message t55u):

> "I approve connector-limits v002 (proposals/2026-10-16-connectors2, text hash d4fbfa8f391f), including Notion/Todoist sharing on my words plus a dry run, Explorer writing to Notion/Todoist, and no Mem0 writers for now, with the conservative defaults (no Imitator route for Notion/Todoist, routed work confirmed with me, workflows wait for Safeguard, no deletion exception, backup-only archiving in Notion/Todoist, Imitator's email replies as MVR v004 item 1 with first replies per R-038, GitHub-xai read-only, Vercel per R-037) — record and deploy."

- **They name both the proposal folder and the text hash.** d4fbfa8f391f is the default revision 7 text and nothing else.
- They also pick the default's sharing option ("sharing on my words plus a dry run"), not variant B's "total ban".
- **The choice of the default is unambiguous.** It's a direct approval in Archivist's chat (R-027, R-029). "Deploy" has nothing to do here, because this is a shared document, not a profile.

## 4. The connector-limits folder

| File | sha256 | birth | mtime | Result |
|---|---|---|---|---|
| v001.md | e1f86f22fb55… | 11:06:00.982 | 11:06:00.982 | **Unchanged.** Same hash as the base stated since revision 1; ctime is also 11:06:00. Immutable (C4/R-023) |
| v002.md | c290e699516b… | 15:55:16.320 | 15:55:16.320 | New, written once |
| CHANGELOG.md | b8f6c28d2fa5… | 11:06:00.982 | 15:55:16.332 | **Changed by appending only.** Diffed against its backup, one row was added (version 2) |

- **CHANGELOG row 2:** "Gem, directly in Archivist's chat 16 Oct 2026 3:54pm AEST (t55u): "I approve connector-limits v002 (proposals/2026-10-16-connectors2, text hash d4fbfa8f391f), … — record and deploy." … recorded at 3:54:35pm before this entry (R-029)… Default text, not variant B." The quote is shortened with "…", but it points to the full words in v002.md and the approvals record. Fine.
- **index.md:** the row for `_shared/connector-limits/` now reads v002, "default text d4fbfa8f391f, not variant B… waiting for Scrutineer's check". There's no separate manifest, which is normal for a shared document.
- **Nothing else changed in the folder.** The proposal files kept their r7 hashes after recording. The only change in the folder after recording is the README's Status line.

## 5. verify.py (run read-only)
- Command: `python3 -B codex/_tools/verify.py`, exit code 0, 211 lines. Last lines: "STRICT latest==live: 17/37 match; 0 logged pending-deploy: -" … "OVERALL: PASS".
- Every live bot shows MATCH (latest codex version equals the live profile's instructions). Retired bots show "DELETED (profile gone)", which isn't a failure.
- **Caveat: verify.py doesn't check `_shared/connector-limits/` at all.** Its shared-file checks cover only handoff-phase1 and collaboration-map. So its PASS is no evidence for v002. My own byte checks in sections 2 and 4 are the evidence for v002.

## 6. profile.json changes around 3:50–4:00pm
- **No profile was written for v002**, and none needed to be.
- However, **six live profiles were rewritten between 15:47:20 and 15:51:35.** Each file was replaced: birth time equals mtime.

  | Time | Bot | Profile |
  |---|---|---|
  | 15:47:20 | Mediator | 90f9eb20 |
  | 15:48:57 | Imitator | 6ae584b8 |
  | 15:49:25 | Inquirer | 0314faa4 |
  | **15:51:01** | **Engineer** | f8e3fdc6 |
  | **15:51:17** | **Investigator** | f2016e9b |
  | **15:51:35** | **Arbiter** | 2133048d |

  The last three fall inside the 3:50–4:00pm window.
- **Instructions are unchanged.** verify.py shows each one MATCHES its latest codex version; for example, Mediator's description hash caf84f624c4d equals connector-steward v006's text hash. No new codex version exists for any of them.
- **What changed is unknown.** There are no earlier copies, and the 3:45–4:00pm governance files say nothing about it.
  - All six now have a coloured "heart" avatar, which may point to an avatar or settings change made in the app.
  - I printed only the name, harness, avatar and serverId fields, and description hashes. No other values.
- This doesn't affect v002. Safekeeper or Archivist may want to note the cause.

## 7. Arbiter's correction note in rulings.md
- **It's present and dated:** "## Correction note (16 Oct 2026, 3:48pm, from the system clock): Time stamps on R-037 and R-038". rulings.md mtime is 15:49:11, which is consistent.
- **It reads:** "R-037 and the interim R-038 were written just before about 3:41pm. The final R-038 was written between Gem's 3:41pm answer and 3:41:49pm… the original stamps are left as written. From now on, Arbiter takes every stamp from the system clock when writing."
- **The original stamps are intact, and the file was only appended to.** The first 45,804 bytes of the current file (48,484 bytes) hash to **3b91efe6dc5d**, exactly the whole file as I hashed it at 15:44. Lines 260, 266 and 273 still say "3:45pm", "3:45pm" and "3:43pm".
- **Two loose ends:**
  - The note says the approvals record's "~3:43pm" "should likewise read 3:41pm". That line is unchanged, which is correct: the record shouldn't be rewritten, and the note serves as the correction.
  - R-039 (3:49pm) was appended after the note. It's a separate ruling that lets Mediator create the private workspace repo on Gem's direct ask, under conditions.

## 8. Minor notes (none affect the record)
1. **verify.py doesn't cover shared rules beyond the two 4 Oct documents.** Worth adding a check for `_shared/connector-limits/` and `_shared/message-verification-rule/` that compares the text with its source.
2. **Time stamps written ahead of the clock again,** this time by Archivist:
   - index.md says "Last rebuilt ~3:58pm" but was written at 15:56:16.
   - The README Status says "~4:00pm" but was written at 15:57:02.
   These are the same kind of slip Arbiter has just corrected, so stamps should be taken from the system clock.
3. **Six profile.json files were replaced between 3:47 and 3:51pm,** with instructions unchanged and the cause unrecorded (section 6).

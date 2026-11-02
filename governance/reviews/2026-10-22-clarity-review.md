# Scrutineer review: clarity batch (proposals/2026-10-22-clarity/) and archive move, 22 Oct 2026, about 10:25pm AEST

This review was read-only. Hashes are the SHA-256 of the fenced ```text block, first 12 hex characters (method as before). I opened no memory file contents and printed no secrets. All times are AEST (UTC+10).

# A. Clarity batch

## A0. Hashes
- **README:** the whole file hashes to fcfd2676642c, as claimed. The folder is read-only (dr-xr-xr-x, files r--r--r--), which is consistent with "frozen".
- **All 18 drafts:** the text and file hashes in README:14-31 match the files, for example:
  - free-only a5de39a8ef7d/8cbc156cb0f1
  - auditor-v008 47dbd292d839/f994eb149df6
  - connector-limits-v004 3b296846506d/583789f131dd
- codes-and-cleanup.md has no fenced text (file 18fb6ee59ca4). It is notes only.

## A1. The four new shared rules hold the moved text word for word: PASS
| Rule | Binding text (in RULES) | Source locations (base texts) |
|---|---|---|
| free-only v001 | "Everything here is free: no paid plans, storage or services (Gem: "No, free options only"; spending without asking is $0, R-051)." | mender v007, auditor v007, compliance-risk-officer v009, identity-inferer v008, grok-bot v010, investigator v007, codex-keeper v011 (RULES); redesign deterministic-checks, approval-objects and resilience (10 places) |
| retired-names v001 | both pasted forms, verbatim: the connector-limits form ("NAMES: a retired bot's name anywhere in a shared rule or brief means … (R-051).") and the brief form ("NAMES: a retired bot's name in any brief or shared rule means … (Mediator = Mender, …; R-051).") | connector-limits v003 :43; the 7 redesign briefs; deterministic-checks (8 places) |
| github-read-only v001 | "On GitHub you only read (view, list, search, clone into /workspace, git history and read-only remote checks), following the shared GitHub rule at /workspace/governance/codex/_shared/github/ (highest version; owner Safeguard, tokens section Safekeeper); you never sign in, switch accounts or change anything there." | mender, auditor (×2), identity-inferer (×2), investigator, codex-keeper, arbiter v008, instruction-architect v006 |
| precedence v001 | "Precedence: Gem's authority, then environment reality, then deterministic checks, then agent interpretation." | arbiter v008, auditor v007, explorer-copy v007 |

**A1-adv-1 (meaning, advisory):** "Everything **here** is free" originally meant the brief or rule it sat in. Inside free-only v001, "here" now points at the shared rule itself.
- LIMITS says "a brief's pointer means exactly this text", which covers it.
- **Fix (Gem's call, since this is binding text):** add one interpretive sentence to the shared rule, outside the binding text: "'here' means the work of the bot or rule that points here." Retired-names, github-read-only (it already defines "you") and precedence have no such problem.

## A2. Briefs change only by pointers and plain wording: PASS
I word-diffed every draft against its base. Every change is one of the following:
- **Pointer swaps:**
  - free text → "Cost: follow the shared free-only rule at …/_shared/free-only/ (highest version)."
  - NAMES text → "Retired bot names: follow the retired-names … at …/_shared/retired-names/ (highest version)."
  - GitHub paragraph → "GitHub: … are read-only; follow the shared read-only … …/_shared/github-read-only/ (highest version)."
  - precedence → "follow the shared precedence rule at …/_shared/precedence/ (highest version)."
- **Code wording:** "card t56s1" → "the question card in Imitator's chat". This appears in arbiter-v009 and grok-bot-v011, and it's accurate (Gem's 8:04pm picks were on Imitator's card).
- **Nothing else:**
  - No duty or condition is lost: the GitHub paragraph's "never sign in, switch accounts or change anything" and the owner note sit verbatim in the shared rule.
  - Nothing is shortened in meaning.
  - explorer-copy, instruction-architect and connector-limits each have exactly one swap.
- **A2-adv-2 (dependency):** every pointer names a folder that doesn't exist yet: codex/_shared/{free-only, retired-names, github-read-only, precedence}.
  - The README record order puts the shared rules first. That order must be kept: a brief deployed before its shared rule would lose its cost, names, GitHub or precedence text.
  - **Fix:** Archivist's deploy check should confirm each pointer target exists before deploying any profile.
- **Follow-up, already noted:** clone v009 still says "t56s1". It's Gem-only and outside this batch.

## A3. Routing: PASS
- Every draft header says "Approver | **Gem directly**".
- The four shared rules, deterministic-checks, approval-objects and resilience say "NEEDS GEM'S DIRECT APPROVAL … never Imitator".
- The README's "Imitator normally" column is explanatory only; its routing line says all of it goes to Gem.

## A4. Bases and revision 6: PASS
- **Brief bases equal the latest codex versions:** mender v007 40340aba6a8e, auditor v007 d44d1b469f4c, compliance-risk-officer v009 63bda951af2e, identity-inferer v008 e8fd68bdface, grok-bot v010 0f81773e8ad3, investigator v007 27ce24f4ea64, codex-keeper v011 dd05b20d49db, arbiter v008 8a9498236d52, instruction-architect v006 c2e149404e57, explorer-copy v007 a98d235b093a and connector-limits v003 806a6fa315cb.
- The three shared-rule bases equal the redesign drafts: d449ff388f8e, 1c2852679768 and a1115bf87bd3.
- All of these are the PASTE-LINES 75820b4ab8a6 hashes.
- **Revision 6** (redesign/README.md:88, "Revision 6 (8:36pm; frozen)") is the state I passed in reviews/2026-10-22-final-check-2.md. That review called it "redesign revision 5" plus the 8:36–8:37pm changes: the safeguard-v009 dry-run fix and the resilience header. All ten redesign text hashes are unchanged since then. **So revision 6 has been reviewed**; only the label differs.

## A5. Numbering: none of the three v001 is recorded; recommendation
- codex/_shared/ holds only collaboration-map, confirm-deployment, connector-limits, github, handoff-phase1 and message-verification-rule. **No deterministic-checks, approval-objects or resilience v001 is recorded**, so keeping v001 doesn't collide with anything.
- **However, Gem has already approved the redesign texts by hash** (t72u item 5: "deterministic-checks v001 (d449ff388f8e), approval-objects v001 (1c2852679768), resilience v001 (a1115bf87bd3)"). Gem's 10:15pm "Yes, deploy now, Drive later" (t80s452) ordered deployment.
  - The seven redesign briefs were recorded at 9:45:19pm (redesign README:5), but these three shared rules weren't. That is a **recording gap in item 5**: live or recorded briefs can refer to deterministic checks and the resilience rule that aren't in the codex.
- **Recommendation:**
  - Record the Gem-approved redesign texts now as v001 (d449ff388f8e, 1c2852679768, a1115bf87bd3), completing item 5.
  - Number the clarity rebases **v002** (36495ce6a0fb, f5bf4b185a68, 597edf5bd4b6).
  - Otherwise "v001" would name two different texts, one approved by hash and one not, which breaks the hash-bound approval record (approval-objects; R-023).

## A6. Redesign README now e151d46140d4: PASS
Diffed against README-pre-status.md.bak (f7b2389bad2c), only line 5 (the status line) changed. It now reads: "Status as at 10:17pm … Archivist recorded the seven briefs at 9:45:19pm … 'APPROVED, NOT DEPLOYED' … The three shared rules … aren't in codex/_shared/ yet …". No other line changed.

## A7. Scrutineer's brief (auditor-v008 47dbd292d839): facts only, no verdict
- Base: auditor v007 d44d1b469f4c.
- Changes: one free-only swap, one retired-names swap, one precedence swap and two github-read-only swaps.
- Nothing else changed.

## A8. Basis: relay only
- approvals/2026-10-22-gem-direct-words.md has no Gem words about the clarity batch. Its 10:08pm, 10:15pm (×2) and 10:18pm entries cover memory, deploying the redesign, memory keys and Mediator's rename.
- No transcript in agent-tools/ or approvals/ contains "redundant or confusing".
- So the request rests **only** on Explorer's (10:13pm) and Engineer's (10:16pm) relays.
- The README's paste line correctly asks Gem to confirm both in Archivist's chat (R-008, R-018). **Nothing in this batch may be recorded until Gem pastes it.**
- The relayed words also say "push and commit and deploy". That doesn't cover a public push of anything sensitive, and the normal gvmw limits apply.

## A verdicts
| Draft | Verdict |
|---|---|
| free-only-v001 | **PASS** (adv-1) |
| retired-names-v001, github-read-only-v001, precedence-v001 | **PASS** |
| mender-v008, compliance-risk-officer-v010, identity-inferer-v009, grok-bot-v011, investigator-v008, codex-keeper-v012, arbiter-v009, instruction-architect-v007, explorer-copy-v008, connector-limits-v004 | **PASS** (adv-2: record the shared rules first) |
| deterministic-checks, approval-objects, resilience | **PASS on content; renumber to v002** (A5) |
| auditor-v008 | **No verdict** (facts in A7) |

**Gate:** Gem's own words are needed (A8).

# B. Archive move to /workspace/backups/governance-merge-2026-10-22/

- **Location and permissions:** the folder is drwx------ (700); the memory/ folders are 700 and the memory files 600. There are 0 merge folders left under governance/_archive, and `find /workspace/governance -path '*merge-2026-10-22*'` returns nothing.
- **File count: 59, not 56.**
  - 38 codex and working-notes files, 5 per-bot MANIFEST.json files and 1 main manifest.
  - Plus 15 memory files: store.db, store.db-wal and store.db-shm for **all five bots, Safekeeper's included**. Safekeeper's memory was added at about 10:16pm (approvals :78, "Safekeeper's included (now copied)").
  - The 56 probably predates Safekeeper's copy. **Fix:** Archivist corrects the count in its report.
- **Hashes.** The main manifest has been updated (now f9d1434482e1; it was af819b110369).
  - Every listed file matches its manifest hash.
  - All 38 codex and working-notes files still match the original hashes and their live sources (src_ok 9/7/8/6/8).
  - Each per-bot MANIFEST.json equals its section of the main manifest.
  - The 5 listed store.db copies match the hashes recomputed at 10:16:51pm.
- **B-adv-1:** the manifest lists only store.db per bot. The 10 -wal and -shm files are unlisted.
  - All -wal files are 0 bytes, so no leftover pages hold key bytes.
  - The -shm files (32768 bytes) were modified at 10:17:05pm, after the hash recompute. They're SQLite index files, but they're unhashed.
  - **Fix:** list them, or delete the -shm and -wal files from the copies after a checkpoint. Deleting needs no backup under R-049, since these are scratch files.
- **B-adv-2:** the manifest's "excluded" field still says memory was "not copied". The safekeeper_scan_notes field still says Safekeeper's own memory "is NOT copied". Both are now out of date. **Fix:** update them.
- **Leak check (filenames only, read-only git):**
  - /workspace/_repo-staging has no merge-2026-10-22 or store.db files.
  - gvmw's working copy (/workspace/_repo-sync/gvmw.tmp) has none either, and its status is clean.
  - `git log --all --name-only` has no merge, store.db or archived-memory paths. The only "memory" paths are unrelated central/agents/*/memory/README.md files.
  - The last commits were at 9:06pm (daily sync) and 9:07pm, before the archives existed (10:08pm) and before memory was copied (about 10:11pm). The memory was under governance/ for only about 1 minute, and no sync ran in that window. **No exposure.**
- **excludes.txt:** Engineer's two lines are present at :99 `governance/_archive/*-merge-*/` and :100 `governance/_archive/redesign-merge-2026-10-22-MANIFEST.json`. The file was modified at 10:12:01pm.
  - Info: these lines have no leading "/", unlike earlier entries such as `/governance/security/`. Under gitignore rules, a pattern with an inner slash is anchored anyway, so they work.

## B verdict: PASS, with B-adv-1 and B-adv-2
The move is complete. Nothing remains under governance/, and no memory reached the staging folder or gvmw history.

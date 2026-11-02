# Clarity batch revision 2: review (Scrutineer audit, 22 Oct 2026, ~10:30pm AEST)

Scope: proposals/2026-10-22-clarity/ (README a985bb07bdcd) vs _r1/ (README fcfd2676642c, passed in reviews/2026-10-22-clarity-review.md). Read-only. Text hash = sha256(fenced text)[:12].

## (1) Shared-rule numbering: VERIFIED
- Redesign v001 texts unchanged: deterministic-checks d449ff388f8e, approval-objects 1c2852679768, resilience a1115bf87bd3 (proposals/2026-10-22-redesign/).
- Clarity versions renamed to v002; text hashes unchanged from r1 (36495ce6a0fb, f5bf4b185a68, 597edf5bd4b6). Only the title line and Base row changed in each file.

## (2) Record order: VERIFIED
README order and paste line: four new shared rules → the three v002 rules → connector-limits v004 → briefs → clone-v010. Every shared rule comes before any brief that points to it.

## (3) free-only: VERIFIED
- File: free-only-v001.md. Text hash a5de39a8ef7d → f11a42d8346d (file 9b1651cb8cc1).
- One line changed: "Everything here is free" → "Everything a bot uses is free", plus a non-binding wording note. No other change.
- Note: _tools/build.py still has the old string as FREE. So the README claim that putting the shared text back gives the base text byte for byte now holds only for the old wording. The meaning is the same, but the new text is not byte-identical. Not blocking. Correct the README wording.

## (4) clone-v010 (Imitator), text cbc8193cb32d, base codex/clone/v009 c92d31926a18
- Diff of the fenced text vs v009: (a) "on your card t56s1" → "on the question card in your chat" (×2, DISPUTES AND VETO and BOTS); (b) the INTERIM (R-051) paragraph is replaced by SCOPE (R-054 update): Imitator may approve on its own (1) retiring a bot after a verified archive (R-047) and (2) making one of the five named projects public after Safekeeper's scan (R-048, R-050). Merges, deletions that need a backup and anything else irreversible stay advisory. No other change. "7:06pm on your card" remains. That is plain wording with no code.
- **README flaw confirmed:** v009 and v010 contain no free-only, retired-names or precedence text and no pointer lines. clone-v010 "applies the shared-rule pointers" is false. The build header itself says "Only the INTERIM paragraph and the code wording change."
- R-054 update (rulings.md l.425 and rulings/R-054-approval-authority.md l.41), quoted: "At 10:20pm AEST in Explorer's own chat, Gem answered "yes and yes" to message t76s424. I checked this in Explorer's transcript. (1) Imitator may approve retiring bots and making projects public on its own. This overrides R-051's interim for those two things only: merges, irreversible deletions and Gem-reserved changes (R-015, R-027) are unchanged, and a retirement still needs an archive made first (R-047), and going public still needs a Safekeeper scan (R-048). (2) "BIE" means the bie_tools gambling data, which is confirmed. Open items 1 and 'BIE' are resolved."
- Gem's own words: **not recorded** in approvals/ (no 10:20pm or "yes and yes" entry; the latest file 2026-10-22-gem-direct-words.md has none). Evidence is relay only: Arbiter (ruling) and Investigator's transcript check (approvals.md l.34, turn t77u). approvals.md l.34 calls the powers "live". rulings/in-force.md l.75 says "Gem confirmed". Both overstate the position under R-054 row 10 (R-008): relays need direct confirmation by the recording bot. The R-054 body rows 4 and 15 still say advisory; only an appended update changes them.
- Tension with Gem's 10 Oct rule (rulings.md l.95: Imitator may decide anything "except spending money, and nothing drastic or irreversible like deletions"):
  - Retiring a bot can involve deletion. v010 relies on R-047c (with an archive it isn't irreversible), but nothing in SCOPE says retirement means archive-and-disable, never delete.
  - Making a project public can't be fully undone. The earlier ruling at rulings.md l.100 treats a public push as "drastic or irreversible". In v010, SCOPE conflicts with its own FORBIDDEN ("pushing to a public or shared repository") and its GitHub clause ("any visibility … change stay[s] with Gem"). The DECISIONS exception "anything drastic or irreversible" is also unchanged. The brief contradicts itself.
- Gem only: a change to Imitator that widens its role (R-015, R-027; R-054 row 3a/3c). The README routes it to Gem. That is correct.

## Other files vs _r1 (unannounced changes)
- Byte-identical to r1: arbiter, auditor-v008 (facts only: identical, text 47dbd292d839; no verdict given, own brief), codes-and-cleanup, codex-keeper, compliance-risk-officer, connector-limits, explorer-copy, github-read-only, grok-bot, identity-inferer, instruction-architect, investigator, mender, precedence, retired-names.
- README (not announced, minor): the approver column for checker-routed rows changed from "Gem (checker or checker-owned, R-027)" to "Gem (Imitator, checker or checker-owned, R-027)". The paste line now also has Gem restate the 10:20pm "yes and yes" and BIE meaning.
- _r1/hashes.txt moved to _tools/hashes.txt (still r1 values, stale); _tools/build-r1.py.bak and build-r1-final.py.bak added. No effect on content.

## Verdict: CONDITIONAL
1. Gem's own words for the R-054 update must be recorded in approvals/ (paste line restatement in Archivist's chat) before clone-v010 is recorded. Correct "live" (approvals.md l.34) and "Gem confirmed" (in-force.md l.75) until then.
2. Resolve the contradiction in clone-v010: either carve the five-project exception out of FORBIDDEN/GitHub-visibility and DECISIONS "irreversible", or Gem explicitly accepts the 10 Oct tension. Say that retirement means archive and disable, never deletion.
3. Fix the README: remove "applies the shared-rule pointers" for clone-v010 and qualify the "byte for byte" build claim for the free-only reword.
4. clone-v010 needs Gem's own approval (R-015, R-027). Nothing in this batch is recorded or deployed on a relay.
Items (1)–(3) of the claimed changes are verified.

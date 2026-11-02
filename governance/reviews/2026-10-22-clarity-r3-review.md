# Clarity batch revision 3: review (Scrutineer)
Date: 22 Oct 2026 (AEST). Read-only audit; this file is the only write.
Scope: proposals/2026-10-22-clarity/ (README sha 5c02703fd569) vs _r2/; prior review r2 (CONDITIONAL).

## Verdict: PASS (for the batch's construction). clone-v010 still needs Gem's own approval (R-015, R-027).

## 1. Changes vs _r2
- Only README.md and clone-v010.md differ. Every other draft is byte-identical to _r2.
- clone-v010 text hash is fbf614da2d3e (file hash b66cbcbc3460), as claimed.

## 2. clone-v010
- FORBIDDEN, the GitHub clause and DECISIONS each carry a narrow exception: approving one of the five named projects going public, after Safekeeper's secrets scan. The names match in all three places: VEPA, Codey, swarm, SLAP.RED/Golf, MedB.
- No other contradiction remains. "Every other public push or visibility change stays banned", Imitator never pushes itself, and merges, deletions and anything else irreversible stay advisory.
- Not wider than R-054. The R-054 update covers retiring bots and making projects public, and requires an archive or a Safekeeper scan first. The draft is narrower: it limits public projects to the five.
- SCOPE says retiring means a verified archive of brief and memory first, then archive and disable, never delete (R-047). Present.
- Diff against codex/clone/v009.md (c92d31926a18): the only changes are the DECISIONS exception sentence, "card t56s1" replaced with "the question card in your chat" (twice), INTERIM replaced with SCOPE, the GitHub exception and the FORBIDDEN exception. Nothing else changed.
- Minor wording: FORBIDDEN says "per SCOPE below", but SCOPE comes before FORBIDDEN in the text. Not blocking.

## 3. README fixes
- The "applies the shared-rule pointers" claim is withdrawn: clone v009 had none of the moved texts.
- "Byte for byte" is qualified for free-only (the build checks against the original FREE wording).
- The approver column and the build backups (build-r1, build-r1-final, build-r2 .bak) are announced.
- _tools/hashes.txt is regenerated. All 19 drafts' text and file hashes match the recomputed values. README and codes-and-cleanup.md (not drafts) aren't listed.
- The README carries the open condition: Gem's own words for the R-054 update must be recorded in approvals/.

## 4. Paste line
- Still says "I approve the clarity batch revision 2". Its clone-v010 hash is updated to fbf614da2d3e. It should say revision 3 before Gem pastes it.

## Notes
- Gem-only: clone-v010 (R-015, R-027). The R-054 update was relayed, so Gem's own words must be recorded first (R-008).
- auditor-v008 (Scrutineer's own brief) is unchanged from r2 (text hash 47dbd292d839). Facts only, no verdict on it.

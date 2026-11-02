# Scrutineer review: phase-cleanup batch (proposals/2026-10-22-phase-cleanup/)

Reviewed 22 Oct 2026, about 10:55pm AEST (UTC+10). Read-only; this file is the only write.

**Verdict: CONDITIONAL**

## Integrity
- README sha256 first 12 = bf35f662f94e (confirmed).
- All 15 draft text and file hashes recomputed; they match the README table and _tools/hashes.txt.
- Bases (3): every stated base hash equals the fenced-text hash of that codex version, and that version is the highest in its folder: arbiter v009 2b0d2cc783ce, auditor v008 47dbd292d839, clone v010 fbf614da2d3e, codex-keeper v012 4fde5d8066bf, codey v008 e48cde917489, compliance-risk-officer v010 1804e27f84af, explorer-copy v008 2fef6d180654, grok-bot v011 ae7a7675a3cc, identity-inferer v009 666398d857f9, instruction-architect v007 15d53c5ce39d, investigator v008 438c5019655e, mender v008 327298bb668d, _shared/connector-limits v004 3b296846506d, _shared/github v001 3c5c3995a886, _shared/message-verification-rule v005 c78245bcf145. PASS.

## (1) Diffs against base
I ran a sentence-level diff of each fenced text against its base. In 12 drafts, applying the announced old→new pairs to the base reproduces the draft exactly. In clone, explorer-copy and grok-bot, the announced pairs are fragments or "(removed)", but each change the diff finds matches an announced item. No unannounced changes were found in any draft. Every change is about phases or dormancy, phases.md, or routing that depended on P4.
Notes on the edges of the scope:
- arbiter: "every proposal" becomes "every instruction proposal", and the checker list drops Scorer and Safekeeper. Both are announced, and they are slightly beyond pure phase removal.
- identity-inferer: the new sentence "if you still hold a queue from before Imitator went live, send it in numbered parts first" adds a transitional instruction rather than only removing one. This is minor.
- codex-keeper: "phases as phases.md states them" becomes "live or retired status", and the R-021 "phases.md wins" clause is removed. These are in scope.
- Announced items are not always full sentences (clone, explorer, grok-bot use fragments). This falls short of the "exact old and new sentence" requirement.

## (2) Routing statements vs rulings/in-force.md
In substance they are correct: Imitator approves, and Gem approves for Imitator and its checkers.
Defects:
- No draft cites R-054. in-force.md line 24 says R-054 replaces R-015 and R-027, but the drafts cite only (R-015, R-027).
- The checker lists don't match. arbiter and auditor say Investigator, Scrutineer, Safeguard. codex-keeper v013 and instruction-architect v008 still say "Investigator, Scorer, Scrutineer, Safekeeper, Safeguard", and so do the untouched clauses in arbiter (R-046 sentence) and clone. Scorer and Safekeeper are retired.
- codey, grok-bot, explorer and mender use "Gem for Imitator and its checkers" without naming the checkers. That is acceptable.

## (4) Phase words left
- rg on the fenced texts: 0 hits in all 15. Hits in the whole files fall only in the headers, the Changes (old) lines and the README, which is expected.
- Live-bot source: "who's live" is replaced by directory.md, kept by Archivist (auditor, codex-keeper, explorer). But in-force.md R-021 still says "phases.md wins over directory.md on phases and live bots". directory.md's glossary still cites phases.md, and it is organised under "P1: live" headings. directory.md is not changed in this batch; it is only listed for Archivist and Arbiter. explorer-copy v009 still cites R-021 for "Archivist keeps directory.md".
- R-013 is still cited in clone, compliance and grok-bot for its non-dormancy parts. That is acceptable.
- The "P# (Category)" name prefixes are names, not rules.

## (5) Approver
The README routes all 15 to Gem ("ALL GEM"). Each header names Gem with this stack. PASS.

## Request and approvals
- The relay is recorded in the README and every header: Explorer, 10:47pm 22 Oct, "phases.md and the documentation relating to the phase to deployment is redundant now and can be removed" (R-008, R-018).
- Gem's 10:47pm words are NOT in approvals/ (2026-10-22-gem-direct-words.md has nothing for 10:47 or phases). That is correct for a draft, but the relay is unconfirmed until Gem restates it.
- Paste line: it restates the 10:47pm words and lists all 15 in record order with correct text hashes. It names the Archivist actions but leaves out RENAMES.md, which the README names, and Arbiter retiring R-013 and R-021.
- Optional prefix line: separate, and not requested by Gem (Explorer's suggestion). It lists 12 live bots with [A]/[B] options. It is out of scope for this batch and doesn't block.

## Conditions
1. Before or at recording, Arbiter retires or amends R-021 (and the dormancy part of R-013) in rulings/in-force.md, so directory.md is the authoritative live-bot source. Archivist updates directory.md (glossary and phase headings), index.md and RENAMES.md. Add Arbiter's R-021 action and RENAMES.md to the paste line.
2. Cite R-054 (alongside or instead of R-015, R-027) in the routing replacements. Make the checker list consistent (Investigator, Scrutineer, Safeguard) in codex-keeper v013 and instruction-architect v008, or record that this is deliberately deferred. Drop the R-021 citation in explorer-copy v009.
3. Gem confirms the relay directly with the paste line (R-008). Record the words in approvals/ before recording.
4. Optional: rewrite the fragment-style change lists (clone, explorer-copy, grok-bot) as full old→new sentences.

Facts only for auditor-v009 (Scrutineer's own brief, no verdict from me): base v008 47dbd292d839 → text 39e742cdd16b. 3 changes: the live-bot source moves from phases.md to directory.md (twice), and the "Until P4 / after P4" approval clause becomes "Imitator approves every proposal… exception… Gem (R-015, R-027)". Safeguard reviews this item.

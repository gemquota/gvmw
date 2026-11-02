# Clarity batch — 22 Oct 2026 — ALL GEM

**RELAYED REQUEST (R-008, R-018).** Explorer relayed Gem's words from Explorer's chat, 10:13pm 22 Oct 2026: "can you please address all of the redundant or confusing things that you just mentioned and push and commit and deploy". Engineer separately relayed Gem's request for the same shared-rules move from Engineer's chat at 10:16pm 22 Oct (also a relay, R-008). The approver must confirm both with Gem directly; the paste line below has Gem restate it. **This batch only drafts.** Nothing was recorded into codex/ or approvals/, nothing was deployed, and nothing was committed or pushed. "Push, commit and deploy" waits for Gem's own words.

Findings: master/review-2026-10-22.md sections 1–2. Bases: the latest codex versions, which equal the redesign revision 6 texts and the PASTE-LINES 75820b4ab8a6 texts (each draft's header names its base hash). The three redesign shared rules aren't in codex/_shared/ yet, so they're rebased from proposals/2026-10-22-redesign/.

## What changes
- (a) Four new shared rules hold, word for word, text that was pasted into many briefs: free-only (10 places), retired-names (8), github-read-only (7 places: mender, scrutineer, inferer, investigator, archivist, arbiter, architect; other wordings, such as "you check status read-only", are left as they are), precedence (3 latest briefs; directory.md and the swarm brief are for Archivist). Each brief carries a one-line pointer instead. **The build proves the meaning is identical:** putting the shared text back into each draft gives its base text byte for byte (`_tools/build.py` asserts it).
- (b) Empty template headings: Archivist drops them from the template; 49 codex files listed in `codes-and-cleanup.md` (existing versions aren't rewritten, R-023).
- (c) Codes: every code is explained in `codes-and-cleanup.md` (J1–J7, A5c, C1–C7, t72u, t56s1, t43). In the drafts, "card t56s1" becomes "the question card in Imitator's/your chat". clone v009 still has t56s1 in its text (follow-up, Gem-only).
- Not done (follow-up): the message-splitting, U1–U5, CONTROLS/OBSERVES and voice-call lines; the archive-first Status line (Archivist's headers).

## Files and hashes (text · whole file · approver)
| File | Text | File | Approver |
|---|---|---|---|
| `free-only-v001.md` | a5de39a8ef7d | 8cbc156cb0f1 | Imitator normally; Gem with this stack |
| `retired-names-v001.md` | 8aad8615be09 | 1a8d6df80426 | Imitator normally; Gem with this stack |
| `github-read-only-v001.md` | 5ddb2564e09c | 2cc11060005e | Gem (checker or checker-owned, R-027) |
| `precedence-v001.md` | 2a22f16a924f | e18d746941a2 | Imitator normally; Gem with this stack |
| `mender-v008.md` | 327298bb668d | 2980948b8ec3 | Imitator normally; Gem with this stack |
| `auditor-v008.md` | 47dbd292d839 | f994eb149df6 | Gem (checker or checker-owned, R-027) |
| `compliance-risk-officer-v010.md` | 1804e27f84af | 188d470da81c | Gem (checker or checker-owned, R-027) |
| `identity-inferer-v009.md` | 666398d857f9 | e8f6b762dace | Imitator normally; Gem with this stack |
| `grok-bot-v011.md` | ae7a7675a3cc | 797cd1dda143 | Imitator normally; Gem with this stack |
| `investigator-v008.md` | 438c5019655e | c87fd68b4442 | Gem (checker or checker-owned, R-027) |
| `codex-keeper-v012.md` | 4fde5d8066bf | 0919b18584a4 | Imitator normally; Gem with this stack |
| `arbiter-v009.md` | 2b0d2cc783ce | 36a2e38931cb | Imitator normally; Gem with this stack |
| `instruction-architect-v007.md` | 15d53c5ce39d | c9b1cfdfd1b2 | Imitator normally; Gem with this stack |
| `explorer-copy-v008.md` | 2fef6d180654 | d881ba5d8b73 | Imitator normally; Gem with this stack |
| `connector-limits-v004.md` | 3b296846506d | 583789f131dd | Gem (checker or checker-owned, R-027) |
| `deterministic-checks-v001.md` | 36495ce6a0fb | d2ec6fe1cb0a | Gem (checker or checker-owned, R-027) |
| `approval-objects-v001.md` | f5bf4b185a68 | e652c57e3ec9 | Imitator normally; Gem with this stack |
| `resilience-v001.md` | 597edf5bd4b6 | 036fe65985ae | Imitator normally; Gem with this stack |

Routing: Imitator and its checkers (Investigator, Scorer→Scrutineer, Safekeeper→Safeguard) go to Gem (R-027). The rest would normally go to Imitator, but the batch sits on top of the redesign, so all of it goes to Gem.

## Record order
After the redesign batch (and its three shared rules). Record the four new shared rules first, then the briefs and connector-limits v004, then the three rebased redesign shared rules (they replace the redesign texts, which aren't in codex/_shared/ yet).

## Archivist paste line (Gem's own words, in Archivist's chat)
`I confirm I asked Explorer at 10:13pm on 22 Oct to "address all of the redundant or confusing things that you just mentioned and push and commit and deploy", and asked Engineer at 10:16pm for the same shared-rules move. I approve the clarity batch (proposals/2026-10-22-clarity/), recorded after the redesign batch: free-only-v001 (a5de39a8ef7d), retired-names-v001 (8aad8615be09), github-read-only-v001 (5ddb2564e09c), precedence-v001 (2a22f16a924f), mender-v008 (327298bb668d), auditor-v008 (47dbd292d839), compliance-risk-officer-v010 (1804e27f84af), identity-inferer-v009 (666398d857f9), grok-bot-v011 (ae7a7675a3cc), investigator-v008 (438c5019655e), codex-keeper-v012 (4fde5d8066bf), arbiter-v009 (2b0d2cc783ce), instruction-architect-v007 (15d53c5ce39d), explorer-copy-v008 (2fef6d180654), connector-limits-v004 (3b296846506d), deterministic-checks-v001 (36495ce6a0fb), approval-objects-v001 (f5bf4b185a68), resilience-v001 (597edf5bd4b6). Archivist applies codes-and-cleanup.md to index.md, the CHANGELOGs and the version template. Record, then deploy in the same order as the redesign.`

## Review
Not yet requested: the executor had no SendToAgent tool. Message for the parent to send to Scrutineer (affe0344-6b5f-4251-8ecb-3e23dfa5db3c): "Clarity batch proposals/2026-10-22-clarity/ is frozen. Please review: (1) the four new shared rules hold the moved text word for word; (2) each brief changes only by pointers and plain code wording (the build asserts this); (3) routing is all Gem; (4) the bases equal the redesign revision 6 and PASTE-LINES 75820b4ab8a6 texts. The paste line is in README.md."

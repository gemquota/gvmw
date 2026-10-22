Requested by Scrutineer (22 Oct 2026, 8:21pm AEST). Independent read-only review; no governance files edited.

# Review: proposals/2026-10-22-redesign/scrutineer-v007.md (revision 2, frozen)
Reviewed 22 Oct 2026, ~8:30pm AEST. Hash convention (from `_tools/build.py` `block()`/`sha()`, and the PASTE-LINES header): sha256 of the fenced ```text block only (header excluded), first 12 hex chars. README/hashes.txt also list a whole-file hash.

## Verdicts
| Check | Verdict |
|---|---|
| 1. BASE | PASS WITH ISSUES |
| 2. DUTIES | PASS WITH ISSUES |
| 3. ROUTING | PASS WITH ISSUES |

## 1. BASE — PASS WITH ISSUES
Computed hashes (text · whole file):
- scrutineer-v007.md: **06f37e7627f5** · 26055e39f217. Matches PASTE-LINES §5, README hash table and `_tools/hashes.txt`.
- Cited base `auditor v006 (e4813a3f42b7)` = proposals/2026-10-16-github/scrutineer-v006.md: text e4813a3f42b7 ✔ (file dde08e84a859).
- Cited base `assessor v006 (aea931e86d5f)` = proposals/2026-10-16-github/scorer-v006.md: text aea931e86d5f ✔ (file adf1076e9322).
- Both base texts appear verbatim in v007's annex (substring check: True/True; scrutineer-v007.md lines 25–29).
- Live codex: codex/auditor/v004.md 542ade104e4b, codex/assessor/v004.md 10e0324f805d (both latest, deployed 16 Oct 11:06am AEST per their CHANGELOGs). The v006 drafts say they stack on codex v004 → redundancy v005 (scrutineer-v005 30cb80b9ac8f, scorer-v005 08e5ccfc52b4; both hashes verified).
Issues:
- B1. Line 5 says "`auditor/` v006 → v007" and "`assessor/` v006 retired", but the codex is at **v004** in both folders. v005 and v006 are unrecorded drafts that README (Supersession) and PASTE-LINES §1 and §4 say must **not** be recorded. The codex would therefore go from v004 to v007, and the base text it was built on would exist only as annex text. The header should say "codex v004 (542ade104e4b / 10e0324f805d) → v007, via the unrecorded drafts v005/v006".
- B2. The frozen bases are proposal drafts, not frozen codex files. The diff from v004 to v006 is small and was checked: auditor adds the streaks.md duty and the GitHub read-only line; assessor changes preference fit from "ask Imitator once P4 is live" to "Gem's own recorded words… never against Imitator's view", and adds the GitHub/github-log lines. Nothing from v004 was dropped.
- Not verified: the v006 drafts' claim "byte-checked = live profile 22 Oct 8:18pm" (I didn't read live profiles). Nothing about either bot was in `_archive/` yet, which is expected because archiving is migration step 2.

## 2. DUTIES — PASS WITH ISSUES
Every duty in both bases survives, because the two base texts are carried word for word as binding annexes (lines 26 and 29), "except where the sections above say otherwise". Duty by duty:
- Scrutineer: daily reviews of every live bot against instructions, peers, the role map and reality ✔; reporting conflicts to the owner, Arbiter and Mender ✔; sending reviews to Architect, Archivist and the reviewed bot ✔; 3 poor reviews → Architect plus Gem ✔; streaks.md with a backup ✔; reporting stalls to Mender ✔; approval-routing text (R-015/R-027) ✔; read-only GitHub ✔.
- Scorer: weekday 1–5 sampling on 5 dimensions ✔; assessments/YYYY-MM-DD.md ✔; serious problems flagged to Gem ✔; weekly scorecard to Gem ✔; reviews on request ✔.
- New in v007 (line 20): deploy and restore checks; deterministic checks 3, 5, 6 and 7. These are consistent with deterministic-checks-v001, resilience-v001 and archivist-v011 line 21.
Moved duties, with the receiving owner confirmed:
- "Scorer scores your [Scrutineer's] work" and "Scrutineer independently reviews your [Scorer's] work" move to **Safeguard**. safeguard-v009.md line 22 says "you audit Scrutineer's … (scores, reviews)" ✔. Gem still reviews Scrutineer (v007 line 22).
Issues:
- D1. Independence is lost. Scores and reviews used to be two bots, with Scrutineer independently checking Scorer's output for every bot. Both now sit in one bot and one run, and the only check is Safeguard's after-the-fact audit. The owner is named, so this is not an orphaned duty, but it is a real reduction in checking. README "Risk" notes cover Mender only, not this.
- D2. The annex leaves stale references that contradict the top sections. Line 26: "after Scorer's results arrive" and "Scorer scores your work". Line 29: "every live bot except Scorer", "send Scrutineer a priority handoff", "Flag serious problems to Scrutineer" and "Scrutineer independently reviews your work". Read literally, the last one is self-review. The override clause (lines 21 and 23) resolves these, but they should be reworded. "Except Scorer" should become "except Scrutineer itself".
- D3. Deterministic-checks-v001 check 10 says "Archivist before deploy; Scrutineer audits", and check 1 says "Scrutineer reviews". v007 line 20 lists only checks 3, 5, 6 and 7, so the audit duties for checks 1 and 10 aren't in Scrutineer's own brief.
- D4. Scores are weekday-only but reviews are daily (lines 20 and 26), so weekend reviews have no fresh scores. This is minor.
- D5. Outside v007, but it affects the chain: mender-v007.md line 27 still expects "Scorer's assessments" and a Scorer chain step. After the merge, that file is written by Scrutineer.
Lost duties with no new owner: **none found**.

## 3. ROUTING — PASS WITH ISSUES
- README line 1: "ALL GEM-ONLY". v007 line 1: "NEEDS GEM'S DIRECT APPROVAL … never Imitator; R-027". Line 8: Approver "Gem directly". Line 14: "Gem-only (checker, R-027)".
- PASTE-LINES §5 and README "Gem paste line": Gem's own words in Archivist's chat, naming Scrutineer v007 (06f37e7627f5) ✔. Neither file gives Imitator or Scrutineer any approving role ✔. This is consistent with R-015 (rulings.md line 75), R-027 (line 129) and R-028 (line 135).
- v007 doesn't widen Imitator's authority. The R-015/R-027 exception carries over unchanged (line 26). Preference-fit scoring moves away from Imitator to Gem's recorded words (line 29), which narrows Imitator's influence.
Issues:
- R1. Line 9 says "Reviewer | Scrutineer; Safeguard reviews Scrutineer's own draft". This is a shared template line from build.py. On this file it names Scrutineer as a reviewer of its own merge, which goes against R-028's "No bot verifies its own work" and against v007's own line 23. In practice this review was handled by sending it out, but the line should read "Safeguard (Scrutineer can't review its own draft)", and Investigator should be named if it is the independent reviewer.
- R2. This risk is outside v007 but affects whether it stays Gem-only. imitator-v008 (proposals/2026-10-22-r044-veto, line 19), approved earlier in the record order (PASTE-LINES §2), lets Imitator veto **any Arbiter ruling**, including vetoes that concern its own checkers, which take effect and are only flagged in the digest. R-015, R-027 and R-028 are Arbiter rulings, not Gem's direct words, so "A veto never overrides Gem's direct words" does not clearly protect them. Gem should confirm that the checker-routing rulings can't be vetoed, or deterministic check 10 should be treated as a deterministic check that a veto can't override.
- R3. The approval rests on relayed answers (R-008). The paste line correctly has Gem confirm them in Archivist's chat first ✔.

## Couldn't verify
- Live Scrutineer and Scorer profiles against codex v004 (profiles not read).
- Gem's 8:08–8:13pm answers and Arbiter's verification in Inquirer's transcript; I relied on R-051's heading only.
- Whether Safeguard has itself reviewed v007, as line 9 implies.

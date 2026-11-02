# Dry run: public GitHub Pages site for governance docs (22 Oct 2026, 22:07 AEST)

Requested by Gem per Explorer (10:05pm AEST 22 Oct 2026), relayed and not verified. Reviewer: P1 (Checks) Safeguard. Read-only; nothing pushed, published, moved or shared. Held area /workspace/backups/bie-caches-2026-10-10/ not read.
Relied on: codex compliance-risk-officer v006; connector-limits v003 (rules 6 and 14; the gvmw exception "covers no other repo, fork, gist, Pages site").

**A dry run is not a sign-off. The go/no-go is Gem's.**

## Files located
| # | Item | Exact file(s) |
|---|---|---|
| 1 | Master doc A | governance/master/governance-master-2026-10-22.md (8,452 lines) + .html render |
| 2 | Master doc B | governance/master/governance-master-latest-2026-10-22.md (4,256 lines) + .html render |
| 3 | Role map | governance/cartography/role-map-interactive.html (latest numbered: role-map-v20.mmd/.svg/.png). Which one is meant is ambiguous; confirm. |
| 4 | 15 Oct authority report | governance/reviews/2026-10-15-governance-authority-responsibility.md / .html / .png |
| 5 | 10 Oct I/O report | governance/reviews/2026-10-10-governance-io-report.md / .html / .png |
| 6 | Workspace map | /workspace/workspace-map.html (817 KB; one huge embedded-JSON line, 216) |

## Findings per file
### 1 and 2: master docs (HIGH, do not publish as-is)
- Account handles: about 150 lines (A) and 130 (B) name gemquota, slapredgit, slapredpokies, artifactrap and DayneK, e.g. A:155/B:154 "gemquota/gvmw", A:1421–1438 (R-040 narrative).
- Masked emails of real people: A:5659–5663, 5713 / B:3420–3424, 3474: "person's PayID email (`yvon***@gmail…`)", "`dayn***@gmail`", "`gemq***@gmail`". Partly masked, but they still point to a real person and a payment identifier. The real name "Dayne" appears about 61 (A) and 53 (B) times.
- Identity/ID notes about Gem: about 42 (A) and 32 (B) lines, e.g. A:248/B:265 "/workspace/id-notes/gem-profile.md", A:1215/B:731 "factcheck-2026-10-10.md", B:951 "The public content includes personal data: id-investigator/factcheck…".
- Credentials: no live secret found. Hits at A:4863/B:2624 (a gh credential-helper command line, no value), A:5226/B:2987 (a redaction regex), A:5687–5691/B:3448–3452 (descriptions of false positives) and A:7304 (sk- false positive). These go to Safekeeper for confirmation. The command line shows how gemquota is authenticated on the box.
- BIE/gambling: about 185 (A) and 145 (B) lines, e.g. A:149 "BIE … gambl…", A:1276/B:788 "bonus_scores_AU.xlsx", A:1332–1357 (R-031 hold and Gem's "public" words). There are also references to the bonus_terms material.
- Private paths: about 600 (A) and 390 (B) /workspace/ paths, plus 34 (A) and 31 (B) mentions of bie-caches or /workspace/backups.
- Bot ids: 275 (A) and 92 (B) lines with bot UUIDs, e.g. A:241–244 (directory table).
- Also: the full internal governance, risk register narrative, incidents (RR-045) and Gem's quoted words.
- The HTML renders have the same content (A.html: 277 bot-id lines, 148 handle lines, 66 casino/pokies/bonus_scores lines; B.html: 94/123/60).
### 3: role map (LOW)
- role-map-interactive.html line 96: one BIE mention and one /workspace/governance/directory.md path. v20.mmd: no hits.
### 4: 15 Oct authority report (LOW)
- .md line 150: "Extractor | BIE/research datasets and scrapers". No PII, ids, paths or secrets. The .html had no hits.
### 5: 10 Oct I/O report (LOW–MEDIUM)
- .md lines 29, 197, 213 mention BIE ("RR-002 (BIE legal)"); line 8 has a /workspace/ path; .html lines 162 and 481 are similar. No PII or secrets found by the scan.
### 6: workspace-map.html (HIGH)
- Line 216 (embedded JSON tree) lists the whole box: id-notes (marked private), bonus_terms_AU.xlsx/.rows.json/_anomalies/_dups, page_truebluepokies…html and page_pokiesmate…html (pokies/casino sites), "BIE … casino-bonus", backups/bie-caches-2026-10-10 (held), 3 UUID-named files, and every private path.
- Not checked: PNG images (OCR not run). If they're included, they need a visual check.

## Breaches of connector-limits v003
- Rule 6: the ban on gambling, casino, pokies and BIE-derived content on any public page applies. Files 1, 2 and 6 breach it (and 3–5 contain light BIE mentions). The gvmw exception in rule 14 expressly doesn't cover any Pages site, even one built from gvmw.
- Rule 14: a Pages site is a new public GitHub target and new content. It needs Gem's direct words naming it. Explorer's relay doesn't count (R-019). It follows the shared GitHub rule (Engineer writes).
- Rule 15 and RR-008/010: third-party personal data (masked emails, real names) going to a public page.

## Predicted effects of public exposure
Permanent in practice: Pages is crawled and indexed (Google cache, Wayback), and the source repo can be cloned or forked. Deleting it later doesn't recall copies. It would expose Gem's account map (which helps phishing and account takeover), the identity notes, third-party data, the IGA advertising risk from the casino/pokies/bonus content, and the box layout and backup locations.

## Options (Gem's call)
1. **Publish as-is:** not advised. It breaches v003 rule 6, and needs Gem's words plus a v003 change.
2. **Redact list:** remove or replace in all files: account handles and emails (including masked ones), "Dayne" and the PayID reference, id-notes/factcheck/gem-profile references, every BIE/gambling/casino/pokies/bonus_* passage, /workspace and /cursor paths, backup and bie-caches paths, bot UUIDs, and the gh credential-helper line. Then Safekeeper re-scans and Safeguard runs a fresh dry run. For the master docs this is a large edit, so a purpose-written public summary is more practical.
3. **Exclude files:** publish only 3 (v20 .mmd/.svg, or interactive with line 96 cleaned), 4 (line 150 BIE wording reworded) and 5 (BIE lines and path reworded). Exclude 1, 2 and 6.
4. **Keep private:** GitHub Pages from a private repo isn't available on the Free plan (it needs Pro/Team, and even then the site is public unless it's an Enterprise private site). The private option is to keep the files in a private repo or on the box, not on Pages.

Safeguard's view: option 3, or option 4 for the master docs and workspace map. This informs only.

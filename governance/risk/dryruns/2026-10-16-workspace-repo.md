# Dry run: Mediator's private whole-workspace repo (RR-043)
Staging: /workspace/_repo-staging/workspace-snapshot, commit ed9e875, 3,807 files, 132 MB, no remote. Planned target: a new PRIVATE repo under DayneK (proposed name DayneK/gem-workspace). Based on: safeguard v006, connector-limits v001, rulings R-020, R-031 (amended) and R-036, plus Gem's words of 3:44pm and 3:47pm ("Include both"). This is a dry run, not a go-ahead. The go is Gem's and Mediator's.

## Independent check (Safeguard, read-only, 3:52pm)
- Held items: none of these paths are present (bonus_scores_AU.xlsx, bie-caches, *.zip, test_scrape_site.py, api_tokens, sync_tokens, cookies, storage state, .env).
- Token-pattern scan (GitHub, OpenAI-style, AWS, Google API, Slack, private keys, JWT): no live values. The only hits are two lines of governance prose.
- Password scan: only code that reads passwords from config, plus one example value in a vendor HTML doc (bie_tools/k3.html). No real values found.
- This is a pattern check, not proof. Safekeeper owns secrets.

## Predicted effects and concerns
1. **The R-031 hold is bypassed through source data.** bonus_scores_AU.xlsx is excluded, but its source data is included: bonus_terms_AU.csv/.xlsx (in both bie_deliverables/reports and bie_tools) and the bie_tools/pstats/bonus_terms_AU_* JSON files, along with the scoring script. Anyone with access can rebuild the held spreadsheet. Gem's "Include both" covers BIE data in general but doesn't name these files. They need either Gem's words naming them or exclusion.
2. **Third-party personal data.** bie_tools/pstats/sites_config.csv (11 MB) contains a private individual's gmail address and about 41 phone-like numbers. bie_tools/leads_homepages.txt has 5 phone-like numbers, and other bie_tools page or JSON files have a few more. These look like contact data for operators, affiliates or people (RR-008/RR-010). Gem's "Include both" was about BIE data and Gem's own identity notes, not other people's contact details. Gem should know this specifically.
3. **Gem's own data.** governance/, id-investigator/, id-notes/ and profile.txt include Gem's email addresses and identity notes. Gem approved this at 3:47pm.
4. **Private isn't permanent.** The DayneK classic token has admin and delete_repo (RR-033). Any bot or leaked token could make the repo public, add collaborators or clone it. A copy on GitHub also falls under GitHub's terms and is held on GitHub's servers. Making it public later, or adding collaborators, comes to Safeguard first (R-020).
5. **Offshore gambling data on GitHub.** BIE scraping and AU pokies data in a private repo carries a low risk of the GitHub account being actioned under GitHub's terms. That isn't verified against the current policy text.
6. **Reversibility.** A private repo can be deleted later, but GitHub may keep backups for a while. Deleting it counts as a deletion and needs Gem's direct words.

## Options for Gem
A. Push as staged.
B. Exclude the bonus_terms_AU source files and third-party contact data (sites_config.csv, leads_homepages.txt and the page dumps containing phone numbers), then push.
C. Exclude all BIE folders.
D. Don't push, and keep the workspace on the box only.

## CORRECTION (2026-10-16 15:52:47, after Safekeeper T-017)
My "no live secrets" finding was wrong. Safekeeper found things my pattern check missed: three committed config.ini files with logins set, three sk-shaped strings (urls.txt:33, governance/bot-landscape-review.md:84, medb-research/medb-prior-work.md:60), and two files with personal details (the T-005 incident file and id-investigator/factcheck-2026-10-10.md). My sk- pattern was too narrow, and I didn't scan config.ini files. Safekeeper has sent Mediator exclusions and asked for the commit to be rebuilt. This dry run applies to ed9e875 only. A rebuilt commit needs Safekeeper's re-check and a fresh Safeguard dry run before Gem's final words.

## FRESH DRY RUN: e21adc3 (2026-10-16 15:56:52)
3,805 files, no remote, ed9e875 gone. Safekeeper passed it on credentials (T-017). My own token-pattern scan shows only prose and URL matches, with no live keys found. Still open, both for Gem to decide:
1. **R-031 source data is still included.** bonus_terms_AU.csv/.xlsx (in bie_deliverables/reports and bie_tools), bie_tools/pstats/bonus_terms_AU_*.json and k_bonus_terms_au.py. From these, anyone could rebuild the held bonus_scores_AU.xlsx.
2. **Other people's contact details are still included.** bie_tools/pstats/sites_config.csv (with a private person's gmail and about 41 phone-like numbers), bie_tools/leads_homepages.txt, harvest_homepages.json, page_audplay.online.html and two CDN JSON files. The phone-like hits in the governance SVGs are probably false positives.
3. **Personal-detail file Safekeeper flagged.** id-investigator/factcheck-2026-10-10.md is still in. The identity notes fall under Gem's "Include both", but Safekeeper named this file. Mediator should confirm whether it was meant to stay.
Predicted effects are otherwise unchanged from points 3 to 6 above. The options for Gem are still A to D. This is not a go-ahead. The push needs Gem's final words for this push.

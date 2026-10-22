# Optional proposal: fold Extractor into Emissary — NEEDS GEM'S DIRECT APPROVAL (Gem's alone, R-019; a separate yes/no in Archivist's chat; never Imitator)

| Field | Value |
|---|---|
| Source | Imitator's assessment (reviews/2026-10-22-redundancy-assessment-imitator.md): "Make Extractor collection and scraping only, or fold it into Emissary after archiving it". Gem's reply relayed by Imitator, 22 Oct 7:07pm (R-008): "Yeah fix those and proceed as suggested" |
| Approver | **Gem directly, and only Gem.** Retiring or folding a bot is irreversible (R-019), and it changes a shared rule (R-027) |
| Reviewer | Scrutineer; Safeguard dry-runs the merged brief |
| Status | **Not ready for a yes.** Gem's yes can only come after the merged Emissary brief and connector-limits update below are drafted and reviewed. They aren't drafted now |
| Depends on | The main batch (emissary-v007, extractor-v006, explorer-v006 in this folder) being recorded first |

## What the fold needs before Gem can say yes
1. **A merged Emissary brief with a wall between posting and scraping.** Emissary is the only poster. The merged brief must keep any scraped data (BIE and gambling data above all) away from anything Emissary posts or publishes, carry Extractor's collection rules word for word (public data only, robots.txt and terms, no evasion, no credentials, a Safeguard dry run before each new job, target or scope change, datasets stay on the box), and have Safeguard dry-run the wall.
2. **R-031 and RR-015 carried over unchanged.** The R-031 hold on bonus_scores_AU (and R-031 permission rules generally), RR-015's pause on the scraper zip, and the open decisions on the 44 AU sites, the 3 unknown sites and the lists-only zip all move to Emissary word for word, with nothing lifted by the fold.
3. **connector-limits updated.** connector-limits names Extractor as the Apify runner ("Extractor runs Apify") and as the owner of scraping under notebooks. A further connector-limits version has to name Emissary instead, keeping every Apify limit. That's a shared-rule change for Gem (R-027).
4. **Records updated:** the role map (Archivist), phases.md (Explorer) and Explorer's assignment list.

## How it would happen, if Gem says yes after those
1. **Archive first, delete nothing.** Archivist copies `codex/scraper/` (v001–v005 and the CHANGELOG) and Extractor's work files to `/workspace/governance/_archive/extractor-fold-<date>/`, checks the copy and says where it is. The codex folder and Extractor's agent folder stay.
2. **Extractor is recorded as retired** (folded into Emissary) only when the merged Emissary brief and the connector-limits update are both deployed. Explorer stops assigning to it then.

## For and against
- **For:** one owner for research and collection, with no hand-offs.
- **Against:** the only poster would also hold scraped BIE and gambling data. Today the split keeps them apart by default, so the wall above is essential.

## Not decided here
This proposal changes no brief. Without Gem's yes, the main batch stands alone, and Extractor keeps collection and scraping.

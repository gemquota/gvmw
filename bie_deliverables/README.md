# BIE Scraper — organised files

Snapshot organised 4 Oct 2026 (AEST). Counts are merchants/sites as of this date.

## scraper/
The Bonus Intelligence Engine project, ready to run (virtualenv and caches removed).
Fixes already applied: err/log + db auto-create, fresh-DB setup order, AbuseIPDB
ts/timestamp column + migration, dashboard bound to 127.0.0.1 with auth on every route.
NOTE: in/config/config.ini contains your account logins — keep private.
The engine reads in/config/urls.txt only; swap in another list by copying over it (keep a backup).

## lists/all/  (every country)
- urls_original.txt      580  — your starting list, unchanged
- urls_combined.txt    7,629  — original + all confirmed new domains (incl. mirrors), deduped
- newurls_found.txt    7,049  — the confirmed new domains alone
- urls_by_merchant.txt 1,847  — one verified working URL per merchant ID
- urls_by_merchant.csv        — same, with merchant_id, merchant_name, mirror_count, checked_at

## lists/australia/  (AUD sites)
- urls_au.txt         1,055  — one verified URL per Australian merchant
- urls_au.csv                — same with merchant details
- au_registered.csv     422  — AU sites your records tie to an account (all under U1)
- au_unregistered.csv   558  — AU sites with no account on record (+ .txt)
- au_unknown.csv         75  — AU sites matched to old records by brand name only (unclear)

## reports/
Partnership files here are AU-ONLY (Australian / AUD sites; rebuilt offline 10 Oct 2026).
The all-countries versions are in reports/_all-countries/.
- partnership_stats_AU.xlsx  — AU-only partnerships table (Partnerships / Sites / Notes sheets)
- partnership_stats_AU.csv   — AU-only, one row per partnership group
- partnership_sites_AU.csv   — AU-only, one row per site
- partnership_summary_AU.md  — AU-only method + caveats
- partnership_sites_unknown_country.csv — sites with no country, left out of AU files (to review)
- reachability.csv           — per-site no-login check results for the original 580
- newurls_found_detail.csv   — every new domain with merchant, source, mirror flag
- DISCOVERY.md               — how sites were discovered (repeatable method)

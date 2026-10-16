# AU-ONLY Partnership bonus stats (Australian / AUD sites only; public data only, no login)

AU-ONLY. Built offline 2026-10-10 13:10 AEST from existing data already on disk (no scraping or network); bonus terms are the 2026-10-02 public snapshot. Files: partnership_stats_AU.csv / partnership_stats_AU.xlsx (sheets Partnerships, Sites, Notes), partnership_sites_AU.csv, partnership_sites_unknown_country.csv. All-countries versions: reports/_all-countries/.

## AU scope
- Of the 1615 member sites in the all-countries build: 540 AU, 622 unknown country, 453 excluded non-AU (MY 378, PG 30, SG 29, HK 10, NP 4, BN 1, KH 1). 540 + 622 + 453 = 1615.
- AU basis: country=AU / currency=AUD field 540; blank country+currency matched exactly by merchant_id 0, by host 0, by sites_config 0.
- Unknown-country sites (622, all domain-only members with no merchant ID, country or currency) are EXCLUDED from every AU count and stat; they are listed with their current group ids in partnership_sites_unknown_country.csv for review.

## Coverage
- Partnership rows: 262 AU groups (of 755 all-countries groups; 493 dropped for having <2 AU sites), clustered into 173 families (`family_id`, Jaccard >= 0.8 on AU member sets vs the family's largest group). Group ids are kept from the all-countries build for traceability; rows are ordered by AU site count.
- AU member sites: 540 distinct (521 in at least one surviving AU group; 19 AU sites have n_partnerships = 0 because all their groups had <2 AU sites); 540 resolved to a merchant ID; 537 have public promotion data (99.4% of AU sites).
- Of AU merchant sites: no-deposit found 451, welcome deposit found 506.
- Field fill (AU merchant sites): nd_amount 448, nd_win_over 448, nd_max_cashout 440, nd_turnover_x 27, nd_min_withdraw 20, wl_pct 484, wl_fixed 21, wl_max_bonus 90, wl_min_deposit 504, wl_win_over_x 481, wl_turnover_x 284, wl_min_withdraw 13, wl_max_withdraw 306
- Currency mix of AU merchant sites: AUD 540

## Top 10 AU partnerships by AU site count (largest group per family)

| # | partnership | family | AU sites | w/ data | currency | % reach | % ND | ND amt min/avg/max | ND win-over avg | ND max cashout avg | WL % avg | WL min dep avg | WL win-over x avg | WL turnover x avg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Partnership (https://eb7png.com/partnership) | F0001 | 37 | 37 | AUD:37 | 100.0 | 94.6 | 18.0/54.18/99.0 | 1015.8 | 20.56 | 59.94 | 31.43 | 5.57 | 5.83 |
| 2 | Exclusive Alliance Partnership (https://megabet26.com/eap) | F0002 | 29 | 29 | AUD:29 | 100.0 | 58.6 | 9.0/16.13/31.0 | 274.29 | 25.94 | 64.59 | 51.11 | 5.33 | 7.74 |
| 3 | testnew par (https://1313au.com/testnewpartner) | F0003 | 27 | 27 | AUD:27 | 100.0 | 81.5 | 10.0/149.44/399.0 | 419.95 | 30.28 | 84.58 | 32.2 | 4.56 | 4.76 |
| 4 | partnership (https://7mg.online/partnership) | F0004 | 27 | 27 | AUD:27 | 100.0 | 96.3 | 18.0/48.06/96.0 | 808.13 | 20.77 | 63.92 | 32.0 | 5.8 | 5.83 |
| 5 | partners (https://cgroup05.vip/partners) | F0005 | 25 | 24 | AUD:25 | 100.0 | 100.0 | 13.77/18.57/22.0 | 186.08 | 19.83 | 86.96 | 844.42 | 5.25 | 4.91 |
| 6 | Partnership – SPACE77, CRYSTALBET777, ROYALAUD, HARBOUR33, SOLIDLUCK33, SPINSAGE33, HOLLYWOODAUS, WINSHIFT77, TOPAZ33, LUCK777, POKIESCLUB (https://royalaud.com/luxepartner) | F0006 | 24 | 24 | AUD:24 | 100.0 | 75.0 | 8.0/44.67/200.0 | 877.11 | 19.94 | 44.1 | 23.81 | 3.86 | 4.0 |
| 7 | partner (https://saferoox.com/partner) | F0007 | 22 | 22 | AUD:22 | 100.0 | 100.0 | 9.6/15.29/23.0 | 172.12 | 31.64 | 77.49 | 70.45 | 7.32 | 6.17 |
| 8 | Partnership – SPEEDAU , SPEEDAU2 , SPEEDAUVIP , TAXIS33 , TOKENAUD , ETHBET , SPEEDX (https://bfmtaxis33.online/bfmpartner) | F0008 | 20 | 20 | AUD:20 | 100.0 | 70.0 | 10.0/39.5/100.0 | 592.0 | 18.0 | 42.71 | 22.06 | 3.47 | 4.0 |
| 9 | trypartner (https://ioi6.com/trypartner) | F0009 | 18 | 18 | AUD:18 | 100.0 | 100.0 | 9.99/14.53/23.0 | 162.32 | 27.39 | 79.76 | 74.71 | 6.82 | 4.56 |
| 10 | partner (https://betworld96.com/partner) | F0010 | 16 | 16 | AUD:16 | 100.0 | 87.5 | 28.0/53.63/96.96 | 955.69 | 20.0 | 50.62 | 30.0 | 4.69 | 4.0 |

## Method
- Built offline by g_build_au.py / j_md_au.py / h_report_au.py (bie_tools/pstats), reusing g_build.py logic unchanged (verified: with the AU filter off it reproduces the all-countries partnership_stats.csv and partnership_sites.csv byte-for-byte). Inputs: groups.json, sites_config.csv, by_merchant.jsonl, members_check.csv, pubinfo.jsonl, partnership_sites.csv, urls_au.csv.
- AU classification (au_classify.py): AU = country AU or currency AUD. Sites with blank country and currency become AU only on an EXACT merchant_id match to urls_au.csv, an EXACT normalized host match (lowercase, no scheme/www./path) of site / verified_url / any_known_domain to urls_au hosts, or an exact host / merchant_id AU/AUD entry in sites_config.csv. No fuzzy or brand-name matching; anything else is UNKNOWN and excluded.
- Regrouping: each all-countries group keeps only its AU members; groups with <2 AU sites are dropped; every count, percentage, stat, currency_mix, stats_currency, member_sites, common_bonus_names, deposit methods, n_domains and family_id is recomputed on AU members only. Each AU site's n_partnerships / partnership_ids list only surviving AU groups.
- Original sources of the data (unchanged): partner directories from cached homepages via public `/page/getPage`; bonus terms from public `/merchants/getPublicInfo` (2026-10-02); reachability from no-login checks (2026-10-02).

## Caveats
- Money stats (amounts, win-over, cashout, deposits) are computed over sites in the group's main currency (`stats_currency`, AUD for every AU group).
- One "main" no-deposit and one "main" welcome promo per site (lowest displayOrder among classified promos). Sites often run several; others are ignored.
- Classification of promos is heuristic (name keywords + claimCondition + deposit terms). Some "free credit" promos needing a deposit or app download may be misclassified.
- `minWithdraw` is platform-ambiguous: for no-deposit promos it is treated as the win-over target amount (`nd_win_over`); for deposit promos as a win-over multiplier (`wl_win_over_x`). Values <1 are treated as ratios, not money.
- Groups are exact site sets in the all-countries build; after removing non-AU members some groups have identical AU member sets (kept as separate rows; same family_id). Use `family_id` to roll up. A site can belong to many groups.
- Unknown-country sites are excluded, so AU groups can under-count real AU membership. 8 unknown sites have a merchant ID in members_check.csv that is in urls_au.csv; this is shown as a review hint only and was NOT used to classify them.
- Blank cells = not published / not parsed; nothing imputed or invented. Terms are a 2026-10-02 snapshot and change often.

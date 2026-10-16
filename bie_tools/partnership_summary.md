# Partnership bonus stats (public data only, no login)

Built 2026-10-02 (AEST). Files: partnership_stats.csv / .xlsx (sheets Partnerships, Sites, Notes), partnership_sites.csv.

## Coverage
- Partnership rows: 755 exact-membership groups (>=2 sites; directories listing the identical site set collapsed), clustered into 505 families (`family_id`, Jaccard >= 0.8 vs the family's largest group). 193 directory pages listing <2 sites excluded.
- Member sites: 1615 distinct; 993 resolved to a merchant ID; 990 have public promotion data (61% of all sites, 99.7% of merchant-ID sites). The rest are domains with no working site (DNS dead, parse failed) or newly confirmed members not yet fetched.
- Of merchant sites: no-deposit found 866, welcome deposit found 941.
- Field fill (merchant sites): nd_amount 862, nd_win_over 852, nd_max_cashout 777, nd_turnover_x 44, nd_min_withdraw 116, wl_pct 915, wl_fixed 24, wl_max_bonus 217, wl_min_deposit 938, wl_win_over_x 885, wl_turnover_x 595, wl_min_withdraw 18, wl_max_withdraw 404
- Currency mix of merchant sites: AUD 540, MYR 378, PGK 30, SGD 29, HKD 10, NPR 4, BND 1, USD 1

## Top 10 partnerships by site count (largest group per family)

| # | partnership | family | sites | w/ data | currency | % reach | % ND | ND amt min/avg/max | ND win-over avg | ND max cashout avg | WL % avg | WL min dep avg | WL win-over x avg | WL turnover x avg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | SamaMenang Partnership (https://limau55.co/samamenangpartnership) | F0001 | 45 | 41 | MYR:41 | 93.3 | 100.0 | 5.0/34.25/300.0 | 685.34 | 21.02 | 49.76 | 10.2 | 4.08 | 4.26 |
| 2 | SamaMenang Partnership (https://bandarj33.com/samamenangpartnership) | F0002 | 44 | 43 | MYR:43 | 97.7 | 100.0 | 5.0/35.89/300.0 | 725.56 | 23.05 | 50.93 | 10.26 | 4.24 | 4.44 |
| 3 | samamenangpartnership (https://spinking33.club/samamenangpartnership) | F0003 | 44 | 39 | MYR:39 | 93.2 | 100.0 | 5.0/38.65/300.0 | 782.0 | 21.35 | 50.26 | 9.51 | 4.13 | 4.34 |
| 4 | 4DGang Partnership (https://jd88.xyz/4dgangpartnership) | F0004 | 43 | 40 | MYR:40 | 95.3 | 100.0 | 5.0/37.49/300.0 | 749.98 | 22.55 | 51.0 | 9.53 | 4.33 | 4.58 |
| 5 | Partnership (https://eb7png.com/partnership) | F0005 | 43 | 39 | AUD:37, PGK:2 | 97.7 | 94.6 | 18.0/54.18/99.0 | 1015.8 | 20.56 | 59.94 | 31.43 | 5.57 | 5.83 |
| 6 | 4DGang Partnership (https://h2m.club/4dgangpartnership) | F0006 | 42 | 40 | MYR:40 | 95.2 | 100.0 | 5.0/36.61/300.0 | 732.48 | 22.64 | 50.75 | 9.3 | 4.0 | 4.18 |
| 7 | SamaMenang Partnership (https://dmcslot.asia/samamenangpartnership) | F0007 | 42 | 39 | MYR:39 | 95.2 | 100.0 | 5.0/35.17/300.0 | 715.36 | 22.7 | 51.03 | 8.15 | 4.05 | 4.24 |
| 8 | SamaMenang Partnership (https://bantu88a.com/samamenangpartnership) | F0008 | 42 | 39 | MYR:39 | 95.2 | 100.0 | 5.0/38.96/300.0 | 799.95 | 23.57 | 51.54 | 8.49 | 4.32 | 4.56 |
| 9 | Exclusive Alliance Partnership (https://megabet26.com/eap) | F0009 | 42 | 29 | AUD:29 | 71.4 | 58.6 | 9.0/16.13/31.0 | 274.29 | 25.94 | 64.59 | 51.11 | 5.33 | 7.74 |
| 10 | samamenangpartnership (https://ag888.app/samamenangpartnership) | F0010 | 40 | 37 | MYR:37 | 92.5 | 100.0 | 5.0/30.61/99.0 | 745.92 | 23.18 | 51.62 | 9.7 | 4.19 | 4.39 |

## Method
- Partner directories: CUSTOMPAGE entries in cached homepages -> `/page/getPage` (public, no login); member domains harvested from page HTML and mapped to merchant IDs via earlier no-login checks.
- Bonus terms: `/merchants/getPublicInfo` (public, form-encoded POST, the same call the site JS makes pre-login), one request per merchant, 6 concurrent; site-level min deposit / withdrawal limits and deposit methods from homepage CONFIG JSON.
- Reachability: fresh no-login check (homepage + merchant id + API) on 2026-10-02 for every merchant (urls_by_merchant), plus earlier checks / a fresh check of 205 untested member domains.

## Caveats
- Money stats (amounts, win-over, cashout, deposits) are computed only over sites in the group's dominant currency (`stats_currency`); other-currency members are counted but not averaged. Multipliers are currency-free but use the same subset.
- One "main" no-deposit and one "main" welcome promo per site (lowest displayOrder among classified promos). Sites often run several (event-game variants, iOS/app versions); others are ignored.
- Classification is heuristic (name keywords + claimCondition + deposit terms). Some "free credit" promos needing a deposit or app download may be misclassified.
- `minWithdraw` is platform-ambiguous: for no-deposit promos it is treated as the win-over target amount (`nd_win_over`, source in Sites sheet `nd_src_win_over`); for deposit promos as a win-over multiplier (`wl_win_over_x`). Description text overrides fields where it states terms explicitly. Values <1 are treated as ratios, not money.
- Turnover multipliers are rarely published for no-deposit (few values); many sites state only win-over.
- Groups are exact site sets, so one real partnership appears as many near-identical rows (e.g. SamaMenang / 4dgang); use `family_id` to roll up. A site can belong to many groups.
- Blank = not published / not parsed; nothing imputed. Terms are a 2026-10-02 snapshot and change often.
- 54 member domains confirmed working in the fresh members check were not regrouped by merchant ID or fetched for promos; they count toward reachability only.

import csv, json, collections
T = '/workspace/bie_tools'; M = json.load(open(f'{T}/pstats/build_meta.json'))
P = list(csv.DictReader(open(f'{T}/partnership_stats.csv'))); S = list(csv.DictReader(open(f'{T}/partnership_sites.csv')))
fam = {}
for r in sorted(P, key=lambda r: -int(r['n_sites'])): fam.setdefault(r['family_id'], r)
top = list(fam.values())[:10]
ms = [s for s in S if s['merchant_id']]
cov = lambda f: sum(1 for s in ms if s[f] != '')
L = ['# Partnership bonus stats (public data only, no login)', '', f'Built 2026-10-02 (AEST). Files: partnership_stats.csv / .xlsx (sheets Partnerships, Sites, Notes), partnership_sites.csv.', '',
 '## Coverage', f"- Partnership rows: {M['n_groups']} exact-membership groups (>=2 sites; directories listing the identical site set collapsed), clustered into {M['n_families']} families (`family_id`, Jaccard >= 0.8 vs the family's largest group). {M['n_single']} directory pages listing <2 sites excluded.",
 f"- Member sites: {M['n_sites']} distinct; {M['merchant_sites']} resolved to a merchant ID; {M['sites_with_data']} have public promotion data ({100*M['sites_with_data']/M['n_sites']:.0f}% of all sites, {100*M['sites_with_data']/M['merchant_sites']:.1f}% of merchant-ID sites). The rest are domains with no working site (DNS dead, parse failed) or newly confirmed members not yet fetched.",
 f"- Of merchant sites: no-deposit found {sum(1 for s in ms if s['nd_name'])}, welcome deposit found {sum(1 for s in ms if s['wl_name'])}.",
 '- Field fill (merchant sites): ' + ', '.join(f'{f} {cov(f)}' for f in ['nd_amount','nd_win_over','nd_max_cashout','nd_turnover_x','nd_min_withdraw','wl_pct','wl_fixed','wl_max_bonus','wl_min_deposit','wl_win_over_x','wl_turnover_x','wl_min_withdraw','wl_max_withdraw']),
 f"- Currency mix of merchant sites: " + ', '.join(f'{c} {n}' for c, n in collections.Counter(s['currency'] for s in ms).most_common()),
 '', '## Top 10 partnerships by site count (largest group per family)', '',
 '| # | partnership | family | sites | w/ data | currency | % reach | % ND | ND amt min/avg/max | ND win-over avg | ND max cashout avg | WL % avg | WL min dep avg | WL win-over x avg | WL turnover x avg |', '|' + '---|' * 15]
for i, r in enumerate(top, 1):
    L.append(f"| {i} | {r['partnership_name']} ({r['partnership_url']}) | {r['family_id']} | {r['n_sites']} | {r['n_sites_with_bonus_data']} | {r['currency_mix']} | {r['pct_sites_reachable']} | {r['pct_offering_nodeposit']} | {r['nd_amount_min']}/{r['nd_amount_avg']}/{r['nd_amount_max']} | {r['nd_win_over_avg']} | {r['nd_max_cashout_avg']} | {r['wl_pct_avg']} | {r['wl_min_deposit_avg']} | {r['wl_win_over_x_avg']} | {r['wl_turnover_x_avg']} |")
L += ['', '## Method', '- Partner directories: CUSTOMPAGE entries in cached homepages -> `/page/getPage` (public, no login); member domains harvested from page HTML and mapped to merchant IDs via earlier no-login checks.',
 '- Bonus terms: `/merchants/getPublicInfo` (public, form-encoded POST, the same call the site JS makes pre-login), one request per merchant, 6 concurrent; site-level min deposit / withdrawal limits and deposit methods from homepage CONFIG JSON.',
 '- Reachability: fresh no-login check (homepage + merchant id + API) on 2026-10-02 for every merchant (urls_by_merchant), plus earlier checks / a fresh check of 205 untested member domains.',
 '', '## Caveats',
 '- Money stats (amounts, win-over, cashout, deposits) are computed only over sites in the group\'s dominant currency (`stats_currency`); other-currency members are counted but not averaged. Multipliers are currency-free but use the same subset.',
 '- One "main" no-deposit and one "main" welcome promo per site (lowest displayOrder among classified promos). Sites often run several (event-game variants, iOS/app versions); others are ignored.',
 '- Classification is heuristic (name keywords + claimCondition + deposit terms). Some "free credit" promos needing a deposit or app download may be misclassified.',
 '- `minWithdraw` is platform-ambiguous: for no-deposit promos it is treated as the win-over target amount (`nd_win_over`, source in Sites sheet `nd_src_win_over`); for deposit promos as a win-over multiplier (`wl_win_over_x`). Description text overrides fields where it states terms explicitly. Values <1 are treated as ratios, not money.',
 '- Turnover multipliers are rarely published for no-deposit (few values); many sites state only win-over.',
 '- Groups are exact site sets, so one real partnership appears as many near-identical rows (e.g. SamaMenang / 4dgang); use `family_id` to roll up. A site can belong to many groups.',
 '- Blank = not published / not parsed; nothing imputed. Terms are a 2026-10-02 snapshot and change often.',
 '- 54 member domains confirmed working in the fresh members check were not regrouped by merchant ID or fetched for promos; they count toward reachability only.']
open(f'{T}/partnership_summary.md', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[:30]))

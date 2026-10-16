"""AU-ONLY summary md (j_md.py style) + partnership_sites_unknown_country.csv. Offline; reads local files only."""
import sys, os, csv, json, collections, datetime
sys.path.insert(0, '/workspace/bie_tools/pstats'); import au_classify as AC
D = os.environ.get('OUT', '/tmp/au_out'); T = '/workspace/bie_tools'
M = json.load(open(f'{D}/build_meta_AU.json'))
P = list(csv.DictReader(open(f'{D}/partnership_stats_AU.csv', encoding='utf-8'))); S = list(csv.DictReader(open(f'{D}/partnership_sites_AU.csv', encoding='utf-8')))
CL = AC.classify(); G = json.load(open(f'{T}/pstats/groups.json')); groups = [g for g in G['groups'] if len(g['sites']) >= 2]
BUILT = datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + ' AEST'
cnt = collections.Counter(v['cls'] for v in CL.values())
basis = collections.Counter(v['match_basis'] for v in CL.values() if v['cls'] == 'AU')
excl = collections.Counter(v['row']['country'] or v['row']['currency'] for v in CL.values() if v['cls'] == 'EXCLUDED')
# unknown-country review file: current (all-countries) group ids, untruncated, plus review-only hints (NOT used for classification)
memb = collections.defaultdict(list)
for g in groups:
    for s in g['sites']: memb[s].append(g['group_id'])
mc = {AC.nh(r['url']): r for r in csv.DictReader(open(f'{T}/pstats/members_check.csv'))}
au_mid = {a['merchant_id'] for a in csv.DictReader(open(AC.URLS_AU))}
ctry = {s: (v['row']['country'] or v['row']['currency'] or '?') for s, v in CL.items()}
U = []
for s, v in sorted(CL.items()):
    if v['cls'] != 'UNKNOWN': continue
    r = v['row']; h = AC.nh(s); m = mc.get(h, {})
    co = collections.Counter(ctry[x] for gid in memb[s] for g in [groups[int(gid[1:]) - 1]] for x in g['sites'] if x != s)
    U.append({'site': s, 'normalized_host': h, 'merchant_id': r['merchant_id'], 'merchant_name': r['merchant_name'], 'verified_url': r['verified_url'],
              'any_known_domain': r['any_known_domain'], 'country': r['country'], 'currency': r['currency'], 'reachable': r['reachable'],
              'n_partnerships_all_countries': len(memb[s]), 'partnership_ids_all_countries': ','.join(memb[s]),
              'review_hint_members_check_merchant_id': m.get('merchant_id', ''),
              'review_hint_that_id_in_urls_au': ('yes' if m.get('merchant_id') in au_mid else 'no') if m.get('merchant_id') else '',
              'review_hint_comember_country_mix': ', '.join(f'{k}:{n}' for k, n in co.most_common()),
              'status': 'UNKNOWN - excluded from AU stats; no exact merchant_id/host/sites_config match (not guessed)'})
assert all(groups[int(g[1:]) - 1]['group_id'] == g for u in U for g in u['partnership_ids_all_countries'].split(',') if g)
with open(f'{D}/partnership_sites_unknown_country.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, list(U[0])); w.writeheader(); w.writerows(U)
hint8 = [u for u in U if u['review_hint_that_id_in_urls_au'] == 'yes']
json.dump({'counts': cnt, 'au_basis': basis, 'excluded_by_country': excl, 'unknown_with_members_check_au_id': len(hint8), 'built': BUILT}, open(f'{D}/au_classify_meta.json', 'w'), indent=1)
# ---- summary md (same structure as j_md.py, AU members only)
fam = {}
for r in sorted(P, key=lambda r: -int(r['n_sites'])): fam.setdefault(r['family_id'], r)
top = list(fam.values())[:10]
ms = [s for s in S if s['merchant_id']]
cov = lambda f: sum(1 for s in ms if s[f] != '')
L = ['# AU-ONLY Partnership bonus stats (Australian / AUD sites only; public data only, no login)', '',
 f'AU-ONLY. Built offline {BUILT} from existing data already on disk (no scraping or network); bonus terms are the 2026-10-02 public snapshot. Files: partnership_stats_AU.csv / partnership_stats_AU.xlsx (sheets Partnerships, Sites, Notes), partnership_sites_AU.csv, partnership_sites_unknown_country.csv. All-countries versions: reports/_all-countries/.', '',
 '## AU scope', f"- Of the 1615 member sites in the all-countries build: {cnt['AU']} AU, {cnt['UNKNOWN']} unknown country, {cnt['EXCLUDED']} excluded non-AU ({', '.join(f'{k} {n}' for k, n in excl.most_common())}). {cnt['AU']} + {cnt['UNKNOWN']} + {cnt['EXCLUDED']} = {sum(cnt.values())}.",
 f"- AU basis: country=AU / currency=AUD field {basis.get('field', 0)}; blank country+currency matched exactly by merchant_id {basis.get('merchant_id', 0)}, by host {basis.get('host', 0)}, by sites_config {basis.get('sites_config', 0)}.",
 f"- Unknown-country sites ({cnt['UNKNOWN']}, all domain-only members with no merchant ID, country or currency) are EXCLUDED from every AU count and stat; they are listed with their current group ids in partnership_sites_unknown_country.csv for review.",
 '', '## Coverage', f"- Partnership rows: {M['n_groups']} AU groups (of {M['n_groups_all']} all-countries groups; {M['n_dropped_lt2_au']} dropped for having <2 AU sites), clustered into {M['n_families']} families (`family_id`, Jaccard >= 0.8 on AU member sets vs the family's largest group). Group ids are kept from the all-countries build for traceability; rows are ordered by AU site count.",
 f"- AU member sites: {M['n_sites']} distinct ({M['n_au_sites_in_groups']} in at least one surviving AU group; {M['n_sites'] - M['n_au_sites_in_groups']} AU sites have n_partnerships = 0 because all their groups had <2 AU sites); {M['merchant_sites']} resolved to a merchant ID; {M['sites_with_data']} have public promotion data ({100*M['sites_with_data']/M['n_sites']:.1f}% of AU sites).",
 f"- Of AU merchant sites: no-deposit found {sum(1 for s in ms if s['nd_name'])}, welcome deposit found {sum(1 for s in ms if s['wl_name'])}.",
 '- Field fill (AU merchant sites): ' + ', '.join(f'{f} {cov(f)}' for f in ['nd_amount','nd_win_over','nd_max_cashout','nd_turnover_x','nd_min_withdraw','wl_pct','wl_fixed','wl_max_bonus','wl_min_deposit','wl_win_over_x','wl_turnover_x','wl_min_withdraw','wl_max_withdraw']),
 f"- Currency mix of AU merchant sites: " + ', '.join(f'{c} {n}' for c, n in collections.Counter(s['currency'] for s in ms).most_common()),
 '', '## Top 10 AU partnerships by AU site count (largest group per family)', '',
 '| # | partnership | family | AU sites | w/ data | currency | % reach | % ND | ND amt min/avg/max | ND win-over avg | ND max cashout avg | WL % avg | WL min dep avg | WL win-over x avg | WL turnover x avg |', '|' + '---|' * 15]
for i, r in enumerate(top, 1):
    L.append(f"| {i} | {r['partnership_name']} ({r['partnership_url']}) | {r['family_id']} | {r['n_sites']} | {r['n_sites_with_bonus_data']} | {r['currency_mix']} | {r['pct_sites_reachable']} | {r['pct_offering_nodeposit']} | {r['nd_amount_min']}/{r['nd_amount_avg']}/{r['nd_amount_max']} | {r['nd_win_over_avg']} | {r['nd_max_cashout_avg']} | {r['wl_pct_avg']} | {r['wl_min_deposit_avg']} | {r['wl_win_over_x_avg']} | {r['wl_turnover_x_avg']} |")
L += ['', '## Method', '- Built offline by g_build_au.py / j_md_au.py / h_report_au.py (bie_tools/pstats), reusing g_build.py logic unchanged (verified: with the AU filter off it reproduces the all-countries partnership_stats.csv and partnership_sites.csv byte-for-byte). Inputs: groups.json, sites_config.csv, by_merchant.jsonl, members_check.csv, pubinfo.jsonl, partnership_sites.csv, urls_au.csv.',
 '- AU classification (au_classify.py): AU = country AU or currency AUD. Sites with blank country and currency become AU only on an EXACT merchant_id match to urls_au.csv, an EXACT normalized host match (lowercase, no scheme/www./path) of site / verified_url / any_known_domain to urls_au hosts, or an exact host / merchant_id AU/AUD entry in sites_config.csv. No fuzzy or brand-name matching; anything else is UNKNOWN and excluded.',
 '- Regrouping: each all-countries group keeps only its AU members; groups with <2 AU sites are dropped; every count, percentage, stat, currency_mix, stats_currency, member_sites, common_bonus_names, deposit methods, n_domains and family_id is recomputed on AU members only. Each AU site\'s n_partnerships / partnership_ids list only surviving AU groups.',
 '- Original sources of the data (unchanged): partner directories from cached homepages via public `/page/getPage`; bonus terms from public `/merchants/getPublicInfo` (2026-10-02); reachability from no-login checks (2026-10-02).',
 '', '## Caveats',
 '- Money stats (amounts, win-over, cashout, deposits) are computed over sites in the group\'s main currency (`stats_currency`, AUD for every AU group).',
 '- One "main" no-deposit and one "main" welcome promo per site (lowest displayOrder among classified promos). Sites often run several; others are ignored.',
 '- Classification of promos is heuristic (name keywords + claimCondition + deposit terms). Some "free credit" promos needing a deposit or app download may be misclassified.',
 '- `minWithdraw` is platform-ambiguous: for no-deposit promos it is treated as the win-over target amount (`nd_win_over`); for deposit promos as a win-over multiplier (`wl_win_over_x`). Values <1 are treated as ratios, not money.',
 '- Groups are exact site sets in the all-countries build; after removing non-AU members some groups have identical AU member sets (kept as separate rows; same family_id). Use `family_id` to roll up. A site can belong to many groups.',
 f"- Unknown-country sites are excluded, so AU groups can under-count real AU membership. {len(hint8)} unknown sites have a merchant ID in members_check.csv that is in urls_au.csv; this is shown as a review hint only and was NOT used to classify them.",
 '- Blank cells = not published / not parsed; nothing imputed or invented. Terms are a 2026-10-02 snapshot and change often.']
open(f'{D}/partnership_summary_AU.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L[:28]))

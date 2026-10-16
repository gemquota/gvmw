"""AU-ONLY variant of g_build.py (offline; reads existing local files only, no network). Set AU=0 to reproduce the all-countries build for verification.
Step G: per-partnership stats + per-site detail -> partnership_stats.csv/.xlsx + partnership_summary.md.
Streams pubinfo.jsonl (large) line by line. Blank = unknown; never imputed."""
import sys, os, re, csv, json, collections, statistics, datetime
sys.path.insert(0, '/workspace/bie_tools/pstats'); import parse_promos as P
T = '/workspace/bie_tools'; O = f'{T}/pstats'
AU_MODE = os.environ.get('AU', '1') == '1'; OUT = os.environ.get('OUT', T); SFX = '_AU' if AU_MODE else ''
G = json.load(open(f'{O}/groups.json'))
groups = [g for g in G['groups'] if len(g['sites']) >= 2]; single = [g for g in G['groups'] if len(g['sites']) < 2]
dom_mid = G['dom_mid']; dom_status = dict(G['dom_status'])
if AU_MODE:
    sys.path.insert(0, O); import au_classify as AC
    CL = AC.classify()                                              # site -> dict(cls, country_basis, match_basis, ...)
    AUS = {s for s, c in CL.items() if c['cls'] == 'AU'}
    au_groups = []
    for idx, g in enumerate(groups):
        s = [x for x in g['sites'] if x in AUS]
        if len(s) >= 2: au_groups.append((idx, dict(g, sites=s, domains=[d for d in g['domains'] if dom_mid.get(d, d) in AUS])))
    n_dropped = len(groups) - len(au_groups)
    groups = [g for _, g in sorted(au_groups, key=lambda t: (-len(t[1]['sites']), t[0]))]   # largest first, original order on ties
if os.path.exists(f'{O}/members_check.csv'):                      # fresh checks of previously never-tested member domains
    for r in csv.DictReader(open(f'{O}/members_check.csv')):
        ok = int(r.get('merchant_ok') == '1' and r.get('api_ok') == '1'); dom_status[r['url']] = ok
        if ok and r.get('merchant_id'): dom_mid.setdefault(r['url'], r['merchant_id'])
verified = {}
if os.path.exists(f'{O}/by_merchant.jsonl'):
    for l in open(f'{O}/by_merchant.jsonl'): j = json.loads(l); verified[j['merchant_id']] = j
# site config per merchant (first cached homepage wins; currency quotes stripped)
cfg = {}; mdoms = collections.defaultdict(set)
for r in csv.DictReader(open(f'{O}/sites_config.csv')):
    mdoms[r['merchant_id']].add('https://' + r['host'])
    if r['merchant_id'] not in cfg: cfg[r['merchant_id']] = r
for d, m in dom_mid.items(): mdoms[m].add(d)
def methods(gw):
    try: j = json.loads(gw) if gw else {}
    except Exception: return []
    return sorted({re.sub(r'[\d_]+$', '', k).upper() for k in j}) if isinstance(j, dict) else []
# stream promotions -> parsed terms per merchant
terms = {}
for l in open(f'{O}/pubinfo.jsonl'):
    try: r = json.loads(l)
    except Exception: continue
    if not r.get('ok'): 
        terms.setdefault(r['merchant_id'], None); continue
    nd, wl, n_nd, n_wl = P.site_terms(r.get('promotions') or [])
    terms[r['merchant_id']] = {'nd': nd, 'wl': wl, 'n_promos': len(r.get('promotions') or []), 'name': r.get('merchant_name'), 'fetched_at': r.get('fetched_at'),
                               'names': [P.clean(p.get('name')) for p in (r.get('promotions') or [])][:60]}
def site_reachable(s):
    if s in verified: return 1 if verified[s].get('url') else 0
    if s.startswith('https://'): return dom_status.get(s)
    st = [dom_status.get(d) for d in mdoms.get(s, ())]; st = [x for x in st if x is not None]
    return (1 if any(st) else 0) if st else None
ND_F = ['amount', 'win_over', 'max_cashout', 'turnover_x', 'min_withdraw']
W_F = ['pct', 'fixed', 'max_bonus', 'min_deposit', 'max_deposit', 'win_over_x', 'win_over_amt', 'turnover_x', 'min_withdraw', 'max_withdraw']
S_F = ['min_deposit', 'site_min_withdraw', 'site_max_withdraw']
def stat(vals):
    v = [x for x in vals if isinstance(x, (int, float))]
    return (round(min(v), 2), round(statistics.mean(v), 2), round(max(v), 2), len(v)) if v else ('', '', '', 0)
def cur(s): return (cfg.get(s, {}).get('currency') or '').strip("'\" ") if not s.startswith('https://') else ''
def fnum(x):
    try: return float(x)
    except Exception: return None
rows = []; fam = []
for g in groups:                                                   # family = Jaccard >= 0.8 with an earlier (larger) group
    S = set(g['sites']); fid = None
    for f_id, rep in fam:
        if len(S & rep) / len(S | rep) >= 0.8: fid = f_id; break
    if not fid: fid = f'F{len(fam)+1:04d}'; fam.append((fid, S))
    g['family_id'] = fid
for g in groups:
    sites = g['sites']; mids = [s for s in sites if not s.startswith('https://')]
    with_data = [s for s in mids if terms.get(s)]
    currs = collections.Counter(cur(s) for s in mids if cur(s))
    dom_cur = currs.most_common(1)[0][0] if currs else ''
    same = [s for s in with_data if cur(s) == dom_cur]             # money stats only over the dominant currency
    reach = [site_reachable(s) for s in sites]; known = [x for x in reach if x is not None]
    nd = [terms[s]['nd'] for s in same if terms[s]['nd']]; wl = [terms[s]['wl'] for s in same if terms[s]['wl']]
    nm = collections.Counter(); meth = collections.Counter()
    for s in with_data:
        for k in ('nd', 'wl'):
            if terms[s][k]: nm[re.sub(r'[^a-z0-9% ]', '', terms[s][k]['name'].lower()).strip()] += 1
    for s in mids:
        for m in methods(cfg.get(s, {}).get('gateway')): meth[m] += 1
    row = {'group_id': g['group_id'], 'family_id': g['family_id'], 'partnership_name': g['name'], 'partnership_url': g['url'],
           'n_directory_pages': g['n_pages'], 'n_sites': len(sites), 'n_sites_known_merchant': len(mids), 'n_domains': len(g['domains']),
           'n_sites_with_bonus_data': len(with_data), 'pct_sites_with_bonus_data': round(100 * len(with_data) / len(sites), 1) if sites else '',
           'currency_mix': ', '.join(f'{c}:{n}' for c, n in currs.most_common()), 'stats_currency': dom_cur,
           'n_sites_in_stats_currency': len(same),
           'pct_sites_reachable': round(100 * sum(known) / len(known), 1) if known else '', 'n_sites_reachability_known': len(known),
           'pct_offering_nodeposit': round(100 * sum(1 for s in same if terms[s]['nd']) / len(same), 1) if same else '',
           'pct_offering_welcome': round(100 * sum(1 for s in same if terms[s]['wl']) / len(same), 1) if same else ''}
    for k in ND_F:
        a, m, b, n = stat([x.get(k) for x in nd]); row.update({f'nd_{k}_min': a, f'nd_{k}_avg': m, f'nd_{k}_max': b, f'nd_{k}_n': n})
    for k in W_F:
        a, m, b, n = stat([x.get(k) for x in wl]); row.update({f'wl_{k}_min': a, f'wl_{k}_avg': m, f'wl_{k}_max': b, f'wl_{k}_n': n})
    for k in S_F:
        a, m, b, n = stat([fnum(cfg.get(s, {}).get(k)) for s in same]); row.update({f'site_{k}_min': a, f'site_{k}_avg': m, f'site_{k}_max': b})
    row['common_bonus_names'] = '; '.join(f'{k} ({v})' for k, v in nm.most_common(5))
    row['common_deposit_methods'] = '; '.join(f'{k} ({v})' for k, v in meth.most_common(6))
    row['member_sites'] = ' | '.join((cfg.get(s, {}).get('merchant_name') or s) for s in sites)[:3000]
    row['directory_page_urls'] = ' | '.join(g['page_urls'][:20])
    rows.append(row)
with open(f'{OUT}/partnership_stats{SFX}.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)
# per-site detail
memb = collections.defaultdict(list)
for g in groups:
    for s in g['sites']: memb[s].append(g['group_id'])
site_rows = []
for s in sorted((AUS if AU_MODE else memb), key=lambda x: (x.startswith('https://'), x)):
    c = cfg.get(s, {}); t = terms.get(s) or {}; nd = t.get('nd') or {}; wl = t.get('wl') or {}; v = verified.get(s, {})
    r = {'site': s, 'merchant_id': '' if s.startswith('https://') else s, 'merchant_name': c.get('merchant_name') or t.get('name') or '',
         'verified_url': v.get('url', ''), 'any_known_domain': sorted(mdoms.get(s, {s} if s.startswith('https://') else set()))[0] if mdoms.get(s) or s.startswith('https://') else '',
         'n_domains_known': len(mdoms.get(s, ())), 'reachable': site_reachable(s) if site_reachable(s) is not None else '',
         'currency': cur(s), 'country': c.get('country', ''), 'bonus_data': 1 if t else (0 if s in terms else ''),
         'n_public_promotions': t.get('n_promos', ''), 'promos_fetched_at': t.get('fetched_at', ''),
         'n_partnerships': len(memb[s]), 'partnership_ids': ','.join(memb[s][:40]),
         'site_min_deposit': c.get('min_deposit', ''), 'site_min_withdraw': c.get('site_min_withdraw', ''), 'site_max_withdraw': c.get('site_max_withdraw', ''),
         'deposit_methods': ', '.join(methods(c.get('gateway')))}
    for k in ['name'] + ND_F + ['src_win_over']: r[f'nd_{k}'] = nd.get(k, '') if nd.get(k) is not None else ''
    for k in ['name'] + W_F: r[f'wl_{k}'] = wl.get(k, '') if wl.get(k) is not None else ''
    if AU_MODE: r['country_basis'] = CL[s]['country_basis']; r['match_basis'] = CL[s]['match_basis']
    site_rows.append(r)
with open(f'{OUT}/partnership_sites{SFX}.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, list(site_rows[0])); w.writeheader(); w.writerows(site_rows)
json.dump({'n_groups': len(rows), 'n_single': len(single), **({'n_groups_all': len(G['groups']) - len(single), 'n_dropped_lt2_au': n_dropped, 'n_au_sites_in_groups': sum(1 for s in AUS if memb.get(s))} if AU_MODE else {}), 'n_families': len(fam), 'n_sites': len(site_rows),
           'sites_with_data': sum(1 for r in site_rows if r['bonus_data'] == 1), 'merchant_sites': sum(1 for r in site_rows if r['merchant_id']),
           'terms_fetched': len(terms), 'terms_ok': sum(1 for v in terms.values() if v)}, open(f'{OUT}/build_meta{SFX}.json', 'w'))
print('groups', len(rows), 'families', len(fam), 'single-site pages', len(single), 'sites', len(site_rows))

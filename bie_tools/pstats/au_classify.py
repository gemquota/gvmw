"""AU-only classification of partnership member sites (offline, exact matches only, no fuzzy/brand matching).
AU  = country AU or currency AUD in partnership_sites.csv.
Blank country AND currency -> AU only on EXACT merchant_id match to urls_au.csv, EXACT normalized host match
      (site / verified_url / any_known_domain vs urls_au hosts), or exact host / merchant_id lookup in sites_config.csv
      giving country AU or currency AUD. Otherwise UNKNOWN (never guessed). Everything else EXCLUDED."""
import csv, re, collections
SITES = '/workspace/bie_tools/partnership_sites.csv'
URLS_AU = '/workspace/bie/in/config/urls_au.csv'
CFG = '/workspace/bie_tools/pstats/sites_config.csv'
def nh(u):
    u = (u or '').strip().lower()
    u = re.sub(r'^[a-z][a-z0-9+.-]*://', '', u)
    u = re.split(r'[/?#]', u, maxsplit=1)[0].split('@')[-1].split(':')[0].rstrip('.')
    return u[4:] if u.startswith('www.') else u
def cl(x): return (x or '').strip("'\" ").upper()
def classify():
    A = list(csv.DictReader(open(URLS_AU, encoding='utf-8')))
    au_mid = {a['merchant_id'].strip() for a in A if a['merchant_id'].strip()}
    au_host = {nh(a['url']) for a in A if nh(a['url'])}
    cfg_host = collections.defaultdict(set); cfg_mid = collections.defaultdict(set)
    for r in csv.DictReader(open(CFG, encoding='utf-8')):
        cc = (cl(r['country']), cl(r['currency']))
        cfg_host[nh(r['host'])].add(cc); cfg_mid[r['merchant_id'].strip()].add(cc)
    isau = lambda ccs: bool(ccs) and all(c == 'AU' or cu == 'AUD' for c, cu in ccs)   # unambiguous AU only
    out = {}
    for s in csv.DictReader(open(SITES, encoding='utf-8')):
        c, cu, mid = cl(s['country']), cl(s['currency']), s['merchant_id'].strip()
        hosts = sorted({nh(s[k]) for k in ('site', 'verified_url', 'any_known_domain') if nh(s[k])})
        d = {'cls': '', 'country_basis': '', 'match_basis': '', 'match_detail': '', 'row': s}
        if c == 'AU' or cu == 'AUD':
            d.update(cls='AU', match_basis='field', country_basis='field:' + ','.join(x for x in (f'country={c}' if c else '', f'currency={cu}' if cu else '') if x))
        elif c or cu:
            d.update(cls='EXCLUDED', country_basis=f'field:country={c or "-"},currency={cu or "-"}')
        else:
            if mid and mid in au_mid: d.update(cls='AU', match_basis='merchant_id', match_detail=f'merchant_id {mid} in urls_au.csv')
            elif any(h in au_host for h in hosts):
                d.update(cls='AU', match_basis='host', match_detail='host ' + ','.join(h for h in hosts if h in au_host) + ' in urls_au.csv')
            elif any(isau(cfg_host.get(h)) for h in hosts) or (mid and isau(cfg_mid.get(mid))):
                d.update(cls='AU', match_basis='sites_config', match_detail='exact host/merchant_id in sites_config.csv with AU/AUD')
            else: d.update(cls='UNKNOWN')
            d['country_basis'] = 'blank-matched' if d['cls'] == 'AU' else 'blank-no-exact-match'
        out[s['site']] = d
    return out
if __name__ == '__main__':
    C = classify(); print(collections.Counter(v['cls'] for v in C.values()), collections.Counter((v['cls'], v['country_basis'], v['match_basis']) for v in C.values()))

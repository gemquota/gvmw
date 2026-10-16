"""Step A: enumerate partner pages (CUSTOMPAGE entries mentioning partner) across cached homepages; extract site config."""
import os, re, json, csv
T = '/workspace/bie_tools'; C = f'{T}/cache'; O = f'{T}/pstats'
dec = json.JSONDecoder()
def obj(h, name):
    m = re.search(r'\b' + name + r'\s*=\s*', h)
    if not m: return None
    try: return dec.raw_decode(h[m.end():])[0]
    except Exception: return None
def sval(h, name):
    m = re.search(r'\b' + name + r'\s*=\s*"?([^";\n]*)"?\s*;', h); return m.group(1) if m else ''
pages = {}; sites = []
for fn in sorted(os.listdir(C)):
    host = fn[:-5]; h = open(f'{C}/{fn}', errors='ignore').read()
    mid = sval(h, 'MERCHANTID'); mname = sval(h, 'MERCHANTNAME')
    if not mid: continue
    cfg = obj(h, 'CONFIG') or {}; cp = obj(h, 'CUSTOMPAGE') or {}
    gw = cfg.get('GatewayConfig')
    try: gw = json.loads(gw) if isinstance(gw, str) else gw
    except Exception: pass
    sites.append({'host': host, 'merchant_id': mid, 'merchant_name': mname, 'country': sval(h, 'COUNTRY'), 'currency': sval(h, 'CURRENCY'),
                  'min_deposit': cfg.get('MinDeposit'), 'site_min_withdraw': cfg.get('MinWithdraw'), 'site_max_withdraw': cfg.get('MaxWithdraw'),
                  'gateway': json.dumps(gw)[:2000] if gw else '', 'promotion_page': cfg.get('PromotionPage')})
    for slug, p in cp.items():
        if not isinstance(p, dict) or not p.get('id'): continue
        title = str(p.get('pageTitle') or '')
        if 'partner' in slug.lower() or 'partner' in title.lower():
            e = pages.setdefault(str(p['id']), {'page_id': str(p['id']), 'slug': slug, 'title': title, 'host': host, 'merchant_id': mid, 'seen_on': []})
            e['seen_on'].append(host)
json.dump(pages, open(f'{O}/pages.json', 'w'))
with open(f'{O}/sites_config.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, list(sites[0])); w.writeheader(); w.writerows(sites)
print('cached homepages with merchant', len(sites), '| unique partner page ids', len(pages), '| merchants', len({s['merchant_id'] for s in sites}))

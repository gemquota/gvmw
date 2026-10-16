"""Step E: build partnership groups from fetched partner pages. Site = merchant ID (mirrors collapse) when known, else the domain."""
import sys, os, re, csv, json, collections
sys.path.insert(0, '/workspace/bie_tools'); import discover as D
from nologin_check import normalize
T = '/workspace/bie_tools'; O = f'{T}/pstats'
dom_mid = {}; dom_status = {}
for r in csv.DictReader(open(f'{O}/sites_config.csv')): dom_mid[f"https://{r['host']}"] = r['merchant_id']
files = ['/workspace/bie/db/reachability.csv'] + [f'{T}/{x}' for x in os.listdir(T) if x.startswith('candidates_') and x.endswith('.csv')]
for f in files:
    ts = os.path.getmtime(f)
    for r in csv.DictReader(open(f)):
        ok = r.get('merchant_ok') == '1' and r.get('api_ok') == '1'
        if ok and r.get('merchant_id'): dom_mid.setdefault(r['url'], r['merchant_id'])
        prev = dom_status.get(r['url'])
        if not prev or ts >= prev[1]: dom_status[r['url']] = (int(ok), ts)
NOISE = re.compile(r'(gwvkyk|b-cdn|vefrop|heylink|schema\.org|w3\.org|google|facebook|instagram|t\.me|telegram|whatsapp|youtube|tiktok|twitter|wa\.me|linktr)', re.I)
pages = [json.loads(l) for l in open(f'{O}/pages_content.jsonl')]
groups = {}
for p in pages:
    if not p.get('ok'): continue
    html = (p.get('html') or '').replace('\\/', '/')
    doms = set()
    for host in re.findall(r'https?://([a-z0-9.-]+\.[a-z]{2,})', html, re.I):
        if NOISE.search(host): continue
        for d in D.harvest(host): doms.add(d)
    if not doms: continue
    sites = frozenset(dom_mid.get(d, d) for d in doms)
    g = groups.setdefault(sites, {'pages': [], 'domains': set(), 'sites': sites})
    g['pages'].append(p); g['domains'] |= doms
def gname(g):
    best = max(g['pages'], key=lambda p: (p['seen_on'], len(p['title'] or '')))
    t = re.sub(r'\s+', ' ', best['title'] or '').strip()
    return best, (t or best['slug'])
out = []
for sites, g in groups.items():
    best, name = gname(g)
    out.append({'group_id': '', 'name': name[:150], 'url': f"https://{best['host']}/{best['slug']}", 'n_pages': len(g['pages']),
                'pages_seen_on_hosts': sum(p['seen_on'] for p in g['pages']), 'sites': sorted(sites), 'domains': sorted(g['domains']),
                'page_urls': sorted({f"https://{p['host']}/{p['slug']}" for p in g['pages']})})
out.sort(key=lambda r: (-len(r['sites']), -r['pages_seen_on_hosts']))
for i, r in enumerate(out, 1): r['group_id'] = f'G{i:04d}'
json.dump({'groups': out, 'dom_mid': dom_mid, 'dom_status': {k: v[0] for k, v in dom_status.items()}}, open(f'{O}/groups.json', 'w'))
sz = collections.Counter(min(len(r['sites']), 10) for r in out)
print('pages ok', sum(1 for p in pages if p.get('ok')), '| with links', sum(len(r['n_pages'] * [0]) for r in out), '| groups', len(out), '| size dist (10=10+)', sorted(sz.items()))
unknown = {d for r in out for d in r['domains'] if d not in dom_status}
print('member domains', len({d for r in out for d in r['domains']}), '| never tested', len(unknown))
open(f'{O}/untested_members.txt', 'w').write('\n'.join(sorted(unknown)) + '\n')
for r in out[:12]: print(r['group_id'], len(r['sites']), r['n_pages'], r['url'], '|', r['name'][:80])

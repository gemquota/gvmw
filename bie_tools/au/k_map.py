"""Build host->merchant_id map from every local no-login result; list record hosts that remain unmapped."""
import csv, json, os, re, glob, collections
T = '/workspace/bie_tools'; B = '/workspace/bie'; C = f'{B}/in/config'; A = f'{T}/au'
def host(u):
    u = (u or '').strip(); u = re.sub(r'^\d+\.\s*', '', u)
    if not u: return ''
    if '://' not in u: u = 'https://' + u
    h = re.sub(r'^https?://', '', u, flags=re.I).split('/')[0].split('?')[0].split(':')[0].lower().strip('.')
    return h[4:] if h.startswith('www.') else h
hm = collections.defaultdict(collections.Counter); names = {}
def add(h, mid, name=''):
    h = host(h); mid = str(mid or '').strip()
    if h and mid and mid not in ('0', 'None'):
        hm[h][mid] += 1
        if name: names.setdefault(mid, name)
files = [f'{B}/db/reachability.csv'] + glob.glob(f'{T}/candidates_*.csv') + [f'{T}/pstats/members_check.csv', f'{T}/au/recheck.csv']
for f in files:
    if not os.path.exists(f): continue
    for r in csv.DictReader(open(f, encoding='utf-8', errors='replace')):
        if str(r.get('merchant_ok')) == '1' and r.get('merchant_id'):
            add(r['url'], r['merchant_id'], r.get('merchant_name', ''))
            if r.get('final_url'): add(r['final_url'], r['merchant_id'])
for r in csv.DictReader(open(f'{T}/pstats/sites_config.csv', encoding='utf-8')): add(r['host'], r['merchant_id'], r['merchant_name'])
for f in [f'{C}/urls_by_merchant.csv', f'{C}/urls_au.csv']:
    for r in csv.DictReader(open(f, encoding='utf-8')): add(r['url'], r['merchant_id'], r['merchant_name'])
for l in open(f'{T}/pstats/by_merchant.jsonl'):
    j = json.loads(l); add(j.get('url'), j['merchant_id'], j.get('merchant_name'))
H = {h: c.most_common(1)[0][0] for h, c in hm.items()}
conflict = {h: dict(c) for h, c in hm.items() if len(c) > 1}
json.dump({'host_mid': H, 'names': names, 'conflicts': conflict}, open(f'{A}/host_mid.json', 'w'))
rec_files = ['newregistered.txt', 'newunregistered.txt', 'check.txt', 'urls.txt', 'newurls.txt', 'urls_backup.txt']
md = [f'{B}/{x}' for x in os.listdir(B) if x.endswith('.md')] + glob.glob(f'{B}/docs/*.md')
rh = set()
for f in rec_files: rh |= {host(l) for l in open(f'{C}/{f}') if host(l)}
for f in md: rh |= {host(u) for u in re.findall(r'https?://[^\s)\]|>"]+', open(f).read())}
un = sorted(h for h in rh if h not in H)
open(f'{A}/unmapped_hosts.txt', 'w').write(''.join(f'https://{h}\n' for h in un))
print('hosts mapped', len(H), 'conflicting hosts', len(conflict), '| record hosts', len(rh), 'unmapped', len(un))

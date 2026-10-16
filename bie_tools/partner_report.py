"""Per partner-directory accounting: listed domains, how many are confirmed platform sites,
how many were already in the 826-entry baseline, and whether every listed domain was tested."""
import sys, os, csv, json, socket, concurrent.futures as cf
sys.path.insert(0, '/workspace/bie_tools'); from nologin_check import normalize
T = '/workspace/bie_tools'
baseline = {normalize(l) for l in open(f'{T}/urls_combined.before_v3.txt') if normalize(l)}
rows = {}
for f in ['/workspace/bie/db/reachability.csv'] + [f'{T}/{x}' for x in os.listdir(T) if x.startswith('candidates_') and x.endswith('.csv')]:
    for r in csv.DictReader(open(f)): 
        if r['url'] not in rows or r.get('merchant_ok') == '1': rows[r['url']] = r
ok = {u for u, r in rows.items() if r.get('merchant_ok') == '1' and r.get('api_ok') == '1'}
dirs = json.load(open(f'{T}/partner_dirs.json'))
alld = sorted({d for x in dirs for d in x['domains']})
untested = [d for d in alld if d not in rows and d not in baseline]
def res(u):
    try: socket.getaddrinfo(u[8:], 443); return True
    except Exception: return False
with cf.ThreadPoolExecutor(16) as ex: unres = {d for d, ok_ in zip(untested, ex.map(res, untested)) if not ok_}
still = [d for d in untested if d not in unres]
out = []
for x in dirs:
    plat = [d for d in x['domains'] if d in ok or d in baseline]
    out.append({'directory': x['url'], 'title': x['title'][:90], 'on_sites': x['seen_on_sites'], 'domains_listed': len(x['domains']),
                'platform_sites': len(plat), 'already_had': sum(d in baseline for d in plat), 'new_confirmed': sum(d in ok and d not in baseline for d in plat)})
out.sort(key=lambda r: -r['platform_sites'])
with open(f'{T}/partner_dirs_report.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, list(out[0])); w.writeheader(); w.writerows(out)
print(f'directories {len(dirs)} | distinct listed domains {len(alld)} | untested-but-resolving {len(still)} | unresolvable(DNS) {len(unres)}')
print(f"heylink dirs {sum(1 for x in dirs if x['key'].startswith('heylink:'))}, on-site dirs {sum(1 for x in dirs if not x['key'].startswith('heylink:'))}")
for r in out[:25]: print(r)
open(f'{T}/partner_untested.txt', 'w').write('\n'.join(still) + '\n')

"""AU-only merge: confirmed candidates whose merchant is not in urls_au -> confirm COUNTRY/CURRENCY from homepage config ->
fresh re-verify best URL -> append to newurls_found.txt, urls_combined.txt, urls_au.txt/.csv; log au_new_merchants.csv."""
import sys, os, re, csv, glob, datetime, concurrent.futures as cf
sys.path.insert(0, '/workspace/bie_tools'); import discover as D; from nologin_check import normalize, check
T = '/workspace/bie_tools'; C = '/workspace/bie/in/config'; A = f'{T}/au'
def sval(h, name):
    m = re.search(r'\b' + name + r'\s*=\s*["\']?([^"\';\n]*)["\']?\s*;', h); return m.group(1).strip() if m else ''
au_rows = list(csv.DictReader(open(f'{C}/urls_au.csv', encoding='utf-8'))); au_mids = {r['merchant_id'] for r in au_rows}
cand = {}  # url -> row
for f in sorted(glob.glob(f'{T}/candidates_*.csv')):
    for r in csv.DictReader(open(f, encoding='utf-8', errors='replace')):
        if str(r.get('merchant_ok')) == '1' and str(r.get('api_ok')) == '1' and r.get('merchant_id') and r['merchant_id'] not in au_mids:
            r['_file'] = os.path.basename(f); r['_mtime'] = os.path.getmtime(f); cand.setdefault(r['url'], r)
D.cache_homepages(sorted(cand))
info = {}
for u, r in cand.items():
    fn = f'{D.CACHE}/{u[8:]}.html'; h = open(fn, errors='ignore').read() if os.path.exists(fn) else ''
    info[u] = (sval(h, 'COUNTRY'), sval(h, 'CURRENCY'))
aud = collections = {}
for u, r in cand.items():
    co, cu = info[u]
    if co == 'AU' or cu == 'AUD': aud.setdefault(r['merchant_id'], []).append(r)
print('confirmed candidates outside urls_au', len(cand), 'merchants', len({r['merchant_id'] for r in cand.values()}), '| AU/AUD merchants', len(aud), flush=True)
side = cf.ThreadPoolExecutor(16)
def safe(u):
    try: return side.submit(check, u).result(timeout=90)
    except Exception: return {'merchant_ok': 0, 'api_ok': 0, 'merchant_id': '', 'elapsed_s': 90, 'failure_stage': 'reachable', 'failure_reason': 'hung'}
def pick(mid):
    rows = sorted(aud[mid], key=lambda r: (-r['_mtime'], float(r.get('elapsed_s') or 99)))
    for i, r in enumerate(rows, 1):
        x = safe(r['url'])
        if str(x['merchant_ok']) == '1' and str(x['api_ok']) == '1' and str(x['merchant_id']) == mid:
            return dict(merchant_id=mid, merchant_name=x['merchant_name'] or r['merchant_name'], url=r['url'], mirror_count=len(rows),
                        checked_at=datetime.datetime.now().astimezone().isoformat(timespec='seconds'), elapsed_s=x['elapsed_s'], mirrors_tried=i, last_error=''), rows
    return None, rows
with cf.ThreadPoolExecutor(6) as ex: res = list(ex.map(pick, sorted(aud)))
newf = {normalize(l) for l in open(f'{C}/newurls_found.txt') if normalize(l)}; comb = {normalize(l) for l in open(f'{C}/urls_combined.txt') if normalize(l)}
add_nf, add_cb, add_au, log = [], [], [], []
for best, rows in res:
    for r in rows:
        co, cu = info[r['url']]
        log.append({'merchant_id': r['merchant_id'], 'merchant_name': r['merchant_name'], 'url': r['url'], 'country': co, 'currency': cu,
                    'source': r.get('source') or r['_file'], 'candidate_file': r['_file'], 'chosen': int(bool(best) and best['url'] == r['url']), 'verified_now': int(bool(best))})
    if not best: continue
    add_au.append(best)
    for r in rows:
        if r['url'] not in newf: add_nf.append(r['url']); newf.add(r['url'])
        if r['url'] not in comb: add_cb.append(r['url']); comb.add(r['url'])
if add_nf: open(f'{C}/newurls_found.txt', 'a').write(''.join(u + '\n' for u in add_nf))
if add_cb: open(f'{C}/urls_combined.txt', 'a').write(''.join(u + '\n' for u in add_cb))
if add_au:
    with open(f'{C}/urls_au.csv', 'a', newline='', encoding='utf-8') as fh:
        csv.DictWriter(fh, list(au_rows[0])).writerows(add_au)
    open(f'{C}/urls_au.txt', 'a').write(''.join(b['url'] + '\n' for b in add_au))
lp = f'{A}/au_new_merchants.csv'; new = not os.path.exists(lp)
with open(lp, 'a', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, list(log[0]) if log else ['merchant_id']);
    if new: w.writeheader()
    w.writerows(log)
print(f'new AUD merchants added {len(add_au)} (unverified now {len(aud) - len(add_au)}); newurls_found +{len(add_nf)}, urls_combined +{len(add_cb)}; urls_au total {len(au_rows) + len(add_au)}')
os._exit(0)

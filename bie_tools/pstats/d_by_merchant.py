"""Step D: one verified working URL per merchant ID across urls.txt + newurls_found.txt.
Candidates per merchant = every domain that previously passed the full no-login check with that merchant ID.
Order: most recent pass first (mtime of the result file), then fastest elapsed; re-verify now with nologin_check.check,
fall back to the next mirror until one passes. Checkpointed to JSONL."""
import sys, os, csv, json, time, datetime, threading, concurrent.futures as cf
sys.path.insert(0, '/workspace/bie_tools'); from nologin_check import normalize, check
T = '/workspace/bie_tools'; B = '/workspace/bie'; O = f'{T}/pstats'; out = f'{O}/by_merchant.jsonl'
scope = {normalize(l) for f in ['in/config/urls.txt', 'in/config/newurls_found.txt'] for l in open(f'{B}/{f}') if normalize(l)}
files = [f'{B}/db/reachability.csv'] + [f'{T}/{x}' for x in os.listdir(T) if x.startswith('candidates_') and x.endswith('.csv')]
cand = {}   # mid -> {url: (passed_ts, elapsed, name)}
for f in files:
    ts = os.path.getmtime(f)
    for r in csv.DictReader(open(f)):
        if r.get('merchant_ok') == '1' and r.get('api_ok') == '1' and r['url'] in scope and r.get('merchant_id'):
            cur = cand.setdefault(r['merchant_id'], {}).get(r['url'])
            el = float(r.get('elapsed_s') or 99)
            if not cur or ts > cur[0]: cand[r['merchant_id']][r['url']] = (ts, el, r.get('merchant_name', ''))
for r in csv.DictReader(open(f'{O}/sites_config.csv')):          # extra mirrors: cached homepages with same merchant id (lowest priority)
    u = 'https://' + r['host']
    if u in scope and r.get('merchant_id') and u not in cand.get(r['merchant_id'], {}):
        cand.setdefault(r['merchant_id'], {})[u] = (0, 99, r.get('merchant_name', ''))
scope_failed = len(scope - {u for m in cand.values() for u in m})
done = set()
if os.path.exists(out):
    for l in open(out): done.add(json.loads(l)['merchant_id'])
todo = sorted(m for m in cand if m not in done)
print(f'in-scope urls {len(scope)} | merchants {len(cand)} | todo {len(todo)} | in-scope urls without a passing merchant id {scope_failed}', flush=True)
lock = threading.Lock(); fh = open(out, 'a')
_side = cf.ThreadPoolExecutor(32)
def safe_check(u):
    try: return _side.submit(check, u).result(timeout=90)
    except Exception as e: return {'merchant_ok': 0, 'api_ok': 0, 'merchant_id': '', 'merchant_name': '', 'elapsed_s': 90, 'failure_stage': 'reachable', 'failure_reason': 'hung'}
def work(mid):
    urls = sorted(cand[mid].items(), key=lambda kv: (-kv[1][0], kv[1][1]))
    name = urls[0][1][2]; tried = []
    rec = {'merchant_id': mid, 'merchant_name': name, 'mirror_count': len(urls), 'url': '', 'checked_at': '', 'elapsed_s': '', 'tried': 0}
    for u, _ in urls:
        r = safe_check(u); tried.append(u); rec['tried'] = len(tried)
        now = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
        if str(r['merchant_ok']) == '1' and str(r['api_ok']) == '1' and str(r['merchant_id']) == str(mid):
            rec.update(url=u, checked_at=now, elapsed_s=r['elapsed_s'], merchant_name=r['merchant_name'] or name); break
        rec['checked_at'] = now; rec['last_error'] = f"{r.get('failure_stage')}:{r.get('failure_reason')}" + ('' if str(r.get('merchant_id')) in ('', str(mid)) else f" (now merchant {r.get('merchant_id')})")
    with lock: fh.write(json.dumps(rec) + '\n'); fh.flush()
    return bool(rec['url'])
n = ok = 0
with cf.ThreadPoolExecutor(6) as ex:
    for r in ex.map(work, todo):
        n += 1; ok += r
        if n % 100 == 0: print(f'{n}/{len(todo)} verified {ok}', flush=True)
print('finished', n, 'verified', ok, flush=True)

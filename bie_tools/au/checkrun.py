"""Generic polite no-login checker: checkrun.py <in.txt> <out.csv>. 6 workers, 90s hard cap per site, checkpointed."""
import sys, os, csv, concurrent.futures as cf
sys.path.insert(0, '/workspace/bie_tools'); from nologin_check import normalize, check
src, out = sys.argv[1], sys.argv[2]
urls = list(dict.fromkeys(normalize(l) for l in open(src) if normalize(l)))
done = {r['url'] for r in csv.DictReader(open(out))} if os.path.exists(out) else set()
todo = [u for u in urls if u not in done]
F = ['url', 'reachable', 'merchant_ok', 'api_ok', 'merchant_id', 'merchant_name', 'final_url', 'elapsed_s', 'failure_stage', 'failure_reason', 'checked_at']
fh = open(out, 'a', newline=''); w = csv.DictWriter(fh, F, extrasaction='ignore')
if not done: w.writeheader()
side = cf.ThreadPoolExecutor(32)
import datetime
def safe(u):
    try: r = side.submit(check, u).result(timeout=90)
    except Exception: r = {'reachable': 0, 'merchant_ok': 0, 'api_ok': 0, 'failure_stage': 'reachable', 'failure_reason': 'hung', 'elapsed_s': 90}
    r['url'] = u; r['checked_at'] = datetime.datetime.now().astimezone().isoformat(timespec='seconds'); return r
print('todo', len(todo), flush=True)
with cf.ThreadPoolExecutor(6) as ex:
    for i, r in enumerate(ex.map(safe, todo), 1):
        w.writerow({k: r.get(k, '') for k in F}); fh.flush()
        if i % 50 == 0: print(i, flush=True)
print('finished', len(todo), flush=True); os._exit(0)

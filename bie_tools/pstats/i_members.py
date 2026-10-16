"""No-login check of member domains listed in partner directories but never tested. -> members_check.csv (checkpointed)."""
import sys, os, csv, concurrent.futures as cf
sys.path.insert(0, '/workspace/bie_tools'); from nologin_check import normalize, check
O = '/workspace/bie_tools/pstats'; out = f'{O}/members_check.csv'
urls = sorted({normalize(l) for l in open(f'{O}/untested_members.txt') if normalize(l)})
done = {r['url'] for r in csv.DictReader(open(out))} if os.path.exists(out) else set()
todo = [u for u in urls if u not in done]
F = ['url', 'merchant_ok', 'api_ok', 'merchant_id', 'merchant_name', 'elapsed_s', 'failure_stage', 'failure_reason']
fh = open(out, 'a', newline=''); w = csv.DictWriter(fh, F, extrasaction='ignore')
if not done: w.writeheader()
side = cf.ThreadPoolExecutor(32)
def safe(u):
    try: r = side.submit(check, u).result(timeout=90)
    except Exception: r = {'merchant_ok': 0, 'api_ok': 0, 'failure_stage': 'reachable', 'failure_reason': 'hung', 'elapsed_s': 90}
    r['url'] = u; return r
with cf.ThreadPoolExecutor(6) as ex:
    for i, r in enumerate(ex.map(safe, todo), 1):
        w.writerow({k: r.get(k, '') for k in F}); fh.flush()
print('members checked', len(todo), flush=True); os._exit(0)

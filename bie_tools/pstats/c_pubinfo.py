"""Step C: public promotions per merchant via /merchants/getPublicInfo (what the public promotion page loads; no login).
One request per merchant (falls back to up to 2 mirrors). Trimmed records checkpointed to JSONL."""
import sys, csv, json, re, threading, datetime, concurrent.futures as cf
sys.path.insert(0, '/workspace/bie_tools/pstats'); from common import api, done_keys
O = '/workspace/bie_tools/pstats'; out = f'{O}/pubinfo.jsonl'
KEEP = ['id', 'name', 'bonus', 'bonusFixed', 'bonusRandom', 'claimCondition', 'claimConfig', 'rollover', 'minWithdraw', 'maxWithdraw',
        'minTopup', 'maxTopup', 'reset', 'maxRound', 'minRound', 'displayAmount', 'displayOrder', 'description', 'startDateTime', 'endDateTime']
def desc_text(d):
    try: j = json.loads(d) if d else {}
    except Exception: j = {'Description': d}
    t = (j.get('DescQuillHTML') or j.get('Description') or '') if isinstance(j, dict) else str(d)
    t = re.sub(r'<[^>]+>', ' ', t).replace('&amp;', '&').replace('&nbsp;', ' ')
    return ' '.join(t.split())[:2000]
hosts = {}
for r in csv.DictReader(open(f'{O}/sites_config.csv')): hosts.setdefault(r['merchant_id'], []).append(r['host'])
try:   # prefer the verified host from step D when available
    for l in open(f'{O}/by_merchant.jsonl'):
        j = json.loads(l)
        if j.get('url'): hosts.setdefault(j['merchant_id'], []).insert(0, j['url'][8:])
except FileNotFoundError: pass
done = done_keys(out, 'merchant_id'); todo = sorted(m for m in hosts if m not in done)
print('merchants', len(hosts), 'todo', len(todo), flush=True)
lock = threading.Lock(); fh = open(out, 'a')
def work(mid):
    rec = {'merchant_id': mid, 'ok': 0, 'fetched_at': datetime.datetime.now().astimezone().isoformat(timespec='seconds')}
    for h in list(dict.fromkeys(hosts[mid]))[:3]:
        try:
            d = api(h, '/merchants/getPublicInfo', mid)
            if d.get('status') == 'SUCCESS' and isinstance(d.get('data'), dict):
                promos = []
                for p in d['data'].get('promotions') or []:
                    q = {k: p.get(k) for k in KEEP}; q['description'] = desc_text(p.get('description')); promos.append(q)
                rec.update(ok=1, via=h, merchant_name=(d['data'].get('merchant') or {}).get('name'), promotions=promos,
                           providers=sorted((d['data'].get('siteName') or {}).values())[:80] if isinstance(d['data'].get('siteName'), dict) else [])
                break
            rec['err'] = str(d)[:200]
        except Exception as e: rec['err'] = f'{type(e).__name__}: {str(e)[:150]}'
    with lock: fh.write(json.dumps(rec) + '\n'); fh.flush()
    return rec['ok']
n = ok = 0
with cf.ThreadPoolExecutor(6) as ex:
    for r in ex.map(work, todo):
        n += 1; ok += r
        if n % 200 == 0: print(f'{n}/{len(todo)} ok {ok}', flush=True)
print('finished', n, 'ok', ok, flush=True)

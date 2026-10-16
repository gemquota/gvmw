"""Step B: fetch each unique partner page via public /page/getPage (one request per page id), checkpoint to JSONL."""
import json, sys, concurrent.futures as cf, threading
sys.path.insert(0, '/workspace/bie_tools/pstats'); from common import api, done_keys
O = '/workspace/bie_tools/pstats'; out = f'{O}/pages_content.jsonl'
pages = json.load(open(f'{O}/pages.json')); done = done_keys(out, 'page_id')
todo = [p for k, p in pages.items() if k not in done]; lock = threading.Lock(); fh = open(out, 'a')
print('todo', len(todo), 'done', len(done), flush=True)
def work(p):
    rec = {'page_id': p['page_id'], 'host': p['host'], 'slug': p['slug'], 'title': p['title'], 'seen_on': len(p['seen_on'])}
    hosts = [p['host']] + [h for h in p['seen_on'] if h != p['host']][:2]   # fall back to up to 2 mirrors
    for h in hosts:
        try:
            d = api(h, '/page/getPage', p['merchant_id'], {'pageId': p['page_id']})
            x = d.get('data'); x = x[0] if isinstance(x, list) and x else x
            if d.get('status') == 'SUCCESS' and isinstance(x, dict):
                rec.update(ok=1, via=h, html=x.get('html') or '', page_url=x.get('pageUrl')); break
            rec.update(ok=0, err=str(d)[:200])
        except Exception as e: rec.update(ok=0, err=f'{type(e).__name__}: {str(e)[:150]}')
    with lock: fh.write(json.dumps(rec) + '\n'); fh.flush()
    return rec.get('ok')
n = ok = 0
with cf.ThreadPoolExecutor(6) as ex:
    for r in ex.map(work, todo):
        n += 1; ok += bool(r)
        if n % 200 == 0: print(f'{n}/{len(todo)} ok {ok}', flush=True)
print('finished', n, 'ok', ok)

"""Repeatable discovery of sites on the same platform as BIE's urls.txt.
Never logs in, registers, or follows referral links (only bare https://host homepages are fetched).
Usage: python discover.py <source> [args]   sources: homepages | crtsh | pages | file
  homepages : fetch homepage of every confirmed site (urls_combined.txt ∩ confirmed), harvest embedded domains
  crtsh PAT.. : certificate-transparency lookups on crt.sh (e.g. '%96.co')
  pages URL..  : harvest domains from arbitrary public pages (aggregators, heylink.me, t.me/s/ previews, vendor docs)
  file PATH    : candidates from a text file
Then: DNS pre-filter -> nologin_check.check (6 workers) -> writes candidates_<tag>.csv
Finally run `python discover.py merge` to append confirmed to newurls_found.txt and rebuild urls_combined.txt."""
import sys, os, re, csv, json, socket, time, concurrent.futures as cf
sys.path.insert(0, '/workspace/bie_tools'); sys.path.insert(0, '/workspace/bie')
from nologin_check import normalize, check, FIELDS
import requests
BIE = '/workspace/bie'; T = '/workspace/bie_tools'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}
TLD = r'(?:com\.au|com|net|co|vip|bet|win|live|club|pro|asia|one|cc|me|io|xyz|online|app|fun|site|info|org|biz|games|casino|top|shop|store|link|today|world|space|life|ltd|au)'
DOM = re.compile(r'\b((?:[a-z0-9-]{1,40}\.)+' + TLD + r')\b', re.I)
NOISE = re.compile(r'(google|gstatic|facebook|fbcdn|twitter|instagram|youtube|tiktok|whatsapp|telegram|t\.me|cloudflare|jsdelivr|unpkg|b-cdn|bunny|vefrop|alicdn|aliyun|jquery|bootstrap|w3\.org|schema\.org|apple|microsoft|amazon|heylink|linktr|wordpress|gravatar|sentry|github|example|localhost|hosting|cdn\.|fonts|apis|analytics|doubleclick|hotjar|clarity|livechat|tawk|zendesk|crisp|intercom|wikipedia|paypal|visa|mastercard|payid|bitcoin|tether|binance|crt\.sh|mochi)', re.I)

def known():
    s = set()
    for f in ['in/config/urls_combined.txt', 'in/config/urls.txt']:
        p = os.path.join(BIE, f)
        if os.path.exists(p): s |= {normalize(l) for l in open(p) if normalize(l)}
    # everything already tested (pass or fail) is skipped too, so reruns only test new hosts
    for f in os.listdir(T):
        if f.startswith('candidates_') and f.endswith('.csv') or f == 'candidates_check.csv':
            for r in csv.DictReader(open(os.path.join(T, f))): s.add(r['url'])
    return s

def harvest(text):
    out = set()
    for m in DOM.findall(text):
        m = m.lower().strip('.')
        if NOISE.search(m): continue
        parts = m.split('.')
        apex = '.'.join(parts[-3:]) if m.endswith('.com.au') else '.'.join(parts[-2:])
        n = normalize(apex)
        if n: out.add(n)
    return out

def fetch(url, timeout=15, deadline=30, max_bytes=3_000_000):
    """GET with a hard total deadline and size cap (requests' timeout is per-read only)."""
    try:
        t0 = time.time(); buf = bytearray()
        with requests.get(url, headers=UA, timeout=timeout, verify=False, stream=True) as r:
            for chunk in r.iter_content(65536):
                buf += chunk
                if time.time() - t0 > deadline or len(buf) > max_bytes: break
            enc = r.encoding or 'utf-8'
        return buf.decode(enc, errors='ignore')
    except Exception: return ''

def src_homepages():
    urls = cache_homepages(confirmed_urls()); found = {}
    for u in urls:
        fn = f'{CACHE}/{u[8:]}.html'
        if not os.path.exists(fn): continue
        html = open(fn, errors='ignore').read().replace('\\/', '/')
        for d in harvest(html): found.setdefault(d, f'homepage-links:{u}')
        for h in re.findall(r'https?://(?:t|telegram)\.me/([A-Za-z0-9_]{4,})', html): found.setdefault('TG:' + h.lower(), u)
        for h in re.findall(r'https?://(?:www\.|m\.)?facebook\.com/(?:groups/)?([A-Za-z0-9_.-]{4,})', html): found.setdefault('FB:' + h.lower(), u)
    return found

def src_crtsh(patterns):
    found = {}
    for p in patterns:
        for attempt in range(3):
            try:
                r = requests.get('https://crt.sh/', params={'q': p, 'output': 'json', 'exclude': 'expired'}, headers=UA, timeout=90)
                rows = r.json(); break
            except Exception as e: rows = []; time.sleep(5)
        for row in rows:
            for name in str(row.get('name_value', '')).split('\n'):
                name = name.strip().lstrip('*.')
                for d in harvest(name): found.setdefault(d, f'crt.sh:{p}')
        print(f'crt.sh {p}: {len(rows)} certs, {len(found)} domains cumulative', flush=True)
        time.sleep(3)
    return found

def src_pages(urls):
    found = {}
    for u in urls:
        html = fetch(u, 25)
        for d in harvest(html): found.setdefault(d, f'page:{u}')
        print(f'page {u}: {len(html)} bytes, {len(found)} domains cumulative', flush=True)
    return found


def src_sameip(ips, max_pages=40):
    """Reverse-IP via rapiddns.io same-IP pages (free, paginated, 100 rows/page)."""
    found = {}
    for ip in ips:
        seen_page = None
        for page in range(1, max_pages + 1):
            html = fetch(f'https://rapiddns.io/sameip/{ip}?page={page}', 40)
            names = re.findall(r'<td>([a-z0-9.-]+\.[a-z]{2,})</td>', html, re.I)
            if not names or names == seen_page: break
            seen_page = names
            for n in names:
                for d in harvest(n): found.setdefault(d, f'rapiddns-sameip:{ip}')
            time.sleep(1.5)
        print(f'sameip {ip}: pages {page}, cumulative {len(found)}', flush=True)
    return found


CACHE = f'{T}/cache'

def confirmed_urls():
    out = []
    for f in ['/workspace/bie/db/reachability.csv', f'{T}/candidates_check.csv'] + [f'{T}/{x}' for x in os.listdir(T) if x.startswith('candidates_') and x.endswith('.csv')]:
        if os.path.exists(f): out += [r['url'] for r in csv.DictReader(open(f)) if r.get('merchant_ok') == '1' and r.get('api_ok') == '1']
    return sorted(set(out))

def cache_homepages(urls):
    """One GET per confirmed homepage, cached to cache/<host>.html (skips already-cached)."""
    os.makedirs(CACHE, exist_ok=True)
    todo = [u for u in urls if not os.path.exists(f'{CACHE}/{u[8:]}.html')]
    def get(u):
        html = fetch(u); open(f'{CACHE}/{u[8:]}.html', 'w').write(html); return len(html)
    with cf.ThreadPoolExecutor(6) as ex:
        for i, _ in enumerate(ex.map(get, todo), 1):
            if i % 50 == 0: print(f'cached {i}/{len(todo)}', flush=True)
    return urls

PAGE_RE = re.compile(r'"([A-Za-z0-9_-]{2,60})":\{"id":"\d+","pageTitle":"((?:[^"\\]|\\.)*)"')
def partner_dirs():
    """From cached homepages: pages whose slug/title mention partner(ship) + heylink.me *partner* links."""
    dirs = {}   # key: normalized title (or heylink url) -> dict(url=first page url, title, sites=set(hosting sites))
    for fn in os.listdir(CACHE):
        host = fn[:-5]; html = open(f'{CACHE}/{fn}', errors='ignore').read()
        for slug, title in PAGE_RE.findall(html):
            try: title = json.loads(f'"{title}"')
            except Exception: pass
            if 'partner' in slug.lower() or 'partner' in title.lower():
                key = re.sub(r'\s+', ' ', title.strip().lower()) or slug.lower()
                d = dirs.setdefault(key, {'url': f'https://{host}/{slug}', 'title': title, 'seen_on': set()}); d['seen_on'].add(host)
        for h in set(re.findall(r'https?:\\?/\\?/heylink\.me\\?/([A-Za-z0-9_.-]+)', html)):
            key = 'heylink:' + h.lower()
            d = dirs.setdefault(key, {'url': f'https://heylink.me/{h}/', 'title': f'heylink.me/{h}', 'seen_on': set()}); d['seen_on'].add(host)
    return dirs

def brands_in_title(title):
    t = re.sub(r'(?i)^.*?partnership\s*[\u2013\u2014:-]\s*', '', title)
    t = re.sub(r'(?i)best casino partnership.*$', '', t)
    return [b.strip().lower() for b in re.split(r'[,/|&]+', t) if 2 < len(b.strip()) < 30]

def src_partners():
    urls = cache_homepages(confirmed_urls())
    dirs = partner_dirs()
    print(f'partner directories found: {len(dirs)}', flush=True)
    found = {}; report = []
    pc = f'{T}/cache_partner'; os.makedirs(pc, exist_ok=True)
    for key, d in sorted(dirs.items()):
        fn = f"{pc}/{re.sub(r'[^A-Za-z0-9]+', '_', d['url'])[:150]}.html"
        if not os.path.exists(fn): open(fn, 'w').write(fetch(d['url'], 25)); time.sleep(0.5)
        html = open(fn, errors='ignore').read().replace('\\/', '/')
        doms = harvest(html)
        host_home = os.path.join(CACHE, d['url'].split('/')[2] + '.html')
        # domains specific to this directory = on partner page; brands from title mapped to domains by label
        brands = brands_in_title(d['title']) if not key.startswith('heylink:') else []
        for x in doms: found.setdefault(x, f"partner-dir:{d['url']}")
        report.append({'key': key, 'url': d['url'], 'title': d['title'][:160], 'seen_on_sites': len(d['seen_on']), 'brands': brands, 'domains': sorted(doms)})
    json.dump(report, open(f'{T}/partner_dirs.json', 'w'), indent=1)
    return found


TG_SKIP = re.compile(r'(bot$|_bot|cs\d*$|_cs|staff|admin|support|service|helpdesk|livechat|agent|customer|^share$|^joinchat$|^addstickers$|^proxy$|^iv$|^s$)', re.I)
def src_telegram(extra=()):
    """Public channel previews https://t.me/s/<handle> (no account). Handles come from leads_*.txt (TG:...) plus `extra`."""
    handles = list(extra)
    for f in os.listdir(T):
        if f.startswith('leads_') and f.endswith('.txt'):
            handles += [l.split('\t')[0][3:] for l in open(f'{T}/{f}') if l.startswith('TG:')]
    handles = [h for h in dict.fromkeys(h.lower() for h in handles) if not TG_SKIP.search(h)]
    tc = f'{T}/cache_tg'; os.makedirs(tc, exist_ok=True); found = {}; productive = 0
    for i, h in enumerate(handles, 1):
        fn = f'{tc}/{h}.html'
        if not os.path.exists(fn): open(fn, 'w').write(fetch(f'https://t.me/s/{h}', 20)); time.sleep(1)
        html = open(fn, errors='ignore').read()
        doms = harvest(html); productive += bool(doms)
        for d in doms: found.setdefault(d, f'telegram:t.me/s/{h}')
        if i % 100 == 0: print(f'telegram {i}/{len(handles)} handles, {len(found)} domains', flush=True)
    print(f'telegram handles {len(handles)}, with domains {productive}, domains {len(found)}', flush=True)
    return found


def src_urlscan(queries, max_pages=60):
    """Fingerprint search: urlscan.io public search API for pages that loaded the platform's shared CDN hosts."""
    found = {}
    for q in queries:
        after = None
        for page in range(max_pages):
            params = {'q': q, 'size': 100}
            if after: params['search_after'] = after
            d = None
            for attempt in range(4):
                try:
                    resp = requests.get('https://urlscan.io/api/v1/search/', params=params, headers={'User-Agent': 'bie-discovery/1.0'}, timeout=60)
                    if resp.status_code == 429: time.sleep(30); continue
                    d = resp.json(); break
                except Exception as e: print('urlscan retry', attempt, str(e)[:80], flush=True); time.sleep(10 * (attempt + 1))
            if d is None: break
            res = d.get('results', [])
            if not res: print('urlscan stop', d.get('message', '')[:120]); break
            for x in res:
                for k in ('domain', 'apexDomain'):
                    v = (x.get('page') or {}).get(k)
                    for dd in harvest(v or ''): found.setdefault(dd, f'urlscan:{q}')
            after = ','.join(str(v) for v in res[-1].get('sort', []))
            if not d.get('has_more') and len(res) < 100: break
            time.sleep(2)
        print(f'urlscan {q}: pages {page+1}, cumulative {len(found)}', flush=True)
    return found

def resolves(u):
    try: socket.getaddrinfo(u.split('://')[1], 443); return True
    except Exception: return False

def test(found, tag):
    if os.getenv('HARVEST_ONLY'):
        json.dump(found, open(f'{T}/harvest_{tag}.json', 'w')); print(f'[{tag}] harvested {len(found)} (saved, not tested)'); return []
    json.dump(found, open(f'{T}/harvest_{tag}.json', 'w'))          # checkpoint the harvest itself
    extra = sorted(k for k in found if not k.startswith('https://'))
    if extra: open(f'{T}/leads_{tag}.txt', 'w').write('\n'.join(f'{k}\t{found[k]}' for k in extra) + '\n')
    ks = known()                                                       # includes every row already in any candidates_*.csv
    cands = sorted(d for d in found if d.startswith('https://') and d not in ks)
    with cf.ThreadPoolExecutor(16) as ex: alive = [d for d, ok in zip(cands, ex.map(resolves, cands)) if ok]
    print(f'[{tag}] harvested {len(found)}, untested {len(cands)}, resolving {len(alive)}', flush=True)
    out = f'{T}/candidates_{tag}.csv'; new_file = not os.path.exists(out)
    fh = open(out, 'a', newline=''); w = csv.DictWriter(fh, FIELDS + ['source'])
    if new_file: w.writeheader(); fh.flush()
    n_ok = n = 0
    ex = cf.ThreadPoolExecutor(6)
    futs = {ex.submit(check, u): u for u in alive}; pending = set(futs)
    while pending:
        done, pending = cf.wait(pending, timeout=180, return_when=cf.FIRST_COMPLETED)
        if not done:   # nothing finished in 180s: record stragglers as hung and move on
            for f in pending:
                if f.running():
                    r = dict.fromkeys(FIELDS, ''); r.update(url=futs[f], reachable=0, homepage_ok=0, merchant_ok=0, api_ok=0, failure_stage='reachable', failure_reason='hung', source=found[futs[f]])
                    w.writerow(r); n += 1
            fh.flush(); print(f'[{tag}] {len(pending)} hung/unstarted futures abandoned', flush=True)
            ex.shutdown(wait=False, cancel_futures=True); break
        for fut in done:
            r = fut.result(); r['source'] = found[r['url']]; w.writerow(r); fh.flush(); n += 1   # checkpoint every row
            n_ok += str(r['merchant_ok']) == '1' and str(r['api_ok']) == '1'
            if n % 100 == 0: print(f'[{tag}] {n}/{len(alive)} tested, {n_ok} confirmed', flush=True)
    fh.close()
    print(f'[{tag}] tested {n}, confirmed {n_ok}', flush=True)
    return n_ok

def merge():
    detail = f'{T}/newurls_found_detail.csv'
    have = [r for r in csv.DictReader(open(detail))]
    have_urls = {r['url'] for r in have}
    existing = [normalize(l) for l in open(f'{BIE}/in/config/urls.txt') if normalize(l)]
    merch = {}
    for f in ['/workspace/bie/db/reachability.csv']:
        for r in csv.DictReader(open(f)):
            if r['merchant_ok'] == '1': merch.setdefault(r['merchant_id'], r['url'])
    for r in have: merch.setdefault(r['merchant_id'], r['url'])
    combined_before = {normalize(l) for l in open(f'{BIE}/in/config/urls_combined.txt') if normalize(l)}
    added = []
    for f in sorted(os.listdir(T)):
        if not (f.startswith('candidates_') and f.endswith('.csv')) or f in ('candidates_check.csv',): continue
        for r in csv.DictReader(open(f'{T}/{f}')):
            if r['merchant_ok'] == '1' and r['api_ok'] == '1' and r['url'] not in have_urls and r['url'] not in combined_before:
                mirror = r['merchant_id'] in merch
                added.append({'url': r['url'], 'merchant_id': r['merchant_id'], 'merchant_name': r['merchant_name'], 'source': r.get('source', f), 'mirror_of_existing_merchant': int(mirror)})
                merch.setdefault(r['merchant_id'], r['url']); have_urls.add(r['url'])
    with open(detail, 'a', newline='') as fh:
        w = csv.DictWriter(fh, ['url', 'merchant_id', 'merchant_name', 'source', 'mirror_of_existing_merchant']); w.writerows(added)
    with open(f'{BIE}/in/config/newurls_found.txt', 'a') as fh:
        for a in added: fh.write(a['url'] + '\n')
    allnew = [normalize(l) for l in open(f'{BIE}/in/config/newurls_found.txt') if normalize(l)]
    combined = list(dict.fromkeys(existing + allnew))
    open(f'{BIE}/in/config/urls_combined.txt', 'w').write('\n'.join(combined) + '\n')
    print(f'added {len(added)} (mirrors {sum(a["mirror_of_existing_merchant"] for a in added)}), combined total {len(combined)}')
    return added

if __name__ == '__main__':
    import urllib3; urllib3.disable_warnings()
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == 'homepages': test(src_homepages(), 'homepages')
    elif cmd == 'crtsh': test(src_crtsh(args), 'crtsh')
    elif cmd == 'pages': test(src_pages(args), os.getenv('TAG', 'pages'))
    elif cmd == 'file': test({normalize(l): f'file:{args[0]}' for l in open(args[0]) if normalize(l)}, os.getenv('TAG', 'file'))
    elif cmd == 'sameip': test(src_sameip([l.strip() for l in open(args[0]) if l.strip()][:int(os.getenv('MAX_IPS', '40'))]), 'sameip')
    elif cmd == 'partners': test(src_partners(), 'partners')
    elif cmd == 'telegram': test(src_telegram(args), 'telegram')
    elif cmd == 'urlscan': test(src_urlscan(args), 'urlscan')
    elif cmd == 'testharvest': test(json.load(open(f'{T}/harvest_{args[0]}.json')), args[0])
    elif cmd == 'merge': merge()

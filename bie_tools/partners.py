"""Crawl confirmed sites for partner directories + social leads (cached, polite, no login).
Stage 1  homepages : fetch https://host/ for every confirmed site (6 workers) -> cache/home/<host>.html.gz
Stage 2  partners  : parse embedded page JSON ("slug":{"id":..,"pageTitle":"Partnership – A, B, C"}) and
                     footer/button links containing partner|affiliat; fetch each unique directory once
                     -> cache/partner/*.html.gz ; write partner_directories.csv
Stage 3  social    : heylink.me pages + t.me/s/<channel> public previews + public facebook pages found on sites
Writes candidates file all_leads.tsv (host \t source) for discover.py-style testing."""
import sys, os, re, csv, gzip, json, time, hashlib, concurrent.futures as cf
sys.path.insert(0, '/workspace/bie_tools'); sys.path.insert(0, '/workspace/bie')
from discover import harvest, fetch, normalize
T = '/workspace/bie_tools'; C = f'{T}/cache'
for d in ['home', 'partner', 'social']: os.makedirs(f'{C}/{d}', exist_ok=True)

def cached(kind, key, url, timeout=20):
    p = f'{C}/{kind}/{hashlib.md5(key.encode()).hexdigest()[:16]}_{re.sub(r"[^A-Za-z0-9.]", "_", key)[:60]}.html.gz'
    if os.path.exists(p): return gzip.open(p, 'rt', encoding='utf-8', errors='replace').read()
    html = fetch(url, timeout)
    with gzip.open(p, 'wt', encoding='utf-8') as f: f.write(html)
    return html

def confirmed():
    out = set()
    for f in ['/workspace/bie/db/reachability.csv'] + [f'{T}/{x}' for x in os.listdir(T) if x.startswith('candidates_') and x.endswith('.csv')]:
        for r in csv.DictReader(open(f)):
            if r.get('merchant_ok') == '1' and r.get('api_ok') == '1': out.add(r['url'])
    return sorted(out)

def unesc(s): return s.replace('\\/', '/')

PAGE_RE = re.compile(r'"([A-Za-z0-9_\-\\/]{2,80})":\{"id":"\d+","pageTitle":"((?:[^"\\]|\\.)*)"')
LINK_RE = re.compile(r'href=\\?"(https?:[^"\\]+|/[^"\\]*)\\?"[^>]{0,200}>((?:(?!</a).){0,200})', re.I | re.S)

def stage_home(sites):
    with cf.ThreadPoolExecutor(6) as ex:
        list(ex.map(lambda u: cached('home', u.split('//')[1], u +

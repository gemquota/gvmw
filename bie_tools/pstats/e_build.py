"""Step E: group partner directories, parse public promotion terms, compute per-partnership stats, write CSV/XLSX/MD."""
import sys, os, re, csv, json, statistics, collections
sys.path.insert(0, '/workspace/bie_tools'); sys.path.insert(0, '/workspace/bie')
from nologin_check import normalize
import discover as D
import logic
T = '/workspace/bie_tools'; O = f'{T}/pstats'; B = '/workspace/bie'
def jl(p):
    try: return [json.loads(l) for l in open(p)]
    except FileNotFoundError: return []
def num(v):
    try:
        f = float(str(v).replace(',', ''))
        return f
    except Exception: return None

# ---------- domain -> merchant map (only domains that passed the full no-login check at some point) ----------
dom2m = {}; mname = {}
for f in [f'{B}/db/reachability.csv'] + [f'{T}/{x}' for x in os.listdir(T) if x.startswith('candidates_') and x.endswith('.csv')]:
    for r in csv.DictReader(open(f)):
        if r.get('merchant_ok') == '1' and r.get('api_ok') == '1' and r.get('merchant_id'):
            dom2m[r['url']] = r['merchant_id']; mname.setdefault(r['merchant_id'], r.get('merchant_name', ''))
passed_ever = set(dom2m)
tested_ever = set()
for f in [f'{B}/db/reachability.csv'] + [f'{T}/{x}' for x in os.listdir(T) if x.startswith('candidates_') and x.endswith('.csv')]:
    for r in csv.DictReader(open(f)): tested_ever.add(r['url'])
cfg = {}
for r in csv.DictReader(open(f'{O}/sites_config.csv')):
    dom2m.setdefault('https://' + r['host'], r['merchant_id']); cfg.setdefault(r['merchant_id'], r)
verified = {j['merchant_id']: j for j in jl(f'{O}/by_merchant.jsonl')}
pub = {j['merchant_id']: j for j in jl(f'{O}/pubinfo.jsonl')}

# ---------- partner directories ----------
NOISE_PATH = re.compile(r'(heylink|t\.me|telegram|wa\.me|whatsapp|facebook|instagram|tiktok|youtube|static\.|cdn|b-cdn|gwvkyk|schema\.org|google)', re.I)
def members_from_html(html):
    out = set()
    for href in re.findall(r'href\s*=\s*["\']([^"\']+)["\']', html or '', re.I):
        if not href.startswith('http') or NOISE_PATH.search(href): continue
        n = normalize(href)
        if n:   # keep full host (sites use subdomains rarely); strip www.
            out.add(n.replace('https://www.', 'https://'))
    return out
dirs = []
for p in jl(f'{O}/pages_content.jsonl'):
    if not p.get('ok'): continue
    dirs.append({'url': f"https://{p['host']}/{p['slug']}", 'title': p['title'], 'kind': 'site-page', 'seen_on': p['seen_on'], 'members': members_from_html(p.get('html'))})
# heylink partnership pages (link-in-bio lists)
pdj

"""Step G: per-partnership stats + per-site detail -> partnership_stats.csv/.xlsx + summary markdown."""
import sys, os, re, csv, json, collections, statistics, datetime
sys.path.insert(0, '/workspace/bie_tools/pstats'); import parse_promos as P
T = '/workspace/bie_tools'; O = f'{T}/pstats'
G = json.load(open(f'{O}/groups.json')); groups = [g for g in G['groups'] if len(g['sites']) >= 2]; single = [g for g in G['groups'] if len(g['sites']) < 2]
dom_mid = G['dom_mid']; dom_status = dict(G['dom_status'])
for fn in ['members_check.csv']:                                 # fresh checks of never-tested member domains
    if os.path.exists(f'{O}/{fn}'):
        for r in csv.DictReader(open(f'{O}/{fn}')):
            ok = int(r.get('merchant_ok') == '1' and r.get('api_ok') == '1'); dom_status[r['url']] = ok
            if ok and r.get('merchant_id'): dom_mid.setdefault(r['url'], r['merchant_id'])
verified = {}
if os.path.exists(f'{O}/by_merchant.jsonl'):
    for l in open(f'{O}/by_merchant.jsonl'): j = json.loads(l); verified[j['merchant_id']] = j
cfg = collections.defaultdict(list)
for r in csv.DictReader(open(f'{O}/sites_config.csv')): cfg[r['merchant_id']].append(r)
pub = {}
for l in open(f'{O}/pubinfo.jsonl'):
    j = json.loads(l)
    if j['merchant_id'] not in pub or j.get('ok'): pub[j['merchant_id']] = j
mid_domains = collections.defaultdict(set)
for d, m in dom_mid.items(): mid_domains[m].add(d)
def methods(gw):
    try: j = json.loads(gw) if gw else {}
    except Exception: return []
    return sorted({re.sub(r'[\d_]+$', '', k).upper() for k in j}) if isinstance(j, dict) else []
site_rows = {}
def site(s):
    if s in site_rows: return site_rows[s]
    is_mid = not s.startswith('https://')
    doms = sorted(mid_domains.get(s, set())) if is_mid else [s]
    c = cfg.get(s, [{}]) if is_mid else [{}]
    c0 = c[0]
    cur = (c0.get('currency') or '').strip("'\" ") or None
    v = verified.get(s, {}) if is_mid else {}
    reach = 1 if v.get('url') else (int(any(dom_status.get(d) == 1 for d in doms)) if not v else 0)
    if not is_mid: reach = dom_status.get(s)                       # None = unknown
    r = {'site': s, 'merchant_id': s if

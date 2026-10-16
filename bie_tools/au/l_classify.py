"""Classify AUD merchants (urls_au.csv) as registered / unregistered / unknown from LOCAL records only. No passwords output."""
import csv, json, os, re, glob, collections, configparser, sys
sys.path.insert(0, '/workspace/bie_tools/au')
T = '/workspace/bie_tools'; B = '/workspace/bie'; C = f'{B}/in/config'; A = f'{T}/au'
exec(open(f'{A}/k_map.py').read().split('hm = collections')[0])   # reuse host()
M = json.load(open(f'{A}/host_mid.json')); H = M['host_mid']
cp = configparser.ConfigParser(); cp.read(f'{C}/config.ini')
users = {}  # phone -> 'U1'
for s in cp.sections():
    if re.fullmatch(r'U\d+', s): users[cp.get(s, 'u', fallback=cp.get(s, 'username', fallback=''))] = s
default_user = next(iter(users.items()), ('', ''))
def ulabel(phone): return f"{phone} ({users[phone]})" if phone in users else phone
ev = collections.defaultdict(list)   # key -> [(kind, strength, source, username, detail)]
def key(h): return H.get(h) or f'host:{h}'
def put(h, kind, strength, src, user='', detail=''):
    if h: ev[key(h)].append((kind, strength, src, user, detail or h))
for l in open(f'{C}/newregistered.txt'):
    h = host(l); m = re.search(r'/RF([^/\s?]+)', l); code = m.group(1) if m else ''
    put(h, 'pos', 3, 'newregistered.txt', ulabel(code) if code and code != 'UNKNOWN' else '', f'{h} referral code RF{code}')
for l in open(f'{C}/newunregistered.txt'): put(host(l), 'neg', 3, 'newunregistered.txt')
du = f'{ulabel(default_user[0])} [engine default; may be U2-U5 fallback]'
for f in ['urls.txt', 'urls_backup.txt']:
    for l in open(f'{C}/{f}'): put(host(l), 'pos', 2, f'{f} (engine login target)', du)
for f in sorted([x for x in os.listdir(B) if x.endswith('.md')]):            # reports built from logged-in scrape history (bonuses table)
    for u in set(re.findall(r'https?://[^\s)\]|>"]+', open(f'{B}/{f}').read())): put(host(u), 'pos', 2, f'{f} (logged-in scrape history)', du)
ACC = {'history', 'chatroom', 'changeemail', 'settings', 'downline', 'uploads'}
for l in open(f'{C}/check.txt'):
    h = host(l); p = (re.sub(r'^\d+\.\s*', '', l.strip()).split('/', 3) + ['', '', '', ''])[3].split('?')[0].lower()
    if p in ACC: put(h, 'weakpos', 1, 'check.txt', '', f'{h}/{p} (account-only page)')
    else: put(h, 'neutral', 0, 'check.txt', '', f'{h}/{p}')
for l in open(f'{C}/newurls.txt'): put(host(l), 'neutral', 0, 'newurls.txt (candidate list)')
au = list(csv.DictReader(open(f'{C}/urls_au.csv', encoding='utf-8')))
def lab(x): return re.sub(r'[^a-z0-9]', '', x.lower())
def hlab(h):
    parts = h.split('.'); core = parts[0] if len(parts) <= 2 or len(parts[-1]) > 2 else parts[0]
    return lab(core)
aumid = {str(r['merchant_id']) for r in au}; idx = collections.defaultdict(set)
for r in au:
    if len(lab(r['merchant_name'])) >= 4: idx[lab(r['merchant_name'])].add(str(r['merchant_id']))
for h, m in H.items():
    if m in aumid and len(hlab(h)) >= 4: idx[hlab(h)].add(m)
name_ev = collections.defaultdict(list)
for k, v in ev.items():
    if k.startswith('host:'):
        h = k[5:]; ms = idx.get(hlab(h), set())
        if len(ms) == 1:
            for x in v: name_ev[next(iter(ms))].append((x[0], x[1], x[2], x[3], f'{x[4]} [unresolved host; brand-label match {hlab(h)}]'))
reg, unreg, unk = [], [], []; tally = collections.Counter()
for r in au:
    e = ev.get(str(r['merchant_id']), [])
    kinds = {x[0] for x in e}
    srcs = '; '.join(sorted({f"{x[2]}: {x[4]}" for x in e}))[:1500]
    pos3 = [x for x in e if x[0] == 'pos' and x[1] == 3]; pos2 = [x for x in e if x[0] == 'pos' and x[1] == 2]
    base = {'merchant_id': r['merchant_id'], 'merchant_name': r['merchant_name'], 'url': r['url']}
    if ('pos' in kinds) and ('neg' in kinds):
        unk.append({**base, 'reason': 'conflict: registered evidence and newunregistered.txt on same merchant (mirrors)', 'evidence_source': srcs}); tally['unknown_conflict'] += 1
    elif 'pos' in kinds:
        u = next((x[3] for x in pos3 if x[3]), '') or next((x[3] for x in pos2 if x[3]), '')
        reg.append({**base, 'username': u, 'evidence_source': srcs, 'evidence_strength': 'strong' if pos3 else 'medium'}); tally['registered_' + ('strong' if pos3 else 'medium')] += 1
    elif 'neg' in kinds:
        unreg.append({**base, 'evidence_source': srcs, 'basis': 'explicit (newunregistered.txt)'}); tally['unregistered_explicit'] += 1
    elif 'weakpos' in kinds:
        unk.append({**base, 'reason': 'only check.txt account-page visit (likely registered, user not recorded)', 'evidence_source': srcs}); tally['unknown_checkacct'] += 1
    elif kinds:
        unk.append({**base, 'reason': 'listed only in candidate/check lists with no registered/unregistered status', 'evidence_source': srcs}); tally['unknown_listed'] += 1
    elif name_ev.get(str(r['merchant_id'])):
        ne = name_ev[str(r['merchant_id'])]; nk = {x[0] for x in ne}
        st = 'positive' if 'pos' in nk and 'neg' not in nk else 'negative' if 'neg' in nk and 'pos' not in nk else 'mixed/neutral'
        unk.append({**base, 'reason': f'brand-name match only ({st}): record host has no resolvable merchant id', 'evidence_source': '; '.join(sorted({f"{x[2]}: {x[4]}" for x in ne}))[:1500]}); tally['unknown_namematch_' + st] += 1
    else:
        unreg.append({**base, 'evidence_source': 'none: merchant (and its known mirrors) absent from every local record', 'basis': 'no record'}); tally['unregistered_norecord'] += 1
def wr(p, rows, cols):
    with open(p, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, cols); w.writeheader(); w.writerows(rows)
wr(f'{C}/au_registered.csv', reg, ['merchant_id', 'merchant_name', 'url', 'username', 'evidence_source', 'evidence_strength'])
wr(f'{C}/au_unregistered.csv', unreg, ['merchant_id', 'merchant_name', 'url', 'evidence_source', 'basis'])
open(f'{C}/au_unregistered.txt', 'w').write(''.join(r['url'] + '\n' for r in unreg))
wr(f'{C}/au_unknown.csv', unk, ['merchant_id', 'merchant_name', 'url', 'reason', 'evidence_source'])
# record hosts that could not be tied to any merchant
unt = collections.Counter(x[2].split(' ')[0] for k, v in ev.items() if k.startswith('host:') for x in v)
aus = {str(r['merchant_id']) for r in au}
nonau = collections.Counter(x[2].split(' ')[0] for k, v in ev.items() if not k.startswith('host:') and k not in aus for x in v)
print('AU', len(au), 'registered', len(reg), 'unregistered', len(unreg), 'unknown', len(unk)); print(dict(tally))
print('record entries on hosts with no merchant id:', dict(unt)); print('record entries on non-AU merchants:', dict(nonau))

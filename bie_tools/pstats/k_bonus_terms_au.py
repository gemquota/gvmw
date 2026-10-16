"""Step K: AU-only per-promotion bonus terms table (offline; reads cached pubinfo.jsonl / pages_content.jsonl only).
Reuses parse_promos (text_terms, classify, pos/money/f) and logic.normalize/extract. Structured fields only; no description text is output.
Blank = not published. Never imputed."""
import sys, os, re, csv, json, html, collections, statistics, datetime
sys.path.insert(0, '/workspace/bie_tools/pstats'); import parse_promos as P
import logic
O = '/workspace/bie_tools/pstats'; R = '/workspace/bie_deliverables/reports'
URLS_AU = '/workspace/bie/in/config/urls_au.csv'; PS = f'{R}/partnership_sites_AU.csv'
NOW = datetime.datetime.now().astimezone()
COLS = ['merchant_id', 'merchant_name', 'site_url', 'currency', 'in_partnership', 'promo_type', 'promo_name', 'amount_fixed', 'amount_pct',
        'max_bonus', 'min_deposit', 'rollover_x', 'rollover_amt', 'turnover_x', 'min_withdraw', 'max_withdraw', 'commission_pct',
        'commission_levels', 'source', 'fetched_at', 'classification_basis']
NUM = ['amount_fixed', 'amount_pct', 'max_bonus', 'min_deposit', 'rollover_x', 'rollover_amt', 'turnover_x', 'min_withdraw', 'max_withdraw', 'commission_pct']
TYPES = ['REGISTER', 'WELCOME', 'SHARE', 'DOWNLINE_FIRST_DEPOSIT', 'COMMISSION']
SHEET = {'REGISTER': 'Register', 'WELCOME': 'Welcome', 'SHARE': 'Share', 'DOWNLINE_FIRST_DEPOSIT': 'Downline FD', 'COMMISSION': 'Commission'}

# ---------------- sanitizers ----------------
TLD = r'(?:com|net|org|vip|club|co|online|site|me|fun|io|asia|au|bet|win|xyz|top|live|pro|app|info|biz|cc|tv|link|shop|world|life|games?|casino|store|one|plus|today|best|my|sg)'
URL_RX = re.compile(r'(?i)(https?://\S+|www\.\S+|\b(?:t|wa)\.me/\S*|[\w.+-]+@[\w-]+\.[\w.-]+|\b[\w-]+(?:\.[\w-]+)*\.' + TLD + r'\b\S*|[?&]\S+=\S*|(?<![\w.])@\w{2,}|\+?\d[\d\s-]{7,}\d)')
CODE_WORD = re.compile(r'(?i)\b(ref|aff|code|invite\s*code|promo\s*code|referral\s*code|password|pwd|pass)\s*[=:#]|\bcode\b|\bpassword\b')
def is_codeish(tok):
    t = re.sub(r'[^A-Za-z0-9]', '', tok)
    if len(t) < 5: return False
    has_d, has_a = any(ch.isdigit() for ch in t), any(ch.isalpha() for ch in t)
    mixed = any(ch.islower() for ch in t) and any(ch.isupper() for ch in t) and len(re.findall(r'[A-Z]', t[1:])) > 0 and not t[1:].islower()
    return (has_d and has_a) or (mixed and not re.fullmatch(r'[A-Z][a-z]+', t))
def plain(s):
    s = html.unescape(re.sub(r'<[^>]+>', ' ', str(s or ''))); s = html.unescape(s)
    return ' '.join(s.split())
def sanitize_name(name):
    s = plain(name)
    if not s: return ''
    if CODE_WORD.search(s): return ''                       # anything code/credential-like -> blank
    s = URL_RX.sub(' ', s)
    s = ' '.join(tok for tok in s.split() if not is_codeish(tok))
    s = re.sub(r'\s+', ' ', s).strip(' -|:/,~')
    if not re.search(r'[A-Za-z]{3}', s): return ''        # nothing meaningful left
    return s[:80]
def sanitize_merchant(name):
    s = plain(name); s = URL_RX.sub(' ', s); return ' '.join(s.split())
def bare_site(u):
    u = (u or '').strip().lower()
    m = re.match(r'^(?:https?://)?([^/?#:@\s]+)', u)
    if not m: return ''
    h = m.group(1).rstrip('.')
    return 'https://' + h if '.' in h else ''

# ---------------- inputs ----------------
AU = {r['merchant_id'].strip(): r for r in csv.DictReader(open(URLS_AU, encoding='utf-8')) if r['merchant_id'].strip()}
PSR = {r['merchant_id'].strip(): r for r in csv.DictReader(open(PS, encoding='utf-8')) if r['merchant_id'].strip()}
BM = {}
for l in open(f'{O}/by_merchant.jsonl'):
    j = json.loads(l); BM[j['merchant_id']] = j
CUR = collections.defaultdict(set)
for r in csv.DictReader(open(f'{O}/sites_config.csv', encoding='utf-8')):
    c = (r.get('currency') or '').strip("'\" ").upper()
    if c: CUR[r['merchant_id']].add(c)
def merchant_currency(mid):
    if mid in PSR and PSR[mid].get('currency'): return PSR[mid]['currency'].strip().upper(), 'partnership_sites_AU'
    cs = CUR.get(mid)
    if cs: return (next(iter(cs)) if len(cs) == 1 else 'MIXED'), 'sites_config'
    return 'AUD', 'urls_au.csv (AUD merchant list)'
def site_url(mid):
    for u in (PSR.get(mid, {}).get('verified_url'), BM.get(mid, {}).get('url'), AU[mid].get('url') if not AU[mid].get('last_error', '').strip() else ''):
        b = bare_site(u)
        if b: return b
    return ''

# ---------------- classification ----------------
FIELD_TYPE = {'sharebonus': 'SHARE', 'downlinefirstdeposit': 'DOWNLINE_FIRST_DEPOSIT', 'downlinedeposit:bonus': 'DOWNLINE_FIRST_DEPOSIT',
              'downlinedeposit': 'DOWNLINE_FIRST_DEPOSIT', 'unlimiteddownlinedeposit': 'DOWNLINE_FIRST_DEPOSIT',
              'commissionweek': 'COMMISSION', 'commission': 'COMMISSION'}
SELF_REBATE = {'rollcomm', 'rebate', 'rebatedays', 'instantRebate', 'netlossladder'}
K_COMM = re.compile(r'(?i)\b(comm?iss?ions?|commision|comission|commssion|comms|agent|affiliate|partner\s*program|passive\s*income|royalty)\b')
K_DOWN_REB = re.compile(r'(?i)\b(downline|referral|referal|refer)\b.*\b(rebate|loss|lose|win\s*lose)\b')
K_DOWN = re.compile(r'(?i)\b(downline|referr?al|refer(?:\s*a)?\s*friend|invite|invitational|recruit)\b')
K_DOWN_NOT = re.compile(r'(?i)\b(top|ranking|competition|leaderboard|winner|red\s*packet|race)\b')
K_SOCIAL_INV = re.compile(r'(?i)\b(telegram|facebook|whatsapp|social|group|tiktok|instagram)\b')
K_SHARE = re.compile(r'(?i)\b(share|sharing|social\s*share|share\s*to\s*friends?)\b')
def cfgget(c, key):
    for k, v in c.items():
        if k.replace(' ', '').lower() == key.lower(): return v
    return None
def classify(p, c, name):
    cb = str(c.get('customBonus') or '').strip()
    if cb in FIELD_TYPE: return FIELD_TYPE[cb], f'field:customBonus={cb}'
    if cb in SELF_REBATE:
        m = K_COMM.search(name) or K_DOWN_REB.search(name)
        if m: return 'COMMISSION', f'keyword:{m.group(1).lower()}'
        return 'OTHER', f'field:customBonus={cb}'
    m = K_COMM.search(name)
    if m: return 'COMMISSION', f'keyword:{m.group(1).lower()}'
    m = K_DOWN.search(name)
    if m and K_SOCIAL_INV.search(name): return 'SHARE', f'keyword:{K_SOCIAL_INV.search(name).group(1).lower()}+{m.group(1).lower()}'
    if m and K_DOWN_NOT.search(name): return 'OTHER', f'keyword:{K_DOWN_NOT.search(name).group(1).lower()}'
    if m: return 'DOWNLINE_FIRST_DEPOSIT', f'keyword:{m.group(1).lower()}'
    m = K_SHARE.search(name)
    if m: return 'SHARE', f'keyword:{m.group(1).lower()}'
    k = P.classify(p)                                       # reused parse_promos name rules (ND_NAME/W_NAME + claimCondition/minTopup)
    if k == 'nodeposit':
        m = P.ND_NAME.search(name); return 'REGISTER', f'keyword:{m.group(0).lower().strip()}'
    if k == 'welcome':
        m = P.W_NAME.search(name); return 'WELCOME', f'keyword:{m.group(0).lower().strip()}'
    return 'OTHER', ''

# ---------------- term extraction ----------------
NUMR = r'(\d{1,6}(?:\.\d{1,2})?)'
def rxf(pat, t):
    m = re.search(pat, t, re.I)
    try: return float(m.group(1).replace(',', '')) if m else None
    except Exception: return None
NONAUD = re.compile(r'(\bRM\s?\d|\bMYR\b|\bSGD\b|\bS\$\s?\d|\bIDR\b|\bTHB\b|\bBND\b|\bHKD\b|\bKHR\b|\bNPR\b|\bPGK\b|\bUSD\b(?!T)|\bUS\$)')
AUDT = re.compile(r'(AUD|A\$|AU\$)', re.I)
def levels_from_text(t):
    lv = {}
    for m in re.finditer(r'(?i)\b(?:level|lvl|lv|tier|L)\s*-?\s*([1-5])\b[^%\d]{0,40}?(\d{1,2}(?:\.\d{1,2})?)\s*%', t):
        lv.setdefault(int(m.group(1)), float(m.group(2)))
    return lv
def fmt_levels(lv):
    return ' / '.join(f'L{k} {g(v)}%' for k, v in sorted(lv.items())) if len(lv) >= 2 else ''
def g(v): return ('%g' % v) if isinstance(v, float) else str(v)
def rate_levels(c):
    r = c.get('rate')
    if isinstance(r, str):
        try: r = json.loads(r.replace("'", '"'))
        except Exception: r = None
    if not isinstance(r, dict): return None, ''
    tup = collections.Counter()
    for v in r.values():
        if isinstance(v, dict):
            for x in v.values():
                if isinstance(x, list) and x and any(isinstance(y, (int, float)) and y > 0 for y in x): tup[tuple(x)] += 1
    if not tup: return None, ''
    top = tup.most_common(1)[0][0]
    lv = {i + 1: float(y) for i, y in enumerate(top) if isinstance(y, (int, float)) and y > 0}
    return (float(top[0]) if top[0] else None), fmt_levels(lv)
def terms(p, c, typ, desc, name):
    n = logic.normalize(p); t = P.text_terms(desc + ' ' + name); T = (desc + ' ' + name).upper().replace('WIN OVER', 'WINOVER')
    o = {k: None for k in NUM}; o['commission_levels'] = ''; flags = []
    fixed = P.pos(n.get('bonusfixed')); pct = P.pos(n.get('bonus'))
    if typ == 'COMMISSION':
        rp, rlv = rate_levels(c)
        o['commission_pct'] = pct or rp or rxf(r'(\d{1,2}(?:\.\d{1,2})?)\s*%\s*(?:WEEKLY\s*|DAILY\s*|MONTHLY\s*)?(?:DOWNLINE\s*)?COMM', T) \
                              or rxf(r'COMM\w*\D{0,25}?(\d{1,2}(?:\.\d{1,2})?)\s*%', T)
        o['commission_levels'] = fmt_levels(levels_from_text(T)) or rlv
        o['amount_fixed'] = fixed
    else:
        o['amount_fixed'] = fixed or (t['amount'] if not pct else None)
        o['amount_pct'] = pct or (t['pct'] if typ == 'WELCOME' and not fixed else None)
        if typ in ('DOWNLINE_FIRST_DEPOSIT',): o['commission_levels'] = fmt_levels(levels_from_text(T))
    o['max_bonus'] = t['max_bonus']
    dmin = cfgget(c, 'downlineMinTopupAmount') if typ in ('SHARE', 'DOWNLINE_FIRST_DEPOSIT') else None
    o['min_deposit'] = P.pos(n.get('mintopup')) or P.pos(cfgget(c, 'min_topup')) or P.pos(dmin) or t['min_deposit']
    # win-over: text first, then platform minWithdraw (small = multiplier, large = credit target; minWithdrawTimeAmount flag = multiplier)
    mw = P.pos(n.get('minwithdraw')) or P.pos(cfgget(c, 'min_withdraw'))
    mw_mult_flag = bool(P.pos(cfgget(c, 'minWithdrawTimeAmount')))
    o['rollover_x'] = t['win_over_x']; o['rollover_amt'] = t['win_over_amt']
    if mw and o['rollover_x'] is None and o['rollover_amt'] is None:
        if mw_mult_flag or mw <= 50: o['rollover_x'] = mw
        else: o['rollover_amt'] = mw
    o['turnover_x'] = t['turnover_x'] or P.pos(n.get('rollover')) or P.pos(cfgget(c, 'rollover'))
    o['min_withdraw'] = rxf(r'MIN(?:IMUM)?\s*WITHDRAW(?:AL)?\s*(?:IS|:|=)?\s*(?:AUD|A\$|AU\$|\$)\s*' + r'(\d{1,6}(?:,\d{3})?(?:\.\d{1,2})?)(?!\s*X)', T)
    mx = P.money(n.get('maxwithdraw')) or P.money(cfgget(c, 'max_withdraw'))
    if mx and P.pos(cfgget(c, 'maxWithdrawTimeDeposit')): mx = None; flags.append('max_withdraw_is_deposit_multiple')
    elif mx and P.pos(cfgget(c, 'maxWithdrawTimeAmount')):
        base = o['amount_fixed']
        mx = round(mx * base, 2) if base else None; flags.append('max_withdraw_x_amount' + ('' if base else '_unresolved'))
    o['max_withdraw'] = mx or t['max_cashout']
    for k in NUM:                                            # non-positive -> blank; 99999.. / >=1e6 placeholders ('unlimited'/disabled) -> blank
        v = o[k]
        if v is None: continue
        if v <= 0: o[k] = None
        elif v >= 1e6 or re.fullmatch(r'9{5,}(\.9+)?', ('%f' % v).rstrip('0').rstrip('.')): o[k] = None; flags.append(f'sentinel_blanked:{k}')
    return o, flags

# ---------------- build ----------------
fetched_merchants = set(); with_promos = set(); rows = []; other = collections.Counter(); other_m = collections.defaultdict(set)
excl_nonaud = 0; excl_nonaud_m = set(); flags_c = collections.Counter(); seen = set(); n_promos_total = 0; mcur_src = collections.Counter()
for l in open(f'{O}/pubinfo.jsonl'):
    try: r = json.loads(l)
    except Exception: continue
    mid = str(r.get('merchant_id', '')).strip()
    if mid not in AU: continue
    fetched_merchants.add(mid)
    promos = r.get('promotions') or []
    if str(r.get('ok')) != '1' or not promos: continue
    with_promos.add(mid)
    cur, csrc = merchant_currency(mid); mcur_src[csrc] += 1
    if cur != 'AUD':
        excl_nonaud += len(promos); excl_nonaud_m.add(mid); continue
    base = {'merchant_id': mid, 'merchant_name': sanitize_merchant(AU[mid].get('merchant_name') or r.get('merchant_name')), 'site_url': site_url(mid),
            'currency': 'AUD', 'in_partnership': 'yes' if mid in PSR else 'no', 'source': 'pubinfo', 'fetched_at': r.get('fetched_at', '')}
    for p in promos:
        key = (mid, str(p.get('id')))
        if key in seen: continue
        seen.add(key); n_promos_total += 1
        try: c = json.loads(p.get('claimConfig')) if p.get('claimConfig') not in (None, '', 'None') else {}
        except Exception: c = {}
        if not isinstance(c, dict): c = {}
        name = plain(p.get('name')); desc = plain(p.get('description'))
        if NONAUD.search(desc + ' ' + name) and not AUDT.search(desc + ' ' + name):
            excl_nonaud += 1; continue
        typ, basis = classify(p, c, name)
        if typ == 'OTHER':
            other['OTHER'] += 1; other_m['OTHER'].add(mid); continue
        o, fl = terms(p, c, typ, desc, name)
        for x in fl: flags_c[(typ, x)] += 1
        row = dict(base, promo_type=typ, promo_name=sanitize_name(p.get('name')), classification_basis=basis, **o)
        rows.append(row)
# page source: merchant's own affiliate/commission program pages (title names the merchant); COMMISSION only
pages = json.load(open(f'{O}/pages.json'))
pmtime = datetime.datetime.fromtimestamp(os.path.getmtime(f'{O}/pages_content.jsonl')).astimezone().isoformat(timespec='seconds')
PROG = re.compile(r'(?i)affiliat|commission|referral|partner(ship)?\s*program')
def alnum(s): return re.sub(r'[^a-z0-9]', '', (s or '').lower())
def txt(h):
    h = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', h or ''); return plain(h)
page_rows = []; page_seen = set()
for l in open(f'{O}/pages_content.jsonl'):
    try: r = json.loads(l)
    except Exception: continue
    pg = pages.get(str(r.get('page_id'))) or {}; mid = str(pg.get('merchant_id', ''))
    if mid not in AU or str(r.get('ok')) != '1' or not r.get('html'): continue
    title = str(r.get('title') or ''); slug = str(r.get('slug') or '')
    if not PROG.search(title + ' ' + slug): continue
    mn = alnum(AU[mid].get('merchant_name'))
    mn = re.sub(r'(aud|au|aus|australia)$', '', mn) or mn
    if len(mn) < 3 or mn not in alnum(title): continue        # page must name this merchant (own programme, not a partner directory)
    if merchant_currency(mid)[0] != 'AUD': continue
    T = txt(r['html']).upper()
    lv = levels_from_text(T)
    pct = rxf(r'(?:UP\s*TO\s*)?(\d{1,2}(?:\.\d{1,2})?)\s*%\s*(?:PURE\s*|VOLUME\s*|WEEKLY\s*|DAILY\s*|LIFETIME\s*)*COMMISSION', T) \
          or rxf(r'COMMISSION\s*(?:REWARD|RATE)?\s*:?\s*(?:UP\s*TO\s*)?(\d{1,2}(?:\.\d{1,2})?)\s*%', T) \
          or rxf(r'REVENUE\s*SHARE\s*:?\s*(?:UP\s*TO\s*)?(\d{1,2}(?:\.\d{1,2})?)\s*%', T) \
          or rxf(r'UP\s*TO\s*(\d{1,2}(?:\.\d{1,2})?)\s*%\s*REVENUE\s*SHARE', T) or (lv.get(1) if lv else None)
    if not pct or (mid, pct) in page_seen: continue
    page_seen.add((mid, pct))
    o = {k: None for k in NUM}; o['commission_pct'] = pct; o['commission_levels'] = fmt_levels(lv)
    page_rows.append({'merchant_id': mid, 'merchant_name': sanitize_merchant(AU[mid].get('merchant_name')), 'site_url': site_url(mid), 'currency': 'AUD',
                      'in_partnership': 'yes' if mid in PSR else 'no', 'promo_type': 'COMMISSION', 'promo_name': 'Affiliate programme (page)',
                      'source': 'page', 'fetched_at': pmtime, 'classification_basis': 'keyword:' + PROG.search(title + ' ' + slug).group(0).lower(), **o})
rows += page_rows
order = {t: i for i, t in enumerate(TYPES)}
rows.sort(key=lambda x: (order[x['promo_type']], int(x['merchant_id']) if x['merchant_id'].isdigit() else 0, x['source'], x['promo_name']))
def cell(v):
    if v is None: return ''
    if isinstance(v, float): return round(v, 2)
    return v
rows = [{k: cell(r.get(k)) for k in COLS} for r in rows]
json.dump({'built': NOW.strftime('%Y-%m-%d %H:%M AEST'), 'au_merchants': len(AU), 'au_in_pubinfo': len(fetched_merchants), 'au_with_promos': len(with_promos),
           'promos_seen': n_promos_total, 'other': other['OTHER'], 'other_merchants': len(other_m['OTHER']), 'excl_nonaud_promos': excl_nonaud,
           'excl_nonaud_merchants': len(excl_nonaud_m), 'page_rows': len(page_rows), 'flags': {f'{a}|{b}': v for (a, b), v in flags_c.items()},
           'currency_source': dict(mcur_src)}, open(f'{O}/bonus_terms_AU_meta.json', 'w'), indent=1)
with open(f'{O}/bonus_terms_AU.rows.json', 'w') as fh: json.dump(rows, fh)
print(json.load(open(f'{O}/bonus_terms_AU_meta.json')))
print(collections.Counter(r['promo_type'] for r in rows))

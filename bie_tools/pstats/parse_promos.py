"""Classify and parse public promotions. Reuses logic.normalize / logic.extract / logic.numeric from the BIE project.
Text in the promotion description is preferred; platform fields are fallbacks (documented per field)."""
import sys, re, json
sys.path.insert(0, '/workspace/bie'); import logic
NUM = r'(\d{1,6}(?:[.,]\d{1,2})?)'
def f(x):
    try: return float(str(x).replace(',', '')) if x not in (None, '') else None
    except Exception: return None
def pos(x): v = f(x); return v if v and v > 0 else None
def money(x): v = f(x); return v if v and v >= 1 else None   # maxWithdraw < 1 is a ratio/percent on this platform, not money
def clean(name): return ' '.join(re.sub(r'<[^>]+>', ' ', str(name or '')).split())
ND_NAME = re.compile(r'(new\s*(member|register|reg\b|user|player|sign)|register|registration|sign\s*-?\s*up|newbie|new\s*comer|first\s*time\s*free|free\s*credit\s*new|welcome\s*free|free\s*new|new\s*free)', re.I)
ND_BAD = re.compile(r'(daily|weekly|monthly|365|hour|loss|share|download|\bapp\b|apps|birthday|vip|downline|telegram|social|rebate|commission|deposit|topup|top\s*up|reload|referr|refer|invite|check\s*-?\s*in|mystery|lucky|angpao|spin\b|tournament|leaderboard|losscredit|convert)', re.I)
W_NAME = re.compile(r'(welcome|1st\s*deposit|first\s*deposit|first\s*top\s*up|new\s*member\s*\d+\s*%|newbie\s*\d+\s*%|new\s*member\s*bonus\s*\d+|sign\s*up\s*bonus\s*\d+\s*%)', re.I)
W_BAD = re.compile(r'(welcome\s*back|daily|weekly|monthly|reload|rebate|loss|commission|downline|vip)', re.I)
def rx(pat, t, flags=re.I):
    m = re.search(pat, t, flags); return f(m.group(1)) if m else None
def text_terms(t):
    t = t.upper().replace('WIN OVER', 'WINOVER').replace('TURN OVER', 'TURNOVER').replace('ROLL OVER', 'ROLLOVER')
    return {
        'win_over_x':   rx(r'WINOVER\s*(?:X|TIMES?\s*)\s*' + NUM, t) or rx(NUM + r'\s*X\s*\(?\s*WINOVER', t),
        'win_over_amt': rx(r'WINOVER\s*(?:CREDIT\s*)?(?:MUST\s*)?(?:HIT|REACH|IS|:|=)?\s*(?:AUD|RM|SGD|\$|A\$)\s*' + NUM, t)
                        or rx(r'(?:CREDIT|BALANCE)\s*(?:MUST\s*)?(?:HIT|REACH)\s*(?:AUD|RM|SGD|\$|A\$)?\s*' + NUM, t),
        'turnover_x':   rx(r'(?:TURNOVER|ROLLOVER)\s*(?:X|TIMES?\s*)\s*' + NUM, t) or rx(NUM + r'\s*X\s*(?:TURNOVER|ROLLOVER)', t),
        'max_cashout':  rx(r'MAX(?:IMUM)?\s*(?:WITHDRAW(?:AL)?|CASH\s*-?\s*OUT|PAYOUT)\s*(?:IS|:|=)?\s*(?:AUD|RM|SGD|\$|A\$)\s*' + NUM, t)
                        or rx(r'MAX(?:IMUM)?\s*(?:WITHDRAW(?:AL)?|CASH\s*-?\s*OUT|PAYOUT)\s*(?:IS|:|=)?\s*' + NUM + r'(?!\s*X)', t),
        'min_withdraw': rx(r'MIN(?:IMUM)?\s*WITHDRAW(?:AL)?\s*(?:IS|:|=)?\s*(?:AUD|RM|SGD|\$|A\$)?\s*' + NUM, t),
        'max_bonus':    rx(r'MAX(?:IMUM)?\s*BONUS\s*(?:IS|:|=|UP\s*TO)?\s*(?:AUD|RM|SGD|\$|A\$)?\s*' + NUM, t),
        'min_deposit':  rx(r'MIN(?:IMUM)?\s*(?:DEPOSIT|TOP\s*-?\s*UP)\s*(?:IS|:|=)?\s*(?:AUD|RM|SGD|\$|A\$)?\s*' + NUM, t),
        'amount':       rx(r'(?:BONUS|FREE|CREDIT)\s*(?:AUD|RM|SGD|\$|A\$)\s*' + NUM, t),
        'pct':          rx(NUM + r'\s*%', t),
    }
def classify(p):
    n = logic.normalize(p); name = clean(n.get('name')); cond = str(n.get('claimcondition') or '').upper()
    desc = str(n.get('description') or '')
    is_dep = cond == 'DEPOSIT' or bool(pos(n.get('mintopup')))
    if ND_NAME.search(name) and not ND_BAD.search(name) and not is_dep and cond in ('FREE', 'CUSTOM', ''): return 'nodeposit'
    if W_NAME.search(name) and not W_BAD.search(name) and (is_dep or pos(n.get('bonus'))): return 'welcome'
    return None
def parse(p, kind):
    n = logic.normalize(p); t = text_terms(str(n.get('description') or '') + ' ' + clean(n.get('name')))
    cc = logic.extract(n)   # flattened claimConfig (conf_*), project helper
    rollover = pos(n.get('rollover'))
    if kind == 'nodeposit':
        return {'name': clean(n.get('name')), 'amount': pos(n.get('bonusfixed')) or t['amount'],
                'win_over': t['win_over_amt'] or pos(n.get('minwithdraw')),                    # platform minWithdraw = win-over credit target on free credits
                'max_cashout': money(n.get('maxwithdraw')) or t['max_cashout'],
                'turnover_x': t['turnover_x'] or rollover,
                'min_withdraw': t['min_withdraw'],
                'src_win_over': 'text' if t['win_over_amt'] else ('field:minWithdraw' if pos(n.get('minwithdraw')) else '')}
    mw = pos(n.get('minwithdraw'))
    return {'name': clean(n.get('name')), 'pct': pos(n.get('bonus')) or (t['pct'] if not pos(n.get('bonusfixed')) else None),
            'fixed': pos(n.get('bonusfixed')), 'max_bonus': t['max_bonus'],
            'min_deposit': pos(n.get('mintopup')) or t['min_deposit'],
            'win_over_x': t['win_over_x'] or (mw if mw and mw <= 50 else None),                  # deposit bonuses: minWithdraw small values = multiplier (validated vs text)
            'win_over_amt': t['win_over_amt'],
            'turnover_x': t['turnover_x'] or rollover,
            'max_deposit': pos(n.get('maxtopup')),
            'min_withdraw': t['min_withdraw'], 'max_withdraw': money(n.get('maxwithdraw')) or t['max_cashout'],
            'text_win_over_x': t['win_over_x'], 'field_minWithdraw': mw}
def site_terms(promos):
    """Pick the main no-deposit sign-up and main welcome-deposit promotion for a site (lowest displayOrder)."""
    nd = [p for p in promos if classify(p) == 'nodeposit' and (pos(p.get('bonusFixed')) or text_terms(str(p.get('description')))['amount'] or p.get('bonusRandom'))]
    wl = [p for p in promos if classify(p) == 'welcome']
    key = lambda p: (f(p.get('displayOrder')) if f(p.get('displayOrder')) is not None else 9999)
    return (parse(sorted(nd, key=key)[0], 'nodeposit') if nd else None, parse(sorted(wl, key=key)[0], 'welcome') if wl else None, len(nd), len(wl))

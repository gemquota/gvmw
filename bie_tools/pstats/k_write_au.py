"""Write bonus_terms_AU.csv/.xlsx from k_bonus_terms_au.py output, then copy to bie_tools. Offline."""
import json, csv, statistics, collections, shutil, datetime
import openpyxl
from openpyxl.styles import Font
O = '/workspace/bie_tools/pstats'; R = '/workspace/bie_deliverables/reports'; T = '/workspace/bie_tools'
rows = json.load(open(f'{O}/bonus_terms_AU.rows.json')); meta = json.load(open(f'{O}/bonus_terms_AU_meta.json'))
COLS = ['merchant_id', 'merchant_name', 'site_url', 'currency', 'in_partnership', 'promo_type', 'promo_name', 'amount_fixed', 'amount_pct',
        'max_bonus', 'min_deposit', 'rollover_x', 'rollover_amt', 'turnover_x', 'min_withdraw', 'max_withdraw', 'commission_pct',
        'commission_levels', 'source', 'fetched_at', 'classification_basis']
NUM = ['amount_fixed', 'amount_pct', 'max_bonus', 'min_deposit', 'rollover_x', 'rollover_amt', 'turnover_x', 'min_withdraw', 'max_withdraw', 'commission_pct']
TYPES = ['REGISTER', 'WELCOME', 'SHARE', 'DOWNLINE_FIRST_DEPOSIT', 'COMMISSION']
SHEET = {'REGISTER': 'Register', 'WELCOME': 'Welcome', 'SHARE': 'Share', 'DOWNLINE_FIRST_DEPOSIT': 'Downline FD', 'COMMISSION': 'Commission'}
built = meta['built']
with open(f'{R}/bonus_terms_AU.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, COLS); w.writeheader(); w.writerows(rows)
def st(v):
    v = [x for x in v if isinstance(x, (int, float))]
    return (round(min(v), 2), round(statistics.mean(v), 2), round(max(v), 2), len(v)) if v else ('', '', '', 0)
summ = []
for t in TYPES:
    rs = [r for r in rows if r['promo_type'] == t]
    s = {'promo_type': t, 'n_merchants': len({r['merchant_id'] for r in rs}), 'n_promos': len(rs),
         'n_merchants_in_partnership': len({r['merchant_id'] for r in rs if r['in_partnership'] == 'yes'})}
    for k in NUM:
        a, m, b, n = st([r[k] for r in rs]); s.update({f'{k}_min': a, f'{k}_avg': m, f'{k}_max': b, f'{k}_n': n})
    summ.append(s)
summ.append({'promo_type': 'OTHER (excluded from sheets)', 'n_merchants': meta['other_merchants'], 'n_promos': meta['other']})
fill = {t: {k: round(100 * sum(1 for r in rows if r['promo_type'] == t and r[k] not in ('', None)) / max(1, sum(1 for r in rows if r['promo_type'] == t)), 1)
            for k in NUM + ['promo_name', 'site_url', 'commission_levels']} for t in TYPES}
json.dump({'summary': summ, 'fill': fill}, open(f'{O}/bonus_terms_AU_summary.json', 'w'), indent=1)
notes = [
 f'AU-ONLY, PRIVATE RESEARCH. Built offline {built} from cached public promo data; no logins.',
 '',
 'METHOD',
 f'Scope: all {meta["au_merchants"]} merchant IDs in urls_au.csv (AUD merchant list). {meta["au_in_pubinfo"]} have a cached pubinfo record; {meta["au_with_promos"]} have at least one cached public promotion.',
 'in_partnership = yes when the merchant_id is one of the 540 rows in partnership_sites_AU.csv.',
 'Primary source = pubinfo.jsonl (platform public promotion list, no login), fetched_at = the original cache timestamp of that record.',
 'Secondary source = pages_content.jsonl: only the merchant\'s own affiliate or commission programme page (page title names the merchant), COMMISSION rows only. Partner directory pages were NOT used because their offer cards describe other sites. Page rows carry the cache file time as fetched_at (no per-page timestamp exists).',
 'Classification order: (1) structured claimConfig.customBonus (sharebonus = SHARE; downlinefirstdeposit, downlinedeposit, unlimiteddownlinedeposit = DOWNLINE_FIRST_DEPOSIT; commissionweek, commission = COMMISSION; rollcomm, rebate, rebatedays, instantRebate, netlossladder = player self-rebate = OTHER unless the name says commission or downline); (2) name keywords (commission, affiliate, agent, downline, referral, invite, share, social); (3) reused parse_promos rules for REGISTER (new member, register, sign up, without deposit) and WELCOME (welcome, first deposit). classification_basis records which rule fired.',
 'Field mapping (reused from parse_promos.py / g_build.py, text in the promo terms preferred, platform fields as fallback): amount_fixed = bonusFixed; amount_pct = bonus (percent); commission_pct = bonus for commission promos, else claimConfig rate level 1, else stated percentage; min_deposit = minTopup / conf min_topup / conf downlineMinTopupAmount (downline min deposit for SHARE and DOWNLINE rows); turnover_x = stated turnover multiple, else platform rollover / conf rollover.',
 'Win-over: rollover_x / rollover_amt come from stated win-over terms first; otherwise from platform minWithdraw: values up to 50 (or minWithdrawTimeAmount set) are read as a multiplier (rollover_x), larger values as the credit target amount (rollover_amt).',
 'max_withdraw = platform maxWithdraw (values below 1 are ratios and ignored). If maxWithdrawTimeAmount is set, maxWithdraw is a multiple of the bonus and is converted only when a fixed bonus amount is published, otherwise left blank. If maxWithdrawTimeDeposit is set it is a multiple of the deposit and is left blank.',
 'min_withdraw = explicitly stated minimum withdrawal in AUD only. On this platform the stated minimum withdrawal for free credits usually equals the win-over credit target, so it often duplicates rollover_amt.',
 'max_bonus = stated maximum bonus only. commission_levels = tiered rates when two or more levels are published (stated text, or claimConfig rate arrays).',
 '',
 'CAVEATS',
 'Blank = not published in the cached data. Nothing is estimated or imputed. All amounts AUD.',
 f'Promotions whose terms mention a non-AUD currency (and no AUD) were dropped: {meta["excl_nonaud_promos"]} promos.',
 f'OTHER promotions (daily/weekly reload, rebate, VIP, birthday, check-in, minigames, cross-site invitations etc.) are counted but not listed: {meta["other"]} promos across {meta["other_merchants"]} merchants.',
 'DOWNLINE_FIRST_DEPOSIT includes customBonus=downlinedeposit (bonus when a new downline deposits); the basis column lets you filter to downlinefirstdeposit only.',
 'Multiple rows per merchant per type are normal (tiers, slot vs live variants, mirrored listings).',
 'Platform minWithdraw semantics are inferred (multiplier vs target); about 90 percent (1114 of 1240) match the stated terms where both exist, and the stated terms win when present. See anomalies in the build report.',
 'Data is a snapshot from the cache dates; promotions change frequently.',
 'Safety: structured fields only; promo names sanitised (links, domains, handles, codes, contact details removed or blanked); no descriptions, links or codes are included.',
]
def nz(v): return isinstance(v, (int, float))
AN = [('turnover_x > 60 (platform rollover field likely holds the win-over target amount)', lambda r: nz(r['turnover_x']) and r['turnover_x'] > 60),
      ('turnover_x equals rollover_amt (same number in both fields)', lambda r: nz(r['turnover_x']) and r['turnover_x'] == r['rollover_amt']),
      ('commission_pct > 30', lambda r: nz(r['commission_pct']) and r['commission_pct'] > 30),
      ('WELCOME amount_pct > 200', lambda r: r['promo_type'] == 'WELCOME' and nz(r['amount_pct']) and r['amount_pct'] > 200),
      ('min_deposit >= 9999 (placeholder or accumulated downline deposit tier)', lambda r: nz(r['min_deposit']) and r['min_deposit'] >= 9999),
      ('max_withdraw >= 30000 (likely an effectively uncapped placeholder)', lambda r: nz(r['max_withdraw']) and r['max_withdraw'] >= 30000),
      ('REGISTER amount_fixed > 500', lambda r: r['promo_type'] == 'REGISTER' and nz(r['amount_fixed']) and r['amount_fixed'] > 500),
      ('rollover_amt below amount_fixed (target lower than the bonus)', lambda r: nz(r['rollover_amt']) and nz(r['amount_fixed']) and r['rollover_amt'] < r['amount_fixed']),
      ('no numeric term published at all', lambda r: not any(nz(r[k]) for k in NUM))]
anom = []
for label, fn in AN:
    rs = [r for r in rows if fn(r)]
    anom.append({'check': label, 'n_rows': len(rs), 'by_type': dict(collections.Counter(r['promo_type'] for r in rs)),
                 'examples': [f"{r['merchant_id']} {r['promo_type']} " + ' '.join(f'{k}={r[k]}' for k in NUM if nz(r[k])) for r in rs[:4]]})
json.dump(anom, open(f'{O}/bonus_terms_AU_anomalies.json', 'w'), indent=1)
dups = sum(v - 1 for v in collections.Counter(tuple(r[k] for k in COLS if k != 'fetched_at') for r in rows).values() if v > 1)
notes += ['', 'ANOMALY FLAGS (values kept as published; treat with care)'] + [f"{a['check']}: {a['n_rows']} rows" for a in anom] + \
         [f'Exact duplicate rows (same merchant, type, name and terms; separate promo IDs on the platform): {dups}',
          'Placeholder values of 1,000,000 or more, or runs of nines (99999 and up), were blanked as not real limits: ' + str(sum(v for k, v in meta['flags'].items() if 'sentinel' in k)) + ' cells.']
json.dump({'dups': dups}, open(f'{O}/bonus_terms_AU_dups.json', 'w'))
wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'All'
def put(ws, rs):
    ws.append(COLS)
    for c in ws[1]: c.font = Font(bold=True)
    for r in rs: ws.append([r[k] for k in COLS])
    ws.freeze_panes = 'A2'
put(ws, rows)
for t in TYPES: put(wb.create_sheet(SHEET[t]), [r for r in rows if r['promo_type'] == t])
ws = wb.create_sheet('Summary'); hdr = ['promo_type', 'n_merchants', 'n_merchants_in_partnership', 'n_promos'] + [f'{k}_{s}' for k in NUM for s in ('min', 'avg', 'max', 'n')]
ws.append(hdr)
for c in ws[1]: c.font = Font(bold=True)
for s in summ: ws.append([s.get(k, '') for k in hdr])
ws.append([]); ws.append(['All values AUD. n = number of rows with the field published.'])
ws = wb.create_sheet('Notes')
for line in notes: ws.append([line])
ws.column_dimensions['A'].width = 160
wb.save(f'{R}/bonus_terms_AU.xlsx')
for f in ('bonus_terms_AU.csv', 'bonus_terms_AU.xlsx'): shutil.copy2(f'{R}/{f}', f'{T}/{f}')
print('rows', len(rows)); print(json.dumps(summ, indent=0)[:6000]); print(json.dumps(fill))

"""RR-019 safety check over every cell of bonus_terms_AU.csv and .xlsx (both copies). Exit 1 on any hit."""
import re, csv, sys, openpyxl, collections
FILES = ['/workspace/bie_deliverables/reports/bonus_terms_AU', '/workspace/bie_tools/bonus_terms_AU']
CHECKS = {
 'url_http_www': re.compile(r'(?i)https?:|\bwww\.'),
 'domain_tld': re.compile(r'(?i)\.(com|net|vip|club|co|online|site|me|fun|io|asia)\b'),
 'ref_params': re.compile(r'(?i)\b(ref|aff|affid|invite|invitecode|code|refcode|referral|referralcode)\s*[=:]|[?&](ref|aff|invite|code|referral)\w*\s*='),
 'handle': re.compile(r'(?<![\w.])@[A-Za-z0-9_]{2,}'),
 'tme_wame': re.compile(r'(?i)\b(t|wa)\.me\b'),
 'email': re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+'),
 'digits8': re.compile(r'\d{8,}'),
 'plus61': re.compile(r'\+\s?61'),
 'au_mobile_04xx': re.compile(r'(?<![\d.:\-])04\d{2}(?!\d)'),
 'password': re.compile(r'(?i)passw(or)?d'),
}
CODEISH = re.compile(r'(?=[A-Za-z0-9]{5,})(?:[A-Za-z]+\d|\d+[A-Za-z])[A-Za-z0-9]*')
SITE = re.compile(r'^https://[a-z0-9.-]+\.[a-z0-9-]+$')
hits = collections.Counter(); examples = []; cells = 0
def scan(where, header, row):
    global cells
    for h, v in zip(header, row):
        s = '' if v is None else str(v); cells += 1
        if h == 'site_url':
            if s and not SITE.match(s): hits['site_url_not_bare'] += 1; examples.append((where, h, s))
            continue
        for k, rx in CHECKS.items():
            if rx.search(s): hits[k] += 1; len(examples) < 30 and examples.append((where, h, k, s[:80]))
        if h == 'promo_name' and CODEISH.search(s): hits['promo_name_codeish'] += 1; examples.append((where, h, 'codeish', s[:80]))
for base in FILES:
    with open(base + '.csv', encoding='utf-8') as fh:
        rd = csv.reader(fh); header = next(rd); scan(base + '.csv:header', ['h'] * len(header), header)
        for row in rd: scan(base + '.csv', header, row)
    wb = openpyxl.load_workbook(base + '.xlsx', read_only=True)
    for ws in wb.worksheets:
        it = ws.iter_rows(values_only=True); header = [str(x) if x is not None else '' for x in next(it)]
        scan(f'{base}.xlsx:{ws.title}:header', ['h'] * len(header), header)
        for row in it: scan(f'{base}.xlsx:{ws.title}', header if ws.title not in ('Notes',) else ['note'] * len(row), row)
print('cells scanned', cells, '| hits', sum(hits.values()), dict(hits))
for e in examples[:30]: print('  ', e)
sys.exit(1 if hits else 0)

"""Write in/config/urls_by_merchant.txt + .csv from by_merchant.jsonl (last record per merchant wins)."""
import json, csv
B = '/workspace/bie'; O = '/workspace/bie_tools/pstats'
rec = {}
for l in open(f'{O}/by_merchant.jsonl'): j = json.loads(l); rec[j['merchant_id']] = j
key = lambda m: (0, int(m)) if m.isdigit() else (1, m)
ok = [rec[m] for m in sorted(rec, key=key) if rec[m]['url']]
with open(f'{B}/in/config/urls_by_merchant.txt', 'w') as f: f.write(''.join(r['url'] + '\n' for r in ok))
with open(f'{B}/in/config/urls_by_merchant.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['merchant_id', 'merchant_name', 'url', 'mirror_count', 'checked_at', 'elapsed_s', 'mirrors_tried', 'last_error'])
    for m in sorted(rec, key=key):
        r = rec[m]; w.writerow([m, r['merchant_name'], r['url'], r['mirror_count'], r['checked_at'], r['elapsed_s'], r['tried'], '' if r['url'] else r.get('last_error', '')])
print('merchants', len(rec), 'with url', len(ok), 'without', len(rec) - len(ok))

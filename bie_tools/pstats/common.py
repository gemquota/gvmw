import json, time, requests, urllib3
urllib3.disable_warnings()
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest'}
def api(host, module, merchant_id, extra=None, deadline=30, max_bytes=8_000_000):
    """Public (no-login) platform API call exactly as the site's own JS does it: empty accessId/accessToken."""
    data = {'module': module, 'merchantId': merchant_id, 'accessId': '', 'accessToken': '', 'walletIsAdmin': ''}
    data.update(extra or {})
    t0 = time.time(); buf = bytearray()
    with requests.post(f'https://{host}/api/v1/index.php', data=data, headers={**UA, 'Referer': f'https://{host}/', 'Origin': f'https://{host}'},
                       timeout=15, verify=False, stream=True) as r:
        for ch in r.iter_content(65536):
            buf += ch
            if time.time() - t0 > deadline or len(buf) > max_bytes: raise TimeoutError('deadline/size')
    return json.loads(buf.decode('utf-8', errors='ignore'))
def done_keys(path, key):
    s = set()
    try:
        for l in open(path):
            try: s.add(json.loads(l)[key])
            except Exception: pass
    except FileNotFoundError: pass
    return s

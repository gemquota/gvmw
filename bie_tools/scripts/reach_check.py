"""No-login reachability check reusing BIE's own steps (net.create_session, net.get_html,
flow.get_merchant_details, flow.get_api_endpoint). Never logs in or registers.
Usage (cwd = /workspace/bie): python /workspace/bie_tools/scripts/reach_check.py <urls_file> <out_csv> [workers]"""
import sys, csv, time, json, re, concurrent.futures as cf
from urllib.parse import urlparse
import requests, cloudscraper
import base, net, flow

def norm(u):
    u = u.strip().strip('<>').split()[0] if u.strip() else ''
    if not u: return ''
    if '://' not in u: u = 'https://' + u
    p = urlparse(u)
    host = (p.hostname or '').lower().rstrip('.')
    return f"https://{host}" if host else ''

def classify(e):
    s = f"{type(e).__name__}: {e}"
    if isinstance(e, requests.exceptions.HTTPError):
        code = e.response.status_code if e.response is not None else 0
        server = (e.response.headers.get('server','') if e.response is not None else '').lower()
        if code in (403, 503) and 'cloudflare' in server: return 'cloudflare_403', s
        if code == 403: return 'http_403', s
        return f'http_{code}', s
    if 'cloudflare' in type(e).__name__.lower() or 'Captcha' in s or 'challenge' in s.lower(): return 'cloudflare_challenge', s
    if 'Blocked: Access Denied' in s: return 'access_denied', s
    if isinstance(e, requests.exceptions.Timeout) or 'timed out' in s.lower(): return 'timeout', s
    if isinstance(e, requests.exceptions.SSLError): return 'ssl', s
    if 'NameResolution' in s or 'Failed to resolve' in s or 'gaierror' in s or 'Name or service not known' in s: return 'dns', s
    if isinstance(e, requests.exceptions.ConnectionError): return 'connection', s
    if 'merchant identification' in s: return 'parse_failed', s
    return 'other', s

def check(url):
    row = {'url': url, 'reachable': 0, 'http_status': '', 'final_url': '', 'html_len': 0,
           'merchant_ok': 0, 'merchant_id': '', 'merchant_name': '', 'api_endpoint': '', 'api_ok': 0,
           'api_reply': '', 'stage_failed': '', 'reason': '', 'detail': '', 'secs': 0}
    t = time.time(); stage = 'homepage'
    try:
        s = net.create_session(None)
        first = {}
        s.hooks['response'].append(lambda r, *a, **k: first.setdefault('r', r))
        html = net.get_html(s, url)
        r = first.get('r')
        row.

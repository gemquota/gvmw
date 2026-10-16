import requests
import cloudscraper
import re
import base64
import json
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin
import aiohttp
import asyncio

# ==============================================================================
# SECTION: NETWORK (Original: network.py)
# Description: Sync/Async HTTP stacks and redirect handlers.
# ==============================================================================

class AsyncNetworkManager:
    """Manages asynchronous network sessions for high-volume API requests."""
    def __init__(self):
        self.connector = aiohttp.TCPConnector(limit=100, ssl=False)
        self.client = None

    async def __aenter__(self):
        self.client = aiohttp.ClientSession(connector=self.connector)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.client: await self.client.close()

    async def post_json(self, url, data, cookies=None, proxy=None):
        import base
        headers = {'User-Agent': base.USER_AGENT}
        try:
            async with self.client.post(url, json=data, cookies=cookies, proxy=proxy, timeout=base.TIMEOUT) as response:
                return await response.json()
        except Exception as error: raise error

    async def get_json(self, url, params=None, cookies=None, proxy=None):
        import base
        headers = {'User-Agent': base.USER_AGENT}
        try:
            async with self.client.get(url, params=params, cookies=cookies, proxy=proxy, timeout=base.TIMEOUT) as response:
                return await response.json()
        except Exception as error: raise error

def create_session(proxy=None):
    """Creates a cloudscraper session, optionally with a proxy."""
    import base
    session = cloudscraper.create_scraper()
    session.headers.update({'User-Agent': base.USER_AGENT})
    if proxy:
        proxy_str = proxy if '://' in proxy else f"http://{proxy}"
        session.proxies = {'http': proxy_str, 'https': proxy_str}
    return session

def get_next_healthy_proxy(api_key):
    """Get next healthy proxy from DB, verifying via AbuseIPDB."""
    import base
    while True:
        query_str = """
            SELECT proxy, burn_count FROM proxy_health 
            WHERE status = 'active' 
            OR (status = 'cooling' AND datetime(last_burn_ts, '+' || (burn_count * 12) || ' hours') < CURRENT_TIMESTAMP)
            ORDER BY burn_count ASC, RANDOM() LIMIT 1
        """
        results = base.query(query_str)
        if not results: return None
        proxy_ip = results[0][0]
        parsed = urlparse(proxy_ip if '://' in proxy_ip else f"http://{proxy_ip}")
        clean_ip = parsed.hostname or proxy_ip.split(':')[0]
        if burned(api_key, clean_ip):
            mark_proxy_burned(proxy_ip)
            continue
        base.query("UPDATE proxy_health SET status='active' WHERE proxy=?", (proxy_ip,))
        return proxy_ip

def mark_proxy_burned(proxy_ip):
    """Mark proxy as burned/cooling in the database."""
    import base
    if not proxy_ip: return
    base.log("WARNING", "NET", f"Proxy Burned: {proxy_ip}")
    res = base.query("SELECT burn_count FROM proxy_health WHERE proxy=?", (proxy_ip,))
    if not res:
        base.query("INSERT INTO proxy_health (proxy, burn_count, last_burn_ts, status) VALUES (?, 1, CURRENT_TIMESTAMP, 'cooling')", (proxy_ip,))
        return
    burn_count = res[0][0] + 1
    status_str = 'cooling'
    if burn_count >= 10: status_str = 'blacklisted'
    base.query("UPDATE proxy_health SET burn_count=?, last_burn_ts=CURRENT_TIMESTAMP, status=? WHERE proxy=?", (burn_count, status_str, proxy_ip))

def get_html(session, url):
    """Fetches HTML from a URL, handling various redirect types."""
    import base
    response = session.get(url, timeout=base.TIMEOUT)
    response.raise_for_status()
    html = response.text
    # ParkLogic check
    if '<title>Redirecting...</title>' in html and 'router.parklogic.com' in html:
        match = re.search(r'"(ey[A-Za-z0-9+/=]{50,})"', html)
        if match:
            payload = json.loads(base64.b64decode(match.group(1)))
            payload['parameters'].update({'adBlockingDetected': False, 'webdriver': False})
            response = session.post('https://router.parklogic.com/', data=json.dumps(payload), timeout=base.TIMEOUT)
            if response.text.startswith('http'): 
                return session.get(response.text.strip(), timeout=base.TIMEOUT).text
    # JS Redirect check
    patterns = [r'window\.location\.href\s*=\s*["\']([^"\"]+)["\']', r'location\.replace(["\']([^"\"]+)["\'])']
    for regex_pattern in patterns:
        match = re.search(regex_pattern, html)
        if match:
            return session.get(urljoin(url, match.group(1)), timeout=base.TIMEOUT).text
    return html

def post_json(session, url, data):
    import base
    return session.post(url, json=data, timeout=base.TIMEOUT).json()

def get_json(session, url, params=None):
    import base
    return session.get(url, params=params, timeout=base.TIMEOUT).json()

# ==============================================================================
# SECTION: HEALTH (Original: network_health.py)
# Description: AbuseIPDB reputation monitoring and status mapping.
# ==============================================================================

def check(api_key, ip):
    """Actual AbuseIPDB check with caching."""
    import base
    if not api_key: return 0, "No Key"
    res = base.query("SELECT score, timestamp FROM ip_cache WHERE ip=?", (ip,))
    if res:
        score, timestamp = res[0]
        if datetime.fromisoformat(timestamp) + timedelta(hours=1) > datetime.utcnow(): return score, "Cached"
    try:
        url = 'https://api.abuseipdb.com/api/v2/check'
        headers = {'Accept': 'application/json', 'Key': api_key}
        resp = requests.get(url, headers=headers, params={'ipAddress': ip, 'maxAgeInDays': '90'}, timeout=10)
        if resp.status_code == 200:
            score = resp.json()['data']['abuseConfidenceScore']
            base.query("REPLACE INTO ip_cache (ip, score, timestamp) VALUES (?, ?, CURRENT_TIMESTAMP)", (ip, score))
            return score, "Live"
        if resp.status_code == 429: return 0, "Rate Limit"
        return 100, f"HTTP {resp.status_code}"
    except Exception as error: return 0, str(error)

def burned(api_key, ip):
    """Is proxy burned? (Score > 50)"""
    if not api_key: return False
    score, _ = check(api_key, ip)
    return score > 50

def status(ip_score):
    """Returns human-readable status and color."""
    if ip_score >= 90: return "HEALTHY", "green"
    if ip_score >= 50: return "WARN", "yellow"
    return "CRITICAL", "red"
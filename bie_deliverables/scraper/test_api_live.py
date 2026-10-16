import cloudscraper
import flow
import json

url = "https://1bigwin.com"
try:
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url, timeout=15)
    html = response.text
    mid, mname = flow.get_merchant_details(html, None, url)
    print(f"Merchant ID: {mid}, Name: {mname}")
    
    api_endpoint = flow.get_api_endpoint(url)
    headers = {
        "Referer": url,
        "Origin": url,
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    payload = {
        "module": "/users/userData",
        "merchantId": mid,
        "token": "",
        "id": "",
        "domainId": "0",
        "walletIsAdmin": ""
    }
    resp = scraper.post(api_endpoint, json=payload, headers=headers, timeout=15)
    print(f"Status: {resp.status_code}")
    print(f"Text: {resp.text[:100]}")
    data = resp.json()
    print(f"Response: {data}")
except Exception as e:
    print(f"Error: {e}")

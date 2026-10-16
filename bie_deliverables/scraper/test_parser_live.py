import requests
import flow
import net

url = "https://ufo9.com"
try:
    response = requests.get(url, timeout=15)
    html = response.text
    print(f"Status: {response.status_code}")
    print(f"HTML length: {len(html)}")
    if "Access denied" in html:
        print("Access Denied detected")
    
    mid, mname = flow.get_merchant_details(html, None, url)
    print(f"Merchant ID: {mid}, Name: {mname}")
except Exception as e:
    print(f"Error: {e}")

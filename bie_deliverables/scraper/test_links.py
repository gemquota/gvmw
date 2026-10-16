import requests
import concurrent.futures

urls = [
    "https://bondi333.com", "https://avg88.com", "https://luck77au.com", "https://in8.one",
    "https://legit99.com", "https://select777.net", "https://mrpokies77.com", "https://ozreel88.com",
    "https://queenau.com", "https://epicpokies.com", "https://1winbet369.com", "https://jw8au.com",
    "https://spinfortune777.com", "https://hello88au.com", "https://play369.co", "https://kingdom9aus.com",
    "https://mcdollar9.com", "https://ausbet88.com", "https://rolex9.net", "https://southern9.com",
    "https://bigboss88.vip", "https://unitedau.com", "https://spaceman369.com", "https://wombats88.com",
    "https://aud77.net", "https://emax7.co", "https://keno99.com", "https://super996.com",
    "https://avengeraus1.com", "https://tab99au.com", "https://mrpoint.co", "https://candy96.com",
    "https://cyberpunk369.com", "https://mnp88.pro", "https://pokies4bet.com", "https://raabet9.com",
    "https://candymommy.co", "https://aud33.com", "https://ufo9.asia", "https://panda95au.com"
]

def check_url(url):
    try:
        response = requests.get(url, timeout=10, verify=False)
        if response.status_code < 400:
            return url, True
    except Exception:
        pass
    return url, False

online_urls = []
print("Checking links...")
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(check_url, urls)
    for url, is_online in results:
        if is_online:
            online_urls.append(url)
            print(f"[ONLINE] {url}")
        else:
            print(f"[OFFLINE] {url}")

with open("online_commission_sites.md", "w") as f:
    f.write("# Active Commission and Downline Bonus Sites\n\n")
    f.write("The following sites from the original list were found to be online.\n\n")
    for url in online_urls:
        f.write(f"- [{url}]({url})\n")

print(f"\nDone! Saved {len(online_urls)} active sites to online_commission_sites.md")

import requests
import concurrent.futures

urls = [
    "https://9au.com", "https://bondi333.com", "https://avg88.com", "https://luck77au.com",
    "https://in8.one", "https://legit99.com", "https://select777.net", "https://mrpokies77.com",
    "https://ozreel88.com", "https://queenau.com", "https://ubet96.com", "https://weplay88.com",
    "https://epicpokies.com", "https://cr33au.com", "https://1winbet369.com", "https://jw8au.com",
    "https://spinfortune777.com", "https://astar77au.com", "https://hello88au.com", "https://play369.co",
    "https://kingdom9aus.com", "https://mcdollar9.com", "https://enjoy96.com", "https://clubimperioaus.com",
    "https://ezaud.com", "https://v8au.com", "https://betzilla88.com", "https://ausbet88.com",
    "https://rolex9.net", "https://southern9.com", "https://bigboss88.vip", "https://nightclubaus.com",
    "https://unitedau.com", "https://spaceman369.com", "https://wombats88.com", "https://eebet9.com",
    "https://aud77.net", "https://vip99.com", "https://audgaming8.com", "https://emax7.co",
    "https://keno99.com", "https://sm8aud.com", "https://bonus96.com", "https://super996.com",
    "https://aud2u.com", "https://avengeraus1.com", "https://tab99au.com", "https://mrpoint.co",
    "https://candy96.com", "https://cyberpunk369.com", "https://mnp88.pro", "https://ufo9.asia",
    "https://onyxaud.com", "https://pokies4bet.com", "https://vpower8.com", "https://thepokies96.com",
    "https://topaz33.com", "https://aus2u.com", "https://bs22au.com", "https://raabet9.com",
    "https://harbour33.com", "https://candymommy.co", "https://panda95au.com", "https://aud33.com",
    "https://thepokies33.com"
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

with open("online_expanded_bonus_sites.md", "w") as f:
    f.write("# Active Expanded Bonus Sites\n\n")
    f.write("The following sites from the expanded list (Commissions, Downlines, Rebates, Airdrops) were found to be online.\n\n")
    for url in online_urls:
        f.write(f"- [{url}]({url})\n")

print(f"\nDone! Saved {len(online_urls)} active sites to online_expanded_bonus_sites.md")

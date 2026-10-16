import sqlite3
import requests
import concurrent.futures
import csv

def get_stats():
    conn = sqlite3.connect('db/base.db')
    cursor = conn.cursor()
    query = """
    WITH filtered_bonuses AS (
        SELECT url, bonus_name, amount FROM bonuses
        WHERE 
            (
                (bonus_name LIKE '%commission%' OR bonus_name LIKE '%commish%' OR bonus_name LIKE '%comision%' OR bonus_name LIKE '%referral%' OR bonus_name LIKE '%affiliate%' OR bonus_name LIKE '%share bonus%')
                AND (amount >= 5 OR bonus_name LIKE '%$5%' OR bonus_name LIKE '%5$%')
            )
            OR 
            (
                bonus_name LIKE '%downline%' 
                AND bonus_name LIKE '%deposit%'
                AND amount > 0
            )
            OR
            (
                bonus_name LIKE '%rebate%' OR bonus_name LIKE '%cashback%' OR bonus_name LIKE '%airdrop%' OR bonus_name LIKE '%angpao%'
            )
    ),
    stats AS (
        SELECT 
            url, 
            MAX(CASE WHEN bonus_name LIKE '%commission%' OR bonus_name LIKE '%commish%' OR bonus_name LIKE '%comision%' OR bonus_name LIKE '%referral%' OR bonus_name LIKE '%affiliate%' OR bonus_name LIKE '%share bonus%' THEN amount ELSE 0 END) as last_comm_val,
            AVG(CASE WHEN amount > 0 THEN amount ELSE NULL END) as historical_avg,
            SUM(amount) as total_value,
            MAX(amount) as max_amount
        FROM filtered_bonuses 
        GROUP BY url
    )
    SELECT 
        s.url, s.last_comm_val, s.historical_avg, s.total_value,
        (SELECT b.bonus_name FROM bonuses b WHERE b.url = s.url AND b.amount = s.max_amount LIMIT 1) as best_bonus_type
    FROM stats s;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def check_url(row):
    url = row[0]
    try:
        response = requests.get(url, timeout=10, verify=False)
        if response.status_code < 400:
            return row, True
    except Exception:
        pass
    return row, False

def main():
    print("Gathering stats from DB...")
    stats = get_stats()
    
    print(f"Checking status for {len(stats)} sites...")
    online_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(check_url, row): row for row in stats}
        for future in concurrent.futures.as_completed(future_to_url):
            row, is_online = future.result()
            if is_online:
                online_data.append(row)
                print(f"[ONLINE] {row[0]}")
            else:
                print(f"[OFFLINE] {row[0]}")

    # Sort by total value descending
    online_data.sort(key=lambda x: x[3], reverse=True)

    print("\nGenerating report...")
    with open("online_stats_report.md", "w") as f:
        f.write("# Active Sites with Commission Statistics\n\n")
        f.write("| Site URL | Last Commission | Historical Avg | Total Value | Best Type |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        for url, last, avg, total, btype in online_data:
            # Clean HTML tags from bonus type
            clean_type = "N/A"
            if btype:
                clean_type = btype.replace("<b>", "").replace("</b>", "").replace('<b style="color:gold;">', "").replace('<b style="color:black;">', "").strip()
            
            last_fmt = f"${last:,.2f}" if last else "$0.00"
            avg_fmt = f"${avg:,.2f}" if avg else "$0.00"
            total_fmt = f"${total:,.2f}" if total else "$0.00"
            f.write(f"| [{url}]({url}) | {last_fmt} | {avg_fmt} | {total_fmt} | {clean_type} |\n")

    print(f"Done! Saved {len(online_data)} active sites to online_stats_report.md")

if __name__ == "__main__":
    main()

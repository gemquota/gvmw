# Repeatable same-platform discovery (no login / no registration / no referral links)

Platform test (nologin_check.py): homepage has MERCHANTID/MERCHANTNAME (flow.get_merchant_details) AND
GET https://<host>/api/v1/index.php returns the platform JSON ({"status":"ERROR","data":{"message":"Invalid Action!"}}).
Only bare https://<host> URLs are ever fetched; referral paths (e.g. /RF123...) are stripped by normalize().

Run from /tmp (shell quirk): `cd /workspace/bie && .venv/bin/python /workspace/bie_tools/discover.py <source>`
Every test appends rows to bie_tools/candidates_<tag>.csv as it goes; already-tested hosts are skipped on rerun.
`discover.py merge` appends newly confirmed hosts to in/config/newurls_found.txt, rebuilds urls_combined.txt
(urls.txt + newurls_found.txt, deduped) and appends to bie_tools/newurls_found_detail.csv (source + mirror flag).
`run_all.sh` = full sequential pipeline with a merge after each step.

Sources (productive first):
- partners   : on every confirmed site's cached homepage, pages whose slug/title contain "partner" (embedded pages JSON,
               e.g. /luxegamingpartner, /speedpoolfloating, /partnership) + heylink.me link pages -> fetch each, harvest domains.
- homepages  : every confirmed homepage embeds sister-site links; also yields Telegram/Facebook handles (leads_homepages.txt).
- telegram   : public channel previews https://t.me/s/<handle> for handles found on homepages (bots/CS accounts skipped).
- urlscan    : fingerprint search on urlscan.io public API for pages loading the platform CDN hosts
               (domain:cdn.vefrop.com, domain:xt30sf.b-cdn.net). Use a plain User-Agent; ~32 pages before throttling.
- sameip     : reverse IP via rapiddns.io same-IP pages for platform IPs (platform_ips.txt; Alibaba Cloud SG 47.x / 43.98.x / 8.2xx).
- file       : any candidate list (e.g. web-search findings in search_v3.txt, TAG=websearch).
- pages      : arbitrary public listing pages (aggregators such as pokiesmate.bet/bonus, truebluepokies.win/bonus, auspokieslist.com).
Unproductive / unavailable: crt.sh (502 outage all session), HackerTarget reverse IP (free quota exhausted),
Facebook/X/Threads (login wall; no listings readable logged-out), k3o58k.com API docs (only placeholder domains).

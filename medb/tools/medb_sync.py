#!/usr/bin/env python3
"""Live account sync from cron / the command line (D-78). Talks only to the local MedB API
(http://127.0.0.1:8765) with **your user token** -- assistants' tokens are refused by the API.

    python3 tools/medb_sync.py status
    python3 tools/medb_sync.py run --all                # every enabled + connected service
    python3 tools/medb_sync.py run --service github
    python3 tools/medb_sync.py connect --service github # device flow: prints the code, waits for you

Cron example (hourly):  0 * * * *  cd /path/to/medb && python3 tools/medb_sync.py run --all >> data/sync_cron.log 2>&1

Token: --token, else $MEDB_USER_TOKEN, else the "user" entry of data/api_tokens.json. The token is never printed.
Exit status: 0 ok, 1 a sync failed, 2 refused / API unreachable.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def user_token(arg):
    if arg:
        return arg
    if os.environ.get("MEDB_USER_TOKEN"):
        return os.environ["MEDB_USER_TOKEN"]
    tokens = json.loads((ROOT / "data" / "api_tokens.json").read_text())
    return tokens.get("user") or next(t for t, a in tokens.items() if a == "user")


def call(api, token, path, body=None):
    if not api.startswith(("http://127.0.0.1", "http://[::1]", "http://localhost")):
        raise SystemExit("medb_sync talks to the local MedB API only")
    req = urllib.request.Request(api + path, data=None if body is None else json.dumps(body).encode(),
                                 method="GET" if body is None else "POST",
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read() or b"{}")
        except ValueError:
            return e.code, {}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["status", "run", "connect"])
    ap.add_argument("--service")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--api", default="http://127.0.0.1:8765")
    ap.add_argument("--token")
    a = ap.parse_args(argv)
    tok = user_token(a.token)
    try:
        if a.cmd == "status":
            st, r = call(a.api, tok, "/api/sync/status")
            if st != 200:
                print(json.dumps(r), file=sys.stderr)
                return 2
            for s, v in r["services"].items():
                last = v["last_sync"] or {}
                print(f"{s:16} {'on ' if v['enabled'] else 'off'} {'connected' if v['connected'] else '-':10} "
                      f"{v['account_id'] or '':30} items={v['items']:<6} last={last.get('at') or 'never'} "
                      f"{('ERROR ' + last['error']) if last.get('error') else ''}")
            return 0
        if a.cmd == "run":
            if not (a.all or a.service):
                ap.error("run needs --service or --all")
            st, r = call(a.api, tok, "/api/sync/run", {"all": True} if a.all else {"service": a.service})
            print(json.dumps(r, indent=1))
            if st != 200:
                return 2
            runs = r.get("runs", [r])
            return 0 if all(x.get("ok") for x in runs) else 1
        # connect
        if not a.service:
            ap.error("connect needs --service")
        st, r = call(a.api, tok, "/api/sync/connect", {"service": a.service})
        if st != 200:
            print(json.dumps(r), file=sys.stderr)
            return 2
        if r.get("mode") == "device":
            print(f"Open {r['verification_uri']} and enter the code:  {r['user_code']}")
        elif r.get("mode") == "loopback":
            print("Open this URL in your browser and approve read-only access:\n" + r["auth_url"])
        else:
            print(json.dumps(r))
            return 0
        while True:
            time.sleep(max(2, int(r.get("interval") or 2)))
            st, p = call(a.api, tok, "/api/sync/connect_poll", {"service": a.service})
            if st != 200:
                print(json.dumps(p), file=sys.stderr)
                return 2
            if not p.get("pending"):
                print(f"Connected: {p.get('account_id')}  scopes={p.get('scopes')}")
                return 0
    except urllib.error.URLError as e:
        print(f"MedB API unreachable at {a.api}: {e.reason}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

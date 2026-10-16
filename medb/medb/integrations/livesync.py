"""Live account sync into the local corpus (Gem's F-26 ruling, DECISIONS D-76..D-78).

Off by default; each service is opted into by the user (``config.integrations.sync``)
and connected by the user (OAuth for remote providers; a profile path for local
browsers). Assistants (agent/inference/MCP actors), readers and auditors can
never connect, sync or disconnect.

Every synced item is an ordinary corpus item (ingest grant required, default
sensitivity high, use grant required to read, withdrawable, never erased) with
provenance: service, provider, account id, API endpoint, remote object id,
version (etag / updated time / history id), sync run id, response SHA-256.
Sync is incremental (Gmail history ids, Calendar/People sync tokens, GitHub
``since``/ETags, browser visit-time cursors) and idempotent: a
remote object whose version is already in the corpus is skipped; a changed
version is ingested as a new item that names the item it supersedes.

Remote deletions are recorded (``REMOTE_DELETION`` in the ``sync`` stream) and
notified; they never erase or withdraw anything automatically (F-32).
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import secrets
import shutil
import sqlite3
import tempfile
from pathlib import Path
from urllib.parse import quote

from ..errors import NotAuthorized, PermissionDenied
from ..interfaces import reaches
from . import oauth
from .importers import COOKIE_SQL, _clip, mail_item, unix_us_ts, webkit_ts
from .sync_http import ALLOWED_HOSTS, HostNotAllowed, SyncHttp, SyncHttpError
from .sync_tokens import ClientStore, TokenStore

STREAM = "sync"
SERVICES = {
    "google_gmail": {"provider": "google", "label": "Gmail", "scope": "correspondence"},
    "google_calendar": {"provider": "google", "label": "Google Calendar", "scope": "calendar"},
    "google_contacts": {"provider": "google", "label": "Google Contacts (People API)", "scope": "contacts"},
    "github": {"provider": "github", "label": "GitHub", "scope": "code"},
    "chrome_local": {"provider": "local", "label": "Chrome profile (local, live)", "scope": "browsing"},
    "firefox_local": {"provider": "local", "label": "Firefox profile (local, live)", "scope": "browsing"},
}
SYNC_ACTORS = ("user", "system")  # system = the user's own local schedule (config), never an assistant


class SyncRefused(Exception):
    def __init__(self, reason: str, detail: str = ""):
        super().__init__(detail or reason)
        self.reason = reason


class SyncDisabled(SyncRefused):
    """The service (or live sync as a whole) is off, or no OAuth client is configured (HTTP 409)."""


def _sha(obj) -> str:
    b = obj if isinstance(obj, bytes) else json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(b).hexdigest()


def _next_link(link: str | None) -> str | None:
    for part in (link or "").split(","):
        m = re.match(r'\s*<([^>]+)>;\s*rel="next"', part)
        if m:
            return m.group(1)
    return None


class SyncManager:
    def __init__(self, medb, config: dict, root: Path, transport=None, suspensions=None):
        self.m = medb
        self.config = config or {}
        self.root = Path(root)
        self.tokens = TokenStore(self._p(self.config.get("token_dir", "data/sync_tokens")))
        self.clients = ClientStore(self._p(self.config.get("clients_file", "data/sync_clients.json")))
        self.http = SyncHttp(transport)
        self.pending: dict[str, dict] = {}
        self._suspensions = suspensions

    def _p(self, rel) -> Path:
        p = Path(rel).expanduser()
        return p if p.is_absolute() else self.root / p

    # ------------------------------------------------------------ config/state
    @property
    def enabled(self) -> bool:
        return bool(self.config.get("enabled"))

    def svc_cfg(self, service: str) -> dict:
        return (self.config.get("services") or {}).get(service) or {}

    def service_enabled(self, service: str) -> bool:
        return self.enabled and service in SERVICES and bool(self.svc_cfg(service).get("enabled"))

    def provider_services(self, provider: str) -> list[str]:
        return [s for s, d in SERVICES.items() if d["provider"] == provider and self.service_enabled(s)]

    def events(self, service: str | None = None, kinds=None) -> list[dict]:
        return [e for e in self.m.store.events(STREAM, kinds=kinds) if service is None or e["body"].get("service") == service]

    def connection(self, service: str) -> dict | None:
        prov = SERVICES[service]["provider"]
        if prov == "local":
            evs = self.events(service, kinds=["CONNECT", "DISCONNECT"])
            return evs[-1]["body"] if evs and evs[-1]["kind"] == "CONNECT" else None
        return self.tokens.public(prov)

    def source(self, service: str) -> str:
        """Ingest source: ``sync:<service>`` unless the user set ``services.<id>.source`` (must start with
        ``sync:``; e.g. one ``sync:google`` grant for the three Google services)."""
        src = self.svc_cfg(service).get("source") or f"sync:{service}"
        if not str(src).startswith("sync:"):
            raise ValueError(f"services.{service}.source must start with 'sync:'")
        return src

    def connectable(self, service: str) -> tuple[bool, list[str]]:
        """(ready to Connect, names of what is missing) -- never values."""
        d = SERVICES[service]
        why = [] if self.service_enabled(service) else ["service_disabled"]
        if d["provider"] == "local":
            pp = self.svc_cfg(service).get("profile_path")
            if not pp or not Path(pp).expanduser().is_dir():
                why.append("profile_path")
        else:
            why += self.clients.missing(d["provider"])
        return not why, why

    def hosts_in_use(self) -> list[str]:
        provs = {SERVICES[s]["provider"] for s in SERVICES if self.service_enabled(s)}
        return sorted(h for p in provs for h in ALLOWED_HOSTS.get(p, ()))

    # ------------------------------------------------------------ guards
    def _user_only(self, actor: str, what: str, service: str):
        if actor != "user":
            self.m.gov.record("PROHIBITED_ATTEMPT", actor, reason=f"sync_{what}_requires_user", service=service)
            raise NotAuthorized(f"only the user can {what} account sync")

    def _refuse(self, actor: str, reason: str, detail: str, service: str):
        self.m.gov.record("SYNC_REFUSED", actor, reason=reason, detail=detail, service=service)
        cls = SyncDisabled if reason in ("service_disabled", "oauth_client_not_configured") else SyncRefused
        raise cls(reason, detail)

    def _need_enabled(self, actor, service):
        if service not in SERVICES:
            self._refuse(actor, "unknown_service", f"unknown service {service!r}", str(service))
        if not self.service_enabled(service):
            self._refuse(actor, "service_disabled",
                         f"{service} is off (config.integrations.sync.enabled and .services.{service}.enabled)", service)

    def _append(self, kind: str, actor: str, body: dict, summary: dict) -> dict:
        ev = self.m.store.append(STREAM, kind, actor, body, self.m.clock.now_iso(), self.m.ids.new("sev"))
        self.m.gov.mirror(ev, actor, summary)
        return ev

    # ------------------------------------------------------------ connect
    @reaches("integrations.sync")
    def connect(self, service: str, actor: str) -> dict:
        self._user_only(actor, "connect", service)
        self._need_enabled(actor, service)
        prov = SERVICES[service]["provider"]
        if prov == "local":
            path = self.svc_cfg(service).get("profile_path")
            if not path or not Path(path).expanduser().is_dir():
                self._refuse(actor, "profile_path_missing", "set services.<svc>.profile_path to the browser profile directory", service)
            acct = f"local:{Path(path).expanduser().name}"
            self._append("CONNECT", actor, {"service": service, "provider": "local", "account_id": acct},
                         {"service": service, "connected": True})
            return {"service": service, "mode": "local", "connected": True, "account_id": acct}
        client = self.clients.get(prov)
        if self.clients.missing(prov):
            self._refuse(actor, "oauth_client_not_configured",
                         f"data/sync_clients.json {prov} is missing: {', '.join(self.clients.missing(prov))} "
                         "(docs/INTEGRATIONS.md §5)", service)
        state = secrets.token_urlsafe(24)
        if prov == "google":
            scopes = sorted({s for sv in self.provider_services("google") for s in oauth.SCOPES[sv]}) + oauth.GOOGLE_IDENTITY
            verifier, challenge = oauth.pkce_pair()
            lst = oauth.LoopbackListener(0, float(self.config.get("connect_timeout_s", 300)))
            redirect = f"http://127.0.0.1:{lst.port}/"
            self._replace_pending(prov, {"kind": "loopback", "state": state, "verifier": verifier, "listener": lst,
                                         "redirect_uri": redirect, "scopes": scopes, "service": service})
            return {"service": service, "provider": prov, "mode": "loopback", "scopes": scopes,
                    "auth_url": oauth.google_auth_url(client["client_id"], redirect, scopes, state, challenge)}
        # github device flow
        j, _, _ = self.http.json("github", "POST", oauth.GITHUB_DEVICE,
                                 form={"client_id": client["client_id"], "scope": " ".join(oauth.SCOPES["github"])})
        self._replace_pending(prov, {"kind": "device", "device_code": j["device_code"], "interval": int(j.get("interval", 5)),
                                     "service": service, "scopes": oauth.SCOPES["github"]})
        return {"service": service, "provider": prov, "mode": "device", "user_code": j["user_code"],
                "verification_uri": j["verification_uri"], "interval": int(j.get("interval", 5)),
                "expires_in": j.get("expires_in"), "scopes": oauth.SCOPES["github"]}

    def _replace_pending(self, prov, p):
        old = self.pending.pop(prov, None)
        if old and old.get("listener"):
            old["listener"].close()
        self.pending[prov] = p

    @reaches("integrations.sync")
    def connect_poll(self, service: str, actor: str) -> dict:
        """Finish a pending connect (called by the app while the user authorises in the browser)."""
        self._user_only(actor, "connect", service)
        self._need_enabled(actor, service)
        prov = SERVICES[service]["provider"]
        p = self.pending.get(prov)
        if p is None:
            return {"service": service, "pending": False, "connected": self.connection(service) is not None}
        client = self.clients.get(prov)
        if p["kind"] == "device":
            j, _, _ = self.http.json("github", "POST", oauth.GITHUB_TOKEN, form={
                "client_id": client["client_id"], "device_code": p["device_code"],
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code"})
            if j.get("error") in ("authorization_pending", "slow_down"):
                return {"service": service, "pending": True, "interval": p["interval"] + (5 if j["error"] == "slow_down" else 0)}
            if j.get("error") or not j.get("access_token"):
                self.pending.pop(prov, None)
                self._refuse(actor, "oauth_denied", str(j.get("error") or "no token"), service)
            granted = [s for s in re.split(r"[ ,]+", j.get("scope", "")) if s]
            tok = {"access_token": j["access_token"], "token_type": j.get("token_type", "bearer"), "scopes": granted}
            user, _, _ = self.http.json("github", "GET", "https://api.github.com/user", token=tok["access_token"],
                                        headers={"Accept": "application/vnd.github+json"})
            tok["account_id"] = f"github:{user.get('login')}:{user.get('id')}"
            return self._store_token(prov, service, actor, tok)
        res = p["listener"].result
        if not res:
            return {"service": service, "pending": True}
        self.pending.pop(prov, None)
        p["listener"].close()
        if res.get("error") or res.get("state") != p["state"] or not res.get("code"):
            self._refuse(actor, "oauth_denied", "authorisation denied or state mismatch", service)
        if prov == "google":
            form = {"code": res["code"], "client_id": client["client_id"], "redirect_uri": p["redirect_uri"],
                    "grant_type": "authorization_code", "code_verifier": p["verifier"]}
            if client.get("client_secret"):
                form["client_secret"] = client["client_secret"]
            j, _, _ = self.http.json("google", "POST", oauth.GOOGLE_TOKEN, form=form)
            claims = oauth.jwt_claims(j.get("id_token", ""))
            tok = {"access_token": j["access_token"], "refresh_token": j.get("refresh_token"),
                   "expires_at": self._in(j.get("expires_in", 3600)), "scopes": j.get("scope", "").split(),
                   "token_type": j.get("token_type", "Bearer"),
                   "account_id": f"google:{claims.get('email') or claims.get('sub') or 'unknown'}"}
            return self._store_token(prov, service, actor, tok)
        raise SyncRefused("unknown_provider", prov)  # pragma: no cover - only google uses the loopback flow

    def _in(self, seconds) -> str:
        import datetime as _dt
        return (self.m.clock.now() + _dt.timedelta(seconds=int(seconds))).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _store_token(self, prov, service, actor, tok) -> dict:
        if not oauth.is_read_only(tok.get("scopes") or []):
            self._refuse(actor, "scope_not_read_only", f"provider granted scopes outside the read-only set: {tok['scopes']}", service)
        tok.update(provider=prov, obtained_at=self.m.clock.now_iso())
        self.tokens.put(prov, tok)
        pub = self.tokens.public(prov)
        self._append("CONNECT", actor, {"service": service, "provider": prov, "account_id": pub["account_id"],
                                        "scopes": pub.get("scopes"), "services": self.provider_services(prov)},
                     {"service": service, "connected": True})
        return {"service": service, "pending": False, "connected": True, "account_id": pub["account_id"],
                "scopes": pub.get("scopes")}

    # ------------------------------------------------------------ disconnect
    @reaches("integrations.sync", plane="revocation")
    def disconnect(self, service: str, actor: str, remote_revoke: bool = False) -> dict:
        """User-only. Never blocked by a suspension (it only removes capability, D-77)."""
        self._user_only(actor, "disconnect", service)
        if service not in SERVICES:
            raise KeyError(service)
        prov = SERVICES[service]["provider"]
        remote = None
        if prov == "local":
            removed = self.connection(service) is not None
        else:
            tok = self.tokens.get(prov)
            if tok and remote_revoke:
                remote = self._remote_revoke(prov, tok)
            removed = self.tokens.delete(prov)
            old = self.pending.pop(prov, None)
            if old and old.get("listener"):
                old["listener"].close()
        affected = [service] if prov == "local" else [s for s, d in SERVICES.items() if d["provider"] == prov]
        self._append("DISCONNECT", actor, {"service": service, "provider": prov, "token_deleted": bool(removed),
                                           "services": affected, "remote_revoke": remote},
                     {"service": service, "connected": False})
        return {"service": service, "provider": prov, "disconnected": True, "token_deleted": bool(removed),
                "services": affected, "remote_revoke": remote}

    def _remote_revoke(self, prov, tok) -> str:
        try:
            if prov == "google":
                self.http.request("google", "POST", oauth.GOOGLE_REVOKE, form={"token": tok.get("refresh_token") or tok["access_token"]})
                return "revoked"
            return "manual: revoke the app at https://github.com/settings/applications"
        except (SyncHttpError, HostNotAllowed, OSError) as e:
            return f"failed: {type(e).__name__}"

    # ------------------------------------------------------------ tokens
    def _token(self, prov: str) -> str:
        tok = self.tokens.get(prov)
        if not tok:
            raise SyncRefused("not_connected", f"{prov} is not connected")
        if prov == "google" and tok.get("expires_at") and tok["expires_at"] <= self._in(60) and tok.get("refresh_token"):
            client = self.clients.get("google")
            form = {"client_id": client.get("client_id"), "refresh_token": tok["refresh_token"], "grant_type": "refresh_token"}
            if client.get("client_secret"):
                form["client_secret"] = client["client_secret"]
            j, _, _ = self.http.json("google", "POST", oauth.GOOGLE_TOKEN, form=form)
            tok.update(access_token=j["access_token"], expires_at=self._in(j.get("expires_in", 3600)))
            self.tokens.put("google", tok)
        return tok["access_token"]

    # ------------------------------------------------------------ sync
    def cursor(self, service: str):
        for e in reversed(self.events(service, kinds=["RUN"])):
            if not e["body"].get("error"):
                return e["body"].get("cursor_after")
        return None

    def index(self, service: str) -> dict[str, tuple]:
        idx = {}
        for it in self.m.corpus.items().values():
            p = it.get("provenance") or {}
            if p.get("sync") and p.get("service") == service:
                idx[p["remote_id"]] = (p.get("version"), it["corpus_id"])
        return idx

    @reaches("integrations.sync", "corpus.ingest", "permissions.closure")
    def sync(self, service: str, actor: str) -> dict:
        if actor not in SYNC_ACTORS:
            self.m.gov.record("PROHIBITED_ATTEMPT", actor, reason="sync_run_requires_user", service=service)
            raise NotAuthorized("only the user (or the user's local schedule) can run account sync")
        self._need_enabled(actor, service)
        d = SERVICES[service]
        conn = self.connection(service)
        if conn is None:
            self._refuse(actor, "not_connected", f"{service} is not connected", service)
        scope = self.svc_cfg(service).get("scope") or d["scope"]
        source = self.source(service)
        grants = self.m.perms.covering("ingest", [{"scope": scope, "sensitivity": "high"}], source=source)
        if not grants:
            self.m.gov.record("PROHIBITED_ATTEMPT", actor, reason="ingest_without_grant", source=source, scope=scope,
                              via="SyncManager.sync")
            raise PermissionDenied(f"no ingest grant covers source={source} scope={scope} sensitivity=high")
        run_id = self.m.ids.new("sync")
        before = self.cursor(service)
        state = {"cursor": before}
        max_items = int(self.config.get("max_items_per_run", 2000))
        max_chars = int(self.config.get("max_item_chars", 200000))
        idx = self.index(service)
        known_deleted = {e["body"]["remote_id"] for e in self.events(service, kinds=["REMOTE_DELETION"])}
        counts = {"ingested": 0, "updated": 0, "unchanged": 0, "remote_deletions": 0, "third_party": 0}
        error, truncated = None, False
        try:
            for item in getattr(self, "_fetch_" + service)(state, max_chars):
                if counts["ingested"] + counts["updated"] >= max_items:
                    truncated = True
                    break
                rid = str(item["remote_id"])
                if item.get("deleted"):
                    if rid in idx and rid not in known_deleted:
                        known_deleted.add(rid)
                        counts["remote_deletions"] += 1
                        self._append("REMOTE_DELETION", actor, {"service": service, "remote_id": rid, "run_id": run_id,
                                                                "corpus_id": idx[rid][1], "action": "none (no erasure; the user may withdraw)"},
                                     {"service": service, "remote_id": rid, "corpus_id": idx[rid][1]})
                    continue
                version = str(item.get("version"))
                prev = idx.get(rid)
                if prev and prev[0] == version:
                    counts["unchanged"] += 1
                    continue
                prov = {"sync": "medb.integrations.livesync/1", "service": service, "provider": d["provider"],
                        "account_id": conn.get("account_id"), "endpoint": item["endpoint"], "remote_id": rid,
                        "version": version, "run_id": run_id, "response_sha256": item["response_sha256"],
                        "supersedes_corpus_id": prev[1] if prev else None,
                        "third_party_content": bool(item.get("third_party"))}
                if item.get("details"):
                    prov["details"] = item["details"]
                r = self.m.corpus.ingest(item["content"], source=source, scope=scope, actor=actor, sensitivity="high",
                                         media_type=item.get("media_type", "text/plain"), provenance=prov)
                idx[rid] = (version, r["corpus_id"])
                counts["updated" if prev else "ingested"] += 1
                counts["third_party"] += bool(item.get("third_party"))
        except (SyncHttpError, HostNotAllowed, SyncRefused, OSError, sqlite3.Error, ValueError, KeyError) as e:
            error = f"{type(e).__name__}: {e}"[:300]
        after = before if (error or truncated) else state["cursor"]
        body = {"service": service, "run_id": run_id, "account_id": conn.get("account_id"), "source": source,
                "scope": scope, "grant_id": grants[0]["grant_id"], **counts, "truncated": truncated, "error": error,
                "cursor_before": before, "cursor_after": after}
        self._append("RUN", actor, body, {"service": service, "run_id": run_id, **counts, "error": bool(error)})
        return {k: v for k, v in body.items() if k not in ("cursor_before", "cursor_after")} | {"ok": error is None}

    # ------------------------------------------------------------ Google
    def _g(self, method, url, **kw):
        return self.http.json("google", method, url, token=self._token("google"), **kw)

    def _fetch_google_gmail(self, state, n):
        base = "https://gmail.googleapis.com/gmail/v1/users/me"
        prof, _, _ = self._g("GET", base + "/profile")
        ids, deleted = [], []
        cur = state["cursor"] or {}
        full = not cur.get("history_id")
        if not full:
            page = None
            try:
                while True:
                    j, _, _ = self._g("GET", base + "/history?historyTypes=messageAdded&historyTypes=messageDeleted",
                                      params={"startHistoryId": cur["history_id"], "pageToken": page, "maxResults": 500})
                    for h in j.get("history", []):
                        ids += [x["message"]["id"] for x in h.get("messagesAdded", [])]
                        deleted += [x["message"]["id"] for x in h.get("messagesDeleted", [])]
                    page = j.get("nextPageToken")
                    if not page:
                        break
            except SyncHttpError as e:
                if e.status != 404:  # 404: history id too old -> full resync (dedupe keeps it idempotent)
                    raise
                full, ids, deleted = True, [], []
        if full:
            page, q = None, self.svc_cfg("google_gmail").get("query", "newer_than:365d")
            while True:
                j, _, _ = self._g("GET", base + "/messages", params={"q": q, "pageToken": page, "maxResults": 100})
                ids += [x["id"] for x in j.get("messages", [])]
                page = j.get("nextPageToken")
                if not page or len(ids) >= int(self.config.get("max_items_per_run", 2000)):
                    break
        for mid in deleted:
            yield {"remote_id": mid, "deleted": True}
        for mid in dict.fromkeys(ids):
            if mid in deleted:
                continue
            j, _, raw_body = self._g("GET", f"{base}/messages/{quote(mid)}", params={"format": "raw"})
            raw = base64.urlsafe_b64decode(j["raw"] + "=" * (-len(j["raw"]) % 4))
            it = mail_item(raw, n, mid)
            det = dict(it["extra"]["mail"], label_ids=j.get("labelIds"), internal_date=j.get("internalDate"),
                       message_id_header=it["ref"])
            yield {"remote_id": mid, "version": j.get("historyId"), "endpoint": f"gmail/v1/users/me/messages/{mid}",
                   "content": it["content"], "media_type": "message/rfc822", "response_sha256": _sha(raw_body),
                   "third_party": True, "details": {"mail": det}}
        state["cursor"] = {"history_id": prof.get("historyId")}

    def _fetch_google_calendar(self, state, n):
        url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
        cur = state["cursor"] or {}
        page, sync_token = None, cur.get("sync_token")
        while True:
            params = {"pageToken": page, "maxResults": 250}
            if sync_token:
                params["syncToken"] = sync_token
            try:
                j, _, _ = self._g("GET", url, params=params)
            except SyncHttpError as e:
                if e.status == 410 and sync_token:  # sync token expired: full resync
                    sync_token, page = None, None
                    continue
                raise
            for ev in j.get("items", []):
                if ev.get("status") == "cancelled":
                    yield {"remote_id": ev["id"], "deleted": True}
                    continue
                att = [a.get("email", "") for a in ev.get("attendees", [])]
                lines = [f"Event: {ev.get('summary', '')}",
                         f"Start: {(ev.get('start') or {}).get('dateTime') or (ev.get('start') or {}).get('date', '')}",
                         f"End: {(ev.get('end') or {}).get('dateTime') or (ev.get('end') or {}).get('date', '')}"]
                for k in ("location", "description"):
                    if ev.get(k):
                        lines.append(f"{k.title()}: {ev[k]}")
                if (ev.get("organizer") or {}).get("email"):
                    lines.append(f"Organizer: {ev['organizer']['email']}")
                if att:
                    lines.append("Attendees: " + ", ".join(att))
                yield {"remote_id": ev["id"], "version": ev.get("etag") or ev.get("updated"),
                       "endpoint": "calendar/v3/calendars/primary/events", "content": _clip("\n".join(lines), n),
                       "media_type": "text/calendar", "response_sha256": _sha(ev),
                       "third_party": bool(att) or bool((ev.get("organizer") or {}).get("email")),
                       "details": {"updated": ev.get("updated"), "html_link": ev.get("htmlLink")}}
            page = j.get("nextPageToken")
            if not page:
                state["cursor"] = {"sync_token": j.get("nextSyncToken")}
                break

    def _fetch_google_contacts(self, state, n):
        url = "https://people.googleapis.com/v1/people/me/connections"
        fields = "names,emailAddresses,phoneNumbers,organizations,birthdays,biographies,metadata"
        cur = state["cursor"] or {}
        page, sync_token = None, cur.get("sync_token")
        while True:
            params = {"personFields": fields, "pageSize": 200, "requestSyncToken": "true", "pageToken": page}
            if sync_token:
                params["syncToken"] = sync_token
            try:
                j, _, _ = self._g("GET", url, params=params)
            except SyncHttpError as e:
                if e.status in (400, 410) and sync_token:
                    sync_token, page = None, None
                    continue
                raise
            for p in j.get("connections", []):
                if (p.get("metadata") or {}).get("deleted"):
                    yield {"remote_id": p["resourceName"], "deleted": True}
                    continue
                lines = []
                for key, label, sub in (("names", "Name", "displayName"), ("emailAddresses", "Email", "value"),
                                        ("phoneNumbers", "Phone", "value"), ("organizations", "Org", "name"),
                                        ("biographies", "Note", "value")):
                    for x in p.get(key, []):
                        if x.get(sub):
                            lines.append(f"{label}: {x[sub]}")
                for b in p.get("birthdays", []):
                    dd = b.get("date") or {}
                    lines.append(f"Birthday: {dd.get('year', '????')}-{dd.get('month', '??')}-{dd.get('day', '??')}")
                yield {"remote_id": p["resourceName"], "version": p.get("etag"), "endpoint": "v1/people/me/connections",
                       "content": _clip("\n".join(lines), n), "media_type": "text/vcard", "response_sha256": _sha(p),
                       "third_party": True}
            page = j.get("nextPageToken")
            if not page:
                state["cursor"] = {"sync_token": j.get("nextSyncToken")}
                break

    # ------------------------------------------------------------ GitHub
    def _gh_pages(self, url, params=None, headers=None, limit=10):
        h = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        h.update(headers or {})
        for _ in range(limit):
            st, rh, data = self.http.request("github", "GET", url, params=params, token=self._token("github"),
                                             headers=h, ok=(200, 304))
            if st == 304:
                return
            yield json.loads(data or b"[]"), rh
            url, params = _next_link(rh.get("link")), None
            if not url:
                return

    def _fetch_github(self, state, n):
        cur = dict(state["cursor"] or {})
        user, _, _ = self.http.json("github", "GET", "https://api.github.com/user", token=self._token("github"),
                                    headers={"Accept": "application/vnd.github+json"})
        login = user.get("login")
        yield {"remote_id": f"user:{user.get('id')}", "version": user.get("updated_at"), "endpoint": "GET /user",
               "content": _clip(json.dumps({k: user.get(k) for k in ("login", "name", "bio", "company", "location",
                                            "blog", "public_repos", "followers", "following", "created_at")}, indent=1), n),
               "media_type": "application/json", "response_sha256": _sha(user)}
        for page, _ in self._gh_pages("https://api.github.com/user/repos", {"per_page": 100, "sort": "updated"}):
            for r in page:
                yield {"remote_id": f"repo:{r['id']}", "version": r.get("pushed_at") or r.get("updated_at"),
                       "endpoint": "GET /user/repos", "media_type": "application/json", "response_sha256": _sha(r),
                       "content": _clip(json.dumps({k: r.get(k) for k in ("full_name", "html_url", "description", "private",
                                                    "fork", "language", "stargazers_count", "created_at", "pushed_at")}, indent=1), n)}
        for page, _ in self._gh_pages("https://api.github.com/user/starred", {"per_page": 100},
                                      headers={"Accept": "application/vnd.github.star+json"}):
            for s in page:
                r = s.get("repo", s)
                yield {"remote_id": f"star:{r['id']}", "version": s.get("starred_at"), "endpoint": "GET /user/starred",
                       "media_type": "application/json", "response_sha256": _sha(s),
                       "content": f"Starred: {r.get('full_name')}\n{r.get('html_url')}\n{r.get('description') or ''}\nAt: {s.get('starred_at')}"}
        etag_hdr = {"If-None-Match": cur["events_etag"]} if cur.get("events_etag") else {}
        new_etag = cur.get("events_etag")
        for i, (page, rh) in enumerate(self._gh_pages(f"https://api.github.com/users/{quote(str(login))}/events",
                                                      {"per_page": 100}, headers=etag_hdr, limit=3)):
            if i == 0:
                new_etag = rh.get("etag", new_etag)
            for ev in page:
                yield {"remote_id": f"event:{ev['id']}", "version": ev["id"], "endpoint": f"GET /users/{login}/events",
                       "media_type": "application/json", "response_sha256": _sha(ev),
                       "content": f"GitHub event {ev.get('type')} on {(ev.get('repo') or {}).get('name')} at {ev.get('created_at')}"}
            etag_hdr = {}
        since = cur.get("issues_since")
        newest = since
        for page, _ in self._gh_pages("https://api.github.com/issues", {"filter": "all", "state": "all", "per_page": 100,
                                                                         "since": since}):
            for it in page:
                newest = max(newest or "", it.get("updated_at") or "")
                yield {"remote_id": f"issue:{it['id']}", "version": it.get("updated_at"), "endpoint": "GET /issues",
                       "media_type": "text/markdown", "response_sha256": _sha(it),
                       "third_party": (it.get("user") or {}).get("login") != login,
                       "content": _clip(f"{'PR' if it.get('pull_request') else 'Issue'}: {it.get('title')} ({it.get('state')})\n"
                                        f"{it.get('html_url')}\nBy: {(it.get('user') or {}).get('login')}\n\n{it.get('body') or ''}", n)}
        state["cursor"] = {"events_etag": new_etag, "issues_since": newest}

    # ------------------------------------------------------------ local browsers (live)
    def _copy_profile(self, service, names):
        prof = Path(self.svc_cfg(service).get("profile_path") or "").expanduser()
        tmp = Path(tempfile.mkdtemp(prefix="medb-sync-"))
        os.chmod(tmp, 0o700)
        found = {}
        for key, rels in names.items():
            for rel in rels:
                src = prof / rel
                if src.is_file():
                    dst = tmp / key
                    shutil.copy2(src, dst)
                    for suffix in ("-wal", "-shm"):
                        if Path(str(src) + suffix).exists():
                            shutil.copy2(str(src) + suffix, str(dst) + suffix)
                    found[key] = dst
                    break
        return tmp, found

    @staticmethod
    def _ro(path):
        return sqlite3.connect(f"file:{quote(str(path))}?mode=ro", uri=True)

    def _local_cursor(self, state):
        return dict(state["cursor"] or {})

    def _fetch_chrome_local(self, state, n):
        cur = self._local_cursor(state)
        tmp, f = self._copy_profile("chrome_local", {"history": ["History"], "bookmarks": ["Bookmarks"],
                                                     "cookies": ["Network/Cookies", "Cookies"]})
        try:
            hmax = int(cur.get("history_max", 0))
            if "history" in f:
                con = self._ro(f["history"])
                try:
                    for url, title, visits, last in con.execute(
                            "SELECT url, title, visit_count, last_visit_time FROM urls WHERE last_visit_time > ? "
                            "ORDER BY last_visit_time", (hmax,)):
                        hmax = max(hmax, int(last or 0))
                        yield {"remote_id": f"url:{url}"[:600], "version": str(last), "endpoint": "profile:History/urls",
                               "media_type": "text/plain", "response_sha256": _sha([url, title, visits, last]),
                               "content": f"Visited: {title or ''}\n{url}\nVisits: {visits}\nLast visit: {webkit_ts(last)}"}
                finally:
                    con.close()
            if "bookmarks" in f:
                doc = json.loads(f["bookmarks"].read_text(encoding="utf-8-sig"))

                def walk(node, folder):
                    if node.get("type") == "url":
                        yield node, folder
                    for c in node.get("children") or []:
                        yield from walk(c, folder + "/" + node.get("name", "") if node.get("type") == "folder" else folder)
                for root in (doc.get("roots") or {}).values():
                    if isinstance(root, dict):
                        for b, folder in walk(root, ""):
                            yield {"remote_id": f"bookmark:{b.get('guid') or b.get('id')}",
                                   "version": str(b.get("date_modified") or b.get("date_added")),
                                   "endpoint": "profile:Bookmarks", "media_type": "text/plain", "response_sha256": _sha(b),
                                   "content": f"Bookmark: {b.get('name') or ''}\n{b.get('url')}\nFolder: {folder or '/'}\nAdded: {webkit_ts(b.get('date_added'))}"}
            if "cookies" in f and self.svc_cfg("chrome_local").get("cookies", True):
                yield from self._cookie_items(f["cookies"], "chrome_cookies_meta")
            state["cursor"] = {"history_max": hmax}
        finally:
            shutil.rmtree(tmp, ignore_errors=True)  # the copy (incl. any cookie DB) is deleted after every run

    def _fetch_firefox_local(self, state, n):
        cur = self._local_cursor(state)
        tmp, f = self._copy_profile("firefox_local", {"places": ["places.sqlite"], "cookies": ["cookies.sqlite"]})
        try:
            hmax = int(cur.get("history_max", 0))
            if "places" in f:
                con = self._ro(f["places"])
                try:
                    for url, title, visits, last in con.execute(
                            "SELECT url, title, visit_count, last_visit_date FROM moz_places WHERE visit_count > 0 AND "
                            "last_visit_date > ? ORDER BY last_visit_date", (hmax,)):
                        hmax = max(hmax, int(last or 0))
                        yield {"remote_id": f"url:{url}"[:600], "version": str(last), "endpoint": "profile:places.sqlite/moz_places",
                               "media_type": "text/plain", "response_sha256": _sha([url, title, visits, last]),
                               "content": f"Visited: {title or ''}\n{url}\nVisits: {visits}\nLast visit: {unix_us_ts(last)}"}
                    cols = {r[1] for r in con.execute("PRAGMA table_info(moz_bookmarks)")}
                    mod_col = "b.lastModified" if "lastModified" in cols else "b.dateAdded"
                    for bid, url, title, added, mod in (con.execute(
                            f"SELECT b.id, p.url, b.title, b.dateAdded, {mod_col} FROM moz_bookmarks b "
                            "JOIN moz_places p ON p.id = b.fk WHERE b.type = 1 ORDER BY b.id") if cols else ()):
                        yield {"remote_id": f"bookmark:{bid}", "version": str(mod or added),
                               "endpoint": "profile:places.sqlite/moz_bookmarks", "media_type": "text/plain",
                               "response_sha256": _sha([bid, url, title, added, mod]),
                               "content": f"Bookmark: {title or ''}\n{url}\nAdded: {unix_us_ts(added)}"}
                finally:
                    con.close()
            if "cookies" in f and self.svc_cfg("firefox_local").get("cookies", True):
                yield from self._cookie_items(f["cookies"], "firefox_cookies_meta")
            state["cursor"] = {"history_max": hmax}
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def _cookie_items(self, path, fmt):
        """Cookie metadata only: the SQL (shared with the importer, D-72) never selects names or values."""
        sql, conv = COOKIE_SQL[fmt]
        con = self._ro(path)
        try:
            for host, count, first, last in con.execute(sql):
                dom = (host or "").lstrip(".")
                yield {"remote_id": f"cookies:{dom}", "version": f"{count}|{last}", "endpoint": f"profile:{fmt}",
                       "media_type": "text/plain", "response_sha256": _sha([dom, count, first, last]),
                       "content": f"Cookie metadata for {dom}: {count} cookie(s); first set {conv(first)}; last accessed {conv(last)}. "
                                  "Cookie names and values were not read.",
                       "details": {"cookie_meta": {"domain": dom, "count": count, "first_seen": conv(first),
                                                   "last_seen": conv(last), "values_imported": False}}}
        finally:
            con.close()

    # ------------------------------------------------------------ status
    def status(self) -> dict:
        out = {}
        items: dict[str, int] = {}
        for it in self.m.corpus.items().values():
            p = it.get("provenance") or {}
            if p.get("sync"):
                items[p["service"]] = items.get(p["service"], 0) + 1
        for s, d in SERVICES.items():
            runs = self.events(s, kinds=["RUN"])
            last = runs[-1]["body"] if runs else None
            conn = self.connection(s)
            out[s] = {"service": s, "label": d["label"], "provider": d["provider"], "enabled": self.service_enabled(s),
                      "connected": conn is not None, "account_id": (conn or {}).get("account_id"),
                      "scopes": (conn or {}).get("scopes"),
                      "client_configured": True if d["provider"] == "local" else not self.clients.missing(d["provider"]),
                      "client_missing": [] if d["provider"] == "local" else self.clients.missing(d["provider"]),
                      "connectable": self.connectable(s)[0], "not_connectable_because": self.connectable(s)[1],
                      "source": self.source(s), "scope": self.svc_cfg(s).get("scope") or d["scope"],
                      "hosts": list(ALLOWED_HOSTS.get(d["provider"], ())), "pending_connect": d["provider"] in self.pending,
                      "items": items.get(s, 0),
                      "last_sync": None if not last else {"at": runs[-1]["ts"], "run_id": last["run_id"], "ingested": last["ingested"],
                                                          "updated": last["updated"], "unchanged": last["unchanged"],
                                                          "remote_deletions": last["remote_deletions"], "error": last["error"],
                                                          "actor": runs[-1]["actor"]}}
        return out


class SyncScheduler:
    """Optional interval sync inside the API process (off by default). Runs on the server's main thread
    between requests (``tick``), as actor ``system`` on the user's standing configuration."""

    def __init__(self, manager: SyncManager):
        self.sm = manager
        self.last: str | None = None

    def due(self) -> bool:
        sch = self.sm.config.get("schedule") or {}
        if not (self.sm.enabled and sch.get("enabled")):
            return False
        if self.last is None:
            return True
        import datetime as _dt
        nxt = _dt.datetime.fromisoformat(self.last.replace("Z", "+00:00")) + _dt.timedelta(minutes=float(sch.get("interval_minutes", 60)))
        return self.sm.m.clock.now() >= nxt

    def tick(self) -> list[dict]:
        if not self.due():
            return []
        self.last = self.sm.m.clock.now_iso()
        out = []
        for s in SERVICES:
            if self.sm.service_enabled(s) and self.sm.connection(s) is not None:
                try:
                    out.append(self.sm.sync(s, actor="system"))
                except Exception as e:  # refusals (grant, suspension) are logged by the primitives
                    out.append({"service": s, "ok": False, "error": type(e).__name__})
        return out

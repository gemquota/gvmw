"""Outbound HTTPS for live account sync -- the only module allowed to reach the
user's account providers (Gem's F-26 ruling, DECISIONS D-76).

Reconciling local-first (Principle 8, D-01) with live sync:

* this is a separate, declared **outbound class** (``live_sync``) in the
  generated network self-description (``netscan``, D-68), next to RFC 3161
  anchoring (D-62); nothing else in MedB opens outbound connections;
* every request is checked against a **fixed per-provider host allowlist**
  (``ALLOWED_HOSTS`` below; not configurable, so config cannot widen it) and
  must be **HTTPS** -- anything else is refused *before* a connection is
  attempted (``HostNotAllowed``);
* redirects are never followed (a 3xx is returned to the caller as an error),
  so an allowed host cannot bounce a request elsewhere;
* only providers whose services the user enabled *and* connected are
  contacted; sync runs locally and items land only in the local corpus;
* request/response bodies are not logged; bearer tokens are added here from
  the local token store and never written anywhere else.
"""
from __future__ import annotations

import json
from urllib.parse import urlencode, urlparse

ALLOWED_HOSTS = {
    "google": ("accounts.google.com", "oauth2.googleapis.com", "gmail.googleapis.com", "www.googleapis.com",
               "people.googleapis.com"),
    "github": ("github.com", "api.github.com"),
}
NETWORK_DECLARATION = {
    "direction": "outbound",
    "class": "live_sync",
    "purpose": "user-authorised read-only sync of the user's own accounts into the local corpus (F-26, D-76); "
               "per-service opt-in, off by default",
    "protocol": "HTTPS only (stdlib http.client, default TLS verification), no redirects followed",
    "allowed_hosts": {k: list(v) for k, v in ALLOWED_HOSTS.items()},
    "sends_content": False,
    "sends": "OAuth requests and read-only API GETs (the user's own access token); never MedB corpus or claim content",
    "default_enabled": False,
    "outbound": True,
}


class HostNotAllowed(Exception):
    pass


class SyncHttpError(Exception):
    def __init__(self, status: int, detail: str = ""):
        super().__init__(f"HTTP {status}: {detail}"[:300])
        self.status = status


def check_url(provider: str, url: str) -> None:
    """Refuse anything but https://<allowlisted host>[:443]/... for this provider."""
    u = urlparse(url)
    if u.scheme != "https":
        raise HostNotAllowed(f"live sync is HTTPS only (got {u.scheme or 'no scheme'})")
    if u.username or u.password or (u.port not in (None, 443)):
        raise HostNotAllowed("credentials or non-standard ports in sync URLs are refused")
    if (u.hostname or "") not in ALLOWED_HOSTS.get(provider, ()):
        raise HostNotAllowed(f"host {u.hostname!r} is not on the {provider} allowlist")


def https_transport(method: str, url: str, headers: dict, body: bytes | None, timeout: float):
    """Default transport: one HTTPS request, certificate-verified, no redirects."""
    import http.client
    import ssl
    u = urlparse(url)
    conn = http.client.HTTPSConnection(u.hostname, 443, timeout=timeout, context=ssl.create_default_context())
    try:
        path = u.path or "/"
        if u.query:
            path += "?" + u.query
        conn.request(method, path, body=body, headers=headers)
        r = conn.getresponse()
        return r.status, {k.lower(): v for k, v in r.getheaders()}, r.read()
    finally:
        conn.close()


class SyncHttp:
    def __init__(self, transport=None, timeout: float = 30.0):
        self.transport = transport or https_transport
        self.timeout = timeout

    def request(self, provider: str, method: str, url: str, params: dict | None = None, form: dict | None = None,
                token: str | None = None, headers: dict | None = None, ok=(200,)):
        """Returns (status, headers, body_bytes). The allowlist check happens before the transport is called."""
        if params:
            url += ("&" if "?" in url else "?") + urlencode({k: v for k, v in params.items() if v is not None})
        check_url(provider, url)
        h = {"Accept": "application/json", "User-Agent": "MedB-live-sync/0.1"}
        h.update(headers or {})
        body = None
        if form is not None:
            body = urlencode(form).encode()
            h["Content-Type"] = "application/x-www-form-urlencoded"
        if token:
            h["Authorization"] = f"Bearer {token}"
        status, rh, data = self.transport(method, url, h, body, self.timeout)
        if status not in ok:
            detail = ""
            try:
                j = json.loads(data or b"{}")
                e = j.get("error")
                detail = (e.get("message") if isinstance(e, dict) else e) or j.get("message") or ""
            except ValueError:
                pass
            raise SyncHttpError(status, str(detail))
        return status, rh, data

    def json(self, provider, method, url, **kw):
        status, rh, data = self.request(provider, method, url, **kw)
        return (json.loads(data) if data else {}), rh, data

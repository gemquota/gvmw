"""User-authorised OAuth flows for live sync (D-76). Read-only scopes only.

* Google: installed-app **loopback redirect + PKCE (S256)**. MedB opens a
  one-shot listener on ``127.0.0.1:<ephemeral port>``; the user's own browser
  visits ``accounts.google.com`` and is redirected back with a code; MedB
  exchanges it at ``oauth2.googleapis.com``.
* GitHub: **device flow** (``github.com/login/device/code``): the user enters a
  short code at github.com; MedB polls for the token. No redirect, no secret.

The loopback listener only stores ``(state, code)``; the token exchange and all
logging happen on the API's main thread when the app polls, so the database is
never written from another thread.
"""
from __future__ import annotations

import base64
import hashlib
import json
import secrets
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

NETWORK_DECLARATION = {
    "direction": "loopback",
    "purpose": "one-shot OAuth redirect listener for Google connect (D-76); started only when the user "
               "clicks Connect, closed after one callback or a timeout",
    "protocol": "HTTP (stdlib http.server) on 127.0.0.1, receives the authorisation code from the user's browser",
    "allowed_hosts": ["127.0.0.1"],
    "default_enabled": False,
    "sends_content": False,
    "outbound": False,
}

GOOGLE_AUTH = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN = "https://oauth2.googleapis.com/token"
GOOGLE_REVOKE = "https://oauth2.googleapis.com/revoke"
GITHUB_DEVICE = "https://github.com/login/device/code"
GITHUB_TOKEN = "https://github.com/login/oauth/access_token"

# Read-only scopes (Gem's constraint). openid/email only identify the account (from the id_token).
SCOPES = {
    "google_gmail": ["https://www.googleapis.com/auth/gmail.readonly"],
    "google_calendar": ["https://www.googleapis.com/auth/calendar.readonly"],
    "google_contacts": ["https://www.googleapis.com/auth/contacts.readonly"],
    "github": ["read:user"],          # public repos/stars/events/issues; add "repo" only if you want private repos (F-28)
}
GOOGLE_IDENTITY = ["openid", "email"]
# The only scopes MedB will request or accept back from a provider (anything else: refused, token deleted).
ALLOWED_SCOPES = frozenset(sum(SCOPES.values(), []) + GOOGLE_IDENTITY + [
    "https://www.googleapis.com/auth/userinfo.email"])  # Google reports 'email' under this name


def is_read_only(scopes) -> bool:
    return all(s in ALLOWED_SCOPES for s in scopes)


def pkce_pair() -> tuple[str, str]:
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(48)).rstrip(b"=").decode()
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    return verifier, challenge


def jwt_claims(id_token: str) -> dict:
    """Payload of an id_token received directly from the token endpoint over TLS (OIDC 3.1.3.7: TLS
    server validation may stand in for signature checking in this case)."""
    try:
        part = id_token.split(".")[1]
        return json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))
    except Exception:
        return {}


class LoopbackListener:
    """One-shot redirect receiver on 127.0.0.1 (thread); keeps only state->code/error."""

    def __init__(self, port: int = 0, timeout_s: float = 300):
        self.result: dict = {}
        outer = self

        class H(BaseHTTPRequestHandler):
            def do_GET(self):
                q = parse_qs(urlparse(self.path).query)
                outer.result = {"code": (q.get("code") or [None])[0], "state": (q.get("state") or [None])[0],
                                "error": (q.get("error") or [None])[0]}
                msg = b"MedB: authorisation received. You can close this tab and return to MedB."
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(msg)))
                self.end_headers()
                self.wfile.write(msg)
                threading.Thread(target=outer.close, daemon=True).start()

            def log_message(self, *a):  # never log the query string (it carries the code)
                pass

        self.srv = HTTPServer(("127.0.0.1", port), H)
        self.srv.timeout = 1
        self.port = self.srv.server_port
        self._t = threading.Thread(target=self.srv.serve_forever, daemon=True)
        self._t.start()
        self._timer = threading.Timer(timeout_s, self.close)
        self._timer.daemon = True
        self._timer.start()

    def close(self):
        try:
            self._timer.cancel()
            self.srv.shutdown()
            self.srv.server_close()
        except Exception:
            pass


def google_auth_url(client_id: str, redirect_uri: str, scopes: list[str], state: str, challenge: str) -> str:
    return GOOGLE_AUTH + "?" + urlencode({
        "client_id": client_id, "redirect_uri": redirect_uri, "response_type": "code",
        "scope": " ".join(scopes), "state": state, "code_challenge": challenge, "code_challenge_method": "S256",
        "access_type": "offline", "prompt": "consent", "include_granted_scopes": "false"})

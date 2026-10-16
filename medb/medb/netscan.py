"""Generated network profile for ``self_description`` (D-19 style; DECISIONS D-68).

Nothing here is hand-written prose about what MedB does on the network. The
profile is derived from:

* an AST scan of every ``.py`` file in the ``medb`` package for imports of
  network-capable stdlib/third-party modules (top-level *and* function-local
  imports, e.g. the lazy ``import urllib.request`` in ``anchoring``);
* each such module's machine-readable ``NETWORK_DECLARATION`` constant;
* the running configuration (anchoring enabled / method / TSA URL) and the
  API's loopback bind list.

A module with network imports but no declaration is reported under
``undeclared`` (tests require that list to be empty), so the description
cannot silently go stale when network code is added.
"""
from __future__ import annotations

import ast
import hashlib
import importlib
from pathlib import Path

from .util import digest

PKG_DIR = Path(__file__).resolve().parent
# module prefixes that can open sockets (stdlib + common third-party clients)
NETWORK_MODULES = ("socket", "ssl", "http.client", "http.server", "socketserver", "urllib.request",
                   "urllib3", "requests", "httpx", "aiohttp", "asyncio", "smtplib", "ftplib", "poplib",
                   "imaplib", "telnetlib", "xmlrpc", "websockets", "websocket", "paramiko")


def _is_net(name: str) -> bool:
    return any(name == p or name.startswith(p + ".") for p in NETWORK_MODULES)


def network_imports(source: str) -> list[str]:
    """Network-capable modules imported anywhere in ``source`` (sorted, unique)."""
    found = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found |= {a.name for a in node.names if _is_net(a.name)}
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            if _is_net(node.module):
                found.add(node.module)
            else:  # e.g. ``from urllib import request``
                found |= {f"{node.module}.{a.name}" for a in node.names if _is_net(f"{node.module}.{a.name}")}
    return sorted(found)


def scan_package(pkg_dir: Path = PKG_DIR) -> dict[str, list[str]]:
    """{module: [network imports]} for every module of the package that has any."""
    out = {}
    for f in sorted(pkg_dir.rglob("*.py")):
        if "__pycache__" in f.parts:
            continue
        imps = network_imports(f.read_text(encoding="utf-8"))
        if imps:
            rel = f.relative_to(pkg_dir.parent).with_suffix("").as_posix().replace("/", ".")
            out[rel] = imps
    return out


def network_profile(m) -> dict:
    found = scan_package()
    modules, undeclared = [], []
    for mod, imps in found.items():
        decl = getattr(importlib.import_module(mod), "NETWORK_DECLARATION", None)
        src = PKG_DIR.parent / (mod.replace(".", "/") + ".py")
        entry = {"module": mod, "imports": imps, "source_sha256": hashlib.sha256(src.read_bytes()).hexdigest()}
        if decl is None:
            undeclared.append(entry)
            continue
        entry.update(decl)
        if mod == "medb.integrations.outbox":
            entry.update({"enabled": m.outbox.webhook()["enabled"], "url_is_loopback": m.outbox.webhook()["url_is_loopback"]})
        if mod == "medb.integrations.mcp_server":
            entry.update({"enabled": m.mcp_activity.enabled})
        if mod == "medb.integrations.sync_http":  # live sync (D-76): enabled services and the hosts they may reach
            sm = m.sync
            on = [s for s in sorted(sm.config.get("services") or {}) if sm.service_enabled(s)]
            entry.update({"enabled": bool(on), "services_enabled": on, "hosts_in_use": sm.hosts_in_use()})
        if mod == "medb.integrations.oauth":
            entry.update({"enabled": bool(m.sync.pending)})
        if mod == "medb.anchoring":  # live state from the running configuration
            a = m.anchoring
            from .system import DEFAULT_CONFIG, load_config
            entry.update({"enabled": a.enabled, "method": a.config.get("method"),
                          "tsa_url": a.config.get("tsa_url"),
                          "default_enabled": bool(load_config(DEFAULT_CONFIG).get("anchoring", {}).get("enabled")),
                          "config_digest": digest(a.config)})
        modules.append(entry)
    outbound = [e for e in modules if e.get("direction") == "outbound"]
    return {
        "derived_from": "AST import scan of every module in the medb package + each module's "
                        "NETWORK_DECLARATION + running config",
        "network_modules_checked": list(NETWORK_MODULES),
        "modules_with_network_code": modules,
        "outbound_modules": [e["module"] for e in outbound],
        "outbound_enabled": any(e.get("enabled") for e in outbound),
        "inbound_modules": [e["module"] for e in modules if e.get("direction") == "inbound"],
        # loopback-only (127.0.0.1 / ::1): MCP bridge -> local API, outbox webhook, OAuth redirect listener (D-73/D-74/D-77)
        "loopback_modules": [e["module"] for e in modules if e.get("direction") == "loopback"],
        "undeclared": undeclared,
    }

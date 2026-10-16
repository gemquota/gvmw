import urllib3
import configparser
import random
import os
import sqlite3
import threading
import aiosqlite
import csv
import json
import datetime
import requests
import sys
import http.client

# ==============================================================================
# SECTION: CONFIG (Original: config.py)
# Description: Global settings, credential parsing, and proxy loading.
# ==============================================================================

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize Config Parser
config_reader = configparser.ConfigParser()
config_reader.read('in/config/config.ini')

# Global Constants
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
TIMEOUT = 15
MIN_DELAY = config_reader.getfloat('SETTINGS', 'min_delay', fallback=1.0)
MAX_DELAY = config_reader.getfloat('SETTINGS', 'max_delay', fallback=3.0)
IP_KEY = config_reader.get('SETTINGS', 'abuseipdb_key', fallback=None)
UI_USER = config_reader.get('SETTINGS', 'ui_user', fallback='admin')
UI_PASS = config_reader.get('SETTINGS', 'ui_pass', fallback='password')
DEFAULT_MAX_WITHDRAW = config_reader.getfloat('SETTINGS', 'default_max_withdraw', fallback=3776.0)

def get_proxies():
    """Reads proxy list from proxies.txt."""
    proxy_path = 'in/config/proxies.txt'
    if os.path.exists(proxy_path):
        with open(proxy_path, 'r', encoding='utf-8') as proxy_file:
            return [line.strip() for line in proxy_file if line.strip()]
    return []

def parse_targets_and_credentials(force_shuffle=False):
    """Parses URLs from urls.txt and Credentials from config.ini."""
    all_urls = []
    if os.path.exists('in/config/urls.txt'):
        with open('in/config/urls.txt', 'r', encoding='utf-8') as url_file:
            all_urls = [line.strip() for line in url_file if line.strip()]
    try:
        non_active_urls = [row[0] for row in query("SELECT url FROM targets WHERE status IN ('purgatory', 'pruned')")]
        active_urls = [url for url in all_urls if url not in non_active_urls]
    except: active_urls = all_urls
    random.shuffle(active_urls)
    credentials = []
    for section in config_reader.sections():
        if section.startswith('U') and section[1:].isdigit():
            user = config_reader.get(section, 'username', fallback=config_reader.get(section, 'u', fallback=None))
            pwd = config_reader.get(section, 'password', fallback=config_reader.get(section, 'p', fallback=None))
            if user and pwd: credentials.append((user, pwd))
    return active_urls, credentials

# Single-word aliases
agent, timeout, proxies, parse, reader = USER_AGENT, TIMEOUT, get_proxies, parse_targets_and_credentials, config_reader

# ==============================================================================
# SECTION: DB (Original: db.py)
# Description: Thread-local SQLite management and query abstraction.
# ==============================================================================

local_storage = threading.local()

def get_conn():
    if not hasattr(local_storage, "connection"):
        local_storage.connection = sqlite3.connect('db/base.db')
        local_storage.connection.execute("PRAGMA journal_mode=WAL;")
    return local_storage.connection

async def async_query(query_str, args=()):
    """Async wrapper for read-only queries."""
    async with aiosqlite.connect('db/base.db') as db:
        async with db.execute(query_str, args) as cursor: return await cursor.fetchall()

def setup():
    """Initializes the database schema."""
    conn = get_conn(); conn.execute("PRAGMA journal_mode=WAL;")
    conn.executescript("""
  CREATE TABLE IF NOT EXISTS targets(url TEXT PRIMARY KEY, merchant_name TEXT, priority INTEGER, group_id INTEGER, active_flag INT DEFAULT 1, last_scraped_at DATETIME, status TEXT DEFAULT 'active', failure_count INTEGER DEFAULT 0, retest_count INTEGER DEFAULT 0, username TEXT, alts_tried TEXT DEFAULT '[]', manual_verified_at DATETIME, verification_status TEXT DEFAULT 'pending');
  CREATE TABLE IF NOT EXISTS proxy_health (proxy TEXT PRIMARY KEY, burn_count INTEGER DEFAULT 0, last_burn_ts DATETIME, status TEXT DEFAULT 'active');
  CREATE TABLE IF NOT EXISTS ip_cache (ip TEXT PRIMARY KEY, score INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);
  CREATE TABLE IF NOT EXISTS raw_data (hash TEXT PRIMARY KEY, json_data TEXT);
  CREATE TABLE IF NOT EXISTS bonuses(unique_id TEXT PRIMARY KEY, external_id TEXT, url TEXT, amount REAL, perceived_value REAL, raw_json_hash TEXT, expiration_date DATETIME, fingerprint TEXT, mirrors TEXT, first_seen_at DATETIME DEFAULT CURRENT_TIMESTAMP, last_seen_at DATETIME, verified BOOLEAN DEFAULT 0, manual_note TEXT, merchant_name TEXT, bonus_name TEXT, conf_startDate TEXT, conf_max_round TEXT, conf_claimTime TEXT, conf_mobileAppOnly TEXT, conf_registerBeforeDate TEXT, conf_mustJoinTelegramChannel TEXT, conf_maxCount TEXT, conf_registerDate TEXT, conf_withdrawLessThan TEXT, conf_ignoreTrxAmount TEXT, conf_walletId TEXT, conf_reset TEXT, conf_initialFreeTurnover TEXT, conf_changeGameld TEXT, conf_changeGameId TEXT, conf_onlyCheckIsDeposited TEXT, conf_maxWithdrawTimeDeposit TEXT, conf_minCount TEXT, conf_fixRT TEXT, conf_showIfAmount TEXT, conf_maxWithdrawTimeAmount TEXT, conf_claimGroup TEXT, conf_rollover TEXT, conf_displayDescriptionOnly TEXT, conf_customBonus TEXT, conf_hidewhenNA TEXT, conf_offUsernames TEXT, conf_initialFreeAmount TEXT, conf_initial_free_limit TEXT, conf_lastWeekTotalDepositPercent TEXT, conf_max_withdraw TEXT, conf_creditLessThan TEXT, conf_resetHour TEXT, conf_displayAngpaoText TEXT, conf_deposit_free_limit TEXT, conf_min_withdraw TEXT);
  CREATE TABLE IF NOT EXISTS sessions(username TEXT, url TEXT, cookies BLOB, session_data BLOB, user_agent TEXT, ip_address TEXT, is_valid INT DEFAULT 1, last_used_at DATETIME DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(username, url));
  CREATE TABLE IF NOT EXISTS metrics(run_id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, duration_seconds REAL, total_scraped INT, new_bonuses INT, spv REAL, errors INT);
  CREATE TABLE IF NOT EXISTS logs(log_id INTEGER PRIMARY KEY, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, level TEXT, source TEXT, message TEXT);
  """); conn.commit()

def query(query_str, args=()):
    """Executes args synchronous query."""
    conn = get_conn()
    try:
        cursor = conn.cursor(); cursor.execute(query_str, args)
        if any(keyword in query_str.upper() for keyword in ["INSERT", "UPDATE", "DELETE", "REPLACE"]):
            conn.commit()
        return cursor.fetchall()
    except Exception as error: raise error

# ==============================================================================
# SECTION: IO (Original: io_manager.py)
# Description: CSV handling and JSON session persistence.
# ==============================================================================

def serialize_cookies(cookie_jar):
    if hasattr(cookie_jar, '__iter__'): return [{'name': cookie.name, 'value': cookie.value, 'domain': cookie.domain, 'path': cookie.path} for cookie in cookie_jar]
    return []

def deserialize_cookies(cookie_list):
    cookie_jar = requests.cookies.RequestsCookieJar()
    if isinstance(cookie_list, list):
        for cookie in cookie_list: cookie_jar.set(cookie['name'], cookie['value'], domain=cookie.get('domain'), path=cookie.get('path'))
    return cookie_jar

def load(username, url):
    """Loads session data from the database."""
    results = query("SELECT cookies, session_data, last_used_at FROM sessions WHERE username=? AND url=?", (username, url))
    if not results: return None
    raw_cookies, raw_session, timestamp = results[0]
    try:
        cookies_json = raw_cookies.decode('utf-8') if isinstance(raw_cookies, bytes) else raw_cookies
        session_json = raw_session.decode('utf-8') if isinstance(raw_session, bytes) else raw_session
        return {'cookie_jar': deserialize_cookies(json.loads(cookies_json)), 'session_data': json.loads(session_json), 'timestamp': timestamp}
    except: return None

def save(username, url, cookie_jar, session_data):
    """Saves session data using safe JSON serialization."""
    query("REPLACE INTO sessions(username, url, cookies, session_data, last_used_at) VALUES(?, ?, ?, ?, CURRENT_TIMESTAMP)", (username, url, json.dumps(serialize_cookies(cookie_jar)), json.dumps(session_data)))

def init(headers, file_path='db/bonuses.csv', overwrite=False):
    """Initializes args CSV file with headers."""
    if not overwrite and os.access(file_path, os.F_OK): return
    with open(file_path, 'w', newline='', encoding='utf-8') as file_obj: csv.DictWriter(file_obj, headers).writeheader()

def append(headers, row_data, file_path='db/bonuses.csv'):
    """Appends a single row to CSV."""
    with open(file_path, 'a', newline='', encoding='utf-8') as file_obj: csv.DictWriter(file_obj, headers).writerow(row_data)

import logging
from logging.handlers import RotatingFileHandler

# ==============================================================================
# SECTION: LOGGING
# Description: Structured system logging with rotation.
# ==============================================================================

# Setup Logger
logger = logging.getLogger("BIE")
logger.setLevel(logging.INFO)

# File Handler (5MB limit, keep last 3 logs)
os.makedirs('err/log', exist_ok=True)
os.makedirs('db', exist_ok=True)
file_handler = RotatingFileHandler('err/log/engine.log', maxBytes=5*1024*1024, backupCount=3)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def log(level, source, message):
    """Logs an error message to file and database."""
    import ui
    # 1. Log to Structured File
    log_msg = f"[{source}] {message}"
    if level.upper() == "INFO": logger.info(log_msg)
    elif level.upper() == "WARNING": logger.warning(log_msg)
    elif level.upper() == "ERROR" or level.upper() == "FATAL": logger.error(log_msg)
    
    # 2. Console Output (if requested)
    if ui.VERBOSITY == "max": print(f"[{level}] {source}: {message}", file=sys.stderr)
    
    # 3. Database Persistence
    query("INSERT INTO logs(level, source, message) VALUES(?, ?, ?)", (level, source, message))

# ==============================================================================
# SECTION: CONFIG (Original: config.py)
# Description: Global settings, credential parsing, and proxy loading.
# ==============================================================================

class SystemState:
    """Manages global thread-safe state for the scraper (Pause, Stop, Resume)."""
    def __init__(self):
        self._pause_event, self._stop_event = threading.Event(), threading.Event()
        self._pause_event.set()
    @property
    def is_paused(self): return not self._pause_event.is_set()
    @property
    def is_stopped(self): return self._stop_event.is_set()
    def pause(self): self._pause_event.clear()
    def resume(self): self._pause_event.set()
    def stop(self): self._stop_event.set(); self._pause_event.set()
    def wait_for_resume(self): self._pause_event.wait()

state = SystemState()

# ==============================================================================
# SECTION: ERRORS (Original: error_definitions.py)
# Description: Custom error code mapping and descriptions.
# ==============================================================================

ERROR_DEFINITIONS = {
    101: {"brief": "Server Offline", "verbose": "Host unreachable."},
    102: {"brief": "Proxy/DNS Error", "verbose": "Pool exhausted."},
    104: {"brief": "Timeout", "verbose": "Request timed out."},
    201: {"brief": "ID/Name Not Found", "verbose": "Layout change likely."},
    202: {"brief": "Captcha Detected", "verbose": "Bot protection triggered."},
    301: {"brief": "Unexpected Error", "verbose": "Check snapshots."}
}

for code, phrase in http.client.responses.items():
    if code >= 400: ERROR_DEFINITIONS[code] = {"brief": phrase, "verbose": f"HTTP {code} ({phrase})."}

def get_error_info(code):
    return ERROR_DEFINITIONS.get(code, {"brief": f"Error {code}", "verbose": "Undefined error."})

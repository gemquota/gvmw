import re
import urllib.parse
import json
import net

# ==============================================================================
# SECTION: AUTH (Original: auth.py)
# Description: Handles user authentication and credential rotation.
# ==============================================================================

def login(session, url, mobile, password, merchant_id):
    """Performs login and returns user data dictionary."""
    payload = {
        "module": "/users/login",
        "mobile": mobile,
        "password": password,
        "merchantId": merchant_id,
        "domainId": "0",
        "accessId": "",
        "accessToken": "",
        "walletIsAdmin": ""
    }
    try:
        response_data = net.post_json(session, url, payload)
        if response_data.get('status') == 'SUCCESS':
            return response_data.get('data', {})
        else:
            # Return the error message wrapped in a dict if it's not a success
            error_data = response_data.get('data', {})
            if isinstance(error_data, dict):
                return error_data
            return {'message': response_data.get('status', 'Unknown Error')}
    except Exception as e:
        return {'message': str(e)}

# ==============================================================================
# SECTION: API (Original: api.py)
# Description: Endpoint construction and syncData payload management.
# ==============================================================================

def get_api_endpoint(base_url):
    """Constructs the standard PHP API endpoint for a given base URL."""
    return f"{base_url.rstrip('/')}/api/v1/index.php"

def get_auth_token(session, endpoint_url, merchant_id, session_token, session_id):
    """
    Exchanges a session token for an authorization token via a GET request.
    This is the 'Ritual' required before calling syncData or other restricted endpoints.
    """
    params = {
        "module": "/users/userData",
        "merchantId": merchant_id,
        "token": session_token,
        "id": session_id,
        "domainId": "0"
    }
    try:
        data = net.get_json(session, endpoint_url, params=params)
        if data.get('status') == 'SUCCESS':
            # Returns the full user data with the actual authorization tokens
            return data.get('data', {})
    except Exception:
        pass
    return None

def fetch_sync_data(session, endpoint_url, merchant_id, access_token, access_id):
    """Fetches synchronized bonus/promotion data from the site API."""
    payload = {
        "module": "/users/syncData",
        "merchantId": merchant_id,
        "accessToken": access_token,
        "accessId": access_id,
        "domainId": "0",
        "walletIsAdmin": ""
    }
    return net.post_json(session, endpoint_url, payload)

# ==============================================================================
# SECTION: PARSER (Original: parser.py)
# Description: Variable extraction from HTML and external JavaScript bundles.
# ==============================================================================

def extract_variable(text, var_name):
    """
    Extracts a variable value from a string of HTML/JS using multiple regex patterns.
    """
    # 1. Try standard variable assignment: const NAME = "VALUE"
    var_pattern = r'(?:var|const|let)\s+' + var_name + r'\s*=\s*["\']([^"\\]+)["\\]'
    match = re.search(var_pattern, text)
    if match: return match.group(1)
    
    # 2. Try unquoted numeric assignment: const NAME = 123
    num_pattern = r'(?:var|const|let)\s+' + var_name + r'\s*=\s*(\d+)'
    match = re.search(num_pattern, text)
    if match: return match.group(1)
    
    # 3. Try object property style: merchantId:"123"
    obj_pattern = var_name + r'\s*[:=]\s*["\']([^"\\]+)["\\]'
    match = re.search(obj_pattern, text)
    if match: return match.group(1)

    raise ValueError(f"Variable '{var_name}' not found in source.")

def get_merchant_details(html_content, session=None, base_url=None):
    """
    Extracts Merchant ID and Name from HTML or associated JS bundles.
    """
    if "Just a moment..." in html_content or "Enable JavaScript" in html_content:
        raise ValueError("Captcha: Cloudflare challenge detected.")
    if "Access denied" in html_content or "Access Denied" in html_content:
        raise ValueError("Blocked: Access Denied.")

    try:
        merchant_id = extract_variable(html_content, 'MERCHANTID')
        merchant_name = extract_variable(html_content, 'MERCHANTNAME')
        return merchant_id, merchant_name
    except ValueError:
        pass
        
    if session and base_url:
        scripts = re.findall(r'<script[^>]+src=["\\]([^"\\]+)["\\]', html_content)
        candidates = [s for s in scripts if 'entry-index' in s or 'index' in s or 'app' in s]
        
        for script_src in candidates:
            script_url = urllib.parse.urljoin(base_url, script_src)
            try:
                response = session.get(script_url, timeout=10)
                if response.status_code != 200: continue
                js_content = response.text
                try:
                    merchant_id = extract_variable(js_content, 'MERCHANTID')
                    merchant_name = extract_variable(js_content, 'MERCHANTNAME')
                    return merchant_id, merchant_name
                except ValueError: pass
                id_match = re.search(r'merchantId\s*:\s*["\\]([^"\\]+)["\\]', js_content)
                name_match = re.search(r'merchantName\s*:\s*["\\]([^"\\]+)["\\]', js_content)
                if id_match: return id_match.group(1), (name_match.group(1) if name_match else "Unknown")
            except Exception: continue
                    
    raise ValueError("Could not find merchant identification details in HTML or JS.")

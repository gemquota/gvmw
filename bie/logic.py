import json
import re
import datetime
import hashlib
from math import pow, log2, log10
import difflib
from urllib.parse import urlparse
from typing import List, Dict, Any, Optional, Union

# ==============================================================================
# SECTION: MODELS (Original: models.py)
# Description: Data structures, key normalization, and API-to-DB mapping.
# ==============================================================================

# Base headers for bonus discovery
BONUS_HEADERS: List[str] = "url,merchant_name,external_id,bonus_name,transactiontype,bonusfixed,amount,minwithdraw,maxwithdraw,rollover,ratio,balance,claimconfig,claimcondition,bonus,bonusrandom,reset,mintopup,maxtopup,referlink,perceived_value,is_new".split(',')

# Keys within the 'claimconfig' JSON field that we want to flatten into dedicated columns
CONFIGURATION_KEYS: List[str] = [
    'startDate', 'max_round', 'claimTime', 'mobileAppOnly', 'registerBeforeDate', 
    'mustJoinTelegramChannel', 'maxCount', 'registerDate', 'withdrawLessThan', 
    'ignoreTrxAmount', 'walletId', 'reset', 'initialFreeTurnover', 'changeGameld', 
    'changeGameId', 'onlyCheckIsDeposited', 'maxWithdrawTimeDeposit', 'minCount', 
    'fixRT', 'showIfAmount', 'maxWithdrawTimeAmount', 'claimGroup', 'rollover', 
    'displayDescriptionOnly', 'customBonus', 'hidewhenNA', 'offUsernames', 
    'initialFreeAmount', 'initial_free_limit', 'lastWeekTotalDepositPercent', 
    'max_withdraw', 'creditLessThan', 'resetHour', 'displayAngpaoText', 
    'deposit_free_limit', 'min_withdraw'
]

# Extended headers for CSV exports including flattened configuration fields
EXTENDED_BONUS_HEADERS: List[str] = BONUS_HEADERS + [f"conf_{key}" for key in CONFIGURATION_KEYS]

def normalize(bonus_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Lowercases all keys in a dictionary for case-insensitive access."""
    return {key.lower(): value for key, value in bonus_dict.items()}

def extract(bonus_dict: Dict[str, Any]) -> Dict[str, str]:
    """
    Extracts and flattens nested JSON config fields from 'claimconfig' 
    into a flat dictionary prefixed with 'conf_'.
    """
    claim_config = bonus_dict.get('claimconfig')
    if isinstance(claim_config, str):
        try: 
            claim_config = json.loads(claim_config)
        except: 
            claim_config = {}
    elif not isinstance(claim_config, dict):
        claim_config = {}
        
    flattened_config = {}
    for key in CONFIGURATION_KEYS:
        value = claim_config.get(key)
        if isinstance(value, (list, dict)):
            value = json.dumps(value)
        flattened_config[f"conf_{key}"] = str(value) if value is not None else None
    return flattened_config

def map(bonus_data: Dict[str, Any], site_url: str, merchant_name: str, pv_score: float, is_new: int) -> Dict[str, Any]:
    """
    Maps a raw bonus dictionary from the scraper to the standardized CSV/DB header format.
    """
    # Create base dictionary mapping available keys to headers
    row_dict = {header: bonus_data.get(header, bonus_data.get(header.upper(), '')) for header in BONUS_HEADERS}
    
    # Overwrite/Set specific fields
    row_dict['url'] = site_url
    row_dict['merchant_name'] = merchant_name
    row_dict['perceived_value'] = pv_score
    row_dict['is_new'] = is_new
    
    # Handle common alias mappings
    if not row_dict.get('external_id'): 
        row_dict['external_id'] = bonus_data.get('id', '')
    if not row_dict.get('bonus_name'): 
        row_dict['bonus_name'] = bonus_data.get('name', '')

    # Ratio calculation
    try:
        amt = float(str(row_dict.get('amount', 0) or 0).replace(',', ''))
        mw = float(str(row_dict.get('minwithdraw', 0) or 0).replace(',', ''))
        row_dict['ratio'] = mw / amt if amt > 0 else 0
    except:
        row_dict['ratio'] = 0
    
    return row_dict

# Compatibility aliases
headers = BONUS_HEADERS
extended = EXTENDED_BONUS_HEADERS
norm = normalize
row = map

# ==============================================================================
# SECTION: DEDUPLICATION (Original: deduplication.py)
# Description: Fuzzy matching logic to prevent mirror-site data collision.
# ==============================================================================

def clean_name(name: str) -> str:
    """Normalizes a bonus name by removing HTML tags and collapsing whitespace."""
    if not name: return ""
    name = re.sub(r'<[^>]+>', '', name)
    name = ' '.join(name.split())
    return name.lower()

def extract_numbers(text: str) -> List[str]:
    """Extracts all sequences of digits from a string."""
    return re.findall(r'\d+', text)

def extract_roman_numerals(text: str) -> List[str]:
    """Extracts potential roman numerals (I through X) that appear as separate words."""
    return re.findall(r'\b(i{1,3}|iv|v|vi{1,3}|ix|x)\b', text)

def calculate_similarity(string1: str, string2: str) -> float:
    """Calculates the similarity ratio between two strings using difflib."""
    return difflib.SequenceMatcher(None, clean_name(string1), clean_name(string2)).ratio()

def is_fuzzy_match(string1: str, string2: str, threshold: float = 0.80) -> bool:
    """
    Returns True if similarity is high and tier markers (numbers/romans) match.
    """
    cleaned1, cleaned2 = clean_name(string1), clean_name(string2)
    if not cleaned1 and not cleaned2: return True
    if not cleaned1 or not cleaned2: return False
    ratio = difflib.SequenceMatcher(None, cleaned1, cleaned2).ratio()
    if ratio < threshold: return False
    if extract_numbers(cleaned1) != extract_numbers(cleaned2):
        if extract_numbers(cleaned1) and extract_numbers(cleaned2): return False
    if extract_roman_numerals(cleaned1) != extract_roman_numerals(cleaned2):
        if extract_roman_numerals(cleaned1) and extract_roman_numerals(cleaned2): return False
    return True

# ==============================================================================
# SECTION: FILTER & PV (Original: filter.py)
# Description: Scoring algorithm V14 and high-level data filtering.
# ==============================================================================

def numeric(value: Any, default: float = 0.0) -> float:
    """Safely converts a value to float, handling strings and nested dicts."""
    if isinstance(value, (int, float)): return float(value)
    if isinstance(value, str):
        try: return float(value)
        except: return default
    if isinstance(value, dict):
        return numeric(value.get('value', value.get('amount', default)), default)
    return default

def fuzzy(name: str, existing_names: List[str], threshold: float = 0.80) -> Optional[str]:
    """Checks if 'name' is a fuzzy duplicate of any entry in 'existing_names'."""
    for name_to_check in existing_names:
        if is_fuzzy_match(name, name_to_check, threshold):
            return name_to_check
    return None

def fingerprint(bonus_dict: Dict[str, Any]) -> str:
    """Generates a SHA256 hash based on core bonus parameters."""
    components = [
        str(bonus_dict.get('name')), str(bonus_dict.get('amount')),
        str(bonus_dict.get('rollover')), str(bonus_dict.get('minwithdraw')),
        str(bonus_dict.get('maxwithdraw'))
    ]
    return hashlib.sha256("|".join(components).encode()).hexdigest()

def score(bonus_dict: Dict[str, Any]) -> float:
    """Calculates 'Beatability' using V14 of the PV Algorithm."""
    amount = numeric(bonus_dict.get('amount', 0))
    if amount <= 0: return 0.0
    max_withdraw = numeric(bonus_dict.get('maxwithdraw', 0))
    if max_withdraw <= 0:
        import base
        max_withdraw = base.DEFAULT_MAX_WITHDRAW
    min_withdraw, rollover = numeric(bonus_dict.get('minwithdraw', 0)), numeric(bonus_dict.get('rollover', 0))
    reward = (10 * log2(max_withdraw + 1)) * (1 + 0.2 * log10(amount + 1))
    difficulty = pow(max(1, max(min_withdraw, amount * rollover) / amount), 1.25) * (1 + rollover / 20)
    return max(0.0, reward / difficulty)

def filter(bonus_dict: Dict[str, Any]) -> bool:
    """Business rules for filtering junk bonuses."""
    name = str(bonus_dict.get('name', bonus_dict.get('bonus_name', ''))).lower()
    condition = str(bonus_dict.get('claimcondition', '')).lower()
    if any(search_keyword in name or search_keyword in condition for search_keyword in ['telegram', 'download', 'app']): return True
    amount = numeric(bonus_dict.get('amount', bonus_dict.get('bonusfixed', 0)))
    if amount < 1: return True
    if (numeric(bonus_dict.get('minwithdraw', 0)) / amount if amount > 0 else 0) > 30: return True
    rollover = numeric(bonus_dict.get('rollover', 0))
    if rollover > 30 * amount: return True
    max_withdraw = numeric(bonus_dict.get('maxwithdraw', 0))
    if 1 <= max_withdraw <= 15: return True
    return False

def highvalue(bonus_dict: Dict[str, Any]) -> bool:
    """Identifies premium bonuses."""
    amount = numeric(bonus_dict.get('amount', bonus_dict.get('bonusfixed', 0)))
    if amount < 1: return False
    if numeric(bonus_dict.get('maxwithdraw', 0)) < 50: return False
    name, condition = str(bonus_dict.get('name', '')).lower(), str(bonus_dict.get('claimcondition', '')).lower()
    keywords = ['commission', 'rebate', 'loss', 'rollover', 'downline', 'first deposit', 'share']
    if any(search_keyword in name or search_keyword in condition for search_keyword in keywords): return True
    return score(bonus_dict) > 10.0

def expiry(text: str) -> Optional[datetime.datetime]:
    """Placeholder for expiration extraction logic."""
    return None

# Compatibility Aliases
safe_float = numeric
fuzzy_match = fuzzy
gen_fingerprint = fingerprint
calc_score = score
should_filter = filter
is_high = highvalue
extract_expiry = expiry

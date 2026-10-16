import base
import net
import re
import collections
import datetime
import time
import threading
import requests
import http.client
import os
import sys
try:
    import psutil
except ImportError:
    psutil = None
from rich.console import Console, Group
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.align import Align
from rich import box

# --- Global UI Components ---
console = Console(highlight=False)
DURATION_SAMPLES = collections.deque(maxlen=10)
# Rolling history for calculating health windows (Max 100 to cover R100) 
ROLLING_HISTORY = collections.deque(maxlen=100) 
BONUS_HISTORY = collections.deque(maxlen=50)
UPDATE_LOCK = threading.Lock()
VERBOSITY = "min"
START_TIME = time.time()

# Streak Tracking Globals
CURRENT_STREAK_TYPE = None # True = Success, False = Fail
CURRENT_STREAK_COUNT = 0

# Mapping of success rates to status icons
STATUS_MARKERS = [
 (0.0,"🟥"),(10.0,"🔴"),(20.0,"♥️ "),(25.0,"🟧"),(35.0,"🟠"),
 (45.0,"🧡"),(50.0,"🟨"),(60.0,"🟡"),(70.0,"💛"),(75.0,"🟩"),
 (85.0,"🟢"),(95.0,"💚"),(100.0,"💚")
]

STEPS = ["red", "orange1", "yellow", "lime", "green", "turquoise2", "blue", "dark_blue", "purple", "violet"]

def init_dashboard_data(task_count, available_proxy_count, num_workers, shuffle_mode, ip_score):
    """
    Prepares the configuration dictionary for the initialization dashboard.
    """
    throughput_est = int((60 / ((base.MIN_DELAY + base.MAX_DELAY) / 2)) * num_workers)
    shuffle_status = "ENABLED" if shuffle_mode else "DISABLED"
    priority_status = "Randomized" if shuffle_mode else "Sequential"
    io_status = "OPTIMAL" if os.access('db/base.db', os.W_OK) else "READ-ONLY"
    network_type = "Async/uvloop" if 'uvloop' in sys.modules else "Async/Standard"
    
    return {
        'urls': task_count,
        'proxies': available_proxy_count,
        'workers': num_workers,
        'throughput': f"~{throughput_est} URLs/min",
        'proxy_logic': 'Sticky-Session',
        'network_type': network_type,
        'priority': priority_status,
        'shuffle': shuffle_status,
        'db_name': 'base.db (WAL)',
        'io_status': io_status,
        'ssl_status': 'Disabled',
        'user_agent': base.USER_AGENT,
        'ip_score': ip_score
    }

def print_initialization_dashboard(config_data):
    """
    ENGINE v5.0: THE SYMMETRY COMMAND CENTER
    Full-width rebuild with 6-panel telemetry and expanded data categories.
    """
    from rich.text import Text
    from rich.align import Align
    import platform

    def create_panel_table(title_color="cyan"):
        t = Table(show_header=False, box=None, padding=(0, 1), expand=True)
        t.add_column(justify="left", style="white", ratio=1)
        return t

    # --- PANEL 1: PERFORMANCE (Telemetry) ---
    perf_t = create_panel_table("bright_cyan")
    perf_t.add_row(f"[bold bright_cyan]Concurrency[/]\n[yellow]{config_data.get('workers', 0)} Workers[/]")
    perf_t.add_row(f"[bold bright_cyan]Throughput[/]\n[green]{config_data.get('throughput', 'N/A')}[/]")
    perf_t.add_row(f"[bold bright_cyan]Delays[/]\n[green]{base.MIN_DELAY}-{base.MAX_DELAY}s[/]")
    perf_t.add_row(f"[bold bright_cyan]Timeout[/]\n[green]{base.TIMEOUT}s[/]")

    # --- PANEL 2: INFRASTRUCTURE ---
    infra_t = create_panel_table("bright_magenta")
    infra_t.add_row(f"[bold bright_magenta]Proxy Pool[/]\n[green]{config_data.get('proxies', 0)} Active[/]")
    infra_t.add_row(f"[bold bright_magenta]Proxy Logic[/]\n[magenta]{config_data.get('proxy_logic', 'Sticky-Session')}[/]")
    infra_t.add_row(f"[bold bright_magenta]Network Type[/]\n[magenta]{config_data.get('network_type', 'AsyncIO')}[/]")

    # --- PANEL 3: JOB INTELLIGENCE ---
    job_t = create_panel_table("bright_yellow")
    job_t.add_row(f"[bold bright_yellow]Total Tasks[/]\n[cyan]{config_data.get('urls', 0)} Targets[/]")
    job_t.add_row(f"[bold bright_yellow]Priority[/]\n[yellow]{config_data.get('priority', 'Standard')}[/]")
    job_t.add_row(f"[bold bright_yellow]Shuffle[/]\n[green]{config_data.get('shuffle', 'OFF')}[/]")
    job_t.add_row(f"[bold bright_yellow]Max Withdraw[/]\n[yellow]${base.DEFAULT_MAX_WITHDRAW:.0f}[/]")

    # --- PANEL 4: ENVIRONMENT ---
    env_t = create_panel_table("bright_blue")
    env_t.add_row(f"[bold bright_blue]OS[/] [white]{platform.system()}[/]")
    env_t.add_row(f"[bold bright_blue]Py Version[/]\n[white]{platform.python_version()}[/]")
    env_t.add_row(f"[bold bright_blue]Database[/]\n[green]{config_data.get('db_name', 'base.db')}[/]")

    # --- PANEL 5: SYSTEM HEALTH ---
    sys_t = create_panel_table("bright_green")
    cpu_usage = "N/A"
    mem_usage = "N/A"
    if psutil:
        try:
            cpu_usage = f"{psutil.cpu_percent()} %"
            mem_usage = f"{psutil.virtual_memory().percent} %"
        except: pass
    sys_t.add_row(f"[bold bright_green]CPU Load[/]\n[bright_white]{cpu_usage}[/]")
    sys_t.add_row(f"[bold bright_green]RAM Usage[/]\n[bright_white]{mem_usage}[/]")
    sys_t.add_row(f"[bold bright_green]IO Status[/]\n[green]{config_data.get('io_status', 'Unknown')}[/]")

    # --- PANEL 6: SECURITY & AUTH ---
    sec_t = create_panel_table("bright_red")
    sec_t.add_row(f"[bold bright_red]Auth User[/]\n[magenta]{base.UI_USER}[/]")
    sec_t.add_row(f"[bold bright_red]SSL Check[/]\n[green]{config_data.get('ssl_status', 'Unknown')}[/]")
    sec_t.add_row(f"[bold bright_red]IP Reputation[/]\n[yellow]{config_data.get('ip_score', 'N/A')}/100[/]")

    # --- PANEL 7: USER AGENT (Full Width) ---
    ua_panel = Panel(
        Align.center(f"[bold white]User Agent Identity[/]\n[yellow]{config_data.get('user_agent', 'Default')}[/]"),
        title="[bold]🕵️ USER AGENT[/]",
        border_style="bright_white",
        expand=True
    )
    
    # --- HEALTH METRICS PANEL (Vertical, Narrow) ---
    health_items = []
    for health_rate, health_icon in STATUS_MARKERS:
        health_items.append(f"{health_icon} {int(health_rate)}%")
    
    health_panel = Panel(
        Text("\n".join(health_items), justify="left"),
        title="[bold]HEALTH[/]",
        border_style="white",
        width=14,
        height=20
    )

    # --- ERRORS PANEL (Vertical, Narrow) ---
    error_lines = [
        ("✅ OK", "bright_green"),
        ("👻 404", "grey58"),
        ("🚫 403", "red"),
        ("🚚 301", "cyan"),
        ("📡 101", "yellow"),
        ("☁️ 503", "gold1"),
        ("🐌 Lag", "orange1"),
        ("📉 Track", "dim white")
    ]
    error_text_obj = Text()
    for txt, style in error_lines:
        error_text_obj.append(txt + "\n", style=style)

    error_panel = Panel(
        error_text_obj,
        title="[bold]ERRORS[/]",
        border_style="grey58",
        width=14,
        height=20
    )

    # --- CONSTRUCTING THE LEFT GRID (2x3) ---
    left_grid = Table.grid(expand=True)
    left_grid.add_column(ratio=1)
    left_grid.add_column(ratio=1)
    left_grid.add_column(ratio=1)

    left_grid.add_row(
        Panel(perf_t, title="[bold]⚡ PERFORMANCE[/]", border_style="bright_cyan", expand=True),
        Panel(infra_t, title="[bold]🌐 INFRASTRUCTURE[/]", border_style="bright_magenta", expand=True),
        Panel(job_t, title="[bold]🧠 JOB INTEL[/]", border_style="bright_yellow", expand=True)
    )
    left_grid.add_row(
        Panel(env_t, title="[bold]💻 ENVIRONMENT[/]", border_style="bright_blue", expand=True),
        Panel(sys_t, title="[bold]💾 SYSTEM HEALTH[/]", border_style="bright_green", expand=True),
        Panel(sec_t, title="[bold]🛡️ SECURITY[/]", border_style="bright_red", expand=True)
    )

    # --- MASTER GRID (Left Grid + Health + Errors) ---
    master_grid = Table.grid(expand=True)
    master_grid.add_column(ratio=1)
    master_grid.add_column(width=14)
    master_grid.add_column(width=14)

    master_grid.add_row(left_grid, health_panel, error_panel)

    # --- DASHBOARD LAYOUT GROUP ---
    dashboard_layout = Group(
        master_grid,
        ua_panel
    )

    # --- COMMAND STRIP (DASHBOARD LINK) ---
    link_panel = Panel(
        Align.center(f"[bold white]📡 COMMAND DASHBOARD ACTIVE :[/][bold cyan] http://127.0.0.1:8000[/]"),
        border_style="bright_white",
        style="on blue",
        padding=(0, 1)
    )

    # --- FINAL ASSEMBLY ---
    console.print("\n")
    console.print(Panel(
        dashboard_layout,
        title="[bold white]🚀 Bonus Scraper Engine v5.0[/bold white]",
        border_style="bright_white",
        padding=(1, 1)
    ))
    console.print(link_panel)
    console.print(Align.center("[bold red]●[/][bold white] SYSTEM READY [/][bold cyan]PRESS [CTRL+C] TO TERMINATE[/]"))
    console.print("\n")

def print_final_summary(stats):
    """
    Renders the final run summary using a detailed 2x3 grid layout similar to initialization.
    """
    from rich.panel import Panel
    from rich.table import Table
    from rich.align import Align
    from rich.text import Text

    def create_panel_table(title_color="cyan"):
        t = Table(show_header=False, box=None, padding=(0, 1), expand=True)
        t.add_column(justify="left", style="white", ratio=1)
        return t

    total_sites = stats.get('index', 0)
    successes = stats.get('successes', 0)
    failures = stats.get('failures', 0)
    total_bonuses = stats.get('total_bonuses', 0)
    new_bonuses = stats.get('new_bonuses', 0)
    
    success_rate = (successes / max(1, total_sites)) * 100
    yield_rate = (total_bonuses / max(1, total_sites)) * 100

    # --- PANEL 1: EXECUTION STATS ---
    exec_t = create_panel_table("bright_cyan")
    exec_t.add_row(f"[bold bright_cyan]Duration[/]\n[white]{stats.get('duration_str', '--:--:--')}[/]")
    exec_t.add_row(f"[bold bright_cyan]Throughput[/]\n[green]{stats.get('throughput_final', '--')} URLs/s[/]")
    exec_t.add_row(f"[bold bright_cyan]Total Requests[/]\n[white]{total_sites}[/]")

    # --- PANEL 2: YIELD ANALYSIS ---
    yield_t = create_panel_table("bright_yellow")
    yield_t.add_row(f"[bold bright_yellow]Total Volume[/]\n[yellow]{total_bonuses} Bonuses[/]")
    yield_t.add_row(f"[bold bright_yellow]Net New[/]\n[green]{new_bonuses} Found[/]")
    yield_t.add_row(f"[bold bright_yellow]Value Density[/]\n[white]{(total_bonuses/max(1, total_sites)):.2f} Bonus/Site[/]")

    # --- PANEL 3: NETWORK HEALTH ---
    health_t = create_panel_table("bright_red")
    health_t.add_row(f"[bold bright_red]Success Rate[/]\n[{get_success_color(success_rate)}]{success_rate:.1f}%[/]")
    health_t.add_row(f"[bold bright_red]Failure Rate[/]\n[red]{(failures/max(1, total_sites)*100):.1f}%[/]")
    health_t.add_row(f"[bold bright_red]Avg Latency[/]\n[yellow]{stats.get('avg_latency', '~150ms')}[/]")

    # --- PANEL 4: RESOURCE USAGE ---
    res_t = create_panel_table("bright_blue")
    res_t.add_row(f"[bold bright_blue]Peak RAM[/]\n[white]{stats.get('peak_ram', '-- MB')}[/]")
    res_t.add_row(f"[bold bright_blue]Avg CPU[/]\n[white]{stats.get('avg_cpu', '-- %')}[/]")
    res_t.add_row(f"[bold bright_blue]Threads[/]\n[magenta]{stats.get('threads_status', 'Clean Exit')}[/]")

    # --- PANEL 5: DATA INTEGRITY ---
    data_t = create_panel_table("bright_green")
    data_t.add_row(f"[bold bright_green]DB Updates[/]\n[green]{successes} Rows[/]")
    data_t.add_row(f"[bold bright_green]Files Saved[/]\n[white]{stats.get('files_saved', '2 (CSV/JSON)')}[/]")
    data_t.add_row(f"[bold bright_green]Audit[/]\n[green]{stats.get('audit_status', 'PASSED')}[/]")

    # --- PANEL 6: DISTRIBUTION ---
    dist_t = create_panel_table("white")
    # Simple text graph
    graph = "🟩" * int(success_rate / 10) + "🟥" * int((100 - success_rate) / 10)
    dist_t.add_row(f"[bold]Success vs Fail[/]\n{graph}")
    dist_t.add_row(f"[bold]Yield Efficiency[/]\n[{get_yield_color(yield_rate)}]{yield_rate:.1f}% Efficiency[/]")

    grid = Table.grid(expand=True)
    grid.add_column(ratio=1)
    grid.add_column(ratio=1)
    grid.add_column(ratio=1)

    grid.add_row(
        Panel(exec_t, title="[bold]⚡ EXECUTION STATS[/]", border_style="bright_cyan", expand=True),
        Panel(yield_t, title="[bold]💎 YIELD ANALYSIS[/]", border_style="bright_yellow", expand=True),
        Panel(health_t, title="[bold]🩺 NETWORK HEALTH[/]", border_style="bright_red", expand=True)
    )
    grid.add_row(
        Panel(res_t, title="[bold]💾 RESOURCES[/]", border_style="bright_blue", expand=True),
        Panel(data_t, title="[bold]🗄️ DATA INTEGRITY[/]", border_style="bright_green", expand=True),
        Panel(dist_t, title="[bold]📈 DISTRIBUTION[/]", border_style="white", expand=True)
    )

    console.print("\n")
    console.print(Panel(
        grid,
        title="[bold white]🏁 MISSION COMPLETE: FINAL REPORT[/bold white]",
        border_style="bright_white",
        padding=(1, 1)
    ))
    console.print("\n")


def get_status_icon(rate):
    """Returns the appropriate emoji icon based on a percentage rate."""
    for limit, icon in reversed(STATUS_MARKERS):
        if rate >= limit:
            return icon
    return STATUS_MARKERS[0][1]

def get_success_color(percentage):
    """Returns a hex color string representing a gradient from red to green."""
    if percentage < 25:
        r, g, b = 255, int(165 * (percentage / 25)), 0
    elif percentage < 50:
        r, g, b = 255, int(165 + (90 * ((percentage - 25) / 25))), 0
    elif percentage < 75:
        r, g, b = int(255 * ((75 - percentage) / 25)), 255, 0
    else:
        r, g, b = 0, int(255 - (155 * ((percentage - 75) / 25))), 0
    return f"#{r:02x}{g:02x}{b:02x}"

def get_eta_color(current_idx, total_sites):
    """Complex gradient: 0-5% (Blue->Purple->Red), 5-100% (Red->Orange->Yellow->Green->Dark Green)."""
    if total_sites <= 0: return "#0000ff"
    progress = current_idx / total_sites
    
    if progress <= 0.05:
        p = progress / 0.05
        if p < 0.5: 
            sp = p / 0.5
            r, g, b = int(128 * sp), 0, int(255 - 127 * sp)
        else: 
            sp = (p - 0.5) / 0.5
            r, g, b = int(128 + 127 * sp), 0, int(128 - 128 * sp)
    else:
        p = (progress - 0.05) / 0.95
        if p < 0.25:
            sp = p / 0.25
            r, g, b = 255, int(165 * sp), 0
        elif p < 0.50:
            sp = (p - 0.25) / 0.25
            r, g, b = 255, int(165 + 90 * sp), 0
        elif p < 0.75:
            sp = (p - 0.50) / 0.25
            r, g, b = int(255 * (1 - sp)), 255, 0
        else:
            sp = (p - 0.75) / 0.25
            r, g, b = 0, int(255 - 155 * sp), 0
            
    return f"#{r:02x}{g:02x}{b:02x}"

def get_yield_color(value):
    """
    Returns a hex color string based on yield percentage value using interpolation.
    0-100: Yellow -> Green
    100-200: Green -> Dark Green
    200-300: Dark Green -> Dark Blue -> Blue
    300-400: Blue -> Dark Purple
    400-500: Dark Purple -> Purple
    500-600: Purple -> Dark Orange
    600-700: Dark Orange -> Orange
    >700: Red, Yellow, Teal, Violet
    """
    stops = {
        0: (255, 255, 0),      # Yellow
        100: (0, 255, 0),      # Green
        200: (0, 100, 0),      # Dark Green
        250: (0, 0, 139),      # Dark Blue (midpoint)
        300: (0, 0, 255),      # Blue
        400: (75, 0, 130),     # Dark Purple (Indigo)
        500: (128, 0, 128),    # Purple
        600: (255, 140, 0),    # Dark Orange
        700: (255, 165, 0),    # Orange
        800: (255, 0, 0),      # Red
        900: (255, 255, 0),    # Yellow
        1000: (0, 128, 128),   # Teal
        1100: (238, 130, 238)  # Violet
    }
    
    max_k = max(stops.keys())
    if value >= max_k:
        r, g, b = stops[max_k]
        return f"#{r:02x}{g:02x}{b:02x}"
        
    lower = 0
    upper = 100
    for k in sorted(stops.keys()):
        if k <= value:
            lower = k
        else:
            upper = k
            break
            
    if upper == lower:
        r, g, b = stops[lower]
        return f"#{r:02x}{g:02x}{b:02x}"
    
    ratio = (value - lower) / (upper - lower)
    start_c = stops[lower]
    end_c = stops[upper]
    
    r = int(start_c[0] + (end_c[0] - start_c[0]) * ratio)
    g = int(start_c[1] + (end_c[1] - start_c[1]) * ratio)
    b = int(start_c[2] + (end_c[2] - start_c[2]) * ratio)
    
    return f"#{r:02x}{g:02x}{b:02x}"

def calculate_rolling_metric(history, window_size):
    """Calculates success % for the last N items in history."""
    if not history: return 0
    # Slice the deque to get the last N items
    window = list(history)[-window_size:]
    if not window: return 0
    return int((sum(window) / len(window)) * 100)

def format_metric(value):
    """Formats percentage for display: '100' -> 'AA', <10 with leading zero."""
    if value == 100: return "[bright_green]AA[/]"
    color = get_success_color(value)
    return f"[{color}]{value:02d}[/]"

def update_dashboard(data):
    """Renders a single-line status update to the console."""
    global CURRENT_STREAK_TYPE, CURRENT_STREAK_COUNT
    
    index = data['index']
    successes = data['successes']
    site_url = data['site_url'].replace('https://', '').replace('www.', '')
    status_msg = data['status_message']
    total_sites = data.get('N', 0)
    failures = data.get('failures', 0)
    ip_score = data.get('ip_score', 0)
    site_new_bonuses = int(data.get("site_new_bonuses", 0))
    total_new_bonuses = int(data.get("total_new_bonuses", 0))

    elapsed_total = time.time() - START_TIME
    elapsed_item = data.get('elapsed', 0)
    DURATION_SAMPLES.append(elapsed_item)
    avg_duration = sum(DURATION_SAMPLES) / len(DURATION_SAMPLES) if DURATION_SAMPLES else 0
    avg_delay = (base.MIN_DELAY + base.MAX_DELAY) / 2
    remaining_sites = total_sites - index
    worker_count = int(data.get('nw', 1))
    
    est_remaining_sec = (remaining_sites * (avg_duration + avg_delay)) / (worker_count if worker_count > 0 else 1)
    minutes = int(est_remaining_sec // 60)
    seconds = est_remaining_sec % 60
    time_str = f"{minutes}m{seconds:06.3f}s"

    # --- Streak & History Logic ---
    is_success = 1 if status_msg.startswith("✅") else 0
    ROLLING_HISTORY.append(is_success)

    # Streak Counter
    if CURRENT_STREAK_TYPE is None:
        CURRENT_STREAK_TYPE = bool(is_success)
        CURRENT_STREAK_COUNT = 1
    elif CURRENT_STREAK_TYPE == bool(is_success):
        CURRENT_STREAK_COUNT += 1
    else:
        CURRENT_STREAK_TYPE = bool(is_success)
        CURRENT_STREAK_COUNT = 1

    streak_icon = "✅" if CURRENT_STREAK_TYPE else "❌"
    streak_color = "bright_green" if CURRENT_STREAK_TYPE else "red"
    streak_display = f"[{streak_color}]{streak_icon}{CURRENT_STREAK_COUNT:02d}[/]"

    # Calculate Rolling Metrics
    r5 = calculate_rolling_metric(ROLLING_HISTORY, 5)
    r10 = calculate_rolling_metric(ROLLING_HISTORY, 10)
    r20 = calculate_rolling_metric(ROLLING_HISTORY, 20)
    r50 = calculate_rolling_metric(ROLLING_HISTORY, 50)
    r100 = calculate_rolling_metric(ROLLING_HISTORY, 100)
    
    # Calculate Yield (Value Rate)
    # Yield = (Total Diamonds Found / Total Rows Processed) * 100
    yield_val = (total_new_bonuses / index * 100) if index > 0 else 0.0

    cumulative_rate = (successes / index * 100) if index > 0 else 0
    cumulative_color = get_success_color(cumulative_rate)
    eta_color = get_eta_color(index, total_sites)
    yield_color = get_yield_color(yield_val)
    
    # Text Status Formatting
    if status_msg.startswith("✅"):
        text, icon, style = "DONE", "✅", "bright_green"
    elif "404" in status_msg:
        text, icon, style = "E404", "👻", "grey58"
    elif "403" in status_msg:
        text, icon, style = "E403", "🚫", "red"
    elif "301" in status_msg:
        text, icon, style = "E301", "🚚", "cyan"
    elif "101" in status_msg:
        text, icon, style = "E101", "📡", "yellow"
    elif "503" in status_msg:
        text, icon, style = "E503", "☁️", "gold1"
    elif "502" in status_msg:
        text, icon, style = "E502", "🌩️", "gold1"
    elif "500" in status_msg:
        text, icon, style = "E500", "💥", "red"
    elif "Timeout" in status_msg or "408" in status_msg or "104" in status_msg:
        text, icon, style = "TIME", "🐌", "orange1"
    else:
        error_match = re.search(r"E(\d+)", status_msg)
        text, icon, style = (f"E{error_match.group(1)}", "💻", "red") if error_match else ("FAIL", "⛔", "red")

    mem_icon = ""
    if psutil:
        try:
            mem_p = psutil.virtual_memory().percent
            if mem_p > 80: mem_icon = f"[red]💾{int(mem_p)}%[/]"
        except: pass

    # --- Color Transitions ---
    # 1. Index Transition: Red to Green
    idx_ratio = (index / total_sites) if total_sites > 0 else 0
    idx_r = int(255 * (1 - idx_ratio))
    idx_g = int(255 * idx_ratio)
    index_color = f"#{idx_r:02x}{idx_g:02x}00"

    # 2. Diamond Recoloring
    BONUS_HISTORY.append(site_new_bonuses)
    last_50_count = sum(BONUS_HISTORY)
    
    # "increase the second two zeroes one step for each one more" (total_new_bonuses)
    total_step = total_new_bonuses % len(STEPS)
    total_color = STEPS[total_step]
    
    # "the first two zeros one step for each new bonus in the last 50 sites"
    site_step = last_50_count % len(STEPS)
    site_color_step = STEPS[site_step]

    # Commission/Share coloring
    comm_color = "bright_white"
    site_type = data.get('site_type')
    if site_type == 'share': comm_color = "lime"
    elif site_type == 'comm_low': comm_color = "green"
    elif site_type == 'comm_mid': comm_color = "purple"
    elif site_type == 'comm_high': comm_color = "violet"

    site_color = "[bright_green]" if site_new_bonuses > 0 else ""
    site_end = "[/]" if site_new_bonuses > 0 else ""

    # --- Constructed Line ---
    # Layout: Index|Status|Streak [R100 R50 R20 R10 R5] Cumul% Yield%💎Site|Total⏱️ ETA🌐URL
    line = (
        f"[{index_color}]{index:03d}[/]"
        f"[{style}]{icon}{text}[/]"
        f"{streak_display} "
        f"{format_metric(r5)}{format_metric(r10)}{format_metric(r20)}{format_metric(r50)}{format_metric(r100)} "
        f"[{cumulative_color}]{int(cumulative_rate):03d}[/] "
        f"[{yield_color}]{yield_val:05.1f}[/]"
        f"💎[{site_color_step}]{site_new_bonuses:02d}[/]|[{total_color}]{total_new_bonuses:02d}[/] "
        f"⏱️ [{eta_color}]{time_str}[/]"
        f"{mem_icon}🌐[{comm_color}]{site_url}[/]"
    )

    def _send_update(payload):
        try: requests.post('http://localhost:8000/update', json=payload, timeout=0.1)
        except: pass

    if not hasattr(update_dashboard, "_queue"):
        import queue
        update_dashboard._queue = queue.Queue()
        def _worker():
            while True:
                payload = update_dashboard._queue.get()
                _send_update(payload)
                update_dashboard._queue.task_done()
        threading.Thread(target=_worker, daemon=True).start()

    update_dashboard._queue.put(data)

    with UPDATE_LOCK:
        console.print(line)
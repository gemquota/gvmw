#!/usr/bin/env python3
import sys as _s; _s.dont_write_bytecode = True
"""Independent liveness watchdog for Gem's bot swarm (draft, 22 Oct 2026).

Checks that today's governance files exist and are fresh, and that no billing
failure marker is present. Stdlib only. Never reads secrets.

  python3 watchdog.py --dry-run            # print what it would alert, send nothing
  python3 watchdog.py --date 2026-10-16    # check a past day
  python3 watchdog.py --json               # machine-readable result

Alerts: appended to /workspace/governance/digest/inbox/<Brisbane date>/Watchdog.md.
Local only: no network calls. Off switch: touch /workspace/watchdog/WATCHDOG_DISABLED
Exit code: 0 = all OK, 1 = problems found, 2 = watchdog itself broke.
"""
import argparse, datetime as dt, json, os, sys
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Australia/Brisbane")
ROOT = os.environ.get("WATCHDOG_ROOT", "/workspace/governance")

# (label, path template, due time HH:MM AEST, weekdays_only)
CHECKS = [
    ("Combined digest sent (Explorer 7:41am)", "digest/sent/{d}.md", "08:30", False),
    ("Scorer assessment (7:45am weekdays)", "assessments/{d}.md", "09:00", True),
    ("Scrutineer review (by 11:45am weekdays)", "reviews/{d}.md", "12:30", True),
]
INBOX = "digest/inbox/{d}"
INBOX_MIN_FILES = int(os.environ.get("WATCHDOG_INBOX_MIN", "5"))
INBOX_DUE = "10:00"
# Billing: any of these files existing = alert. A bot or Gem can drop a marker;
# the off-box version should instead rely on a missing heartbeat (dead man's switch).
BILLING_MARKERS = ["state/BILLING_FAILURE", "costs/BILLING_FAILURE"]
# (Keyword scanning of notes was tried and removed: it false-alarms on incident write-ups.)


def due_passed(now, hhmm):
    h, m = map(int, hhmm.split(":"))
    return now >= now.replace(hour=h, minute=m, second=0, microsecond=0)


def scheduler_status():
    """(ok, message). Used by run() and by --check-scheduler-only."""
    pidf = "/workspace/watchdog/scheduler.pid"
    alive = False
    try:
        pid = int(open(pidf).read().strip())
        alive = "scheduler.sh" in open(f"/proc/{pid}/cmdline").read()
    except (OSError, ValueError):
        pass
    if os.path.exists("/workspace/watchdog/SCHEDULER_DISABLED"):
        return True, "Scheduler: disabled by switch"
    if alive:
        return True, "Scheduler: running"
    return False, "SCHEDULER not running (watchdog/scheduler.pid dead or missing)"


def run(day, now):
    d = day.isoformat()
    weekday = day.weekday() < 5
    problems, ok = [], []
    for label, tmpl, due, wk_only in CHECKS:
        if wk_only and not weekday:
            continue
        p = os.path.join(ROOT, tmpl.format(d=d))
        if os.path.isfile(p) and os.path.getsize(p) > 0:
            ok.append(f"{label}: present")
        elif day < now.date() or due_passed(now, due):
            problems.append(f"MISSING {label}: {tmpl.format(d=d)}")
        else:
            ok.append(f"{label}: not due until {due}")
    ib = os.path.join(ROOT, INBOX.format(d=d))
    n = len([f for f in os.listdir(ib) if f.endswith(".md")]) if os.path.isdir(ib) else 0
    if n >= INBOX_MIN_FILES:
        ok.append(f"Digest inbox: {n} bot files")
    elif day < now.date() or due_passed(now, INBOX_DUE):
        problems.append(f"LOW Digest inbox {INBOX.format(d=d)}: {n} files (want >= {INBOX_MIN_FILES})")
    for m in BILLING_MARKERS:
        if os.path.exists(os.path.join(ROOT, m)):
            problems.append(f"BILLING marker present: {m}")
    # Staleness: newest file anywhere under ROOT (mtimes are weak evidence; see plan)
    newest = 0
    for dp, _, fs in os.walk(ROOT):
        for f in fs:
            try:
                newest = max(newest, os.path.getmtime(os.path.join(dp, f)))
            except OSError:
                pass
    age_h = (now.timestamp() - newest) / 3600
    if age_h > 26:
        problems.append(f"STALE: nothing under governance changed for {age_h:.0f} hours")
    sched_ok, sched_msg = scheduler_status()
    (ok if sched_ok else problems).append(sched_msg)
    # Disk space (snapshots are never pruned): warn under 15% or 5 GB free
    st = os.statvfs("/workspace")
    free = st.f_bavail * st.f_frsize; total = st.f_blocks * st.f_frsize
    pct = 100 * free / total if total else 0
    if pct < 15 or free < 5 * 1024**3:
        problems.append(f"DISK low on /workspace: {free/1024**3:.1f} GB free ({pct:.0f}%)")
    else:
        ok.append(f"Disk: {free/1024**3:.1f} GB free ({pct:.0f}%)")
    return {"date": d, "checked_at": now.isoformat(timespec="minutes"), "ok": ok, "problems": problems}


def alert(result, dry):
    """Append the result to the digest inbox (Brisbane date). Governance-relative paths only."""
    now = dt.datetime.now(TZ)
    lines = result["problems"] or ["all checks OK"]
    tag = "Urgent" if result["problems"] else "FYI"
    entry = f"- {tag} ({now:%H:%M} AEST, checking {result['date']}): " + "; ".join(lines) + "\n"
    inbox = os.path.join(ROOT, "digest/inbox", now.date().isoformat())
    out = os.path.join(inbox, "Watchdog.md")
    if dry:
        print(f"[dry-run] would append to {out}:\n{entry}", end="")
        return
    os.makedirs(inbox, exist_ok=True)
    new = not os.path.exists(out)
    with open(out, "a", encoding="utf-8") as f:
        if new:
            f.write(f"# Watchdog, {now.date().isoformat()}\n")
        f.write(entry)
    print(f"appended to {out}")
    # ledger event (best effort)
    try:
        sys.path.insert(0, "/workspace/governance/ledger")
        import ledger
        ledger.append("Watchdog", "watchdog_ok" if not result["problems"] else "watchdog_alert", "digest/inbox/" + now.date().isoformat() + "/Watchdog.md")
    except Exception as e:
        print(f"ledger append skipped: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--date")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check-scheduler-only", action="store_true",
                    help="only check the scheduler loop; print result, exit 0/1; writes nothing")
    a = ap.parse_args()
    if a.check_scheduler_only:
        if os.path.exists("/workspace/watchdog/WATCHDOG_DISABLED"):
            print("DISABLED: watchdog off switch is set"); return 2
        # exit 0 = running, 1 = DOWN (alert appended to Watchdog.md), 2 = DISABLED by switch
        if os.path.exists("/workspace/watchdog/SCHEDULER_DISABLED"):
            print("DISABLED: scheduler off switch is set"); return 2
        good, msg = scheduler_status(); print(msg)
        if not good:
            now = dt.datetime.now(TZ)
            alert({"date": now.date().isoformat(), "problems": [msg]}, a.dry_run)
        return 0 if good else 1
    if os.path.exists("/workspace/watchdog/WATCHDOG_DISABLED"):
        print("watchdog disabled"); return 0
    now = dt.datetime.now(TZ)
    day = dt.date.fromisoformat(a.date) if a.date else now.date()
    try:
        r = run(day, now)
    except Exception as e:  # watchdog failure is itself an alert
        r = {"date": day.isoformat(), "ok": [], "problems": [f"WATCHDOG ERROR: {type(e).__name__}"]}
        alert(r, a.dry_run)
        return 2
    print(json.dumps(r, indent=2) if a.json else "\n".join(["OK  " + x for x in r["ok"]] + ["BAD " + x for x in r["problems"]]))
    alert(r, a.dry_run)
    return 1 if r["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env bash
# Scheduler loop (this box has no cron and no systemd --user).
# Runs watchdog at 09:30 and 21:30 AEST, snapshot at 02:00 AEST.
# Each slot has a 15-minute catch-up window (09:30-09:44, 21:30-21:44, 02:00-02:14)
# so a brief freeze/restore that skips the exact minute still fires once.
# Start: nohup /workspace/watchdog/scheduler.sh >> /workspace/watchdog/scheduler.log 2>&1 &
# Off:   touch /workspace/watchdog/SCHEDULER_DISABLED   (loop exits within 20 s)
# Not reboot-safe: re-run the Start line after a box restart (cron/crontab absent on this box).
export TZ=Australia/Brisbane
export PYTHONDONTWRITEBYTECODE=1
D=/workspace/watchdog
echo $$ > $D/scheduler.pid
echo "$(date -Iseconds) scheduler started pid $$"
last=""
while true; do
  [ -e $D/SCHEDULER_DISABLED ] && { echo "$(date -Iseconds) disabled, exiting"; exit 0; }
  hm="$(date +%H:%M)"
  due=""
  case $hm in
    09:3[0-9]|09:4[0-4]) due="09:30" ;;
    21:3[0-9]|21:4[0-4]) due="21:30" ;;
    02:0[0-9]|02:1[0-4]) due="02:00" ;;
  esac
  if [ -n "$due" ]; then
    slot="$(date +%F) $due"
    if [ "$slot" != "$last" ]; then
      last="$slot"
      case $due in
        09:30|21:30) echo "$(date -Iseconds) watchdog"; [ -e $D/WATCHDOG_DISABLED ] || python3 $D/watchdog.py ; $D/heartbeat.sh ;;
        02:00) echo "$(date -Iseconds) snapshot"; python3 $D/snapshot.py ;;
      esac
    fi
  fi
  sleep 20
done

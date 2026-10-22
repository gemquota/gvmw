#!/usr/bin/env bash
# Scheduler loop (this box has no cron and no systemd --user).
# Runs watchdog at 09:30 and 21:30 AEST, snapshot at 02:00 AEST.
# Start: nohup /workspace/watchdog/scheduler.sh >> /workspace/watchdog/scheduler.log 2>&1 &
# Off:   touch /workspace/watchdog/SCHEDULER_DISABLED   (loop exits within 20 s)
# Not reboot-safe: re-run the Start line after a box restart.
export TZ=Australia/Brisbane
export PYTHONDONTWRITEBYTECODE=1
D=/workspace/watchdog
echo $$ > $D/scheduler.pid
echo "$(date -Iseconds) scheduler started pid $$"
last=""
while true; do
  [ -e $D/SCHEDULER_DISABLED ] && { echo "$(date -Iseconds) disabled, exiting"; exit 0; }
  slot="$(date +%F) $(date +%H:%M)"
  if [ "$slot" != "$last" ]; then
    case ${slot#* } in
      09:30|21:30) last="$slot"; echo "$(date -Iseconds) watchdog"; [ -e $D/WATCHDOG_DISABLED ] || python3 $D/watchdog.py ;;
      02:00) last="$slot"; echo "$(date -Iseconds) snapshot"; python3 $D/snapshot.py ;;
    esac
  fi
  sleep 20
done

#!/bin/bash
# Pushes a UTC heartbeat to private gemquota/box-heartbeat. Off switch: touch /workspace/watchdog/HEARTBEAT_DISABLED
[ -e /workspace/watchdog/HEARTBEAT_DISABLED ] && exit 0
cd /workspace/box-heartbeat || exit 1
date -u +%Y-%m-%dT%H:%M:%SZ > heartbeat.txt
git -c user.name=gemquota -c user.email=gemquota@users.noreply.github.com commit -qam "heartbeat" || exit 0
git -c credential.helper= -c 'credential.helper=!f(){ echo username=gemquota; echo "password=$(/usr/local/bin/gh auth token --user gemquota)"; }; f' push -q origin main

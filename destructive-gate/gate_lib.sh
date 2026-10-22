#!/usr/bin/env bash
# Shared approval check. Token file: $GATE_DIR/approvals/<sha256-of-action>.token
# Token contents (key: value lines):
#   action_sha256: <hash of the exact command string>
#   action: <exact command, for humans>
#   approved_by_gem: <Gem's words + where/when>
#   safeguard_dryrun: <path to Safeguard dry-run record>
#   expires: <ISO 8601 with +10:00>
# A token is single use: the gate renames it to .used after the action runs.
GATE_DIR="${GATE_DIR:-/workspace/destructive-gate}"
gate_hash() { printf '%s' "$1" | sha256sum | cut -d' ' -f1; }
gate_check() {  # $1 = exact action string
  local h tok exp now
  h=$(gate_hash "$1"); tok="$GATE_DIR/approvals/$h.token"
  if [ ! -f "$tok" ]; then
    echo "GATE: blocked. No approval token for this exact action." >&2
    echo "GATE: action sha256 = $h" >&2
    echo "GATE: needs Safeguard dry run + Gem's approval -> $tok" >&2
    return 1
  fi
  for k in action_sha256 approved_by_gem safeguard_dryrun expires; do
    grep -q "^$k: ..*" "$tok" || { echo "GATE: token missing '$k'" >&2; return 1; }
  done
  grep -q "^action_sha256: $h\$" "$tok" || { echo "GATE: token hash mismatch" >&2; return 1; }
  exp=$(sed -n 's/^expires: //p' "$tok"); now=$(date +%s)
  [ "$(date -d "$exp" +%s 2>/dev/null || echo 0)" -gt "$now" ] || { echo "GATE: token expired" >&2; return 1; }
  local dr; dr=$(sed -n 's/^safeguard_dryrun: //p' "$tok")
  [ -f "$dr" ] || { echo "GATE: Safeguard dry-run record not found: $dr" >&2; return 1; }
  echo "GATE: approved ($h)" >&2; return 0
}
gate_consume() { local h; h=$(gate_hash "$1"); mv "$GATE_DIR/approvals/$h.token" "$GATE_DIR/approvals/$h.used" 2>/dev/null; true; }
gate_log() { mkdir -p "$GATE_DIR/log"; printf '%s\t%s\t%s\n' "$(date -Iseconds)" "$1" "$2" >> "$GATE_DIR/log/gate.log"; }

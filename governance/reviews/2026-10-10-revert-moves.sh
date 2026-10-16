#!/usr/bin/env bash
# Revert the 10 Oct 2026 /workspace organise moves (Grok Bot executor for Gem).
# Reads 2026-10-10-workspace-moves.tsv and moves each new_path back to old_path.
# Safe: never overwrites (mv -n), skips if old path already exists or new path is missing.
# Also restores the reference edits from /workspace/_archive/pre-move-edits/ (cp, keeps the copies).
# Created folders (bie_tools/_runlogs, bie_tools/scripts, bie_tools/_history, medb-research,
# governance/_archive) are left in place; remove them by hand with rmdir once empty if wanted.
# Usage: bash 2026-10-10-revert-moves.sh [--dry-run]
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
MANIFEST="$HERE/2026-10-10-workspace-moves.tsv"
EDITS=/workspace/_archive/pre-move-edits
DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1
run(){ if [ $DRY = 1 ]; then echo "DRY: $*"; else "$@"; fi; }
# 1) restore edited files first (while they are still at the paths recorded in index.tsv): each .pre-move copy records its original absolute path in EDITS/index.tsv
if [ -f "$EDITS/index.tsv" ]; then
  while IFS=$'\t' read -r orig copy; do
    [ -z "$orig" ] && continue
    run cp -p "$copy" "$orig" && echo "restored edit: $orig"
  done < "$EDITS/index.tsv"
fi
# 2) move everything back, newest first
tail -n +2 "$MANIFEST" | tac | while IFS=$'\t' read -r old new ts; do
  [ -z "$old" ] && continue
  # a symlink left at the old path (pointing to new) is moved aside first
  if [ -L "$old" ] && [ "$(readlink -f "$old")" = "$(readlink -f "$new")" ]; then
    run mv -n "$old" "$old.revert-symlink"; echo "moved aside symlink $old -> $old.revert-symlink"
  fi
  if [ -e "$old" ]; then echo "SKIP (old path exists): $old"; continue; fi
  if [ ! -e "$new" ]; then echo "SKIP (new path missing): $new"; continue; fi
  run mkdir -p "$(dirname "$old")"
  run mv -n "$new" "$old" && echo "reverted: $new -> $old"
done

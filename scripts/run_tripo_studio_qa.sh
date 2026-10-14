#!/usr/bin/env bash
# Offline QA of a Tripo Studio export. Does not call Tripo API or generate assets.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
/Volumes/CLOVERWOOD_DEV/Tools/require-dev-disk.sh
BLENDER=/opt/homebrew/bin/blender
[[ -x "$BLENDER" ]] || { echo "Blender missing: $BLENDER" >&2; exit 2; }
[[ "$ROOT" == /Volumes/CLOVERWOOD_DEV/* ]] || { echo "Run from the verified dev disk" >&2; exit 2; }
export TMPDIR=/Volumes/CLOVERWOOD_DEV/Caches
export CLOVERWOOD_REPO_ROOT="$ROOT"
export CLOVERWOOD_REPO_NAME=CODEX-GAME-DEV-03
export CLOVERWOOD_RUN_ID="TSQA-$(date +%H%M%S)-$$"
export CLOVERWOOD_EXCLUSIVE_MAC=1
exec bash "$ROOT/scripts/cloverwood-local-run.sh" -- \
  "$BLENDER" --background --factory-startup --disable-autoexec \
  --python-exit-code 2 --python "$ROOT/scripts/blender_studio_asset_qa.py" -- "$@"

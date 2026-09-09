#!/usr/bin/env bash
set -u
set -o pipefail
if [ "${1:-}" = "--" ]; then shift; fi
if [ "$#" -eq 0 ]; then echo "usage: cloverwood-local-run.sh -- <command> [args...]" >&2; exit 64; fi
umask 077
REPO_ROOT="${CLOVERWOOD_REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
REPO_NAME="${CLOVERWOOD_REPO_NAME:-$(basename "$REPO_ROOT")}"
BASE_TMP="${TMPDIR:-/tmp}"; BASE_TMP="${BASE_TMP%/}"
RUN_ID="${CLOVERWOOD_RUN_ID:-$(date -u +%Y%m%dT%H%M%SZ)-$$}"
REPO_RUN_BASE="$BASE_TMP/cloverwood-ci/$REPO_NAME"; RUN_ROOT="$REPO_RUN_BASE/$RUN_ID"
MIN_FREE_GIB="${CLOVERWOOD_MIN_FREE_GIB:-20}"; EXCLUSIVE_MAC="${CLOVERWOOD_EXCLUSIVE_MAC:-0}"
LOCK_DIR="$BASE_TMP/cloverwood-ci/.mac-heavy.lock"; LOCK_OWNED=0
free_kib() { df -Pk "$BASE_TMP" | awk 'NR==2 {print $4}'; }
BEFORE_KIB="$(free_kib)"; REQUIRED_KIB=$((MIN_FREE_GIB * 1024 * 1024))
if [ "$BEFORE_KIB" -lt "$REQUIRED_KIB" ]; then echo "CLOVERWOOD_RUN_BLOCKED reason=low_disk free_kib=$BEFORE_KIB required_kib=$REQUIRED_KIB repo=$REPO_NAME" >&2; exit 78; fi
mkdir -p "$REPO_RUN_BASE"
for stale in "$REPO_RUN_BASE"/*; do
  [ -d "$stale" ] || continue
  [ "$(find "$stale" -prune -mmin +1440 -print 2>/dev/null)" ] || continue
  stale_pid="$(cat "$stale/.owner-pid" 2>/dev/null || true)"
  if [ -n "$stale_pid" ] && kill -0 "$stale_pid" 2>/dev/null; then continue; fi
  rm -rf -- "$stale"
done
if [ "$EXCLUSIVE_MAC" = "1" ]; then
  mkdir -p "$(dirname "$LOCK_DIR")"
  if ! mkdir "$LOCK_DIR" 2>/dev/null; then echo "CLOVERWOOD_RUN_BLOCKED reason=mac_busy lock=$LOCK_DIR repo=$REPO_NAME" >&2; exit 75; fi
  LOCK_OWNED=1; printf '%s\n' "$$" > "$LOCK_DIR/pid"
fi
mkdir -p "$RUN_ROOT/tmp" "$RUN_ROOT/DerivedData" "$RUN_ROOT/swiftpm" "$RUN_ROOT/results"; printf '%s\n' "$$" > "$RUN_ROOT/.owner-pid"
export CLOVERWOOD_RUN_ROOT="$RUN_ROOT" CLOVERWOOD_DERIVED_DATA_PATH="$RUN_ROOT/DerivedData" CLOVERWOOD_SWIFTPM_SCRATCH_PATH="$RUN_ROOT/swiftpm" CLOVERWOOD_RESULT_BUNDLE_PATH="$RUN_ROOT/results/TestResults.xcresult" TMPDIR="$RUN_ROOT/tmp/"
cleanup() {
  status=$?; trap - EXIT INT TERM HUP; cleanup_state=PASS
  chmod -R u+w "$RUN_ROOT" 2>/dev/null || true; rm -rf -- "$RUN_ROOT" 2>/dev/null || cleanup_state=FAIL; [ ! -e "$RUN_ROOT" ] || cleanup_state=FAIL
  if [ "$LOCK_OWNED" = "1" ]; then rm -rf -- "$LOCK_DIR" 2>/dev/null || cleanup_state=FAIL; fi
  after_kib="$(free_kib 2>/dev/null || echo 0)"; echo "CLOVERWOOD_CLEANUP_RECEIPT repo=$REPO_NAME run_id=$RUN_ID command_exit=$status cleanup=$cleanup_state free_before_kib=$BEFORE_KIB free_after_kib=$after_kib"
  if [ "$cleanup_state" != "PASS" ]; then exit 86; fi; exit "$status"
}
trap cleanup EXIT; trap 'exit 130' INT; trap 'exit 143' TERM; trap 'exit 129' HUP
echo "CLOVERWOOD_RUN_START repo=$REPO_NAME run_id=$RUN_ID run_root=$RUN_ROOT free_before_kib=$BEFORE_KIB"
"$@"

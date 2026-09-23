#!/usr/bin/env bash
# Cooperative foreground-job wrapper; compatible with macOS /bin/bash 3.2.
set -u
set -o pipefail
if [ "${1:-}" = "--" ]; then shift; fi
if [ "$#" -eq 0 ]; then echo "usage: cloverwood-local-run.sh -- <command> [args...]" >&2; exit 64; fi
umask 077
REPO_ROOT="${CLOVERWOOD_REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
REPO_NAME="${CLOVERWOOD_REPO_NAME:-$(basename "$REPO_ROOT")}"
# Do not expose a configurable shared-lock root: callers must agree on this root.
SYSTEM_TMP=/tmp
BASE_TMP="${TMPDIR:-/tmp}"
RUN_ID="${CLOVERWOOD_RUN_ID:-$(date -u +%Y%m%dT%H%M%SZ)-$$}"
MIN_FREE_GIB="${CLOVERWOOD_MIN_FREE_GIB:-20}"
EXCLUSIVE_MAC="${CLOVERWOOD_EXCLUSIVE_MAC:-0}"
BEFORE_KIB=0; RUN_ROOT_OWNED=0; RUN_MARKED=0
RUN_ROOT=""; REPO_RUN_BASE=""
OWNED_LOCKS=(); MARKED_LOCKS=(); LOCK_PATHS=()

blocked() { echo "CLOVERWOOD_RUN_BLOCKED reason=$1 repo=$REPO_NAME" >&2; exit "$2"; }
free_kib() { df -Pk "$BASE_TMP" | awk 'NR==2 {print $4}'; }
segment_ok() {
  case "$1" in ""|.*|*[!A-Za-z0-9._-]*) return 1 ;; esac
  [ "${#1}" -le 128 ]
}
owned_marker() {
  [ -d "$1" ] && [ ! -L "$1" ] && [ -O "$1" ] &&
    [ -f "$1/$2" ] && [ ! -L "$1/$2" ] && [ "$(cat "$1/$2" 2>/dev/null)" = "$$" ]
}
remove_run() {
  # Only trusted disposable, owner-marked directories under this repo namespace.
  [ ! -L "$BASE_TMP/cloverwood-ci" ] && [ ! -L "$REPO_RUN_BASE" ] &&
    [ -d "$1" ] && [ ! -L "$1" ] && [ -O "$1" ] || return 1
  # Unlinking needs directory access, not writable file contents. Never chmod
  # regular files: a disposable hard link can share an inode with source/cache.
  # Preorder, non-following traversal opens each directory before descending.
  find -P "$1" -type d -exec chmod u+rwx {} \; 2>/dev/null || return 1
  rm -rf -- "$1" || return 1
  [ ! -e "$1" ] && [ ! -L "$1" ]
}
cleanup() {
  status=$?; trap - EXIT; trap '' INT TERM HUP
  cleanup_state=PASS
  if [ "$RUN_ROOT_OWNED" = 1 ]; then
    if [ "$RUN_MARKED" = 1 ] && owned_marker "$RUN_ROOT" .owner-pid; then
      remove_run "$RUN_ROOT" || cleanup_state=FAIL
    elif [ "$RUN_MARKED" = 0 ] && [ ! -L "$RUN_ROOT" ]; then
      rmdir "$RUN_ROOT" 2>/dev/null || cleanup_state=FAIL
    else cleanup_state=FAIL; fi
  fi
  for owned in "${OWNED_LOCKS[@]-}"; do
    [ -n "$owned" ] || continue
    was_marked=0
    for marked in "${MARKED_LOCKS[@]-}"; do
      [ "$owned" != "$marked" ] || was_marked=1
    done
    if owned_marker "$owned" pid; then
      # Never recursively remove locks, unknown contents, or another owner.
      rm -f -- "$owned/pid" && rmdir "$owned" 2>/dev/null || cleanup_state=FAIL
    elif [ "$was_marked" = 0 ] && [ -d "$owned" ] && [ ! -L "$owned" ] &&
         [ -O "$owned" ] && [ ! -e "$owned/pid" ] && [ ! -L "$owned/pid" ]; then
      # Only pre-marker setup failure permits empty-directory rollback. A PID
      # disappearing after successful marking is lost ownership, never success.
      rmdir "$owned" 2>/dev/null || cleanup_state=FAIL
    else cleanup_state=FAIL; fi
  done
  after_kib="$(free_kib 2>/dev/null || echo 0)"
  echo "CLOVERWOOD_CLEANUP_RECEIPT repo=$REPO_NAME run_id=$RUN_ID command_exit=$status cleanup=$cleanup_state free_before_kib=$BEFORE_KIB free_after_kib=$after_kib"
  [ "$cleanup_state" = PASS ] || exit 86
  exit "$status"
}
# Install traps before acquiring locks or creating any run-owned directory.
trap cleanup EXIT
trap 'exit 130' INT; trap 'exit 143' TERM; trap 'exit 129' HUP
segment_ok "$REPO_NAME" && segment_ok "$RUN_ID" || blocked invalid_identifier 64
case "$MIN_FREE_GIB" in ""|*[!0-9]*) blocked invalid_disk_threshold 64 ;; esac
[ "${#MIN_FREE_GIB}" -le 6 ] || blocked invalid_disk_threshold 64
case "$EXCLUSIVE_MAC" in 0|1) ;; *) blocked invalid_exclusive_flag 64 ;; esac
case "$BASE_TMP" in /*) ;; *) blocked invalid_tmpdir 64 ;; esac
BASE_TMP="$(cd "$BASE_TMP" 2>/dev/null && pwd -P)" || blocked invalid_tmpdir 73
[ "$BASE_TMP" != / ] || blocked invalid_tmpdir 64
BEFORE_KIB="$(free_kib)" || blocked disk_probe_failed 78
case "$BEFORE_KIB" in ""|*[!0-9]*) blocked disk_probe_failed 78 ;; esac
REQUIRED_KIB=$((10#$MIN_FREE_GIB * 1024 * 1024))
[ "$BEFORE_KIB" -ge "$REQUIRED_KIB" ] || blocked low_disk 78
CANONICAL_TMP="$(getconf DARWIN_USER_TEMP_DIR 2>/dev/null || printf '%s' "$SYSTEM_TMP")"
[ -n "$CANONICAL_TMP" ] || CANONICAL_TMP="$SYSTEM_TMP"
REPO_RUN_BASE="$BASE_TMP/cloverwood-ci/$REPO_NAME"
RUN_ROOT="$REPO_RUN_BASE/$RUN_ID"
for parent in "$BASE_TMP/cloverwood-ci" "$REPO_RUN_BASE"; do
  [ ! -L "$parent" ] || blocked unsafe_run_parent 73
  mkdir -p "$parent" || blocked run_parent_failed 73
  [ -O "$parent" ] || blocked foreign_run_parent 73
done
# An existing requested run must never be reused, swept or overwritten.
[ ! -e "$RUN_ROOT" ] && [ ! -L "$RUN_ROOT" ] || blocked run_id_exists 73

# Sweep only old, same-user, marked, dead-owner run directories. Never guess at
# an unknown directory or an orphaned heavy lock; SIGKILL needs operator review.
locks_present=0
for lock_base in "$SYSTEM_TMP" "$CANONICAL_TMP" "$BASE_TMP"; do
  candidate="${lock_base%/}/cloverwood-ci/.mac-heavy.lock"
  if [ -e "$candidate" ] || [ -L "$candidate" ]; then locks_present=1; fi
done
if [ "$locks_present" = 0 ]; then
  for stale in "$REPO_RUN_BASE"/*; do
    [ -d "$stale" ] && [ ! -L "$stale" ] && [ -O "$stale" ] || continue
    [ -f "$stale/.owner-pid" ] && [ ! -L "$stale/.owner-pid" ] || continue
    [ "$(find "$stale" -prune -mmin +1440 -print 2>/dev/null)" ] || continue
    stale_pid="$(cat "$stale/.owner-pid" 2>/dev/null)"
    case "$stale_pid" in ""|0|*[!0-9]*) continue ;; esac
    [ "${#stale_pid}" -le 10 ] && [ "$stale_pid" -le 2147483647 ] || continue
    kill -0 "$stale_pid" 2>/dev/null && continue
    remove_run "$stale" || blocked stale_cleanup_failed 86
  done
fi

if [ "$EXCLUSIVE_MAC" = 1 ]; then
  # SPLIT-compatible order: common /tmp first, macOS user temp, caller temp.
  # Canonical physical paths deduplicate /tmp vs /private/tmp and trailing '/'.
  for lock_base in "$SYSTEM_TMP" "$CANONICAL_TMP" "$BASE_TMP"; do
    case "$lock_base" in /*) ;; *) blocked lock_parent_failed 73 ;; esac
    lock_base="$(cd "$lock_base" 2>/dev/null && pwd -P)" || blocked lock_parent_failed 73
    [ "$lock_base" != / ] || blocked lock_parent_failed 73
    lock_parent="$lock_base/cloverwood-ci"
    [ ! -L "$lock_parent" ] || blocked unsafe_lock_parent 73
    mkdir -p "$lock_parent" || blocked lock_parent_failed 73
    candidate="$lock_parent/.mac-heavy.lock"
    duplicate=0
    for existing in "${LOCK_PATHS[@]-}"; do [ "$candidate" != "$existing" ] || duplicate=1; done
    [ "$duplicate" = 1 ] || LOCK_PATHS+=("$candidate")
  done
  for candidate in "${LOCK_PATHS[@]-}"; do
    if ! mkdir "$candidate" 2>/dev/null; then
      # Recover only an unambiguous lock whose sole numeric owner PID is dead.
      stale_pid=""
      if [ -d "$candidate" ] && [ ! -L "$candidate" ] && [ -O "$candidate" ] &&
         [ -f "$candidate/pid" ] && [ ! -L "$candidate/pid" ] &&
         [ "$(find "$candidate" -mindepth 1 -maxdepth 1 -print 2>/dev/null | wc -l | tr -d ' ')" = 1 ]; then
        stale_pid="$(cat "$candidate/pid" 2>/dev/null)"
      fi
      case "$stale_pid" in ""|0|*[!0-9]*) stale_pid="" ;; esac
      if [ -n "$stale_pid" ] && [ "${#stale_pid}" -le 10 ] && [ "$stale_pid" -le 2147483647 ] &&
         ! kill -0 "$stale_pid" 2>/dev/null; then
        rm -f -- "$candidate/pid" && rmdir "$candidate" 2>/dev/null || blocked stale_lock_cleanup_failed 86
        echo "CLOVERWOOD_STALE_LOCK_RECOVERED lock=$candidate dead_pid=$stale_pid repo=$REPO_NAME" >&2
        mkdir "$candidate" 2>/dev/null || blocked lock_reacquire_failed 75
      else
        echo "CLOVERWOOD_RUN_BLOCKED reason=mac_busy lock=$candidate repo=$REPO_NAME" >&2
        exit 75
      fi
    fi
    # Register immediately, so partial acquisition is rolled back on failure.
    OWNED_LOCKS+=("$candidate")
    printf '%s\n' "$$" > "$candidate/pid" || blocked lock_marker_failed 73
    MARKED_LOCKS+=("$candidate")
  done
fi

# mkdir, not mkdir -p: two invocations with the same explicit ID cannot share it.
mkdir "$RUN_ROOT" 2>/dev/null || blocked run_id_exists 73
RUN_ROOT_OWNED=1
printf '%s\n' "$$" > "$RUN_ROOT/.owner-pid" || blocked run_marker_failed 73
RUN_MARKED=1
mkdir "$RUN_ROOT/tmp" "$RUN_ROOT/DerivedData" "$RUN_ROOT/swiftpm" "$RUN_ROOT/results" || blocked run_setup_failed 73
export CLOVERWOOD_RUN_ROOT="$RUN_ROOT" CLOVERWOOD_DERIVED_DATA_PATH="$RUN_ROOT/DerivedData" CLOVERWOOD_SWIFTPM_SCRATCH_PATH="$RUN_ROOT/swiftpm" CLOVERWOOD_RESULT_BUNDLE_PATH="$RUN_ROOT/results/TestResults.xcresult" TMPDIR="$RUN_ROOT/tmp/"
echo "CLOVERWOOD_RUN_START repo=$REPO_NAME run_id=$RUN_ID run_root=$RUN_ROOT free_before_kib=$BEFORE_KIB"
# Foreground wait is intentional. A signal sent ONLY to this shell is deferred
# until its foreground command returns: do not unlock while that child runs.
# For immediate cancellation, terminate the invocation's dedicated process group.
# Detached/daemonized descendants are outside this cooperative wrapper contract.
"$@"

# Shared Mac heavy-job lock — library adoption

Reviewed: 2026-09-22

## Scope and provenance

Owner-approved bounded step: adapt the existing SPLIT lock protocol into this
library, add lightweight process tests, and preserve safe cleanup. No scheduler,
new service, dependency install, model, Viewer or game change is included.

Library baseline: `8d9468cd159b6983ab2eefc60bd0db740995a5d3` (PR #3).
Source reference: `cloverwoodstudio/SPLIT`, `scripts/cloverwood-local-run.sh`,
Git blob `aa89add520d291ce0234d9186e4637965d7d16fc`. This blob was fetched read-only
and verified for the actual Mac interoperability smoke test. The code here adapts
that protocol; it is not a claim that every game wrapper has been updated.

## What changes

The caller's TMPDIR still selects its disposable workspace. Heavy jobs now acquire
three compatible lock locations in a fixed order: `/tmp/cloverwood-ci/.mac-heavy.lock`,
the macOS per-user temporary directory's equivalent, then the caller's equivalent.
Physical path normalization removes duplicate locations (including `/private/tmp`).
All upgraded callers contend for the first common lock even with different TMPDIRs.
Existing SPLIT callers share the protocol; legacy callers using the common or
canonical-user temp location are covered. Old wrappers using arbitrary *other*
custom temp roots remain a migration gap, not silently protected.

- Atomic mkdir claims each lock; another owner/unknown/orphaned lock blocks with 75.
- Partial lock acquisition releases only locations acquired by this invocation.
- Cleanup checks PID ownership, does not recursively delete locks, and fails if
  ownership changes, a previously written PID marker disappears, or unexpected
  lock contents prevent removal. Empty-lock rollback is limited to pre-marker
  setup failure; missing evidence later is never treated as permission to unlock.
- A run ID must be a safe path component and a new directory, claimed atomically.
  Existing IDs and symlink roots are never reused or removed as this run's output.
- Cleanup is registered before locks/run directories. Child exit status is preserved
  unless cleanup fails (86). Low disk blocks before execution (78), retaining the
  default 20 GiB floor. Invalid configuration exits 64; setup/collision exits 73.
- Cleanup adjusts access only on real directories before traversal, not regular
  files. Hard-linked source/cache files retain their permission bits; symlink
  targets are not followed. Nested no-access disposable directories can be removed.
- The existing exports for DerivedData, SwiftPM, test results and TMPDIR remain.
- Only same-user, old, marked, dead-owner run directories can be swept. Unknown,
  malformed, symlink and live-owner directories remain untouched. Existing heavy
  locks suspend the stale sweep; no automatic orphaned-lock deletion is introduced.

The reusable empty `cloverwood-ci/<repo>` parents may remain. Disposable *run*
directories must be gone after successful cleanup; intentional receipts remain
in the repository. Each run prints the before/after free-space and cleanup receipt.

## Signals and honest limits

This is a cooperative foreground-command wrapper, not a process supervisor or
security sandbox. A signal sent only to Bash is deferred while the foreground
command runs; that deliberately prevents premature unlock. For immediate
cancellation, run the invocation in its own process group and signal that group,
not a shared terminal/CI group. The foreground command must finish/reap its own
children before returning; this shell does not supervise signal-ignoring descendants.
Tests cover TERM, HUP and INT after child startup.

SIGKILL, host crash or power loss cannot execute a shell trap. The orphaned lock
therefore remains and prevents a new heavy job from proceeding. Inspect the exact
recorded owner and its still-running children before authorized targeted recovery;
a dead wrapper PID alone is not permission to erase its lock/workspace. Do not
use broad pkill, remove all locks, or clear global caches to get a PASS.

Commands that detach or daemonize children are outside this foreground contract.
Unwrapped processes, older incompatible wrappers, different users unable to access
shared locks, and hostile modification by another process are not magically
controlled. Locking and PID markers are coordination, not authentication.

## Verification

`tests/test_local_run.py` executes real small Bash/Python processes, not Xcode or
Blender. Its private script copy replaces only the fixed system-temp path; fixture
getconf/df/mkdir commands provide isolated canonical paths, disk values and setup
failure. There is no configurable production shared-lock-root bypass.

Tests exercise contention across TMPDIRs and repo names, compatibility occupancy,
partial rollback, path aliases, successful/error exits, signal cancellation,
wrapper-only termination, SIGKILL orphan blocking, source/lock ownership changes,
run-ID collisions, low disk, symlink containment and bounded stale cleanup.

Local invocation:

```sh
bash scripts/cloverwood-local-run.sh -- python3 -B -m unittest discover -s tests -p test_local_run.py -v
```

The existing registry workflow runs the complete tests on Linux. A small
[macOS workflow](../.github/workflows/local-run.yml) also checks the wrapper using
the existing hosted-macOS convention; it uses the wrapper for its temporary files.
The separately observed smoke test used the *unmodified production-root* wrapper
on the authorized Mac and the exact pinned SPLIT script. It reproduced the old
bug, blocked both new and SPLIT contenders, then allowed SPLIT after release.

Source checks and CI do not authorize merge, deployment or rolling this change
out to additional repositories. Review the exact PR head and its evidence first.

Retained local observations: [validation receipt](evidence/shared-mac-lock-2026-09-22.json).

Additional review regressions and corrections: [PR #4 review](pr4-review-2026-09-22.md).

# DIRECT_QA_CONTRACT — Swift Testing and Swift concurrency

**Reviewed:** 2026-10-13. **Status:** DRAFT, companion to [SKILL.md](../SKILL.md). No authorization to change any Apple product. The existing [Apple-platform skill](../../apple-platform-development/SKILL.md) governs toolchain and device/release routing.

## Mandatory report

```text
TICKET / OWNER APPROVAL / GAME_OR_APP / AUTHORITY:
SOURCE_REPO + MAIN_SHA / CANDIDATE_HEAD / WORKTREE_CLEAN:
TARGET_NAME / SWIFT_VERSION / XCODE_VERSION / PACKAGE_TOOLS_VERSION:
ACTOR_ISOLATION_DEFAULT / SWIFT_STRICT_CONCURRENCY / SWIFT_COMPILER_FLAGS:
ROUTE: SWIFT_TESTING | XCODE_TEST | XCTEST_UI | CONCURRENCY_DIAGNOSIS
FILES_IN_SCOPE / BEFORE_AFTER_DIFF:
POSITIVE / NEGATIVE / CANCELLATION / REENTRANCY:
COMMAND / EXIT_CODE / TEST_COUNT / COMPILER_ERRORS / WARNINGS:
SWIFT_TESTS: PASS | FAIL | NOT_RUN
CONCURRENCY_CHECK: PASS | FAIL | NOT_RUN
XCODE_OR_SIMULATOR: PASS | FAIL | NOT_RUN
PHYSICAL_DEVICE: PASS | FAIL | NOT_RUN
LOGS / XCTEST_XCRESULT / TOOLCHAIN_AND_SOURCE_HASHES:
DISK_PREFLIGHT / EXCLUSIVE_LOCK / CLEANUP_RECEIPT:
LIMITATIONS / INDEPENDENT_REVIEW / STOP:
```

Use source/version-appropriate commands, not guessed settings:

- Swift package: `swift --version`, inspect `Package.swift` and target settings, then `swift test --scratch-path "$CLOVERWOOD_RUN_ROOT/swiftpm"`.
- Xcode target: `xcodebuild -list` / `xcodebuild -showBuildSettings` and discover scheme/destination. Use reviewed signing-disabled commands if applicable; capture `.xcresult` and test exit status.
- Swift 6 **language mode** gives complete data-race checks. In Swift 5 compatibility mode, `SWIFT_STRICT_CONCURRENCY=complete` can expose warnings without changing product language mode. Never pretend the flag is required to turn strict checks on for Swift 6.
- `MainActor` default isolation can differ by target, Swift version and Xcode build settings; derive it from the build, not a blanket default.
- Test ordinary async return values by `await`; test callback *counts* with `confirmation` only when callback delivery completes **before the closure returns**. Never claim it awaits future callbacks for you.
- Swift Testing defaults to parallel tests; global mutable state may create suite-level interactions. A serialized suite does not provide cross-suite mutex semantics.
- `#expect` and `#require` have different control flow. Do not convert XCTest's UI automation/performance coverage just because `@Test` exists.

## Result-bundle retention before wrapper cleanup

The Mac wrapper **always deletes** its disposable `CLOVERWOOD_RUN_ROOT` after a run, even on failure. A `.xcresult` stored only inside that root is **NOT retained proof**. An authorized Xcode testing ticket must name an access-controlled evidence location on the development disk **outside that disposable root**, and approve the size/privacy classification of the bundle **before** running a potentially heavy test.

The following is a **command-shape example**, not a copy/paste invocation for an unknown app; discover the actual project, scheme and destination first. Run all of these steps **within the same wrapper invocation** so the failure bundle is copied **before cleanup** and the real test exit code survives:

```bash
# Before running: select a unique, owner-approved directory outside /tmp/cloverwood-ci.
# Create EVIDENCE_DIR under the authorized development disk with restricted access.
export EVIDENCE_DIR="/Volumes/CLOVERWOOD_DEV/QA_EVIDENCE/<repo>/<ticket>/<sha>"
test -d "$EVIDENCE_DIR" && test ! -L "$EVIDENCE_DIR"

bash scripts/cloverwood-local-run.sh -- bash -c '
  set -u
  source_bundle="$CLOVERWOOD_RUN_ROOT/results/ScopedTests.xcresult"
  # Use the *discovered* Xcode project/scheme/destination and explicit build flags.
  xcodebuild test -project "<actual>.xcodeproj" -scheme "<actual-scheme>" \
    -destination "<actual-destination>" \
    -derivedDataPath "$CLOVERWOOD_RUN_ROOT/DerivedData" \
    -resultBundlePath "$source_bundle"
  test_exit=$?
  # Preserve a FAILED test bundle too; never put this after `set -e` early exit.
  if test -d "$source_bundle"; then
    case "$EVIDENCE_DIR" in "$CLOVERWOOD_RUN_ROOT"|"$CLOVERWOOD_RUN_ROOT"/*)
      echo "EVIDENCE_FAIL: destination is disposable" >&2; exit 86 ;;
    esac
    target="$EVIDENCE_DIR/ScopedTests.xcresult"
    if test -e "$target" || test -L "$target"; then
      echo "EVIDENCE_FAIL: refuse evidence overwrite" >&2; exit 86
    fi
    ditto "$source_bundle" "$target" || exit 86
    test -d "$target" || exit 86
    xcrun xcresulttool get test-results summary --path "$target" \
      > "$EVIDENCE_DIR/ScopedTests-summary.json" || exit 86
    test -s "$EVIDENCE_DIR/ScopedTests-summary.json" || exit 86
    echo "XCRESULT_RETENTION_PASS $target"
  else
    echo "EVIDENCE_FAIL: no result bundle; retain bounded stderr/build log separately" >&2
    exit 86
  fi
  exit "$test_exit"
'
```

**Validation limits:** The placeholder command is not pre-approved for any real app. The evidence directory must be pre-created and independently validated against symlink/path traversal, disk capacity and sensitive data; never use a shared public folder for private logs. Prefer a per-run unique destination and hash/size receipt. The `xcodebuild` invocation above does not contain project-specific signing decisions. When `xcodebuild` returns nonzero, **retaining the bundle does not convert FAIL into PASS**. If the tool crashes before producing `.xcresult`, retain a bounded separate log, mark `EVIDENCE_FAIL / TEST_FAIL`, and never manufacture a bundle. Only the repo-approved `CLOVERWOOD_RUN_ROOT` is automatically cleaned; intentional evidence survives. Avoid overwriting previous evidence.

**Codex vs OpenCode skill discovery:** OpenCode's `opencode/autoinvoke: "false"` is an OpenCode metadata preference, **not a Codex skill-discovery control**. Codex may infer skill relevance from `name` / `description` even when it is DRAFT. Keep this skill only in the isolated pilot branch; direct Codex to load it only by exact user/owner request, and leave other projects on existing stable skills. This is a documented policy, not a guarantee of technical suppression of Codex's implicit selection.

## Static decision fixtures — expected, not runtime results

| ID | Scenario | Required decision |
| --- | --- | --- |
| ST01 | Target builds under Swift 5 mode; `-strict-concurrency=complete` emits diagnostics | Document warnings; no unapproved Swift 6 migration |
| ST02 | Swift 6 target fails on non-Sendable crossing an actor boundary | Compiler FAIL; do not add `@unchecked Sendable` without proof |
| ST03 | `@Test` uses `Task.sleep` to wait for callback race | Reject as flaky; introduce observable completion/injected clock |
| ST04 | `confirmation` closure returns before callback is delivered | FAIL or redesign test; it does not wait |
| ST05 | `#expect` failure followed by unsafe optional dereference | Change to `try #require` where appropriate; preserve test intent |
| ST06 | `@Suite(.serialized)` protects one suite while sibling suite shares mutable global | NOT safe across suites; isolate state |
| ST07 | Simulator test PASS, iPhone not exercised | DEVICE=NOT_RUN; never claim iPhone acceptance |
| ST08 | Task canceled after a newer request starts; older response overwrites current UI | Regression FAIL; require stale-completion guard and explicit task ownership |
| ST09 | `swift test` returns 0 but log contains a Swift Testing issue treated as known | Explicit known-issue scope; no false claim of all expectations passing |
| ST10 | Test requires UI automation or supported performance metric | Route to XCTest/XCUIAutomation and Apple-platform skill |
| ST11 | User says GO after a single test PASS | No broad fixes, package install, OTA, MERGE, signing or app deployment |
| ST12 | Existing Xcode project already uses `swiftui-pro` and an Apple routing skill | Avoid duplicating their rules; restrict to compiler/test evidence |
| ST13 | Dirty working tree owned by another agent or shared Mac heavy lock | BLOCKED; no lock deletion/reconfiguration |
| ST14 | Build/test wrote DerivedData to internal disk without wrapper receipt | Not complete; rerun safely with approved paths and cleanup |
| ST15 | External open-source concurrency skill URL exists | Reference only until license/version/scope authorized; no automatic install |
| ST16 | `@MainActor` added to all code to silence an isolation error | Reject unsafe global change; inspect real target default isolation and minimal fix |

These are conceptual review fixtures, **not** executed model A/B or real compiler results.

## Proof hierarchy and adoption

1. **STATIC:** source and decision-fixture audit, no claimed runtime proof.
2. **SWIFT_COMPILE/TEST:** exact pinned Swift target built, test counts and exit logged; runtime failures preserved.
3. **XCODE:** exact actual app scheme and simulator suite, result bundle preserved. Needed before claiming integration.
4. **DEVICE:** physical target, owner acceptance and performance evidence. Neither a SwiftPM test nor a simulator run proves this.
5. **SKILL_A_B:** freeze one authorized task and its exact repo SHA, compare baseline Apple routing vs additional skill under an independent reviewer, count material new confirmed defects, false positives, false PASS and effort. Incremental usefulness **NOT_MEASURED** until this is performed.

## Primary sources

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Testing asynchronous code](https://developer.apple.com/documentation/testing/testing-asynchronous-code)
- [XCTest migration and interoperability](https://developer.apple.com/documentation/testing/migratingfromxctest)
- [Running tests in parallel / serialized trait](https://developer.apple.com/documentation/testing/parallelization)
- [Swift 6 concurrency migration guide](https://www.swift.org/migration/documentation/migrationguide/)
- [Data-race safety checking modes](https://www.swift.org/migration/documentation/swift-6-concurrency-migration-guide/enabledataracesafety/)
- [Paul Hudson's concurrency skill (optional source, not installed)](https://github.com/twostraws/Swift-Concurrency-Agent-Skill)

---
name: swift-testing-concurrency
description: "DRAFT PILOT: load only if owner explicitly names swift-testing-concurrency for a scoped, isolated Swift Testing/concurrency test; otherwise use existing Apple skill. Evidence for actor isolation, Sendable, async cancellation and XCTest boundary. No implicit adoption, production refactor, signing or deployment."
metadata:
  opencode/autoinvoke: "false"
---

# Swift Testing + Concurrency — Cloverwood isolated pilot

**Status: DRAFT / NOT ADOPTED / EXPLICIT OWNER INVOCATION ONLY BY POLICY.** This is a source-backed, narrowly scoped testing skill. OpenCode honors `opencode/autoinvoke: "false"` by excluding it from model-facing automatic skill suggestions; that flag **does not control Codex**. Codex may discover repo-local skill name/description and implicitly select it, so the **description itself forbids implicit use** and this proposal stays only on its isolated DRAFT branch until separately approved. The instruction is a policy guard, **not a technical disable switch for Codex**. Never globally link/install or copy it into product repos during this pilot. Merely opening a checkout can expose its metadata; no agent/model activation has been proven.

## 1. Authority, no duplication

1. Establish owner's exact ticket, project repository and `AGENTS.md`, immutable decisions, `main`/HEAD, target and Xcode/Swift configuration. Preserve dirty worktrees. `GO` does not grant broad refactoring, signing, OTA or MERGE.
2. Load [Apple platform development](../apple-platform-development/SKILL.md) **only for** Xcode, build, simulator, device and release/toolchain decisions. Use its tool catalog progressively; this skill does not replace its gates.
3. In a SwiftUI repository, load its own approved `swiftui-pro` where installed; **that skill** owns SwiftUI API, architecture, accessibility and rendering advice. Here inspect only testability and concurrency evidence. Paul Hudson's separate [Swift Concurrency Pro](https://github.com/twostraws/Swift-Concurrency-Agent-Skill) is an optional upstream reference for subtle concurrency bugs, **not** installed automatically or duplicated into this skill.
4. Keep this pilot limited to one approved Swift package, target or isolated fixture. Existing XCTest UI/performance tests remain authoritative in their domain. Do not assume a project supports Swift Testing, uses Swift 6 mode, or defaults to `MainActor`.

## 2. Select a precise test or audit route

- **TESTING:** For a pure/async Swift unit or integration behavior, prefer native Swift Testing (`import Testing`, `@Test`, `#expect`, `#require`), only if available in the actual toolchain/target. Parameterized tests should assert each meaningful boundary value. `#require` means subsequent statements need its value; `#expect` records and continues.
- **ASYNC CALLBACK:** Prefer `await` of a result/stream. Use Swift Testing `confirmation` for callback/event counts that occur **within its closure**; it is not an arbitrary delay, semaphore or `XCTestExpectation` replacement for callbacks happening after the closure returns. Ensure observation lifetime and completion are explicit.
- **CONCURRENCY:** Confirm Swift toolchain, `SWIFT_VERSION`, `SWIFT_STRICT_CONCURRENCY`, `SWIFT_DEFAULT_ACTOR_ISOLATION` or package settings **for the exact target**. Diagnose data crossings, actor boundaries, `Sendable` requirements, task ownership, cancellation and main-actor UI updates. Swift 6 language mode enables complete data-race checking; Swift 5 targets may opt into `complete` diagnostics without a migration.
- **XCTEST/UI:** Keep XCTest for UI automation or platform-performance workflows; do not mass-convert tests. Mixed suites need pinned version-specific interoperability checks. Simulator runtime evidence is not physical-device evidence.

## 3. Test design and hazards

1. Freeze the known behavior and source SHA. Record one positive case, one negative/boundary case and one regression for cancellation/reentrancy/state isolation where relevant.
2. Inject deterministic clocks, data, fake async streams, storage and network responses. Never use arbitrary `Task.sleep`, `usleep`, polling loops or flaky ordering assertions to force success.
3. Swift Testing may execute tests concurrently in-process. Give each test independently owned state, or use narrowly justified `.serialized` for shared resources. Serialization is **not** a fix for production data races.
4. Always await task completion or cancellation before evaluating final state. Test that canceled/superseded work cannot overwrite newer state when the product contract requires it.
5. Keep callbacks/continuations single-completion; verify failure paths and cancellation behavior. Never silence test failures through `try?`, unconditional `withKnownIssue`, `@unchecked Sendable`, `nonisolated(unsafe)`, `@preconcurrency` or reduced compiler checks just to obtain PASS.
6. Runtime tests do not prove absence of every data race. Use the compiler diagnostics as a **separate** gate; use sanitizers/Thread Sanitizer on a supported target when warranted, recording compatibility and limits.
7. Don't change app concurrency defaults or blanket-`@MainActor` modules to silence errors. For Swift 6.2+ first inspect effective default actor isolation and `nonisolated(nonsending)` behavior per actual compiler/project; do not assume semantics from the OS version.

## 4. Execute with evidence

- Read [direct QA contract](references/DIRECT_QA_CONTRACT.md) and use its ticket/evidence template.
- Authorized local Mac: preflight external dev disk UUID/write/free space; 20 GiB internal free minimum for heavy work; check shared heavy lock. For all build/test commands use repository-owned `bash scripts/cloverwood-local-run.sh -- ...` and distinct disposable roots under `/tmp/cloverwood-ci/<repo>/<run-id>`; pass `swift test --scratch-path "$CLOVERWOOD_RUN_ROOT/swiftpm"` and `xcodebuild -derivedDataPath "$CLOVERWOOD_RUN_ROOT/DerivedData" -resultBundlePath "$CLOVERWOOD_RUN_ROOT/results/<name>.xcresult"` when applicable. **Before the wrapper exits**, preserve the requested `.xcresult` (including on test FAIL) and bounded logs to a preapproved, access-controlled evidence directory **outside** the disposable root; confirm the copied bundle exists and is readable, preserve the original `xcodebuild` exit code, and only then let the wrapper clean up. See [mandatory evidence-retention example](references/DIRECT_QA_CONTRACT.md#result-bundle-retention-before-wrapper-cleanup). If preservation fails, report `EVIDENCE_FAIL`, not `PASS`. Never commit potentially private test data. Verify cleanup receipt.
- Run an actual scoped `swift test` or `xcodebuild test`, with exact toolchain, source/head SHA, command, exit code, test count and stderr diagnostics. A static read/format check is `STATIC_PASS`, not `TEST_PASS`. Check `swiftc` actor isolation diagnostics separately.
- No simulator creation/deletion, automatic dependency installation, new test frameworks, signing, TestFlight, OTA, global skill install or edits to product games/apps without explicit authorization.

## 5. Independent review / stop conditions

Report `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN` separately for compiler, Swift Testing runtime, XCTest/UI, simulator/device and cancellation/negative tests. Include the real target's destination and errors; never use a green test count as proof of gameplay, iPhone performance or visual acceptance.

Stop on unclear owner scope, a dirty canonical worktree, a version-mismatched compiler example, silent retry masking failures, a test leaving background tasks alive, or a request to suppress concurrency diagnostics. Submit the smallest targeted FIX/REVIEW packet. **No MERGE, DEPLOY or global promotion** from test PASS; only the owner may authorize those actions.

**Pilot success criterion:** evidence of a *material, independently confirmed* testing/concurrency finding or measurable reduction in false-PASS at equal workload vs. baseline Apple skill/runbook, with zero unsafe operations. The sample fixture is isolated evidence only; skill's incremental agent effectiveness remains **NOT_MEASURED** until a controlled A/B.

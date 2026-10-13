# Swift Testing + Concurrency — isolated pilot fixture

**Reviewed:** 2026-10-13. **Status:** DRAFT sample, NOT ADOPTED.

A minimal Swift 6 language-mode package containing one actor and four focused
Swift Testing checks. It has no app resources, signing, network API calls,
consumer dependencies, user data, iPhone target or external provider.

## Contract

- **Current revision wins** even if an older async completion arrives later.
- **Invalid request tokens** never overwrite actor state.
- **Concurrent token creation** produces unique sequence IDs under actor isolation.
- **Task cancellation before delivery** rejects a completion deterministically,
  without sleeps or probabilistic delays.

Tests use `import Testing`, `@Suite`, `@Test`, `#expect`, `async let` and
`Task` cancellation. The production logic is intentionally tiny; this is **not**
a production app, exhaustive concurrency audit or evidence of improved agent output.

## Run under the required Mac wrapper

From the **repository root** after checking your authorized worktree and disk:

```bash
CLOVERWOOD_REPO_NAME=codex-game-dev-library \
CLOVERWOOD_EXCLUSIVE_MAC=0 \
bash scripts/cloverwood-local-run.sh -- \
  bash -c 'cd samples/swift-testing-concurrency-pilot && swift test --scratch-path "$CLOVERWOOD_RUN_ROOT/swiftpm"'
```

Use Swift 6+ toolchain with Swift Testing available. `Package.swift` uses
`swift-tools-version: 6.0`, so SwiftPM enables Swift 6 mode for targets by default.
A successful test run is only a bounded runtime+compiler PASS.

For Xcode app work, follow the project-local `AGENTS.md`, the
[Apple skill](../../.agents/skills/apple-platform-development/SKILL.md) and
the [Swift Testing and concurrency skill](../../.agents/skills/swift-testing-concurrency/SKILL.md).
Capture source HEAD, toolchain, warnings, exit code, test count, wrapper cleanup.
Never extrapolate Mac package tests to an iPhone build or UI test.

## Negative test design

The second test rejects an out-of-generation result. The fourth triggers
cancellation **inside its own Task** before delivery, avoiding a scheduling
race between a test-side `cancel()` and a worker doing an immediate write.
This does not prove all asynchronous cancellation cases; it is a stable unit
fixture. A future authorized A/B can compare whether the new skill recognizes
stale completion and cancellation risks better than the base Apple guidance.

## Upstream

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Swift Testing asynchronous code](https://developer.apple.com/documentation/testing/testing-asynchronous-code)
- [Swift 6 full data-race checking](https://www.swift.org/migration/documentation/swift-6-concurrency-migration-guide/enabledataracesafety/)

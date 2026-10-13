# CW-SWIFT-TESTING-CONCURRENCY-PILOT-01 — existing-skill audit and isolated proposal

**Reviewed:** 2026-10-13  
**State:** DRAFT / REVIEW REQUIRED / NOT ADOPTED / NO MERGE  
**Baseline:** `cloverwoodstudio/codex-game-dev-library` main `d2e16245c23f6c47b8e4ebc74b88255f0918055e`.  
**Scope:** New repo-local skill, reference contract, one tiny **isolated** SwiftPM test package and CI/static fixtures; docs/source index/backlog. **No CRYVIQ, Personal OS, game or company monorepo edits.** No Codex use, new packages, app signing/OTA, global skill installation or deployment.

## Audit of our actual skills

| Existing source | Observed location | Owns already | Proposed skill must NOT duplicate |
| --- | --- | --- | --- |
| Apple platform development | `codex-game-dev-library/.agents/skills/apple-platform-development/SKILL.md` | Apple tool/SDK discovery, project target, Xcode, simulator/device, signing/release | Xcode project setup or release automation |
| SwiftUI Pro (Paul Hudson, MIT, pinned project copy) | `cloverwoodstudio/CRYVIQ/.agents/skills/swiftui-pro/SKILL.md` | SwiftUI API/data flow, performance, UI/accessibility, basic concurrency advice | A competing UI linter, compulsory UIKit refactor or generic modern Swift rules |
| Shared game-testing and Apple build playbooks | `guides/workflows/game-testing.md`, `guides/workflows/apple-build-release.md` | General test pyramid, XCTest/XCUIAutomation, simulator/device matrix, release evidence | Another entire test pyramid or device deployment policy |
| Paul Hudson Swift Concurrency Pro (upstream candidate) | https://github.com/twostraws/Swift-Concurrency-Agent-Skill | Advanced Swift concurrency coding/review guidance; not a library-local installed skill | Vendoring upstream content or replacing its general concurrency expertise |

The requested increment is **testing-specific evidence engineering**: use Swift Testing to catch stale async completions, cancellation/state isolation defects and isolate compiler diagnostics from test claims. No broad migration to Swift 6 or toolchain updates. The pilot proposes `.agents/skills/swift-testing-concurrency/SKILL.md` with `metadata.opencode/autoinvoke: "false"` (manual-only until owner adopts). No addition to the pinned v1 capability registry until a separately approved adoption; avoiding a registry entry prevents falsely advertising a production-installed helper and avoids rehashing unrelated pinned sources.

## Primary source findings

1. Swift Testing supports `@Test`, `#expect`, `#require`, argument-driven tests and async test methods. `confirmation` verifies events **inside** its closure, and does not independently await future callbacks. https://developer.apple.com/documentation/testing and https://developer.apple.com/documentation/testing/testing-asynchronous-code
2. Swift Testing runs tests concurrently by default; `.serialized` is narrowly scoped and does not serialize unrelated suites. Prefer isolated test fixtures. https://developer.apple.com/documentation/testing/parallelization
3. XCTest remains needed for UI automation and appropriate performance workflows; migration must be selective and toolchain-specific. https://developer.apple.com/documentation/testing/migratingfromxctest
4. Swift 6 mode enables full data-race checking, but earlier Swift language modes can report complete concurrency warnings incrementally. Target-specific compiler settings and actor isolation must be inspected before proposing changes. https://www.swift.org/migration/documentation/swift-6-concurrency-migration-guide/enabledataracesafety/ and https://www.swift.org/migration/documentation/migrationguide/
5. Paul Hudson's dedicated concurrency skill is MIT-licensed and addresses agent mistakes; **only link to it**, do not install/fork blindly. https://github.com/twostraws/Swift-Concurrency-Agent-Skill

## Candidate and boundaries

- [Manual-only pilot skill](../.agents/skills/swift-testing-concurrency/SKILL.md)
- [Direct QA receipt and 16 static decision fixtures](../.agents/skills/swift-testing-concurrency/references/DIRECT_QA_CONTRACT.md)
- [Isolated Swift 6 fixture](../samples/swift-testing-concurrency-pilot/README.md): one actor, four tests for stale completion, invalid ticket, concurrent token issuance and task cancellation, no sleeps or external packages.
- [Intentionally broken disposable fixture runner](../samples/swift-testing-concurrency-pilot/verify-negative-regression.sh): drops the revision guard in a disposable copy only, and must observe a **real Swift Testing failure** while the verified source stays untouched.
- [Static contract tests](../tests/test_swift_testing_concurrency_pilot.py) and [macOS CI job](../.github/workflows/swift-testing-concurrency-pilot.yml).

### Initial isolated Mac evidence — real, not app QA

On owner-authorized Mac via DC and repository wrapper, pinned local Swift toolchain output was `Apple Swift 6.4` (`Xcode-27.1-RC` developer path). After creating an external-disk isolated clean checkout at `/Volumes/CLOVERWOOD_DEV/Pilots/SwiftTestingConcurrency-01/workspace/library`:

- Green test run with `swift test --scratch-path "$CLOVERWOOD_RUN_ROOT/swiftpm" --parallel`: **4 tests / 1 suite PASS**, exit 0, cleanup PASS; separate retained log `.../evidence/swift_test_first.log`.
- A separate disposable package copy with the `token == generation` safety check intentionally removed: `swift test` returned **exit 1** with the expected named stale-completion assertion failure, so the **negative harness PASS**, wrapper exit 0, cleanup PASS. Retained log `.../evidence/swift_expected_red.log`.
- No product code, Xcode simulator, build signing, device or UI test was run. The synthetic actor proves one behavioral contract only, **not** a production race diagnosis or comparative skill benefit.

The new CI must pass on **the eventual exact PR HEAD**; `Green` and intentional `Red` must be reported separately. A regression catching one deliberate bug does not by itself prove the *agent skill* adds signal above baseline.

## Adoption / independent A-B required

| Gate | Evidence required | Status |
| --- | --- | --- |
| Existing-skill overlap classified | Real sources, scoped non-duplication | PASS, audit above |
| Swift sample: actual compiler and four tests | Swift/version/HEAD/exit/log/cleanup | PASS, isolated Mac run |
| Deliberately broken fixture rejected | Failure from the named assertion, **not** generic compile failure | PASS, isolated Mac run |
| CI and static skill checks | Green GitHub checks at **exact current HEAD** | PENDING until CI |
| Apple app integration | Specific authorized project and target, actual build and tests | NOT_RUN |
| OpenCode/Codex/ChatGPT skill load | Tool-specific actual load event | NOT_RUN |
| Independent baseline vs skill A/B | Same frozen source SHA, confirmed defects, false positives and effort | NOT_MEASURED |
| Owner adoption, global installation, MERGE, OTA | Explicit later decision | NOT_APPROVED |

Pilot advancement requires a real defect/evidence improvement, zero unsafe actions and acceptable time overhead. If it adds no value beyond the Apple router and existing SwiftUI/concurrency skills, keep as a testing reference rather than install globally. Do not extrapolate the SwiftPM fixture to physical iPhone correctness.

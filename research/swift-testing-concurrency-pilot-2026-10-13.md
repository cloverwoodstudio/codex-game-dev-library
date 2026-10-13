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

The requested increment is **testing-specific evidence engineering**: use Swift Testing to catch stale async completions, cancellation/state isolation defects and isolate compiler diagnostics from test claims. No broad migration to Swift 6 or toolchain updates. The pilot proposes `.agents/skills/swift-testing-concurrency/SKILL.md` with `metadata.opencode/autoinvoke: "false"` (manual-only **within OpenCode**; Codex may still discover it on this isolated branch, so its description limits usage to explicit owner requests). No addition to the pinned v1 capability registry until a separately approved adoption; avoiding a registry entry prevents falsely advertising a production-installed helper and avoids rehashing unrelated pinned sources.

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
- [Strict single-test red-output checker](../samples/swift-testing-concurrency-pilot/verify_expected_red.py) and [11 parser regressions](../tests/test_swift_negative_red_parser.py): fail closed on unrelated test failures, no matching test, wrong assertion, compiler errors and zero-test runs.
- [Static contract tests](../tests/test_swift_testing_concurrency_pilot.py) and [macOS CI job](../.github/workflows/swift-testing-concurrency-pilot.yml).

### Initial isolated Mac evidence — real, not app QA

On owner-authorized Mac via DC and repository wrapper, pinned local Swift toolchain output was `Apple Swift 6.4` (`Xcode-27.1-RC` developer path). After creating an external-disk isolated clean checkout at `/Volumes/CLOVERWOOD_DEV/Pilots/SwiftTestingConcurrency-01/workspace/library`:

- Green test run with `swift test --scratch-path "$CLOVERWOOD_RUN_ROOT/swiftpm" --parallel`: **4 tests / 1 suite PASS**, exit 0, cleanup PASS; separate retained log `.../evidence/swift_test_first.log`.
- A separate disposable package copy with the `token == generation` safety check intentionally removed: `swift test` returned **exit 1** with the expected named stale-completion assertion failure, so the **negative harness PASS**, wrapper exit 0, cleanup PASS. Retained log `.../evidence/swift_expected_red.log`.
- No product code, Xcode simulator, build signing, device or UI test was run. The synthetic actor proves one behavioral contract only, **not** a production race diagnosis or comparative skill benefit.

The new CI must pass on **the eventual exact PR HEAD**; `Green` and intentional `Red` must be reported separately. A regression catching one deliberate bug does not by itself prove the *agent skill* adds signal above baseline.

## GitHub CI evidence on the code-bearing PR HEAD

The isolated pilot was executed on GitHub at exact commit `1f62e4d90a5a46b4e85e82e590dc7b8112696659` (DRAFT PR #10).

- [macOS Swift Testing pilot job](https://github.com/cloverwoodstudio/codex-game-dev-library/actions/runs/38433281921/job/115420706478): **SUCCESS** under **Apple Swift 6.3.3** on GitHub runner. All **4/4 Swift Testing cases PASS**, intentional stale-response bug produces the expected red assertion and nonzero status, regression harness passes. Foreground wrapper cleanup **PASS**.
- [Offline registry and library tests](https://github.com/cloverwoodstudio/codex-game-dev-library/actions/runs/38433281786/job/115420706062): **SUCCESS**, including the pilot's seven static contract tests and existing 123 library tests. Capability registry remains `DISCOVERY_ONLY`, 12 existing entries and no newly promoted capability.
- [Links CI](https://github.com/cloverwoodstudio/codex-game-dev-library/actions/runs/38433281841/job/115420704407): **SUCCESS**.
- The full exact-HEAD check inventory comprised **eight named check types**, all SUCCESS: Swift pilot, offline registry, links, SpriteKit, Apple iOS, Godot, Phaser and deterministic conformance.
- No paid services or project accounts accessed. The Apple CI runtime is a **small pure SwiftPM fixture**, not an iPhone app build or device acceptance.

These are **compiler/runtime and integrity** results for the earlier test-fixture gate. The actual subsequent, controlled A/B model comparison is now documented in [the completed synthetic A/B study](swift-testing-concurrency-ab-2026-10-13.md). Any later documentation-only commit advances PR HEAD; revalidate checks on that exact HEAD before review or merge.

## Review FIX — 2026-10-13

The independent REVIEW of PR #10 on `d187be16227b28a6bb5a88a66e8fa361435bea2a` reported one P1 and two P2 findings. **This section documents fixes in the pilot branch; not a production adoption.**

- **P1 — false red-test PASS:** A synthetic fake Swift runner on the owner Mac printed that the **expected stale-response test passed** and **another test failed**. The former harness incorrectly returned `EXPECTED_RED_TEST_PASS` (exit 0). The fixed `verify-negative-regression.sh` now filters to the specific Swift Testing method and delegates to `verify_expected_red.py`, which requires the **sole started/failed test** to be the expected one, the **exact revision-guard expectation**, and a **one-test/one-issue failed run**; it rejects other passing/failing tests, compile failures and zero-test runs. Eleven focused parser regressions include the original independently reproduced false-PASS, plus the real Swift mutant run.
- **P2 — lost `.xcresult` evidence:** The prior instructions generated a bundle within a disposable directory without a mandatory within-wrapper save step. The skill and [direct QA contract](../.agents/skills/swift-testing-concurrency/references/DIRECT_QA_CONTRACT.md#result-bundle-retention-before-wrapper-cleanup) now require **copy/inspect to an approved persistent external evidence directory before cleanup**, on success or failure, while preserving original `xcodebuild` exit status. The example intentionally uses project/scheme/destination placeholders; an app-specific `.xcresult` retention run is **NOT_RUN** and no app build is claimed.
- **P2 — Codex implicit discovery:** OpenCode's `opencode/autoinvoke: "false"` preference does not disable Codex. The pilot skill now says this explicitly in frontmatter description and main instructions, restricting **policy usage** to explicit owner invocation; the DRAFT branch is **not** merged or installed globally. This is not a technical switch guaranteeing non-discovery in Codex. A Codex model invocation is **NOT_RUN**.

**Local FIX test receipt:** owner Mac external isolated checkout at `/Volumes/CLOVERWOOD_DEV/Pilots/SwiftTestingConcurrency-01/workspace/library` on code-bearing HEAD `a8809985348abc4517af5fb83b7948452e3e80b4`; Apple Swift 6.4; `20/20` Python pilot regressions PASS, `4/4` real Swift Testing PASS, intentionally mutated stale-response test **failed with the expected exact assertion** and the red verifier PASS, `REGISTRY_CHECK_PASS`, cleanup PASS. Evidence log retained at `/Volumes/CLOVERWOOD_DEV/Pilots/SwiftTestingConcurrency-01/evidence/review_fix_local.log`.

**CI:** dedicated macOS workflow updated to run the parser unit regressions and real green/red Swift tests. The **latest post-FIX PR HEAD** must have its own successful GitHub checks; old `d187be16` CI is not a substitute. **At this initial CI stage the skill A/B had not run**; the subsequent small synthetic four-run comparison is now complete with no improvement in seeded-bug recall. No app/production changes were authorized.

**A/B completed (2026-10-13):** [Frozen benchmark, actual OpenCode responses, blind-scoring receipts and compiler-verified post-hoc spinner regression](swift-testing-concurrency-ab-2026-10-13.md): both A and B detected **all three seeded bugs in both repetitions (6/6 each)**; candidate B detected an additional valid loading-ownership bug in **2/2** vs **1/2** baseline, but used **~5× prompt bytes**, longer outputs and longer average completion time. Same model and isolated sessions; zero tool calls or product mutations. The earlier free-tier blocker was resolved by correctly using OpenCode V2 `permissions`. **No broad production benefit has been established; PR remains DRAFT.**

## Adoption / independent A-B required

| Gate | Evidence required | Status |
| --- | --- | --- |
| Existing-skill overlap classified | Real sources, scoped non-duplication | PASS, audit above |
| Swift sample: actual compiler and four tests | Swift/version/HEAD/exit/log/cleanup | PASS, isolated Mac run |
| Deliberately broken fixture rejected | Failure from the named assertion, **not** generic compile failure | PASS, isolated Mac run |
| CI and static skill checks | Green GitHub checks at tested code HEAD `1f62e4d` | PASS at that HEAD; recheck subsequent docs-only HEAD |
| Apple app integration | Specific authorized project and target, actual build and tests | NOT_RUN |
| OpenCode/Codex/ChatGPT skill load | Tool-specific actual load event | NOT_RUN |
| Independent baseline vs skill A/B | Same frozen source SHA, blind scoring, actual model responses and elapsed time | COMPLETED on one synthetic benchmark; 6/6 vs 6/6 seeded TP, limited extra spinner signal, not generalized |
| Owner adoption, global installation, MERGE, OTA | Explicit later decision | NOT_APPROVED |

Pilot advancement requires a real defect/evidence improvement, zero unsafe actions and acceptable time overhead. If it adds no value beyond the Apple router and existing SwiftUI/concurrency skills, keep as a testing reference rather than install globally. Do not extrapolate the SwiftPM fixture to physical iPhone correctness.

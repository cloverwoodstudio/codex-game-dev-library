# Automated game testing strategy

Reviewed: 2026-08-29

Automate stable facts; playtest feel. A useful suite catches rule, content and integration regressions quickly while real play sessions evaluate readability, emotion, pacing, controls, audio and fun.

## Test layers

1. **Pure logic:** math, rules, economy, inventory, quests, parsing and migrations.
2. **Simulation:** fixed-step systems with seeded inputs and no renderer.
3. **Content validation:** IDs, references, bounds, localization, assets and graph reachability.
4. **Engine integration:** scenes, prefabs/actors, physics, animation, saves and platform services.
5. **Playable journeys:** launch, onboarding, core loop, win/fail, restart and recovery.
6. **Non-functional:** performance, memory, load, soak, network faults, accessibility and compatibility.

Keep most tests low and deterministic. Use fewer high-level journeys because they are slower and more environment-sensitive, but never omit the real packaged build.

## Testability architecture

Separate simulation from presentation, use injected clocks and random streams, address content by stable IDs, expose read-only diagnostic state, and drive player intent through semantic actions. Avoid tests that depend on arbitrary sleeps; wait for observable state with a deadline.

A failure must report seed, tick, build/content versions, expected/actual state and artifacts. A flaky test is a defect: quarantine only with owner, reason and expiry, never silently retry until green.

## Engine routes

- Godot supports command-line/headless runs and headless export for CI; project tests commonly use a chosen test framework or project-owned harness.
- Unity Test Framework supports EditMode, PlayMode and target-player runs from the command line with NUnit-style result XML.
- Unreal Automation supports command-line test filters, JSON/HTML reports, connected clients and screenshot comparison.

Pin the exact engine version and licensing/runtime requirements in CI. Cache only reconstructible dependencies; never treat cache contents as release artifacts.

## Pull-request gate

Run formatting/static checks, pure tests, content validation, deterministic smoke replay and the smallest headless integration test. Upload logs/results on every failure. Heavier target builds, visual suites, fuzz seeds, multiplayer and performance scenarios can run on main, nightly or release gates according to cost.

## Definition of a valuable test

- protects a player-visible or production-critical contract;
- controls time, randomness and initial state;
- has one clear reason to fail;
- leaves actionable evidence;
- runs at the cheapest layer able to prove the behavior;
- is exercised in CI with an explicit owner.

## Sources

- Godot command-line/headless workflow: https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html
- Unity Test Framework command-line reference: https://docs.unity3d.com/Packages/com.unity.test-framework@2.0/manual/reference-command-line.html
- Unreal Automation System: https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-system-user-guide-in-unreal-engine
- Unreal command-line automation tests: https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine

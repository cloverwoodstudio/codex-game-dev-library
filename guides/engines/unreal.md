# Unreal Engine

Reviewed: 2026-08-29

Use the Gameplay Framework intentionally: GameMode for server-side rules, GameState for replicated match state, PlayerState for replicated player state, controllers for intent, and pawns/characters for embodiment. Keep Blueprint APIs narrow and move stable/high-cost systems to C++ when justified.

Use Automation and Functional Testing for repeatable checks. Build/package from the command line in CI. Profile frame time on target hardware; Editor preview is not a substitute for device profiling.

Primary sources:

- https://dev.epicgames.com/documentation/unreal-engine/gameplay-framework-in-unreal-engine
- https://dev.epicgames.com/documentation/unreal-engine/automation-test-framework-in-unreal-engine
- https://dev.epicgames.com/documentation/unreal-engine/introduction-to-performance-profiling-and-configuration-in-unreal-engine

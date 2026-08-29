# Unreal Engine production playbook

Reviewed: 2026-08-29

## Best fit

Choose Unreal for high-end 3D, large worlds, built-in multiplayer patterns, strong cinematic tooling, or teams that benefit from C++ plus Blueprint collaboration. Prove target hardware, source-vs-launcher engine policy, platform SDKs, build-farm capacity and content storage before scaling production.

## Recommended project shape

```text
Game.uproject
Source/
  GameCore/          # stable rules and shared contracts
  GameFeatures/      # bounded runtime modules
Plugins/GameFeatures/# optional independently activated features
Content/             # assets organized by ownership, not file type alone
Config/
Tests/
Build/
```

Do not commit generated `Binaries/`, `DerivedDataCache/`, `Intermediate/` or `Saved/` content. Define a deliberate source-control policy for large binary assets and use One File Per Actor where it genuinely improves world collaboration.

## Gameplay ownership

- `GameMode`: authoritative rules for the current mode; it exists on the server.
- `GameState`: replicated match state clients must observe.
- `PlayerState`: replicated player identity and match data that should survive pawn changes.
- `PlayerController`: player intent, local UI coordination and possession.
- `Pawn`/`Character`: the possessed physical embodiment.
- `GameInstance` or a subsystem: carefully scoped state and services spanning map loads.

Keep Blueprint APIs narrow and intentional. Blueprints are excellent for composition, tuning and presentation. Move stable, performance-sensitive, security-critical or widely reused logic to C++ when evidence justifies it; do not rewrite working visual logic merely for stylistic purity.

## Codex loop

1. Read the `.uproject`, module/plugin descriptors, target files, owning C++ classes and Blueprint-facing contracts.
2. Identify authority, replication and lifecycle ownership before changing gameplay state.
3. Add the narrowest automation or functional test that can prove the rule.
4. Compile the affected target and run focused automation headlessly.
5. Exercise the actual map with real inputs, network roles and transitions.
6. Cook/package and launch outside the editor for milestone proof.

Command shapes differ by engine installation, host OS and target platform:

```sh
UnrealEditor-Cmd <project.uproject> -ExecCmds="Automation RunTest <Group>;Quit" -unattended -nopause -testexit="Automation Test Queue Empty"
RunUAT BuildCookRun -project=<project.uproject> -build -cook -stage -pak -archive -archivedirectory=<output>
```

Version-control the exact working wrapper scripts. Keep logs, test reports, cooked manifests and packaged-build smoke-test evidence as CI artifacts.

## Validation ladder

1. Low-level automation for deterministic C++ or Blueprint-exposed rules.
2. Editor/module compile and content validation.
3. Functional test in a tiny representative map.
4. Standalone and listen/dedicated-server sessions for the required network roles.
5. Cooked development build launched outside the editor.
6. Release-like package on target hardware.
7. Unreal Insights trace covering representative gameplay.

## Asset, world and performance rules

- Use naming and directory ownership that make migration and dependency review predictable.
- Avoid hard-reference chains that load entire content families unintentionally; inspect asset dependencies.
- Treat redirector cleanup, map resaves and bulk Blueprint compilation as isolated reviewed operations.
- Establish CPU, GPU, memory, streaming, shader, package-size and network budgets per platform.
- Profile standalone or packaged builds. Editor overhead and preview scalability are not shipping evidence.
- For large worlds, test streaming boundaries, spawn ownership, save identity, AI activation and network relevancy under adverse I/O.

## Primary sources

- [Gameplay Framework](https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-framework-in-unreal-engine)
- [Run automation tests from the command line](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine)
- [BuildCookRun](https://dev.epicgames.com/documentation/unreal-engine/build-operations-cooking-packaging-deploying-and-running-projects-in-unreal-engine)
- [Unreal Insights](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-in-unreal-engine)
- [Lyra sample](https://dev.epicgames.com/documentation/en-us/unreal-engine/lyra-sample-game-in-unreal-engine)

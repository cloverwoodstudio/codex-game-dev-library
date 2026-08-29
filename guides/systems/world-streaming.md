# Large worlds, streaming and spatial persistence

Reviewed: 2026-08-29

Streaming is a state-management system, not merely an optimization. A world cell can disappear while quests, AI, saves, audio, navigation and network authority still need coherent state.

## Partition contract

Define world coordinates/origin policy, cell and hierarchy sizes, streaming sources, load radius/hysteresis, priority, dependencies, always-loaded services, memory/I/O budgets, async cancellation, failure fallback and teleport/fast-travel prefetch.

Keep persistent domain state separate from loaded presentation instances. Entities use stable world IDs; loading materializes their current state, unloading commits only the intended persistent state and releases transient resources.

## Cell lifecycle

`unloaded → requested → loading → dependencies ready → activated → deactivating → unloaded/failed`

Every transition is idempotent and cancellation-safe. Do not expose half-loaded interactables. Cross-cell references should use stable handles and tolerate the target being absent; hard object references often force cells to load together.

Unreal World Partition divides a persistent world into distance-streamed grid cells and works with One File Per Actor, Data Layers and HLOD. The underlying lessons apply across engines: authoring partition, runtime partition and gameplay ownership are related but distinct.

## Test routes

Automate worst-speed traversal, repeated boundary oscillation, teleport, death/reload at boundary, save during transition, quest actor unloaded, multiplayer players far apart, slow/corrupt I/O and memory-pressure eviction. Record cell timeline, stalls, peak memory and missing-reference diagnostics.

## Content rules

Set per-cell budgets for geometry, materials, textures, audio, navigation, AI and activation time. Generate HLOD/proxies and navigation through reproducible build steps. Use data layers/variants for world states only with explicit save and networking semantics.

## Sources

- Unreal World Partition: https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine
- Unreal Data Layers: https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition---data-layers-in-unreal-engine
- Unreal One File Per Actor: https://dev.epicgames.com/documentation/en-us/unreal-engine/one-file-per-actor-in-unreal-engine

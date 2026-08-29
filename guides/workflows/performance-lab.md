# Performance budgets and optimization lab

Reviewed: 2026-08-29

Performance is a product constraint measured on target hardware. Choose budgets before content scales, capture a baseline, change one justified bottleneck, and keep evidence.

## Budget sheet

For every supported hardware tier define:

- target refresh/FPS and total frame time: 30 FPS ≈ 33.33 ms, 60 ≈ 16.67 ms, 120 ≈ 8.33 ms;
- CPU game/render/job and GPU budgets with safety headroom;
- resident and peak memory, allocation/GC and streaming limits;
- startup, scene transition and interaction latency;
- disk/install/download, network bandwidth and server tick budgets;
- sustained thermal/power target for mobile and handheld devices.

Frame time—not average FPS—is the useful currency. Record distributions and worst-tail behavior; a smooth average can still conceal hitches.

## Reproducible capture

Record commit, build configuration, content version, device/OS/driver, power/thermal state, resolution/quality, scene, camera path, seed, warm-up, duration and profiler settings. Use target-like release builds on physical hardware. Editor and attached-profiler results are diagnostic, not release proof.

## Optimization loop

1. Reproduce the representative worst case and capture baseline.
2. Decide whether it is CPU, GPU, memory, I/O, network or synchronization bound.
3. Drill down with the engine/platform profiler.
4. Rank opportunities by measured player impact versus risk/cost.
5. Change one variable family; preserve visual and gameplay intent.
6. Repeat the identical capture and compare distributions.
7. Keep, revise or revert; document the result and regression guard.

Unreal Insights records high-rate trace events and analyzes CPU, GPU, memory and network behavior. Android guidance stresses stable pacing and tail metrics in addition to average FPS; mobile captures must also include thermal soak because short cold runs can mislead.

## Common traps

- optimizing a microbenchmark instead of the player-visible path;
- testing only on a fast development machine;
- trading stutter for a higher average;
- attaching a heavy profiler and treating its numbers as absolute;
- lowering quality globally before identifying the bound;
- missing asset-loading, shader-compilation and save/autosave spikes.

## Evidence artifact

Store a short Markdown report plus raw profiler capture when practical: hypothesis, before/after table, capture recipe, screenshots, visual differences, decision and follow-up. Use `templates/PERFORMANCE_REPORT.template.md`.

## Sources

- Unreal performance profiling: https://dev.epicgames.com/documentation/en-us/unreal-engine/introduction-to-performance-profiling-and-configuration-in-unreal-engine
- Unreal Insights: https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-in-unreal-engine
- Android game optimization: https://developer.android.com/games/optimize
- Android frame-rate metrics: https://developer.android.com/games/optimize/framerate

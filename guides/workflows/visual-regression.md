# Visual regression and capture discipline

Reviewed: 2026-08-29

Visual comparison detects unintended rendering changes; it does not judge whether an image is good. Build deterministic capture scenes, compare automatically, then require human review for meaningful differences.

## Control the capture

Pin build/content version, scene, save/seed, camera transform and projection, resolution/DPI, quality tier, renderer/API, locale, UI scale, time, animation tick, weather, exposure and device class. Warm shaders and assets before capture. Disable nondeterministic overlays, timestamps and irrelevant particles—or mask them explicitly.

Keep separate baselines for materially different rendering platforms. Do not loosen one global threshold until every GPU appears to pass.

## Comparison methods

- exact pixels for deterministic UI and generated diagrams;
- per-pixel tolerance for small numeric/render differences;
- structural/perceptual comparison for anti-aliasing or compression variation;
- semantic assertions for text, layout bounds, contrast and element presence.

Always preserve baseline, candidate, diff/heatmap and capture metadata. A changed baseline is a reviewed product decision, not an automatic “fix.”

## Capture set

Cover the core loop, menus/settings, win/fail, representative worlds, VFX extremes, lighting states, safe areas, aspect ratios, UI scales, long strings, pseudo-localization, RTL where supported, accessibility modes and low/high quality tiers.

Godot can render deterministic frame sequences with `--write-movie` and fixed FPS. Unity exposes screenshot capture APIs. Unreal's Automation frontend includes screenshot comparison. Each still requires project-owned state setup and baseline policy.

## Review workflow

1. Reproduce changed captures locally in the same environment.
2. Classify expected, defect, environment drift or nondeterminism.
3. For expected change, review all affected viewports/locales and update the baseline with rationale.
4. For defect, fix and retain the diff as evidence.
5. For nondeterminism, isolate its source rather than increasing tolerance broadly.

Visual checks complement—and do not replace—play sessions, accessibility inspection, performance profiling and video review of motion.

## Sources

- Godot command-line movie capture: https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html
- Unity `ScreenCapture.CaptureScreenshot`: https://docs.unity3d.com/ScriptReference/ScreenCapture.CaptureScreenshot.html
- Unreal Automation screenshot comparison: https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-system-user-guide-in-unreal-engine

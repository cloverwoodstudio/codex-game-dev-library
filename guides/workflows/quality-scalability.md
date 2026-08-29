# Quality tiers and rendering scalability

Reviewed: 2026-08-29

Quality settings trade presentation cost for performance, power and memory. They must preserve gameplay information, competitive fairness and accessibility.

## Tier contract

For minimum, recommended and high tiers define resolution/upscaling, frame target, textures/streaming pool, geometry/LOD distance, shadows, lighting/GI/reflections, post-processing, VFX, foliage/crowds, animation/physics/AI limits and memory/build-size budgets.

Set safe automatic defaults from measured hardware classes, then let players change them. Keep recovery mode and command-line reset for a configuration that fails to render or exceeds memory.

## Fairness and readability

Low settings must not remove cover, reveal hidden players, erase telegraphs, disable captions or change collision/simulation. Unreal explicitly warns that scalability choices can affect competitive fairness—for example, hiding grass that provided concealment. Scale non-gameplay detail first.

## Verification matrix

Capture the same deterministic scenes at every tier, resolution/aspect ratio and representative GPU. Compare frame-time tails, memory, load, visual diffs and gameplay cues. Test changes live and after restart; verify settings survive upgrades and invalid old values migrate safely.

Dynamic resolution and adaptive quality need bounded step sizes, hysteresis and cooldown so the image does not oscillate. Never use the current frame alone as the decision signal. Track thermal/power behavior on mobile and XR.

## Sources

- Unreal scalability guidance: https://dev.epicgames.com/documentation/en-us/unreal-engine/scalability-and-the-developer-for-unreal-engine
- Unreal scalability reference: https://dev.epicgames.com/documentation/en-us/unreal-engine/scalability-reference-for-unreal-engine
- Android game optimization: https://developer.android.com/games/optimize

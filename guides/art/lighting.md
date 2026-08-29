# Real-time lighting and readability

Reviewed: 2026-08-29

Lighting has four simultaneous jobs: gameplay readability, mood/story, material/shape description and performance. Establish the target hardware and rendering path before choosing baked, mixed or dynamic techniques.

## Lighting brief

For each environment record time/weather, emotional intent, focal hierarchy, navigation cues, exposure range, darkest playable value, character/key-light policy, light mobility, shadow/reflection/GI strategy, fog/atmosphere and per-tier budgets.

Start with broad environment and key directions, validate grayscale/value structure, then add motivated local lights and accents. Decorative lights without narrative or readability purpose consume budget and flatten hierarchy.

## Gameplay checks

- objectives, threats, pickups and traversal edges remain legible;
- the player can distinguish safe, dangerous and interactive space;
- exposure changes do not blind the player during required actions;
- darkness is playable on representative displays and room conditions;
- color-blind and low-vision modes do not rely on color alone;
- dynamic time/weather maintains the same critical contracts.

## Technical workflow

Choose static/baked, mixed or dynamic per light and platform. Control shadowed-light count, overlap, distance, resolution, cascades, reflection updates, volumetrics and transparency. Bake/probe errors, light leaks and missing runtime environment data must be checked in packaged builds—not only editor preview.

Capture worst-case GPU traces and a visual matrix across quality tiers. Treat changes in exposure, tone mapping and color grading as baseline changes requiring review of UI, VFX, characters and accessibility cues.

## Sources

- Unreal environment lighting: https://dev.epicgames.com/documentation/en-us/unreal-engine/lighting-the-environment-in-unreal-engine
- Godot 3D environment, cameras and lights: https://docs.godotengine.org/en/stable/tutorials/3d/introduction_to_3d.html
- Khronos real-time asset guidelines: https://github.com/KhronosGroup/3DC-Asset-Creation/blob/main/asset-creation-guidelines/RealtimeAssetCreationGuidelines.md

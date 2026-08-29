# Shaders and visual effects

Reviewed: 2026-08-29

VFX communicates gameplay first and decorates second. Define anticipation, action, impact, persistence and recovery; make team, danger, direction and magnitude readable under the gameplay camera.

## Effect brief

Trigger and owner; gameplay meaning; world/screen-space size; timing curve; color/value hierarchy; required lights/decals/distortion/audio/camera response; occlusion policy; scalability tiers; maximum concurrent instances; CPU/GPU/memory/overdraw budget; photosensitivity and motion concerns.

## Runtime discipline

- prefer bounded lifetimes and explicit pooling only after measurement
- set fixed bounds where safe; test culling from real cameras
- reduce transparent layers and full-screen overdraw
- batch/instance compatible effects; avoid unnecessary unique materials and emitters
- create low/medium/high scalability variants and graceful fallbacks
- warm critical shaders/effects when the engine/platform requires it
- profile aggregate worst-case encounters, not an isolated hero effect

Sources:

- Unreal Niagara scalability: https://dev.epicgames.com/documentation/unreal-engine/scalability-and-best-practices-for-niagara
- Unity VFX Graph: https://docs.unity3d.com/Manual/VFXGraph.html
- Godot particle shaders: https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/particle_shader.html

# Blender game-asset workflow

Reviewed: 2026-08-29

## Scene conventions

Define units, forward/up axes, naming, collections, origins and export rules before production. Apply/verify transforms deliberately. Keep source `.blend`, interchange export, baked textures and engine-imported asset distinct.

## Checklist

- clean topology appropriate to deformation and shading
- intentional hard edges, UV seams and custom normals
- non-overlapping UVs where baked maps require them; consistent texel density
- cage and bake tested for artifacts
- minimum material slots and texture sets consistent with quality
- rig uses a documented root, hierarchy and naming scheme
- animation clips have explicit ranges, loop rules and root-motion policy
- collisions, sockets/attachment points and LODs are named predictably
- exported glTF/FBX is reopened in a clean validation scene before engine import

Prefer glTF/GLB when the target supports it well; use the target engine's documented FBX settings where that pipeline is more mature. Never assume Blender viewport appearance will match runtime materials.

For premium Apple-native assets with named runtime state nodes, reproducible Python generation, USDZ packaging and physical-device approval, use the dedicated [Blender → USDZ → RealityKit workflow](premium-blender-usdz-realitykit.md).

Sources:

- Blender manual: https://docs.blender.org/manual/en/latest/
- Blender glTF exporter (4.4 manual): https://docs.blender.org/manual/en/4.4/addons/import_export/scene_gltf2.html
- Khronos glTF validator: https://github.khronos.org/glTF-Validator/

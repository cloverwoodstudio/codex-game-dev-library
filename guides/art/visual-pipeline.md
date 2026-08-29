# Visual pipeline: concept to runtime

Reviewed: 2026-08-29

## Art bible before asset batches

Lock representative references, shape language, palette, value hierarchy, material vocabulary, edge treatment, texture density, camera distance, lighting assumptions, UI language and “do not” examples. Store generated-image prompts and seeds/settings where available.

## 2D pipeline

Brief → thumbnails → composition/value pass → palette → production art → slicing/atlas → pivots/collision → animation → import settings → runtime inspection. Test at native and scaled resolutions; prevent texture filtering and pixel-grid errors when using pixel art.

## 3D pipeline

Brief/reference → blockout → modeling/sculpt → retopology → UVs → baking → PBR texturing → rig/animation when needed → export → import preset → collision/LODs → runtime review → profiling.

For metallic/roughness PBR, treat base color, metalness, roughness, normal, occlusion and emissive as data with correct color-space settings. Validate normals, tangents, scale, transforms and texture channels after import.

## Runtime budgets

Set budgets per asset class: triangles, draw calls/material slots, bones/influences, texture dimensions/memory, shader complexity, particles, overdraw and LOD distances. Budgets depend on platform and scene density; benchmark representative worst cases.

Primary sources:

- Khronos real-time asset guidelines: https://github.com/KhronosGroup/3DC-Asset-Creation/blob/main/asset-creation-guidelines/RealtimeAssetCreationGuidelines.md
- glTF: https://www.khronos.org/gltf/
- Adobe PBR/texturing overview: https://www.adobe.com/products/substance3d/discover/how-to-create-3d-textures.html

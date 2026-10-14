---
name: cloverwood-tripo-studio-game-assets
description: Use Tripo Studio subscriptions/credits via browser or already installed Tripo Blender DCC Bridge (never Tripo API/CLI generation), preserve 3D masters and run read-only Blender GLB/FBX geometry, rig and animation QA before Unity/Godot game integration.
---

# Tripo Studio game-asset pipeline

This is a game-asset skill, NOT permission to generate images or models,
spend credits, publish or modify any game. Always first read the target
game's AGENTS.md, Bible, existing game-dev library START_HERE.md and
docs/AI_VISUAL_ASSET_PIPELINE.md.

1. Use **Tripo Studio** (studio.tripo3d.ai) and its **Studio credits**.
   Tripo Studio and Tripo API have independent billing. Do NOT call
   tripo make, tripo ai, API endpoints, topup, or other API-credit flows.
   Only use an explicitly scoped browser session or existing Tripo
   Blender Bridge, and only after Design Datasheet Gate 0 + owner PASS.
2. An installed Bridge is NOT a verified active Studio connection.
   Prefer a Studio manual GLB export for predictable, auditable tests.
   FBX is useful for rigged characters/Unity. Keep texture sidecars.
3. Keep the original **MASTER** file byte-identical. Record SHA-256,
   asset ID/revision, Studio task/reference, Studio export method,
   observed credit cost if any, subscription/rights evidence and source
   design reference. Never infer origin/license from filename alone.
4. Any optimized **GAME** file MUST be separate from MASTER; don't
   overwrite source, modify authored game scripts or auto-publish.
5. Use read-only Blender inspector via:
   scripts/run_tripo_studio_qa.sh --input /absolute/model.glb
   --output /external/qa/report.json --max-triangles 25000
   --max-materials 8 --require-uv [--expect-rig --expect-animation]
   [--manifest /path/to/owner-evidence.json]
   All heavy jobs go through the approved disk-gated cleanup wrapper.
6. The manifest template in templates/ requires actual source SHA and
   owner-provided claims. No manifest => provenance unverified and
   shipping HOLD, even if technical QA passes.
7. Blender checks mesh, triangles, UV, materials, images, bones, skin
   weights, actions, geometry NaNs and bounding box. Actual scale,
   topology quality, look/feel and animation deformation need human
   and engine evidence; these are not proved by counts.
8. Godot/Unity tests must import a separate asset copy into a disposable
   test project; real mobile performance is a separate target-device QA.
9. Before any game integration, OWNER PASS/FIX in Asset Viewer after
   real Blender or target-engine visual review. Never auto MERGE/DEPLOY.

Read docs/TRIPO_STUDIO_GAME_ASSET_PIPELINE_03.md for receipts and limits.

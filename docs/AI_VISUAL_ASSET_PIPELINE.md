# AI Visual Asset Pipeline

Status: validated experimental workflow, 2026-09-23.
Purpose: create visually complex game assets while keeping gameplay semantics deterministic.

## Authority and gates
1. Design brief and Design Datasheet come first. Datasheet is Gate 0: same object in useful multiview angles, dimensions, materials, function, moving parts/ranges, Design ID and revision.
2. OWNER PASS/FIX on the datasheet happens before geometry realization.
3. AI geometry is visual geometry only. Game Lab owns connectors, axes, snap points, collision proxies, signal paths, gameplay state and logic.
4. Preserve the high-detail master; never destructively optimize or overwrite it.
5. Publish a separate runtime candidate, run technical QA, then OWNER PASS/FIX in Asset Viewer. Promotion/shipping is separate.

## Validated route
Design brief -> Datasheet -> OWNER PASS -> clean multiview references -> Tripo multiview generation -> high-detail MASTER GLB -> low-poly/texture-baked GAME GLB -> Blender QA -> Viewer -> OWNER review.

CW-SR-XR-001 Xeno Reactor is a pipeline fixture only. It is NOT a Starfall Rescue content change.

## Provenance required
Record Design ID/revision, provider/model, task ID, source views, settings, credits if applicable, original master SHA-256, runtime SHA-256, mesh/material/UV counts, triangle count, file size and QA result. Keep provider output and runtime derivative distinguishable.

## Validated benchmark
Tripo multiview task 3b057e68-4846-4426-aeb5-a6cad1b8fb1d produced the Xeno master: 2 meshes, 2 materials, 765,373 vertices, 1,467,794 triangles, 43,300,344 bytes, SHA-256 6104e86476ce8c3a81b5838bd7f4c4f689943db1fd916dd0e6ea4fdbcf19c0ce.
Tripo highpoly-to-lowpoly task 1e084a03-6bea-4dcb-972a-f4a12e60d9f1 with texture baking produced the runtime candidate: 1 mesh, 1 material, 34,659 vertices, 27,080 triangles, 4,256,076 bytes, 1 UV layer, SHA-256 5a6664a7f6d6b556c1cd9974412100da09f189d5be16e9bf043019cd1f4821a8. Blender import QA passed. Owner observed only small visual loss in Viewer; owner approval remains a separate explicit action.

## Viewer review
Use the Project Forge Asset Viewer. Publish MASTER and GAME as separate GLBs. QA sidecars must use a Viewer-recognized name/schema; for optimization use OPTIMIZE_QA.json. Never infer owner approval from technical PASS.

On mobile the Viewer supports a larger asset browser and FULLSCREEN model inspection. Fullscreen hides catalog/detail/review UI but keeps camera/material/light/background controls and EXIT. Use it to inspect silhouette, baked detail, seams, connectors and material fidelity before owner review.

## Decision rule
If the local optimized candidate preserves the approved look and meets runtime budget, prefer it. If not, create a controlled alternate optimization rather than modifying the master. Test actual target devices before promotion. Do not automatically add a benchmark asset to any game.

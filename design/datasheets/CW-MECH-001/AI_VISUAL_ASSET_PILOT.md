# CW-MECH-001 — AI Visual Asset Pilot
Status: EXPERIMENTAL — NOT PROMOTED
Design authority: CW-MECH-001 REV A — OWNER PASS
Purpose: benchmark deterministic CAD against AI visual realizations without changing gameplay authority.

## A/B/C benchmark
- A — Parametric CAD R3: deterministic multi-part reference realization.
- B — to3D single-image: job `58d5a8ef-adcc-4303-9254-9eb548b001cf`; uploaded GLB SHA-256 `ade6a21e587f373c164ceeffe7d1c1dd8115294bbda6ea9e77206f142a6f4c70`.
- C — multiview/high-quality AI realization: pending controlled generation.
- All three remain realizations of REV A; none creates REV B.

## Authority split
Game Lab owns dimensions, connectors, snap points, rotation axes, collisions, signal paths and gameplay state.
The approved Design Datasheet owns visual intent and silhouette.
AI generation may create visual geometry and materials only; it never defines gameplay semantics.
Blender owns runtime mesh validation/optimization, not replacement gameplay modeling.

## Gate sequence
1. Gate 0: Design Datasheet OWNER PASS.
2. Generate candidate visual asset with recorded provenance.
3. Technical mesh QA and runtime-budget inspection.
4. Datasheet conformance review.
5. Publish candidate plus QA sidecar to Viewer.
6. OWNER PASS/FIX in Viewer.
7. Only after PASS may a candidate be promoted to game integration.
## Required provenance receipt
Record: design ID/revision, provider, provider model/version when exposed, task/job ID, generation timestamp, source-view identities, source ownership, quality/usage/export settings, seeds when exposed, requested face budget, PBR/quad/retopo settings, original output hash and runtime output hash.
Provider URLs are transport/cache locations, never the sole Cloverwood master.

## C multiview input contract
Use one consistent object identity across FRONT, LEFT, BACK and RIGHT references.
Keep proportions, appendages, couplers, chamber, coil, arm joints and gripper mechanically consistent between views.
Prefer neutral framing and consistent illumination; avoid perspective changes that imply different geometry.
Generate a high-detail master first. Runtime reduction is a separate measured step.

## Runtime QA
Report mesh/material count, vertices, polygons/triangles, bounds/scale, origin/orientation, UV presence, texture/PBR channels, normals, degenerate geometry, non-manifold/open boundaries where meaningful, and file size.
Preserve an untouched master before optimization.
Derive LOD/runtime budgets from measured iPhone 16 and iPhone 11 performance rather than an arbitrary universal number.

## Review statuses
`technicalStatus`: PASS/FAIL — machine validity only.
`designConformance`: PASS/FIX — comparison with approved REV A datasheet.
`ownerReviewStatus`: PENDING/PASS/FIX — only the owner may resolve this gate.
Technical PASS must never imply design or owner PASS.

## Promotion rule
Do not merge or ship this experimental capability merely because generation succeeds.
Promote only after an end-to-end candidate reaches Viewer, receives OWNER PASS, integrates behind deterministic Game Lab semantics, and survives device QA.
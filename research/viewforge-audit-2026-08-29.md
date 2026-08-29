# ViewForge and reference-to-3D audit — 2026-08-29

## Executive finding

The library now has a real, tested bridge from orthographic evidence to a measurable Blender mesh. This removes Codex's worst failure mode—free-form guessing from a turnaround sheet—for the outer silhouette. It does not yet solve calibrated perspective, hidden/concave features, smooth surface inference, topology, materials or engine-ready optimization.

The correct strategy is staged reconstruction, not one-shot image-to-mesh generation. Every later stage must preserve which geometry is measured, silhouette-supported or estimated.

## Proven today

| Capability | Evidence | Status |
|---|---|---|
| Shared front/side/top sheet | One source PGM with three manifest crop rectangles | Tested |
| Uniform-background segmentation | Four-corner RGB estimate plus explicit tolerance | Tested on fixture; intentionally limited |
| Separate dark/light/alpha masks | Supported by manifest and prior smoke run | Implemented |
| Dimensioned visual hull | 3-axis voxel intersection in declared metric dimensions | Tested |
| Input audit trail | Source size, requested crops, detected bounds and segmentation settings in JSON | Tested |
| Inspectable normalized masks | Exact reconstruction masks emitted as PGM | Tested |
| Numerical validation | Per-view reprojection IoU/missing/extra pixels | Tested at IoU 1.0 |
| Editable/runtime/Apple output | `.blend`, `.glb`, `.usdc` | Tested with Blender 5.2.1 LTS |
| Scale preservation | Exported GLB reimported as 2.0 × 1.0 × 1.5 m | Tested |
| Visual evidence | Orthographic front/side/top renders | Inspected |
| Source/mask/projection evidence | Enlarged per-view overlays with agreement, missing and extra classifications | Tested and inspected |
| Automated rejection | Configurable minimum per-view IoU, launcher-enforced nonzero exit and retained diagnostics | Tested with intentionally inconsistent fixture; launcher compensates for Blender 5.2 returning zero after a Python exception |
| Dimension-led calibration | Per-axis inclusive pixel anchors, physical dimension names, shared ledger IDs and scale ratios | Tested; conflicting cross-view ledger IDs are rejected |
| Codex discovery | Repo-local `reference-sheet-to-3d` skill | Validated |

## Remaining gaps

### P0 — trustworthy input calibration

1. Perspective/keystone correction for photographed drawings and non-orthographic sheets.
2. Connected-component filtering and explicit foreground/background seed points for noisy sheets; automatic segmentation must remain reviewable.
3. Additional negative tests for bad crops, object-at-corner backgrounds and empty intersections. Inconsistent views and conflicting ledger IDs already have failure fixtures.

### P1 — evidence-driven shape refinement

1. Parametric cutters for dimensioned holes, slots, wheel arches and through-bores; visual hull alone cannot recover concavity.
2. Cross-sections at declared stations for controlled curvature instead of generic smoothing.
3. Symmetry, repeated-part and assembly manifests with stable part IDs/pivots.
4. A FreeCAD/OpenSCAD master for a permissively licensed real datasheet, with automated dimensions and ViewForge comparison.
5. Texture/decal projection with provenance and occlusion review.

### P1 — game-ready derivative

1. Tested retopology/decimation recipe with silhouette error budget.
2. UV and bake fixture, tangent/normal validation, material slots and texture packing.
3. LOD generation measured by screen-space silhouette/material error.
4. Convex/compound collision proxies and articulation sockets.
5. Import presets and real runtime evidence in Godot, Unity, Unreal and RealityKit.

### P2 — broader capture routes

- Multi-photo photogrammetry/Object Capture route for objects that can be photographed around all sides.
- Character turnaround workflow with landmarks and manual deformation topology; visual hull is only a blockout.
- Neural single-image methods may propose class-C geometry, but cannot upgrade unknown depth into measured evidence.

## Next implementation order

1. Perspective correction and segmentation failure fixtures.
2. Dimension-led negative volumes and cross-sections.
3. Dimension-led negative volumes and cross-sections.
4. One real permissively licensed product reconstruction through CAD, ViewForge, Blender and engine import.
5. Game-ready LOD/collision/material derivative and Apple RealityKit validation.

## Acceptance rule

A generated model is not complete because it looks plausible. Completion requires source identity, coordinate and dimension contracts, reviewed masks, numerical reprojection, disclosed unknown geometry, final-format validation and a real engine/device render appropriate to the claimed use.

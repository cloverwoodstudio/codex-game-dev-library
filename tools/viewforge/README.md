# ViewForge — calibrated views to a 3D starting mesh

Reviewed: 2026-08-29

ViewForge turns calibrated front/side/top views into a deterministic 3D visual hull in Blender. The views can be separate masks or pixel crops from one shared reference sheet. It is designed for Codex workflows where a reference sheet exists but free-form mesh generation would otherwise become guesswork.

It does **not** infer hidden concavities, materials, mechanisms or anatomy. Instead it creates the largest volume consistent with every supplied silhouette, reports reprojection agreement and input provenance, and exports an editable `.blend`, runtime `.glb`, Apple-oriented `.usdc`, normalized masks, source/mask/projection overlays, validation JSON and orthographic renders. The result is a grounded blockout for deliberate refinement, not a finished production asset.

## Quick start

Requires Blender 5.2 LTS or a compatible version on `PATH`.

```sh
tools/viewforge/viewforge.sh tools/viewforge/examples/crate/viewforge.json
```

Outputs are written to the manifest's `output_directory`. Run the smoke test with:

```sh
tools/viewforge/tests/smoke.sh
```

## Input contract

- Use orthographic or perspective-corrected front, side and top masks.
- Every view must describe the same variant, pose and articulation state.
- Calibrate all views against the same real dimensions; never stretch each view independently by eye.
- Use alpha masks, dark/light silhouettes with an explicit threshold, or `background` mode for a uniformly colored sheet.
- A shared sheet can be referenced by all three views with top-left pixel `crop` rectangles. The example exercises this route.
- Remove unrelated text, dimensions and view labels. ViewForge automatically crops each mask to its non-background bounds, then maps that silhouette to the declared object dimensions.
- `background` mode estimates the background from the four crop corners and uses `background_tolerance` as normalized RGB distance. It is intentionally simple and auditable: do not use it when the object touches a corner, the backdrop is nonuniform, shadows merge with the object or foreground/background colors overlap. Supply reviewed masks instead.
- The model coordinate contract is `+X = right`, `+Y = back`, `+Z = up`; the origin is centered on the ground plane.
- Front image maps horizontal to X and vertical to Z. Side maps horizontal to Y and vertical to Z. Top maps horizontal to X and vertical to Y.

See `manifest.schema.json` and the example manifest. Resolution controls the reconstruction grid, not the output image size. Start around 32–64 cells on the longest axis; high resolutions grow memory and face counts cubically.

ViewForge writes the exact normalized masks used for reconstruction under `output/masks/`. It also writes enlarged review images under `output/overlays/`: the resampled source is dimmed, green means source mask and hull projection agree, red means requested silhouette is missing from the hull, and magenta means the hull projects outside the mask. Inspect these before trusting a good numerical score; a consistently wrong mask can still reproject perfectly.

## What the report means

For each view, ViewForge projects occupied voxels back to 2D and compares the projection with the input mask:

- `iou`: intersection-over-union; `1.0` is exact silhouette agreement.
- `missing_pixels`: mask regions unsupported by the final three-view intersection. These expose inconsistent drawings, pose differences or calibration problems.
- `extra_pixels`: projected regions outside the mask; normally zero because the hull is carved by every view.

A high IoU proves silhouette consistency at the chosen grid resolution. It does not prove surface curvature or hidden geometry. Record such choices as estimated in the dimension ledger.

`quality_gate.minimum_iou` sets the required per-view IoU from 0 through 1 and defaults to `0.95`. ViewForge writes all diagnostic outputs and `validation.json`, then exits unsuccessfully when any view falls below the threshold. This makes bad input stop an automated Codex workflow while preserving the evidence needed to repair it. The `examples/inconsistent/` fixture deliberately exercises this failure path.

## Production continuation

1. Require `quality_gate.passed`, then review the three overlays, renders and validation report.
2. Correct crop, orientation, thresholds and real dimensions before sculpting.
3. Add known holes/concavities with parametric cutters driven by the dimension ledger.
4. Use Blender shrinkwrap/sculpt tools for supported curvature; keep the hull as evidence.
5. Retopologize deforming objects manually. Blender documents that voxel remesh is not animation topology.
6. Build UVs, materials, LODs, collision and pivots as a separate game-ready derivative.
7. Validate USD with `usdchecker` when available, then inspect in Reality Composer Pro/RealityKit. Apple notes that structural USD validation cannot catch visual/runtime differences.

## Primary sources

- [Laurentini, “The Visual Hull Concept for Silhouette-Based Image Understanding”](https://doi.org/10.1109/34.273735)
- [Blender remeshing and retopology](https://docs.blender.org/manual/en/latest/modeling/meshes/retopology.html)
- [Khronos real-time asset creation guidelines](https://github.com/KhronosGroup/3DC-Asset-Creation/blob/main/asset-creation-guidelines/RealtimeAssetCreationGuidelines.md)
- [Apple: Creating USD files for Apple devices](https://developer.apple.com/documentation/usd/creating-usd-files-for-apple-devices)
- [Reality Composer Pro](https://developer.apple.com/documentation/realitycomposerpro)

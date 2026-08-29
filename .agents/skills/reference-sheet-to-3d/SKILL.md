---
name: reference-sheet-to-3d
description: Reconstruct a measurable 3D starting mesh from front, side and top reference images, turnaround sheets, blueprints or datasheets. Use when Codex must create or validate a game/app 3D object from image views; do not use for unconstrained text-to-3D or when only a single uncalibrated perspective image exists.
---

# Reference sheet to 3D

Use the repository's `tools/viewforge/` pipeline to create an evidence-constrained visual hull before manual Blender modeling.

## Establish whether reconstruction is possible

1. Read `guides/art/datasheet-to-3d.md` and classify the requested accuracy as A, B or C.
2. Identify exact object variant, pose, units, overall width/depth/height and source/license.
3. Confirm front, side and top views are orthographic or perspective-corrected, share one scale and show the same pose.
4. If a critical dimension or view is absent, label it unknown and ask for evidence when it materially changes the result. Do not silently invent it.
5. A single ordinary photograph cannot determine hidden depth. Use it only for a disclosed class-C approximation, or request more views/photos for photogrammetry.

## Run the grounded blockout

1. Preserve source images unchanged. Identify top-left pixel crop rectangles for front, side and top. Use reviewed masks for difficult backgrounds; use `background` mode only for uniform backgrounds with clear corner samples.
2. Copy `tools/viewforge/examples/crate/viewforge.json` into the asset working directory and update paths, crops, dimensions, units, resolution, flips and segmentation settings.
3. Run `tools/viewforge/viewforge.sh <manifest>`.
4. Require `validation.json` to report `quality_gate.passed: true`; inspect `output/overlays/`, `output/masks/` and front/side/top renders. Green overlay pixels agree, red mask pixels are missing from the hull, and magenta pixels are extra projection. Do not continue if the hull is empty, masks are wrong or important views have poor IoU; fix crops, calibration, orientation or segmentation first.
5. Keep the generated hull as evidence. Refine a duplicate with dimension-led parametric cutters, supported curvature, retopology, UVs, materials, collision and LODs.
6. Run the final asset in its target engine or RealityKit renderer. For Apple targets, export/validate USD and load the `apple-platform-development` skill.

## Claims and stopping conditions

- The visual hull is the largest volume consistent with supplied silhouettes. It cannot recover hidden holes, concavities or true surface curvature.
- Never call the raw hull game-ready, animation-ready or engineering-accurate.
- For deforming characters, manual topology following deformation flow remains required.
- Record every inferred feature as `estimated` in the dimension ledger and preserve the ViewForge manifest/report with asset provenance.
- Stop refinement when a requested critical feature is unsupported by evidence rather than optimizing a guess.

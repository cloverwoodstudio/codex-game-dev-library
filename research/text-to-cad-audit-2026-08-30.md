# Text-to-CAD audit for Apple game assets

Reviewed: 2026-08-30

## Verdict

`earthtojake/text-to-cad` is useful for the library and for the lighthouse game,
but as a **parametric hard-surface factory**, not as a universal 3D artist. The
audited route produced a dimensionally controlled puzzle component and carried
it through STEP, GLB, strict USDZ validation and a real RealityKit load.

## Source and maintenance

- Source: https://github.com/earthtojake/text-to-cad
- Audited commit: `0e94cd1d2b5fa2013d89aa9504ecadcf16ce39f6`
- Published version: 0.4.28
- License: MIT, copyright Thompson Labs LLC
- Upstream description: agent skills for CAD, CAE and CAM.
- CAD implementation: `cadgen` plus build123d/OpenCascade; STEP is primary and
  STL, 3MF and native GLB are secondary exports.

The project is actively developed, but the audit pins one commit because main
is moving and the security policy supports only the latest release.

## What was actually tested

1. Installed upstream requirements in an isolated Python 3.14 environment.
2. Authored a parameterized four-way junction tile from a short CAD brief.
3. Generated STEP and upstream render/topology artifacts.
4. Ran facts/plane inspection and soundness validation.
5. Rendered and visually inspected an isometric snapshot.
6. Exported native GLB and STL.
7. Ran the repository asset-intake budget/provenance gate on GLB.
8. Converted GLB to USDC with Blender 5.2.1, packaged USDZ, and passed
   `usdchecker --arkit --strict`.
9. Loaded the USDZ in a compiled macOS RealityKit harness.

Measured result: 940 GLB triangles, one mesh, one material, no textures;
RealityKit bounds 0.092 × 0.010 × 0.092 m.

## Strengths

- Dimensions and feature intent remain editable Python parameters.
- STEP provides a better source artifact than guessing directly in a mesh.
- Validation distinguishes topology success from closed, positive-volume
  geometry and requires visual snapshot review.
- Native GLB is already Y-up and metre-scaled, avoiding a common Apple import
  error.
- The workflow is deterministic enough to create families of compatible tiles
  and mechanical props from shared parameters.

## Costs and risks

- The isolated environment occupied about 1.4 GB because OpenCascade/VTK and
  snapshot-browser dependencies are substantial.
- Snapshot rendering needs a separate Playwright Chromium download.
- The first cold generation paid roughly 23 seconds of Python/CAD imports;
  actual geometry construction was only tens of milliseconds.
- Relative secondary export paths resolve beside the model and can create an
  unexpected nested directory; use absolute paths.
- The local viewer is unauthenticated and must stay on loopback.
- Valid CAD is not automatically beautiful, game-optimized or animation-ready.
  UVs, textures, artistic bevel language, materials, LODs, collisions and
  device performance remain separate gates.

## Adoption decision

Keep the tested fixture and evidence in the knowledge base. Do not vendor the
whole upstream repository or globally install its plugin yet. For production,
pin an upstream commit/release and expose the CAD skill to Codex through the
official plugin/skill installation route only when a concrete hard-surface
asset batch begins. Continue to route each derivative through asset intake,
Blender harmonization where needed, strict USDZ validation and RealityKit.

# Image-to-3D versus parametric CAD for Codex game assets

Reviewed: 2026-08-30

## Question

Can Codex reliably create game-ready 3D assets from an image, or should it
generate precise geometry through Python CAD?

The two routes solve different problems. Treating either as a universal 3D
solution produces misleading results.

## Sources reviewed

- Aident: https://aident.ai/blog/turn-image-into-3d-model-codex-fal
- fal Hunyuan 3D Rapid API: https://fal.ai/models/fal-ai/hunyuan-3d/v3.1/rapid/image-to-3d/api
- Safal Sharma: https://safalsharma.com.np/blog/building-3d-models-using-codex-and-build123d
- build123d: https://github.com/gumyr/build123d
- Tested Text-to-CAD audit: `text-to-cad-audit-2026-08-30.md`

The two blog posts are experience reports. Provider schemas, the build123d
repository and retained local tests are stronger evidence for capability
claims.

## Route A: single image to 3D through fal/Hunyuan

Codex does not reconstruct the mesh itself. It prepares the input, calls an
external image-to-3D provider and reviews the returned model. The reviewed fal
schema accepts one front-view JPG, PNG or WebP image from 128 to 5,000 pixels
and up to 8 MB. It offers optional PBR generation or a geometry-only mode and
returns generated model files such as GLB/OBJ, with USDZ listed among available
model URL types.

The hidden back, underside, physical scale, wall thickness and internal
structure are not observed. They are inferred. Therefore a convincing front
view is not reconstruction evidence for the complete object.

Use this route for:

- rapid blockouts and concept validation;
- decorative rocks, wreckage, statues and background props;
- disposable candidates that will pass through visual, topology and runtime
  gates before adoption.

Do not directly trust it for:

- dimensioned puzzle connectors or modular interfaces;
- replacement parts, manufacturing or print tolerances;
- animation-ready character topology;
- collision meshes, polygon budgets, UV quality or hidden surfaces;
- commercial use until the exact provider/output terms are recorded.

The provider call spends credits and uploads an image to an external service.
Re-list the active model and price, preflight one bounded request, keep secrets
out of prompts/history, record input/options/seed, and require explicit cost
authorization before generation.

Status in this library: `source-reviewed`, not runtime-tested. Do not promote
image-to-3D to a reusable capability until an exact paid run, artifact intake,
multi-view visual review, topology report, Apple conversion and RealityKit load
are retained.

## Route B: Codex plus build123d/Text-to-CAD

Codex writes parametric Python that constructs boundary-representation CAD
geometry over OpenCascade. Dimensions and feature intent remain editable in
source, and STEP is a stronger master artifact than an unconstrained generated
mesh.

The Safal Sharma article correctly identifies lower prompt/context overhead and
the value of CAD-as-code, but its examples are exploratory. The author reports
that the initial phone stand's intended function was unclear, and a logo
extrusion does not establish general image-to-3D reconstruction.

The route is also not dependency-free or artistically complete. The audited
Text-to-CAD environment occupied about 1.4 GB, snapshot review required a
browser runtime, and Blender was still required for the tested USDC/USDZ path.

Use this route for:

- tiles, housings, pipes, gears, brackets and rails;
- architectural and modular pieces with measurable sockets;
- families of compatible objects driven by shared parameters;
- technical objects that need deterministic regeneration and validation.

The retained Text-to-CAD fixture passed closed-solid validation, native GLB
intake, strict ARKit USDZ checking and a macOS RealityKit load. That evidence
does not prove organic modeling, rich materials, UV art, animation, collision
fitness or physical-iPhone performance.

## Recommended hybrid asset ladder

1. Search exact licensed asset libraries first.
2. Use kitbashing when compatible licensed parts exist.
3. Use Text-to-CAD/build123d for dimensioned hard-surface geometry.
4. Use image-to-3D only for a bounded visual candidate when hidden geometry can
   remain inferred.
5. Use Blender for cleanup, UVs, retopology, material work, baking, LOD and
   collision candidates.
6. Run repository asset intake and preserve provider, license and input
   provenance.
7. Export USD/pack USDZ, run `usdchecker --arkit --strict`, then load in
   RealityKit.
8. Inspect the asset in the actual game composition and profile on the target
   iPhone before production approval.

## Decision for the lighthouse game

- Puzzle topology, connector seams, modular decks and mechanical fixtures:
  Text-to-CAD/build123d.
- Background rocks, wreckage and non-interactive decorative candidates:
  image-to-3D may be trialled under a one-generation cost cap.
- Lighthouse and hero landmarks: licensed asset or controlled hybrid workflow;
  never approve from one generated front view.
- Final beauty comes from materials, lighting, composition and authored detail,
  not from CAD validity or a single AI generation alone.

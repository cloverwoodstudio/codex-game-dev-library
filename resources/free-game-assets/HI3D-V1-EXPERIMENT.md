# Hi3D v1.0 — experimental AI 3D geometry refinement

**Reviewed:** 2026-10-23  
**Status:** SOURCE REGISTERED / EXPERIMENTAL / LICENSE REVIEW HOLD  
**Catalog ID:** `hi3d-v1-geometry-refinement`

## Primary evidence
- Announcement: https://www.hi3d.ai/hi3d-1-0-open-source
- Official source and documented API: https://github.com/hi3d-official/Hi3Dv1.0
- Official model artifacts: https://huggingface.co/hi3d-official/Hi3Dv1.0
- Binding license: https://github.com/hi3d-official/Hi3Dv1.0/blob/main/LICENSE
- README-linked demo: https://huggingface.co/spaces/ilcve21/Sparc3D — named **Sparc3D**; this is not sufficient evidence that it runs the exact Hi3D v1.0 weights. Verify the Space implementation/version before labeling a result "Hi3D 1.0".

## What it does and does not
Hi3D v1.0 **refines geometry** from a reference image of the same object and an existing **coarse mesh**. It does not by itself generate the coarse mesh, textures, UVs, PBR materials, rig, animation or a game-ready optimized model. The optional README Hunyuan coarse-generation example is a **separate third-party dependency** with its own terms.

Supported nominal refinement resolutions: **512, 1024, 1536**. These represent sparse extraction grids, **not** triangle budgets. The resulting mesh is normalized and re-centered; world scale/original placement must be checked explicitly. The original coarse structure affects accuracy; hidden surfaces are inferred rather than ground truth.

## Runtime reality
Official setup: **Linux, Python 3.10, NVIDIA GPU compute capability >= 8.0, CUDA 12.0–12.5**, PyTorch/flash-attn/spconv. No official Metal/MPS or CPU inference path. A 96 GB NVIDIA H20 was used for the highest 1536 mode; there is **no published validated minimum VRAM** for other configurations. The Mac mini M4 can inspect repository metadata and finished GLBs, but **cannot run official Hi3D v1.0 inference locally**. Do not install the CUDA stack on the Mac, download checkpoints, or rent a GPU without separate authorization.

## License gate
License: **Hi3D Open License Agreement Version 1.0** (custom; NOT MIT/Apache for all components). Commercial integrations using/containing Hi3D materials have notices and **Powered by Hi3D 1.0** obligations under the Agreement. Separate license/notification requirements are tied to stated MAU/revenue thresholds. The license defines **standalone outputs** differently: a generated/edited mesh with no embedded Hi3D materials or model derivative does not by itself trigger the integration branding/scale obligations, though inputs and third-party rights still matter. The bundled Sparc3D and optional Hunyuan dependencies are **not all relicensed** by this agreement.

**Policy:** `commercial_game_use=verify-item`, `attribution=per-item`. No Hi3D-generated asset or inference service is production-approved by adding this URL. Preserve exact input rights, license version, generation method, source/model revision, and credits where needed.

## Comparative acceptance protocol — no inference executed

Choose **three owner-cleared image + matching coarse-GLB pairs**. Do not borrow commercial samples without permission. Prefer:
1. **Rigid prop:** a container or small architectural object — preserve silhouette, holes and repeated details.
2. **Organic static prop:** a rock/root/sculpted object — inspect volume, smoothness, thin features and back-view guesswork.
3. **Animation-sensitive candidate:** a simple riggable creature/humanoid mesh — measure topology and retopology/rigging effort; no animation claim.

For every test, keep identical inputs and orientation across a baseline coarse mesh and each model under comparison. Record tool/build/revision, seed, prompt/settings, elapsed run time, GPU VRAM, mesh file size, vertices/faces, connected components, manifold status, normals, UV/material presence, render angles (front, back, left, right, top) and exact input reference. Check original scale/centroid. Rate silhouette, geometry fidelity, hidden view plausibility, Blender cleanup, safe use rights and iPhone GLB frame-time/memory on the **optimized derivative**.

**Decision gates:** source/license validation → reproducible geometry improvement → retopology/material/rig tasks quantified → game export QA → iPhone device QA → explicit owner review. Any input/output mismatch, topology collapse, unknown license or missing authorship blocks production integration.

## Security and rollout
Metadata/link only; no model files or checkpoint mirrors, no provider API credentials, no third-party ZIP/GLB/PNG copied into this library. This document does not authorize an online inference submission, cloud GPU spend, MERGE or DEPLOY.

At this stage only the **tool listing and benchmark plan** exist. No quality score, real inference result or Mac runtime PASS is claimed.

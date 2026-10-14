# CODEX GAME DEV 03 — Tripo Studio → Blender → Unity/Godot

Reviewed: 2026-10-14
Status: DRAFT / QA PILOT. No MERGE, DEPLOY, image generation, Studio generation or Studio/API credits spent.

## Authority and required workflow

This augments, never replaces:
- Project Bible / AGENTS.md and existing game-specific technical authority;
- docs/AI_VISUAL_ASSET_PIPELINE.md Gate 0: owner-approved Design Datasheet;
- provider MASTER is immutable, GAME derivative is separate;
- Asset Viewer and OWNER visual PASS/FIX are independent from technical QA.

### Tripo Studio only — billing safety
Our source of generated geometry must be **Tripo Studio web workspace**
https://studio.tripo3d.ai/ , **not** Tripo Developer API or Tripo CLI.
Tripo explicitly states Studio credits and API credits cannot be combined.

Chrome on the Mac has Tripo Studio tabs open. This confirms open tabs,
NOT that Studio is logged in, the current credit balance, plan or a
specific export's origin. No credentials, account cookies or Studio
billing details are used by these local scripts.

A Tripo Blender DCC Bridge addon (installed v1.0.34 in Blender 5.2)
was found under the Mac's user addons. Studio supports browser DCC
Bridge and ordinary downloads. The Bridge was discovered read-only; no
live authenticated transfer was performed in this pilot.

**Production path:**
1. Owner-approved Design Datasheet / useful image multiview.
2. In Tripo Studio, generate or select a model with available Studio
   credits. Confirm actual cost, mode, plan/rights, and model revision.
   Do not start chargeable AI tasks automatically from this QA script.
3. Download GLB as source MASTER (PBR embedded) or FBX + texture folder
   for rigged Unity character. Or manually use already installed
   Studio → Blender DCC Bridge, keeping original exported source bytes.
4. Save MASTER and SHA-256. Optional Studio manifest is owner
   evidence/attestation; metadata alone cannot cryptographically prove
   Studio attribution, account credits or commercial licensing.
5. Create independent GAME candidate through *separately authorized*
   retopology, rig cleanup and texture baking. Never overwrite MASTER.
6. Use Blender QA on MASTER and GAME independently, with explicit
   different triangle/material budgets. Review geometry scale, UVs,
   skinning, animation clips, texture maps and material behavior.
7. Isolated Unity/Godot import validation, real-engine render and on-device
   profiling. Only then Asset Viewer + OWNER PASS/FIX.
8. Only approved assets may enter a game's own branch and review workflow.

**Licensing gate:** a Studio free plan does not grant commercial use
according to Tripo's published guidance. Commercial rights require
checking the actual plan and terms **at generation time**. Recorded
owner evidence does not itself establish legal rights.

## Reusable read-only inspector

From the library root on the Mac:

    scripts/run_tripo_studio_qa.sh \
      --input "/absolute/TripoStudio/MASTER.glb" \
      --output "/Volumes/CLOVERWOOD_DEV/Development/CIReports/asset-qa-MASTER.json" \
      --max-triangles 100000 --max-materials 12 --require-uv

For a rigged optimized candidate:

    scripts/run_tripo_studio_qa.sh \
      --input "/absolute/TripoStudio/GAME.glb" \
      --output "/Volumes/CLOVERWOOD_DEV/Development/CIReports/asset-qa-GAME.json" \
      --max-triangles 25000 --max-materials 8 --require-uv \
      --expect-rig --expect-animation \
      --manifest "/absolute/owner-asset-manifest.json"

The output path must be new in an existing directory. The script
refuses to overwrite a report or input, imports into a factory-clean
headless Blender with automatic script execution disabled, hashes
the original source before and after, and writes JSON evidence only.
Each invocation uses the shared disk-guarded exclusive-Mac wrapper.
The counters are factual checks; no render, sculpt, regeneration or
optimization is performed by this tool.

Template: templates/TRIPO_STUDIO_ASSET_MANIFEST.template.json.
Fill real SHA-256, unique asset ID, engine, export method, licensing
evidence and Studio reference. Unknown source/license must not be
promoted merely because a filename mentions Tripo.

## Live Mac audit / explicit evidence

- macOS Mac mini: Blender 5.2.1 LTS; Tripo Blender Bridge found v1.0.34.
- **Existing file**, not newly generated:
  Downloads/Mara_Voss_Tripo_10K_RIGGED_IDLE_WALK_RUN.glb
- Blender import QA: **PASS_WITH_WARNINGS** — 2 meshes, 20,262 vertices,
  **18,686 triangles**, 1 material, 2 UV layers, 1 armature, **65 bones**,
  20,220 weighted vertices, 3 actions (idle, walk, run), 3 image
  datablocks, zero non-finite coordinates. Input SHA unchanged.
- Source SHA: c57f95cb26859a3c1a0ad35ab03140f15d218f1ea415af4a097ef860daf9a099
- Report: /Volumes/CLOVERWOOD_DEV/Development/CIReports/TRIPO_STUDIO_GAMEDEV_03/MARA_VOSS_EXISTING_IMPORT_QA.json
- Provenance/licence: **HOLD**, Studio origin and subscription rights not
  independently verified for this historical model.
- Existing BETWEEN Blue FBX: Blender FBX parser PASS; 52,000 triangles,
  budget 25,000 => **FIX** (intended negative gate). No source edit.
- Godot 4.7.2 independent import: existing Mara GLB copied into
  /Volumes/CLOVERWOOD_DEV/Development/CIReports/TRIPO_STUDIO_GAMEDEV_03/godot_import_pilot
  and headless imported. Scene instantiated: 5 nodes, 1 MeshInstance3D,
  1 Skeleton3D, 1 AnimationPlayer. This is import QA, **not**
  real iPhone performance/rig visual approval.
- Runner cleanup receipts PASS; no production-game files touched.

## Known limits
- Tripo Studio user balance and live DCC Bridge session are not verified;
  no Studio credit was spent in this pilot.
- The importer does not verify skin deformation during motion, pose
  correspondence, correct world scale, visually faithful PBR, collider
  shape, proper LODs, target iPhone FPS or licensing.
- API or CLI generation is prohibited for this route. No automatic
  paid provider calls / purchased credits and no hidden account keys.
- Unity live import is a separate gate; the script can inspect FBX/GLB
  intended for Unity but doesn't claim to have imported it into a real
  Unity Editor in this pilot.
- Blender addon auto-execution is disabled during QA and plugin code
  is not deliberately loaded. Running arbitrary third-party assets
  within a desktop DCC still has residual risk; use isolated projects.

## Official sources
- Tripo Studio workspace: https://studio.tripo3d.ai/
- Tripo Studio DCC Bridge/manual exports:
  https://www.tripo3d.ai/help/features/how-to-export-and-import-to-dcc-tools
- Tripo Studio subscription and API separation:
  https://www.tripo3d.ai/de/help/api-plugins/tripo-studiotripo-api
- Tripo rig and animation support:
  https://www.tripo3d.ai/help/features/can-tripo-create-animation-ready-3d-models

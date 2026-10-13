# Eterea Blender Tools — Cloverwood isolated pilot

Reviewed: 2026-10-13
Status: **local technical pilot PASS; not approved for production or global installation**
Scope: 3D tooling only. No game repository, master asset, CI configuration, TestFlight, deployment, or merge changed.

## Source and license

- Author page: https://etereaestudios.com/resources/blender-resources/
- Source/release: https://github.com/Eterea/blender_addons
- Version tested: **v1.7.0** (release 2026-10-07): https://github.com/Eterea/blender_addons/releases/tag/v1.7.0
- Release archive: `etr_blender_tools-1.7.0.zip`
- GitHub release SHA-256 and independently measured download SHA-256: `e3caab4aa0ecb9100a0e774e67041961d219bf17f3cfe46ff7d2d456550ebf78`.
- Blender extension manifest: minimum Blender **5.2.0**; code published as **GPL-3.0-or-later**.
- Manual: https://github.com/Eterea/blender_addons/blob/main/etr_blender_tools_docs/README.md
- License note: do not vendor this add-on's code into proprietary game/app repositories without a separate legal/compatibility review. Use as an independent authoring tool only where permitted.

## Verified host and isolation

- Tested on CLOVERWOOD Mac mini via Desktop Commander; Blender **5.2.1 LTS**.
- Preserved pilot root: `/Volumes/CLOVERWOOD_DEV/Pilots/EtereaBlenderTools-01/`.
- Original source model never edited. Only a copy of Block Bouncer's `table_cardboard.glb` was imported/exported.
- Extension extracted into pilot-local `vendor/` and registered at runtime using `bpy` in a Blender **factory-startup background process** with an isolated configuration directory. **No global user profile installation**.
- Static screening of included Python files checked for direct network/system-process execution patterns; none observed. This is not a comprehensive third-party security audit.
- Executed the final run through the library's mandatory `scripts/cloverwood-local-run.sh` wrapper, with `CLOVERWOOD_EXCLUSIVE_MAC=1`. Exit 0, cleanup PASS, with free space recorded before/after. Preserve host receipt in `reports/cloverwood_run_receipt.txt`.

## Actual tests (5/5 PASS)

1. Runtime extension registration: expected operators exposed.
2. `Round Near-Integer Values`: location + scale near integers snapped precisely, scale `5.01` remained unchanged.
3. `Batch Operate Attributes`: rename then delete selected custom attributes on **3** synthetic mesh objects.
4. `Join Equalizing Bevels`: joined **2** weighted-bevel synthetic meshes; resulting modifier width **0.04**.
5. GLB roundtrip on a **copied Block Bouncer table**: **22 meshes**, **968 triangles** before and after. Source and source-copy SHA-256 both `d81692e5c459fd7df3e605857d5effca65b27bfeb4c9b429f2787313e9d1257d`. Round-trip output: **86,096 bytes**.

Test program: `qa/blender_pilot_01.py` under the pilot root.
Retained evidence: `reports/qa_results.json`, `reports/blender_qa.log`, `reports/cloverwood_run_receipt.txt`; test outputs under `work/`.

### Important evidence boundaries

- The **add-on operators were run only on synthetic meshes**; the copied Block Bouncer asset underwent a standard Blender GLB import/export test, not an Eterea geometry transformation.
- Triangle and mesh counts alone do **not** prove visual/material/UV/rig/animation parity. No visual owner review, in-engine render, target-device performance test, or asset promotion was performed.
- Blender 5.2.1 success does not automatically validate future Blender/add-on releases.
- The tool is an editor convenience kit, **not** a retopology, rigging, animation, export-validation, or Unity/Godot integration replacement.

## Suggested use by ChatGPT, OpenCode and other agents

1. Read the current project's authority and asset pipeline instructions; preserve approved MASTER and its provenance.
2. Confirm Blender >=5.2, check exact extension version and release SHA, and review source/license changes. Never silently install in the user's normal Blender profile.
3. Copy the working asset into an isolated external-disk pilot, not the release/game tree; keep original hash.
4. Pick the operator only when relevant: `Round Values` for transform drift; `Batch Operate Attributes` for attribute cleanup; `Join Equalizing Bevels` only on vetted objects with edge-weight-compatible modifiers.
5. Run local Blender commands with the shared Cloverwood wrapper, heavy lock, space gate and cleanup receipt.
6. Compare **mesh/material/UV/rig/animation** counts as applicable, export a separate candidate, render/view it in the *real game engine* and in Asset Viewer.
7. Obtain **OWNER PASS** before adoption or promotion. No autonomous install, game integration, OTA, MERGE or production bulk edits from this reference.

## Next validation gates

- Pilot a real *copy* of an approved Bevel-heavy prop with geometry/material comparison and visual review.
- Inspect behavior with shared data blocks, large models, rigs/animation and undo before any bulk operation.
- Optionally assess other tools in the author's reference collection; references are not runtime dependencies.

# Eterea Blender Tools visual pilot 02 — Block Bouncer bar stool

Reviewed: 2026-10-13
Status: **Technical PASS; owner visual approval PENDING**
Scope: isolated Mac-side review candidate only, no game/production asset change.

## Source and provenance

- Original Block Bouncer runtime prop: `bar_stool_cardboard.glb` in `/Volumes/CLOVERWOOD_DEV/Work/BB_CH3_VALIDATOR_PREVIEW_IOS_20261004/assets/props/`
- Original GLB SHA-256: `e1ca6e6f48b401387162755601dc6b4bf39773c6cff2de5e010351e34fd90237`
- Source-copy hash matches original. Untouched original: four mesh objects, 160 triangles, four UV layers, four materials.
- Tooling: Blender 5.2.1 LTS, Eterea Blender Tools 1.7.0, `object.join_equalizing_bevels`.
- Test archive checksum and tool license: see [pilot 01](../guides/art/eterea-blender-tools-pilot.md).

## Experiment performed

The GLB import had *disconnected corner vertices*, so no usable noncoplanar manifold edges for a weighted bevel. **Only inside the copied pilot candidate**, bmesh vertex welding at 0.00002 Blender units repaired topology for two objects:

| Copied object | Before weld | After weld | Weighted edges | Test Bevel width |
| --- | ---: | ---: | ---: | ---: |
| Foot | 72 vertices | 24 vertices | 24 | 0.019 |
| Stem | 48 vertices | 16 vertices | 24 | 0.011 |

Original asset did **not** contain Bevel modifiers; two modifiers were added to the *test copy* to give the tool a legitimate joining workload.

Captured three fixed-camera, actual Blender Cycles renders (same studio, lighting, material setup, 680×760):
1. Original untouched asset.
2. Foot and Stem with separate weighted Bevel modifiers.
3. Eterea Join Equalizing Bevels result: Foot and Stem merged into one mesh with maximum Bevel width 0.019 and proportionally scaled edge weights.

## Results and verification

- Operator finished; candidate has **three meshes** (versus four in source).
- The control (separate Bevel modifiers) and Eterea-joined evaluated geometry both have **656 triangles**.
- **Control and Eterea render pixels compare exactly** at the tested angle; `ffmpeg` PSNR reports **infinite** average / channel PSNR. PNG file byte hashes differ, which does not contradict the pixel equivalence.
- Exported candidate GLB: 49,740 bytes, SHA-256 `95c4779e1ec2e820e368e0c7bb72e147b58258f6ecf17e2328689e41d97c4221`.
- After export/reimport: **three meshes, 656 triangles**.
- Actual GLB JSON retains precisely the source material names: `CorrugatedEdge`, `PackingTape`, `RawCardboard`, `RedPaper`.
- Blender showed `.001` suffixes when re-importing into a process that already contained namesake materials; GLB JSON names confirmed to be unchanged.
- Local run used the library's mandatory run wrapper, host cleanup receipt **PASS**, with exclusive heavy-job lock.

## Owner inspection paths

Mac, preserved pilot evidence:
`/Volumes/CLOVERWOOD_DEV/Pilots/EtereaBlenderTools-01/visual-qa/`

Copied into Mac iCloud folder for owner's iPhone review:
`~/Library/Mobile Documents/com~apple~CloudDocs/Cloverwood Inbox/ETEREA_BLENDER_PILOT_01/`

First open: `00_POROVNANIE_ETEREA_PRED_PO.png` (labelled three-way side-by-side).
Also includes individual PNG renders, original source copy, experimental GLB candidate, editable Blender `.blend`, Slovak README and `visual_qa_report.json`. The SHA-256 of the contact sheet and candidate GLB matches between pilot and Mac iCloud folder. iCloud server/mobile synchronization is not independently confirmed.

## Guardrails and next gates

This result supports the specific technical claim that *for this modified copy and single fixed Blender view*, Eterea's bevel-join operator can preserve the rendered output while reducing object count. It does **not** prove geometry optimization, UV fidelity in every view, skeletal/animation handling, Godot/Unity renderer parity, runtime speed improvement, or visual owner approval.

The experiment adds bevels, raising triangles from 160 to 656; it is **not an optimization recommendation for this game prop**. Do not replace the approved Block Bouncer prop.

Remaining gates:
1. Owner reviews labelled render comparison and candidate GLB in Asset Viewer or Blender; marks PASS/FIX.
2. If owner wants adoption, separately test artifact from the approved project at more angles, UV/material parity and target-engine render/performance.
3. No MERGE, auto-install, production asset overwrite or OTA without explicit authorization.

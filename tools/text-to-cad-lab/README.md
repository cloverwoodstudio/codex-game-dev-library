# Text-to-CAD Apple game-asset lab

Reviewed: 2026-08-30

This lab evaluates the MIT-licensed
[`earthtojake/text-to-cad`](https://github.com/earthtojake/text-to-cad) CAD skill
at pinned commit `0e94cd1d2b5fa2013d89aa9504ecadcf16ce39f6` (version 0.4.28).
It proves one hard-surface route:

```text
plain-language CAD brief -> build123d source -> validated STEP
-> native Y-up/metre GLB -> Blender USDC -> strict USDZ
-> RealityKit load on macOS
```

The fixture is a 92 × 92 × 10 mm four-way junction tile for the lighthouse
puzzle. Its dimensions and channels are named parameters in
`models/lighthouse_junction.step.py`; generated files are derivatives.

## Evidence from the audited run

- STEP validation: one closed, positive-volume solid; 92 × 92 × 10 mm.
- Native GLB intake: 940 triangles, one mesh, one material, no textures.
- Apple packaging: `usdchecker --arkit --strict` passed.
- RealityKit: USDZ loaded; bounds were 0.092 × 0.010 × 0.092 metres.
- Visual review: `evidence/preview.png`.

The retained machine reports are in `evidence/`. Large/generated render caches,
executables and final interchange binaries should remain outside normal source
review; regenerate them from the Python model where practical.

## Reproduction contract

Use an isolated environment. The audited install used Python 3.14 and:

```text
cadgen==0.4.28
playwright==1.62.0
```

Clone the pinned upstream source, create a virtual environment, install
`skills/cad/requirements.txt`, and install Playwright Chromium for snapshots.
Run the upstream CAD commands from this repository root so target paths resolve
against this workspace:

```bash
python <cad-skill>/scripts/gen \
  tools/text-to-cad-lab/models/lighthouse_junction.step.py --write
python <cad-skill>/scripts/inspect validate \
  tools/text-to-cad-lab/models/lighthouse_junction.step.py
python <cad-skill>/scripts/snapshot \
  --input tools/text-to-cad-lab/models/lighthouse_junction.step.py \
  --output /absolute/path/to/lighthouse_junction_iso.png --camera iso
python <cad-skill>/scripts/export \
  tools/text-to-cad-lab/models/lighthouse_junction.step.py \
  --glb /absolute/path/to/lighthouse_junction.glb
```

Use absolute secondary-output paths: upstream resolves a relative export path
beside the model rather than from the shell working directory.

## Decision boundary

Use this route for measurable hard-surface assets: puzzle tiles, housings,
brackets, pipes, gears, rails, doors, architectural modules and mechanical
landmarks. It is not an autonomous production-art solution for creatures,
foliage, cloth, sculpted characters, deformation topology, UV art or rich PBR
materials. CAD geometry still needs art direction, material work, LOD/collision
review and target-device profiling before shipping.

The upstream viewer is an unauthenticated local tool whose documented trust
boundary is loopback. Never expose it on a non-loopback address without adding
authentication. Only the latest upstream release receives security fixes.

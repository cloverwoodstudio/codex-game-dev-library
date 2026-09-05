# Premium Blender → USDZ → RealityKit workflow

Reviewed: 2026-09-05

## Purpose

Use this workflow for final game-ready models whose materials, silhouette and animation must survive close inspection on iPhone or iPad. The workflow is code-reproducible: a committed Blender Python generator is the editable source of truth, not a hand-edited binary export.

## Core contract

Before modelling, define a small asset contract shared by art and runtime:

- world axes and unit scale;
- ground or mounting datum;
- connector/pipe centreline datum;
- maximum footprint and height;
- stable root and state-node names;
- dormant, active, failed and reduced-motion states;
- which geometry belongs to the asset and which belongs to the game runtime.

Treat these values as one system. Never repair a single asset by eye while neighbouring assets continue to use another datum.

## Production principles

1. The function must be readable from silhouette before labels or colour.
2. Use one dominant mass, one supporting mass and one state indicator.
3. Give every manufactured edge enough bevel to catch light at gameplay scale.
4. Use decorative detail only when it explains construction or function.
5. Animate named mechanical subassemblies; do not replace the authored body at runtime.
6. Keep the gameplay conductor continuous. Do not place a second transparent tube over the runtime tube.
7. Approve glass, reflections, transparency and motion on the target device, not from a still desktop render.

## Material language

Recommended starting ranges:

| Surface | Metallic | Roughness | Notes |
| --- | ---: | ---: | --- |
| Aged bronze | 0.85–0.95 | 0.16–0.26 | Dark body with warm reflected highlights |
| Warm gold/brass | 0.85–0.95 | 0.10–0.18 | Restrained functional accent, not yellow paint |
| Optical glass | 0 | 0.02–0.08 | Needs thickness, a visible boundary and a metal seat |
| Smoked diffuser | 0–0.1 | 0.18–0.30 | Hides internal crossings while dormant |
| Energy core | project-defined | low | Visible only when gameplay state says energy is present |

These are authoring starts, not universal constants. RealityKit under the shipping scene lighting is the final authority.

## Stable hierarchy

Names are an API between Blender/USD and runtime code. Name by mechanical role, not current colour.

```text
PremiumModule
├── LowerHousing
├── MainBody
├── StateChamberGlass
├── StateCore
├── MovingAssembly
├── Connector_north
│   ├── ConnectorCollar_north
│   └── ConnectorAccent_north
└── Connector_east
```

Put all direction-specific geometry below its directional group. Runtime can then remove an unused port by removing one subtree instead of hiding unrelated meshes individually.

## Reproducible authoring

The generator should:

- start from an empty scene;
- create shared PBR materials programmatically;
- construct named meshes and parent hierarchy deterministically;
- apply scale before export;
- add bevel and smoothing intentionally;
- generate a neutral studio preview;
- save an editable `.blend` and an intermediate USD scene.

Example invocation:

```sh
ASSET_WORK="$(mktemp -d /tmp/premium-module.XXXXXX)"
/Applications/Blender.app/Contents/MacOS/Blender --background \
  --python Tools/module-production/create_premium_module.py \
  -- "$ASSET_WORK"
```

If Blender cannot initialise its headless graphics backend, a deterministic USD authoring script may mirror the same hierarchy with native USD primitives. Treat it as an authoring fallback, never as runtime procedural art.

## USDZ packaging

Package the approved scene as an ARKit-compatible USDZ and clear accidental extended attributes:

```sh
/usr/bin/usdzip Assets/Runtime/Modules/module_runtime_v1.usdz \
  --arkitAsset "$ASSET_WORK/module_runtime_v1.usdc"
xattr -cr Assets/Runtime/Modules/module_runtime_v1.usdz
```

Inspect both package contents and authored hierarchy:

```sh
/usr/bin/usdzip Assets/Runtime/Modules/module_runtime_v1.usdz -l -
/usr/bin/usdcat "$ASSET_WORK/module_runtime_v1.usdc" | less
```

Reject the export when required nodes are absent, dormant emission is visible, directional groups are unstable, the connector datum drifts or ARKit packaging fails.

## RealityKit integration

- Bundle the USDZ in Copy Bundle Resources.
- Load one template and clone it recursively for instances.
- Recurse through imported wrapper entities when changing materials; the visible mesh is not guaranteed to be the root entity.
- Remove unused directional groups from their parent instead of depending on wrapper visibility.
- Preserve authored metal and glass materials unless a real state transition requires a material change.
- Drive named cores, shutters, rotors and indicators from the exact solver state.
- Provide a code-native primitive fallback only for load failure. Never use it for visual approval.

## State and animation

- **Dormant:** neutral glass, dark or smoked chamber, no energy colour.
- **Energized:** stable conductor colour plus a contained travelling impulse or mechanical response.
- **Interrupted:** illuminate only the physically reached path.
- **Reduced Motion:** show the same final mechanical and lighting state without travel or pulsing.

Avoid global brightness oscillation; it reads as scene flicker and changes the apparent colour of unrelated surfaces.

## Verification gate

Automate what can be deterministic:

- required USD node names;
- forbidden legacy geometry;
- asset membership in the Xcode project and bundle resources;
- runtime references to state nodes;
- shared datums and connector dimensions;
- unit and gameplay tests.

Then test on a physical device:

- default camera and maximum inspection zoom;
- dormant, active, failed and solved states;
- every supported connector direction;
- low oblique angles that expose floating or intersecting geometry;
- bright and dark environments;
- Reduced Motion enabled.

## Definition of done

The model ships only when its function is readable without help text, joins align, no route is doubled, the hierarchy is stable, automated checks pass, and materials plus motion are approved on the target device. Commit the generator and approved USDZ; keep disposable working exports out of version control.

## Primary sources

- [Blender manual](https://docs.blender.org/manual/en/latest/)
- [Apple: Creating USD files for Apple devices](https://developer.apple.com/documentation/usd/creating-usd-files-for-apple-devices)
- [Apple: Loading entities from a file](https://developer.apple.com/documentation/realitykit/loading-entities-from-a-file)
- [Khronos real-time asset creation guidelines](https://github.com/KhronosGroup/3DC-Asset-Creation/blob/main/asset-creation-guidelines/RealtimeAssetCreationGuidelines.md)

The pipeline details and acceptance gates were validated in a shipping-oriented RealityKit module family. Project-specific names and dimensions must remain in the consuming game's own asset contract.

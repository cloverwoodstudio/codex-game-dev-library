# Three.js procedural prototype → GLB workflow

Reviewed: 2026-09-05

## Purpose

Use Three.js to answer design questions quickly in an interactive browser:

- Is the silhouette distinct from related modules?
- Are connector positions and axes correct?
- Does a rotor, gear, shutter or lever move around the right pivot?
- Can an energy pulse visibly traverse the intended route?
- Are the object proportions readable from the expected camera?

This workflow is intentionally faster and more geometric than the premium production pipeline. Unless explicitly promoted and revalidated, its GLB is a prototype/reference asset rather than shipping art.

## Minimal structure

```text
threejs-prototype/
├── index.html
├── main.js
├── style.css
├── package.json
└── README.md
```

Use pinned package versions. Import controls and exporter from the matching Three.js release:

```js
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFExporter } from "three/addons/exporters/GLTFExporter.js";
```

## Modelling approach

1. Create the scene, physically reasonable lighting, tone mapping and a fixed inspection camera.
2. Build the object inside one named root `THREE.Group`.
3. Define a small shared material palette instead of creating materials ad hoc per mesh.
4. Establish connector centreline and footprint before detail modelling.
5. Build the dominant housing and unique mechanism first.
6. Use custom `Shape`/`ExtrudeGeometry` for identity geometry such as gear profiles rather than arrays of visually disconnected boxes.
7. Put each moving mechanism in its own named pivot group.
8. Keep the travelling pulse and lights separate from the exportable static housing when appropriate.

## Animation rules

- Rotate a gear around the axis normal to its face, not the model root.
- Animate pivot groups rather than recalculating mesh geometry every frame.
- Base motion on frame delta so speed is independent of refresh rate.
- Give every demonstration a pause/resume control.
- Model the energy pulse along the real connector centreline.
- Include a reset-camera action for repeatable review.

## Interactive review

The prototype page should provide:

- orbit and constrained zoom;
- start/stop mechanism animation;
- energy-flow demonstration;
- reset camera;
- visible status feedback;
- GLB export.

Check browser console errors, test all controls and capture one default-camera screenshot for comparison with the in-game module.

## GLB export

Export the named model root instead of the entire presentation scene:

```js
const exporter = new GLTFExporter();
const result = await exporter.parseAsync(modelRoot, {
  binary: true,
  onlyVisible: false
});

const blob = new Blob([result], { type: "model/gltf-binary" });
```

Verify the exported file starts with the glTF magic bytes and opens in an independent viewer. Preserve meaningful node names so a later production conversion can recover pivots and mechanical roles.

## Known limitations

- Browser PBR and Apple-device RealityKit rendering are not visually equivalent.
- Procedural primitives tend to look cleaner and more synthetic than authored production meshes.
- Transmission and glass can change substantially during GLB → USDZ conversion.
- A correct browser animation does not guarantee a compatible RealityKit hierarchy.
- CDN-based previews require network access; use installed dependencies for repeatable offline builds.

## Promotion to production

When the concept is approved, record:

- dimensions and datums;
- camera used for approval;
- material intent, not just numeric web values;
- pivot axes and animation ranges;
- stable mechanical node names;
- screenshots or a short motion capture.

Rebuild or refine the asset through the premium Blender/USDZ pipeline, then apply its complete validation and physical-device gate. Do not bypass those gates merely because the exported GLB looks correct in the browser.

## Primary sources

- [Three.js installation and addon versioning](https://threejs.org/manual/en/installation.html)
- [Three.js OrbitControls](https://threejs.org/docs/pages/OrbitControls.html)
- [Three.js GLTFExporter](https://threejs.org/docs/pages/GLTFExporter.html)
- [glTF 2.0 specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)

This workflow was validated with a procedural mechanical module containing an animated gear, two connectors, an energy pulse, orbit controls and client-side binary GLB export.

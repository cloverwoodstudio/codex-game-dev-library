# Datasheet-to-3D production workflow

Reviewed: 2026-08-29

Use this workflow for vehicles, machines, electronics, tools, furniture, architecture, props and other objects reconstructed from manufacturer datasheets, dimensioned drawings, manuals, photographs or existing CAD exchange files.

## Declare the accuracy class first

| Class | Claim | Acceptable use |
|---|---|---|
| A — engineering reconstruction | Every critical interface is stated or traceably derived with tolerances | fit/layout studies after qualified review; not automatically manufacturing-certified |
| B — dimensionally grounded visual model | Overall dimensions and important interfaces are verified; hidden/detail geometry may be estimated | games, visualization, XR and digital twins with disclosed limits |
| C — visual approximation | Silhouette and appearance are matched from incomplete references | background/game art only; never claim engineering accuracy |

Do not upgrade the class because the render looks convincing. A model is only as certain as its measurement ledger.

## 1. Create the evidence package

Preserve original source files unchanged and record:

- manufacturer/product, exact variant, revision, publication date and source URL;
- datasheet/manual/drawing page and figure numbers;
- native CAD files and their declared units/version when supplied;
- photographs, focal-length/EXIF information when available, and whether perspective correction was applied;
- license, trademark and redistribution restrictions;
- SHA-256 or equivalent hash for durable source identity.

Do not redistribute proprietary datasheets, CAD or logos merely because they are publicly downloadable. Store links and extracted facts when repository licensing does not permit the original file.

## 2. Build a dimension ledger

Normalize every measurement into one canonical unit while retaining the original notation.

Each row needs:

- stable dimension ID and human meaning;
- value, original/canonical unit and tolerance;
- axis or datum relationship;
- status: `stated`, `derived`, `estimated`, `unknown` or `conflicting`;
- exact source page/figure/callout;
- derivation formula or estimation method;
- affected features and criticality;
- reviewer and review date.

Resolve variant ambiguity before modeling. A drawing for the 1200 mm variant cannot silently drive the 900 mm product. If two official sources conflict, preserve both values, stop dependent work and record the decision authority.

## 3. Establish datums and coordinate contract

Define origin, up/forward axes, center planes, ground/contact plane and primary reference faces. Prefer functional datums—mounting face, shaft axis, wheel centerline—over arbitrary image edges.

Record:

- CAD master units and tolerance;
- DCC units;
- runtime units and axes;
- intended pivot and assembly origins;
- handedness and conversion transforms;
- zero-state articulation and moving-part limits.

Never scale each orthographic view independently. Calibrate all views from the same confirmed dimensions and verify aspect ratio before tracing.

## 4. Choose the master representation

### Existing STEP/CAD source

Inspect units, bodies, assemblies, names, missing references and licensing. Preserve the original file and create a conversion copy. STEP normally preserves solid/NURBS structure better than a triangle format; triangulate only for downstream DCC/runtime use.

### Parametric CAD master

Use FreeCAD or another reviewed CAD system for dimension-driven solids, interfaces, repeated hole patterns, mechanical assemblies and variants. Name sketches, constraints and parameters by ledger ID. Keep the model fully or intentionally constrained and regenerate after every parameter change.

### Scripted parametric master

Use OpenSCAD or a versioned FreeCAD Python script for repeatable prismatic/CSG shapes, product families and batch variants. Keep all source dimensions in one parameter block with units and ledger references. Scripts are preferable to opaque manual edits when reproducibility is the priority.

### Blender/DCC master

Use Blender for organic surfaces, visual-only reconstruction and game mesh finishing. Drive critical dimensions numerically; use orthographic references only after calibration. Keep modifiers non-destructive until the validation gate permits applying them.

## 5. Model in evidence order

1. Datum planes and overall bounding envelope.
2. Primary masses from stated dimensions.
3. Functional interfaces: mounts, openings, wheel/shaft axes, clearances and articulation.
4. Symmetry and repeated features.
5. Derived transitions and secondary forms.
6. Estimated cosmetic detail, isolated and labeled.
7. Materials, decals and surface breakup only after geometry validation.

Never let a photograph override a dimensioned drawing without recording why. Perspective images are valuable for form and material evidence but unreliable for direct measurement unless camera calibration is defensible.

## 6. Validate the technical master

- Recompute the model from a clean state.
- Measure bounding box, datum distances, hole/shaft diameters, angles and clearances.
- Compare every critical ledger row against model measurement within its declared tolerance.
- Generate front/side/top orthographic overlays against calibrated drawings.
- Create section views for hidden/internal relationships when evidence exists.
- Check solid validity, self-intersections, non-manifold results and assembly clashes.
- Change a representative driving parameter and confirm dependent geometry updates correctly.

Automate measurement checks where the CAD/DCC API permits. Store the report beside the model; screenshots alone are not numerical proof.

## 7. Derive the game-ready asset

Keep the CAD/parametric master immutable as the dimensional source. Create a separate runtime derivative:

1. Tessellate with documented chord/angle tolerances.
2. Remove invisible manufacturing detail that contributes no silhouette, shading or interaction.
3. Retopologize for deformation, shading and target GPU behavior.
4. Repair normals and deliberate hard edges; create UVs and material slots.
5. Bake normal/AO/curvature or other maps from the validated high-detail source.
6. Create LODs/HLODs and collision proxies from gameplay/performance requirements.
7. Preserve pivot, scale, articulation axes, sockets and stable part names.
8. Export and validate in the actual engine, not only in the DCC viewport.

Do not use STL as the archival master: it is a tessellated surface format and commonly loses units, hierarchy and parametric intent. Prefer native parametric source plus STEP for solid interchange; use glTF/GLB or the engine-approved format for runtime delivery.

## 8. Acceptance gates

- [ ] Exact product variant and source revisions are identified.
- [ ] Every critical dimension exists in the ledger with provenance and tolerance.
- [ ] Unknown, estimated and conflicting geometry is visually/reportably distinguishable.
- [ ] Master coordinate, units, datums and pivots are documented.
- [ ] Automated/manual measurement report passes for the claimed accuracy class.
- [ ] Orthographic overlays and representative perspective renders were reviewed.
- [ ] Runtime derivative retains scale, silhouette, interfaces and articulation.
- [ ] Engine import, collision, LOD, material and performance budgets pass.
- [ ] Source and output licensing/provenance are recorded.
- [ ] No manufacturing or safety claim exceeds the available evidence and qualified review.

## Primary sources

- [FreeCAD features: units, parametric modeling and exchange formats](https://www.freecad.org/features.php)
- [FreeCAD manual](https://www.freecad.org/manual/a-freecad-manual.pdf)
- [Blender retopology](https://docs.blender.org/manual/en/latest/modeling/meshes/retopology.html)
- [Khronos real-time asset creation guidelines](https://github.com/KhronosGroup/3DC-Asset-Creation/blob/main/asset-creation-guidelines/RealtimeAssetCreationGuidelines.md)
- [glTF specification: coordinate system and units](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
- [Khronos glTF Asset Auditor](https://www.khronos.org/gltf/gltf-asset-auditor/)

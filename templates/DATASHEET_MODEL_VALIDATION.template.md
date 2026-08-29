# Datasheet model validation report

Asset/version: `<name and immutable revision>`

Master model: `<path/hash>`

Runtime derivative: `<path/hash>`

Dimension ledger: `<path/hash>`

Tools/versions: `<CAD, DCC, validator and engine>`

## Numerical checks

| Dimension ID | Expected | Tolerance | Measured | Error | Result | Evidence |
|---|---:|---:|---:|---:|---|---|
| D-001 | `<value>` | `<±value>` | `<value>` | `<value>` | pass/fail | `<report/link>` |

## Geometry checks

- [ ] Clean regeneration/recompute succeeds.
- [ ] Required bodies are valid solids; intended open surfaces are documented.
- [ ] No unintended self-intersections, non-manifold edges or duplicate shells.
- [ ] Assembly clearances/articulation ranges pass.
- [ ] Front, side and top overlays are within approved tolerance.
- [ ] Estimated or unknown regions are identified in evidence views.

## Runtime derivative

| Check | Budget/expected | Measured | Result/evidence |
|---|---:|---:|---|
| dimensions and pivot | `<value>` | `<value>` | `<result>` |
| LOD0 triangles | `<budget>` | `<count>` | `<result>` |
| material slots | `<budget>` | `<count>` | `<result>` |
| texture memory | `<budget>` | `<value>` | `<result>` |
| collision error | `<tolerance>` | `<value>` | `<result>` |
| engine frame/render cost | `<budget>` | `<value>` | `<capture>` |

## Visual evidence

- Orthographic overlay contact sheet:
- Perspective reference comparison:
- Silhouette at intended gameplay distance:
- Normal/bake artifact review:
- Engine viewport and representative lighting:

## Limitations and disposition

- Claimed accuracy class:
- Stated/derived/estimated/unknown dimension counts:
- Unresolved conflicts:
- Prohibited uses or unsupported claims:
- Approved by/date:

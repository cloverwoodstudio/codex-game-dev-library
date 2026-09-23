# AI Visual Asset Lab

Experimental adapter area for complex visual-mesh generation. This does not own gameplay semantics and is not a promoted capability by itself.

## Canonical validated Tripo route
Use the official `tripo` CLI. The 2026-09-23 Xeno benchmark was completed end-to-end with Tripo CLI 0.5.1 after interactive `tripo login`; no API key or custom HTTP wrapper is required.

Typical flow:
- `tripo generate multiview-to-model <front> <left> <back> <right> --out <dir> --name <name> --yes --no-open`
- record the returned task ID and query/download it with `tripo task get <task-id> --download -o <dir> --yes --no-open`
- preserve downloaded MASTER unchanged
- create a separate optimized GAME derivative with the official CLI processing command selected from `tripo --help`; record its task ID/settings
- run Blender QA and Viewer owner review as defined in `docs/AI_VISUAL_ASSET_PIPELINE.md`

Do not invent or depend on undocumented Tripo HTTP endpoints/payloads. Re-check `tripo --help` before automation because provider CLI syntax can evolve. Provider authorization, uploads and credit spending remain explicit-owner-authorized actions.

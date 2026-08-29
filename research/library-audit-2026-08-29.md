# Library audit — 2026-08-29

## Executive finding

The library has broad, source-backed conceptual coverage and a strong evidence-oriented philosophy. Its primary weakness is execution depth: most topics stop at guidance, while few include runnable samples, engine-specific presets, captured outputs or cross-engine conformance tests. The next phase should turn high-value guidance into reproducible reference implementations rather than continuing breadth alone.

## Inventory snapshot

- 10 engine/native-framework playbooks plus engine selection;
- 13 genre vertical-slice playbooks;
- 16 gameplay/system guides;
- 20 production workflow guides;
- 6 art/3D guides, 12 design guides and 2 platform guides;
- 17 reusable templates, 10 pseudocode patterns and one prompt library;
- one automated external-link workflow;
- no broken local Markdown targets at audit time;
- first executable sample added by this audit: `samples/determinism-conformance/`.

Counts describe presence, not completeness. Several guides are intentionally concise and need samples or deeper engine variants before they can be considered production-proven.

## Scorecard

| Dimension | Score | Evidence | Main gap |
|---|---:|---|---|
| Breadth of game-development map | 4/5 | design, systems, art, production, release and lifecycle are represented | 2D art, tools, non-Apple platforms and production management are thinner |
| Source quality | 4/5 | current official sources dominate; reviewed dates are common | source claims are not mapped per paragraph; update cadence is manual |
| Codex usability | 4/5 | `AGENTS.md`, plan/bootstrap templates and routed playbooks | no machine-readable catalog or task-to-file routing validator |
| Reproducibility | 2/5 | deterministic principles, CI guidance and templates | almost no runnable projects, fixtures, captures or pinned toolchains |
| Engine depth | 3/5 | ten substantial engine playbooks | few tested import/build/CI recipes; PixiJS, Defold, GameMaker and custom C++ missing |
| Asset pipeline depth | 3/5 | Blender, animation, lighting, provenance and datasheet-to-3D | tested assets/presets absent; 2D/sprite, materials/scanning and procedural tools thin |
| Platform depth | 2/5 | Apple and XR are strong; generic platform guide exists | Android, Windows, Linux/Steam Deck and web/PWA deserve dedicated playbooks |
| Quality and release | 4/5 | testing, visual regression, performance, privacy, ratings and rollback | runnable fault-injection and release reference projects absent |
| Maintenance health | 3/5 | link checker and backlog exist | no schema/lint for reviewed dates, source sections, duplicate backlog or navigation coverage |

## Highest-priority gaps

### P0 — executable evidence

1. Port the determinism conformance fixture to Godot, Unity, Unreal and Phaser.
2. Add tiny buildable starter repositories/projects with pinned versions and exact commands.
3. Store test reports, screenshots and performance baselines as documented evidence shapes.
4. Add automated validation for templates, internal navigation, reviewed dates and source declarations.

Why first: runnable evidence tests whether the advice survives real engine lifecycle, serialization, numeric and build behavior.

### P1 — asset production proof

1. Build a permissively licensed FreeCAD/OpenSCAD datasheet reconstruction sample with automated dimension checks.
2. Derive a Blender game mesh with tessellation settings, retopology, UV, bake, LOD and engine import evidence.
3. Add dedicated 2D/sprite, texture/material scanning and procedural DCC playbooks.
4. Publish tested import presets per engine and target platform.

### P1 — platform engineering

Add dedicated playbooks and test matrices for:

- Android/Google Play, device fragmentation, ADPF and Play Asset Delivery;
- Windows, packaging/signing, DirectX diagnostics and store variants;
- Linux/Steam Deck, graphics drivers, filesystem casing and Proton boundaries;
- browser/PWA delivery, service workers, storage quotas and mobile browser lifecycle.

Console details must remain limited to publicly documentable material; NDA-only requirements do not belong in a public repository.

### P1 — legal and commercial safety

The backlog item “Licensing and AI-generated asset provenance” overlaps the existing provenance guide but is not closed. Expand it into a decision matrix covering training/input rights, output review, trademarks, publicity/personality rights, voice likeness, open-source code compatibility and storefront disclosure. Label it operational guidance, not legal advice.

### P2 — missing engines and tools

- PixiJS, Defold, GameMaker and custom C++ foundations;
- Houdini/procedural content, Krita/Aseprite 2D, material capture and photogrammetry;
- DCC automation via Blender Python, FreeCAD Python and command-line asset validation.

### P2 — production operations

Add scope estimation, milestone/critical-path planning, outsourcing handoff, vendor review, localization recording management, budget/burn tracking and decision-log templates. These should complement—not replace—the playable evidence loop.

## Content-quality findings

- Many compact guides have useful links but no explicit `Primary sources` heading. Standardize source sections so automated checks can reason about provenance.
- Genre guides correctly emphasize vertical slices but have no runnable slices or objective comparison fixture.
- The source index is strong but long and manually curated; add topic ownership and next-review dates before scale makes it stale.
- `prompts/README.md` is useful but monolithic. Split prompts by domain once navigation tooling exists.
- The backlog mixes foundations, samples and ongoing research in one flat list. Future revision should label `foundation`, `sample`, `platform`, `engine` and `continuous` work.

## Implementation sequence

1. Determinism conformance lab and ports.
2. Repository health/audit script and CI.
3. Datasheet-to-3D executable sample.
4. Godot/Unity/Unreal/Phaser tiny starters.
5. Android and Linux/Steam Deck platform playbooks.
6. Licensing/AI provenance expansion.
7. 2D/sprite and procedural-content pipelines.
8. Remaining engines and production-operations templates.

## Definition of done for future library additions

A foundation guide needs current primary sources, trade-offs, acceptance gates and routing. A “tested sample” additionally needs pinned tools, a clean setup command, automated checks, a real run, retained expected output and a documented limitation. A platform or engine claim is not “proven” until exercised in that platform or engine.

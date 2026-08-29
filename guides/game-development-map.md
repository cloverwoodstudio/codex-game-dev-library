# Complete game-development map

Reviewed: 2026-08-29

This is the master taxonomy for the library. A game rarely needs every branch, but every project should explicitly decide which branches apply.

## 1. Vision and product

Player fantasy, audience, genre, platform, scope, references, differentiator, session length, business model, ethical boundaries, budget, schedule, team, risks, market validation.

## 2. Game and narrative design

Core loop, mechanics, verbs, rules, resources, economy, progression, difficulty, combat, puzzles, quests, dialogue, lore, characters, tutorials, accessibility, retention without manipulation.

## 3. World and level design

Setting bible, geography, history, factions, cultures, ecology, level grammar, metrics, landmarks, navigation, encounters, pacing, procedural generation, streaming, lighting, environmental storytelling.

## 4. Technology

Engine, languages, architecture, tools, data pipeline, physics, input, camera, AI, UI, saves, networking, platform services, build system, CI, observability, security, modding.

## 5. Visual production

Art bible, concept art, color/script, 2D illustration, sprites, UI, typography, modeling, sculpting, retopology, UVs, PBR materials, rigging, animation, VFX, shaders, lighting, optimization, LODs.

## 6. Audio

Sound language, field/foley recording, SFX, dialogue, localization, music, adaptive systems, spatial audio, mixing, loudness, compression, accessibility.

## 7. Quality

Unit/integration/functional tests, deterministic simulations, input replay, compatibility, visual regression, performance budgets, playtests, UX research, accessibility tests, localization QA, soak testing, crash recovery.

## 8. Production and release

Version control, task slicing, asset provenance, licensing, ratings, privacy, storefronts, builds, signing, achievements, cloud saves, telemetry, crash reporting, community, patches, live operations, preservation.

## Recommended order

Concept → risk prototype → playable loop → vertical slice → production pipeline → systems alpha → content beta → polish/optimization → release candidate → launch/live operations.

Never scale content before proving both the core loop and the content-production pipeline.

## Production routes

- Engine selection and bootstrap: `engine-selection.md`, `engines/`, `../templates/ENGINE_BOOTSTRAP.template.md`
- Apple-native games: `engines/apple-native.md`, `platforms/apple.md`, `workflows/apple-build-release.md`, `../templates/APPLE_TEST_MATRIX.template.md`
- Repository and binary assets: `workflows/version-control-assets.md`
- Mods and community content: `systems/modding-ugc.md`
- Backend trust boundaries: `systems/backend-security.md`
- Telemetry, crashes and live operations: `workflows/observability-live-ops.md`
- Performance evidence: `workflows/performance-lab.md`
- Store page and capture pipeline: `workflows/store-marketing.md`
- Procedural generation: `design/procedural-generation.md`
- Automated and playable testing: `workflows/game-testing.md`
- Replay-driven reproduction: `systems/replays-determinism.md`
- Cross-engine determinism fixture: `../samples/determinism-conformance/`
- Visual regression: `workflows/visual-regression.md`
- CI and build evidence: `workflows/continuous-integration.md`
- Level and encounter production: `design/level-design.md`
- Onboarding and objective clarity: `design/onboarding-tutorials.md`
- Character rigging and animation: `art/character-animation.md`
- Datasheet-to-3D reconstruction: `art/datasheet-to-3d.md`, `../templates/DIMENSION_LEDGER.template.md`, `../templates/DATASHEET_MODEL_VALIDATION.template.md`
- Lighting and readability: `art/lighting.md`
- Cinematics and state transitions: `design/cinematics.md`
- Adaptive audio and music: `systems/adaptive-audio.md`
- Privacy and data governance: `workflows/privacy-data-governance.md`
- Ratings and content compliance: `workflows/ratings-content-compliance.md`
- Platform achievements/cloud: `systems/platform-services.md`
- Community and moderation: `workflows/community-moderation.md`
- Patch rollout and rollback: `workflows/patching-rollbacks.md`
- Preservation and sunset: `workflows/preservation-sunset.md`
- Data schemas and internal tools: `systems/data-driven-content.md`
- Large-world streaming: `systems/world-streaming.md`
- Quality tiers and fairness: `workflows/quality-scalability.md`
- XR/VR comfort and testing: `platforms/xr.md`
- Purchases, DLC and entitlements: `systems/commerce-entitlements.md`
- Genre slices: `genres/platformer.md`, `genres/roguelike.md`, `genres/tactics.md`, `genres/puzzle.md`, `genres/racing.md`, `genres/survival-crafting.md`
- More genre slices: `genres/fps.md`, `genres/idle-incremental.md`, `genres/strategy-management.md`, `genres/rhythm.md`, `genres/horror.md`, `genres/party-social.md`, `genres/immersive-sim.md`

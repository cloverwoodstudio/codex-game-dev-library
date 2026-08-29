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

# Worldbuilding and level design

Reviewed: 2026-08-29

## Build from play outward

Worldbuilding serves player decisions. Start with verbs and level metrics, then create fiction that makes those mechanics feel inevitable. Maintain a world bible, but separate immutable pillars from ideas that can change.

## World bible

- premise, tone, themes, prohibited clichés
- rules of reality, technology, magic, cost and limits
- geography, climate, ecology and resources
- timeline and causality
- factions: goals, methods, resources, conflicts
- cultures, languages, architecture, clothing and symbols
- everyday life, economy, governance and belief
- locations with gameplay purpose and visual identity
- open questions and contradiction log

## Level-production loop

1. Define player goal, available verbs and teaching purpose.
2. Establish metrics: character size, speed, jump, camera, combat range, corridor/door dimensions.
3. Draw flow and critical path; add optional loops and landmarks.
4. Graybox with primitives and test traversal immediately.
5. Place encounters and resources around pacing beats.
6. Validate navigation, sightlines, readability and exploits.
7. Art pass without destroying metrics.
8. Lighting, audio and VFX pass.
9. Optimize, accessibility-test and playtest with new players.

## Procedural worlds

Represent generation as seeded stages: macro layout → connectivity validation → biome assignment → gameplay placement → dressing → navmesh → validation. Save the seed and generator version. Reject invalid worlds with explicit invariants; never rely on screenshots alone.

Useful sources:

- Red Blob Games: https://www.redblobgames.com/
- Unreal PCG framework: https://dev.epicgames.com/documentation/unreal-engine/procedural-content-generation-framework-in-unreal-engine
- Godot navigation: https://docs.godotengine.org/en/stable/tutorials/navigation/index.html
- Unity AI Navigation: https://docs.unity3d.com/Packages/com.unity.ai.navigation@latest

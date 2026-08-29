# Level design and encounter production

Reviewed: 2026-08-29

A level is a controlled sequence of player decisions, information and pressure expressed through space. Start from gameplay metrics and intended experience, not finished art.

## Level contract

Record player goal, entry/exit state, verbs tested, required knowledge, target duration, difficulty beat, critical path, optional paths, checkpoints, fail/recovery behavior, narrative purpose, performance tier and accessibility risks.

Maintain a metrics kit inside the engine: character height/radius, jump arcs, movement speeds, camera/FOV, interaction distance, cover dimensions, doors/corridors/stairs, enemy perception and representative input latency. Geometry that ignores the real controller and camera is not a valid blockout.

## Production loop

`paper/flow → metrics gym → blockout → traversal test → encounter pass → readability/navigation → art kit → lighting/audio → optimization → regression`

At blockout, test routes, sightlines, landmarks, pacing, spawn safety, camera collision and recovery. Keep collision simple and materials color-coded by function. Do not hide structural problems with decoration.

## Spatial grammar

Define reusable elements: arrival, vista, choice, gate, teaching space, mastery space, rest, reward, escalation, shortcut, secret and exit. Use landmarks, light, contrast, motion, sound and composition together; waypoints should support—not replace—readable space.

## Encounter sheet

For every encounter state:

- setup, player information and available preparation;
- enemy/obstacle roles, waves and spawn rules;
- intended decisions and counterplay;
- arena affordances, traversal and safe recovery;
- escalation/termination conditions and rewards;
- difficulty parameters and accessibility alternatives;
- deterministic test seed and performance worst case.

Spawn systems must respect visibility, distance, capacity and nav validity. Test players who retreat, rush, skip, arrive under-resourced, return later or break the expected sequence.

## Validation

Automate unreachable objectives, missing references, invalid spawn/nav positions, bounds escapes and budget limits. Playtest navigation without markers, then with final UI. Capture route heatmaps and completion/failure evidence, but interpret them alongside observation: the shortest route is not automatically the best experience.

## Sources

- Unreal Level Editor: https://dev.epicgames.com/documentation/en-us/unreal-engine/level-editor-in-unreal-engine
- Unreal level-design quick start and build/play loop: https://dev.epicgames.com/documentation/en-us/unreal-engine/level-designer-quick-start-in-unreal-engine
- Godot navigation synchronization: https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationservers.html
- Red Blob Games pathfinding: https://www.redblobgames.com/pathfinding/a-star/introduction.html

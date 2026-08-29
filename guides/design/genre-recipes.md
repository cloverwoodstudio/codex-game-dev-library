# Genre starting recipes

Reviewed: 2026-08-29

These are risk maps, not formulas.

| Genre | Prove first | Main technical/design risks |
|---|---|---|
| Platformer | movement, jump and camera test room | collision edges, animation sync, level metrics |
| Puzzle | one rule set with undo/reset | state representation, solvability, hint design |
| Roguelike | seeded complete run | generation validity, balance variance, save/replay |
| Tactics | small encounter with AI | grid/rules determinism, previews, turn state |
| Action RPG | one enemy and item loop | combat feel, content pipeline, inventory/economy |
| Racing | one vehicle/track/time trial | vehicle feel, camera, input devices, ghost/replay |
| FPS | one combat arena | aiming/input latency, weapon feedback, AI/networking |
| Simulation | minimal closed economy | systemic interactions, time scale, data/UX, performance |
| Idle/incremental | simulated progression curve | numerical scaling, offline progress, ethical economy |
| Multiplayer party | two machines, one full round | sessions, authority, latency, disconnect recovery |

For each genre, build the smallest full loop and its authoring pipeline before adding content breadth.

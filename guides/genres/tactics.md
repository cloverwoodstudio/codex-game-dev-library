# Turn-based tactics playbook

Reviewed: 2026-08-29

## Product loop

Inspect state → predict consequences → choose unit/action/target → commit → resolve deterministic rules → react to new state → complete objective. Clarity and trust are more important than animation spectacle.

## Smallest vertical slice

One compact grid/map, three player units/roles, three enemy roles, movement, cover/terrain, two abilities each, objective other than elimination, enemy turn, win/fail/restart and save/replay. Include a complete outcome preview for one representative attack.

## High-risk contracts

- canonical grid/world conversion and occupancy;
- deterministic initiative, movement cost, line of sight, range and effect ordering;
- explicit action command with validate/preview/commit/resolve stages;
- AI bound by the same knowledge and legality rules;
- readable threat ranges, hit/effect preview and interruption/reaction order;
- undo policy before information is revealed.

## Test board

Create small maps for diagonal/corner rules, elevation, cover, area effects, displacement, simultaneous death, reaction chains, unreachable objectives and save mid-turn. Property-test that preview equals resolution for unchanged state.

## Typical traps

UI predicting different math from simulation, ambiguous line of sight, animation owning turn completion, combinatorial reactions without priority, slow enemy turns, elimination-only objectives and difficulty based on hidden bonuses.

## References

- Godot official hexagonal demo: https://github.com/godotengine/godot-demo-projects/tree/master/2d/hexagonal_map
- Red Blob Games grids/pathfinding: https://www.redblobgames.com/grids/hexagons/ and https://www.redblobgames.com/pathfinding/a-star/introduction.html
- Library gameplay-AI guide: ../systems/gameplay-ai.md

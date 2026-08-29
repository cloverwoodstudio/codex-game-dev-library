# Puzzle game playbook

Reviewed: 2026-08-29

## Product loop

Observe rules → form hypothesis → act → receive legible feedback → revise model → discover insight → solve. Difficulty should come from reasoning with understood rules, not fighting controls or guessing designer intent.

## Smallest vertical slice

One mechanic, a safe tutorial, three puzzles that isolate/combine/master it, undo/reset, hint ladder, completion state and save. Include an automated solver or exhaustive validator when the state space permits.

## High-risk contracts

- explicit state model and deterministic action transitions;
- win/deadlock detection and bounded reset/undo history;
- level schema with validation and stable IDs;
- rule feedback through animation/audio without delaying input unnecessarily;
- hint stages that reveal observation, direction, then solution—not one binary spoiler;
- accessibility for color, timing, precision and input.

## Validation lab

Check solvability, shortest/expected solution ranges, unreachable objects, alternate solutions, softlocks and state-count/performance. Record playtest actions and hesitation without assuming the authored solution is the only valid one.

## Typical traps

Teaching two rules at once, accidental solutions before understanding, invisible state, irreversible mistakes without warning, hints detached from current state, excessive traversal between attempts and visual decoration obscuring interactable grammar.

## References

- Godot official grid pathfinding demo: https://github.com/godotengine/godot-demo-projects/tree/master/2d/navigation_astar
- Library onboarding guide: ../design/onboarding-tutorials.md
- Library replay guide: ../systems/replays-determinism.md

# Gameplay AI

Reviewed: 2026-08-29

Game AI exists to create understandable, interesting decisions—not to imitate human intelligence. Design its perception, knowledge, decision and action layers separately so behavior can be inspected.

## Choose the smallest useful model

- Finite-state machine: few exclusive modes and explicit transitions.
- Behavior tree: reusable hierarchical tasks with reactive branching.
- Utility system: scores competing actions when priorities vary continuously.
- GOAP/planning: action sequences emerge from goals and world state; higher debugging and authoring cost.
- Search: tactical/board decisions with a manageable state space.
- Scripted encounter: precise pacing and authored spectacle.

## Production loop

1. Describe desired player-facing behavior and deliberate imperfections.
2. Define only information the agent is allowed to know.
3. Separate sensing from memory; model confidence and forgetting when useful.
4. Make decisions explainable through debug labels, scores and state history.
5. Keep movement/pathfinding separate from strategic choice.
6. Test with deterministic scenarios, seeds and recorded event timelines.
7. Budget perception queries, path requests and decision frequency across worst-case crowds.

Fairness often needs telegraphing, reaction delays, aim error, cooldowns, limited coordination and recovery opportunities. Never let difficulty silently become omniscience.

Sources:

- Unreal AI/EQS: https://dev.epicgames.com/documentation/en-us/unreal-engine/environment-query-system-in-unreal-engine
- Unity AI Navigation: https://docs.unity3d.com/6000.2/Documentation/Manual/com.unity.ai.navigation.html
- Godot navigation: https://docs.godotengine.org/en/stable/tutorials/navigation/index.html
- Game AI Pro (free-to-read; chapters remain copyrighted): https://www.gameaipro.com/

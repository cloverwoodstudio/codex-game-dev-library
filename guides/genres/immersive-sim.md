# Immersive simulation playbook

Reviewed: 2026-08-29

## Product loop

Observe systemic space → form plan from verbs/tools → combine systems → world reacts → adapt to consequences → discover alternate route or story. The promise is credible interaction, not that every object is simulated.

## Smallest vertical slice

One dense location, one objective with at least three mechanically distinct solutions, four reusable verbs/tools, guards or systemic hazards, persistent consequences, save/load and a debug event/state inspector.

## High-risk contracts

- shared interaction interface and affordance language;
- typed events/tags rather than bespoke pairwise scripts;
- consistent fire/electricity/physics/AI/alarm ownership rules;
- AI perception and communication bounded by believable information;
- quest/objective state tolerant of sequence breaking;
- save persistence for altered world and stable entity IDs.

## Possibility lab

Build an interaction matrix of verbs × materials/targets and test combinations automatically where rules are deterministic. Playtest direct, stealth, social/tool and destructive routes; preserve unexpected valid solutions unless they break explicit contracts.

## Typical traps

One-off scripted exceptions, affordances that work only when convenient, objective graph assuming one order, physics chaos corrupting saves, AI omniscience, combinatorial effects without ownership/priority and content cost growing faster than reusable systems.

## References

- Unreal Lyra interaction-system example: https://dev.epicgames.com/documentation/en-us/unreal-engine/lyra-sample-game-interaction-system-in-unreal-engine
- Library gameplay-architecture guide: ../systems/gameplay-architecture.md
- Library quest/narrative guide: ../design/narrative-quests.md

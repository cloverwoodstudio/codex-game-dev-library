# Survival and crafting playbook

Reviewed: 2026-08-29

## Product loop

Assess needs/environment → gather under risk → craft/build → expand capability/safety → explore farther → face stronger pressure. Every resource should create decisions through scarcity, location, risk, transformation or opportunity cost.

## Smallest vertical slice

One biome/day cycle, three needs or pressures at most, six resources, gathering, inventory, two-stage crafting, one placeable shelter/tool, one threat, save/load and a clear short-term survival objective. Prove the resource graph before adding dozens of recipes.

## High-risk contracts

- transactional inventory/crafting with stable item/recipe IDs;
- source/sink/conversion graph and seeded economy simulation;
- placement validation, ownership, persistence and dismantle/refund rules;
- world depletion/regrowth and offline/time progression policy;
- readable need rates and recovery options;
- multiplayer authority, containers and concurrent transactions.

## Simulation lab

Run several player strategies over many seeds. Measure time to first safety/tool, starvation/resource deadlocks, stockpile growth, dominant recipes, travel burden and recovery after death. Fault-test save during crafting/building and simultaneous container access.

## Typical traps

Busywork without decisions, exponential recipe chains, irreversible beginner mistakes, opaque decay, resource scarcity caused by bad seeds, building collision/nav failures, offline timers punishing absence and client-authoritative duplication exploits.

## References

- Library inventory/crafting guide: ../systems/inventory-crafting.md
- Library economy guide: ../design/economy-balancing.md
- Library world-streaming guide: ../systems/world-streaming.md

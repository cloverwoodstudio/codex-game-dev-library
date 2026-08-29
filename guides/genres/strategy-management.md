# Strategy, management and simulation playbook

Reviewed: 2026-08-29

## Product loop

Observe system state → form plan → allocate space/resources/agents → advance time → diagnose consequences → adapt. The UI and simulation observability are core gameplay.

## Smallest vertical slice

One map, two resource flows, one production chain, placement/build/demolish, agents or vehicles with pathfinding, time controls, one failure pressure, goal, save/load and deterministic headless simulation. Prove a complete causal chain.

## High-risk contracts

- fixed-step simulation independent from render/UI;
- stable entity IDs and transactional construction/economy;
- pathfinding/reservations and bounded recalculation;
- explicit time speed/pause and queued commands;
- inspectable source/sink/throughput and failure reasons;
- deterministic save/replay and migration for large state.

## Simulation lab

Tiny deterministic maps for production, congestion, shortage, rerouting, demolition and bankruptcy; plus long soak at maximum speed. Measure tick cost, queue length, path requests, stock levels and conservation invariants.

## Typical traps

Opaque causality, every agent updating every frame, UI querying mutable state inconsistently, runaway feedback loops, pathfinding storms, save snapshots during partial transactions and difficulty created by withholding basic diagnostics.

## References

- OpenTTD source documentation: https://docs.openttd.org/
- OpenTTD source repository: https://github.com/OpenTTD/OpenTTD
- Library fixed-step pattern: ../../code-patterns/fixed-step-pseudocode.md

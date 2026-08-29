# Gameplay architecture

Reviewed: 2026-08-29

## Boundaries that help humans and Codex

- Input produces intent; it does not directly animate or mutate unrelated systems.
- Simulation owns authoritative rules and uses fixed-step time where determinism matters.
- Presentation observes state and may interpolate; it does not decide outcomes.
- Authored definitions are distinct from per-session mutable state.
- Save format is versioned and migrated.
- Randomness is injected/seeded and recorded for reproduction.
- Engine adapters surround domain logic instead of leaking everywhere.

## Common patterns

State machines for clear modes; command pattern for replay/undo/network input; event queues for decoupled consequences; object pools only after measurement; behavior trees/utility AI for explainable decisions; ECS/data-oriented layouts for scale where profiling justifies complexity.

Avoid universal singleton managers, frame-rate-dependent rules, hidden scene-name dependencies, unbounded event recursion, and premature abstraction. Prefer a playable feature slice with tests over an elaborate framework without a game.

Source: https://gameprogrammingpatterns.com/

# Bevy production playbook

Reviewed: 2026-08-29

## Best fit

Choose Bevy when a Rust team wants a data-oriented ECS, explicit systems and schedules, native code, modular plugins and control over engine architecture. Treat version upgrades as planned engineering work: Bevy evolves quickly and its official migration guides are part of the production workflow.

## Recommended project shape

```text
Cargo.toml
src/
  main.rs
  core/          # deterministic domain types and algorithms
  features/      # one plugin per bounded gameplay feature
  presentation/  # rendering, audio, animation and UI systems
  platform/      # persistence, services and target adapters
tests/
assets/
```

- Organize features as plugins with explicit resources, events/messages, system sets and schedule ordering.
- Use components for entity-local data and resources only for genuinely world-wide state.
- Put fixed-rate gameplay/physics rules in `FixedUpdate`; keep presentation and input sampling in the appropriate frame schedules.
- Make ambiguous system ordering explicit instead of depending on incidental execution order.
- Keep algorithms testable as plain Rust functions; build small `App` tests for ECS integration.

## Codex loop

1. Read `Cargo.toml`, feature flags, Bevy version, active plugins, states and system registration.
2. Locate data ownership and schedule ordering before editing a system.
3. Add a pure Rust or minimal-App test for the rule.
4. Run formatting, compiler checks, focused tests and Clippy using repository-defined commands.
5. Run the real app, exercise state transitions and inspect logs and visuals.
6. Produce a release build and profile that build on representative hardware.

Typical command roles:

```sh
cargo fmt --check
cargo check --all-targets
cargo test
cargo clippy --all-targets --all-features -- -D warnings
cargo build --release
```

Projects may intentionally use different feature matrices or lint policies. Record exact verified commands and toolchain pinning in the bootstrap document.

## Validation ladder

1. Plain Rust unit/property tests.
2. Minimal headless `App` schedule tests.
3. Asset loading and state-transition smoke test.
4. Real-window controls and presentation pass.
5. Release build launch on each target.
6. CPU, GPU, memory and asset-loading capture under representative load.

## ECS and release traps

- Avoid monolithic systems with broad queries; keep access narrow and system purpose clear.
- Do not clone large components or allocate per frame without measurement.
- Seed random streams and separate simulation time from wall-clock/presentation time.
- Test asset paths and case sensitivity from the packaged working directory.
- Pin Rust with `rust-toolchain.toml` when reproducibility matters; retain `Cargo.lock` for applications.
- Before a Bevy upgrade, read every intervening official migration guide and isolate the upgrade from feature work.

## Primary sources

- [Bevy Quick Start](https://bevyengine.org/learn/quick-start/getting-started/)
- [Official examples](https://bevyengine.org/examples/)
- [Migration guides](https://bevyengine.org/learn/migration-guides/)
- [App and schedules API](https://docs.rs/bevy/latest/bevy/app/)

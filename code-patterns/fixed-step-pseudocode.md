# Fixed-step simulation and deterministic replay

Use this engine-neutral shape for gameplay that must behave consistently across render frame rates. Adapt to engine APIs; do not blindly copy it.

```text
fixed_dt = 1 / 60
accumulator = 0
previous_time = monotonic_time()

while running:
    now = monotonic_time()
    frame_time = min(now - previous_time, 0.25)
    previous_time = now
    accumulator += frame_time

    input = sample_and_quantize_input()

    while accumulator >= fixed_dt:
        replay_log.append(tick, input, rng.state)
        previous_state = current_state
        current_state = simulate(current_state, input, fixed_dt, rng)
        accumulator -= fixed_dt
        tick += 1

    alpha = accumulator / fixed_dt
    render(interpolate(previous_state, current_state, alpha))
```

Determinism also depends on numeric behavior, iteration order, physics, threading and serialization. Validate by replaying the same input/seed and comparing periodic state hashes. For network architectures, see https://gafferongames.com/ and the selected engine's current networking documentation.

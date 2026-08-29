# Replay envelope and divergence check

Reviewed: 2026-08-29

```text
ReplayEnvelope {
  format_version
  build_id
  content_version
  simulation_version
  tick_rate
  reproduction_key
  initial_state_hash
  commands[] = { tick, player_id, action_id, quantized_value, sequence }
  checkpoints[] = { tick, state_hash, subsystem_hashes }
  integrity_hash
}

play(replay):
  validate_size_schema_version_and_integrity(replay)
  world = create_world(replay.reproduction_key)
  assert hash(world) == replay.initial_state_hash

  for tick in 0..last_tick:
    apply_commands_in_sequence(world, replay.commands_at(tick))
    simulate_fixed_tick(world)
    if replay.has_checkpoint(tick):
      actual = subsystem_hashes(world)
      if actual != replay.checkpoint(tick):
        report_first_divergence(tick, actual, replay.checkpoint(tick))
        fail()
```

Hash stable domain state only. Presentation objects, memory addresses, wall-clock timestamps and unordered container traversal must not enter the comparison.

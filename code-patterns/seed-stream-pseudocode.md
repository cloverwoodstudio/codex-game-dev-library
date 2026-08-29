# Stable named random streams

Reviewed: 2026-08-29

```text
ReproductionKey {
  root_seed
  generator_version
  content_version
  config_hash
}

derive_stream(root_seed, stable_stream_id, scope_id):
  bytes = canonical_encode(root_seed, stable_stream_id, scope_id)
  stream_seed = stable_hash(bytes)       # algorithm/version is part of contract
  return PRNG(stream_seed)

generate_world(key, world_id):
  layout_rng = derive_stream(key.root_seed, "world_layout/v2", world_id)
  loot_rng   = derive_stream(key.root_seed, "world_loot/v1", world_id)

  layout = generate_layout(layout_rng, key.generator_version)
  assert validate_connectivity(layout)
  loot = place_loot(layout, loot_rng, key.content_version)
  result = {layout, loot}
  return result, stable_hash(canonical_encode(result))
```

Use a specified stable hash and canonical encoding; language-default object hashes may change across process or runtime versions. Never derive streams from mutable array position when a stable domain ID exists.

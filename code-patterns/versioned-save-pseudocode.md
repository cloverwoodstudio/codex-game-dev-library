# Versioned, recoverable save pseudocode

```text
function save(slot, domain_state):
    envelope = {
        format_version: CURRENT_VERSION,
        build_version: BUILD_VERSION,
        timestamp_utc: now_utc(),
        payload: encode_stable_state(domain_state)
    }
    bytes = serialize(envelope)
    validate_bounds(bytes)
    write_and_flush(slot + ".tmp", bytes)
    assert load_and_validate(slot + ".tmp") succeeds
    rotate_backup(slot)
    atomic_replace(slot + ".tmp", slot)

function load(slot):
    raw = read_bounded(slot)
    envelope = parse_untrusted(raw)
    validate_envelope(envelope)
    while envelope.format_version < CURRENT_VERSION:
        envelope = migrate_one_version(envelope)
    state = decode_and_validate_domain_state(envelope.payload)
    return state
```

Test migrations using immutable fixtures copied from every shipped format. The exact atomic-replace and flush guarantees vary by platform; use the platform/engine API and verify interruption behavior.

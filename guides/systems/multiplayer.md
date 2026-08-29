# Multiplayer and networking

Reviewed: 2026-08-29

Multiplayer is an architectural decision, not a feature to bolt on at the end. Prototype the real network model during the vertical slice.

## Decide first

- topology: dedicated server, listen server, peer-to-peer or relay
- authority for every important object and action
- simulation/tick rate, replication rate and bandwidth budget
- expected latency, jitter, packet loss, reordering and disconnect behavior
- session discovery, lobby, matchmaking, invites and migration
- persistence, identity, moderation, privacy and abuse handling

For competitive or economy-bearing games, treat clients as untrusted. Clients send bounded intent; the authoritative server validates timing, range, ownership, rate and state transitions.

## Synchronization families

- Lockstep/rollback: exchange inputs and resimulate deterministic state; suitable for small deterministic simulations.
- Snapshot interpolation: buffer authoritative snapshots and render between them; adds delay but smooths remote state.
- Prediction/reconciliation: predict local input immediately, then rewind/correct from authoritative acknowledgement.
- Event/state replication: reliable ordered events for rare transitions; unreliable sequenced updates for frequent replaceable state.

## Test matrix

Run separate processes, not multiple views sharing one state. Automate 0–300 ms latency, jitter, loss, duplication, reordering, bandwidth limits, late join, reconnect, host loss, version mismatch, clock drift, malicious RPC values and long soak sessions. Record server tick, client input sequence and state hashes.

Sources:

- Unreal networking/Iris: https://dev.epicgames.com/documentation/unreal-engine/introduction-to-iris-in-unreal-engine
- Unity netcode choices: https://docs.unity.com/multiplayer/netcode/netcode
- Godot high-level multiplayer: https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html
- Gaffer on Games: https://gafferongames.com/post/snapshot_interpolation/
- OWASP Game Security Framework: https://owasp.org/www-project-gamesec-framework/OGSF

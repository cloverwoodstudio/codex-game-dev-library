# Replays, input recording and deterministic diagnosis

Reviewed: 2026-08-29

A replay is evidence. It may record inputs for deterministic resimulation, authoritative state/events, network replication, snapshots, video, or a hybrid. Choose based on the question it must answer.

## Replay types

| Type | Strength | Main limitation |
|---|---|---|
| Input log + seed | Compact, excellent for deterministic tests | Breaks when simulation/version diverges |
| Authoritative events/state deltas | More resilient and spectator-friendly | Larger and coupled to schemas |
| Periodic snapshots + deltas | Seekable and corruption-tolerant | Highest implementation complexity |
| Video | Faithful visual evidence | Cannot inspect or resimulate state |

## Versioned envelope

Record format version, game/build/content versions, platform, map/mode, tick rate, root seed and named PRNG states, initial state hash, participants, input schema, start UTC, duration and integrity hash. Add privacy classification before uploading player replays.

Replay compatibility is an explicit product policy: same build only, supported migration window, or long-term archival. Unreal's replay system exposes engine and game network versions so projects can adapt data, but migration remains project work.

## Deterministic input replay

Sample gameplay commands at simulation ticks, not OS event timing. Quantize analog values deliberately. Record command order, device-independent action IDs and any authoritative external response. During playback, feed the exact command stream into a fixed-step simulation and compare periodic state hashes.

On divergence, report the first differing tick, subsystem hashes, last commands, random-stream positions and a compact state diff. Do not wait until the final score differs.

## Debug artifact bundle

When a defect occurs, preserve:

- replay and reproduction key;
- build/commit/content identifiers;
- logs and crash data;
- initial/final save or snapshots where permitted;
- settings, platform and device information;
- screenshot or short recording;
- expected versus observed result.

Replay parsers consume untrusted files. Bound sizes and counts, validate versions and checksums, reject unsafe paths, and never deserialize arbitrary runtime types.

## Test strategy

- short golden replays for critical state transitions;
- regression replay for every stable gameplay defect;
- long soak replays with checkpoints;
- cross-frame-rate and headless playback where supported;
- deliberate corruption, truncation and version-mismatch tests;
- multiplayer captures under latency/loss plus authoritative server replay.

## Sources

- Unreal replay system: https://dev.epicgames.com/documentation/en-us/unreal-engine/using-the-replay-system-in-unreal-engine
- Godot independent random state: https://docs.godotengine.org/en/stable/tutorials/math/random_number_generation.html
- Gaffer on Games deterministic lockstep: https://gafferongames.com/post/deterministic_lockstep/

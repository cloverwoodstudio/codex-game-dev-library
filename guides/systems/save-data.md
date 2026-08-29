# Save data and persistence

Reviewed: 2026-08-29

Save the smallest stable domain state needed to reconstruct play. Do not serialize arbitrary runtime object graphs and hope future versions can load them.

## Save envelope

Store format version, game/build version, slot/profile ID, timestamp, playtime, content/DLC identifiers, payload and integrity metadata. Keep settings, progression, checkpoints and transient run state separate when their lifecycles differ.

## Safe write

Serialize to a temporary file → flush/close → validate by reading it → preserve/rotate previous valid save → atomically replace the destination where supported. Never destroy the last known-good save before the new one is verified.

## Migrations

Create explicit sequential migrations (`v1 → v2 → v3`), fixtures from shipped versions and tests for forward migration, missing optional fields, unknown fields, truncation and incompatible content. Do not make releases depend on downgrading saves unless deliberately supported.

Treat imported/cloud/modded saves as untrusted input: bound sizes and collections, validate identifiers/ranges and avoid deserializers that can instantiate executable object types. Encryption hides data but does not make a client authoritative.

Sources:

- Unreal save system: https://dev.epicgames.com/documentation/en-us/unreal-engine/saving-and-loading-your-game-in-unreal-engine
- Unity JSON serialization: https://docs.unity3d.com/6000.1/Documentation/Manual/json-serialization.html
- Godot saving games: https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html

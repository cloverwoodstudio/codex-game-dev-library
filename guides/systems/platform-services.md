# Achievements, cloud and platform-service abstraction

Reviewed: 2026-08-29

Platform services are asynchronous external dependencies. Keep the game's canonical domain state independent, then adapt achievements, stats, cloud, presence and entitlement APIs behind explicit interfaces.

## Achievement contract

Each achievement needs stable internal/platform IDs, localized name/description, hidden policy, icon provenance, unlock condition, progress/stat source, authority, offline behavior and test reset procedure. Reward meaningful mastery, discovery or play styles; avoid forcing harmful grind, inaccessible actions or mutually incompatible choices without clear design intent.

For competitive or valuable unlocks, prefer authoritative server evaluation. Steam distinguishes client, game-server and official-game-server authority for stats/achievements. Do not maintain a conflicting local cache when the platform already owns merge behavior; retain only domain progress needed to recompute safely.

## Adapter behavior

- initialize and request state asynchronously;
- queue bounded idempotent writes while unavailable;
- separate platform failure from gameplay failure;
- reconcile on reconnect using monotonic or domain-specific rules;
- expose diagnostic status without leaking credentials;
- support a no-platform/local development adapter;
- never make launch impossible solely because an optional service is down.

Cloud-save conflicts belong to the save system's versioned conflict policy. Entitlement checks and purchases require server verification where value/security matters.

## Test matrix

First launch, offline launch, delayed callback, account switch, two-device conflict, duplicate unlock, reset, platform overlay, revoked entitlement, service outage, locale change and migration from a build without the feature.

## Sources

- Steam Stats and Achievements: https://partner.steamgames.com/doc/features/achievements
- Steam Cloud: https://partner.steamgames.com/doc/features/cloud
- Epic Online Services documentation: https://dev.epicgames.com/docs/epic-online-services

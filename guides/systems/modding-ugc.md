# Modding and user-generated content

Reviewed: 2026-08-29

Mod support is a public extension API plus an untrusted-content pipeline. Decide early whether users may change data, visuals, levels or executable behavior; each step increases compatibility, moderation and security cost.

## Capability ladder

1. **Configuration:** validated data overrides and cosmetic packs.
2. **Authored content:** maps, quests or items made with a constrained editor.
3. **Scripting:** sandboxed, capability-limited behavior.
4. **Native code:** maximum power and maximum security/support risk; avoid as the default.

Start at the lowest level that enables the intended creativity. Never deserialize arbitrary runtime objects or execute downloaded native code merely because a storefront delivered it.

## Stable mod contract

Each package should have a manifest with stable ID, semantic version, game/API compatibility range, dependencies, conflicts, author, license, content hashes and requested capabilities. Validate paths against traversal, enforce size/count limits and load only allowlisted formats.

Keep the base game and mod API separate. Prefer versioned commands/events over direct access to engine objects. Define deterministic load order and expose diagnostics showing resolved versions, conflicts and rejection reasons.

## Publishing pipeline

`author → local validation → preview/test sandbox → package/hash → upload → automated scan → moderation → distribution → runtime validation`

Steam Workshop supplies storage, discovery, rating, subscription and delivery through `ISteamUGC`, but the game still owns the authoring tools, format validation, loading and compatibility model. New subscriptions may download after the game launches, so show installation state and avoid assuming content is ready immediately.

## Safety and community operations

- Treat names, descriptions, thumbnails and files as untrusted input.
- Provide report, block, takedown, appeal and emergency-disable paths.
- Separate local-only mods from multiplayer-approved content.
- For authoritative multiplayer, the server chooses the allowed package set and verifies hashes.
- Make save files record mod IDs/versions and fail with an actionable missing-mod report.
- Publish creator guidelines, IP/licensing rules, privacy rules and a compatibility policy.

## Test matrix

Test missing dependencies, cycles, conflicting IDs, old/new API versions, corrupt archives, oversized assets, path traversal, duplicate packages, mid-session removal, save recovery, offline mode and multiplayer mismatch. Fuzz manifest and parser boundaries.

## Sources

- Steam Workshop overview: https://partner.steamgames.com/doc/features/workshop
- Steam Workshop implementation: https://partner.steamgames.com/doc/features/workshop/implementation
- Unreal Game Features and Modular Gameplay: https://dev.epicgames.com/documentation/en-us/unreal-engine/game-features-and-modular-gameplay-in-unreal-engine
- OWASP Game Security Framework: https://owasp.org/www-project-gamesec-framework/OGSF

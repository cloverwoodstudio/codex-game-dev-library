# Patching, staged rollout and rollback

Reviewed: 2026-08-29

An update changes code, content, saves, backend schemas, remote configuration and player expectations. Promote one already-tested immutable artifact through channels; do not rebuild different bytes for production.

## Patch contract

Record build/content/schema versions, supported upgrade paths, required disk/download space, save and network compatibility, backend/config dependencies, rollout cohorts, health metrics, rollback threshold, player message and retained rollback artifact.

## Release sequence

`build/sign → clean install + upgrade tests → migration/backward-compatibility tests → private/beta branch → canary cohort → monitor → staged expansion → default → post-release verification`

Steam supports private beta branches and build manifests with file hashes; its documentation recommends testing updates on a branch before moving the selected build to default. itch.io butler uses channels and generates differential patches. Test through the storefront client because depot/channel rules, permissions and patch layout are part of the product.

## Rollback reality

Code rollback may not reverse migrated saves, backend writes, purchases or generated content. Prefer expand/contract backend migrations, backward-readable saves, feature flags and dual-compatible protocol windows. Rehearse rollback with real artifacts and representative accounts.

Never delete the previous known-good build, symbols, manifests, server image, config and migration evidence until the support window closes. Pause rollout automatically or manually when crash-free sessions, data integrity, login, purchases or core-loop completion cross defined thresholds.

## Patch notes

State player-visible changes, fixes, known issues, compatibility/mod impact and required actions. Separate security-sensitive details until mitigation is broadly deployed. Localize critical instructions and preserve notes with exact build IDs.

## Sources

- Steam builds and beta branches: https://partner.steamgames.com/doc/store/application/builds
- Steam updating a build: https://partner.steamgames.com/doc/sdk/updating
- Steam update best practices: https://partner.steamgames.com/doc/store/updates
- itch.io butler pushing and channels: https://itch.io/docs/butler/pushing.html

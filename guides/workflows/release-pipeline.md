# Build, release and live operations

Reviewed: 2026-08-29

The release pipeline must be reproducible from a clean checkout. Pin engine/tool versions and record source commit, content/config versions and build environment in every artifact.

## Pipeline gates

1. format/static checks and asset validation
2. unit/integration tests
3. headless import/build per target
4. smoke launch and input-driven loop
5. save migration and network compatibility tests
6. visual/performance/accessibility checks
7. package, sign/notarize and malware scan as applicable
8. upload to a private branch/channel
9. install through the real storefront/client and retest
10. staged rollout, monitoring and rollback decision

Never place long-lived storefront credentials in the repository. Use CI secrets, minimum privileges, separate test applications/branches and audit logs.

## Release evidence

Changelog, known issues, artifact checksums, dependency/license notices, privacy/ratings declarations, save/protocol compatibility, crash-free baseline, performance captures, rollback artifact and support escalation owner.

Sources:

- Steamworks: https://partner.steamgames.com/doc/home
- Godot exporting: https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html
- itch.io butler: https://itch.io/docs/butler/

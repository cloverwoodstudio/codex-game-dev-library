# Continuous integration and build evidence

Reviewed: 2026-08-29

CI should prove that a clean machine can validate and build the project, then retain enough evidence to diagnose failure. It is not proof that the game feels correct or performs on target hardware.

## Pipeline shape

`checkout/LFS → verify versions → restore cache → validate assets/data → compile → tests → package → smoke run → evidence → optional deploy`

Use immutable engine/dependency versions, least-privilege tokens, protected environments and explicit timeouts. Never run untrusted pull-request code with release secrets. Pin third-party actions to reviewed versions or commit SHAs according to the repository's security policy.

## Fast and slow lanes

- **Pull request:** cheap deterministic checks, content validation and one smoke journey.
- **Main branch:** representative builds, integration/replay and selected visuals.
- **Nightly:** platform matrix, fuzz seeds, soak, network faults, full visuals and scans.
- **Release:** signed reproducible candidates, target-device tests, performance budgets and provenance/store gates.

Use a matrix only for combinations that answer a real compatibility question. Every matrix artifact needs a unique name containing platform/configuration/build identity.

## Evidence retention

Upload test XML/JSON, engine/editor logs, screenshots and diffs, failing seeds/replays, crash dumps, profiler summaries, manifests and packaged builds as appropriate. GitHub distinguishes caches from workflow artifacts: caches accelerate later work; artifacts preserve outputs for use or inspection after a run.

Set artifact retention from the debugging/release need and privacy classification. Fail when a required artifact is missing rather than publishing an empty success.

## Build identity

Embed commit, dirty-state flag, build number, engine version, dependency/content versions, target and timestamp or reproducible-build epoch. Generate a machine-readable manifest with hashes. A release promotion should promote an already-tested artifact, not rebuild different bytes.

## Failure behavior

Cancel superseded non-release builds, but let independent matrix cells finish when their evidence matters. Make cleanup idempotent. Distinguish infrastructure failure from test failure without converting either into success. Document local equivalents for CI commands so Codex and humans can reproduce them.

## Sources

- GitHub Actions workflow syntax and matrices: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- GitHub workflow artifacts: https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts
- GitHub artifact upload action: https://github.com/actions/upload-artifact
- Godot headless export: https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html
- Unreal Automation Tool: https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-automation-tool-overview-for-unreal-engine

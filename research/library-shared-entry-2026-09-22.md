# Shared agent entry and capability registry — implementation scope

Reviewed: 2026-09-22

Baseline: `45d91d6c191b7e42a462e70962161fc439d39a95` in
`cloverwoodstudio/codex-game-dev-library`.

The owner approved the next bounded step after the library audit: a shared entry
point for ChatGPT + DC and Codex, plus a verifiable capability registry. This is
not approval to rename the repository, replace Asset Viewer, expand Game Lab's
product scope, change games, install dependencies, merge or publish a release.

## Implemented slice

[START_HERE.md](../START_HERE.md) routes agents into existing project and library
contracts. [The registry](../capabilities/registry.json) distinguishes 12 library
capabilities from the separate Asset Viewer review evidence reference. An offline
Python checker verifies structure, safe paths, source hashes and evidence links;
unit tests and a dedicated read-only CI job cover positive and negative cases.

The imported [audit observation](evidence/library-audit-2026-09-22.json) remains
explicitly prior evidence. New registry tests do not relabel every asset tool as
retested. No command string from the registry can be executed by the checker.
Existing Codex skill paths, compatibility workflow path and product source paths
are preserved. The remote repository is not renamed.

## Findings intentionally not repaired in this PR

- Replay: unsupported algorithmVersion is accepted; out-of-range axis values are
  clamped instead of rejected. Add strict validation and port-aligned negative
  tests in a separate change, before any production replay integration.
- Local wrapper: its heavy-job lock depends on TMPDIR. Reconcile the shared lock
  protocol before new concurrent heavy jobs. Registry checks are lightweight and
  still use the current wrapper; this PR does not silently change global locks.
- Existing sample CI and external-link health: keep their results separate from
  the new registry checks. A registry PASS is not overall CI or external-link PASS.
- Asset Viewer: preserve model -> link -> interactive owner review. The currently
  indexed PROJECT FORGE document is acceptance evidence, not Viewer source code
  or a new deployment verification. ViewForge is a different reconstruction tool.

## Review boundary

Review changed files and fresh exact-head test evidence; merge requires a separate
owner decision. No signing material, production credentials, accepted asset binary,
new model, game build, provider upload or TestFlight operation is part of this work.

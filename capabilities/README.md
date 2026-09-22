# Capability registry v1

Reviewed: 2026-09-22

[registry.json](registry.json) contains 12 initial library capabilities and one
separate external Asset Viewer workflow reference. It is a curated routing map,
not an inventory of every file, not a tool installer, and not execution authority.
Start with [START_HERE.md](../START_HERE.md).

## Read-only interface

```sh
bash scripts/cloverwood-local-run.sh -- python3 -B scripts/capabilities.py --check
bash scripts/cloverwood-local-run.sh -- python3 -B scripts/capabilities.py --list
bash scripts/cloverwood-local-run.sh -- python3 -B scripts/capabilities.py --show viewforge
bash scripts/cloverwood-local-run.sh -- python3 -B -m unittest discover -s tests -v
```

Run these from the repository root. Python's standard library is sufficient;
there is no package install. The CLI validates the entire registry before showing
any entry. Invalid data, stale hashes or an unknown ID exit nonzero. Outputs go to
stdout/stderr. On local Mac runs the existing wrapper owns disposable files and
cleanup. These lightweight checks do not run Xcode, Blender or a provider.

## Versioned contract

The validator at [scripts/capabilities.py](../scripts/capabilities.py) is the v1
format authority. It accepts exactly these root fields: `schemaVersion` (integer
1), `mode` (`DISCOVERY_ONLY`), `repository`, `sourceCommit` (audit baseline),
`reviewedOn`, `isExecutionAuthority` (false), `capabilities`, `externalWorkflows`.
Unknown fields and duplicate JSON keys are errors; there is no command/run field.

Each capability declares a stable `id`, `title`, `kind`, pinned local `entrypoint`,
`sources` (path -> SHA-256), `requiredTools`, `inputs`, `outputs`, `integrationStatus`,
`verification`, `limitations`, and `authorizationRequired`. Requirements are text
for planning, never shell expressions. Source paths must be bounded, relative,
existing regular files inside this repository; symlinks and traversal are rejected.

Kinds distinguish `PLAYBOOK`, `PLAYBOOK_AND_PSEUDOCODE`, `REFERENCE_CATALOG`,
`EXECUTABLE_HELPER`, `RUNNABLE_SAMPLE`, and `EXTERNAL_TOOL_LAB_FIXTURE`.
Integration states are `NONE`, `PROPOSED`, `PER_PROJECT`,
`NOT_SHARED_IMPLEMENTATION`, and `REFERENCE_ONLY`. None means production approval.

Verification contains a `level`, ISO `date`, limited `scope`, and `evidence` paths
which must also be pinned in `sources`. Allowed levels:

- `SOURCE_REVIEWED`: guidance reviewed, not a workload run.
- `HOST_DISCOVERY_ONLY`: selected installed tools observed, not helper/workload PASS.
- `HISTORICAL_FIXTURE`: prior bounded evidence, not a current upstream re-test.
- `LIMITED_TEST_WITH_GAPS`: existing tests passed with disclosed blockers; never an
  integrated production capability. The replay sample remains in this category.

The imported [prior audit observation](../research/evidence/library-audit-2026-09-22.json)
records the earlier JavaScript and host checks. It is not a fabricated fresh run.

## What a registry PASS does and does not establish

PASS establishes v1 structure, local path existence, recorded SHA-256 equality,
explicit evidence links and non-executing status fields. It does **not** establish
semantic correctness, security, a trusted signature, installation, current upstream
compatibility, current external availability, owner approval or production readiness.
`sourceCommit` is baseline metadata; the offline checker validates its shape, not
its existence on GitHub or the history of a local file. Reviewers verify that ref.

The external Viewer record pins a PROJECT FORGE documentation commit and Git blob.
The offline checker validates that reference's shape; it does not fetch it or prove
that the remote blob is unchanged. Current Viewer source and live deployment remain
explicitly unverified. Owner acceptance of Asset 005 cannot approve another asset.

## Maintenance

When a source changes, checks fail even if the path still exists. Read the diff,
reassess evidence/limitations, then deliberately update its SHA-256 and relevant
dates in the same reviewed PR. Do not auto-refresh pins or bump historical test
dates just to turn CI green. Evidence authenticity still depends on review: editing
both source and hash can satisfy integrity checks without proving a true claim.

Retain IDs and old paths unless a separately reviewed migration is needed. Add a
capability only for a concrete use. No new agent-specific execution engine, Viewer,
provider integration or deployment workflow belongs in this registry change.

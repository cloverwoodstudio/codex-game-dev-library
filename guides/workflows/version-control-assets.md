# Version control for game projects and large assets

Reviewed: 2026-08-29

Game repositories combine mergeable text with large binary assets and editor-owned files. The goal is not one universal tool, but a deliberate policy that prevents silent loss and keeps builds reproducible.

## Choose the storage model

| Situation | Practical default | Main trade-off |
|---|---|---|
| Small team, code-heavy project | Git plus Git LFS | Familiar workflow; LFS storage and bandwidth need monitoring |
| Many artists and binary assets | Perforce Helix Core | Strong locking/large-file workflows; more administration |
| Unity-focused team wanting managed tooling | Unity Version Control | Editor integration and file locking; service dependency |

Do not place generated caches, imported libraries, local builds, IDE state, secrets or platform signing material in source control. Do version engine/project settings, dependency locks, source assets, import metadata required for stable asset identity, build scripts and schemas.

## Binary policy

Classify every extension as one of:

- text and mergeable;
- text but editor-generated, requiring semantic merge or ownership rules;
- binary and lockable;
- generated and ignored.

Use LFS before the first large binary lands in history. Enable locking for files that cannot be safely merged. A lock is coordination, not a backup: short branches, visible ownership and frequent integration still matter.

Unity provides `UnityYAMLMerge`/Smart Merge for scene and prefab YAML. Unreal's One File Per Actor reduces contention by storing world actors in separate files, while its editor has built-in source-control integration. These mechanisms reduce conflicts; they do not make concurrent edits automatically safe.

## Repository contract

Record these decisions in `CONTRIBUTING.md` or `AGENTS.md`:

1. exact engine version and dependency lock;
2. tracked, ignored, LFS and lockable patterns;
3. asset naming, folder and ownership conventions;
4. scene/prefab/map merge procedure;
5. maximum normal Git blob size;
6. required validation before merge;
7. recovery procedure for a broken asset or migration.

## Change workflow

1. Pull and verify the project opens before editing shared assets.
2. Lock non-mergeable assets or announce ownership.
3. Keep source asset and its metadata/import settings together.
4. Commit one coherent change with any migration or build-script update.
5. Open the project from a clean checkout and run the smallest representative build.
6. Unlock only after the pushed commit is available to collaborators.

## CI checks

- reject oversized non-LFS blobs and forbidden file types;
- detect missing LFS objects and case-only path collisions;
- verify engine/dependency versions;
- run asset/database validation and a headless build;
- report duplicate IDs, broken references and unexpected generated changes.

## Sources

- Git LFS locking API: https://github.com/git-lfs/git-lfs/blob/main/docs/api/locking.md
- Unity Smart Merge: https://docs.unity.cn/Manual/SmartMerge.html
- Unreal source control: https://dev.epicgames.com/documentation/en-us/unreal-engine/source-control-in-unreal-engine
- Unreal One File Per Actor: https://dev.epicgames.com/documentation/en-us/unreal-engine/one-file-per-actor-in-unreal-engine
- Perforce for game development: https://www.perforce.com/solutions/game-development

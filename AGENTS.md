# Instructions for game-development agents

This repository is a shared game-development knowledge base. Preserve it as a source-backed, engine-neutral library.

## Shared entry and capability discovery

Read `START_HERE.md` and `capabilities/README.md`. These rules apply to ChatGPT + DC, Codex and other authorized agents. Load relevant skill files explicitly when automatic discovery is not available. Registry entries are non-executing pointers, not installed-tool proof or authorization. Preserve Asset Viewer as the external owner-review workflow; do not confuse it with ViewForge.

## When using this library to build a game

1. Read `guides/engine-selection.md`, the matching `guides/engines/*.md`, and `guides/workflows/codex-loop.md`.
   Route broader work through `guides/game-development-map.md`; consult only the relevant design, art, systems, prompt, and code-pattern files.
   For any Apple target, also load `.agents/skills/apple-platform-development/SKILL.md`, read `guides/platforms/apple.md` and `guides/workflows/apple-build-release.md`, then create `APPLE_TEST_MATRIX.md` from its template. Use the skill's catalog progressively rather than loading every tool section.
2. Create a concrete `PLAN.md` from `templates/PLAN.template.md` before scaffolding.
3. Define player goal, core loop, controls, win/fail states, target hardware, performance budgets, art direction, acceptance criteria, and milestone order.
4. Build a tiny playable vertical slice before content expansion.
5. Run the game after meaningful changes. Test controls and state transitions; capture screenshots or recordings for visual review.
6. Prefer deterministic logic and headless tests for systems; use real play sessions for feel, rendering, audio, and performance.
7. Keep generated asset prompts and provenance. Never assume an asset is commercially usable without checking its license.
   For models reconstructed from images, datasheets or technical drawings, load `.agents/skills/reference-sheet-to-3d/SKILL.md` and follow `guides/art/datasheet-to-3d.md`; create a dimension ledger and validation report before claiming dimensional accuracy.
8. Profile on target hardware before optimizing. Record baseline and after-change evidence.
9. Keep commits small and do not overwrite unrelated user work.

## When extending this library

- Prefer primary/current sources and link the exact page.
- Paraphrase; do not paste copyrighted tutorials.
- Record `Reviewed: YYYY-MM-DD` on engine guides.
- Label community advice as community advice.
- Verify links and avoid unlicensed code/assets.
- Update `references/source-index.md` and `research/backlog.md`.
- Put reusable prompts in `prompts/`, engine-neutral examples in `code-patterns/`, and tested engine-specific examples in a clearly named future sample project.

## Definition of done for a game task

- The requested behavior works in a real run.
- Automated checks relevant to the change pass.
- Controls and main state transitions were exercised.
- Visual changes were inspected at representative viewport sizes.
- Performance-sensitive changes were measured.
- Documentation and durable decisions were updated.

## Local Mac build/test cleanup — OWNER LOCKED 2026-09-09
- This rule is mandatory for every agent and every local Mac build, test or CI run.
- Before a run, measure free disk space. For Xcode, 3D or other large runs, do not start below 20 GiB free; clean stale repo-scoped disposable artifacts first.
- Every run MUST route regenerable outputs to a unique disposable repo-scoped root under `${TMPDIR:-/tmp}/cloverwood-ci/<repo>/<run-id>/` whenever the tool supports an explicit path.
- Xcode must use `-derivedDataPath <run-root>/DerivedData`; SwiftPM must use `--scratch-path <run-root>/swiftpm`; test results, temporary logs, caches, temp clones/worktrees and run-only captures must also stay under the run root when practical.
- Register cleanup with shell `trap` / `finally` semantics where supported so cleanup runs after PASS, FAIL, cancellation or early exit.
- Immediately after each run, delete all run-generated disposable artifacts and verify the run root no longer exists.
- A run is not `PASS`, `READY`, or merge-ready if cleanup was skipped, cleanup verification failed, or the disk-space receipt is missing.
- Preserve source, authored assets, locked references, intentional QA evidence/receipts, signed/release archives and user files. Never delete those as cleanup.
- Never delete whole simulators, runner installations, repositories, keychains, credentials or broad user/global caches merely to free space.
- After an interrupted/crashed run, the next agent must sweep stale repo-scoped disposable run directories before starting new work.
- Record free-space-before, free-space-after, cleanup status and any intentionally retained evidence path in the run receipt.

## Mandatory local-run wrapper — OWNER LOCKED 2026-09-09
- Every local Mac build, test or CI command MUST run through `bash scripts/cloverwood-local-run.sh -- <command> [args...]` so disposable storage, disk gating, signal-safe cleanup and the cleanup receipt are enforced.
- For Xcode, 3D or other heavy Mac workloads set `CLOVERWOOD_EXCLUSIVE_MAC=1` so two heavy jobs cannot compete for CoreSimulator/build storage on the same Mac.
- Do not bypass the wrapper to obtain PASS/READY. If a tool technically cannot be nested under the wrapper, reproduce the same disposable run-root + trap/finally + deletion verification contract and emit an equivalent cleanup receipt.

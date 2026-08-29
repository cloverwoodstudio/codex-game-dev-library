# Instructions for Codex agents

This repository is a shared game-development knowledge base. Preserve it as a source-backed, engine-neutral library.

## When using this library to build a game

1. Read `guides/engine-selection.md`, the matching `guides/engines/*.md`, and `guides/workflows/codex-loop.md`.
   Route broader work through `guides/game-development-map.md`; consult only the relevant design, art, systems, prompt, and code-pattern files.
   For any Apple target, also read `guides/platforms/apple.md` and `guides/workflows/apple-build-release.md`, then create `APPLE_TEST_MATRIX.md` from its template.
2. Create a concrete `PLAN.md` from `templates/PLAN.template.md` before scaffolding.
3. Define player goal, core loop, controls, win/fail states, target hardware, performance budgets, art direction, acceptance criteria, and milestone order.
4. Build a tiny playable vertical slice before content expansion.
5. Run the game after meaningful changes. Test controls and state transitions; capture screenshots or recordings for visual review.
6. Prefer deterministic logic and headless tests for systems; use real play sessions for feel, rendering, audio, and performance.
7. Keep generated asset prompts and provenance. Never assume an asset is commercially usable without checking its license.
   For models reconstructed from datasheets or technical drawings, follow `guides/art/datasheet-to-3d.md`; create a dimension ledger and validation report before claiming dimensional accuracy.
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

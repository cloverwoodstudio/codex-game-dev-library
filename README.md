# Codex Game Development Library

A living, source-backed playbook for building games with Codex. This repository is designed to be cloned into, linked from, or consulted by every Codex agent working on a game.

## Start here

1. Read [`AGENTS.md`](AGENTS.md).
2. Pick an engine with [`guides/engine-selection.md`](guides/engine-selection.md).
3. Copy [`templates/PLAN.template.md`](templates/PLAN.template.md) as `PLAN.md` and [`templates/ENGINE_BOOTSTRAP.template.md`](templates/ENGINE_BOOTSTRAP.template.md) as `ENGINE_BOOTSTRAP.md`.
4. Read the matching playbook in [`guides/engines/`](guides/engines/) and verify its command patterns for the pinned version.
5. Follow [`guides/workflows/codex-loop.md`](guides/workflows/codex-loop.md).
6. Use [`references/source-index.md`](references/source-index.md) for current documentation and proven examples.

## Library map

- `guides/` — distilled, actionable guidance
- `guides/engines/` — engine-specific playbooks
- `guides/platforms/` — platform engineering, including Apple and XR
- `guides/design/` — player experience, worlds, characters and game rules
- `guides/systems/` — architecture, gameplay systems, networking and security
- `guides/art/` — visual, 3D and VFX production pipelines
- `guides/workflows/` — repeatable Codex workflows
- `templates/` — files to copy into new game repositories
- `references/` — curated primary sources and example repositories
- `research/` — research notes, findings, and backlog
- `prompts/` — reusable briefs and prompts for Codex and asset generation
- `code-patterns/` — engine-neutral reference implementations

## Complete development map

See [`guides/game-development-map.md`](guides/game-development-map.md) for the full path from idea and worldbuilding through code, art, audio, testing, release, and live operations.

## Core principle

Game development is an empirical loop: **specify → build the smallest playable slice → run → observe → measure → adjust → preserve the evidence**. A build passing is necessary, but the game must also be played and visually inspected.

## Scope and status

This is a growing foundation, not a claim to contain the whole internet. It now covers the playable-development loop plus art, audio, worlds, systems, accessibility, localization, platforms, provenance, release, modding, backend security, observability, performance and store preparation. Game engines and Codex evolve continuously. Every important claim should link to a primary source, record a review date, and distinguish official guidance from community experience.

## Contributing

Add distilled knowledge, not copied articles. Prefer official manuals, original talks/papers, maintained example repositories, and reproducible experiments. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

License: [CC BY 4.0](LICENSE) for the written knowledge in this repository. Linked code and assets retain their original licenses.

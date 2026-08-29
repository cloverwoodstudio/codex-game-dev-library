# Godot production playbook

Reviewed: 2026-08-29

## Best fit

Choose Godot when a small team values a fast editor loop, open-source tooling, compact distribution, and strong 2D support. Prove platform exports, renderer compatibility, console requirements, and native SDK integrations before committing a large production.

## Recommended project shape

```text
project.godot
src/
  core/          # deterministic rules and shared types
  features/      # player-facing mechanics, grouped vertically
  presentation/  # cameras, effects, animation and UI adapters
tests/
tools/
assets/source/   # editable originals; keep runtime exports separate
```

- Build reusable scenes as self-contained compositions.
- Use signals or narrow interfaces across feature boundaries; avoid brittle deep node paths.
- Reserve autoloads for state that genuinely spans scenes, such as session routing or save access.
- Keep calculations and state transitions outside `_process()` and `_physics_process()` when they can be plain deterministic functions.
- Use Resources for authored configuration, with stable IDs when data is saved or referenced externally.

## Codex loop

1. Read `project.godot`, the owning scene and its direct scripts before editing.
2. Express the requested behavior as a small state transition or acceptance test.
3. Change one feature boundary at a time; let the editor reimport moved or added resources.
4. Run a focused scene, then the normal entry scene.
5. Inspect runtime errors, controls, transitions and a screenshot or recording.
6. Export the real target preset before declaring a milestone complete.

Typical command shapes—replace placeholders with the installed executable, paths and exact preset names:

```sh
godot --headless --path <project> --editor --quit
godot --path <project> <scene.tscn>
godot --headless --path <project> --export-release "<Preset>" <output>
```

The built-in `--test` option runs Godot's own engine tests; project tests need a chosen test harness or a purpose-built headless runner. Record that choice in `PLAN.md` and never claim tests ran unless their process exited successfully.

## Validation ladder

1. Pure rule tests with fixed seeds and inputs.
2. Headless project load/import smoke check.
3. Focused mechanic test scene.
4. Full entry-scene play session with real controls.
5. Release export launched outside the editor.
6. Profiler capture on representative target hardware.

## Assets and performance

- Keep `.godot/` generated state out of source control; commit source assets and relevant sidecars.
- Batch renames and moves through the editor where practical, then check broken resource paths.
- Set frame, memory, draw-call and loading budgets before content expansion.
- Profile the actual bottleneck. Avoid per-frame allocation, repeated tree searches and excessive node counts only when measurements justify the change.
- Verify every export template, native extension, renderer and platform permission in CI or on a clean machine.

## Primary sources

- [Best practices](https://docs.godotengine.org/en/stable/tutorials/best_practices/index.html)
- [Command-line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)
- [Exporting projects](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html)
- [Profiler](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/the_profiler.html)

# Godot

Reviewed: 2026-08-29

Follow scene composition and project-organization guidance from the stable manual. Keep reusable scenes self-contained, avoid global autoloads unless state truly spans scenes, and separate deterministic domain logic from node lifecycle code so it can be tested.

Codex-friendly practices: prefer text resources where practical; run editor/import checks after moving resources; use command-line/headless runs for CI; create tiny test scenes for mechanics; capture runtime errors, screenshots, and performance monitors.

Primary sources:

- https://docs.godotengine.org/en/stable/tutorials/best_practices/index.html
- https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html
- https://docs.godotengine.org/en/stable/tutorials/scripting/debug/the_profiler.html

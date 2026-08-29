# Data-driven content and internal tools

Reviewed: 2026-08-29

Data-driven design moves variation into validated, versioned content without turning every field into an uncontrolled programming language. Stable schemas and author feedback matter more than the choice of spreadsheet, inspector or custom editor.

## Content contract

Each record needs stable ID, schema version, type, localization keys, references by stable ID, bounds/enums, platform or feature gates, provenance and deprecation state. Runtime code consumes a compiled/validated representation rather than arbitrary author files.

Separate source data from generated runtime data. Generated outputs carry compiler/tool version, source hashes and dependency manifest; they are reproducible and usually not hand-edited.

## Authoring pipeline

`source → schema validation → semantic validation → reference graph → compile/import → preview → playtest → package manifest`

Errors should name the exact asset, field, expected rule and suggested repair. Validate uniqueness, missing/cyclic references, unreachable content, localization, numeric bounds, asset compatibility and platform budgets before the game launches.

## Tool design

Build a tool only after observing repeated work. Preserve undo/redo, multi-selection, search, copy/paste, keyboard use, source-control visibility and safe cancellation. Preview with the same runtime code where practical. Batch operations need dry-run, explicit scope and an audit report.

External spreadsheets can be useful for bulk tuning—Unreal supports DataTables and CurveTables imported through CSV workflows—but repository schemas and validators remain authoritative. Never execute spreadsheet formulas/macros in the build pipeline without a deliberate trust decision.

## Compatibility

Add fields with defaults when possible, migrate sequentially, reserve deleted IDs and reject unknown incompatible schema versions. Save games, replays, mods and live config must state which content/schema version they reference.

## Sources

- Unreal data-driven gameplay: https://dev.epicgames.com/documentation/en-us/unreal-engine/data-driven-gameplay-elements-in-unreal-engine
- Godot Resources: https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html
- JSON Schema specification: https://json-schema.org/specification

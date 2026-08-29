# Engine selection

Choose from constraints, not popularity. Prototype the riskiest requirement in the top two candidates when the decision is expensive to reverse.

| Need | Strong starting point | Why |
|---|---|---|
| 2D browser game | Phaser + TypeScript | Browser-native, fast feedback, extensive examples |
| Custom browser 3D rendering | Three.js | Maximum rendering control; game systems must be built |
| Integrated browser 3D/XR | Babylon.js | More built-in engine subsystems and tooling |
| Small/medium open-source 2D or 3D game | Godot | Text-friendly scenes/resources, small editor, strong 2D |
| Cross-platform commercial mobile/indie | Unity | Broad platform/tool ecosystem, C#, mature profiling |
| High-end 3D, console/PC, large worlds | Unreal Engine | Advanced rendering, gameplay framework, C++/Blueprints |
| Native Apple 2D game | SpriteKit | Direct platform integration; narrower portability |
| Native Apple 3D/spatial game | RealityKit | Modern Apple ECS/USD path; Apple-focused |
| Custom Apple renderer or advanced port | Metal | Maximum graphics control; highest engineering cost |
| Rust ECS game | Bevy | Data-oriented schedules and plugins; fast-moving API |
| Minimal native C game | raylib | Small transparent API; architecture and tools are yours |
| Code-first C# game | MonoGame | XNA-style loop and content pipeline; no prescribed scene editor |
| Fully custom engine | custom C/C++/Rust | Maximum control; greatest engineering burden |

Evaluate target platforms, team language, source-control friendliness, headless/CLI builds, automated testing, licensing/royalties, asset ecosystem, accessibility, localization, networking, build size, performance targets, and console access. Re-check current commercial terms at decision time.

After choosing, read the matching guide in `guides/engines/` and complete `templates/ENGINE_BOOTSTRAP.template.md` beside the game's `PLAN.md`. Treat every command in the engine guide as a pattern until it has been verified against the project's exact version and installation.

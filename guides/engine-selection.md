# Engine selection

Choose from constraints, not popularity. Prototype the riskiest requirement in the top two candidates when the decision is expensive to reverse.

| Need | Strong starting point | Why |
|---|---|---|
| 2D browser game | Phaser + TypeScript | Browser-native, fast feedback, extensive examples |
| Custom 2D/3D browser rendering | PixiJS or Three.js | Lower-level control; more systems must be built |
| Small/medium open-source 2D or 3D game | Godot | Text-friendly scenes/resources, small editor, strong 2D |
| Cross-platform commercial mobile/indie | Unity | Broad platform/tool ecosystem, C#, mature profiling |
| High-end 3D, console/PC, large worlds | Unreal Engine | Advanced rendering, gameplay framework, C++/Blueprints |
| Native Apple-focused game | SpriteKit/SceneKit/Metal | Direct platform integration; narrower portability |
| Data-oriented custom engine | Bevy, raylib, MonoGame, custom C++ | Maximum control; greater engineering burden |

Evaluate target platforms, team language, source-control friendliness, headless/CLI builds, automated testing, licensing/royalties, asset ecosystem, accessibility, localization, networking, build size, performance targets, and console access. Re-check current commercial terms at decision time.

After choosing, read the matching guide in `guides/engines/` and complete `templates/ENGINE_BOOTSTRAP.template.md` beside the game's `PLAN.md`. Treat every command in the engine guide as a pattern until it has been verified against the project's exact version and installation.

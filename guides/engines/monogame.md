# MonoGame production playbook

Reviewed: 2026-08-29

## Best fit

Choose MonoGame when a C# team wants a code-first game loop, mature XNA-style APIs and direct control without a scene editor prescribing architecture. It supplies a framework rather than a complete editor-driven engine, so content tools, UI, scene flow, physics and production conventions must be selected deliberately.

## Recommended project shape

```text
Game.sln
src/
  Game.Core/          # deterministic rules; no graphics dependency
  Game.Runtime/       # Game loop and feature coordination
  Game.Presentation/  # graphics, audio and input adapters
  Game.Content/       # MGCB content project
tests/Game.Core.Tests/
tools/
```

- Keep `Game.Update` thin: sample input, advance explicit state and coordinate feature systems.
- Keep `Game.Draw` presentation-only; never make gameplay outcomes depend on whether a frame rendered.
- Separate authored content source from generated MGCB output and document custom processors.
- Centralize input actions and viewport transforms.
- Put save/network data in versioned contracts independent of `Texture2D`, `SpriteBatch` and other runtime objects.

## Codex loop

1. Read the solution, target frameworks, package versions, `.mgcb` file and `Game` subclass.
2. Add a focused .NET test for pure rules.
3. Implement through the smallest runtime/presentation boundary.
4. Restore, format/check, test, build content and compile using repository-defined commands.
5. Run the desktop target, exercise controls and transitions, and inspect visual evidence.
6. Publish and launch the intended target artifact, then profile it on target hardware.

Typical roles, subject to project templates and target platform:

```sh
dotnet restore
dotnet test
dotnet build
dotnet publish -c Release
```

MGCB commands and platform packaging depend on the installed MonoGame templates/tools. Record their exact versions and verified invocations in `ENGINE_BOOTSTRAP.md`.

## Validation ladder

1. Pure .NET rule tests with fixed time and random seeds.
2. Content build on a clean checkout.
3. Compile every supported target configuration.
4. Interactive controls/state-transition pass.
5. Published artifact launched outside the IDE.
6. Target-device CPU, GPU, memory, loading and garbage-collection capture.

## Framework traps

- Avoid allocation-heavy LINQ, string creation and transient collections in measured hot paths.
- Dispose owned graphics/audio/content resources, while respecting `ContentManager` ownership.
- Recreate or reload graphics resources correctly after device/reset lifecycle events on relevant platforms.
- Test viewport scaling, letterboxing, high-DPI input transforms and resize.
- Do not assume desktop file paths, casing or codecs behave identically on mobile, console or packaged builds.

## Primary sources

- [MonoGame documentation](https://docs.monogame.net/)
- [Getting started](https://docs.monogame.net/articles/getting_started/index.html)
- [Content Pipeline](https://docs.monogame.net/articles/getting_started/content_pipeline/why_content_pipeline.html)
- [MonoGame samples](https://github.com/MonoGame/MonoGame.Samples)

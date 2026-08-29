# raylib production playbook

Reviewed: 2026-08-29

## Best fit

Choose raylib when the team wants a small, transparent C library, a hand-built game loop, rapid native prototypes or an educational/custom-engine foundation. It intentionally leaves architecture, tools, scenes, asset pipelines and most higher-level systems to the game.

## Recommended project shape

```text
CMakeLists.txt
src/
  core/          # deterministic rules with no raylib dependency
  features/      # bounded gameplay systems
  platform/      # raylib window, input, audio and files
  render/        # drawing and resource adapters
tests/
assets/source/
assets/runtime/
```

- Choose one reproducible dependency strategy: pinned source/submodule, package manager, or vendored release.
- Hide raylib calls behind narrow platform/render boundaries when logic should run headlessly.
- Pair every successful `Load*` with a clearly owned `Unload*` path.
- Centralize screen modes and input actions; keep drawing out of state-transition rules.
- Use fixed simulation steps when deterministic or physics-sensitive behavior requires them.

## Codex loop

1. Read the toolchain file, CMake options, pinned raylib version and platform definitions.
2. Add a C unit test for deterministic rules before touching the render loop.
3. Implement through explicit update/draw/resource boundaries.
4. Configure and build both Debug and Release with warnings enabled.
5. Run with sanitizers on supported desktop toolchains.
6. Play with real input, then package and launch on the target platform.

Representative CMake command shapes:

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
ctest --test-dir build --output-on-failure
cmake -S . -B build-release -DCMAKE_BUILD_TYPE=Release
cmake --build build-release
```

Multi-configuration generators and cross-platform targets differ. Store working presets or wrapper scripts instead of asking contributors to reconstruct flags.

## Validation ladder

1. Pure C rule tests.
2. Warning-clean Debug build.
3. Address/undefined-behavior sanitizer run where supported.
4. Small interactive proof scene covering load/update/draw/unload.
5. Release build launched outside the IDE.
6. Platform-specific package and performance capture.

## Native-code traps

- Check return values and validity helpers for loaded resources; exercise missing/corrupt asset paths.
- Treat buffer sizes, ownership, lifetime and integer conversions as review-critical.
- Keep compiler warnings high and CI across at least the supported host/target combinations.
- Test minimization, focus, resize, gamepad reconnect, audio shutdown and clean exit.
- Do not copy example code or third-party extensions without checking the exact license and version.

## Primary sources

- [raylib repository and learning guidance](https://github.com/raysan5/raylib)
- [Official examples](https://github.com/raysan5/raylib/tree/master/examples)
- [CMake options](https://github.com/raysan5/raylib/blob/master/CMakeOptions.txt)
- [API cheatsheet](https://www.raylib.com/cheatsheet/cheatsheet.html)
- [Official game template](https://github.com/raysan5/raylib-game-template)

# Babylon.js production playbook

Reviewed: 2026-08-29

## Best fit

Choose Babylon.js when a browser-first 3D game benefits from a more integrated engine layer: scenes, cameras, input, materials, animation, physics adapters, GUI, loaders, inspector and WebXR. Validate the exact package set, renderer backend, browser/device matrix and deployment footprint because convenient subsystems can expand bundle and compatibility scope.

## Recommended project shape

```text
src/
  game/core/       # deterministic rules and serializable state
  game/features/   # gameplay commands and systems
  babylon/         # Engine/Scene ownership and presentation adapters
  platform/        # input, audio unlock, storage and page lifecycle
  ui/              # accessible DOM shell or Babylon GUI adapters
public/assets/
tests/
```

- Create one documented owner for `Engine` and each active `Scene`.
- Keep game identity/state independent from mesh names and scene traversal order.
- Import only the packages/features actually used and measure the production bundle.
- Keep physics implementation behind a narrow adapter; lock plugin and initialization choices.
- Define whether UI lives in accessible DOM, Babylon GUI, or a deliberate combination.

## Codex loop

1. Read package versions, engine/scene bootstrap, render loop, loaders and disposal path.
2. Add deterministic tests outside Babylon for gameplay rules.
3. Implement the smallest adapter into Scene entities, animation, camera and audio.
4. Run repository-defined static checks, tests and production build.
5. Exercise the result in a real browser with console/network capture and visual evidence.
6. Use Inspector or instrumentation for diagnosis, then measure production mode on target devices.

## Validation ladder

1. Pure simulation tests with fixed inputs and time.
2. Type, lint and unit checks.
3. Scene creation/disposal smoke cycles.
4. Asset and physics initialization failure paths.
5. Automated critical input flow plus screenshots.
6. Cross-browser/device run of the production bundle.
7. CPU/GPU/memory evidence for a representative scene and repeated transitions.

## Engine and delivery traps

- Dispose scenes, engine resources, observers and event handlers according to explicit ownership.
- Do not optimize by intuition: use engine instrumentation, browser traces and target-device captures.
- Test shader compilation, texture formats, hardware scaling and post-processing fallbacks on low-tier GPUs.
- Test audio unlock, focus/visibility, resize, orientation, context loss and WebXR session teardown where applicable.
- Prefer offline asset validation and stable IDs over runtime searches by display names.
- Serve the built artifact through the intended URL base, cache headers and content-security policy.

## Primary sources

- [Babylon.js documentation](https://doc.babylonjs.com/)
- [Babylon.js specifications](https://www.babylonjs.com/specifications/)
- [Babylon.js repository](https://github.com/BabylonJS/Babylon.js)
- [Babylon.js examples and playground](https://playground.babylonjs.com/)

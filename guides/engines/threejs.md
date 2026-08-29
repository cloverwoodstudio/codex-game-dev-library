# Three.js production playbook

Reviewed: 2026-08-29

## Best fit

Choose Three.js when the product needs custom browser 3D and the team wants direct control over scene, renderer, assets and application architecture. Three.js is a rendering library rather than a complete game engine: input actions, collision/physics, navigation, save data, UI, audio policy, scene flow and content tools remain explicit project decisions.

## Recommended project shape

```text
src/
  game/core/        # deterministic rules; no Three.js imports
  game/features/    # gameplay slices and commands
  render/           # scene graph, cameras, materials and effects
  platform/         # browser input, audio, storage and lifecycle
  ui/               # DOM accessibility and menus
public/assets/
tests/
```

- Pin `three` and import addons from the same release; do not mix CDN/package versions.
- Keep simulation IDs separate from `Object3D` identity and names.
- Make ownership of textures, geometries, materials, render targets, controls and listeners explicit.
- Use glTF as the normal runtime exchange format and validate asset conventions before bulk production.
- Treat WebGPU renderer adoption as a deliberate compatibility project, especially with custom shaders.

## Codex loop

1. Read `package.json`, lockfile, renderer creation, animation loop and asset loaders.
2. Implement deterministic rules without renderer dependencies and test them with fixed steps.
3. Adapt rule state into a small scene/presentation boundary.
4. Run the repository's existing type, lint, test and production-build scripts.
5. Play the built result with browser input; inspect console, network and canvas screenshots.
6. Record `renderer.info`, frame timings and memory behavior before and after representative level transitions.

Never invent npm script names. Common roles are dependency install, type check, lint, unit tests, build and Playwright end-to-end tests; record their exact commands in `ENGINE_BOOTSTRAP.md`.

## Validation ladder

1. Fixed-step simulation tests with seeded randomness.
2. Type/lint/unit checks.
3. Loader failure and cancelled-load tests.
4. Browser input and scene-transition automation.
5. Screenshot review across representative viewports and pixel ratios.
6. Production bundle under the real base path and caching policy.
7. Target-device GPU/CPU/memory capture through repeated load/unload cycles.

## Rendering and lifecycle traps

- Removing an object from a Scene does not dispose its GPU resources. Call the appropriate `dispose()` methods when project ownership ends.
- Shared resources need reference ownership; premature disposal can create stalls or broken rendering.
- Cap device pixel ratio according to measured GPU budget rather than blindly rendering at the display maximum.
- Test WebGL/context loss, hidden tabs, resize, fullscreen, pointer lock, slow asset delivery and unsupported features.
- Compile representative shaders during controlled loading where possible; runtime material variation can create visible stalls.

## Primary sources

- [Installation](https://threejs.org/manual/en/installation.html)
- [Responsive design](https://threejs.org/manual/en/responsive.html)
- [Cleanup](https://threejs.org/manual/en/cleanup.html)
- [How to dispose of objects](https://threejs.org/manual/en/how-to-dispose-of-objects.html)
- [WebGPU renderer](https://threejs.org/manual/en/webgpurenderer)

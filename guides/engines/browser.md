# Browser and Phaser production playbook

Reviewed: 2026-08-29

## Best fit and stack boundary

Browser games are ideal for instant access, link sharing, game jams, portals, playable marketing and cross-device 2D experiences. Use Phaser for conventional 2D game structure, PixiJS when the main need is rendering, and Three.js or Babylon.js for 3D. Add a UI framework only when menus, account flows or surrounding application UI justify the second lifecycle.

Prove browser support, mobile memory, touch ergonomics, audio policy, hosting limits, asset delivery and offline expectations before content expansion.

## Recommended project shape

```text
src/
  game/
    core/          # deterministic simulation, no DOM or renderer ownership
    features/      # gameplay slices
    presentation/  # Phaser scenes, objects, cameras, audio and effects
  ui/              # DOM application shell when needed
public/assets/
tests/
tools/
```

- Advance simulation through explicit inputs and time steps rather than hiding rules inside `requestAnimationFrame` callbacks.
- Seed randomness and expose small read-only debug snapshots for repeatable tests.
- Keep DOM/UI and canvas ownership clear; do not let both systems independently own pause, focus or input state.
- In Phaser, use Scenes as lifecycle and presentation boundaries. Keep durable domain state outside Scene objects when it must survive restarts or be tested without rendering.
- Centralize input actions so keyboard, pointer, touch and gamepad can drive the same intent.

## Codex loop

1. Read `package.json`, its lockfile, build config, entry point and relevant Scene before editing.
2. Use the repository's existing scripts; never invent a script name from this guide.
3. Add a deterministic unit test for simulation rules when possible.
4. Run type checking, lint and tests, then a production build.
5. Launch locally and play with real browser input.
6. Automate the critical flow with Playwright and inspect canvas screenshots, console errors and network failures.
7. Test the built artifact through the real hosting path or an equivalent static server.

Common script roles—not guaranteed names—are:

```sh
npm ci
npm run lint
npm test
npm run build
npm run e2e
```

## Validation ladder

1. Pure simulation tests with fixed seeds and time steps.
2. Type check, lint and production compilation.
3. Scene boot smoke test with console and unhandled-rejection capture.
4. Playwright input path plus screenshot evidence.
5. Manual keyboard, pointer, touch and gamepad pass as applicable.
6. Production bundle served under the intended base path with cache headers.
7. Cross-browser and representative mobile-device performance pass.

## Browser lifecycle checklist

Test focus loss, hidden tabs, pause/resume, audio unlock, resize, orientation, device-pixel ratio, fullscreen, pointer lock, back navigation, context loss, slow/offline network, asset failure, storage denial, controller reconnect and accessibility both outside and inside the canvas.

## Performance and delivery

- Budget initial download, decoded image/audio memory, JavaScript work, main-thread frame time, GPU fill rate and long tasks.
- Split optional content, compress assets appropriately and version cacheable filenames.
- Pool only measured hot objects; uncontrolled retained listeners and Scene references are common leak sources.
- Measure on mid/low target phones with thermal throttling, not only a desktop development machine.
- Keep deployment headers, service-worker behavior, content security policy and asset base URLs under version control or documented infrastructure.

## Primary sources

- [OpenAI browser-game workflow](https://learn.chatgpt.com/use-cases/browser-games)
- [Phaser Scenes](https://docs.phaser.io/phaser/concepts/scenes)
- [Phaser Input](https://docs.phaser.io/phaser/concepts/input)
- [Playwright](https://playwright.dev/docs/intro)
- [web.dev performance course](https://web.dev/learn/performance/)

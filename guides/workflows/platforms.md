# Platform engineering: web, mobile and desktop

Reviewed: 2026-08-29

Choose a minimum and representative device matrix before asset production. Platform work changes input, UI, memory, shaders, packaging and operations.

## Web

Budget initial/total download, memory and startup. Test WebGL/WebGPU support chosen by the engine, browser storage quotas, cache invalidation, offline/slow networks, autoplay/audio unlock, focus/visibility, resize/fullscreen, touch, keyboard capture, gamepad connect/disconnect and tab suspension. Serve compressed immutable hashed assets and keep a compatible loading shell.

## Mobile

Design for sustained—not first-minute—performance. Test thermal throttling, memory pressure/background termination, interruption/resume, orientation/safe areas, touch reach, controller/keyboard, variable refresh, battery, offline behavior, permissions, app lifecycle, store signing and device migration. Scale resolution/effects before simulation correctness.

## Desktop

Test windowed/borderless/fullscreen, multiple monitors, DPI scaling, refresh rates, keyboard layouts/IME, controller hot-plug, audio device changes, suspend, install paths without write access, cloud-save conflicts, GPU/driver tiers and clean uninstall. Store user data only in platform-approved locations.

Sources:

- Android game optimization/thermal APIs: https://developer.android.com/games/optimize/adpf
- MDN Gamepad API: https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API
- Steam Input: https://partner.steamgames.com/doc/features/steam_controller

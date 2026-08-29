# Apple game test matrix

Copy only when an Apple platform is in scope. Every supported row needs a named physical-device owner before release.

| Platform | OS | Device/GPU | Build | Inputs | Quality/FPS target | Status/evidence |
|---|---|---|---|---|---|---|
| macOS | `<version>` | `<model>` | `<build>` | keyboard/mouse/controller | `<tier>` | `<link>` |
| iOS | `<version>` | `<model>` | `<build>` | touch/controller | `<tier>` | `<link>` |
| iPadOS | `<version>` | `<model>` | `<build>` | touch/keyboard/pointer/controller | `<tier>` | `<link>` |
| tvOS | `<version>` | `<model>` | `<build>` | remote/controller | `<tier>` | `<link>` |
| visionOS | `<version>` | `<model>` | `<build>` | gaze/gesture/controller/spatial | `<tier>` | `<link>` |

## Required scenarios

- [ ] First launch, permissions and Game Center unavailable/declined.
- [ ] Suspend/resume, interruption, background/foreground and termination recovery.
- [ ] Controller connect/disconnect/reconnect, multiple players and control fallback.
- [ ] Touch/pointer/keyboard/controller action parity where promised.
- [ ] Rotation, resize, safe areas, external display and display-scale changes where applicable.
- [ ] Offline, slow network, account change and cloud/save conflicts.
- [ ] StoreKit pending, cancelled, duplicate, restored and revoked transactions.
- [ ] Low storage, memory pressure, long session and thermal throttling.
- [ ] Localization, Dynamic Type/platform accessibility settings and reduced motion.
- [ ] Clean install, update from previous release and save migration.
- [ ] TestFlight or final notarized package—not only an Xcode-installed development build.

## Performance evidence

- Scene/workload:
- Duration and deterministic replay/seed:
- Instruments trace:
- Metal GPU trace/HUD evidence:
- CPU/GPU frame percentiles:
- Hitch threshold and count:
- Peak memory/residency:
- Thermal state over time:
- Quality changes and fairness/readability review:

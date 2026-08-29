# Native Apple game production playbook

Reviewed: 2026-08-29

## Choose the rendering layer

| Need | Starting point | Main trade-off |
|---|---|---|
| Native 2D on iPhone, iPad, Mac or Apple TV | SpriteKit | Productive high-level 2D; narrower portability |
| Modern native 3D, spatial or AR | RealityKit | Apple-first ECS and USD workflow |
| Custom renderer or advanced port | Metal | Maximum control and engineering cost |
| Existing cross-platform engine game | Engine's Apple exporter plus native adapters | Faster port, but signing and Apple services still need native validation |

Do not select SceneKit for a new long-lived project. Apple marks it deprecated and recommends RealityKit. Existing SceneKit games may remain operational, but migration risk belongs in the project plan.

## Recommended project shape

```text
Game.xcodeproj or Game.xcworkspace
Packages/
  GameCore/          # deterministic Swift package; no UI/render imports
  GameFeatures/      # bounded gameplay packages
GameApp/
  Platform/          # lifecycle, input, audio, storage and services
  Presentation/      # SpriteKit, RealityKit or Metal adapters
  Resources/         # catalogs, localized content and runtime assets
GameTests/
GameUITests/
Config/              # versioned xcconfig files without secrets
```

- Pin Xcode, Swift tools version, package dependencies, minimum OS and supported device families.
- Keep gameplay rules independent from `SKNode`, RealityKit `Entity`, Metal resources and view lifecycle.
- Use Swift packages/modules to make dependencies and test scope explicit.
- Keep signing identities, private keys and credentials outside source control. Version entitlements and non-secret build settings.
- Use stable identifiers for saved/networked objects; never persist runtime object pointers or display names.

## Codex loop

1. Read project settings, schemes, package manifests, entitlements, `Info.plist` and lifecycle entry points.
2. Confirm the exact destination: simulator or a named physical-device/OS family.
3. Add Swift Testing or XCTest coverage for deterministic rules.
4. Make the smallest module-boundary change and build without signing where appropriate.
5. Run focused tests, then the real game with its actual control mode.
6. Capture screenshots/recordings and inspect state transitions.
7. Profile a release-like build on physical target hardware.
8. Archive and validate the chosen distribution path before the milestone is complete.

Representative command shapes:

```sh
xcodebuild -list -project <Game.xcodeproj>
xcodebuild test -scheme <Scheme> -testPlan <Plan> -destination '<destination>' -resultBundlePath <Results.xcresult>
xcodebuild archive -scheme <Scheme> -configuration Release -archivePath <Game.xcarchive> -destination 'generic/platform=<platform>'
```

Never guess scheme, workspace, destination or signing values. Discover them from the project and record exact verified commands in `ENGINE_BOOTSTRAP.md`.

## Framework boundaries

- **SpriteKit:** Scenes/nodes own 2D presentation and physics adaptation; deterministic rules remain outside `SKScene.update`.
- **RealityKit:** Components hold entity-local data, Systems implement bounded behavior, and SwiftUI hosts platform UI. USD is the normal 3D interchange path.
- **Metal:** make command queues, pipelines, resource lifetime, synchronization and shader compilation explicit; use validation and GPU captures from the start.
- **GameplayKit:** adopt individual tools—random sources, pathfinding, agents or state machines—behind project interfaces; it need not own the whole architecture.
- **Game Controller:** map touch, keyboard/mouse, remote, physical/virtual and spatial controllers into one game-action layer.
- **GameKit:** isolate authentication, achievements, leaderboards, multiplayer and cloud services behind asynchronous adapters with offline/error states.

## Validation ladder

1. Swift package/unit tests for pure rules.
2. Clean command-line build and asset compilation.
3. Integration tests for lifecycle and platform adapters.
4. UI smoke tests for accessible menus and critical flows.
5. Simulator checks for fast coverage—never treated as performance proof.
6. Physical-device play pass covering controls, interruption, thermal and memory behavior.
7. Release configuration with Instruments and Metal evidence.
8. Archive validation and TestFlight or notarized-package smoke test.

## Primary sources

- [Apple game technologies](https://developer.apple.com/documentation/technologyoverviews/games-technologies)
- [SpriteKit](https://developer.apple.com/documentation/spritekit)
- [RealityKit](https://developer.apple.com/documentation/RealityKit)
- [SceneKit deprecation and RealityKit migration](https://developer.apple.com/documentation/RealityKit/bringing-your-scenekit-projects-to-realitykit)
- [GameplayKit](https://developer.apple.com/documentation/GameplayKit)
- [Xcode testing](https://developer.apple.com/documentation/xcode/testing)

# Determinism conformance lab

Reviewed: 2026-08-29

This is the library's first executable reference. It defines a tiny versioned simulation contract that can be ported to Godot, Unity, Unreal, Phaser and other engines, then checked against identical replay inputs and golden hashes.

## Run

Requires Node.js 20 or newer and no third-party packages.

```sh
npm test
npm run run:golden
```

### Godot port

Verified with Godot `4.7.2.stable.official` on 2026-08-29:

```sh
godot --headless --path godot --editor --quit
godot --headless --path godot --script tests/conformance_runner.gd
godot --path godot
```

The headless port reads the same root fixture and matches all checkpoint/final hashes under three frame-chunk schedules. The real scene was also rendered and visually inspected at 960×540 on Apple M4 using Godot's OpenGL Compatibility renderer over Metal; it displayed final hash `d282e067`, `PASS`, and the state-derived actor position.

### Phaser port

Verified with Phaser `4.2.1`, Vite `8.2.2` and Node.js `24.19.0` on 2026-08-29:

```sh
cd phaser
npm ci
npm test
npm run build
npm run preview
```

The port matches all checkpoint/final hashes, tests render-frame chunk independence and rejects non-quantized input. The production browser build was opened in a real browser: one 960×540 canvas reported `pass`, displayed hash `d282e067`, and produced no console warnings or errors. Baseline production output was 1,378.04 kB minified / 359.11 kB gzip JavaScript; future bundle reduction must be measured against required Phaser subsystems rather than hiding the warning.

### Apple SpriteKit / Swift port

Verified with Xcode `26.6`, Apple Swift `6.3.3` and SpriteKit on Apple M4 on 2026-08-29:

```sh
cd apple-spritekit
swift test
swift build -c release
swift run -c release AppleSpriteKitDemo ../fixtures/golden-replay.json /tmp/apple-spritekit-conformance.png
```

The Swift package contains a renderer-independent `ConformanceCore` library, Swift Testing coverage and a macOS SpriteKit evidence renderer. Three tests cover golden checkpoints, two frame-chunk schedules and invalid input. The Release executable produced hash `d282e067` and a visually inspected 960×540 PNG with the expected state-derived actor position and no runtime warnings. This proves the deterministic core and SpriteKit presentation boundary on macOS.

### iPhone and iPad app target

The shared `ConformanceCore` package is also consumed by a real SwiftUI/SpriteKit Xcode app target supporting iPhone and iPad. It was built, installed, launched and visually inspected on iPhone Air and iPad Pro 11-inch (M5) simulators running iOS/iPadOS 26.5 with Xcode 26.6 on 2026-08-29. Both runs loaded the bundled golden replay, displayed final hash `d282e067` and reported `PASS`.

```sh
xcodebuild \
  -project apple-ios/AppleConformanceApp.xcodeproj \
  -scheme AppleConformanceApp \
  -sdk iphonesimulator \
  -destination 'platform=iOS Simulator,name=iPhone Air,OS=26.5' \
  -derivedDataPath apple-ios/.derived \
  CODE_SIGNING_ALLOWED=NO \
  ONLY_ACTIVE_ARCH=YES \
  build
```

Choose an installed simulator name and OS when reproducing locally. `ONLY_ACTIVE_ARCH=YES` avoids compiling an unused simulator architecture when the local Swift package was resolved for the active Apple Silicon destination. CI selects the runner architecture explicitly. This evidence proves package integration, application lifecycle and adaptive simulator rendering; it does not prove signing, TestFlight, touch feel, thermal behavior or physical-device performance.

## Contract

- signed integer input axes quantized to `[-1000, 1000]`;
- positions stored as integer millimetres;
- one simulation step per replay frame at the declared fixed tick rate;
- unsigned 32-bit XorShift PRNG with explicit zero-seed replacement;
- canonical newline-delimited state field order;
- FNV-1a 32-bit UTF-8 state hash;
- JavaScript 32-bit operations interpreted with unsigned `>>> 0` normalization.

The PRNG and hash are intentionally small teaching/reference algorithms, not cryptographic or necessarily suitable for every shipping game. Changing field order, numeric width, text encoding or algorithm requires a new `algorithmVersion` and new fixtures.

## Port acceptance

An engine port conforms when it:

1. reads the fixture without silently changing numeric values;
2. produces every checkpoint and final hash exactly;
3. produces the same final hash under multiple render-frame chunk schedules;
4. rejects input outside the quantized schema;
5. reports the first divergent tick with state fields and PRNG state.

Keep engine ports in named subdirectories of this sample and add their verified toolchain/command evidence to this README. Current verified ports: JavaScript reference, Godot/GDScript, Phaser 4 and Apple SpriteKit/Swift on macOS, iPhone and iPad Simulator.

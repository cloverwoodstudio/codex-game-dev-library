# Apple tool selection and safety

Reviewed: 2026-08-29

## Default routes

| Goal | Start with | Add only when needed |
|---|---|---|
| Native 2D game | Swift, SwiftUI/UIKit/AppKit, SpriteKit, GameplayKit | Game Controller, GameKit, Core Haptics, StoreKit |
| Native 3D or spatial app/game | SwiftUI, RealityKit, Reality Composer Pro, USD | ARKit, Metal, Object Capture |
| Custom renderer or advanced port | Metal/MetalKit, MSL or metal-cpp | MetalFX, shader/texture converters, GPTK |
| Existing engine game | Engine exporter plus Xcode | Native service adapters, Instruments, Metal debugger |
| Ordinary Apple app | SwiftUI plus platform SDKs | UIKit/AppKit bridging, SwiftData/Core Data, CloudKit |
| CI build/test | `xcodebuild`, SwiftPM, `xcresulttool` | `xcbeautify`, Xcode Cloud, GitHub Actions, fastlane |
| Physical-device diagnosis | `devicectl`, Console, Instruments | MetricKit, Organizer crash/hang reports |
| Simulator automation | `simctl`, XCTest/XCUIAutomation | Accessibility Inspector, Network Link Conditioner |
| App Store release | Xcode archive/validation, App Store Connect | Transporter, App Store Connect API, fastlane |
| Direct macOS release | codesign, notarytool, stapler | pkgbuild/productbuild, Sparkle for updates |

## Avoid tool sprawl

- Choose Swift Package Manager by default for Swift dependencies; add CocoaPods or Carthage only for a dependency that requires it.
- Choose one project generator: native checked-in project, XcodeGen or Tuist.
- Choose one primary formatter and one linter policy. Formatting tools can overwrite broad trees; scope paths explicitly.
- Do not place code generators in every incremental build unless inputs/outputs and sandbox behavior are controlled.
- Never pipe `xcodebuild` through a formatter without `set -o pipefail`; otherwise the formatter can hide the build's exit status.
- Do not use deprecated upload or notarization paths when current Xcode provides supported replacements.

## Evidence boundaries

- Simulator: integration, layout, accessibility and many lifecycle flows; not thermal, camera/AR fidelity, controller feel, GPU or physical memory proof.
- Preview/canvas: fast UI iteration; not application lifecycle or runtime proof.
- Debug build: behavior and diagnostics; not representative performance.
- Engine editor: gameplay iteration; not an Apple package, signing or native lifecycle proof.
- Archive validation: packaging/signing metadata; not player-facing functionality.

## Sources

- [Apple game technologies](https://developer.apple.com/documentation/technologyoverviews/games-technologies)
- [Xcode command-line tool reference](https://developer.apple.com/documentation/xcode/xcode-command-line-tool-reference)
- [Apple Game Porting Toolkit](https://developer.apple.com/games/game-porting-toolkit/)
- [Testing with Xcode](https://developer.apple.com/documentation/xcode/testing)
- [Preparing an app for distribution](https://developer.apple.com/documentation/Xcode/preparing-your-app-for-distribution)

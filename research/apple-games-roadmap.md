# Apple games implementation roadmap

Reviewed: 2026-08-29

## Goal

Make Apple platforms the library's deepest end-to-end route: native creation, cross-platform engine export, PC-game porting, platform services, performance, distribution and physical-device evidence across macOS, iOS, iPadOS, tvOS and visionOS.

## Current proof

- Apple-native, platform and build/release playbooks exist.
- SceneKit is treated as deprecated; new 3D work routes to RealityKit or Metal.
- The first executable native sample now proves a Swift deterministic core, Swift Testing, Release build and SpriteKit render on macOS.
- Apple Game Porting Toolkit and its official agent skills are indexed.
- StoreKit, GameKit, Game Controller, Core Haptics, privacy, TestFlight and notarization foundations are documented but not yet implemented as tested samples.

## P0 — playable native slice

1. Convert the Swift package core into a shared package consumed by real macOS and iOS/iPadOS Xcode app targets.
2. Implement one SpriteKit playable loop with touch, keyboard and controller actions, pause/restart and accessibility-labelled surrounding UI.
3. Add Xcode test plans, simulator UI smoke tests and physical iPhone/iPad evidence.
4. Archive an unsigned CI artifact and document the signing/TestFlight handoff without storing secrets.

## P0 — RealityKit slice

1. Build a small RealityKit ECS scene using USD content and SwiftUI presentation.
2. Reuse the same deterministic core and action layer.
3. Test macOS/iOS rendering first, then add a visionOS window/volume route.
4. Capture entity/system lifecycle, loading, memory and device performance evidence.

## P1 — Metal and porting

1. Create a minimal Metal renderer with validation, offline shader compilation and GPU capture instructions.
2. Exercise Apple's Game Porting Toolkit discovery/plan/validate workflow on a permissively licensed sample renderer.
3. Add Metal Shader Converter and metal-cpp reference paths where appropriate.
4. Record feature-family fallbacks, shader/pipeline cache behavior, MetalFX decisions and Instruments evidence.

## P1 — platform services lab

- Game Controller: connect/disconnect, keyboard/mouse, virtual controller, multiple players and haptics.
- GameKit: authentication unavailable/cancelled, achievements, leaderboards, invites and offline queueing.
- StoreKit: local configuration, sandbox pending/cancel/restore/refund/revocation and idempotent entitlement reconciliation.
- Cloud saves: conflict policy, offline changes, migration and account switching.

Every service stays behind an adapter so gameplay remains testable without Apple accounts or network access.

## P1 — release proof

- simulator and physical-device matrix;
- `xcodebuild` tests with retained `.xcresult`;
- Instruments Game Performance and Metal GPU evidence;
- archive validation, symbols and privacy manifests;
- TestFlight internal build checklist;
- Developer ID signing/notarization sample for direct macOS distribution.

## P2 — engine exports to Apple

Create tiny Godot, Unity and Unreal Apple export projects. For each, verify native lifecycle, input/controller mapping, Metal rendering, signing boundaries, Game Center/StoreKit adapter strategy, suspend/resume, thermal behavior and a real packaged build. Engine editor play mode is not Apple-platform proof.

## Evidence policy

Simulator results prove integration and UI flows, not thermal, GPU, controller, camera/AR or real-device lifecycle performance. Any item labeled “physical-device proven” must name device model, OS, build, controls, duration, performance settings and retained capture.

## Primary sources

- [Apple game technologies](https://developer.apple.com/documentation/technologyoverviews/games-technologies)
- [SpriteKit](https://developer.apple.com/documentation/spritekit)
- [RealityKit](https://developer.apple.com/documentation/RealityKit)
- [Metal performance](https://developer.apple.com/documentation/Metal/improving-your-games-graphics-performance-and-settings)
- [Xcode testing](https://developer.apple.com/documentation/xcode/testing)
- [Game Porting Toolkit](https://developer.apple.com/games/game-porting-toolkit/)

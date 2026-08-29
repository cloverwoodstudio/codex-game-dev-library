# Apple games and applications tool catalog

Reviewed: 2026-08-29

This is a discovery catalog, not a mandatory stack. `Built in` means supplied by Xcode, an Apple SDK or macOS; availability still depends on the installed Xcode/SDK. `Optional` tools must be version-pinned and license-checked before adoption. Search this file by task, command or framework name.

## 1. Foundation, IDE and languages

| Tool | Kind | Best use | Codex entry point |
|---|---|---|---|
| Xcode | Apple app | Projects, editors, SDKs, debugging, signing, archives | Inspect schemes/settings; build the real target |
| Xcode Command Line Tools | Apple bundle | Compiler and developer Unix tools | `xcode-select -p`; `xcrun --find <tool>` |
| Swift | Open-source language | Native app/game logic and tooling | `swift --version`, `swift build`, `swift test` |
| Objective-C | Apple language/runtime | Legacy/native framework and engine interop | Clang target build |
| C/C++ and Apple Clang | Compiler | Engines, native libraries, metal-cpp | `xcrun clang --version` |
| Metal Shading Language | Apple language | GPU shaders and compute | Compile through Xcode/`metal` |
| Swift Package Manager | Built in | Swift dependencies, modular code, CLI tools | `swift package`, `Package.swift` |
| LLDB | Built in | Source and process debugging | Xcode debugger or `xcrun lldb` |
| Swift Playgrounds | Apple app | Learning/prototypes on Mac/iPad | Export/move proven code into a tested project |
| DocC | Built in | API documentation and tutorials | `xcrun docc`; SwiftPM documentation plugin |
| Git | Built in/optional | Source control | Preserve user changes; small commits |
| Git LFS | Optional OSS | Large binary assets | `git lfs track`; confirm remote quotas/locks |

Sources: [Xcode](https://developer.apple.com/xcode/), [Swift](https://www.swift.org/), [Swift packages](https://docs.swift.org/package-manager/), [DocC](https://www.swift.org/documentation/docc/), [Git LFS](https://git-lfs.com/).

## 2. Apple UI, rendering and game frameworks

| Framework/tool | Platforms | Best use | Boundary |
|---|---|---|---|
| SwiftUI | All modern Apple platforms | Declarative app/game shell and HUD | Keep simulation outside Views |
| UIKit | iOS/iPadOS/tvOS | Mature native UI and lifecycle integration | Bridge only where SwiftUI is insufficient |
| AppKit | macOS | Windows, menus, input and Mac-specific UI | Mac-only adapter |
| Mac Catalyst | macOS from iPad code | Shared UIKit app route | Validate Mac idioms/input separately |
| SpriteKit | iOS/iPadOS/macOS/tvOS/watchOS | High-level native 2D | Not for native visionOS scenes |
| RealityKit | iOS/iPadOS/macOS/tvOS/visionOS | Native 3D, AR and spatial ECS | Prefer for new Apple-first 3D |
| RealityView | visionOS and supported SDKs | SwiftUI-hosted RealityKit content | Test immersion transitions on device |
| Metal | Apple GPU platforms | Low-level graphics and compute | Requires explicit performance engineering |
| MetalKit | Apple GPU platforms | Metal views, textures and model I/O helpers | Presentation adapter around renderer |
| MetalFX | Supported Apple GPUs | Temporal/spatial upscaling and frame interpolation capabilities | Check feature/device support |
| Metal Performance Shaders / MPSGraph | Apple GPU platforms | Optimized GPU primitives and ML graphs | Measure versus custom kernels |
| GameplayKit | Apple platforms | State machines, agents, pathfinding, graphs, RNG | Adopt bounded parts, not whole architecture |
| Game Controller | Apple platforms | Controllers, keyboard/mouse, virtual controller | Map into semantic actions |
| GameKit / Game Center | Apple platforms | Achievements, leaderboards, matchmaking, multiplayer | Async optional service adapter |
| Core Haptics | Supported iPhone/iPad/Mac hardware | Custom haptic/audio patterns | Capability and accessibility fallback |
| PHASE | Apple platforms | Spatial and dynamic game audio | Profile voice/object counts |
| AVFAudio / AVAudioEngine | Apple platforms | Playback, mixing, recording and effects | Handle interruption and route changes |
| AudioToolbox / Core Audio | Apple platforms | Low-level/pro audio pipelines | Use only when higher-level APIs fail needs |
| Model I/O | Apple platforms | Mesh/material/asset import and processing | Validate resulting runtime representation |
| SceneKit | Apple platforms, deprecated | Maintaining existing projects | Do not choose for new long-lived 3D work |
| Core Animation | Apple platforms | Layer animation and compositing | UI/presentation, not gameplay clock |
| Core Graphics / Image I/O | Apple platforms | 2D drawing and image codecs/metadata | Keep expensive work off frame-critical path |

Sources: [Game technologies](https://developer.apple.com/documentation/technologyoverviews/games-technologies), [SwiftUI](https://developer.apple.com/xcode/swiftui/), [SpriteKit](https://developer.apple.com/documentation/spritekit), [RealityKit](https://developer.apple.com/documentation/realitykit), [Metal](https://developer.apple.com/metal/), [GameplayKit](https://developer.apple.com/documentation/gameplaykit), [PHASE](https://developer.apple.com/documentation/phase).

## 3. AR, spatial computing, ML and sensors

| Framework/tool | Best use | Verification need |
|---|---|---|
| ARKit | World tracking, anchors, scene understanding | Physical supported device |
| RoomPlan | LiDAR room capture | Supported iPhone/iPad and export inspection |
| Object Capture / PhotogrammetrySession | Photos to 3D reconstruction | Scale/material/topology validation |
| Vision | Image/video analysis, tracking, OCR | Dataset and device performance tests |
| VisionKit | Document/data scanning UI | Real capture conditions |
| Core ML | On-device inference | Model accuracy, latency, memory and fallback |
| Create ML | Apple GUI/API model training | Dataset provenance and held-out evaluation |
| Natural Language | Tokenization, tagging and embeddings | Language coverage tests |
| Sound Analysis | Classify live/recorded audio | Noise/device evaluation |
| Core Motion | Accelerometer, gyro and motion fusion | Physical-device calibration |
| Core Location | Location, heading and regions | Permission/offline/background cases |
| Nearby Interaction | UWB spatial proximity | Compatible physical devices |
| Multipeer Connectivity | Nearby peer sessions | Disconnect/rejoin/version tests |
| GroupActivities / SharePlay | Shared synchronized experiences | Multiple accounts/devices |
| Reality Composer Pro | Author RealityKit scenes/materials/timelines | Inspect USD project and runtime load |

Sources: [ARKit](https://developer.apple.com/augmented-reality/arkit/), [Object Capture](https://developer.apple.com/augmented-reality/object-capture/), [Core ML](https://developer.apple.com/machine-learning/core-ml/), [Create ML](https://developer.apple.com/machine-learning/create-ml/), [visionOS](https://developer.apple.com/visionos/).

## 4. Data, networking, services and application capabilities

| Framework/service | Best use | Risk/adapter note |
|---|---|---|
| SwiftData | Native Swift persistence | Define migrations and backup behavior |
| Core Data | Mature object graph/persistence | Model/version migrations |
| SQLite | Embedded relational storage | Use a maintained wrapper or disciplined C API |
| FileManager / Codable | Small explicit file saves/config | Atomic writes and schema versions |
| CloudKit | Apple-account cloud data/saves | Conflict, quota, account and environment states |
| iCloud Documents / key-value store | User documents/small sync state | Conflict and offline handling |
| Network.framework | TCP/UDP/TLS and local networking | Timeouts, path changes, trust policy |
| URLSession | HTTP/WebSocket transfers | Cancellation, retries and auth boundaries |
| Background Assets | Managed large game/app assets | Version, eviction and partial availability |
| On-Demand Resources | Legacy/established hosted resource route | Confirm current platform strategy |
| StoreKit 2 | Purchases, subscriptions, entitlements | Idempotent server-aware reconciliation |
| App Attest / DeviceCheck | App integrity signals | Never treat as sole anti-cheat authority |
| CryptoKit | Hashing, signatures and encryption primitives | Key lifecycle and protocol review |
| Keychain Services | Credentials/secrets on device | Access group and migration policy |
| LocalAuthentication | Face ID/Touch ID/passcode gating | Fallback and cancellation |
| UserNotifications | Local/remote notifications | Permission, payload and deep-link tests |
| ActivityKit | Live Activities | State expiry and update budget |
| WidgetKit | Widgets/controls | Timeline and shared-container design |
| App Intents | Shortcuts, Siri and system actions | Stable intent semantics |
| MapKit | Maps, annotations and overlays | Offline/region/privacy behavior |
| WeatherKit | Weather data | Entitlement, attribution and quota |
| HealthKit | Health/fitness data | Sensitive-data policy and authorization |
| Accessibility APIs | VoiceOver, Switch Control, accessibility actions | Audit and real assistive-technology pass |
| Foundation localization | String catalogs, formatting and locale | Pseudo-localization and layout tests |

Sources: [Apple frameworks](https://developer.apple.com/documentation/), [StoreKit](https://developer.apple.com/storekit/), [CloudKit](https://developer.apple.com/icloud/cloudkit/), [Background Assets](https://developer.apple.com/documentation/backgroundassets), [Accessibility](https://developer.apple.com/accessibility/).

## 5. Xcode automation and bundled command-line tools

| Tool/command | Purpose | Typical safe discovery |
|---|---|---|
| `xcode-select` | Select active developer directory | `xcode-select -p` |
| `xcrun` | Locate/run active SDK tools | `xcrun --find <tool>` |
| `xcodebuild` | List, build, test, archive, export | `xcodebuild -list`; `-showBuildSettings` |
| `simctl` | Simulator devices, apps, media, IO and status | `xcrun simctl list` |
| `devicectl` | Connected-device discovery/control | `xcrun devicectl list devices` |
| `xcresulttool` | Inspect `.xcresult` bundles | `xcrun xcresulttool help` |
| `xctrace` | Record/export Instruments traces | `xcrun xctrace list templates` |
| `xcdebug` | Start Xcode debugging sessions | `xcdebug --help` |
| `swift` / `swiftc` | Swift driver/compiler | `swift --version` |
| `clang` / `clang++` | C-family compilation | `xcrun clang --version` |
| `metal`, `metallib`, `metal-ar` | Compile/archive Metal shaders | Locate via `xcrun --find` |
| `metal-dsymutil` | Metal shader debug symbols | Locate via `xcrun --find` |
| `actool` | Compile asset catalogs | Normally invoked by build system |
| `ibtool` | Interface Builder resources | Normally invoked by build system |
| `momc` / `mapc` | Core Data model/mapping compilation | Normally invoked by build system |
| `coremlcompiler` | Compile Core ML models | Normally invoked by build system |
| `intentbuilderc` | Compile intent definitions | Normally invoked by build system |
| `stringstool` / string catalog tooling | Localization extraction/validation | Use current Xcode help |
| `agvtool` | Apple Generic Versioning | `man agvtool` |
| `plutil` | Validate/edit property lists | Prefer `-lint`/read operations first |
| `assetutil` | Inspect compiled asset catalogs | `xcrun assetutil --help` |
| `nm`, `otool`, `size`, `strings` | Mach-O symbol/binary inspection | Read-only binary diagnosis |
| `dwarfdump`, `dsymutil`, `atos` | Symbols and crash address resolution | Preserve exact binary/dSYM UUIDs |
| `codesign` | Inspect/sign code | `codesign -dvv`; signing mutates artifacts |
| `security` | Keychain/certificate operations | Avoid printing secrets or broad keychain changes |
| `notarytool` | Submit/check notarization | Requires explicit release authorization |
| `stapler` | Attach/check notarization ticket | Validate final artifact |
| `spctl` | Gatekeeper assessment | `spctl --assess` on final macOS artifact |
| `pkgbuild` / `productbuild` | macOS installer packages | Build in staging path |
| `hdiutil` | Disk images | Avoid destructive image/disk operations |
| `xed` | Open Xcode files/workspaces | UI convenience |
| `opendiff` / FileMerge | Visual diff/merge | Never auto-resolve user work |
| `instruments` UI | CPU/GPU/memory/energy diagnostics | Release-like physical-device capture |
| `Accessibility Inspector` | UI accessibility inspection | Combine with VoiceOver/manual pass |
| `Create ML`, `Reality Composer Pro`, `Simulator` | Bundled companion apps | Launch only when task requires UI |

Primary reference: [Xcode command-line tool reference](https://developer.apple.com/documentation/xcode/xcode-command-line-tool-reference). Individual tools expose current help through `man` or `xcrun <tool> --help`; prefer installed help because options track the active Xcode version.

## 6. Debugging, quality and performance

| Tool | Best use | Evidence |
|---|---|---|
| XCTest | Unit, integration, UI and performance tests | `.xcresult` |
| Swift Testing | Modern Swift unit/integration tests | Test output/`.xcresult` through Xcode |
| XCUIAutomation | End-to-end UI automation | Screenshots, attachments and result bundle |
| Xcode test plans | Matrix/configuration of tests | Versioned `.xctestplan` |
| Xcode previews | Fast SwiftUI iteration | Never sole runtime evidence |
| Instruments Time Profiler | CPU hotspots | Trace plus scenario/build/device |
| Game Performance template | Correlated game performance | Physical-device trace |
| Metal System Trace | CPU/GPU submission timeline | Trace and frame markers |
| Metal debugger/capture | GPU commands, shaders, resources | `.gputrace`/capture metadata |
| Metal HUD | Live frame/GPU counters | Screenshot plus configuration |
| Allocations / Leaks | Memory allocation/leaks | Trace and reproduction |
| Memory Graph Debugger | Retain cycles/object graph | Debug evidence and code fix |
| Energy Log | Energy use | Device/build/scenario |
| Network instrument | Requests and timing | Redacted trace |
| Hangs/launch/time instruments | Responsiveness and launch | Trace and thresholds |
| Thread Sanitizer | Data races in supported targets | Focused test run |
| Address Sanitizer | Memory errors | Focused test run |
| Undefined Behavior Sanitizer | C-family UB | Focused test run |
| Main Thread Checker | UI API misuse | Runtime diagnostics |
| GPU validation / API validation | Metal misuse | Debug run; remeasure without validation |
| MetricKit | Field metrics and diagnostics | Version/device aggregation |
| Organizer | Crashes, energy and distribution reports | Symbolicated reports |
| Console / unified logging | Runtime/device logs | Redact personal/secrets data |
| `os.Logger` / signposts | Structured logs and performance intervals | Stable categories and privacy annotations |
| Network Link Conditioner | Adverse network simulation | Record profile; test recovery |
| Charles / Proxyman | Optional HTTP proxy/debug | Test trust safely; never ship debug certs |
| Accessibility Inspector | Labels, traits, contrast and actions | Manual assistive-tech verification |

Sources: [Xcode testing](https://developer.apple.com/documentation/xcode/testing), [Metal developer workflows](https://developer.apple.com/documentation/Xcode/Metal-developer-workflows), [Instruments](https://developer.apple.com/tutorials/instruments), [MetricKit](https://developer.apple.com/documentation/metrickit).

## 7. Graphics porting and low-level asset tools

| Tool | Status | Best use |
|---|---|---|
| Game Porting Toolkit 4 | Apple download | Evaluate/port Windows DirectX games; includes agent workflows |
| Apple GPTK agent skills | Apple OSS repo | Codex-guided discovery, planning, Metal work, input and optimization |
| Metal Shader Converter | Apple download | DXIL to Metal libraries |
| Metal Texture Converter | Apple tool | Convert/compress textures for Metal formats |
| Metal compiler/offline binary generator | Apple tools | Build GPU-specific shader assets |
| Metal Developer Tools for Windows | Apple download | Compile Apple GPU assets in Windows pipelines |
| Mac Remote Developer Tools for Windows | Apple download | CMake/Visual Studio remote Mac build/debug |
| metal-cpp | Apple headers | Near-zero-overhead C++ Metal interface |
| MetalFX | Apple framework | Upscaling/frame technology where supported |
| Steam Asset Converter | Apple tool | Convert supported Steam metadata/assets for Apple workflows |
| RenderDoc | Optional OSS | Cross-platform graphics capture before Metal boundary; Metal support is not its primary route |
| Xcode Metal debugger | Built in | Authoritative Metal capture/debug/profile path |

Sources: [Game Porting Toolkit](https://developer.apple.com/games/game-porting-toolkit/), [Apple GPTK repository](https://github.com/apple/game-porting-toolkit), [Metal resources](https://developer.apple.com/metal/resources/), [Remote Mac builds](https://developer.apple.com/documentation/technologyoverviews/building-your-macos-game-remotely-from-your-pc).

## 8. 2D, 3D, USD, animation and visual content

| Tool | License/model | Best use | Apple pipeline note |
|---|---|---|---|
| Reality Composer Pro | Apple/Xcode | RealityKit scenes, materials, behaviors | Native `.realitycomposerpro`/USD route |
| Reality Converter | Apple app | Preview/convert common 3D assets to USDZ | Validate current availability and output |
| USD tools (`usdchecker`, `usdcat`, `usdview`) | Pixar OSS | Validate/inspect/convert USD | Pin USD version used by pipeline |
| Blender | GPL | Modeling, sculpting, UV, animation, baking | Export USD/glTF/FBX as validated interchange |
| Autodesk Maya | Commercial | Character/animation/VFX pipelines | USD/FBX export validation |
| Autodesk 3ds Max | Commercial/Windows | Modeling and established pipelines | Convert through validated interchange |
| SideFX Houdini | Commercial/Indie | Procedural worlds, VFX and USD/Solaris | Bake runtime-ready assets |
| Adobe Substance 3D Painter | Commercial | PBR texturing and baking | Export Metal/engine-compatible maps |
| Substance 3D Designer | Commercial | Procedural materials | Freeze seeds/versions for reproducibility |
| ZBrush | Commercial | High-detail sculpting | Retopo and bake before runtime |
| Marvelous Designer | Commercial | Clothing simulation/authoring | Retopo, bake and validate deformation |
| Cascadeur | Commercial/free tier | Assisted character animation | Validate skeleton/root motion |
| Mixamo | Service/license terms | Auto-rigging/motion source | Check exact asset/use terms |
| FreeCAD | LGPL/GPL components | Parametric CAD reconstruction | Tessellate/retopo for game use |
| OpenSCAD | GPL | Scripted parametric CAD | Deterministic dimension-driven models |
| ViewForge (this repository) | Repository code | Calibrated front/side/top silhouettes to visual hull, GLB and USDC | Run `tools/viewforge/viewforge.sh`; inspect reprojection report |
| MeshLab | GPL | Mesh inspection/repair/decimation | Preserve normals/UV/material expectations |
| MaterialX | ASWF OSS | Material interchange | Confirm renderer feature mapping |
| glTF Validator | Khronos OSS/service | Validate glTF interchange | Run before conversion/import |
| KTX-Software / Basis Universal | Khronos/OSS | GPU texture containers/compression | Check Apple GPU format choices |
| TexturePacker | Commercial | Sprite sheets and atlases | Record trim/pivot metadata |
| Aseprite | Commercial/source available | Pixel art and animation | Export deterministic sheets/data |
| Affinity Photo/Designer | Commercial | Raster/vector UI and art | Export source + optimized assets |
| Adobe Photoshop/Illustrator | Commercial | Raster/vector production | Preserve editable masters |
| Krita | GPL | Painting and concept art | Export color-managed runtime assets |
| GIMP / Inkscape | GPL | Raster/vector editing | Validate SVG/raster output |
| Figma | Service/commercial tiers | UI design/prototypes/tokens | Translate semantics/accessibility, not pixels only |
| Sketch | Commercial Mac app | Apple UI design | Maintain design-to-code token contract |
| SF Symbols | Apple app/license | Apple system-symbol design/reference | Follow platform/license rules |
| Icon Composer | Apple tool | Layered app icons for current platforms | Validate with current Xcode/App Store rules |

Sources: [Reality Composer Pro](https://developer.apple.com/augmented-reality/tools/), [OpenUSD](https://openusd.org/release/toolset.html), [Blender](https://docs.blender.org/manual/en/latest/), [Khronos glTF](https://www.khronos.org/gltf/), [SF Symbols](https://developer.apple.com/sf-symbols/), [Apple design resources](https://developer.apple.com/design/resources/).

## 9. Audio, music, video and capture

| Tool | Model | Best use |
|---|---|---|
| Logic Pro | Apple commercial app | Music, sound design, mixing and spatial audio |
| GarageBand | Apple app | Fast music/audio prototypes |
| MainStage | Apple commercial app | Live instruments/performance rigs |
| Final Cut Pro | Apple commercial app | Trailers, App Store video and capture editing |
| Compressor | Apple commercial app | Batch video/audio encoding |
| Motion | Apple commercial app | Motion graphics/titles |
| QuickTime Player | Built in | Device/window/screen recording and inspection |
| Screenshot (`screencapture`) | Built in | Automated Mac screenshots |
| AVFoundation export tools | Apple framework | In-app/offline media pipelines |
| FMOD Studio | Commercial/free thresholds | Interactive game audio middleware |
| Audiokinetic Wwise | Commercial/free thresholds | Large interactive audio pipelines |
| Reaper | Commercial | DAW, batch rendering and scripting |
| Audacity | GPL | Waveform editing and cleanup |
| ocenaudio | Freeware | Lightweight audio editing |
| ffmpeg / ffprobe | LGPL/GPL configurations | Automated transcode and media inspection |
| sox | GPL | Scriptable audio conversion/analysis |

Sources: [Logic Pro](https://www.apple.com/logic-pro/), [Final Cut Pro](https://www.apple.com/final-cut-pro/), [AVFoundation](https://developer.apple.com/av-foundation/), [FMOD](https://www.fmod.com/docs/), [Wwise](https://www.audiokinetic.com/en/public-library/), [FFmpeg](https://ffmpeg.org/documentation.html).

## 10. Engines and cross-platform application stacks

| Engine/stack | Apple targets | Use when | Caveat |
|---|---|---|---|
| Unity | iOS/iPadOS/macOS/tvOS/visionOS routes vary by version | C# cross-platform 2D/3D/XR | Verify exact editor/LTS and Apple module support |
| Unreal Engine | iOS/iPadOS/macOS/tvOS/visionOS routes vary | High-end 3D/C++/Blueprint | Metal, packaging and device cost |
| Godot | iOS/macOS; other Apple routes vary | OSS 2D/3D and small teams | Verify export templates and platform maturity |
| Defold | iOS/macOS | Lightweight Lua engine | Native extension/service coverage |
| Cocos2d-x | iOS/macOS | Existing C++ 2D codebases | Maintenance/community status check |
| Solar2D | iOS/macOS | Lua mobile 2D | Plugin/platform support check |
| MonoGame | iOS/macOS through .NET ecosystem | C# code-first games | Native AOT/package integration |
| SDL | Apple platforms | Portable C/C++ window/input/audio layer | Native services remain custom |
| raylib | macOS and custom mobile integration | Learning/tools/small C games | iOS packaging requires project work |
| bgfx | Apple platforms | Cross-platform renderer abstraction | Own app/platform layer |
| Flutter | iOS/macOS | Cross-platform applications and 2D UI | Not a high-end native game renderer |
| Flame | Flutter-supported targets | Casual 2D games in Dart | Flutter lifecycle/performance constraints |
| React Native | iOS/macOS community routes | Cross-platform application UI | Native bridge and engine embedding costs |
| Kotlin Multiplatform | Shared logic with Apple UI | Shared business/application core | Keep Apple presentation native where useful |
| .NET MAUI | iOS/macOS Catalyst | Cross-platform business apps | Toolchain/platform version matrix |
| Qt | iOS/macOS | C++ cross-platform apps/tools | Licensing and native UX trade-offs |
| Tauri | macOS desktop | Small web-tech desktop apps | Not an iOS game engine |
| Electron | macOS desktop | Web-tech desktop tools/apps | Package size, memory and native integration |

Sources: [Unity platform development](https://docs.unity3d.com/Manual/PlatformSpecific.html), [Unreal platforms](https://dev.epicgames.com/documentation/en-us/unreal-engine/sharing-and-releasing-projects-for-unreal-engine), [Godot exporting for iOS](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_ios.html), [Defold iOS](https://defold.com/manuals/ios/), [Flutter supported platforms](https://docs.flutter.dev/reference/supported-platforms).

## 11. Project generation, dependencies, code quality and generation

| Tool | Model/license | Role | Safe adoption |
|---|---|---|---|
| Tuist | OSS plus optional service | Project generation, caching and platform workflows | Choose instead of, not beside, another generator |
| XcodeGen | MIT | YAML/JSON to Xcode project | Pin version; review generated project diff |
| Bazel + rules_apple/rules_swift | OSS | Large hermetic builds | High setup cost; verify Xcode integration |
| CMake | BSD | Cross-platform C/C++ generation/build | Use Xcode generator or Ninja intentionally |
| Ninja | Apache 2 | Fast low-level builds | Usually generated, not hand-authored |
| Meson | Apache 2 | Cross-platform native builds | Apple package integration remains explicit |
| CocoaPods | MIT | Legacy/ecosystem dependency manager | Prefer only when dependencies require it |
| Carthage | MIT | Binary/source Apple dependencies | Confirm XCFramework support |
| Mint | MIT | Pin/install Swift CLI packages | Commit `Mintfile` and versions |
| mise | MIT | Multi-tool version manager | Commit config/lock; audit plugins/backends |
| Homebrew | BSD | macOS package manager | Pin through Brewfile/CI image where needed |
| SwiftLint | MIT | Swift style/static rules | Start narrow; pin rules/version |
| SwiftFormat | MIT | Swift formatting | Use `--lint` first; scope exact project path |
| SwiftGen | MIT | Typed asset/string/storyboard access | Declare inputs/outputs and generated path |
| Sourcery | MIT | Swift metaprogramming/code generation | Commit templates and deterministic output policy |
| Periphery | MIT | Detect unused Swift code | Treat dynamic/reflection false positives carefully |
| Swift Package Index | Service/OSS | Package discovery/compatibility | Verify package repo, license and maintenance |
| Semgrep | LGPL CLI/rules vary | Static analysis and custom rules | Pin rulesets; inspect findings |
| CodeQL | GitHub terms/OSS components | Security/code analysis | Language/build support varies |
| SonarQube/SonarCloud | Commercial/community editions | Quality/security analysis | Configure exclusions and quality gates |

Sources: [Tuist](https://github.com/tuist/tuist), [XcodeGen](https://github.com/yonaskolb/XcodeGen), [SwiftLint](https://github.com/realm/SwiftLint), [SwiftFormat](https://github.com/nicklockwood/SwiftFormat), [SwiftGen](https://github.com/SwiftGen/SwiftGen), [Sourcery](https://github.com/krzysztofzablocki/Sourcery), [Periphery](https://github.com/peripheryapp/periphery).

## 12. CI, release, store and operations

| Tool/service | Role | Mutation boundary |
|---|---|---|
| Xcode Cloud | Apple CI/CD | Builds/tests/uploads depend on configured workflow |
| GitHub Actions macOS runners | Repository CI | Pin actions and control secrets/artifacts |
| Bitrise | Mobile CI/CD | External service credentials/build minutes |
| Codemagic | Mobile CI/CD | External service credentials/build minutes |
| CircleCI macOS | CI/CD | External service and runner configuration |
| Buildkite Mac agents | Self/hosted CI | Host security and maintenance |
| fastlane | MIT automation suite | Signing/store mutations require explicit lane scope |
| `xcbeautify` | MIT CLI | Readable xcodebuild logs/JUnit; use `pipefail` |
| `xcpretty` | MIT/Ruby | Legacy/common xcodebuild formatting | Prefer maintained choice for new setup |
| Danger Swift | MIT | Pull-request policy automation | Review bot permissions/comments |
| App Store Connect | Apple service | Apps, builds, metadata, TestFlight and release |
| App Store Connect API | Apple API | Automate builds/users/metadata where supported |
| Transporter | Apple app/CLI | Upload app metadata/packages | External upload mutation |
| TestFlight | Apple service | Internal/external beta distribution | Tester/build state mutation |
| `notarytool` / `stapler` | Apple CLI | Direct macOS notarization | Sends artifact to Apple |
| Sentry | SaaS/self-host | Crash/performance reporting | Privacy, symbols and sampling policy |
| Firebase Crashlytics | SaaS | Crash reporting | SDK/privacy and symbol upload |
| Bugsnag | SaaS | Stability monitoring | SDK/privacy and symbol upload |
| Datadog | SaaS | RUM/logs/traces | Cost/privacy/sampling |
| OpenTelemetry | OSS standard | Vendor-neutral telemetry | Mobile SDK maturity and data policy |
| Sparkle | MIT | Direct-distribution macOS updates | Signing/feed/update security |

Sources: [Xcode Cloud](https://developer.apple.com/xcode-cloud/), [App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi), [Transporter](https://apps.apple.com/app/transporter/id1450874784), [fastlane](https://github.com/fastlane/fastlane), [xcbeautify](https://github.com/cpisciotta/xcbeautify), [Sparkle](https://github.com/sparkle-project/Sparkle).

## 13. Product design, accessibility, analytics and collaboration

| Tool | Use | Note |
|---|---|---|
| Apple Human Interface Guidelines | Platform design decisions | Treat platform guidance as source, not visual template |
| Apple Design Resources | Official UI kits/templates | Check current license/use terms |
| Accessibility Inspector | Technical accessibility audit | Pair with real VoiceOver/Switch Control |
| VoiceOver, Switch Control, Voice Control | Assistive-technology tests | Exercise core flows on target hardware |
| App Analytics | App Store acquisition/engagement | Understand aggregation/privacy limits |
| App Store Connect Sales and Trends | Commerce reporting | External account access |
| MetricKit | Field performance | Build/version/device correlation |
| Instruments | Local performance | Controlled reproducible scenario |
| Figma / FigJam | UI systems, flows and collaboration | Preserve tokens, states and accessibility |
| Sketch | Native Mac design workflow | Version/source management |
| Jira / Linear / GitHub Issues | Work tracking | Do not mutate external state without scope |
| TestFlight feedback | Beta evidence | Link reports to build and disposition |

Sources: [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/), [Accessibility](https://developer.apple.com/accessibility/), [App Analytics](https://developer.apple.com/app-store-connect/analytics/).

## Adoption record

When a project adopts an optional tool, record:

```text
Tool and exact version:
Purpose and owner:
Install/pin mechanism:
License and commercial limits checked:
Configuration committed:
CI and local parity:
Inputs, outputs and cache path:
Secrets/capabilities required:
Uninstall/rollback path:
Last verified date and source URL:
```

The catalog intentionally includes alternatives. Inclusion is not endorsement, proof of current compatibility or permission to install/use a paid service.

---
name: apple-platform-development
description: Select, inspect and use Apple-native or cross-platform tools for games and applications targeting iOS, iPadOS, macOS, tvOS or visionOS. Use for Apple project setup, builds, simulators/devices, graphics, assets, testing, profiling, signing, distribution, porting and toolchain audits.
---

# Apple platform development

Use this skill as a router, not as permission to install software, alter signing, upload builds or mutate App Store state.

## Route the task

1. Read the relevant project files and `AGENTS.md` before choosing tools.
2. Read [references/tool-catalog.md](references/tool-catalog.md), but only the sections relevant to the task.
3. For selection trade-offs and safe defaults, read [references/selection-and-safety.md](references/selection-and-safety.md).
4. Run `scripts/audit-apple-tools.sh` when installed-tool or SDK discovery would change the plan. It is read-only and writes nothing by default.
5. Prefer tools already pinned by the repository. Do not introduce a second project generator, dependency manager, formatter or release orchestrator without a concrete need.

## Operating rules

- Discover Xcode paths, schemes, destinations, SDKs and capabilities; never guess them.
- Distinguish simulator evidence from physical-device evidence.
- Keep gameplay/application rules outside rendering and platform-service adapters where practical.
- Use official Apple tools and primary documentation first. Treat third-party tools as optional and verify their current release, license and platform support before adoption.
- Pin external tool and package versions in the consuming project. Never execute remote install scripts without explicit user authorization.
- Keep certificates, private keys, App Store Connect API keys, provisioning profiles and passwords out of the repository and command output.
- Treat signing, notarization, TestFlight/App Store upload, CloudKit production changes and destructive simulator/device operations as external mutations requiring the user's scope or approval.
- Preserve `.xcresult`, crash logs, screenshots, traces and device/OS/build metadata when they are acceptance evidence.

## Minimum verification

For code changes, build the actual target and run focused tests. For visual or interaction changes, launch on a representative destination and inspect it. For performance claims, use a Release-like build on physical target hardware and retain Instruments or Metal evidence. For releases, validate the archive and test the exported artifact; a successful compile is not release proof.

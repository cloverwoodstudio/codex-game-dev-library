# Apple build, testing and release workflow

Reviewed: 2026-08-29

## Version-control the build contract

Commit shared schemes, test plans, package resolution policy, non-secret `.xcconfig` files, entitlements, privacy manifests, asset catalogs and export configuration where safe. Record the Xcode version and SDK used for every release. Never commit certificates, private keys, App Store Connect API private keys or provisioning credentials.

## CI ladder

1. Resolve packages and validate the project graph.
2. Build pure Swift packages and run fast unit tests.
3. Build every supported target in the required configuration.
4. Run integration/UI tests on a controlled simulator destination.
5. Retain `.xcresult`, logs, coverage and failure screenshots.
6. Run scheduled physical-device smoke and performance tests.
7. Archive Release configuration with controlled signing.
8. Validate/export the archive and run a clean-install smoke test.

Use test plans to separate fast PR checks, integration/device checks and pre-release suites. Swift Testing is suitable for unit/integration logic; XCTest/XCUIAutomation remains necessary for UI automation and supported performance workflows.

## Signing and capabilities

- Keep bundle IDs, teams, capabilities and entitlements intentional per target.
- Review entitlement diffs as security/distribution changes.
- Ensure privacy usage descriptions match actual runtime access.
- Prefer CI-managed ephemeral keychains or the chosen secure signing service.
- Test a clean machine/account path before release; a developer workstation can hide provisioning assumptions.

## Beta and release routes

### App Store platforms

Archive, validate, upload to App Store Connect, complete privacy/export/compliance metadata, distribute through TestFlight, triage feedback and crashes, then submit the proven build. TestFlight is a distribution stage, not a substitute for local/device validation.

### Direct macOS distribution

Use Developer ID signing, hardened runtime where required, notarize with current Xcode or `notarytool`, staple the ticket where applicable, and test the final package on a clean Mac. Notarization is a malware/signing check, not App Review and not functional QA.

## Release evidence

- immutable commit and marketing/build versions;
- Xcode/SDK/toolchain version;
- archive/export logs and validation result;
- test results and device matrix;
- symbols needed for crash symbolication;
- licenses, privacy declarations and export-compliance decision;
- TestFlight feedback disposition;
- performance captures for representative devices;
- rollback/hotfix owner and phased-release decision.

## Primary sources

- [Running tests and interpreting results](https://developer.apple.com/documentation/xcode/running-tests-and-interpreting-results)
- [Organizing tests with test plans](https://developer.apple.com/documentation/xcode/organizing-tests-to-improve-feedback)
- [Preparing an app for distribution](https://developer.apple.com/documentation/Xcode/preparing-your-app-for-distribution)
- [Beta testing and releases](https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases)
- [TestFlight overview](https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview)
- [Notarizing macOS software](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution)

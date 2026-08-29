#!/usr/bin/env bash
set -euo pipefail

printf 'Apple host\n'
sw_vers 2>/dev/null || true
uname -m

printf '\nActive developer directory\n'
xcode-select -p 2>/dev/null || printf 'not selected\n'
xcodebuild -version 2>/dev/null || printf 'xcodebuild unavailable\n'

printf '\nSDKs\n'
xcodebuild -showsdks 2>/dev/null || true

printf '\nSwift toolchain\n'
swift --version 2>/dev/null || printf 'swift unavailable\n'

printf '\nApple command-line tools\n'
apple_commands=(xcodebuild xcrun swift swiftc clang metal codesign security notarytool stapler pkgbuild productbuild docc agvtool xed opendiff)
for command_name in "${apple_commands[@]}"; do
  if command -v "$command_name" >/dev/null 2>&1; then
    printf 'yes  %-20s %s\n' "$command_name" "$(command -v "$command_name")"
  elif xcrun --find "$command_name" >/dev/null 2>&1; then
    printf 'yes  %-20s %s\n' "$command_name" "$(xcrun --find "$command_name")"
  else
    printf 'no   %s\n' "$command_name"
  fi
done

printf '\nOptional CLI tools\n'
optional_commands=(brew mise mint tuist xcodegen swiftlint swiftformat swiftgen sourcery periphery xcbeautify fastlane pod carthage git-lfs blender godot unity Unity UnrealEditor cmake ninja)
for command_name in "${optional_commands[@]}"; do
  if command -v "$command_name" >/dev/null 2>&1; then
    printf 'yes  %-20s %s\n' "$command_name" "$(command -v "$command_name")"
  else
    printf 'no   %s\n' "$command_name"
  fi
done

printf '\nSimulators (available)\n'
xcrun simctl list devices available 2>/dev/null || true

printf '\nConnected devices\n'
xcrun devicectl list devices 2>/dev/null || true

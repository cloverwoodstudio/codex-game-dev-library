#!/usr/bin/env bash
# Run only inside cloverwood-local-run.sh; intentionally break a disposable copy.
set -euo pipefail
: "${CLOVERWOOD_RUN_ROOT:?run via approved Cloverwood local-run wrapper}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="$CLOVERWOOD_RUN_ROOT/swift-negative-fixture"
mkdir -p "$DEST"
cp "$ROOT/Package.swift" "$DEST/Package.swift"
cp -R "$ROOT/Sources" "$DEST/Sources"
cp -R "$ROOT/Tests" "$DEST/Tests"
python3 - "$DEST/Sources/CloverwoodConcurrencyPilot/RevisionedInbox.swift" <<'PY'
from pathlib import Path
import sys
path = Path(sys.argv[1])
text = path.read_text()
original = "guard token == generation, !Task.isCancelled else { return false }"
mutant = "guard !Task.isCancelled else { return false }"
assert text.count(original) == 1, "fixture changed: stop rather than guessing"
path.write_text(text.replace(original, mutant))
PY
set +e
(cd "$DEST" && swift test --scratch-path "$CLOVERWOOD_RUN_ROOT/swiftpm-negative" --parallel) > "$CLOVERWOOD_RUN_ROOT/results/negative-swift-test.log" 2>&1
status=$?
set -e
if [ "$status" -eq 0 ]; then
  echo "NEGATIVE_REGRESSION_FAIL: broken stale-response guard unexpectedly passed" >&2
  exit 1
fi
if ! grep -Fq 'latest response wins even if older result arrives later' "$CLOVERWOOD_RUN_ROOT/results/negative-swift-test.log"; then
  echo "NEGATIVE_REGRESSION_FAIL: test invocation not verified, status=$status" >&2
  exit 1
fi
if ! grep -Eq 'failed|issue|Expectation' "$CLOVERWOOD_RUN_ROOT/results/negative-swift-test.log"; then
  echo "NEGATIVE_REGRESSION_FAIL: no expected assertion diagnostics (may be a build error)" >&2
  exit 1
fi
if grep -Eq 'error:|compile command failed|fatal error' "$CLOVERWOOD_RUN_ROOT/results/negative-swift-test.log"; then
  echo "NEGATIVE_REGRESSION_FAIL: compiler failure is not behavioral red test" >&2
  exit 1
fi
echo "EXPECTED_RED_TEST_PASS mutation=drop_stale_generation_guard rejected_by=SwiftTesting"
echo "EXPECTED_RED_TEST_EXIT=$status (nonzero expected; test harness PASS)"

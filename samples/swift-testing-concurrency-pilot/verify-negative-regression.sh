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
# Run exactly the stale-completion test. The output parser refuses a different
# failed test, a zero-test run, a compile failure, or a different expectation.
set +e
(cd "$DEST" && swift test --scratch-path "$CLOVERWOOD_RUN_ROOT/swiftpm-negative" \
  --filter 'RevisionedInboxTests.staleResponseIsRejected') \
  > "$CLOVERWOOD_RUN_ROOT/results/negative-swift-test.log" 2>&1
status=$?
set -e
python3 "$ROOT/verify_expected_red.py" \
  --log "$CLOVERWOOD_RUN_ROOT/results/negative-swift-test.log" \
  --exit-code "$status"

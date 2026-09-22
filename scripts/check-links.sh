#!/usr/bin/env bash
set -euo pipefail
# Resolve the checkout explicitly; never infer a recursive search from stdin.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 -B "$SCRIPT_DIR/check_links.py" "$@"

#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  printf 'Usage: %s path/to/viewforge.json\n' "$0" >&2
  exit 64
fi

if ! command -v blender >/dev/null 2>&1; then
  printf 'ViewForge requires Blender on PATH.\n' >&2
  exit 69
fi

script_directory="$(cd "$(dirname "$0")" && pwd)"
manifest_path="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
report_path="$(python3 - "$manifest_path" <<'PY'
import json
import sys
from pathlib import Path

manifest_path = Path(sys.argv[1])
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
print((manifest_path.parent / manifest["output_directory"] / "validation.json").resolve())
PY
)"
rm -f "$report_path"
blender --background --python "$script_directory/viewforge.py" -- "$manifest_path"

if [[ ! -s "$report_path" ]]; then
  printf 'ViewForge did not produce a validation report; inspect Blender output.\n' >&2
  exit 1
fi

python3 - "$report_path" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as report_file:
    report = json.load(report_file)
if not report.get("quality_gate", {}).get("passed", False):
    failed = ", ".join(report.get("quality_gate", {}).get("failed_views", [])) or "unknown"
    raise SystemExit(f"ViewForge quality gate failed for: {failed}; inspect {sys.argv[1]} and overlays/")
PY

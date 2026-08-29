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
blender --background --python "$script_directory/viewforge.py" -- "$manifest_path"

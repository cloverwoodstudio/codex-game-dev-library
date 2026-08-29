#!/usr/bin/env bash
set -euo pipefail

tool_directory="$(cd "$(dirname "$0")/.." && pwd)"
output_directory="$tool_directory/examples/crate/output"
bad_output_directory="$tool_directory/examples/inconsistent/output"
find "$output_directory" -depth -delete 2>/dev/null || true
find "$bad_output_directory" -depth -delete 2>/dev/null || true

"$tool_directory/viewforge.sh" "$tool_directory/examples/crate/viewforge.json"

test -s "$output_directory/calibration-crate.blend"
test -s "$output_directory/calibration-crate.glb"
test -s "$output_directory/calibration-crate.usdc"
test -s "$output_directory/validation.json"
test -s "$output_directory/front.png"
test -s "$output_directory/side.png"
test -s "$output_directory/top.png"
test -s "$output_directory/masks/front.pgm"
test -s "$output_directory/masks/side.pgm"
test -s "$output_directory/masks/top.pgm"
test -s "$output_directory/overlays/front.png"
test -s "$output_directory/overlays/side.png"
test -s "$output_directory/overlays/top.png"

blender --background --factory-startup --python-expr "import bpy; bpy.ops.import_scene.gltf(filepath='$output_directory/calibration-crate.glb'); model=[item for item in bpy.context.scene.objects if item.type == 'MESH' and item.name.startswith('calibration-crate')][0]; dimensions=tuple(round(value, 4) for value in model.dimensions); assert all(abs(actual - expected) < 0.01 for actual, expected in zip(dimensions, (2.0, 1.0, 1.5))), dimensions"

python3 - "$output_directory/validation.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as report_file:
    report = json.load(report_file)

assert report["occupied_voxels"] > 0
assert report["boundary_faces"] > 0
assert report["quality_gate"]["passed"] is True
assert report["dimension_ledger_ids"] == {"width": "DIM-W", "height": "DIM-H", "depth": "DIM-D"}
assert all(result["mapping_strategy"] == "calibrated_anchors" for result in report["inputs"].values())
assert all(result["calibration"] for result in report["inputs"].values())
assert all(result["mode"] == "background" for result in report["inputs"].values())
assert len({result["path"] for result in report["inputs"].values()}) == 1
for view_name, result in report["views"].items():
    assert result["iou"] >= 0.95, (view_name, result)
print("ViewForge smoke test passed")
PY

if "$tool_directory/viewforge.sh" "$tool_directory/examples/inconsistent/viewforge.json"; then
    echo "Expected inconsistent views to fail the quality gate" >&2
    exit 1
fi

test -s "$bad_output_directory/validation.json"
test -s "$bad_output_directory/overlays/front.png"

python3 - "$bad_output_directory/validation.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as report_file:
    report = json.load(report_file)

assert report["quality_gate"]["passed"] is False
assert report["quality_gate"]["failed_views"]
assert any(result["missing_pixels"] > 0 for result in report["views"].values())
print("ViewForge negative quality-gate test passed")
PY

if "$tool_directory/viewforge.sh" "$tool_directory/examples/conflicting-ledger/viewforge.json"; then
    echo "Expected conflicting ledger IDs to fail calibration" >&2
    exit 1
fi
echo "ViewForge conflicting-ledger test passed"

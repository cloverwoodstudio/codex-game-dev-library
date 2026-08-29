#!/usr/bin/env bash
set -euo pipefail

tool_directory="$(cd "$(dirname "$0")/.." && pwd)"
output_directory="$tool_directory/examples/crate/output"
find "$output_directory" -depth -delete 2>/dev/null || true

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

blender --background --factory-startup --python-expr "import bpy; bpy.ops.import_scene.gltf(filepath='$output_directory/calibration-crate.glb'); model=[item for item in bpy.context.scene.objects if item.type == 'MESH' and item.name.startswith('calibration-crate')][0]; dimensions=tuple(round(value, 4) for value in model.dimensions); assert all(abs(actual - expected) < 0.01 for actual, expected in zip(dimensions, (2.0, 1.0, 1.5))), dimensions"

python3 - "$output_directory/validation.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as report_file:
    report = json.load(report_file)

assert report["occupied_voxels"] > 0
assert report["boundary_faces"] > 0
assert all(result["mode"] == "background" for result in report["inputs"].values())
assert len({result["path"] for result in report["inputs"].values()}) == 1
for view_name, result in report["views"].items():
    assert result["iou"] >= 0.95, (view_name, result)
print("ViewForge smoke test passed")
PY

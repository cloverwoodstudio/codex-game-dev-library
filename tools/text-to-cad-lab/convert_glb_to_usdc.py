"""Convert the native text-to-cad GLB export to USDC with Blender."""

import bpy
import sys
from pathlib import Path


def argument(name: str) -> Path:
    arguments = sys.argv[sys.argv.index("--") + 1 :]
    index = arguments.index(name)
    return Path(arguments[index + 1]).resolve()


source = argument("--input")
destination = argument("--output")
destination.parent.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(source))
bpy.ops.wm.usd_export(filepath=str(destination), export_materials=True)

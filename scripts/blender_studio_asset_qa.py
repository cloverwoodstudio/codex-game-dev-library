#!/usr/bin/env python3
"""Run INSIDE Blender: inspect a user-exported GLB/FBX, never modify source."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
from datetime import datetime, timezone

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from studio_asset_contract import hash_file, evaluate, read_json, validate_manifest


def parse_args() -> argparse.Namespace:
    arguments = sys.argv
    if "--" not in arguments:
        raise ValueError("Expected Blender arguments after --")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--manifest", help="Optional owner-entered Tripo Studio provenance")
    parser.add_argument("--max-triangles", type=int, default=25000)
    parser.add_argument("--max-materials", type=int, default=8)
    parser.add_argument("--require-uv", action="store_true")
    parser.add_argument("--expect-rig", action="store_true")
    parser.add_argument("--expect-animation", action="store_true")
    parsed = parser.parse_args(arguments[arguments.index("--") + 1:])
    if parsed.max_triangles < 1 or parsed.max_materials < 1:
        raise ValueError("Budgets must be positive")
    return parsed


def inspect_blender(src: Path) -> dict:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    if src.suffix.lower() == ".glb":
        bpy.ops.import_scene.gltf(filepath=str(src))
    elif src.suffix.lower() == ".fbx":
        try:
            bpy.ops.import_scene.fbx(filepath=str(src))
        except (AttributeError, RuntimeError):
            bpy.ops.wm.fbx_import(filepath=str(src))
    else:
        raise ValueError("Only GLB and FBX can be inspected")
    bpy.context.view_layer.update()
    objects = list(bpy.data.objects)
    meshes = [o for o in objects if o.type == "MESH"]
    arms = [o for o in objects if o.type == "ARMATURE"]
    vertices = sum(len(o.data.vertices) for o in meshes)
    triangles = sum(sum(max(0, len(poly.vertices) - 2) for poly in o.data.polygons) for o in meshes)
    uv = sum(len(o.data.uv_layers) for o in meshes)
    weighted = sum(sum(bool(v.groups) for v in o.data.vertices) for o in meshes)
    mats = {slot.material.name for o in meshes for slot in o.material_slots if slot.material}
    bone_count = sum(len(o.data.bones) for o in arms)
    images = [i for i in bpy.data.images if i.source not in {"GENERATED", "VIEWER"}]
    coords = [
        value
        for obj in meshes
        for v in obj.data.vertices
        for value in v.co
    ]
    nonfinite = sum(not math.isfinite(float(c)) for c in coords)
    corners = [
        obj.matrix_world @ Vector(v)
        for obj in meshes
        for v in obj.bound_box
    ]
    dimensions = None
    if corners:
        dimensions = [
            round(max(float(v[axis]) for v in corners) - min(float(v[axis]) for v in corners), 5)
            for axis in range(3)
        ]
        if not all(math.isfinite(x) for x in dimensions):
            nonfinite += 1
    return {
        "mesh_count": len(meshes),
        "vertices": vertices,
        "triangles": triangles,
        "material_count": len(mats),
        "material_names": sorted(mats)[:50],
        "uv_layer_count": uv,
        "armatures": len(arms),
        "bones": bone_count,
        "weighted_vertices": weighted,
        "animation_actions": len(bpy.data.actions),
        "animation_names": sorted(a.name for a in bpy.data.actions)[:80],
        "image_count": len(images),
        "image_names": sorted(i.name for i in images)[:50],
        "nonfinite_coordinate_count": nonfinite,
        "bounds_blender_units_unverified_scale": dimensions,
        "mesh_names": sorted(o.name for o in meshes)[:80],
    }


def main() -> int:
    args = parse_args()
    src = Path(args.input).expanduser().resolve(strict=True)
    dest = Path(args.output).expanduser().resolve()
    if src.suffix.lower() not in {".glb", ".fbx"}:
        raise ValueError("Only .glb or .fbx inputs are supported")
    if not src.is_file() or src.stat().st_size <= 0:
        raise ValueError("Source must be nonempty file")
    if not dest.parent.is_dir() or dest.exists():
        raise ValueError("Report parent must exist and report must be new")
    if dest == src:
        raise ValueError("Report cannot overwrite source")
    original_sha = hash_file(src)
    manifest = read_json(Path(args.manifest)) if args.manifest else None
    faults = validate_manifest(manifest, original_sha) if manifest else []
    stats = inspect_blender(src)
    if hash_file(src) != original_sha:
        raise RuntimeError("SOURCE MUTATION DETECTED")
    budget = {
        "max_triangles": args.max_triangles,
        "max_materials": args.max_materials,
        "require_uv": args.require_uv,
        "expect_rig": args.expect_rig,
        "expect_animation": args.expect_animation,
    }
    qa = evaluate(stats, budget, manifest)
    if faults:
        qa["failures"].extend("manifest_" + item for item in faults)
        qa["technical_status"] = "FIX"
    report = {
        "schema_version": 1,
        "inspected_at_utc": datetime.now(timezone.utc).isoformat(),
        "tool": "Blender offline / Cloverwood Studio read-only inspector",
        "source_path": str(src),
        "source_format": src.suffix.lower(),
        "source_sha256": original_sha,
        "source_bytes": src.stat().st_size,
        "provenance": "owner_claimed_tripo_studio" if manifest and not faults else "unverified",
        "manifest": manifest,
        "blender": bpy.app.version_string,
        "budget": budget,
        "metrics": stats,
        "qa": qa,
    }
    with dest.open("x", encoding="utf-8") as out:
        json.dump(report, out, indent=2, ensure_ascii=False)
        out.write("\n")
    print("CW_STUDIO_ASSET_QA " + json.dumps({
        "technical_status": qa["technical_status"],
        "shipping_status": qa["shipping_status"],
        "mesh_count": stats["mesh_count"],
        "triangles": stats["triangles"],
        "armatures": stats["armatures"],
        "actions": stats["animation_actions"],
        "source_unchanged": True,
        "report": str(dest),
    }))
    return 2 if qa["technical_status"] == "FIX" else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, FileNotFoundError, RuntimeError) as exc:
        print("CW_STUDIO_ASSET_QA_ERROR " + repr(exc), file=sys.stderr)
        raise SystemExit(2)

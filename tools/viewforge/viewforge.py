"""Deterministic three-view visual-hull reconstruction for Blender.

Run through viewforge.sh. This script intentionally uses only Blender's bundled
Python modules so the reconstruction stays portable and auditable.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector


UNIT_TO_METERS = {"m": 1.0, "cm": 0.01, "mm": 0.001}


def fail(message: str) -> None:
    raise ValueError(f"ViewForge: {message}")


def parse_arguments() -> Path:
    try:
        separator = sys.argv.index("--")
        arguments = sys.argv[separator + 1 :]
    except ValueError:
        arguments = []
    if len(arguments) != 1:
        fail("expected one manifest path after --")
    path = Path(arguments[0]).resolve()
    if not path.is_file():
        fail(f"manifest does not exist: {path}")
    return path


def load_manifest(path: Path) -> dict:
    with path.open(encoding="utf-8") as manifest_file:
        manifest = json.load(manifest_file)
    if manifest.get("version") != 1:
        fail("manifest version must be 1")
    if manifest.get("units", "m") not in UNIT_TO_METERS:
        fail("units must be m, cm or mm")
    for key in ("name", "dimensions", "resolution", "views", "output_directory"):
        if key not in manifest:
            fail(f"missing manifest key: {key}")
    for axis in ("width", "depth", "height"):
        if float(manifest["dimensions"].get(axis, 0)) <= 0:
            fail(f"dimension {axis} must be positive")
    for axis in ("x", "y", "z"):
        value = manifest["resolution"].get(axis)
        if not isinstance(value, int) or not 2 <= value <= 256:
            fail(f"resolution {axis} must be an integer from 2 through 256")
    for view_name in ("front", "side", "top"):
        if view_name not in manifest["views"]:
            fail(f"missing required view: {view_name}")
    return manifest


def load_pgm(path: Path) -> tuple[int, int, list[float]]:
    tokens = []
    for line in path.read_text(encoding="ascii").splitlines():
        tokens.extend(line.split("#", 1)[0].split())
    if not tokens or tokens[0] != "P2":
        fail(f"only ASCII P2 PGM is supported directly: {path}")
    width, height, maximum = map(int, tokens[1:4])
    values = [int(value) / maximum for value in tokens[4:]]
    if len(values) != width * height:
        fail(f"PGM pixel count does not match header: {path}")
    return width, height, values


def load_pixels(path: Path) -> tuple[int, int, list[tuple[float, float, float, float]]]:
    if path.suffix.lower() == ".pgm":
        width, height, values = load_pgm(path)
        return width, height, [(value, value, value, 1.0) for value in values]

    image = bpy.data.images.load(str(path), check_existing=False)
    width, height = image.size
    raw = list(image.pixels)
    pixels = []
    # Blender stores the first pixel at the lower-left. Normalize to top-left rows.
    for top_y in range(height):
        source_y = height - 1 - top_y
        for x in range(width):
            offset = (source_y * width + x) * 4
            pixels.append(tuple(raw[offset : offset + 4]))
    bpy.data.images.remove(image)
    return width, height, pixels


def build_mask(path: Path, config: dict, target_width: int, target_height: int) -> set[tuple[int, int]]:
    width, height, pixels = load_pixels(path)
    mode = config.get("mode")
    if mode not in ("dark", "light", "alpha"):
        fail(f"view mode must be dark, light or alpha: {path}")
    threshold = float(config.get("threshold", 0.5))
    def is_inside(pixel: tuple[float, float, float, float]) -> bool:
        red, green, blue, alpha = pixel
        luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
        return alpha >= threshold if mode == "alpha" else luminance <= threshold if mode == "dark" else luminance >= threshold

    source_mask = {(x, y) for y in range(height) for x in range(width) if is_inside(pixels[y * width + x])}
    if not source_mask:
        fail(f"view produced an empty mask: {path}")
    minimum_x = min(x for x, _ in source_mask)
    maximum_x = max(x for x, _ in source_mask)
    minimum_y = min(y for _, y in source_mask)
    maximum_y = max(y for _, y in source_mask)
    crop_width = maximum_x - minimum_x + 1
    crop_height = maximum_y - minimum_y + 1

    result = set()
    for v in range(target_height):
        normalized_v = (v + 0.5) / target_height
        if config.get("flip_vertical", False):
            normalized_v = 1.0 - normalized_v
        source_y = min(maximum_y, maximum_y - int(normalized_v * crop_height))
        for u in range(target_width):
            normalized_u = (u + 0.5) / target_width
            if config.get("flip_horizontal", False):
                normalized_u = 1.0 - normalized_u
            source_x = min(maximum_x, minimum_x + int(normalized_u * crop_width))
            if (source_x, source_y) in source_mask:
                result.add((u, v))
    return result


def resolve_view_path(manifest_directory: Path, config: dict) -> Path:
    path = (manifest_directory / config["path"]).resolve()
    if not path.is_file():
        fail(f"view image does not exist: {path}")
    return path


def reconstruct(nx: int, ny: int, nz: int, masks: dict[str, set[tuple[int, int]]]) -> set[tuple[int, int, int]]:
    occupied = set()
    for z in range(nz):
        for y in range(ny):
            for x in range(nx):
                if (x, z) in masks["front"] and (y, z) in masks["side"] and (x, y) in masks["top"]:
                    occupied.add((x, y, z))
    if not occupied:
        fail("the three silhouettes have no common 3D volume; check calibration, orientation and thresholds")
    return occupied


FACE_DEFINITIONS = (
    ((-1, 0, 0), ((0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0))),
    ((1, 0, 0), ((1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1))),
    ((0, -1, 0), ((0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1))),
    ((0, 1, 0), ((0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0))),
    ((0, 0, -1), ((0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0))),
    ((0, 0, 1), ((0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1))),
)


def create_mesh(name: str, occupied: set[tuple[int, int, int]], dimensions: tuple[float, float, float], resolution: tuple[int, int, int]):
    width, depth, height = dimensions
    nx, ny, nz = resolution
    vertex_indices: dict[tuple[int, int, int], int] = {}
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int, int]] = []

    def vertex_index(grid_vertex: tuple[int, int, int]) -> int:
        if grid_vertex not in vertex_indices:
            gx, gy, gz = grid_vertex
            vertex_indices[grid_vertex] = len(vertices)
            vertices.append((gx / nx * width - width / 2, gy / ny * depth - depth / 2, gz / nz * height))
        return vertex_indices[grid_vertex]

    for x, y, z in occupied:
        for neighbor_delta, corners in FACE_DEFINITIONS:
            neighbor = (x + neighbor_delta[0], y + neighbor_delta[1], z + neighbor_delta[2])
            if neighbor in occupied:
                continue
            face = tuple(vertex_index((x + dx, y + dy, z + dz)) for dx, dy, dz in corners)
            faces.append(face)

    mesh = bpy.data.meshes.new(f"{name}-mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    mesh.validate(verbose=True)
    model = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(model)
    return model, len(vertices), len(faces)


def add_material(model) -> None:
    material = bpy.data.materials.new("ViewForge evidence hull")
    material.diffuse_color = (0.055, 0.53, 0.76, 1.0)
    material.metallic = 0.05
    material.roughness = 0.38
    model.data.materials.append(material)


def apply_bevel(model, width: float, segments: int) -> None:
    if width <= 0:
        return
    modifier = model.modifiers.new(name="Evidence-safe bevel", type="BEVEL")
    modifier.width = width
    modifier.segments = segments
    modifier.limit_method = "ANGLE"
    bpy.context.view_layer.objects.active = model
    model.select_set(True)
    bpy.ops.object.modifier_apply(modifier=modifier.name)


def comparison(mask: set[tuple[int, int]], projection: set[tuple[int, int]]) -> dict:
    intersection = len(mask & projection)
    union = len(mask | projection)
    return {
        "iou": round(intersection / union if union else 1.0, 6),
        "mask_pixels": len(mask),
        "projected_pixels": len(projection),
        "missing_pixels": len(mask - projection),
        "extra_pixels": len(projection - mask),
    }


def configure_scene(render_size: int) -> None:
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = render_size
    scene.render.resolution_y = render_size
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.world.color = (0.018, 0.025, 0.04)
    scene.view_settings.look = "AgX - Medium High Contrast"

    bpy.ops.object.light_add(type="AREA", location=(4, -4, 6))
    key = bpy.context.object
    key.data.energy = 900
    key.data.shape = "DISK"
    key.data.size = 4
    bpy.ops.object.light_add(type="AREA", location=(-4, 3, 3))
    fill = bpy.context.object
    fill.data.energy = 500
    fill.data.size = 5


def point_camera(camera, location: tuple[float, float, float], target: tuple[float, float, float], scale: float) -> None:
    camera.location = location
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = scale


def render_views(output_directory: Path, dimensions: tuple[float, float, float]) -> None:
    width, depth, height = dimensions
    extent = max(dimensions)
    target = (0, 0, height / 2)
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    views = {
        "front": ((0, -extent * 3, height / 2), target, max(width, height) * 1.2),
        "side": ((extent * 3, 0, height / 2), target, max(depth, height) * 1.2),
        "top": ((0, 0, extent * 3), (0, 0, 0), max(width, depth) * 1.2),
    }
    for name, (location, view_target, scale) in views.items():
        point_camera(camera, location, view_target, scale)
        bpy.context.scene.render.filepath = str(output_directory / f"{name}.png")
        bpy.ops.render.render(write_still=True)


def export_outputs(output_directory: Path, name: str, model) -> None:
    for item in bpy.context.selected_objects:
        item.select_set(False)
    model.select_set(True)
    bpy.context.view_layer.objects.active = model
    bpy.ops.wm.save_as_mainfile(filepath=str(output_directory / f"{name}.blend"))
    bpy.ops.export_scene.gltf(filepath=str(output_directory / f"{name}.glb"), export_format="GLB", use_selection=True)
    bpy.ops.wm.usd_export(filepath=str(output_directory / f"{name}.usdc"), selected_objects_only=True)


def main() -> None:
    manifest_path = parse_arguments()
    manifest = load_manifest(manifest_path)
    manifest_directory = manifest_path.parent
    unit_scale = UNIT_TO_METERS[manifest.get("units", "m")]
    dimensions = tuple(float(manifest["dimensions"][key]) * unit_scale for key in ("width", "depth", "height"))
    nx, ny, nz = (manifest["resolution"][key] for key in ("x", "y", "z"))

    masks = {
        "front": build_mask(resolve_view_path(manifest_directory, manifest["views"]["front"]), manifest["views"]["front"], nx, nz),
        "side": build_mask(resolve_view_path(manifest_directory, manifest["views"]["side"]), manifest["views"]["side"], ny, nz),
        "top": build_mask(resolve_view_path(manifest_directory, manifest["views"]["top"]), manifest["views"]["top"], nx, ny),
    }
    occupied = reconstruct(nx, ny, nz, masks)

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    model, vertex_count, boundary_faces = create_mesh(manifest["name"], occupied, dimensions, (nx, ny, nz))
    add_material(model)
    apply_bevel(model, float(manifest.get("bevel_width", 0)) * unit_scale, int(manifest.get("bevel_segments", 2)))

    output_directory = (manifest_directory / manifest["output_directory"]).resolve()
    output_directory.mkdir(parents=True, exist_ok=True)
    configure_scene(int(manifest.get("render_size", 512)))
    render_views(output_directory, dimensions)
    export_outputs(output_directory, manifest["name"], model)

    projections = {
        "front": {(x, z) for x, _, z in occupied},
        "side": {(y, z) for _, y, z in occupied},
        "top": {(x, y) for x, y, _ in occupied},
    }
    report = {
        "viewforge_version": 1,
        "source_manifest": str(manifest_path),
        "name": manifest["name"],
        "source_units": manifest.get("units", "m"),
        "output_units": "m",
        "dimensions_m": {"width": dimensions[0], "depth": dimensions[1], "height": dimensions[2]},
        "resolution": {"x": nx, "y": ny, "z": nz},
        "occupied_voxels": len(occupied),
        "mesh_vertices_before_bevel": vertex_count,
        "boundary_faces": boundary_faces,
        "views": {name: comparison(masks[name], projections[name]) for name in masks},
        "claim": "Visual hull constrained by supplied silhouettes; hidden concavities and surface curvature remain unknown.",
    }
    with (output_directory / "validation.json").open("w", encoding="utf-8") as report_file:
        json.dump(report, report_file, indent=2)
        report_file.write("\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

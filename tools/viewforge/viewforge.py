"""Deterministic three-view visual-hull reconstruction for Blender.

Run through viewforge.sh. This script intentionally uses only Blender's bundled
Python modules so the reconstruction stays portable and auditable.
"""

from __future__ import annotations

import json
import sys
from collections import deque
from math import hypot
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


def projective_coordinates(corners: list[tuple[float, float]], u: float, v: float) -> tuple[float, float]:
    """Map a unit rectangle into an ordered TL/TR/BR/BL quadrilateral."""
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = corners
    dx1, dx2 = x1 - x2, x3 - x2
    dy1, dy2 = y1 - y2, y3 - y2
    dx3, dy3 = x0 - x1 + x2 - x3, y0 - y1 + y2 - y3
    denominator = dx1 * dy2 - dx2 * dy1
    if abs(dx3) < 1e-9 and abs(dy3) < 1e-9:
        g = h = 0.0
    else:
        if abs(denominator) < 1e-9:
            fail("perspective quadrilateral is degenerate")
        g = (dx3 * dy2 - dx2 * dy3) / denominator
        h = (dx1 * dy3 - dx3 * dy1) / denominator
    a, b, c = x1 - x0 + g * x1, x3 - x0 + h * x3, x0
    d, e, f = y1 - y0 + g * y1, y3 - y0 + h * y3, y0
    divisor = g * u + h * v + 1.0
    if abs(divisor) < 1e-9:
        fail("perspective mapping crosses infinity")
    return (a * u + b * v + c) / divisor, (d * u + e * v + f) / divisor


def validate_dimension_axes(config: dict, expected_dimensions: tuple[str, str], label: str, path: Path) -> dict:
    metadata = {}
    for axis_name, expected_dimension in zip(("horizontal", "vertical"), expected_dimensions):
        axis = config.get(axis_name)
        if not isinstance(axis, dict):
            fail(f"{label} requires {axis_name} axis: {path}")
        if axis.get("dimension") != expected_dimension:
            fail(f"{label} {axis_name} axis for this view must reference {expected_dimension}: {path}")
        ledger_id = axis.get("ledger_id")
        if not isinstance(ledger_id, str) or not ledger_id.strip():
            fail(f"{label} {axis_name}.ledger_id must be non-empty: {path}")
        metadata[axis_name] = {"dimension": expected_dimension, "ledger_id": ledger_id}
    return metadata


def clean_source_mask(
    mask: set[tuple[int, int]], crop_bounds: tuple[int, int, int, int], config: dict
) -> tuple[set[tuple[int, int]], dict]:
    crop_x, crop_y, crop_width, crop_height = crop_bounds
    crop_points = {
        (x, y)
        for y in range(crop_y, crop_y + crop_height)
        for x in range(crop_x, crop_x + crop_width)
    }
    original_pixels = len(mask)
    closing_radius = config.get("closing_radius", 0)
    if not isinstance(closing_radius, int) or not 0 <= closing_radius <= 8:
        fail("closing_radius must be an integer from 0 through 8")
    if closing_radius:
        offsets = range(-closing_radius, closing_radius + 1)
        dilated = {
            (x + dx, y + dy)
            for x, y in mask
            for dx in offsets
            for dy in offsets
            if (x + dx, y + dy) in crop_points
        }
        mask = {
            point
            for point in crop_points
            if all((point[0] + dx, point[1] + dy) in dilated for dx in offsets for dy in offsets)
        }

    components_found = 0
    if config.get("largest_component", False) and mask:
        unseen = set(mask)
        components = []
        while unseen:
            seed = unseen.pop()
            component = {seed}
            queue = [seed]
            while queue:
                x, y = queue.pop()
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        neighbor = (x + dx, y + dy)
                        if neighbor in unseen:
                            unseen.remove(neighbor)
                            component.add(neighbor)
                            queue.append(neighbor)
            components.append(component)
        components_found = len(components)
        mask = max(components, key=len)

    holes_filled = 0
    if config.get("fill_holes", False):
        exterior = set()
        queue = deque()
        maximum_x = crop_x + crop_width - 1
        maximum_y = crop_y + crop_height - 1
        boundary = (
            {(x, crop_y) for x in range(crop_x, maximum_x + 1)}
            | {(x, maximum_y) for x in range(crop_x, maximum_x + 1)}
            | {(crop_x, y) for y in range(crop_y, maximum_y + 1)}
            | {(maximum_x, y) for y in range(crop_y, maximum_y + 1)}
        )
        for point in boundary - mask:
            exterior.add(point)
            queue.append(point)
        while queue:
            x, y = queue.popleft()
            for neighbor in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if neighbor in crop_points and neighbor not in mask and neighbor not in exterior:
                    exterior.add(neighbor)
                    queue.append(neighbor)
        holes = crop_points - mask - exterior
        holes_filled = len(holes)
        mask |= holes

    return mask, {
        "original_pixels": original_pixels,
        "final_pixels": len(mask),
        "closing_radius": closing_radius,
        "largest_component": bool(config.get("largest_component", False)),
        "components_found": components_found,
        "fill_holes": bool(config.get("fill_holes", False)),
        "holes_filled_pixels": holes_filled,
    }


def build_mask(
    path: Path,
    config: dict,
    target_width: int,
    target_height: int,
    expected_dimensions: tuple[str, str],
) -> tuple[set[tuple[int, int]], dict, dict[tuple[int, int], tuple[float, float, float, float]]]:
    width, height, pixels = load_pixels(path)
    mode = config.get("mode")
    if mode not in ("dark", "light", "alpha", "background"):
        fail(f"view mode must be dark, light, alpha or background: {path}")
    threshold = float(config.get("threshold", 0.5))
    crop = config.get("crop", {"x": 0, "y": 0, "width": width, "height": height})
    crop_x, crop_y = int(crop["x"]), int(crop["y"])
    crop_width, crop_height = int(crop["width"]), int(crop["height"])
    if crop_width <= 0 or crop_height <= 0 or crop_x < 0 or crop_y < 0 or crop_x + crop_width > width or crop_y + crop_height > height:
        fail(f"crop is outside source image bounds: {path}")
    crop_maximum_x = crop_x + crop_width - 1
    crop_maximum_y = crop_y + crop_height - 1
    corner_pixels = [
        pixels[crop_y * width + crop_x],
        pixels[crop_y * width + crop_maximum_x],
        pixels[crop_maximum_y * width + crop_x],
        pixels[crop_maximum_y * width + crop_maximum_x],
    ]
    background_rgb = tuple(sum(pixel[channel] for pixel in corner_pixels) / 4 for channel in range(3))
    background_tolerance = float(config.get("background_tolerance", 0.12))

    def is_inside(pixel: tuple[float, float, float, float]) -> bool:
        red, green, blue, alpha = pixel
        luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
        if mode == "alpha":
            return alpha >= threshold
        if mode == "dark":
            return luminance <= threshold
        if mode == "light":
            return luminance >= threshold
        color_distance = ((red - background_rgb[0]) ** 2 + (green - background_rgb[1]) ** 2 + (blue - background_rgb[2]) ** 2) ** 0.5 / 3**0.5
        return color_distance >= background_tolerance

    source_mask = {
        (x, y)
        for y in range(crop_y, crop_y + crop_height)
        for x in range(crop_x, crop_x + crop_width)
        if is_inside(pixels[y * width + x])
    }
    source_mask, cleanup_metadata = clean_source_mask(source_mask, (crop_x, crop_y, crop_width, crop_height), config)
    if not source_mask:
        fail(f"view produced an empty mask: {path}")
    minimum_x = min(x for x, _ in source_mask)
    maximum_x = max(x for x, _ in source_mask)
    minimum_y = min(y for _, y in source_mask)
    maximum_y = max(y for _, y in source_mask)
    content_width = maximum_x - minimum_x + 1
    content_height = maximum_y - minimum_y + 1

    calibration = config.get("calibration")
    perspective = config.get("perspective_rectification")
    if calibration is not None and perspective is not None:
        fail(f"calibration and perspective_rectification are mutually exclusive: {path}")
    calibration_metadata = None
    perspective_metadata = None
    dimension_axes = None
    perspective_corners = None
    sample_minimum_x, sample_maximum_x = minimum_x, maximum_x
    sample_minimum_y, sample_maximum_y = minimum_y, maximum_y
    if calibration is not None:
        calibration_metadata = validate_dimension_axes(calibration, expected_dimensions, "calibration", path)
        for axis_name in ("horizontal", "vertical"):
            axis = calibration[axis_name]
            pixel_minimum = axis.get("pixel_min")
            pixel_maximum = axis.get("pixel_max")
            if not isinstance(pixel_minimum, int) or not isinstance(pixel_maximum, int) or pixel_minimum >= pixel_maximum:
                fail(f"calibration {axis_name} pixel_min/pixel_max must be increasing integers: {path}")
            crop_minimum = crop_x if axis_name == "horizontal" else crop_y
            crop_maximum = crop_maximum_x if axis_name == "horizontal" else crop_maximum_y
            if pixel_minimum < crop_minimum or pixel_maximum > crop_maximum:
                fail(f"calibration {axis_name} anchors are outside the requested crop: {path}")
            calibration_metadata[axis_name].update(
                {"pixel_min": pixel_minimum, "pixel_max": pixel_maximum, "pixel_span": pixel_maximum - pixel_minimum + 1}
            )
        sample_minimum_x = calibration["horizontal"]["pixel_min"]
        sample_maximum_x = calibration["horizontal"]["pixel_max"]
        sample_minimum_y = calibration["vertical"]["pixel_min"]
        sample_maximum_y = calibration["vertical"]["pixel_max"]
        dimension_axes = calibration_metadata

    if perspective is not None:
        dimension_axes = validate_dimension_axes(perspective, expected_dimensions, "perspective_rectification", path)
        corner_names = ("top_left", "top_right", "bottom_right", "bottom_left")
        perspective_corners = []
        for corner_name in corner_names:
            corner = perspective.get("corners", {}).get(corner_name)
            if not isinstance(corner, dict) or not all(isinstance(corner.get(axis), (int, float)) for axis in ("x", "y")):
                fail(f"perspective_rectification requires numeric {corner_name} x/y: {path}")
            point = (float(corner["x"]), float(corner["y"]))
            if not crop_x <= point[0] <= crop_maximum_x or not crop_y <= point[1] <= crop_maximum_y:
                fail(f"perspective corner {corner_name} is outside the requested crop: {path}")
            perspective_corners.append(point)
        cross_products = []
        for index in range(4):
            previous = perspective_corners[index]
            current = perspective_corners[(index + 1) % 4]
            following = perspective_corners[(index + 2) % 4]
            cross_products.append(
                (current[0] - previous[0]) * (following[1] - current[1])
                - (current[1] - previous[1]) * (following[0] - current[0])
            )
        if any(abs(value) < 1e-9 for value in cross_products) or not (all(value > 0 for value in cross_products) or all(value < 0 for value in cross_products)):
            fail(f"perspective corners must form an ordered, convex quadrilateral: {path}")
        top_left, top_right, bottom_right, bottom_left = perspective_corners
        dimension_axes["horizontal"]["mean_source_edge_pixels"] = round(
            (hypot(top_right[0] - top_left[0], top_right[1] - top_left[1]) + hypot(bottom_right[0] - bottom_left[0], bottom_right[1] - bottom_left[1])) / 2,
            6,
        )
        dimension_axes["vertical"]["mean_source_edge_pixels"] = round(
            (hypot(bottom_left[0] - top_left[0], bottom_left[1] - top_left[1]) + hypot(bottom_right[0] - top_right[0], bottom_right[1] - top_right[1])) / 2,
            6,
        )
        perspective_metadata = {
            "corners": {name: {"x": point[0], "y": point[1]} for name, point in zip(corner_names, perspective_corners)},
            "horizontal": dimension_axes["horizontal"],
            "vertical": dimension_axes["vertical"],
        }

    sample_width = sample_maximum_x - sample_minimum_x + 1
    sample_height = sample_maximum_y - sample_minimum_y + 1

    result = set()
    preview = {}
    for v in range(target_height):
        normalized_v = (v + 0.5) / target_height
        if config.get("flip_vertical", False):
            normalized_v = 1.0 - normalized_v
        for u in range(target_width):
            normalized_u = (u + 0.5) / target_width
            if config.get("flip_horizontal", False):
                normalized_u = 1.0 - normalized_u
            if perspective_corners is not None:
                source_float_x, source_float_y = projective_coordinates(perspective_corners, normalized_u, 1.0 - normalized_v)
                source_x, source_y = round(source_float_x), round(source_float_y)
            else:
                source_y = min(sample_maximum_y, sample_maximum_y - int(normalized_v * sample_height))
                source_x = min(sample_maximum_x, sample_minimum_x + int(normalized_u * sample_width))
            preview[(u, v)] = pixels[source_y * width + source_x]
            if (source_x, source_y) in source_mask:
                result.add((u, v))
    metadata = {
        "path": str(path),
        "source_size": {"width": width, "height": height},
        "requested_crop": {"x": crop_x, "y": crop_y, "width": crop_width, "height": crop_height},
        "detected_content_bounds": {"x": minimum_x, "y": minimum_y, "width": content_width, "height": content_height},
        "mapping_strategy": (
            "projective_rectification" if perspective is not None else "calibrated_anchors" if calibration is not None else "detected_content_bounds"
        ),
        "calibration": calibration_metadata,
        "perspective_rectification": perspective_metadata,
        "dimension_axes": dimension_axes,
        "mask_cleanup": cleanup_metadata,
        "mode": mode,
        "threshold": threshold if mode != "background" else None,
        "background_tolerance": background_tolerance if mode == "background" else None,
    }
    return result, metadata, preview


def write_mask_pgm(path: Path, mask: set[tuple[int, int]], width: int, height: int) -> None:
    lines = ["P2", f"{width} {height}", "255"]
    for image_y in range(height - 1, -1, -1):
        lines.append(" ".join("0" if (x, image_y) in mask else "255" for x in range(width)))
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def write_overlay_png(
    path: Path,
    preview: dict[tuple[int, int], tuple[float, float, float, float]],
    mask: set[tuple[int, int]],
    projection: set[tuple[int, int]],
    width: int,
    height: int,
    scale: int = 8,
) -> None:
    """Write a nearest-neighbor evidence overlay large enough for visual review."""
    pixels = []
    for output_y in range(height * scale):
        v = output_y // scale
        for output_x in range(width * scale):
            u = output_x // scale
            red, green, blue, _ = preview[(u, v)]
            in_mask = (u, v) in mask
            in_projection = (u, v) in projection
            if in_mask and in_projection:
                color = (0.08 + 0.18 * red, 0.72 + 0.22 * green, 0.10 + 0.18 * blue, 1.0)
            elif in_mask:
                color = (1.0, 0.08, 0.04, 1.0)
            elif in_projection:
                color = (0.78, 0.06, 1.0, 1.0)
            else:
                color = (0.20 * red, 0.20 * green, 0.20 * blue, 1.0)
            pixels.extend(color)
    image = bpy.data.images.new(f"ViewForge overlay {path.stem}", width=width * scale, height=height * scale, alpha=True)
    image.pixels.foreach_set(pixels)
    image.filepath_raw = str(path)
    image.file_format = "PNG"
    image.save()
    bpy.data.images.remove(image)


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


def apply_surface_finish(model, config: dict | None, unit_scale: float) -> dict:
    if not config:
        return {"applied": False}
    for item in bpy.context.selected_objects:
        item.select_set(False)
    model.select_set(True)
    bpy.context.view_layer.objects.active = model

    voxel_size_source = float(config.get("voxel_size", 0))
    if voxel_size_source < 0:
        fail("surface_finish.voxel_size must not be negative")
    voxel_size = voxel_size_source * unit_scale
    if voxel_size > 0:
        model.data.remesh_voxel_size = voxel_size
        bpy.ops.object.voxel_remesh()

    smooth_iterations = config.get("smooth_iterations", 0)
    if not isinstance(smooth_iterations, int) or not 0 <= smooth_iterations <= 50:
        fail("surface_finish.smooth_iterations must be an integer from 0 through 50")
    smooth_factor = float(config.get("smooth_factor", 0.18))
    if not 0 <= smooth_factor <= 1:
        fail("surface_finish.smooth_factor must be from 0 through 1")
    if smooth_iterations > 0:
        modifier = model.modifiers.new(name="Evidence-derived Laplacian smooth", type="LAPLACIANSMOOTH")
        modifier.iterations = smooth_iterations
        modifier.lambda_factor = smooth_factor
        modifier.use_volume_preserve = True
        bpy.ops.object.modifier_apply(modifier=modifier.name)

    decimate_ratio = float(config.get("decimate_ratio", 1.0))
    if not 0 < decimate_ratio <= 1:
        fail("surface_finish.decimate_ratio must be greater than 0 and at most 1")
    if decimate_ratio < 1.0:
        modifier = model.modifiers.new(name="Runtime decimation", type="DECIMATE")
        modifier.ratio = decimate_ratio
        bpy.ops.object.modifier_apply(modifier=modifier.name)

    if config.get("shade_smooth", True):
        for polygon in model.data.polygons:
            polygon.use_smooth = True
    model.data.update()
    return {
        "applied": True,
        "voxel_size_m": voxel_size,
        "smooth_iterations": smooth_iterations,
        "smooth_factor": smooth_factor,
        "decimate_ratio": decimate_ratio,
        "vertices": len(model.data.vertices),
        "polygons": len(model.data.polygons),
        "dimensions_m": [round(value, 6) for value in model.dimensions],
        "claim": "Derived surface treatment; silhouette-supported but curvature and topology are estimated.",
    }


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

    masks = {}
    previews = {}
    input_metadata = {}
    target_sizes = {"front": (nx, nz), "side": (ny, nz), "top": (nx, ny)}
    view_dimensions = {
        "front": ("width", "height"),
        "side": ("depth", "height"),
        "top": ("width", "depth"),
    }
    for view_name, (target_width, target_height) in target_sizes.items():
        view_config = manifest["views"][view_name]
        masks[view_name], input_metadata[view_name], previews[view_name] = build_mask(
            resolve_view_path(manifest_directory, view_config),
            view_config,
            target_width,
            target_height,
            view_dimensions[view_name],
        )

    ledger_ids: dict[str, str] = {}
    for metadata in input_metadata.values():
        for axis in (metadata.get("dimension_axes") or {}).values():
            dimension = axis["dimension"]
            existing = ledger_ids.setdefault(dimension, axis["ledger_id"])
            if existing != axis["ledger_id"]:
                fail(f"conflicting calibration ledger IDs for {dimension}: {existing} and {axis['ledger_id']}")
            dimension_value = float(manifest["dimensions"][dimension])
            if "pixel_span" in axis:
                axis["pixels_per_source_unit"] = round(axis["pixel_span"] / dimension_value, 6)
                axis["source_units_per_pixel"] = round(dimension_value / axis["pixel_span"], 6)
            elif "mean_source_edge_pixels" in axis:
                axis["mean_pixels_per_source_unit"] = round(axis["mean_source_edge_pixels"] / dimension_value, 6)
                axis["mean_source_units_per_pixel"] = round(dimension_value / axis["mean_source_edge_pixels"], 6)
    occupied = reconstruct(nx, ny, nz, masks)

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    model, vertex_count, boundary_faces = create_mesh(manifest["name"], occupied, dimensions, (nx, ny, nz))
    add_material(model)
    apply_bevel(model, float(manifest.get("bevel_width", 0)) * unit_scale, int(manifest.get("bevel_segments", 2)))
    surface_finish = apply_surface_finish(model, manifest.get("surface_finish"), unit_scale)

    output_directory = (manifest_directory / manifest["output_directory"]).resolve()
    output_directory.mkdir(parents=True, exist_ok=True)
    masks_directory = output_directory / "masks"
    masks_directory.mkdir(parents=True, exist_ok=True)
    for view_name, (target_width, target_height) in target_sizes.items():
        write_mask_pgm(masks_directory / f"{view_name}.pgm", masks[view_name], target_width, target_height)
    configure_scene(int(manifest.get("render_size", 512)))
    render_views(output_directory, dimensions)
    export_outputs(output_directory, manifest["name"], model)

    projections = {
        "front": {(x, z) for x, _, z in occupied},
        "side": {(y, z) for _, y, z in occupied},
        "top": {(x, y) for x, y, _ in occupied},
    }
    overlays_directory = output_directory / "overlays"
    overlays_directory.mkdir(parents=True, exist_ok=True)
    for view_name, (target_width, target_height) in target_sizes.items():
        write_overlay_png(
            overlays_directory / f"{view_name}.png",
            previews[view_name],
            masks[view_name],
            projections[view_name],
            target_width,
            target_height,
        )

    view_results = {name: comparison(masks[name], projections[name]) for name in masks}
    minimum_iou = float(manifest.get("quality_gate", {}).get("minimum_iou", 0.95))
    if not 0 <= minimum_iou <= 1:
        fail("quality_gate.minimum_iou must be from 0 through 1")
    failed_views = [name for name, result in view_results.items() if result["iou"] < minimum_iou]
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
        "surface_finish": surface_finish,
        "inputs": input_metadata,
        "dimension_ledger_ids": ledger_ids,
        "views": view_results,
        "quality_gate": {
            "minimum_iou": minimum_iou,
            "passed": not failed_views,
            "failed_views": failed_views,
        },
        "evidence": {
            "normalized_masks": "masks/",
            "source_mask_projection_overlays": "overlays/",
            "orthographic_renders": ["front.png", "side.png", "top.png"],
        },
        "claim": "Visual hull constrained by supplied silhouettes; hidden concavities and surface curvature remain unknown.",
    }
    with (output_directory / "validation.json").open("w", encoding="utf-8") as report_file:
        json.dump(report, report_file, indent=2)
        report_file.write("\n")
    print(json.dumps(report, indent=2))
    if failed_views:
        fail(f"quality gate failed for views: {', '.join(failed_views)}; inspect validation.json and overlays/")


if __name__ == "__main__":
    main()

"""Parametric hard-surface junction tile for the Living Fractures prototype.

Units: millimetres. Origin: centre of the footprint on the bottom face.
The STEP model is the source geometry; GLB/USDZ are derived game assets.
"""

from build123d import Align, Axis, Box, Cylinder, Location, fillet


TILE_SIZE = 92.0
TILE_HEIGHT = 10.0
CORNER_RADIUS = 7.0
CHANNEL_WIDTH = 8.0
CHANNEL_DEPTH = 2.2
HUB_RADIUS = 17.0
HUB_RECESS_DEPTH = 1.2


def gen_step():
    """Build a four-way circuit junction as one closed positive-volume solid."""
    tile = Box(
        TILE_SIZE,
        TILE_SIZE,
        TILE_HEIGHT,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    vertical_edges = tile.edges().filter_by(Axis.Z)
    tile = fillet(vertical_edges, radius=CORNER_RADIUS)

    # Overshoot every subtractive tool to avoid coincident boolean faces.
    channel_z = TILE_HEIGHT - CHANNEL_DEPTH
    horizontal_channel = Location((0, 0, channel_z)) * Box(
        TILE_SIZE + 2.0,
        CHANNEL_WIDTH,
        CHANNEL_DEPTH + 1.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    vertical_channel = Location((0, 0, channel_z)) * Box(
        CHANNEL_WIDTH,
        TILE_SIZE + 2.0,
        CHANNEL_DEPTH + 1.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    hub_recess = Location((0, 0, TILE_HEIGHT - HUB_RECESS_DEPTH)) * Cylinder(
        HUB_RADIUS,
        HUB_RECESS_DEPTH + 1.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )

    tile = tile - horizontal_channel - vertical_channel - hub_recess
    tile.label = "lighthouse_junction_tile"
    return tile

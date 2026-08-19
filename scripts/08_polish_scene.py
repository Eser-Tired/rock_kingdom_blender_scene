"""Apply final camera and night-sky polish discovered during render review."""

from pathlib import Path
import importlib
import sys

import bpy


ROOT = Path(r"C:\Users\Eser\Documents\Code\rock_kingdom_blender_scene")
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import common as C

C = importlib.reload(C)

scene = bpy.context.scene
world = scene.world
background = next((node for node in world.node_tree.nodes if node.type == "BACKGROUND"), None)
if background is None:
    raise RuntimeError("World Background node not found")
background.inputs["Color"].default_value = (0.012, 0.040, 0.180, 1.0)
background.inputs["Strength"].default_value = 0.32

close_camera = bpy.data.objects["RK_Camera_Character"]
close_camera.data.lens = 40.0
C.look_at(close_camera, (-0.05, -4.0, 3.05))

wide_camera = bpy.data.objects["RK_Camera_Wide"]
wide_camera.location = (-12.5, -22.5, 6.4)
wide_camera.data.lens = 34.0
C.look_at(wide_camera, (2.0, 5.0, 4.8))

scene["rk_polish"] = "deep_blue_sky_lower_wide_camera_full_character_closeup"
C.save_mainfile()
print("RK_POLISH_OK sky=(0.012,0.040,0.180) close_lens=40 wide_lens=34")

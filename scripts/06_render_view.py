"""Render one named final view. Set RK_RENDER_NAME in the exec globals."""

from pathlib import Path
import sys

import bpy


ROOT = Path(r"C:\Users\Eser\Documents\Code\rock_kingdom_blender_scene")
RENDERS = ROOT / "renders"
RENDERS.mkdir(parents=True, exist_ok=True)

views = {
    "final_hero": ("RK_Camera_Hero", "final_hero.png"),
    "plaza_wide": ("RK_Camera_Wide", "plaza_wide.png"),
    "character_closeup": ("RK_Camera_Character", "character_closeup.png"),
}

render_name = globals().get("RK_RENDER_NAME", "final_hero")
if render_name not in views:
    raise KeyError(f"Unknown render view: {render_name}")

camera_name, filename = views[render_name]
camera_obj = bpy.data.objects.get(camera_name)
if camera_obj is None:
    raise RuntimeError(f"Camera not found: {camera_name}")

scene = bpy.context.scene
scene.camera = camera_obj
scene.render.resolution_x = 960
scene.render.resolution_y = 600
scene.render.resolution_percentage = 100
scene.render.filepath = str(RENDERS / filename)
bpy.context.view_layer.update()
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "rock_kingdom_fantasy_plaza.blend"))

output = RENDERS / filename
if not output.exists() or output.stat().st_size < 100_000:
    raise AssertionError(f"Render output is missing or too small: {output}")
print(f"RK_RENDER_OK {render_name} path={output} bytes={output.stat().st_size}")

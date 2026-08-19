"""Create the night lighting rig, three cameras and final render settings."""

from pathlib import Path
import importlib
import math
import sys

import bpy


ROOT = Path(r"C:\Users\Eser\Documents\Code\rock_kingdom_blender_scene")
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import common as C

C = importlib.reload(C)

light_coll = bpy.data.collections["RK_LIGHTING"]
camera_coll = bpy.data.collections["RK_CAMERAS"]
for target_coll in (light_coll, camera_coll):
    for obj in list(target_coll.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
for datablock in list(bpy.data.lights):
    if datablock.users == 0:
        bpy.data.lights.remove(datablock)
for datablock in list(bpy.data.cameras):
    if datablock.users == 0:
        bpy.data.cameras.remove(datablock)

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 960
scene.render.resolution_y = 600
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.render.image_settings.color_depth = "8"
scene.render.film_transparent = False
scene.render.use_file_extension = True

# Blender 5.2 compositor node groups replace Scene.node_tree. Create a portable
# glow chain when the group API is available; the scene remains renderable if
# a build lacks these node types.
try:
    old_group = bpy.data.node_groups.get("RK_Compositor")
    if old_group is not None:
        bpy.data.node_groups.remove(old_group, do_unlink=True)
    group = bpy.data.node_groups.new("RK_Compositor", "CompositorNodeTree")
    render_layers = group.nodes.new("CompositorNodeRLayers")
    glare = group.nodes.new("CompositorNodeGlare")
    glare.glare_type = "FOG_GLOW"
    glare.quality = "HIGH"
    glare.threshold = 1.0
    glare.size = 6
    composite = group.nodes.new("CompositorNodeComposite")
    group.links.new(render_layers.outputs["Image"], glare.inputs["Image"])
    group.links.new(glare.outputs["Image"], composite.inputs["Image"])
    scene.compositing_node_group = group
    scene.use_nodes = True
    scene["rk_compositor"] = "fog_glow"
except Exception as exc:
    scene["rk_compositor"] = f"native_emission_fallback: {exc}"
    print("RK_COMPOSITOR_FALLBACK", exc)


# Cool moon key.
sun_data = bpy.data.lights.new("RK_Light_Moon_Data", "SUN")
sun_data.color = (0.28, 0.43, 1.0)
sun_data.energy = 1.45
sun_data.angle = math.radians(18)
sun = bpy.data.objects.new("RK_Light_Moon", sun_data)
light_coll.objects.link(sun)
sun.rotation_euler = (math.radians(28), math.radians(-18), math.radians(-32))

# Broad warm/cool balance across architecture and plaza.
C.area_light("RK_Light_WarmArchitecture", (-8.0, -1.0, 11.0), (-4.0, 7.0, 4.0), (1.0, 0.32, 0.10), 1700, 7.0, light_coll)
C.area_light("RK_Light_BlueFill", (13.0, -3.0, 12.0), (5.0, 6.0, 4.5), (0.16, 0.30, 1.0), 1450, 9.0, light_coll)
C.area_light("RK_Light_GateTop", (8.0, 6.2, 13.0), (8.0, 11.0, 6.0), (1.0, 0.42, 0.12), 1200, 5.0, light_coll)
C.area_light("RK_Light_HeroKey", (4.8, -10.5, 8.0), (0.0, -4.0, 3.0), (1.0, 0.45, 0.18), 1250, 4.0, light_coll)
C.area_light("RK_Light_HeroRim", (-4.5, -1.5, 7.5), (0.0, -4.0, 3.2), (0.10, 0.55, 1.0), 1100, 3.5, light_coll)

# Every visible lamp receives an actual point source at its emissive core.
lamp_specs = [
    (-10.8, -6.5, 1.0), (-10.8, 0.2, 1.0), (-10.4, 6.0, 1.0),
    (10.5, -6.5, 1.0), (11.3, 0.0, 1.0), (13.2, 6.6, 1.0),
    (-3.8, 10.0, 0.82), (3.1, 9.3, 0.82),
]
for idx, (x, y, scale) in enumerate(lamp_specs):
    C.point_light(
        f"RK_Light_Lamp_{idx:02d}",
        (x + 0.82 * scale, y, 3.28 * scale),
        (1.0, 0.26, 0.035),
        420 if scale == 1.0 else 330,
        1.0,
        light_coll,
    )

# Windows, gate interior and guild porch provide pools of warm indirect-looking light.
for idx, (location, energy, radius) in enumerate((
    ((-7.0, 4.9, 3.7), 750, 2.2),
    ((-2.5, 4.9, 4.4), 620, 2.0),
    ((1.6, 5.7, 5.0), 620, 1.8),
    ((8.0, 10.2, 4.0), 950, 2.4),
    ((15.2, 3.0, 3.1), 680, 2.0),
)):
    C.point_light(f"RK_Light_Building_{idx:02d}", location, (1.0, 0.30, 0.055), energy, radius, light_coll)

# A subtle cyan light binds the companion sprite to the hero group.
C.point_light("RK_Light_Sprite", (-1.13, -4.0, 3.05), (0.02, 0.62, 1.0), 280, 0.8, light_coll)


# Three curated views: reference-like hero frame, full plaza and character study.
hero_camera = C.camera(
    "RK_Camera_Hero",
    (9.6, -19.0, 6.8),
    (0.0, 0.0, 4.35),
    42.0,
    camera_coll,
)
wide_camera = C.camera(
    "RK_Camera_Wide",
    (-12.5, -22.5, 6.4),
    (2.0, 5.0, 4.8),
    34.0,
    camera_coll,
)
close_camera = C.camera(
    "RK_Camera_Character",
    (4.8, -14.4, 4.7),
    (-0.05, -4.0, 3.05),
    40.0,
    camera_coll,
)

head = bpy.data.objects.get("RK_Hero_Head")
for camera_obj, fstop in ((hero_camera, 6.3), (wide_camera, 9.0), (close_camera, 5.0)):
    camera_obj.data.dof.use_dof = True
    camera_obj.data.dof.focus_object = head
    camera_obj.data.dof.aperture_fstop = fstop
    camera_obj.data.lens_unit = "MILLIMETERS"

scene.camera = hero_camera
scene["rk_render_views"] = ["final_hero", "plaza_wide", "character_closeup"]
scene["rk_lighting_style"] = "warm_architecture_cool_moon"
C.save_mainfile()
C.scene_summary("05_lighting")


"""Reset Blender and construct the plaza/material foundation."""

from pathlib import Path
import math
import sys

import bpy


ROOT = Path(r"C:\Users\Eser\Documents\Code\rock_kingdom_blender_scene")
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import common as C


# Deterministic reset.
for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
for coll in list(bpy.data.collections):
    bpy.data.collections.remove(coll)
for material in list(bpy.data.materials):
    bpy.data.materials.remove(material)
for curve in list(bpy.data.curves):
    if curve.users == 0:
        bpy.data.curves.remove(curve)
for mesh in list(bpy.data.meshes):
    if mesh.users == 0:
        bpy.data.meshes.remove(mesh)


scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 960
scene.render.resolution_y = 600
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.film_transparent = False
scene.render.use_file_extension = True
scene.render.resolution_percentage = 100
scene.render.image_settings.color_depth = "8"
scene.render.engine = "BLENDER_EEVEE"
scene.render.use_compositing = True
scene.render.use_sequencer = False

try:
    scene.view_settings.look = "AgX - Medium High Contrast"
except Exception:
    pass

world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs["Color"].default_value = (0.012, 0.040, 0.180, 1.0)
bg.inputs["Strength"].default_value = 0.32

# Blender 5.2 may expose compositor nodes through the new compositor API rather
# than Scene.node_tree. Native emissive materials remain the deterministic
# fallback, while older-compatible builds receive the Fog Glow node chain.
if hasattr(scene, "node_tree") and scene.node_tree is not None:
    scene.use_nodes = True
    nodes = scene.node_tree.nodes
    links = scene.node_tree.links
    nodes.clear()
    render_layers = nodes.new("CompositorNodeRLayers")
    glare = nodes.new("CompositorNodeGlare")
    glare.glare_type = "FOG_GLOW"
    glare.quality = "HIGH"
    glare.threshold = 0.8
    glare.size = 6
    composite = nodes.new("CompositorNodeComposite")
    links.new(render_layers.outputs["Image"], glare.inputs["Image"])
    links.new(glare.outputs["Image"], composite.inputs["Image"])


collections = {
    name: C.collection(name)
    for name in (
        "RK_PLAZA",
        "RK_ARCHITECTURE",
        "RK_ENVIRONMENT",
        "RK_HERO_CHARACTER",
        "RK_COMPANION",
        "RK_LIGHTING",
        "RK_CAMERAS",
    )
}


palette = {
    "RK_MAT_Pavement": ((0.45, 0.50, 0.66), 0.82, 0.0),
    "RK_MAT_PavementLight": ((0.68, 0.66, 0.78), 0.78, 0.0),
    "RK_MAT_PavementDark": ((0.24, 0.29, 0.43), 0.82, 0.0),
    "RK_MAT_Inlay": ((0.73, 0.43, 0.31), 0.72, 0.0),
    "RK_MAT_StoneCream": ((0.77, 0.68, 0.54), 0.76, 0.0),
    "RK_MAT_StoneWarm": ((0.56, 0.43, 0.35), 0.78, 0.0),
    "RK_MAT_StoneDark": ((0.16, 0.19, 0.28), 0.78, 0.0),
    "RK_MAT_PlasterOrange": ((0.76, 0.31, 0.12), 0.74, 0.0),
    "RK_MAT_PlasterGold": ((0.94, 0.54, 0.18), 0.70, 0.0),
    "RK_MAT_RoofRed": ((0.34, 0.055, 0.065), 0.68, 0.0),
    "RK_MAT_RoofHighlight": ((0.54, 0.10, 0.12), 0.64, 0.0),
    "RK_MAT_Wood": ((0.25, 0.085, 0.035), 0.72, 0.0),
    "RK_MAT_Leather": ((0.20, 0.09, 0.045), 0.58, 0.0),
    "RK_MAT_Gold": ((0.92, 0.48, 0.08), 0.34, 0.55),
    "RK_MAT_Bronze": ((0.32, 0.12, 0.035), 0.46, 0.70),
    "RK_MAT_Silver": ((0.55, 0.64, 0.75), 0.28, 0.78),
    "RK_MAT_BlackMetal": ((0.035, 0.045, 0.08), 0.35, 0.72),
    "RK_MAT_Window": ((0.20, 0.52, 0.82), 0.18, 0.05),
    "RK_MAT_Hedge": ((0.15, 0.36, 0.10), 0.86, 0.0),
    "RK_MAT_LeafGold": ((0.92, 0.50, 0.04), 0.88, 0.0),
    "RK_MAT_LeafOrange": ((0.82, 0.20, 0.035), 0.88, 0.0),
    "RK_MAT_LeafRust": ((0.42, 0.065, 0.025), 0.88, 0.0),
    "RK_MAT_LeafGreen": ((0.12, 0.44, 0.20), 0.88, 0.0),
    "RK_MAT_FlowerBlue": ((0.12, 0.40, 0.95), 0.70, 0.0),
    "RK_MAT_FlowerPink": ((0.95, 0.20, 0.46), 0.70, 0.0),
    "RK_MAT_FlowerCream": ((0.95, 0.82, 0.36), 0.70, 0.0),
    "RK_MAT_Skin": ((0.96, 0.63, 0.50), 0.62, 0.0),
    "RK_MAT_SkinWarm": ((0.86, 0.42, 0.34), 0.62, 0.0),
    "RK_MAT_HairCyan": ((0.24, 0.78, 0.88), 0.50, 0.0),
    "RK_MAT_HairLavender": ((0.62, 0.38, 0.82), 0.54, 0.0),
    "RK_MAT_Navy": ((0.055, 0.07, 0.24), 0.52, 0.0),
    "RK_MAT_NavyLight": ((0.16, 0.16, 0.46), 0.50, 0.0),
    "RK_MAT_White": ((0.91, 0.89, 0.80), 0.60, 0.0),
    "RK_MAT_RedBow": ((0.68, 0.025, 0.09), 0.45, 0.0),
    "RK_MAT_EyeViolet": ((0.36, 0.10, 0.76), 0.30, 0.0),
    "RK_MAT_EyeBlack": ((0.006, 0.004, 0.012), 0.28, 0.0),
    "RK_MAT_PetPurple": ((0.22, 0.09, 0.42), 0.58, 0.0),
    "RK_MAT_PetTeal": ((0.10, 0.58, 0.50), 0.48, 0.0),
}

for name, (color, roughness, metallic) in palette.items():
    C.material(name, color, roughness=roughness, metallic=metallic)

C.material(
    "RK_MAT_LanternGlow",
    (1.0, 0.36, 0.035),
    roughness=0.22,
    emission=(1.0, 0.24, 0.015),
    emission_strength=9.0,
)
C.material(
    "RK_MAT_WindowGlow",
    (1.0, 0.55, 0.12),
    roughness=0.30,
    emission=(1.0, 0.28, 0.02),
    emission_strength=3.6,
)
C.material(
    "RK_MAT_SpriteGlow",
    (0.08, 0.94, 1.0),
    roughness=0.18,
    emission=(0.02, 0.75, 1.0),
    emission_strength=7.0,
)


plaza = collections["RK_PLAZA"]
C.box(
    "RK_Plaza_Base",
    (0.0, 0.2, -0.27),
    (34.0, 30.0, 0.52),
    "RK_MAT_PavementDark",
    plaza,
    bevel_width=0.12,
)

# A grid of broad, slightly varied stone slabs keeps the floor readable and editable.
tile_materials = ["RK_MAT_Pavement", "RK_MAT_PavementLight", "RK_MAT_Pavement"]
for ix in range(-5, 6):
    for iy in range(-4, 5):
        x = ix * 2.82
        y = iy * 2.82 - 0.3
        variation = (ix * 13 + iy * 7) % len(tile_materials)
        tile = C.box(
            f"RK_Plaza_Tile_{ix + 5:02d}_{iy + 4:02d}",
            (x, y, 0.025 + 0.006 * ((ix + iy) % 2)),
            (2.70, 2.70, 0.10),
            tile_materials[variation],
            plaza,
            bevel_width=0.045,
        )
        tile["surface_role"] = "walkable"

# Bronze-red border, circular inlays and an eight-point central sigil.
for radius, minor, material_name in (
    (3.2, 0.10, "RK_MAT_Inlay"),
    (5.2, 0.13, "RK_MAT_StoneCream"),
    (6.0, 0.07, "RK_MAT_Inlay"),
):
    C.torus(
        f"RK_Plaza_Ring_{int(radius * 10):02d}",
        (0.0, -0.3, 0.14),
        radius,
        minor,
        material_name,
        plaza,
        major_segments=64,
        minor_segments=8,
    )

C.star(
    "RK_Plaza_Center_Star",
    (0.0, -0.3),
    0.17,
    2.4,
    0.95,
    8,
    0.08,
    "RK_MAT_Inlay",
    plaza,
    rotation=math.pi / 8,
)
C.star(
    "RK_Plaza_Center_Star_Core",
    (0.0, -0.3),
    0.22,
    0.72,
    0.34,
    8,
    0.08,
    "RK_MAT_Gold",
    plaza,
    rotation=math.pi / 8,
)
for i in range(8):
    angle = i * math.tau / 8
    C.box(
        f"RK_Plaza_Radial_{i:02d}",
        (4.1 * math.cos(angle), -0.3 + 4.1 * math.sin(angle), 0.13),
        (2.35, 0.12, 0.07),
        "RK_MAT_Inlay",
        plaza,
        rotation=(0.0, 0.0, angle),
        bevel_width=0.025,
    )

# Raised outer curbs frame the playable plaza.
C.box("RK_Plaza_Curb_Left", (-16.0, 0.0, 0.18), (0.45, 29.5, 0.42), "RK_MAT_StoneCream", plaza, bevel_width=0.08)
C.box("RK_Plaza_Curb_Right", (16.0, 0.0, 0.18), (0.45, 29.5, 0.42), "RK_MAT_StoneCream", plaza, bevel_width=0.08)
C.box("RK_Plaza_Curb_Back", (0.0, 14.2, 0.18), (32.0, 0.45, 0.42), "RK_MAT_StoneCream", plaza, bevel_width=0.08)

scene["rk_project"] = "Rock Kingdom Fantasy Plaza"
scene["rk_reference_count"] = 6
scene["rk_pipeline_version"] = "1.0"
C.save_mainfile()
C.scene_summary("01_setup")

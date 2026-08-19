"""Populate the fantasy plaza with autumn foliage, lamps, flags and guards."""

from pathlib import Path
import math
import random
import sys

import bpy


ROOT = Path(r"C:\Users\Eser\Documents\Code\rock_kingdom_blender_scene")
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import common as C
import importlib

C = importlib.reload(C)


random.seed(201470094)
coll = bpy.data.collections["RK_ENVIRONMENT"]
for obj in list(coll.objects):
    bpy.data.objects.remove(obj, do_unlink=True)


def tree(name, x, y, scale=1.0, colors=("RK_MAT_LeafGold", "RK_MAT_LeafOrange", "RK_MAT_LeafRust")):
    trunk_z = 2.75 * scale
    C.cylinder(f"{name}_Trunk", (x, y, trunk_z / 2), 0.38 * scale, trunk_z, "RK_MAT_Wood", coll, vertices=14, bevel_width=0.035, smooth_shading=True)
    branch_ends = [
        (-1.45, -0.25, 3.55), (1.25, 0.15, 3.85), (-0.55, 0.65, 4.55),
        (0.65, -0.55, 4.65), (0.0, 0.05, 5.45),
    ]
    for idx, (dx, dy, dz) in enumerate(branch_ends):
        C.cylinder_between(
            f"{name}_Branch_{idx:02d}",
            (x, y, trunk_z * 0.66),
            (x + dx * scale, y + dy * scale, dz * scale),
            0.12 * scale,
            "RK_MAT_Wood",
            coll,
            vertices=10,
            bevel_width=0.018,
        )
    cluster_points = [
        (-1.65, -0.25, 4.15, 2.35), (-0.65, 0.05, 4.65, 2.55),
        (0.65, -0.15, 4.75, 2.60), (1.55, 0.25, 4.15, 2.20),
        (-0.15, 0.45, 5.55, 2.25), (0.25, -0.45, 3.85, 2.30),
        (-1.15, 0.35, 5.25, 2.05), (1.15, -0.25, 5.35, 2.05),
    ]
    for idx, (dx, dy, dz, size) in enumerate(cluster_points):
        jitter = random.uniform(-0.10, 0.10)
        C.ico_sphere(
            f"{name}_Foliage_{idx:02d}",
            (x + dx * scale, y + dy * scale, (dz + jitter) * scale),
            (size * scale, size * 0.80 * scale, size * 0.80 * scale),
            colors[idx % len(colors)],
            coll,
            subdivisions=2,
        )


def cypress(name, x, y, height=6.0, material_name="RK_MAT_LeafGreen"):
    C.cylinder(f"{name}_Trunk", (x, y, height * 0.42), 0.18, height * 0.84, "RK_MAT_Wood", coll, vertices=12, bevel_width=0.02)
    for idx, (z, r) in enumerate(((1.5, 0.70), (2.7, 0.86), (3.9, 0.70), (5.0, 0.52), (5.8, 0.28))):
        C.cone(f"{name}_Tier_{idx:02d}", (x, y, z), r, r * 0.28, 2.1, material_name, coll, vertices=18, smooth_shading=True)


def planter(name, x, y, z=0.0, scale=1.0, flower="RK_MAT_FlowerBlue"):
    C.box(f"{name}_Plinth", (x, y, z + 0.36 * scale), (1.45 * scale, 1.20 * scale, 0.72 * scale), "RK_MAT_StoneWarm", coll, bevel_width=0.10 * scale)
    C.box(f"{name}_Lip", (x, y, z + 0.78 * scale), (1.72 * scale, 1.45 * scale, 0.20 * scale), "RK_MAT_StoneCream", coll, bevel_width=0.08 * scale)
    C.uv_sphere(f"{name}_Green", (x, y, z + 1.18 * scale), (1.65 * scale, 1.35 * scale, 1.0 * scale), "RK_MAT_LeafGreen", coll, segments=20, rings=12)
    for idx in range(8):
        angle = idx * math.tau / 8 + 0.2
        fx = x + math.cos(angle) * 0.64 * scale
        fy = y + math.sin(angle) * 0.50 * scale
        fz = z + (1.18 + 0.22 * (idx % 2)) * scale
        C.ico_sphere(f"{name}_Flower_{idx:02d}", (fx, fy, fz), (0.23 * scale,) * 3, flower if idx % 3 else "RK_MAT_FlowerCream", coll, subdivisions=1)
    # A few hanging vines over the front lip.
    for idx, dx in enumerate((-0.52, 0.0, 0.52)):
        C.bezier_curve(
            f"{name}_Vine_{idx:02d}",
            [(x + dx * scale, y - 0.65 * scale, z + 1.18 * scale), (x + dx * 1.1 * scale, y - 0.72 * scale, z + 0.55 * scale), (x + dx * 0.9 * scale, y - 0.66 * scale, z + 0.18 * scale)],
            0.055 * scale,
            "RK_MAT_LeafGreen",
            coll,
            bevel_resolution=2,
        )


def lamp(name, x, y, scale=1.0):
    C.cylinder(f"{name}_Base", (x, y, 0.28 * scale), 0.42 * scale, 0.56 * scale, "RK_MAT_Bronze", coll, vertices=16, bevel_width=0.05)
    C.cylinder(f"{name}_Post", (x, y, 2.20 * scale), 0.13 * scale, 3.9 * scale, "RK_MAT_BlackMetal", coll, vertices=16, bevel_width=0.025)
    C.torus(f"{name}_Collar", (x, y, 0.82 * scale), 0.24 * scale, 0.06 * scale, "RK_MAT_Gold", coll, major_segments=20, minor_segments=6)
    # Curled fantasy arm and dangling lantern.
    C.bezier_curve(
        f"{name}_ScrollArm",
        [(x, y, 4.0 * scale), (x + 0.50 * scale, y, 4.55 * scale), (x + 1.05 * scale, y, 4.25 * scale), (x + 0.82 * scale, y, 3.92 * scale)],
        0.095 * scale,
        "RK_MAT_BlackMetal",
        coll,
        bevel_resolution=3,
    )
    C.cylinder(f"{name}_Chain", (x + 0.82 * scale, y, 3.75 * scale), 0.025 * scale, 0.44 * scale, "RK_MAT_BlackMetal", coll, vertices=8, bevel_width=0)
    glow = C.ico_sphere(f"{name}_Glow", (x + 0.82 * scale, y, 3.28 * scale), (0.52 * scale, 0.42 * scale, 0.72 * scale), "RK_MAT_LanternGlow", coll, subdivisions=2)
    glow["light_anchor"] = True
    for idx, angle in enumerate((0, math.pi / 2, math.pi, 3 * math.pi / 2)):
        C.cylinder_between(
            f"{name}_Cage_{idx:02d}",
            (x + 0.82 * scale, y, 3.72 * scale),
            (x + 0.82 * scale + math.cos(angle) * 0.30 * scale, y + math.sin(angle) * 0.26 * scale, 2.90 * scale),
            0.025 * scale,
            "RK_MAT_Gold",
            coll,
            vertices=8,
            bevel_width=0.008,
        )


def bench(name, x, y, rotation=0.0):
    root = C.box(f"{name}_Seat", (x, y, 0.65), (2.7, 0.62, 0.20), "RK_MAT_Wood", coll, rotation=(0, 0, rotation), bevel_width=0.08)
    for idx, dx in enumerate((-1.05, 1.05)):
        local_x = x + math.cos(rotation) * dx
        local_y = y + math.sin(rotation) * dx
        C.box(f"{name}_Leg_{idx:02d}", (local_x, local_y, 0.35), (0.22, 0.50, 0.65), "RK_MAT_BlackMetal", coll, rotation=(0, 0, rotation), bevel_width=0.04)
    C.box(f"{name}_Back", (x, y + 0.28 * math.cos(rotation), 1.18), (2.75, 0.15, 0.82), "RK_MAT_Wood", coll, rotation=(0, 0, rotation), bevel_width=0.08)
    return root


def knight(name, x, y, facing=0.0, scale=1.0):
    # Simple but readable stylized guard silhouette from the references.
    C.cylinder(f"{name}_Torso", (x, y, 1.65 * scale), 0.42 * scale, 1.25 * scale, "RK_MAT_NavyLight", coll, vertices=12, bevel_width=0.05)
    C.uv_sphere(f"{name}_Helmet", (x, y, 2.55 * scale), (0.90 * scale, 0.78 * scale, 0.80 * scale), "RK_MAT_Silver", coll, segments=20, rings=12)
    C.box(f"{name}_Visor", (x, y - 0.41 * scale, 2.52 * scale), (0.76 * scale, 0.12 * scale, 0.24 * scale), "RK_MAT_BlackMetal", coll, bevel_width=0.05)
    C.cone(f"{name}_Plume", (x, y, 3.15 * scale), 0.22 * scale, 0.05 * scale, 0.72 * scale, "RK_MAT_RedBow", coll, vertices=12)
    for side, sign in (("L", -1), ("R", 1)):
        C.cylinder_between(f"{name}_Arm.{side}", (x + sign * 0.34 * scale, y, 2.0 * scale), (x + sign * 0.56 * scale, y - 0.05 * scale, 1.35 * scale), 0.13 * scale, "RK_MAT_Silver", coll, vertices=12)
        C.cylinder_between(f"{name}_Leg.{side}", (x + sign * 0.20 * scale, y, 1.05 * scale), (x + sign * 0.24 * scale, y, 0.28 * scale), 0.17 * scale, "RK_MAT_Silver", coll, vertices=12)
        C.box(f"{name}_Boot.{side}", (x + sign * 0.24 * scale, y - 0.08 * scale, 0.16 * scale), (0.36 * scale, 0.60 * scale, 0.30 * scale), "RK_MAT_BlackMetal", coll, bevel_width=0.08)
    spear_x = x + 0.72 * scale
    C.cylinder(f"{name}_SpearShaft", (spear_x, y, 1.85 * scale), 0.045 * scale, 3.7 * scale, "RK_MAT_BlackMetal", coll, vertices=10, bevel_width=0.01)
    C.cone(f"{name}_SpearTip", (spear_x, y, 3.95 * scale), 0.17 * scale, 0.02, 0.52 * scale, "RK_MAT_Silver", coll, vertices=8)


# Autumn tree rows and tall garden cypresses.
tree_specs = [
    ("RK_Tree_LeftFront", -13.5, -5.8, 1.05),
    ("RK_Tree_LeftMid", -14.2, 2.2, 1.18),
    ("RK_Tree_LeftBack", -12.6, 9.0, 0.98),
    ("RK_Tree_RightFront", 15.0, -5.5, 1.05),
    ("RK_Tree_RightMid", 17.0, 1.8, 1.10),
    ("RK_Tree_RightBack", 17.4, 8.8, 0.95),
]
for spec in tree_specs:
    tree(*spec)
for idx, (x, y) in enumerate(((3.1, 10.2), (5.0, 10.5), (11.0, 10.5), (12.8, 10.2))):
    cypress(f"RK_Cypress_{idx:02d}", x, y, height=6.2 - 0.2 * (idx % 2), material_name="RK_MAT_LeafGreen" if idx % 2 else "RK_MAT_LeafGold")

# Geometric hedges on raised sides.
for idx, (x, y, sx, sy) in enumerate((
    (-12.4, 5.1, 6.2, 1.2), (-10.5, 11.0, 5.0, 1.0),
    (13.7, 10.0, 5.5, 1.1), (14.2, -0.5, 3.2, 1.1),
    (-14.6, -0.8, 2.2, 5.2),
)):
    C.box(f"RK_Hedge_{idx:02d}", (x, y, 0.85), (sx, sy, 1.35), "RK_MAT_Hedge", coll, bevel_width=0.38)

# Planters placed along the gate and guild façade.
for idx, (x, y, flower) in enumerate((
    (-10.7, 3.9, "RK_MAT_FlowerBlue"), (-0.1, 3.9, "RK_MAT_FlowerPink"),
    (3.1, 6.0, "RK_MAT_FlowerCream"), (12.9, 6.0, "RK_MAT_FlowerBlue"),
    (15.0, -1.0, "RK_MAT_FlowerPink"), (-13.0, -1.2, "RK_MAT_FlowerCream"),
)):
    planter(f"RK_Planter_{idx:02d}", x, y, 0.0, 0.90 if idx > 3 else 1.0, flower)

# Eight curled lamps around the plaza plus two smaller approach lamps.
lamp_positions = [
    (-10.8, -6.5), (-10.8, 0.2), (-10.4, 6.0),
    (10.5, -6.5), (11.3, 0.0), (13.2, 6.6),
    (-3.8, 10.0), (3.1, 9.3),
]
for idx, (x, y) in enumerate(lamp_positions):
    lamp(f"RK_Lamp_{idx:02d}", x, y, 0.82 if idx >= 6 else 1.0)

bench("RK_Bench_Left", -9.0, 3.3, 0.0)
bench("RK_Bench_Right", 13.6, 2.5, 0.0)
bench("RK_Bench_Front", -6.5, -8.7, math.radians(8))

# Festival bunting stretching across the square.
for line_idx, (y, z, sag) in enumerate(((2.0, 6.2, 0.75), (7.2, 7.1, 0.55))):
    points = [(-13.5, y, z), (-6.8, y, z - sag), (0.0, y, z - sag * 1.2), (6.8, y, z - sag), (13.5, y, z)]
    C.bezier_curve(f"RK_BuntingCord_{line_idx:02d}", points, 0.025, "RK_MAT_BlackMetal", coll, bevel_resolution=2)
    for idx in range(13):
        x = -12.0 + idx * 2.0
        local_z = z - sag * (1.0 - abs(x) / 13.5)
        color = "RK_MAT_RedBow" if idx % 2 == 0 else "RK_MAT_StoneCream"
        C.box(f"RK_Bunting_{line_idx:02d}_{idx:02d}", (x, y, local_z - 0.47), (0.75, 0.08, 0.88), color, coll, rotation=(0, 0, 0.05 * math.sin(idx)), bevel_width=0.04)
        sigil = C.star(f"RK_BuntingSigil_{line_idx:02d}_{idx:02d}", (0, 0), 0, 0.19, 0.08, 4, 0.04, "RK_MAT_Gold", coll, rotation=math.pi / 4)
        sigil.location = (x, y - 0.07, local_z - 0.45)
        sigil.rotation_euler.x = math.pi / 2

# Guard pair on the gate stairs and two plaza sentries.
knight("RK_Guard_GateLeft", 3.3, 5.8, scale=0.86)
knight("RK_Guard_GateRight", 12.7, 5.8, scale=0.86)
knight("RK_Guard_PlazaLeft", -12.0, -2.2, scale=0.78)
knight("RK_Guard_PlazaRight", 14.0, 3.4, scale=0.78)

# Distant pale wizard statue and staff, as seen beyond the plaza.
C.cone("RK_Statue_Robe", (19.0, 10.0, 2.35), 1.35, 0.55, 4.6, "RK_MAT_White", coll, vertices=18, smooth_shading=True)
C.uv_sphere("RK_Statue_Head", (19.0, 10.0, 5.15), (1.10, 1.00, 1.18), "RK_MAT_White", coll, segments=24, rings=16)
C.cone("RK_Statue_Hat", (19.0, 10.0, 6.3), 0.85, 0.05, 2.1, "RK_MAT_White", coll, vertices=18)
C.cylinder("RK_Statue_Staff", (20.2, 10.0, 3.8), 0.08, 5.8, "RK_MAT_Gold", coll, vertices=12, bevel_width=0.02)
C.star("RK_Statue_StaffStar", (0, 0), 0, 0.55, 0.20, 6, 0.10, "RK_MAT_Gold", coll, rotation=math.pi / 6).location = (20.2, 9.92, 6.85)
bpy.data.objects["RK_Statue_StaffStar"].rotation_euler.x = math.pi / 2

# Cyan firefly motes scattered high against the night sky.
for idx in range(18):
    x = random.uniform(-15.0, 18.0)
    y = random.uniform(2.0, 16.0)
    z = random.uniform(6.0, 15.0)
    size = random.uniform(0.05, 0.13)
    C.ico_sphere(f"RK_SkyMote_{idx:02d}", (x, y, z), (size, size, size), "RK_MAT_SpriteGlow", coll, subdivisions=1)

C.save_mainfile()
C.scene_summary("03_environment")

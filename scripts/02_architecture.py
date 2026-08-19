"""Construct the warm guild hall, castle gate, towers and background façades."""

from pathlib import Path
import math
import sys

import bpy


ROOT = Path(r"C:\Users\Eser\Documents\Code\rock_kingdom_blender_scene")
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import common as C


coll = bpy.data.collections["RK_ARCHITECTURE"]
for obj in list(coll.objects):
    bpy.data.objects.remove(obj, do_unlink=True)


def band(name, location, dimensions, material="RK_MAT_StoneCream", bevel=0.04):
    return C.box(name, location, dimensions, material, coll, bevel_width=bevel)


def column(name, x, y, base_z, height, radius=0.34):
    C.cylinder(f"{name}_Shaft", (x, y, base_z + height / 2), radius, height, "RK_MAT_StoneCream", coll, vertices=20, bevel_width=0.025, smooth_shading=True)
    C.cylinder(f"{name}_Base", (x, y, base_z + 0.15), radius * 1.35, 0.30, "RK_MAT_StoneWarm", coll, vertices=20, bevel_width=0.05)
    C.cylinder(f"{name}_Capital", (x, y, base_z + height - 0.13), radius * 1.45, 0.34, "RK_MAT_StoneCream", coll, vertices=20, bevel_width=0.05)
    C.torus(f"{name}_Ring", (x, y, base_z + height - 0.38), radius * 1.02, 0.055, "RK_MAT_Gold", coll, rotation=(math.pi / 2, 0, 0), major_segments=20, minor_segments=6)


def front_window(name, x, y, z, width=1.05, height=1.55, glow=True):
    frame_mat = "RK_MAT_StoneCream"
    pane_mat = "RK_MAT_WindowGlow" if glow else "RK_MAT_Window"
    C.box(f"{name}_Pane", (x, y, z), (width, 0.11, height), pane_mat, coll, bevel_width=0.05)
    frame = 0.11
    C.box(f"{name}_FrameL", (x - width / 2 - frame / 2, y - 0.02, z), (frame, 0.16, height + 0.24), frame_mat, coll, bevel_width=0.025)
    C.box(f"{name}_FrameR", (x + width / 2 + frame / 2, y - 0.02, z), (frame, 0.16, height + 0.24), frame_mat, coll, bevel_width=0.025)
    C.box(f"{name}_FrameT", (x, y - 0.02, z + height / 2 + frame / 2), (width + 0.32, 0.16, frame), frame_mat, coll, bevel_width=0.025)
    C.box(f"{name}_FrameB", (x, y - 0.02, z - height / 2 - frame / 2), (width + 0.32, 0.16, frame), frame_mat, coll, bevel_width=0.025)
    C.box(f"{name}_MullionV", (x, y - 0.08, z), (0.07, 0.09, height), frame_mat, coll, bevel_width=0.01)
    C.box(f"{name}_MullionH", (x, y - 0.08, z), (width, 0.09, 0.07), frame_mat, coll, bevel_width=0.01)


def arched_door(name, x, y, z, width=1.65, height=2.6):
    C.box(f"{name}_Door", (x, y, z + height / 2), (width, 0.18, height), "RK_MAT_Wood", coll, bevel_width=0.12)
    C.arch_ring(f"{name}_Arch", (x, y - 0.08, z + height - width * 0.34), width * 0.55, 0.23, 0.28, "RK_MAT_StoneCream", coll, segments=18)
    C.box(f"{name}_Threshold", (x, y - 0.12, z + 0.08), (width + 0.45, 0.35, 0.18), "RK_MAT_StoneWarm", coll, bevel_width=0.04)
    C.star(f"{name}_Emblem", (0, 0), 0, 0.32, 0.14, 4, 0.08, "RK_MAT_Gold", coll, rotation=math.pi / 4).rotation_euler.x = math.pi / 2
    emblem = bpy.context.view_layer.objects.active


def battlement_wall(name, center, dimensions, merlons, material="RK_MAT_StoneCream"):
    x, y, z = center
    sx, sy, sz = dimensions
    C.box(f"{name}_Body", center, dimensions, material, coll, bevel_width=0.09)
    C.box(f"{name}_Band", (x, y - sy * 0.02, z + sz / 2 - 0.35), (sx + 0.18, sy + 0.14, 0.30), "RK_MAT_RoofRed", coll, bevel_width=0.04)
    step = sx / merlons
    for i in range(merlons):
        mx = x - sx / 2 + step * (i + 0.5)
        C.box(f"{name}_Merlon_{i:02d}", (mx, y, z + sz / 2 + 0.36), (step * 0.58, sy, 0.72), material, coll, bevel_width=0.05)


def tower(name, x, y, height=10.2, radius=2.05):
    C.cylinder(f"{name}_Body", (x, y, height / 2), radius, height, "RK_MAT_StoneCream", coll, vertices=12, bevel_width=0.08)
    C.cylinder(f"{name}_Plinth", (x, y, 0.45), radius * 1.12, 0.9, "RK_MAT_StoneWarm", coll, vertices=12, bevel_width=0.08)
    C.cylinder(f"{name}_UpperBand", (x, y, height - 1.25), radius * 1.10, 0.35, "RK_MAT_RoofRed", coll, vertices=12, bevel_width=0.03)
    C.cylinder(f"{name}_Crown", (x, y, height - 0.42), radius * 1.16, 0.55, "RK_MAT_StoneCream", coll, vertices=12, bevel_width=0.08)
    for i in range(8):
        angle = i * math.tau / 8
        C.box(
            f"{name}_Merlon_{i:02d}",
            (x + math.cos(angle) * radius * 0.92, y + math.sin(angle) * radius * 0.92, height + 0.18),
            (0.62, 0.62, 0.82),
            "RK_MAT_StoneCream",
            coll,
            rotation=(0, 0, angle),
            bevel_width=0.05,
        )
    # Arrow slit and vertical red-gold banner on the front side.
    C.box(f"{name}_ArrowSlit", (x, y - radius - 0.03, height * 0.56), (0.20, 0.08, 0.78), "RK_MAT_StoneDark", coll, bevel_width=0.06)
    C.box(f"{name}_Banner", (x, y - radius - 0.10, height * 0.70), (0.92, 0.08, 3.4), "RK_MAT_RedBow", coll, bevel_width=0.04)
    sigil = C.star(f"{name}_BannerSigil", (0, 0), 0, 0.28, 0.13, 4, 0.06, "RK_MAT_Gold", coll, rotation=math.pi / 4)
    sigil.location = (x, y - radius - 0.17, height * 0.72)
    sigil.rotation_euler.x = math.pi / 2


# ---------------------------------------------------------------------------
# Warm guild hall / academy façade (left and center background)
# ---------------------------------------------------------------------------

C.box("RK_GuildHall_Main", (-5.2, 8.3, 3.25), (12.2, 5.5, 6.2), "RK_MAT_PlasterOrange", coll, bevel_width=0.16)
C.box("RK_GuildHall_Base", (-5.2, 8.3, 0.55), (12.7, 5.8, 0.85), "RK_MAT_StoneWarm", coll, bevel_width=0.12)
band("RK_GuildHall_TrimLow", (-5.2, 5.48, 1.0), (12.5, 0.24, 0.30))
band("RK_GuildHall_TrimMid", (-5.2, 5.48, 3.45), (12.5, 0.28, 0.28))
band("RK_GuildHall_TrimTop", (-5.2, 5.48, 6.12), (12.7, 0.32, 0.38))
C.roof_prism("RK_GuildHall_Roof", (-5.2, 8.35, 6.15), 13.1, 6.4, 3.1, "RK_MAT_RoofRed", coll)
C.box("RK_GuildHall_Ridge", (-5.2, 8.35, 9.28), (0.28, 6.7, 0.28), "RK_MAT_RoofHighlight", coll, bevel_width=0.05)

# Entry porch with classical columns and a shallow pediment.
C.box("RK_GuildHall_PorchRoof", (-5.2, 4.65, 4.35), (11.8, 1.75, 0.46), "RK_MAT_StoneCream", coll, bevel_width=0.10)
C.roof_prism("RK_GuildHall_PorchPediment", (-5.2, 4.55, 4.58), 11.9, 1.75, 1.35, "RK_MAT_StoneCream", coll)
for idx, x in enumerate((-9.7, -6.7, -3.7, -0.7)):
    column(f"RK_GuildHall_Column_{idx:02d}", x, 4.25, 0.35, 4.05, radius=0.37)

# Glowing front windows, main door and side door.
for idx, x in enumerate((-9.1, -7.0, -3.4, -1.25)):
    front_window(f"RK_GuildHall_WindowLower_{idx:02d}", x, 5.42, 2.18, 1.08, 1.45, glow=True)
for idx, x in enumerate((-8.8, -6.0, -3.2, -0.5)):
    front_window(f"RK_GuildHall_WindowUpper_{idx:02d}", x, 5.42, 4.65, 1.12, 1.55, glow=True)
C.box("RK_GuildHall_Door", (-5.2, 5.34, 1.65), (1.72, 0.24, 2.85), "RK_MAT_Wood", coll, bevel_width=0.14)
C.arch_ring("RK_GuildHall_DoorArch", (-5.2, 5.28, 2.72), 1.06, 0.24, 0.30, "RK_MAT_StoneCream", coll, segments=20)
C.box("RK_GuildHall_DoorMullion", (-5.2, 5.18, 1.70), (0.10, 0.13, 2.40), "RK_MAT_Gold", coll, bevel_width=0.02)
door_sigil = C.star("RK_GuildHall_DoorSigil", (0, 0), 0, 0.43, 0.18, 4, 0.08, "RK_MAT_Gold", coll, rotation=math.pi / 4)
door_sigil.location = (-5.2, 5.06, 2.0)
door_sigil.rotation_euler.x = math.pi / 2

# Tall right wing and turret reproduce the reference's asymmetric roofline.
C.box("RK_GuildHall_TowerWing", (1.55, 8.6, 4.35), (4.2, 5.0, 8.4), "RK_MAT_PlasterGold", coll, bevel_width=0.16)
band("RK_GuildHall_TowerWingBand", (1.55, 6.05, 4.65), (4.45, 0.30, 0.32))
for level, z in enumerate((2.25, 5.25)):
    front_window(f"RK_GuildHall_TowerWindow_{level:02d}", 1.55, 6.02, z, 0.96, 1.42, glow=True)
C.roof_prism("RK_GuildHall_TowerRoof", (1.55, 8.60, 8.48), 4.8, 5.5, 3.6, "RK_MAT_RoofRed", coll)
C.cone("RK_GuildHall_TurretRoof", (2.95, 7.35, 10.5), 1.25, 0.08, 3.8, "RK_MAT_RoofHighlight", coll, vertices=20)
C.cylinder("RK_GuildHall_TurretFinial", (2.95, 7.35, 12.65), 0.12, 0.75, "RK_MAT_Gold", coll, vertices=12, bevel_width=0.02)
C.ico_sphere("RK_GuildHall_TurretGem", (2.95, 7.35, 13.08), (0.40, 0.40, 0.50), "RK_MAT_SpriteGlow", coll, subdivisions=1)

# Dormers and chimneys.
for idx, x in enumerate((-8.0, -4.9, -1.9)):
    C.box(f"RK_GuildHall_Dormer_{idx:02d}", (x, 5.83, 7.12), (1.35, 0.70, 1.70), "RK_MAT_PlasterGold", coll, bevel_width=0.08)
    C.roof_prism(f"RK_GuildHall_DormerRoof_{idx:02d}", (x, 5.80, 7.95), 1.70, 1.05, 0.95, "RK_MAT_RoofHighlight", coll)
    front_window(f"RK_GuildHall_DormerWindow_{idx:02d}", x, 5.43, 7.08, 0.60, 0.90, glow=True)
for idx, x in enumerate((-9.2, -2.0)):
    C.box(f"RK_GuildHall_Chimney_{idx:02d}", (x, 9.0, 9.0), (0.70, 0.85, 2.0), "RK_MAT_StoneCream", coll, bevel_width=0.08)
    C.box(f"RK_GuildHall_ChimneyCap_{idx:02d}", (x, 9.0, 10.03), (0.95, 1.10, 0.24), "RK_MAT_StoneWarm", coll, bevel_width=0.05)


# ---------------------------------------------------------------------------
# Cream castle gate, towers and enclosing walls (rear/right)
# ---------------------------------------------------------------------------

gate_x = 8.0
C.box("RK_CastleGate_Main", (gate_x, 12.0, 8.35), (10.5, 2.4, 3.2), "RK_MAT_StoneCream", coll, bevel_width=0.12)
C.box("RK_CastleGate_LeftPier", (gate_x - 4.45, 11.5, 4.1), (2.15, 3.4, 8.0), "RK_MAT_StoneCream", coll, bevel_width=0.12)
C.box("RK_CastleGate_RightPier", (gate_x + 4.45, 11.5, 4.1), (2.15, 3.4, 8.0), "RK_MAT_StoneCream", coll, bevel_width=0.12)
C.box("RK_CastleGate_Opening", (gate_x, 10.92, 3.25), (6.7, 0.20, 6.3), "RK_MAT_StoneDark", coll, bevel_width=0.02)
C.arch_ring("RK_CastleGate_Arch", (gate_x, 10.70, 3.25), 3.35, 0.62, 0.72, "RK_MAT_StoneCream", coll, segments=30)
for side, x in (("L", gate_x - 3.66), ("R", gate_x + 3.66)):
    C.box(f"RK_CastleGate_ArchLeg_{side}", (x, 10.70, 1.75), (0.62, 0.72, 3.5), "RK_MAT_StoneCream", coll, bevel_width=0.05)
band("RK_CastleGate_TopBand", (gate_x, 10.72, 8.98), (10.8, 0.62, 0.40), "RK_MAT_RoofRed")
for i in range(9):
    x = gate_x - 4.55 + i * 1.14
    C.box(f"RK_CastleGate_Merlon_{i:02d}", (x, 11.65, 10.32), (0.70, 1.25, 0.86), "RK_MAT_StoneCream", coll, bevel_width=0.06)

# Gate crest and suspended red-gold banners.
C.star("RK_CastleGate_CrestBack", (0, 0), 0, 1.35, 0.58, 6, 0.18, "RK_MAT_Bronze", coll, rotation=math.pi / 6).location = (gate_x, 10.45, 9.18)
crest = bpy.data.objects["RK_CastleGate_CrestBack"]
crest.rotation_euler.x = math.pi / 2
C.star("RK_CastleGate_CrestGold", (0, 0), 0, 0.84, 0.36, 6, 0.20, "RK_MAT_Gold", coll, rotation=math.pi / 6).location = (gate_x, 10.32, 9.20)
bpy.data.objects["RK_CastleGate_CrestGold"].rotation_euler.x = math.pi / 2
for idx, x in enumerate((gate_x - 2.15, gate_x + 2.15)):
    C.box(f"RK_CastleGate_Banner_{idx:02d}", (x, 10.47, 7.35), (1.25, 0.10, 3.70), "RK_MAT_RedBow", coll, bevel_width=0.05)
    sigil = C.star(f"RK_CastleGate_BannerSigil_{idx:02d}", (0, 0), 0, 0.38, 0.17, 4, 0.07, "RK_MAT_Gold", coll, rotation=math.pi / 4)
    sigil.location = (x, 10.35, 7.55)
    sigil.rotation_euler.x = math.pi / 2

# Grand approach steps and red carpet.
for i in range(9):
    y = 6.75 + i * 0.48
    z = 0.18 + i * 0.20
    depth = 0.54
    C.box(f"RK_CastleGate_Step_{i:02d}", (gate_x, y, z), (8.6, depth, 0.40), "RK_MAT_StoneCream", coll, bevel_width=0.04)
    C.box(f"RK_CastleGate_Carpet_{i:02d}", (gate_x, y - 0.02, z + 0.215), (3.15, depth * 0.92, 0.06), "RK_MAT_RedBow", coll, bevel_width=0.02)

tower("RK_CastleTower_Left", 1.25, 13.2, 11.2, 2.15)
tower("RK_CastleTower_Right", 14.75, 13.2, 11.2, 2.15)
battlement_wall("RK_CastleWall_Left", (-12.8, 13.1, 4.1), (10.0, 2.6, 7.6), 8)
battlement_wall("RK_CastleWall_Right", (20.2, 13.1, 4.1), (8.7, 2.6, 7.6), 7)

# Receding towers visible between roofs.
for idx, (x, y, scale) in enumerate(((-10.5, 17.2, 0.75), (-3.0, 17.8, 0.62), (20.5, 17.5, 0.68))):
    C.cylinder(f"RK_BackgroundTower_{idx:02d}", (x, y, 4.5 * scale), 2.2 * scale, 9.0 * scale, "RK_MAT_StoneCream", coll, vertices=10, bevel_width=0.07)
    C.cylinder(f"RK_BackgroundTowerBand_{idx:02d}", (x, y, 7.5 * scale), 2.38 * scale, 0.34, "RK_MAT_RoofRed", coll, vertices=10, bevel_width=0.03)

# Right-hand boutique façade balances the guild hall and echoes its red roof.
C.box("RK_Boutique_Main", (15.2, 5.7, 3.05), (7.5, 4.4, 5.7), "RK_MAT_PlasterGold", coll, bevel_width=0.14)
C.roof_prism("RK_Boutique_Roof", (15.2, 5.8, 5.83), 8.2, 5.0, 2.7, "RK_MAT_RoofRed", coll)
band("RK_Boutique_Trim", (15.2, 3.43, 3.55), (7.8, 0.25, 0.28))
for idx, x in enumerate((12.7, 15.2, 17.7)):
    front_window(f"RK_Boutique_Window_{idx:02d}", x, 3.44, 2.45, 1.25, 1.70, glow=True)
C.box("RK_Boutique_Door", (15.2, 3.35, 1.40), (1.45, 0.22, 2.55), "RK_MAT_Wood", coll, bevel_width=0.12)

C.save_mainfile()
C.scene_summary("02_architecture")

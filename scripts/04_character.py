"""Build the detailed central chibi heroine, armature, companion and sprite."""

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

hero_coll = bpy.data.collections["RK_HERO_CHARACTER"]
pet_coll = bpy.data.collections["RK_COMPANION"]
for target_coll in (hero_coll, pet_coll):
    for obj in list(target_coll.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def tag(obj, role):
    obj["rk_role"] = role
    obj["source"] = "six_reference_images"
    return obj


def face_curve(name, points, depth, material="RK_MAT_EyeBlack"):
    return tag(C.bezier_curve(name, points, depth, material, hero_coll, bevel_resolution=3), "face_detail")


hero_x = 0.75
hero_y = -4.15

# ---------------------------------------------------------------------------
# Semantic armature and root hierarchy
# ---------------------------------------------------------------------------

root = bpy.data.objects.new("RK_Hero_Root", None)
hero_coll.objects.link(root)
root.location = (hero_x, hero_y, 0.0)
root["asset_role"] = "hero_root"

arm_data = bpy.data.armatures.new("RK_Hero_Armature_Data")
armature = bpy.data.objects.new("RK_Hero_Armature", arm_data)
hero_coll.objects.link(armature)
armature.parent = root
armature.location = (0.0, 0.0, 0.0)
armature.show_in_front = True
armature.display_type = "WIRE"
armature["rig_type"] = "editable_display_rig"

bpy.ops.object.select_all(action="DESELECT")
armature.select_set(True)
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode="EDIT")


def bone(name, head, tail, parent_name=None):
    b = arm_data.edit_bones.new(name)
    b.head = head
    b.tail = tail
    if parent_name:
        b.parent = arm_data.edit_bones.get(parent_name)
    return b


bone("root", (0, 0, 0), (0, 0, 0.55))
bone("pelvis", (0, 0, 0.55), (0, 0, 2.25), "root")
bone("spine", (0, 0, 2.25), (0, 0, 3.35), "pelvis")
bone("neck", (0, 0, 3.35), (0, 0, 3.72), "spine")
bone("head", (0, 0, 3.72), (0, 0, 5.35), "neck")
bone("upper_arm.L", (0, 0, 3.22), (-0.68, -0.02, 2.76), "spine")
bone("forearm.L", (-0.68, -0.02, 2.76), (-0.70, -0.10, 1.95), "upper_arm.L")
bone("upper_arm.R", (0, 0, 3.22), (0.72, -0.05, 2.68), "spine")
bone("forearm.R", (0.72, -0.05, 2.68), (0.64, -0.12, 1.86), "upper_arm.R")
bone("thigh.L", (-0.24, 0, 2.20), (-0.29, 0, 1.30), "pelvis")
bone("shin.L", (-0.29, 0, 1.30), (-0.32, -0.03, 0.38), "thigh.L")
bone("thigh.R", (0.24, 0, 2.20), (0.30, 0, 1.28), "pelvis")
bone("shin.R", (0.30, 0, 1.28), (0.38, -0.02, 0.38), "thigh.R")
bpy.ops.object.mode_set(mode="OBJECT")


# Remember every geometry object created after this point for armature parenting.
hero_geometry_start = set(hero_coll.objects)

# ---------------------------------------------------------------------------
# Anatomy, expressive face and pointed ears
# ---------------------------------------------------------------------------

head = tag(
    C.uv_sphere(
        "RK_Hero_Head",
        (hero_x, hero_y, 4.35),
        (1.62, 1.32, 1.72),
        "RK_MAT_Skin",
        hero_coll,
        segments=48,
        rings=32,
    ),
    "hero_head",
)
head["detail_level"] = "hero"
head["reference_priority"] = "face_hair_costume"

# Ears are elongated cones pointing outward, preserving the reference silhouette.
tag(C.cone("RK_Hero_Ear.L", (hero_x - 0.91, hero_y - 0.01, 4.38), 0.30, 0.015, 0.78, "RK_MAT_Skin", hero_coll, vertices=24, rotation=(0, -math.pi / 2, 0), smooth_shading=True), "anatomy")
tag(C.cone("RK_Hero_Ear.R", (hero_x + 0.91, hero_y - 0.01, 4.38), 0.30, 0.015, 0.78, "RK_MAT_Skin", hero_coll, vertices=24, rotation=(0, math.pi / 2, 0), smooth_shading=True), "anatomy")
C.cone("RK_Hero_EarInner.L", (hero_x - 0.96, hero_y - 0.18, 4.38), 0.13, 0.01, 0.48, "RK_MAT_SkinWarm", hero_coll, vertices=18, rotation=(0, -math.pi / 2, 0), smooth_shading=True)
C.cone("RK_Hero_EarInner.R", (hero_x + 0.96, hero_y - 0.18, 4.38), 0.13, 0.01, 0.48, "RK_MAT_SkinWarm", hero_coll, vertices=18, rotation=(0, math.pi / 2, 0), smooth_shading=True)

eye_specs = (("L", -0.34), ("R", 0.34))
for side, dx in eye_specs:
    eye = tag(C.uv_sphere(f"RK_Hero_Eye.{side}", (hero_x + dx, hero_y - 0.642, 4.42), (0.43, 0.10, 0.52), "RK_MAT_White", hero_coll, segments=32, rings=20), "eye_white")
    iris = tag(C.uv_sphere(f"RK_Hero_Iris.{side}", (hero_x + dx, hero_y - 0.700, 4.40), (0.275, 0.055, 0.36), "RK_MAT_EyeViolet", hero_coll, segments=28, rings=18), "iris")
    pupil = tag(C.uv_sphere(f"RK_Hero_Pupil.{side}", (hero_x + dx, hero_y - 0.735, 4.40), (0.13, 0.035, 0.22), "RK_MAT_EyeBlack", hero_coll, segments=24, rings=16), "pupil")
    C.uv_sphere(f"RK_Hero_EyeHighlightBig.{side}", (hero_x + dx - 0.055, hero_y - 0.758, 4.50), (0.075, 0.025, 0.095), "RK_MAT_White", hero_coll, segments=18, rings=12)
    C.uv_sphere(f"RK_Hero_EyeHighlightSmall.{side}", (hero_x + dx + 0.060, hero_y - 0.760, 4.33), (0.035, 0.018, 0.045), "RK_MAT_White", hero_coll, segments=14, rings=10)
    lash_sign = -1 if side == "L" else 1
    face_curve(
        f"RK_Hero_Lash.{side}",
        [
            (hero_x + dx - 0.21, hero_y - 0.744, 4.56),
            (hero_x + dx, hero_y - 0.770, 4.67),
            (hero_x + dx + 0.22, hero_y - 0.744, 4.55),
        ],
        0.026,
    )
    for lash_idx in range(2):
        lx = hero_x + dx + lash_sign * (0.20 + lash_idx * 0.055)
        face_curve(
            f"RK_Hero_LashTip.{side}.{lash_idx}",
            [(lx, hero_y - 0.744, 4.54), (lx + lash_sign * 0.09, hero_y - 0.746, 4.64 + lash_idx * 0.025)],
            0.018,
        )

# Brows, nose, smile and blush.
face_curve("RK_Hero_Brow.L", [(hero_x - 0.53, hero_y - 0.690, 4.80), (hero_x - 0.33, hero_y - 0.725, 4.86), (hero_x - 0.14, hero_y - 0.696, 4.82)], 0.026, "RK_MAT_HairLavender")
face_curve("RK_Hero_Brow.R", [(hero_x + 0.14, hero_y - 0.696, 4.82), (hero_x + 0.33, hero_y - 0.725, 4.86), (hero_x + 0.53, hero_y - 0.690, 4.80)], 0.026, "RK_MAT_HairLavender")
C.uv_sphere("RK_Hero_Nose", (hero_x, hero_y - 0.760, 4.14), (0.08, 0.055, 0.07), "RK_MAT_SkinWarm", hero_coll, segments=16, rings=10)
face_curve("RK_Hero_Mouth", [(hero_x - 0.14, hero_y - 0.754, 4.00), (hero_x, hero_y - 0.785, 3.95), (hero_x + 0.15, hero_y - 0.754, 4.01)], 0.023, "RK_MAT_RedBow")
C.uv_sphere("RK_Hero_Blush.L", (hero_x - 0.61, hero_y - 0.654, 4.08), (0.23, 0.045, 0.10), "RK_MAT_SkinWarm", hero_coll, segments=20, rings=12)
C.uv_sphere("RK_Hero_Blush.R", (hero_x + 0.61, hero_y - 0.654, 4.08), (0.23, 0.045, 0.10), "RK_MAT_SkinWarm", hero_coll, segments=20, rings=12)

# ---------------------------------------------------------------------------
# Hair cap, bangs, long locks, large bow and small crown
# ---------------------------------------------------------------------------

tag(C.uv_sphere("RK_Hero_HairCap", (hero_x, hero_y + 0.10, 4.55), (1.78, 1.43, 1.82), "RK_MAT_HairCyan", hero_coll, segments=40, rings=28), "hair_base")

hair_paths = [
    # Forehead bangs.
    [(-0.55, -0.58, 5.08), (-0.52, -0.72, 4.82), (-0.43, -0.76, 4.58)],
    [(-0.30, -0.67, 5.18), (-0.24, -0.78, 4.86), (-0.20, -0.78, 4.55)],
    [(0.00, -0.70, 5.22), (0.04, -0.81, 4.91), (0.10, -0.79, 4.62)],
    [(0.30, -0.67, 5.18), (0.28, -0.78, 4.86), (0.25, -0.78, 4.55)],
    [(0.56, -0.57, 5.06), (0.55, -0.70, 4.79), (0.47, -0.75, 4.54)],
    # Side and back locks.
    [(-0.72, -0.40, 4.92), (-0.93, -0.10, 4.38), (-0.84, -0.16, 3.52)],
    [(-0.80, -0.12, 4.84), (-1.00, 0.05, 4.10), (-0.72, 0.02, 3.26)],
    [(-0.66, 0.24, 4.90), (-0.72, 0.48, 4.03), (-0.52, 0.35, 3.25)],
    [(-0.40, 0.48, 5.05), (-0.44, 0.66, 4.12), (-0.32, 0.54, 3.18)],
    [(-0.13, 0.58, 5.14), (-0.15, 0.72, 4.20), (-0.10, 0.62, 3.16)],
    [(0.15, 0.58, 5.14), (0.18, 0.72, 4.18), (0.12, 0.62, 3.15)],
    [(0.42, 0.48, 5.05), (0.47, 0.66, 4.10), (0.36, 0.54, 3.18)],
    [(0.68, 0.24, 4.90), (0.76, 0.48, 4.03), (0.57, 0.35, 3.25)],
    [(0.82, -0.10, 4.84), (1.00, 0.05, 4.10), (0.78, 0.02, 3.30)],
    [(0.73, -0.40, 4.92), (0.94, -0.10, 4.38), (0.86, -0.16, 3.55)],
    # Two extra curled front-side locks.
    [(-0.64, -0.57, 4.75), (-0.83, -0.62, 4.15), (-0.62, -0.68, 3.72)],
    [(0.64, -0.57, 4.75), (0.83, -0.62, 4.15), (0.63, -0.68, 3.72)],
    [(0.00, 0.62, 4.78), (-0.12, 0.78, 3.90), (0.02, 0.69, 3.08)],
]

for idx, local_points in enumerate(hair_paths):
    points = [(hero_x + x, hero_y + y, z) for x, y, z in local_points]
    depth = 0.115 if idx < 5 else 0.145
    material_name = "RK_MAT_HairCyan" if idx % 4 else "RK_MAT_HairLavender"
    lock = tag(C.bezier_curve(f"RK_Hero_HairLock_{idx:02d}", points, depth, material_name, hero_coll, bevel_resolution=4), "hair_lock")
    end = points[-1]
    C.uv_sphere(f"RK_Hero_HairTip_{idx:02d}", end, (depth * 2.0, depth * 1.8, depth * 2.4), "RK_MAT_HairLavender", hero_coll, segments=18, rings=12)

# Crown curl and small decorative hair bead.
C.bezier_curve(
    "RK_Hero_HairCurl",
    [(hero_x + 0.05, hero_y + 0.25, 5.25), (hero_x - 0.12, hero_y + 0.12, 5.58), (hero_x + 0.16, hero_y - 0.02, 5.72), (hero_x + 0.25, hero_y + 0.08, 5.50)],
    0.09,
    "RK_MAT_HairCyan",
    hero_coll,
    bevel_resolution=4,
)
C.ico_sphere("RK_Hero_HairBead", (hero_x + 0.23, hero_y + 0.04, 5.49), (0.17, 0.17, 0.17), "RK_MAT_Gold", hero_coll, subdivisions=2)

# Large red bow is deliberately broad so it reads in the wide shot.
C.uv_sphere("RK_Hero_Bow_Lobe.L", (hero_x - 0.55, hero_y + 0.34, 5.32), (0.92, 0.28, 0.62), "RK_MAT_RedBow", hero_coll, segments=28, rings=18, rotation=(0, 0, math.radians(-18)))
C.uv_sphere("RK_Hero_Bow_Lobe.R", (hero_x + 0.55, hero_y + 0.34, 5.32), (0.92, 0.28, 0.62), "RK_MAT_RedBow", hero_coll, segments=28, rings=18, rotation=(0, 0, math.radians(18)))
tag(C.uv_sphere("RK_Hero_Bow_Center", (hero_x, hero_y + 0.18, 5.32), (0.42, 0.34, 0.42), "RK_MAT_RedBow", hero_coll, segments=28, rings=18), "bow_center")
C.bezier_curve("RK_Hero_BowTail.L", [(hero_x - 0.20, hero_y + 0.36, 5.20), (hero_x - 0.48, hero_y + 0.40, 4.88), (hero_x - 0.62, hero_y + 0.34, 4.58)], 0.12, "RK_MAT_RedBow", hero_coll, bevel_resolution=3)
C.bezier_curve("RK_Hero_BowTail.R", [(hero_x + 0.20, hero_y + 0.36, 5.20), (hero_x + 0.48, hero_y + 0.40, 4.88), (hero_x + 0.62, hero_y + 0.34, 4.58)], 0.12, "RK_MAT_RedBow", hero_coll, bevel_resolution=3)

# Silver mini-crown with cyan jewel and gold ring.
tag(C.cylinder("RK_Hero_Crown", (hero_x, hero_y - 0.08, 5.55), 0.28, 0.16, "RK_MAT_Silver", hero_coll, vertices=20, bevel_width=0.03), "crown")
for idx, dx in enumerate((-0.20, 0.0, 0.20)):
    C.cone(f"RK_Hero_CrownPoint_{idx:02d}", (hero_x + dx, hero_y - 0.08, 5.74 + 0.06 * (idx == 1)), 0.10, 0.01, 0.42, "RK_MAT_Silver", hero_coll, vertices=12)
C.ico_sphere("RK_Hero_CrownGem", (hero_x, hero_y - 0.32, 5.60), (0.17, 0.10, 0.22), "RK_MAT_SpriteGlow", hero_coll, subdivisions=2)
C.torus("RK_Hero_CrownBand", (hero_x, hero_y - 0.08, 5.48), 0.28, 0.035, "RK_MAT_Gold", hero_coll, major_segments=24, minor_segments=6)

# ---------------------------------------------------------------------------
# Neck, torso, layered costume, arms and gloves
# ---------------------------------------------------------------------------

C.cylinder("RK_Hero_Neck", (hero_x, hero_y, 3.54), 0.22, 0.38, "RK_MAT_Skin", hero_coll, vertices=24, bevel_width=0.02, smooth_shading=True)
C.torus("RK_Hero_Choker", (hero_x, hero_y, 3.45), 0.245, 0.055, "RK_MAT_Navy", hero_coll, major_segments=28, minor_segments=8)
C.ico_sphere("RK_Hero_ChokerGem", (hero_x, hero_y - 0.255, 3.43), (0.18, 0.10, 0.22), "RK_MAT_SpriteGlow", hero_coll, subdivisions=2)

tag(C.uv_sphere("RK_Hero_Torso", (hero_x, hero_y, 2.83), (0.98, 0.66, 1.22), "RK_MAT_Navy", hero_coll, segments=32, rings=20), "torso")
C.uv_sphere("RK_Hero_BodiceWhite", (hero_x, hero_y - 0.34, 3.00), (0.78, 0.20, 0.72), "RK_MAT_White", hero_coll, segments=28, rings=18)
C.box("RK_Hero_WaistCorset", (hero_x, hero_y - 0.05, 2.48), (0.90, 0.62, 0.38), "RK_MAT_Leather", hero_coll, bevel_width=0.10)
C.box("RK_Hero_Belt", (hero_x, hero_y - 0.36, 2.40), (1.08, 0.16, 0.18), "RK_MAT_Leather", hero_coll, bevel_width=0.05)
C.box("RK_Hero_BeltBuckle", (hero_x, hero_y - 0.48, 2.40), (0.28, 0.10, 0.25), "RK_MAT_Gold", hero_coll, bevel_width=0.05)
C.ico_sphere("RK_Hero_BeltGem", (hero_x, hero_y - 0.56, 2.40), (0.12, 0.07, 0.15), "RK_MAT_SpriteGlow", hero_coll, subdivisions=1)

# Cross-body leather straps.
C.bezier_curve("RK_Hero_Strap_A", [(hero_x - 0.40, hero_y - 0.47, 3.28), (hero_x, hero_y - 0.51, 2.86), (hero_x + 0.42, hero_y - 0.47, 2.48)], 0.065, "RK_MAT_Leather", hero_coll, bevel_resolution=2)
C.bezier_curve("RK_Hero_Strap_B", [(hero_x + 0.38, hero_y - 0.47, 3.27), (hero_x + 0.05, hero_y - 0.53, 2.88), (hero_x - 0.32, hero_y - 0.46, 2.55)], 0.045, "RK_MAT_Gold", hero_coll, bevel_resolution=2)

# Feather-like shoulder mantle.
for side, sign in (("L", -1), ("R", 1)):
    for idx in range(3):
        sx = hero_x + sign * (0.48 + idx * 0.13)
        sz = 3.27 - idx * 0.10
        C.uv_sphere(f"RK_Hero_ShoulderFeather.{side}.{idx}", (sx, hero_y + 0.02, sz), (0.48, 0.42, 0.28), "RK_MAT_NavyLight", hero_coll, segments=20, rings=12, rotation=(0, math.radians(sign * 18), math.radians(sign * 16)))

arm_pose = {
    "L": ((hero_x - 0.48, hero_y, 3.16), (hero_x - 0.76, hero_y - 0.04, 2.57), (hero_x - 0.69, hero_y - 0.16, 1.92)),
    "R": ((hero_x + 0.48, hero_y, 3.16), (hero_x + 0.78, hero_y - 0.10, 2.50), (hero_x + 0.64, hero_y - 0.20, 1.83)),
}
for side, (shoulder, elbow, wrist) in arm_pose.items():
    C.cylinder_between(f"RK_Hero_UpperArm.{side}", shoulder, elbow, 0.145, "RK_MAT_Skin", hero_coll, vertices=20, bevel_width=0.025)
    C.cylinder_between(f"RK_Hero_Forearm.{side}", elbow, wrist, 0.13, "RK_MAT_Skin", hero_coll, vertices=20, bevel_width=0.025)
    C.uv_sphere(f"RK_Hero_Glove.{side}", wrist, (0.34, 0.30, 0.42), "RK_MAT_White", hero_coll, segments=24, rings=16)
    C.torus(f"RK_Hero_GloveCuff.{side}", (wrist[0], wrist[1], wrist[2] + 0.18), 0.19, 0.055, "RK_MAT_NavyLight", hero_coll, major_segments=20, minor_segments=6)
    for finger in range(3):
        dx = (finger - 1) * 0.07
        C.cylinder_between(f"RK_Hero_Finger.{side}.{finger}", (wrist[0] + dx, wrist[1] - 0.12, wrist[2] - 0.04), (wrist[0] + dx, wrist[1] - 0.18, wrist[2] - 0.23), 0.035, "RK_MAT_White", hero_coll, vertices=10, bevel_width=0.01)

# ---------------------------------------------------------------------------
# Layered feather skirt, legs, straps and star-cuffed boots
# ---------------------------------------------------------------------------

C.cylinder("RK_Hero_SkirtWaist", (hero_x, hero_y, 2.25), 0.56, 0.32, "RK_MAT_Navy", hero_coll, vertices=28, bevel_width=0.08, smooth_shading=True)
for idx in range(10):
    angle = idx * math.tau / 10
    px = hero_x + math.cos(angle) * 0.50
    py = hero_y + math.sin(angle) * 0.32
    pz = 1.92 - 0.08 * (idx % 2)
    panel = C.uv_sphere(
        f"RK_Hero_SkirtPanel_{idx:02d}",
        (px, py, pz),
        (0.42, 0.24, 0.92),
        "RK_MAT_NavyLight" if idx % 2 else "RK_MAT_Navy",
        hero_coll,
        segments=20,
        rings=12,
        rotation=(0, math.radians(8 * math.cos(angle)), angle),
    )
    if idx in (1, 4, 7):
        C.ico_sphere(f"RK_Hero_SkirtGem_{idx:02d}", (px, py - 0.15, pz - 0.22), (0.10, 0.06, 0.16), "RK_MAT_Gold", hero_coll, subdivisions=1)

leg_data = (("L", -0.27, -0.02), ("R", 0.30, 0.06))
for side, dx, dy in leg_data:
    lx = hero_x + dx
    ly = hero_y + dy
    C.cylinder_between(f"RK_Hero_Thigh.{side}", (lx, ly, 2.05), (lx + 0.02 * (1 if side == "R" else -1), ly, 1.28), 0.19, "RK_MAT_Skin", hero_coll, vertices=24, bevel_width=0.025)
    C.torus(f"RK_Hero_ThighStrap.{side}", (lx, ly, 1.62), 0.205, 0.045, "RK_MAT_Leather", hero_coll, major_segments=24, minor_segments=6)
    C.cylinder_between(f"RK_Hero_Shin.{side}", (lx, ly, 1.28), (lx + 0.04 * (1 if side == "R" else -1), ly - 0.03, 0.58), 0.18, "RK_MAT_Skin", hero_coll, vertices=24, bevel_width=0.025)
    bx = lx + 0.04 * (1 if side == "R" else -1)
    C.cylinder(f"RK_Hero_BootShaft.{side}", (bx, ly, 0.68), 0.245, 0.78, "RK_MAT_Navy", hero_coll, vertices=20, bevel_width=0.06)
    C.box(f"RK_Hero_Boot.{side}", (bx, ly - 0.16, 0.27), (0.56, 0.86, 0.46), "RK_MAT_Navy", hero_coll, bevel_width=0.13)
    C.box(f"RK_Hero_BootSole.{side}", (bx, ly - 0.20, 0.09), (0.64, 0.94, 0.15), "RK_MAT_BlackMetal", hero_coll, bevel_width=0.06)
    C.torus(f"RK_Hero_BootCuff.{side}", (bx, ly, 1.03), 0.30, 0.075, "RK_MAT_HairLavender", hero_coll, major_segments=24, minor_segments=7)
    star_obj = C.star(f"RK_Hero_BootStar.{side}", (0, 0), 0, 0.30, 0.13, 6, 0.08, "RK_MAT_NavyLight", hero_coll, rotation=math.pi / 6)
    star_obj.location = (bx, ly - 0.33, 1.10)
    star_obj.rotation_euler.x = math.pi / 2
    # Decorative diagonal ankle ties.
    C.bezier_curve(f"RK_Hero_BootTieA.{side}", [(bx - 0.20, ly - 0.26, 0.80), (bx + 0.20, ly - 0.30, 0.56)], 0.035, "RK_MAT_Leather", hero_coll, bevel_resolution=2)
    C.bezier_curve(f"RK_Hero_BootTieB.{side}", [(bx + 0.20, ly - 0.26, 0.80), (bx - 0.20, ly - 0.30, 0.56)], 0.035, "RK_MAT_Leather", hero_coll, bevel_resolution=2)

# Parent all hero geometry to the semantic armature while preserving transforms.
for obj in list(hero_coll.objects):
    if obj not in hero_geometry_start and obj is not armature and obj is not root:
        world_matrix = obj.matrix_world.copy()
        obj.parent = armature
        obj.matrix_world = world_matrix


# ---------------------------------------------------------------------------
# Purple-white companion with long ears, twin tails and leaf costume
# ---------------------------------------------------------------------------

pet_x = -1.25
pet_y = -4.10
pet_root = bpy.data.objects.new("RK_Companion_Root", None)
pet_coll.objects.link(pet_root)
pet_root.location = (pet_x, pet_y, 0)
pet_root["asset_role"] = "companion_root"

tag(C.uv_sphere("RK_Companion_Body", (pet_x, pet_y, 1.05), (1.15, 0.95, 1.45), "RK_MAT_PetPurple", pet_coll, segments=36, rings=24), "companion_body")
tag(C.uv_sphere("RK_Companion_Head", (pet_x, pet_y - 0.03, 2.03), (1.48, 1.17, 1.26), "RK_MAT_PetPurple", pet_coll, segments=40, rings=28), "companion_head")
C.uv_sphere("RK_Companion_FaceMask", (pet_x, pet_y - 0.57, 2.02), (1.02, 0.18, 0.86), "RK_MAT_White", pet_coll, segments=32, rings=22)
C.uv_sphere("RK_Companion_Muzzle", (pet_x, pet_y - 0.69, 1.80), (0.52, 0.20, 0.35), "RK_MAT_White", pet_coll, segments=24, rings=16)

for side, dx in (("L", -0.31), ("R", 0.31)):
    C.uv_sphere(f"RK_Companion_Eye.{side}", (pet_x + dx, pet_y - 0.65, 2.16), (0.35, 0.08, 0.43), "RK_MAT_EyeBlack", pet_coll, segments=28, rings=18)
    C.uv_sphere(f"RK_Companion_Iris.{side}", (pet_x + dx, pet_y - 0.70, 2.16), (0.20, 0.04, 0.27), "RK_MAT_SpriteGlow", pet_coll, segments=20, rings=14)
    C.uv_sphere(f"RK_Companion_EyeHighlight.{side}", (pet_x + dx - 0.05, pet_y - 0.73, 2.26), (0.07, 0.02, 0.09), "RK_MAT_White", pet_coll, segments=14, rings=10)
C.ico_sphere("RK_Companion_Nose", (pet_x, pet_y - 0.82, 1.86), (0.16, 0.10, 0.13), "RK_MAT_EyeBlack", pet_coll, subdivisions=2)
C.bezier_curve("RK_Companion_Mouth", [(pet_x - 0.12, pet_y - 0.80, 1.72), (pet_x, pet_y - 0.85, 1.66), (pet_x + 0.12, pet_y - 0.80, 1.72)], 0.022, "RK_MAT_RedBow", pet_coll, bevel_resolution=3)

# Drooping ribbon-like ears with pale inner tips.
for side, sign in (("L", -1), ("R", 1)):
    ear_points = [
        (pet_x + sign * 0.48, pet_y + 0.02, 2.55),
        (pet_x + sign * 0.95, pet_y - 0.02, 2.10),
        (pet_x + sign * 1.05, pet_y - 0.15, 1.42),
        (pet_x + sign * 0.82, pet_y - 0.28, 1.12),
    ]
    C.bezier_curve(f"RK_Companion_Ear.{side}", ear_points, 0.19, "RK_MAT_PetPurple", pet_coll, bevel_resolution=4)
    C.uv_sphere(f"RK_Companion_EarTip.{side}", ear_points[-1], (0.48, 0.30, 0.50), "RK_MAT_White", pet_coll, segments=22, rings=14)

# Leaf collar, vest and layered skirt.
C.torus("RK_Companion_Collar", (pet_x, pet_y, 1.48), 0.43, 0.10, "RK_MAT_PetTeal", pet_coll, major_segments=28, minor_segments=8)
C.ico_sphere("RK_Companion_CollarGem", (pet_x, pet_y - 0.49, 1.50), (0.20, 0.12, 0.24), "RK_MAT_SpriteGlow", pet_coll, subdivisions=2)
C.uv_sphere("RK_Companion_Chest", (pet_x, pet_y - 0.42, 1.14), (0.65, 0.20, 0.82), "RK_MAT_White", pet_coll, segments=28, rings=18)
for idx in range(8):
    angle = idx * math.tau / 8
    px = pet_x + math.cos(angle) * 0.48
    py = pet_y + math.sin(angle) * 0.35
    C.uv_sphere(f"RK_Companion_LeafSkirt_{idx:02d}", (px, py, 0.78), (0.38, 0.20, 0.72), "RK_MAT_PetTeal", pet_coll, segments=18, rings=12, rotation=(0, math.radians(12), angle))

# Small paws and violet feet.
for side, sign in (("L", -1), ("R", 1)):
    C.cylinder_between(f"RK_Companion_Arm.{side}", (pet_x + sign * 0.42, pet_y - 0.10, 1.28), (pet_x + sign * 0.62, pet_y - 0.34, 0.88), 0.13, "RK_MAT_PetPurple", pet_coll, vertices=16)
    C.uv_sphere(f"RK_Companion_Paw.{side}", (pet_x + sign * 0.64, pet_y - 0.38, 0.78), (0.34, 0.28, 0.31), "RK_MAT_White", pet_coll, segments=20, rings=14)
    C.cylinder(f"RK_Companion_Leg.{side}", (pet_x + sign * 0.27, pet_y, 0.42), 0.20, 0.68, "RK_MAT_PetPurple", pet_coll, vertices=18, bevel_width=0.05)
    C.uv_sphere(f"RK_Companion_Foot.{side}", (pet_x + sign * 0.28, pet_y - 0.18, 0.16), (0.50, 0.68, 0.32), "RK_MAT_PetPurple", pet_coll, segments=22, rings=14)
    for toe in range(3):
        C.ico_sphere(f"RK_Companion_Toe.{side}.{toe}", (pet_x + sign * 0.28 + (toe - 1) * 0.11, pet_y - 0.51, 0.16), (0.10, 0.08, 0.09), "RK_MAT_HairLavender", pet_coll, subdivisions=1)

# Twin sweeping tails, each with a pale tip.
tail_paths = [
    [(pet_x + 0.35, pet_y + 0.35, 0.95), (pet_x + 1.15, pet_y + 0.25, 0.85), (pet_x + 1.50, pet_y - 0.05, 0.42), (pet_x + 1.15, pet_y - 0.30, 0.20)],
    [(pet_x + 0.15, pet_y + 0.42, 1.05), (pet_x + 0.90, pet_y + 0.55, 1.10), (pet_x + 1.35, pet_y + 0.32, 0.78), (pet_x + 1.40, pet_y - 0.02, 0.48)],
]
for idx, path in enumerate(tail_paths):
    C.bezier_curve(f"RK_Companion_Tail_{idx:02d}", path, 0.25, "RK_MAT_PetPurple", pet_coll, bevel_resolution=5)
    C.uv_sphere(f"RK_Companion_TailTip_{idx:02d}", path[-1], (0.64, 0.48, 0.54), "RK_MAT_White", pet_coll, segments=24, rings=16)

# Cyan jelly-sprite perched just above the companion.
sprite_x, sprite_y, sprite_z = pet_x + 0.12, pet_y + 0.10, 3.05
tag(C.uv_sphere("RK_Sprite_Core", (sprite_x, sprite_y, sprite_z), (0.72, 0.58, 0.58), "RK_MAT_SpriteGlow", pet_coll, segments=28, rings=18), "sprite_core")
C.uv_sphere("RK_Sprite_Face", (sprite_x, sprite_y - 0.31, sprite_z - 0.02), (0.48, 0.08, 0.32), "RK_MAT_HairCyan", pet_coll, segments=22, rings=14)
for side, dx in (("L", -0.13), ("R", 0.13)):
    C.uv_sphere(f"RK_Sprite_Eye.{side}", (sprite_x + dx, sprite_y - 0.365, sprite_z + 0.03), (0.065, 0.02, 0.11), "RK_MAT_EyeBlack", pet_coll, segments=14, rings=10)
for idx in range(5):
    angle = math.pi + idx * math.pi / 4
    C.bezier_curve(
        f"RK_Sprite_Tendril_{idx:02d}",
        [(sprite_x, sprite_y, sprite_z - 0.25), (sprite_x + math.cos(angle) * 0.27, sprite_y + math.sin(angle) * 0.14, sprite_z - 0.46), (sprite_x + math.cos(angle) * 0.35, sprite_y + math.sin(angle) * 0.20, sprite_z - 0.66)],
        0.055,
        "RK_MAT_SpriteGlow",
        pet_coll,
        bevel_resolution=3,
    )
C.cone("RK_Sprite_Tuft", (sprite_x, sprite_y, sprite_z + 0.48), 0.18, 0.02, 0.48, "RK_MAT_SpriteGlow", pet_coll, vertices=14, smooth_shading=True)

for obj in list(pet_coll.objects):
    if obj is not pet_root:
        world_matrix = obj.matrix_world.copy()
        obj.parent = pet_root
        obj.matrix_world = world_matrix

C.save_mainfile()
C.scene_summary("04_character")

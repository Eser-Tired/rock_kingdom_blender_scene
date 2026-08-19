"""Blender-side acceptance contract for the generated Rock Kingdom scene."""

from pathlib import Path
import bpy


PROJECT_ROOT = Path(r"C:\Users\Eser\Documents\Code\rock_kingdom_blender_scene")


def _failures():
    failures = []

    required_collections = {
        "RK_ARCHITECTURE",
        "RK_ENVIRONMENT",
        "RK_HERO_CHARACTER",
        "RK_COMPANION",
        "RK_LIGHTING",
        "RK_CAMERAS",
    }
    missing_collections = sorted(required_collections - set(bpy.data.collections.keys()))
    if missing_collections:
        failures.append(f"missing collections: {missing_collections}")

    required_objects = {
        "RK_Plaza_Base",
        "RK_GuildHall_Main",
        "RK_CastleGate_Main",
        "RK_Hero_Head",
        "RK_Hero_Eye.L",
        "RK_Hero_Eye.R",
        "RK_Hero_Bow_Center",
        "RK_Hero_Crown",
        "RK_Hero_Armature",
        "RK_Companion_Body",
        "RK_Companion_Head",
        "RK_Sprite_Core",
    }
    missing_objects = sorted(required_objects - set(bpy.data.objects.keys()))
    if missing_objects:
        failures.append(f"missing objects: {missing_objects}")

    hair_locks = [obj for obj in bpy.data.objects if obj.name.startswith("RK_Hero_HairLock_")]
    if len(hair_locks) < 12:
        failures.append(f"hero hair locks: expected >= 12, got {len(hair_locks)}")

    if len(bpy.data.objects) < 180:
        failures.append(f"object count: expected >= 180, got {len(bpy.data.objects)}")
    rk_materials = [mat for mat in bpy.data.materials if mat.name.startswith("RK_MAT_")]
    if len(rk_materials) < 20:
        failures.append(f"RK material count: expected >= 20, got {len(rk_materials)}")

    shader_mismatches = []
    for material in rk_materials:
        if not material.use_nodes or material.node_tree is None:
            shader_mismatches.append(f"{material.name}: nodes disabled")
            continue
        output = next((node for node in material.node_tree.nodes if node.type == "OUTPUT_MATERIAL"), None)
        surface_link = next(
            (
                link
                for link in material.node_tree.links
                if output is not None and link.to_node == output and link.to_socket.name == "Surface"
            ),
            None,
        )
        shader = surface_link.from_node if surface_link is not None else None
        base_socket = shader.inputs.get("Base Color") if shader is not None else None
        if shader is None or shader.type != "BSDF_PRINCIPLED" or base_socket is None:
            shader_mismatches.append(f"{material.name}: no connected Principled BSDF")
            continue
        actual = tuple(base_socket.default_value[:3])
        expected = tuple(material.diffuse_color[:3])
        if max(abs(a - b) for a, b in zip(actual, expected)) > 0.025:
            shader_mismatches.append(f"{material.name}: shader={actual}, diffuse={expected}")
    if shader_mismatches:
        failures.append(
            f"connected shader color mismatch in {len(shader_mismatches)} materials; "
            f"first={shader_mismatches[0]}"
        )
    if len(bpy.data.lights) < 10:
        failures.append(f"light count: expected >= 10, got {len(bpy.data.lights)}")
    if len(bpy.data.cameras) < 3:
        failures.append(f"camera count: expected >= 3, got {len(bpy.data.cameras)}")

    world = bpy.context.scene.world
    background = None
    if world is not None and world.use_nodes and world.node_tree is not None:
        background = next((node for node in world.node_tree.nodes if node.type == "BACKGROUND"), None)
    if background is None:
        failures.append("night sky has no world Background node")
    else:
        sky_color = tuple(background.inputs["Color"].default_value[:3])
        if sky_color[2] < 0.15 or sky_color[2] < sky_color[0] * 4.0:
            failures.append(f"night sky is not a readable deep blue: {sky_color}")

    close_camera = bpy.data.objects.get("RK_Camera_Character")
    if close_camera is not None and close_camera.data.lens > 42.0:
        failures.append(f"character closeup lens is too tight: {close_camera.data.lens}mm")

    hero_head = bpy.data.objects.get("RK_Hero_Head")
    if hero_head is not None:
        if max(hero_head.dimensions) < 0.85:
            failures.append(f"hero head is undersized: {tuple(round(v, 3) for v in hero_head.dimensions)}")
        if not hero_head.get("detail_level") == "hero":
            failures.append("hero head missing detail_level='hero' metadata")

    blend_path = Path(bpy.data.filepath) if bpy.data.filepath else None
    if blend_path is None or PROJECT_ROOT not in blend_path.parents:
        failures.append(f"blend file is not saved inside project: {bpy.data.filepath!r}")

    return failures


failures = _failures()
if failures:
    print("TDD_SCENE_CONTRACT_FAIL")
    for item in failures:
        print(f" - {item}")
    raise AssertionError(" | ".join(failures))

print(
    "TDD_SCENE_CONTRACT_PASS "
    f"objects={len(bpy.data.objects)} materials={len(bpy.data.materials)} "
    f"lights={len(bpy.data.lights)} cameras={len(bpy.data.cameras)}"
)

"""Repair localized Blender material nodes created before the type-based fix."""

from pathlib import Path
import sys

import bpy


ROOT = Path(r"C:\Users\Eser\Documents\Code\rock_kingdom_blender_scene")
repaired = 0

for material in [mat for mat in bpy.data.materials if mat.name.startswith("RK_MAT_")]:
    material.use_nodes = True
    tree = material.node_tree
    nodes = tree.nodes
    output = next((node for node in nodes if node.type == "OUTPUT_MATERIAL"), None)
    if output is None:
        output = nodes.new("ShaderNodeOutputMaterial")

    surface_link = next(
        (
            link
            for link in tree.links
            if link.to_node == output and link.to_socket.name == "Surface"
        ),
        None,
    )
    connected = surface_link.from_node if surface_link and surface_link.from_node.type == "BSDF_PRINCIPLED" else None
    if connected is None:
        connected = next((node for node in nodes if node.type == "BSDF_PRINCIPLED"), None)
        if connected is None:
            connected = nodes.new("ShaderNodeBsdfPrincipled")
        tree.links.new(connected.outputs.get("BSDF"), output.inputs.get("Surface"))

    candidates = [node for node in nodes if node.type == "BSDF_PRINCIPLED" and node != connected]
    configured = candidates[-1] if candidates else None
    if configured is not None:
        for source_socket in configured.inputs:
            target_socket = connected.inputs.get(source_socket.name)
            if target_socket is None or not hasattr(source_socket, "default_value"):
                continue
            try:
                target_socket.default_value = source_socket.default_value
            except (TypeError, ValueError):
                try:
                    target_socket.default_value = tuple(source_socket.default_value)
                except Exception:
                    pass

    # Diffuse color is the authoritative project palette entry.
    base = connected.inputs.get("Base Color")
    if base is not None:
        base.default_value = (*material.diffuse_color[:3], 1.0)
    for extra in candidates:
        nodes.remove(extra)
    repaired += 1

bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "rock_kingdom_fantasy_plaza.blend"))
print(f"RK_MATERIAL_REPAIR_OK repaired={repaired}")

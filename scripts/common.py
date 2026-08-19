"""Shared deterministic Blender helpers for the Rock Kingdom scene."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable, Sequence

import bpy
from mathutils import Vector


PROJECT_ROOT = Path(r"C:\Users\Eser\Documents\Code\rock_kingdom_blender_scene")


def collection(name: str, parent: bpy.types.Collection | None = None) -> bpy.types.Collection:
    coll = bpy.data.collections.get(name)
    if coll is None:
        coll = bpy.data.collections.new(name)
        (parent or bpy.context.scene.collection).children.link(coll)
    return coll


def move_to_collection(obj: bpy.types.Object, coll: bpy.types.Collection | str) -> bpy.types.Object:
    if isinstance(coll, str):
        coll = collection(coll)
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    coll.objects.link(obj)
    return obj


def set_active(obj: bpy.types.Object) -> None:
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)


def material(
    name: str,
    color: Sequence[float],
    *,
    roughness: float = 0.68,
    metallic: float = 0.0,
    emission: Sequence[float] | None = None,
    emission_strength: float = 0.0,
    alpha: float = 1.0,
) -> bpy.types.Material:
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.diffuse_color = (*color[:3], alpha)
    nodes = mat.node_tree.nodes
    # Node display names are localized by Blender, so discover nodes by type.
    bsdf = next((node for node in nodes if node.type == "BSDF_PRINCIPLED"), None)
    if bsdf is None:
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
        output = next((node for node in nodes if node.type == "OUTPUT_MATERIAL"), None)
        if output is None:
            output = nodes.new("ShaderNodeOutputMaterial")
        mat.node_tree.links.new(bsdf.outputs.get("BSDF"), output.inputs.get("Surface"))

    def set_input(socket_name: str, value):
        socket = bsdf.inputs.get(socket_name)
        if socket is not None:
            socket.default_value = value

    set_input("Base Color", (*color[:3], 1.0))
    set_input("Roughness", roughness)
    set_input("Metallic", metallic)
    set_input("Alpha", alpha)
    if emission is not None:
        set_input("Emission Color", (*emission[:3], 1.0))
        set_input("Emission Strength", emission_strength)
    mat.surface_render_method = "DITHERED" if alpha < 1.0 else "DITHERED"
    return mat


def mat(name: str) -> bpy.types.Material:
    result = bpy.data.materials.get(name)
    if result is None:
        raise KeyError(f"Material not found: {name}")
    return result


def assign(obj: bpy.types.Object, material_or_name) -> bpy.types.Object:
    material_value = mat(material_or_name) if isinstance(material_or_name, str) else material_or_name
    if hasattr(obj.data, "materials"):
        obj.data.materials.clear()
        obj.data.materials.append(material_value)
    return obj


def bevel(obj: bpy.types.Object, width: float = 0.06, segments: int = 2) -> bpy.types.Object:
    if width <= 0:
        return obj
    mod = obj.modifiers.new("RK_Bevel", "BEVEL")
    mod.width = width
    mod.segments = segments
    mod.limit_method = "ANGLE"
    return obj


def smooth(obj: bpy.types.Object, value: bool = True) -> bpy.types.Object:
    if obj.type == "MESH":
        for poly in obj.data.polygons:
            poly.use_smooth = value
    return obj


def box(
    name: str,
    location: Sequence[float],
    dimensions: Sequence[float],
    material_name,
    coll,
    *,
    rotation: Sequence[float] = (0.0, 0.0, 0.0),
    bevel_width: float = 0.05,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(obj, material_name)
    move_to_collection(obj, coll)
    bevel(obj, bevel_width)
    return obj


def cylinder(
    name: str,
    location: Sequence[float],
    radius: float,
    depth: float,
    material_name,
    coll,
    *,
    vertices: int = 24,
    rotation: Sequence[float] = (0.0, 0.0, 0.0),
    bevel_width: float = 0.03,
    smooth_shading: bool = False,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    assign(obj, material_name)
    move_to_collection(obj, coll)
    bevel(obj, bevel_width)
    smooth(obj, smooth_shading)
    return obj


def cylinder_between(
    name: str,
    start: Sequence[float],
    end: Sequence[float],
    radius: float,
    material_name,
    coll,
    *,
    vertices: int = 16,
    bevel_width: float = 0.02,
    smooth_shading: bool = True,
) -> bpy.types.Object:
    a, b = Vector(start), Vector(end)
    direction = b - a
    midpoint = (a + b) * 0.5
    rotation = direction.to_track_quat("Z", "Y").to_euler()
    return cylinder(
        name,
        midpoint,
        radius,
        direction.length,
        material_name,
        coll,
        vertices=vertices,
        rotation=rotation,
        bevel_width=bevel_width,
        smooth_shading=smooth_shading,
    )


def cone(
    name: str,
    location: Sequence[float],
    radius1: float,
    radius2: float,
    depth: float,
    material_name,
    coll,
    *,
    vertices: int = 24,
    rotation: Sequence[float] = (0.0, 0.0, 0.0),
    smooth_shading: bool = False,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cone_add(
        vertices=vertices,
        radius1=radius1,
        radius2=radius2,
        depth=depth,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    assign(obj, material_name)
    move_to_collection(obj, coll)
    smooth(obj, smooth_shading)
    return obj


def uv_sphere(
    name: str,
    location: Sequence[float],
    dimensions: Sequence[float],
    material_name,
    coll,
    *,
    segments: int = 32,
    rings: int = 20,
    rotation: Sequence[float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments,
        ring_count=rings,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(obj, material_name)
    move_to_collection(obj, coll)
    smooth(obj)
    return obj


def ico_sphere(
    name: str,
    location: Sequence[float],
    dimensions: Sequence[float],
    material_name,
    coll,
    *,
    subdivisions: int = 2,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(obj, material_name)
    move_to_collection(obj, coll)
    smooth(obj)
    return obj


def torus(
    name: str,
    location: Sequence[float],
    major_radius: float,
    minor_radius: float,
    material_name,
    coll,
    *,
    rotation: Sequence[float] = (0.0, 0.0, 0.0),
    major_segments: int = 48,
    minor_segments: int = 8,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_radius,
        minor_radius=minor_radius,
        major_segments=major_segments,
        minor_segments=minor_segments,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    assign(obj, material_name)
    move_to_collection(obj, coll)
    smooth(obj)
    return obj


def bezier_curve(
    name: str,
    points: Iterable[Sequence[float]],
    bevel_depth: float,
    material_name,
    coll,
    *,
    bevel_resolution: int = 3,
    cyclic: bool = False,
) -> bpy.types.Object:
    pts = list(points)
    data = bpy.data.curves.new(name + "_Curve", "CURVE")
    data.dimensions = "3D"
    data.resolution_u = 12
    data.bevel_depth = bevel_depth
    data.bevel_resolution = bevel_resolution
    data.resolution_u = 12
    spline = data.splines.new("BEZIER")
    spline.bezier_points.add(len(pts) - 1)
    for bp, co in zip(spline.bezier_points, pts):
        bp.co = co
        bp.handle_left_type = "AUTO"
        bp.handle_right_type = "AUTO"
    spline.use_cyclic_u = cyclic
    obj = bpy.data.objects.new(name, data)
    coll_value = collection(coll) if isinstance(coll, str) else coll
    coll_value.objects.link(obj)
    assign(obj, material_name)
    return obj


def mesh_object(
    name: str,
    vertices: Sequence[Sequence[float]],
    faces: Sequence[Sequence[int]],
    material_name,
    coll,
    *,
    bevel_width: float = 0.0,
) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(name + "_Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    coll_value = collection(coll) if isinstance(coll, str) else coll
    coll_value.objects.link(obj)
    assign(obj, material_name)
    bevel(obj, bevel_width)
    return obj


def extruded_polygon(
    name: str,
    points_xy: Sequence[Sequence[float]],
    z_center: float,
    depth: float,
    material_name,
    coll,
    *,
    bevel_width: float = 0.02,
) -> bpy.types.Object:
    count = len(points_xy)
    bottom = [(x, y, z_center - depth / 2) for x, y in points_xy]
    top = [(x, y, z_center + depth / 2) for x, y in points_xy]
    vertices = bottom + top
    faces = [tuple(range(count - 1, -1, -1)), tuple(range(count, count * 2))]
    for i in range(count):
        j = (i + 1) % count
        faces.append((i, j, count + j, count + i))
    return mesh_object(name, vertices, faces, material_name, coll, bevel_width=bevel_width)


def star(
    name: str,
    center_xy: Sequence[float],
    z_center: float,
    outer_radius: float,
    inner_radius: float,
    points: int,
    depth: float,
    material_name,
    coll,
    *,
    rotation: float = 0.0,
) -> bpy.types.Object:
    coords = []
    for i in range(points * 2):
        angle = rotation + math.pi / 2 + i * math.pi / points
        radius = outer_radius if i % 2 == 0 else inner_radius
        coords.append((center_xy[0] + radius * math.cos(angle), center_xy[1] + radius * math.sin(angle)))
    return extruded_polygon(name, coords, z_center, depth, material_name, coll, bevel_width=0.025)


def roof_prism(
    name: str,
    location: Sequence[float],
    width: float,
    depth: float,
    height: float,
    material_name,
    coll,
    *,
    rotation_z: float = 0.0,
) -> bpy.types.Object:
    w, d, h = width / 2, depth / 2, height
    verts = [
        (-w, -d, 0), (w, -d, 0), (0, -d, h),
        (-w, d, 0), (w, d, 0), (0, d, h),
    ]
    faces = [(0, 2, 1), (3, 4, 5), (0, 3, 5, 2), (2, 5, 4, 1), (0, 1, 4, 3)]
    obj = mesh_object(name, verts, faces, material_name, coll, bevel_width=0.04)
    obj.location = location
    obj.rotation_euler.z = rotation_z
    return obj


def arch_ring(
    name: str,
    center: Sequence[float],
    inner_radius: float,
    thickness: float,
    depth: float,
    material_name,
    coll,
    *,
    segments: int = 24,
) -> bpy.types.Object:
    outer_radius = inner_radius + thickness
    angles = [i * math.pi / segments for i in range(segments + 1)]
    verts = []
    for yoff in (-depth / 2, depth / 2):
        for radius in (outer_radius, inner_radius):
            for angle in angles:
                verts.append((
                    center[0] + radius * math.cos(angle),
                    center[1] + yoff,
                    center[2] + radius * math.sin(angle),
                ))
    n = len(angles)
    # Each y side has outer then inner arc.
    faces = []
    for side in (0, 1):
        base = side * 2 * n
        for i in range(segments):
            faces.append((base + i, base + i + 1, base + n + i + 1, base + n + i))
    # Outer and inner curved surfaces.
    front, back = 0, 2 * n
    for i in range(segments):
        faces.append((front + i, back + i, back + i + 1, front + i + 1))
        faces.append((front + n + i + 1, back + n + i + 1, back + n + i, front + n + i))
    # End caps.
    faces.append((0, n, 3 * n, 2 * n))
    faces.append((n - 1, 2 * n - 1, 4 * n - 1, 3 * n - 1))
    return mesh_object(name, verts, faces, material_name, coll, bevel_width=0.025)


def parent(child: bpy.types.Object, parent_obj: bpy.types.Object) -> bpy.types.Object:
    child.parent = parent_obj
    child.matrix_parent_inverse = parent_obj.matrix_world.inverted()
    return child


def look_at(obj: bpy.types.Object, target: Sequence[float]) -> None:
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def camera(name: str, location, target, lens: float, coll) -> bpy.types.Object:
    data = bpy.data.cameras.new(name + "_Data")
    data.lens = lens
    data.sensor_width = 36
    obj = bpy.data.objects.new(name, data)
    coll_value = collection(coll) if isinstance(coll, str) else coll
    coll_value.objects.link(obj)
    obj.location = location
    look_at(obj, target)
    return obj


def point_light(name: str, location, color, energy: float, radius: float, coll) -> bpy.types.Object:
    data = bpy.data.lights.new(name + "_Data", "POINT")
    data.color = color
    data.energy = energy
    data.shadow_soft_size = radius
    obj = bpy.data.objects.new(name, data)
    coll_value = collection(coll) if isinstance(coll, str) else coll
    coll_value.objects.link(obj)
    obj.location = location
    return obj


def area_light(name: str, location, target, color, energy: float, size: float, coll) -> bpy.types.Object:
    data = bpy.data.lights.new(name + "_Data", "AREA")
    data.color = color
    data.energy = energy
    data.shape = "DISK"
    data.size = size
    obj = bpy.data.objects.new(name, data)
    coll_value = collection(coll) if isinstance(coll, str) else coll
    coll_value.objects.link(obj)
    obj.location = location
    look_at(obj, target)
    return obj


def set_origin_cursor(obj: bpy.types.Object, cursor=(0.0, 0.0, 0.0)) -> None:
    bpy.context.scene.cursor.location = cursor
    bpy.ops.object.select_all(action="DESELECT")
    set_active(obj)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")
    obj.select_set(False)


def save_mainfile() -> Path:
    path = PROJECT_ROOT / "rock_kingdom_fantasy_plaza.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(path))
    return path


def scene_summary(stage: str) -> None:
    print(
        f"RK_STAGE_OK {stage} objects={len(bpy.data.objects)} "
        f"materials={len(bpy.data.materials)} lights={len(bpy.data.lights)} "
        f"cameras={len(bpy.data.cameras)}"
    )

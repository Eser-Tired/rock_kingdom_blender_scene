"Export the refined Rock Kingdom fantasy plaza to GLB format."

from pathlib import Path
import bpy

ROOT = Path(rC:\Users\Eser\Documents\Code\rock_kingdom_blender_scene)
export_path = ROOT / rock_kingdom_plaza.glb

for coll in bpy.data.collections:
    coll.hide_viewport = False
    coll.hide_render = False

bpy.ops.export_scene.gltf(
    filepath=str(export_path),
    export_format='GLB',
    export_apply=True,
    export_materials='EXPORT',
    export_cameras=True,
    export_lights=True,
    export_extras=True,
)
print(fExported GLB successfully: {export_path} size={export_path.stat().st_size} bytes)

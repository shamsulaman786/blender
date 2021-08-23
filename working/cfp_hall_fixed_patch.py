from bpy import context, data, ops
import glob
import os
import bmesh
import bpy

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(type="EDGE")
bpy.ops.mesh.select_all(action='SELECT')

# extrude to z axis by 2.95
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip": False, "use_dissolve_ortho_edges": False, "mirror": False}, TRANSFORM_OT_translate={"value": (0, 0, 2.95), "orient_type": 'GLOBAL', "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type": 'GLOBAL', "constraint_axis": (False, False, True), "mirror": False, "use_proportional_edit": False, "proportional_edit_falloff": 'SMOOTH',
                                                                                                                                                                "proportional_size": 1, "use_proportional_connected": False, "use_proportional_projected": False, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "gpencil_strokes": False, "cursor_transform": False, "texture_space": False, "remove_on_cancel": False, "release_confirm": False, "use_accurate": False, "use_automerge_and_split": False})
# switch to object mode
bpy.ops.object.mode_set(mode='OBJECT')

# select plane object
bpy.data.objects['Plane'].select_set(True)

# solidify seleceted mesh
bpy.ops.object.modifier_add(type='SOLIDIFY')

# add thickness
plane_object = bpy.data.objects['Plane']
plane_object.modifiers["Solidify"].thickness = 0
plane_object.modifiers["Solidify"].offset = 0
plane_object.modifiers["Solidify"].solidify_mode = 'NON_MANIFOLD'

# creating floor
# add plane
bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0, 0, 1.5), scale=(1, 1, 1))

# scale plane
bpy.ops.transform.resize(value=(50, 50, 50), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True,use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

# perform boolean operation
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.modifier_add(type='BOOLEAN')
extra_plane = bpy.data.objects['Plane.001']
extra_plane.modifiers["Boolean"].object = bpy.data.objects["Plane"]
# extra_plane.modifiers["Boolean"].solver = 'FAST'
bpy.ops.object.modifier_apply(modifier="Boolean")

# delete vertices
# make sure bmesh is imported
bpy.ops.object.mode_set(mode='EDIT')
me = extra_plane.data
bm = bmesh.from_edit_mesh(me)

for i, v in enumerate(bm.verts):
    v.select = i < 4

bmesh.update_edit_mesh(me)
bpy.ops.mesh.delete(type='VERT')

extra_plane.name = 'Floor'  # object rename
extra_plane.data.name = 'Floor'  # mesh rename

# creating Ceil
bpy.ops.object.mode_set(mode='OBJECT')
# grab & move to bottom
bpy.ops.transform.translate(value=(-0, -0, -1.5), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 2.95), "orient_type": 'GLOBAL', "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type": 'GLOBAL', "constraint_axis": (False, False, True), "mirror": True, "use_proportional_edit": False, "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1,"use_proportional_connected": False, "use_proportional_projected": False, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "gpencil_strokes": False, "cursor_transform": False, "texture_space": False, "remove_on_cancel": False, "release_confirm": False, "use_accurate": False, "use_automerge_and_split": False})
ceil_object = bpy.data.objects['Floor.001']
ceil_object.name = 'Ceil'
ceil_object.data.name = 'Ceil'

# add thickness
plane_object = bpy.data.objects['Plane']
plane_object.modifiers["Solidify"].thickness = 0.2
plane_object.modifiers["Solidify"].solidify_mode = 'NON_MANIFOLD'


# naming walls
bpy.data.objects['Plane'].name = 'Walls'
bpy.data.objects['Walls'].data.name = 'Walls'


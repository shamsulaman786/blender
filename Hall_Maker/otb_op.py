from bpy import context, data, ops
import glob
import os
import bmesh
import bpy
from bpy.types import Operator

class OTB_OT_Apply_All_Op(Operator):
    bl_idname = "object.apply_all_mods"
    bl_label = "Make hall"
    bl_description = "Make hall operators of the active object"

    @classmethod
    def poll(self,context):
        obj = context.object

        if obj is not None:
            if obj.mode == "OBJECT":
                return True

        return False

# self says , its implemented fo class
# return state of operator
    def execute(self,context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="EDGE")
        bpy.ops.mesh.select_all(action='SELECT')

        # extrude to z axis by 2.95
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip": False, "use_dissolve_ortho_edges": False, "mirror": False}, TRANSFORM_OT_translate={"value": (0, 0, 2.95), "orient_type": 'GLOBAL', "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type": 'GLOBAL', "constraint_axis": (False, False, True), "mirror": False, "use_proportional_edit": False, "proportional_edit_falloff": 'SMOOTH',
                                                                                                                                                                        "proportional_size": 1, "use_proportional_connected": False, "use_proportional_projected": False, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "gpencil_strokes": False, "cursor_transform": False, "texture_space": False, "remove_on_cancel": False, "release_confirm": False, "use_accurate": False, "use_automerge_and_split": False})
        # switch to object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # select plane object
        wall_object = context.view_layer.objects.active

        # wall_object.select_set(True)

        # solidify seleceted mesh
        bpy.ops.object.modifier_add(type='SOLIDIFY')

        # add thickness
        wall_object_solidify_modifiers = wall_object.modifiers['Solidify']
        wall_object_solidify_modifiers.thickness = 0
        wall_object_solidify_modifiers.offset = 0
        wall_object_solidify_modifiers.solidify_mode = 'NON_MANIFOLD'

        # creating floor
        # add plane
        bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0, 0, 1.5), scale=(1, 1, 1))

        # scale plane
        bpy.ops.transform.resize(value=(50, 50, 50), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True,use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        # perform boolean operation
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.modifier_add(type='BOOLEAN')
        extra_plane = context.view_layer.objects.active
        extra_plane.modifiers["Boolean"].object = wall_object
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


        #naming based on no of halls
        halls = 1
        for obj in bpy.data.objects:
            if 'Walls' in obj.name:
                halls += 1

        extra_plane.name = str(halls) + '.Floor'  # object rename
        extra_plane.data.name = str(halls) + '.Floor'  # mesh rename
        floor_object = extra_plane

        # creating Ceil
        bpy.ops.object.mode_set(mode='OBJECT')
        # grab & move to bottom
        bpy.ops.transform.translate(value=(-0, -0, -1.5), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 2.95), "orient_type": 'GLOBAL', "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type": 'GLOBAL', "constraint_axis": (False, False, True), "mirror": True, "use_proportional_edit": False, "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1,"use_proportional_connected": False, "use_proportional_projected": False, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "gpencil_strokes": False, "cursor_transform": False, "texture_space": False, "remove_on_cancel": False, "release_confirm": False, "use_accurate": False, "use_automerge_and_split": False})
        ceil_object = context.view_layer.objects.active
        ceil_object.name = str(halls) + '.Ceil'
        ceil_object.data.name = str(halls) + '.Ceil'

        # add thickness
        # wall_object = bpy.data.objects['Plane']
        wall_object.modifiers["Solidify"].thickness = 0.2
        wall_object.modifiers["Solidify"].solidify_mode = 'NON_MANIFOLD'
        # bpy.ops.object.modifier_apply()

        # naming walls
        wall_object.name = str(halls) + '.Walls'
        wall_object.data.name = str(halls) + '.Walls'
        bpy.data.objects[ceil_object.data.name].select_set(False)
        bpy.data.objects[wall_object.data.name].select_set(True)
        

        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        bpy.ops.transform.resize(value=(1, 1, 0.03), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        skirt_obj = bpy.data.objects[wall_object.data.name+".001"]
        skirt_obj.name = str(halls)+".Floor Skirt"
        bpy.context.view_layer.objects.active = skirt_obj

        # # # add thickness
        skirt_obj.modifiers["Solidify"].thickness = 0.25
        skirt_obj.modifiers["Solidify"].offset = 0
        skirt_obj.modifiers["Solidify"].solidify_mode = 'NON_MANIFOLD'

        for obj in [skirt_obj,wall_object]:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_apply(modifier="Solidify")
        bpy.context.view_layer.objects.active = wall_object

        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].operation = 'UNION'
        bpy.context.object.modifiers["Boolean"].object = bpy.data.objects[skirt_obj.name]
        bpy.ops.object.modifier_apply(modifier="Boolean")

        #materialising 
        bpy.ops.object.mode_set(mode='EDIT')

        root_dir = "C:\\Program Files\\Blender Foundation\\Blender 2.93\\2.93\\scripts\\addons\\otb\\"
        floor = {"Base Color": "", "Roughness": "", "Normal": "", "dir": ""}
        ceil = {"Base Color": "", "Roughness": "", "Normal": "", "dir": ""}
        wall = {"Base Color": "", "Roughness": "", "Normal": "", "dir": ""}

        objects = {floor_object.name: floor, ceil_object.name: ceil, wall_object.name: wall}
        self.init(root_dir, floor, ceil, wall)
        self.setTextureImage(objects)
        self.setMaterial(objects,halls)
        return {'FINISHED'}

    def init(self,root_dir, floor, ceil, wall):
        for file in glob.glob(root_dir + '*wall*'):
            # global wall_dir
            wall['dir'] = file + "\\"

        for file in glob.glob(root_dir + '*ceil*'):
            # global ceil_dir
            ceil['dir'] = file + "\\"

        for file in glob.glob(root_dir + '*floor*'):
            # global floor_dir
            floor['dir'] = file + "\\"
    def setTextureImage(self,objects):
        for obname, ob in objects.items():
            for file in glob.glob(ob["dir"]+"*color*"):
                ob['Base Color'] = file
            for file in glob.glob(ob["dir"]+"*rough*"):
                ob['Roughness'] = file
            for file in glob.glob(ob["dir"]+"*norm*"):
                ob['Normal'] = file

    def setMaterial(self,objects,halls):
        for obname, ob in objects.items():
            # print(ob)
            ob_mat = bpy.data.materials.new(name=obname+"_mat")
            ob_mat.use_nodes = True
            if obname == str(halls) + '.Floor':
                value_shader_node = ob_mat.node_tree.nodes.new('ShaderNodeValue')
                tex_cord_shader_node = ob_mat.node_tree.nodes.new(
                    'ShaderNodeTexCoord')
                mapping_shader_node = ob_mat.node_tree.nodes.new(
                    'ShaderNodeMapping')
                print(value_shader_node, tex_cord_shader_node, mapping_shader_node)
                ob_mat.node_tree.links.new(
                    value_shader_node.outputs['Value'], mapping_shader_node.inputs['Scale'])
                ob_mat.node_tree.links.new(
                    tex_cord_shader_node.outputs['UV'], mapping_shader_node.inputs['Vector'])
            elif obname == str(halls) + '.Walls':
                wall_mat = bpy.data.materials.new(name=obname+"_mat")
                wall_mat.use_nodes = True

                # wall_mat = bpy.context.object.data.materials['Walls_mat']
                texCordNode = wall_mat.node_tree.nodes.new('ShaderNodeTexCoord')
                fNoiseTexNode = wall_mat.node_tree.nodes.new('ShaderNodeTexNoise')
                sNoiseTexNode = wall_mat.node_tree.nodes.new('ShaderNodeTexNoise')
                wall_mat.node_tree.links.new(texCordNode.outputs['Object'],fNoiseTexNode.inputs['Vector'])
                wall_mat.node_tree.links.new(texCordNode.outputs['Object'], sNoiseTexNode.inputs['Vector'])
                fNoiseTexNode.inputs['Scale'].default_value = 1.5
                fNoiseTexNode.inputs['Roughness'].default_value = .383
                sNoiseTexNode.inputs['Scale'].default_value = 400
                sNoiseTexNode.inputs['Roughness'].default_value = .717

                fColorRamp = wall_mat.node_tree.nodes.new('ShaderNodeValToRGB')
                fColorRamp.color_ramp.elements[0].position= .333
                fColorRamp.color_ramp.elements[0].color = (0.517455, 0.517455, 0.517455, 1)
                wall_mat.node_tree.links.new(fNoiseTexNode.outputs['Fac'], fColorRamp.inputs['Fac'])

                sColorRamp = wall_mat.node_tree.nodes.new('ShaderNodeValToRGB')
                sColorRamp.color_ramp.elements[0].position= .352

                wall_mat.node_tree.links.new(sNoiseTexNode.outputs['Fac'], sColorRamp.inputs['Fac'])

                # principledBsdfNode = wall_mat.node_tree.nodes.new["ShaderNodeBsdfPrincipled"]
                principledBsdfNode = wall_mat.node_tree.nodes['Principled BSDF']
                wall_mat.node_tree.links.new(fColorRamp.outputs['Color'], principledBsdfNode.inputs['Roughness'])

                bumpNode = wall_mat.node_tree.nodes.new('ShaderNodeBump')
                bumpNode.inputs['Strength'].default_value= .35

                wall_mat.node_tree.links.new(sColorRamp.outputs['Color'], bumpNode.inputs['Normal'])
                wall_mat.node_tree.links.new(bumpNode.outputs['Normal'], principledBsdfNode.inputs['Normal'])

            bsdf = ob_mat.node_tree.nodes["Principled BSDF"]
            for texImgName, texImgAddr in ob.items():
                if obname == str(halls) + '.Walls' or (texImgName == "dir"):
                    continue
                texImage = ob_mat.node_tree.nodes.new('ShaderNodeTexImage')
                texImage.image = bpy.data.images.load(texImgAddr)
                if texImgName == 'Normal':
                    normalMapTex = ob_mat.node_tree.nodes.new(
                        'ShaderNodeNormalMap')
                    ob_mat.node_tree.links.new(
                        normalMapTex.inputs['Color'], texImage.outputs['Color'])
                    ob_mat.node_tree.links.new(
                        bsdf.inputs[texImgName], normalMapTex.outputs[texImgName])
                else:
                    ob_mat.node_tree.links.new(
                        bsdf.inputs[texImgName], texImage.outputs['Color'])
                if obname == str(halls) + '.Floor':
                    ob_mat.node_tree.links.new(
                        mapping_shader_node.outputs['Vector'], texImage.inputs['Vector'])
            curOb = bpy.data.objects[obname]
            # Assign it to object
            if curOb.data.materials:
                curOb.data.materials[0] = ob_mat
            else:
                curOb.data.materials.append(ob_mat)
        bpy.data.materials[str(halls)+".Floor_mat"].node_tree.nodes["Value"].outputs[0].default_value = 41
    # nodes = [ShaderNodeValue , ShaderNodeTexCoord , ShaderNodeMapping ] 
            

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
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

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

        # creating skirt
        # add plane
        bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0, 0, 1.5), scale=(1, 1, 1))

        # scale plane
        bpy.ops.transform.resize(value=(50, 50, 50), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True,use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

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

        extra_plane.name = str(halls) + '.Floor Skirt'  # object rename
        extra_plane.data.name = str(halls) + '.Floor Skirt'  # mesh rename
        skirt_object = bpy.data.objects['1.Floor Skirt']
        bpy.context.view_layer.objects.active = bpy.data.objects['1.Floor Skirt']
        bpy.ops.mesh.separate(type='LOOSE')

        floorSkirtObjects = []

        for obj in bpy.data.objects:
            if obj.name.find('Floor Skirt')>=0:
                floorSkirtObjects.append(obj)

        # #converting to curve
        bpy.ops.object.editmode_toggle()

        for obj in floorSkirtObjects:
            bpy.ops.object.convert(target='CURVE')
        bpy.ops.transform.translate(value=(-0, -0, -1.5), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 3.0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        ceilSkirtObjects = bpy.context.selected_objects

        #renaming ceil skirt objects
        for i,obj in enumerate(ceilSkirtObjects):
            obj.name = str(halls) + '.Ceil Skirt'
            obj.name += '.00' + str(i) if i>0 else ''

      
        file_path = 'skirt.blend'
        inner_path = "Curve"
        floor_profile_obj = 'floor_profile'
        ceil_profile_obj = 'ceil_profile'
        
        bpy.ops.wm.append(
            filepath=os.path.join(file_path, inner_path, floor_profile_obj),
            directory=os.path.join(file_path, inner_path),
            filename=floor_profile_obj
            )
        bpy.ops.wm.append(
            filepath=os.path.join(file_path, inner_path, ceil_profile_obj),
            directory=os.path.join(file_path, inner_path),
            filename=ceil_profile_obj
            )
        # naming walls
        wall_object.name = str(halls) + '.Walls'
        wall_object.data.name = str(halls) + '.Walls'
        bpy.data.objects[ceil_object.data.name].select_set(False)
        bpy.data.objects[wall_object.data.name].select_set(True)
        
        #materialising 
        # bpy.ops.object.mode_set(mode='EDIT')

        root_dir = "C:\\Program Files\\Blender Foundation\\Blender 2.93\\2.93\\scripts\\addons\\otb\\"
        floor = {"Base Color": "", "Roughness": "", "Normal": "", "dir": ""}
        # ceil = {"Normal": "", "dir": ""}
        # wall = {"Normal": "", "dir": ""}
        ceil = {"Base Color": "","Specular": "", "Normal": "", "dir": ""}
        wall = {"Base Color": "","Specular": "", "Normal": "", "dir": ""}

        texObjects = {floor_object.name: floor, ceil_object.name: ceil, wall_object.name: wall}
        matObjects = {floor_object.name: floor, ceil_object.name: ceil, wall_object.name: wall}
        self.init(root_dir, floor, ceil, wall)
        self.setTextureImage(texObjects)
        self.setMaterial(matObjects,halls)
        self.doSkirting(floorSkirtObjects, ceilSkirtObjects)
        return {'FINISHED'}

    def doSkirting(self,floorSkirtObjects, ceilSkirtObjects):
        for fsObj in floorSkirtObjects:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = fsObj        # bpy.context.space_data.context = 'DATA'
            # bpy.data.objects['1.Floor Skirt'].select_set(True)
            bpy.context.object.data.bevel_mode = 'OBJECT'
            bpy.context.object.data.bevel_object = bpy.data.objects["floor_profile"]

        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['floor_profile'].select_set(True)
        bpy.ops.transform.resize(value=(0.01, 0.01, 0.01), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        for csObj in ceilSkirtObjects:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = csObj        # bpy.context.space_data.context = 'DATA'
            # bpy.data.objects['1.Ceil Skirt'].select_set(True)
            bpy.context.object.data.bevel_mode = 'OBJECT'
            bpy.context.object.data.bevel_object = bpy.data.objects["ceil_profile"]
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['ceil_profile'].select_set(True)
        bpy.ops.transform.resize(value=(100, 100, 100), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        # bpy.context.view_layer.objects.active = bpy.data.objects['floor_profile']

        # bpy.ops.transform.resize(value=(0.001, 0.001, 0.001), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        # bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        # bpy.context.view_layer.objects.active = bpy.data.objects['ceil_profile']
        # bpy.ops.transform.resize(value=(0.001, 0.001, 0.001), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        # bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        pass


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
            for file in glob.glob(ob["dir"]+"*norm*"):
                ob['Normal'] = file

            for file in glob.glob(ob["dir"]+"*color*"):
                ob['Base Color'] = file
            if ob['Base Color'] == "":
                for file in glob.glob(ob["dir"]+"*diffuse*"):
                    ob['Base Color'] = file
            for file in glob.glob(ob["dir"]+"*rough*"):
                ob['Roughness'] = file
            if obname.find('Floor')>=0:
                continue
            for file in glob.glob(ob["dir"]+"*specular*"):
                ob['Specular'] = file

    def setMaterial(self,objects,halls):
        for obname, ob in objects.items():
            # print(ob)
            ob_mat = bpy.data.materials.new(name=obname+"_mat")
            ob_mat.use_nodes = True
            bsdf = ob_mat.node_tree.nodes["Principled BSDF"]
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
            else:
                wall_mat = bpy.data.materials.new(name=obname+"_mat")
                wall_mat.use_nodes = True
                wall_mat = ob_mat
                
                texCordNode = wall_mat.node_tree.nodes.new('ShaderNodeTexCoord')
                valNode = wall_mat.node_tree.nodes.new('ShaderNodeValue')
                valNode.outputs[0].default_value=10
                # valNode = wall_mat.node_tree.nodes["Value"].outputs[0].default_value = 10
                mapping_shader_node = ob_mat.node_tree.nodes.new(
                    'ShaderNodeMapping')
                ob_mat.node_tree.links.new(texCordNode.outputs['UV'], mapping_shader_node.inputs['Vector'])
                ob_mat.node_tree.links.new(valNode.outputs['Value'], mapping_shader_node.inputs['Scale'])

                fColorRamp = wall_mat.node_tree.nodes.new('ShaderNodeValToRGB')
                fColorRamp.color_ramp.elements[0].position= .333
                fColorRamp.color_ramp.elements[0].color = (0.517455, 0.517455, 0.517455, 1)
                # baseColor = wall_mat.node_tree.nodes['Image Texture']
                wall_mat.node_tree.links.new(fColorRamp.outputs['Color'], bsdf.inputs['Base Color'])

            for texImgName, texImgAddr in ob.items():
                if (texImgName == "dir"):
                    continue
                texImage = ob_mat.node_tree.nodes.new('ShaderNodeTexImage')
                texImage.image = bpy.data.images.load(texImgAddr)
                if (obname != str(halls) + '.Floor' and texImgName == "Base Color"):
                    ob_mat.node_tree.links.new(texImage.outputs['Color'], fColorRamp.inputs['Fac'])
                    ob_mat.node_tree.links.new(fColorRamp.outputs['Color'], bsdf.inputs['Base Color'])

                if texImgName == 'Normal':
                    normalMapTex = ob_mat.node_tree.nodes.new(
                        'ShaderNodeNormalMap')
                    ob_mat.node_tree.links.new(
                        normalMapTex.inputs['Color'], texImage.outputs['Color'])
                    ob_mat.node_tree.links.new(
                        bsdf.inputs[texImgName], normalMapTex.outputs[texImgName])
                elif (texImgName == 'Specular' and obname != str(halls) + '.Floor') or obname == str(halls) + '.Floor':
                    ob_mat.node_tree.links.new(
                        bsdf.inputs[texImgName], texImage.outputs['Color'])
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
            

import bpy
import bmesh
import os
import glob

from bpy import context, data, ops

bpy.ops.object.mode_set(mode='EDIT')

root_dir = "C:\\Program Files\\Blender Foundation\\Blender 2.93\\2.93\\scripts\\addons\\otb\\"
floor = {"Base Color": "", "Roughness": "", "Normal": "", "dir": ""}
ceil = {"Base Color": "", "Roughness": "", "Normal": "", "dir": ""}
wall = {"Base Color": "", "Roughness": "", "Normal": "", "dir": ""}

objects = {'Floor': floor, 'Ceil': ceil, 'Walls': wall}


def init(root_dir, floor, ceil, wall):
    for file in glob.glob(root_dir + '*wall*'):
        # global wall_dir
        wall['dir'] = file + "\\"

    for file in glob.glob(root_dir + '*ceil*'):
        # global ceil_dir
        ceil['dir'] = file + "\\"

    for file in glob.glob(root_dir + '*floor*'):
        # global floor_dir
        floor['dir'] = file + "\\"


init(root_dir, floor, ceil, wall)


def setTextureImage(objects):
    for obname, ob in objects.items():
        for file in glob.glob(ob["dir"]+"*color*"):
            ob['Base Color'] = file
        for file in glob.glob(ob["dir"]+"*rough*"):
            ob['Roughness'] = file
        for file in glob.glob(ob["dir"]+"*norm*"):
            ob['Normal'] = file


setTextureImage(objects)


def setMaterial(objects):
    for obname, ob in objects.items():
        # print(ob)
        ob_mat = bpy.data.materials.new(name=obname+"_mat")
        ob_mat.use_nodes = True
        if obname == 'Floor':
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

        bsdf = ob_mat.node_tree.nodes["Principled BSDF"]
        for texImgName, texImgAddr in ob.items():
            if texImgName == "dir":
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
            if obname == 'Floor':
                ob_mat.node_tree.links.new(
                    mapping_shader_node.outputs['Vector'], texImage.inputs['Vector'])
        curOb = bpy.data.objects[obname]
        # Assign it to object
        if curOb.data.materials:
            curOb.data.materials[0] = ob_mat
        else:
            curOb.data.materials.append(ob_mat)
    bpy.data.materials["Floor_mat"].node_tree.nodes["Value"].outputs[0].default_value = 41


setMaterial(objects)

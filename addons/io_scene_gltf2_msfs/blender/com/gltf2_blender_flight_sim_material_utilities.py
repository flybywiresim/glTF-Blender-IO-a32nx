# Copyright 2021 FlyByWire Simulations.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import bpy
import numpy
from bpy.types import Material
from ..com.gltf2_blender_material_helpers import get_gltf_node_name

def check_if_is_linked_to_active_output(shader_socket):
    """
    Locates the node that is connected to the material output
    """
    for link in shader_socket.links:
        if isinstance(link.to_node, bpy.types.ShaderNodeOutputMaterial) and link.to_node.is_active_output is True:
            return True

        if len(link.to_node.outputs) > 0: # ignore non active output, not having output sockets
            ret = check_if_is_linked_to_active_output(link.to_node.outputs[0]) # recursive until find an output material node
            if ret is True:
                return True

    return False

def get_bsdf_node(mat):
    """
    Locate the BSDF node in the material's node tree
    """
    if mat.node_tree and mat.use_nodes:
        nodes = [n for n in mat.node_tree.nodes if isinstance(n, bpy.types.ShaderNodeBsdfPrincipled) and not n.mute]
        nodes = [node for node in nodes if check_if_is_linked_to_active_output(node.outputs[0])]
        if nodes:
            return nodes[0]
    return None

def is_node_linked(node):
    """
    Checks if the node has any inputs or outputs
    """
    return any([link.is_linked for link in [input for input in node.inputs]]) or any([link.is_linked for link in [output for output in node.outputs]])


def clear_socket(mat, socket): # rename this?
    """
    Removes all nodes/links that are going into a socket.
    Something important to note is that it does not remove a node that has connections to other sockets
    """
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    if socket is None:
        return

    # Clear links and nodes
    for link in socket.links:
        for input in link.from_node.inputs:
            clear_socket(mat, input) # recursive until there are no more nodes/connections going to the socket
        node = link.from_node
        links.remove(link)
        if not is_node_linked(node):
            nodes.remove(node)

def is_opaque(mat):
    return mat.msfs_alpha_mode is None or mat.msfs_alpha_mode == 'OPAQUE'

def calc_locations(mat):
    """Calculate locations to place each bit of the node graph at."""
    # Lay the blocks out top-to-bottom, aligned on the right
    x = -200
    y = 700
    height = 460  # height of each block
    locs = {}

    locs['base_color'] = (x, y)
    y -= height + 150 # give more space for detail textures

    locs['metallic_roughness'] = (x, y)
    y -= height + 150 # give more space for detail textures

    locs['clearcoat'] = (x, y)
    y -= height # the dirt texture is the clearcoat texture and roughness

    locs['blend_mask'] = (x - 650, y) # move the blend mask a bit back to make space
    y -= height
        
    locs['emission'] = (x, y)
    y -= height

    locs['normal'] = (x, y)
    y -= height + 150 # give more space for detail textures

    locs['occlusion'] = (x, y)
    y -= height + 150 # give more space for detail textures

    locs['wetness_ao'] = (x, y)
    y -= height

    return locs

def get_socket(blender_material: bpy.types.Material, name: str):
    """
    For a given material input name, retrieve the corresponding node tree socket.

    :param blender_material: a blender material for which to get the socket
    :param name: the name of the socket
    :return: a blender NodeSocket
    """
    if blender_material.node_tree and blender_material.use_nodes:
        #i = [input for input in blender_material.node_tree.inputs]
        #o = [output for output in blender_material.node_tree.outputs]
        if name == 'Emissive':
            # Check for a dedicated Emission node first, it must supersede the newer built-in one
            # because the newer one is always present in all Principled BSDF materials.
            type = bpy.types.ShaderNodeEmission
            name = 'Color'
            nodes = [n for n in blender_material.node_tree.nodes if isinstance(n, type) and not n.mute]
            nodes = [node for node in nodes if check_if_is_linked_to_active_output(node.outputs[0])]
            inputs = sum([[input for input in node.inputs if input.name == name] for node in nodes], [])
            if inputs:
                return inputs[0]
            # If a dedicated Emission node was not found, fall back to the Principled BSDF Emission socket.
            name = 'Emission'
            type = bpy.types.ShaderNodeBsdfPrincipled
        elif name == 'Background':
            type = bpy.types.ShaderNodeBackground
            name = 'Color'
        else:
            type = bpy.types.ShaderNodeBsdfPrincipled
        nodes = [n for n in blender_material.node_tree.nodes if isinstance(n, type) and not n.mute]
        nodes = [node for node in nodes if check_if_is_linked_to_active_output(node.outputs[0])]
        inputs = sum([[input for input in node.inputs if input.name == name] for node in nodes], [])
        if inputs:
            return inputs[0]

    return None


def get_socket_old(blender_material: bpy.types.Material, name: str):
    """
    For a given material input name, retrieve the corresponding node tree socket in the special glTF node group.

    :param blender_material: a blender material for which to get the socket
    :param name: the name of the socket
    :return: a blender NodeSocket
    """
    gltf_node_group_name = get_gltf_node_name().lower()
    if blender_material.node_tree and blender_material.use_nodes:
        nodes = [n for n in blender_material.node_tree.nodes if \
            isinstance(n, bpy.types.ShaderNodeGroup) and \
            (n.node_tree.name.startswith('glTF Metallic Roughness') or n.node_tree.name.lower() == gltf_node_group_name)]
        inputs = sum([[input for input in node.inputs if input.name == name] for node in nodes], [])
        if inputs:
            return inputs[0]

    return None

def previous_socket(socket):
    while True:
        if not socket.is_linked:
            return None

        from_socket = socket.links[0].from_socket

        # Skip over reroute nodes
        if from_socket.node.type == 'REROUTE':
            socket = from_socket.node.inputs[0]
            continue

        return from_socket

def previous_node(socket):
    prev_socket = previous_socket(socket)
    if prev_socket is not None:
        return prev_socket.node
    return None

def get_rgb_socket(socket):
    """
    This searches for an RGB socket from the provided socket.
    It first checks if the current socket is an RGB socket, and if not, check the node connecting
    to the socket.

    :param socket: a blender NodeSocket
    """
    if not socket.is_linked: # The socket provided is the factor socket
        return socket

    node = previous_node(socket)
    if node is not None:
        x1, x2 = None, None
        if node.type == 'MIX_RGB' and node.blend_type == 'MULTIPLY':
            # TODO: handle factor in inputs[0]?
            x1 = get_root_rgb_socket(node.inputs[1])
            x2 = get_root_rgb_socket(node.inputs[2])
        if x1 is not None and x2 is None: return x1
        if x2 is not None and x1 is None: return x2

    return None

def get_root_rgb_socket(socket):
    """
    Similar to get_rgb_socket, but this checks if there is an RGB node going into the socket,
    and if there is, it returns the socket. If there isn't, return the socket provided
    """
    if not socket.is_linked:
        if socket.type != 'RGBA': return None
        return socket

    # Handle connection to a constant RGB node
    prev_node = previous_node(socket)
    if prev_node is not None:
        if prev_node.type == 'RGB':
            return prev_node.outputs[0]

    return None

def make_settings_node(mat):
    """
    Make a Group node with a hookup for Occlusion and Wetness AO. No effect in Blender, but
    used to tell the exporter what the occlusion map should be.
    """
    node = mat.node_tree.nodes.new('ShaderNodeGroup')
    node.node_tree = get_settings_group()
    return node

def get_settings_group():
    gltf_node_group_name = get_gltf_node_name()
    if gltf_node_group_name in bpy.data.node_groups:
        gltf_node_group = bpy.data.node_groups[gltf_node_group_name]
    else:
        # Create a new node group
        gltf_node_group = bpy.data.node_groups.new(gltf_node_group_name, 'ShaderNodeTree')
        gltf_node_group.inputs.new('NodeSocketFloat', 'Occlusion')
        gltf_node_group.inputs.new('NodeSocketFloat', 'Wetness AO')
        gltf_node_group.nodes.new('NodeGroupOutput')
        gltf_node_group_input = gltf_node_group.nodes.new('NodeGroupInput')
        gltf_node_group_input.location = -200, 0
    return gltf_node_group


def is_detail_mix(node):
    """
    Checks if a detail mix connects to the current node

    :param node: a blender Node
    """
    if isinstance(node, bpy.types.ShaderNodeMixRGB):
        if node.inputs[2].is_linked:
            if isinstance(previous_node(node.inputs[2]), bpy.types.ShaderNodeTexImage):
                return True
    return False

def get_detail_mix_factor_socket(socket):
    """
    Get the detail mix factor socket for a given socket type

    :param socket: a blender NodeSocket
    """

    prev_node = previous_node(socket)
    if prev_node is None:
        return None

    if isinstance(prev_node, bpy.types.ShaderNodeSeparateRGB): # this is either Metallic Roughness or Occlusion
        prev_node = previous_node(prev_node.inputs[0]) # we get the texture going into the separate rgb node
        if is_detail_mix(prev_node):
            return prev_node.inputs[0]
    else: # this is either Base Color or Normal
        # first check if the current node is the detail mix factor
        if is_detail_mix(prev_node):
            return prev_node.inputs[0]
        else: # we search one more node back
            prev_node = previous_node(prev_node.inputs[1]) # assume the first color input is the mix node
            if is_detail_mix(prev_node):
                return prev_node.inputs[0]

    return None
        


def get_detail_factor_sockets(mat):
    """
    This function finds all detail mix factor sockets for the given material.

    :param blender_material: a blender material for which to get the sockets
    :return: a list of blender NodeSockets: detail_base_color_factor_socket, detail_comp_factor_socket, detail_occlusion_factor_socket, detail_normal_factor_socket
    """

    bsdf_node = get_bsdf_node(mat)

    base_color_texture = mat.msfs_base_color_texture
    detail_base_color_texture = mat.msfs_detail_color_texture

    comp_texture = mat.msfs_comp_texture
    detail_comp_texture = mat.msfs_detail_comp_texture

    normal_texture = mat.msfs_normal_texture
    detail_normal_texture = mat.msfs_detail_normal_texture

    detail_base_color_factor_socket = None
    detail_comp_factor_socket = None
    detail_occlusion_factor_socket = None
    detail_normal_factor_socket = None

    # Get base color detail mix socket
    if base_color_texture is not None and detail_base_color_texture is not None:
        detail_base_color_factor_socket = get_detail_mix_factor_socket(bsdf_node.inputs['Base Color'])

    # Get comp and occlusion detail mix socket
    if comp_texture is not None and detail_comp_texture is not None:
        if get_detail_mix_factor_socket(bsdf_node.inputs['Metallic']) == get_detail_mix_factor_socket(bsdf_node.inputs['Roughness']): # make sure the factor socket is the same for both metallic and roughness
            detail_comp_factor_socket = get_detail_mix_factor_socket(bsdf_node.inputs['Metallic']) # set to metallic since it's the same as roughness and metallic comes first

        detail_occlusion_factor_socket = get_detail_mix_factor_socket(get_socket_old(mat, 'Occlusion'))
    
    # Get normal detail mix socket
    if normal_texture is not None and detail_normal_texture is not None:
        detail_normal_factor_socket = get_detail_mix_factor_socket(bsdf_node.inputs['Normal'])

    return detail_base_color_factor_socket, detail_comp_factor_socket, detail_occlusion_factor_socket, detail_normal_factor_socket

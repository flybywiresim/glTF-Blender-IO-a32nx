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
import numpy as np
from bpy.types import Material
from ..com.gltf2_blender_material_helpers import get_gltf_node_name
from . import gltf2_blender_flight_sim_material_utilities as utilities

### Material Creation
def create_material(self, context):
    if not self.is_import:
        self.use_nodes = True
        while self.node_tree.nodes: # clear all nodes
            self.node_tree.nodes.remove(self.node_tree.nodes[0])

        bsdf_node = self.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf_node.location = 10, 300
        
        make_output_nodes(
            self,
            location=(250, 260),
            shader_socket=bsdf_node.outputs[0],
            make_emission_socket=False,
            make_alpha_socket=False,
        )

# => [Add Emission] => [Mix Alpha] => [Material Output]
def make_output_nodes(
    mat,
    location,
    shader_socket,
    make_emission_socket,
    make_alpha_socket,
):
    """
    Creates the Material Output node and connects shader_socket to it.
    If requested, it can also create places to hookup the emission/alpha
    in between shader_socket and the Output node too.

    :return: a pair containing the sockets you should put emission and alpha
    in (None if not requested).
    """
    x, y = location
    emission_socket = None
    alpha_socket = None

    # Create an Emission node and add it to the shader.
    if make_emission_socket:
        # Emission
        node = mat.node_tree.nodes.new('ShaderNodeEmission')
        node.location = x + 50, y + 250
        # Inputs
        emission_socket = node.inputs[0]
        # Outputs
        emission_output = node.outputs[0]

        # Add
        node = mat.node_tree.nodes.new('ShaderNodeAddShader')
        node.location = x + 250, y + 160
        # Inputs
        mat.node_tree.links.new(node.inputs[0], emission_output)
        mat.node_tree.links.new(node.inputs[1], shader_socket)
        # Outputs
        shader_socket = node.outputs[0]

        if make_alpha_socket:
            x += 200
            y += 175
        else:
            x += 380
            y += 125

    # Mix with a Transparent BSDF. Mixing factor is the alpha value.
    if make_alpha_socket:
        # Transparent BSDF
        node = mat.node_tree.nodes.new('ShaderNodeBsdfTransparent')
        node.location = x + 100, y - 350
        # Outputs
        transparent_out = node.outputs[0]

        # Mix
        node = mat.node_tree.nodes.new('ShaderNodeMixShader')
        node.location = x + 340, y - 180
        # Inputs
        alpha_socket = node.inputs[0]
        mat.node_tree.links.new(node.inputs[1], transparent_out)
        mat.node_tree.links.new(node.inputs[2], shader_socket)
        # Outputs
        shader_socket = node.outputs[0]


        x += 480
        y -= 210

    # Material output
    node = mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
    node.location = x + 70, y + 10
    # Outputs
    mat.node_tree.links.new(node.inputs[0], shader_socket)

    return emission_socket, alpha_socket

### Texture Functions
def texture(
    mat,
    texture,
    location, # Upper-right corner of the TexImage node
    label, # Label for the TexImg node
    color_socket=None,
    alpha_socket=None,
    is_data=False,
):
    """Creates nodes for a TextureInfo and hooks up the color/alpha outputs."""
    x, y = location

    # Image Texture
    tex_img = mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex_img.location = x - 240, y
    tex_img.label = label
    tex_img.image = texture

    # Set colorspace for data images
    if is_data:
        if tex_img.image:
            tex_img.image.colorspace_settings.is_data = True

    # Outputs
    if color_socket is not None:
        mat.node_tree.links.new(color_socket, tex_img.outputs['Color'])
    if alpha_socket is not None:
        mat.node_tree.links.new(alpha_socket, tex_img.outputs['Alpha'])

    return tex_img


#      [Texture] => [Mix Colors] => [Color Factor] =>
# [Vertex Color] => [Mix Alphas] => [Alpha Factor] =>
def base_color(
    mat,
    location,
    color_socket,
    alpha_socket=None,
):
    """Handle base color (= baseColorTexture * vertexColor * baseColorFactor)."""
    x, y = location
    base_color_factor = list(mat.msfs_base_color_factor)
    base_color_texture = mat.msfs_base_color_texture
    detail_color_texture = mat.msfs_detail_color_texture

    if base_color_factor is None:
        base_color_factor = [1, 1, 1, 1]

    if base_color_texture is None and detail_color_texture is None:
        color_socket.default_value = base_color_factor[:3] + [1]
        if alpha_socket is not None:
            alpha_socket.default_value = base_color_factor[3]
        return

    # Mix in base color factor
    needs_color_factor = base_color_factor[:3] != [1, 1, 1]
    needs_alpha_factor = base_color_factor[3] != 1.0 and alpha_socket is not None
    if needs_color_factor or needs_alpha_factor:
        if needs_color_factor:
            node = mat.node_tree.nodes.new('ShaderNodeMixRGB')
            node.label = 'Color Factor'
            node.location = x - 140, y
            node.blend_type = 'MULTIPLY'
            # Outputs
            mat.node_tree.links.new(color_socket, node.outputs[0])
            # Inputs
            node.inputs['Fac'].default_value = 1.0
            color_socket = node.inputs['Color1']
            node.inputs['Color2'].default_value = base_color_factor[:3] + [1]

        if needs_alpha_factor:
            node = mat.node_tree.nodes.new('ShaderNodeMath')
            node.label = 'Alpha Factor'
            node.location = x - 140, y - 200
            # Outputs
            mat.node_tree.links.new(alpha_socket, node.outputs[0])
            # Inputs
            node.operation = 'MULTIPLY'
            alpha_socket = node.inputs[0]
            node.inputs[1].default_value = base_color_factor[3]

        x -= 200

    # Mix detail map
    detail_color_socket = None
    base_alpha_socket = None # We need this in case there is an alpha mix, because we still want to keep the reference to the alpha socket on the BSDF node
    detail_alpha_socket = None
    if base_color_texture is not None and detail_color_texture is not None:
        if color_socket is not None:
            node = mat.node_tree.nodes.new('ShaderNodeMixRGB')
            node.label = 'Detail Color Mix'
            node.location = (x - 140, y) if alpha_socket is None else (x - 140, y + 100)
            node.blend_type = 'MULTIPLY'
            # Outputs
            mat.node_tree.links.new(color_socket, node.outputs[0])
            # Inputs
            node.inputs['Fac'].default_value = 1.0
            color_socket = node.inputs['Color1']
            detail_color_socket = node.inputs['Color2']
            node.inputs['Color2'].default_value = [1, 1, 1, 1]

        if alpha_socket is not None:
            node = mat.node_tree.nodes.new('ShaderNodeMixRGB')
            node.label = 'Detail Alpha Mix'
            node.location = (x - 140, y) if alpha_socket is None else (x - 140, y - 100)
            node.blend_type = 'MULTIPLY'
            # Outputs
            mat.node_tree.links.new(alpha_socket, node.outputs[0])
            # Inputs
            node.inputs['Fac'].default_value = 1.0
            base_alpha_socket = node.inputs['Color1']
            detail_alpha_socket = node.inputs['Color2']
            node.inputs['Color2'].default_value = [1, 1, 1, 1]

        x -= 200

    if base_alpha_socket is None:
        base_alpha_socket = alpha_socket

    # Texture
    if base_color_texture is not None:
        texture(
            mat,
            texture=base_color_texture,
            label='BASE COLOR',
            location=(x, y) if detail_color_texture is None else (x, y + 150),
            color_socket=color_socket,
            alpha_socket=base_alpha_socket,
        )

    if detail_color_texture is not None:
        texture(
            mat,
            texture=detail_color_texture,
            label='DETAIL COLOR',
            location=(x, y) if base_color_texture is None else (x, y - 150),
            color_socket=detail_color_socket if base_color_texture is not None else color_socket,
            alpha_socket=detail_alpha_socket if base_color_texture is not None else base_alpha_socket,
        )

# [Texture] => [Separate GB] => [Metal/Rough Factor] =>
def metallic_roughness(
    mat,
    location,
    metallic_socket,
    roughness_socket
):
    x, y = location

    comp_texture = mat.msfs_comp_texture
    detail_comp_texture = mat.msfs_detail_comp_texture
    metal_factor = mat.msfs_metallic_factor
    rough_factor = mat.msfs_roughness_factor

    if metal_factor is None:
        metal_factor = 1.0
    if rough_factor is None:
        rough_factor = 1.0

    if comp_texture is None and detail_comp_texture is None:
        metallic_socket.default_value = metal_factor
        roughness_socket.default_value = rough_factor
        return

    if metal_factor != 1.0 or rough_factor != 1.0:
        # Mix metal factor
        if metal_factor != 1.0:
            node = mat.node_tree.nodes.new('ShaderNodeMath')
            node.label = 'Metallic Factor'
            node.location = x - 140, y
            node.operation = 'MULTIPLY'
            # Outputs
            mat.node_tree.links.new(metallic_socket, node.outputs[0])
            # Inputs
            metallic_socket = node.inputs[0]
            node.inputs[1].default_value = metal_factor

        # Mix rough factor
        if rough_factor != 1.0:
            node = mat.node_tree.nodes.new('ShaderNodeMath')
            node.label = 'Roughness Factor'
            node.location = x - 140, y - 200
            node.operation = 'MULTIPLY'
            # Outputs
            mat.node_tree.links.new(roughness_socket, node.outputs[0])
            # Inputs
            roughness_socket = node.inputs[0]
            node.inputs[1].default_value = rough_factor

        x -= 200

    # Separate RGB
    node = mat.node_tree.nodes.new('ShaderNodeSeparateRGB')
    node.location = x - 150, y - 75
    # Outputs
    mat.node_tree.links.new(metallic_socket, node.outputs['B'])
    mat.node_tree.links.new(roughness_socket, node.outputs['G'])
    # Inputs
    color_socket = node.inputs[0]

    x -= 200

    # Mix detail map
    detail_color_socket = None
    if comp_texture is not None and detail_comp_texture is not None:
        node = mat.node_tree.nodes.new('ShaderNodeMixRGB')
        node.label = 'Detail Comp Mix'
        node.location = x - 140, y
        node.blend_type = 'MULTIPLY'
        # Outputs
        mat.node_tree.links.new(color_socket, node.outputs[0])
        # Inputs
        node.inputs['Fac'].default_value = 1.0
        color_socket = node.inputs['Color1']
        detail_color_socket = node.inputs['Color2']
        node.inputs['Color2'].default_value = [1, 1, 1, 1]

        x -= 200

    if comp_texture is not None:
        texture(
            mat,
            texture=comp_texture,
            label='METALLIC ROUGHNESS',
            location=(x, y) if detail_comp_texture is None else (x, y + 150),
            is_data=True,
            color_socket=color_socket,
        )

    if detail_comp_texture is not None:
        texture(
            mat,
            texture=detail_comp_texture,
            label='DETAIL METALLIC ROUGHNESS',
            location=(x, y) if comp_texture is None else (x, y - 150),
            is_data=True,
            color_socket=detail_color_socket if comp_texture is not None else color_socket,
        )

# [Texture] => [Separate R] => [Mix Strength] =>
def occlusion(
    mat,
    location,
    occlusion_socket
):
    x, y = location

    comp_texture = mat.msfs_comp_texture
    detail_comp_texture = mat.msfs_detail_comp_texture
    if comp_texture is None:
        return

    # We don't need to add strength as the Max exporter always has it at 1.0

    # Separate RGB
    node = mat.node_tree.nodes.new('ShaderNodeSeparateRGB')
    node.location = x - 150, y - 75
    # Outputs
    mat.node_tree.links.new(occlusion_socket, node.outputs['R'])
    # Inputs
    color_socket = node.inputs[0]

    x -= 200

    # Mix detail map
    detail_color_socket = None
    if comp_texture is not None and detail_comp_texture is not None:
        node = mat.node_tree.nodes.new('ShaderNodeMixRGB')
        node.label = 'Detail Occlusion Mix'
        node.location = x - 140, y
        node.blend_type = 'MULTIPLY'
        # Outputs
        mat.node_tree.links.new(color_socket, node.outputs[0])
        # Inputs
        node.inputs['Fac'].default_value = 1.0
        color_socket = node.inputs['Color1']
        detail_color_socket = node.inputs['Color2']
        node.inputs['Color2'].default_value = [1, 1, 1, 1]

        x -= 200

    if comp_texture is not None:
        texture(
            mat,
            texture=comp_texture,
            label='OCCLUSION',
            location=(x, y) if detail_comp_texture is None else (x, y + 150),
            is_data=True,
            color_socket=color_socket,
        )

    if detail_comp_texture is not None:
        texture(
            mat,
            texture=detail_comp_texture,
            label='DETAIL OCCLUSION',
            location=(x, y) if comp_texture is None else (x, y - 150),
            is_data=True,
            color_socket=detail_color_socket if comp_texture is not None else color_socket,
        )

# [Texture] => [Normal Map] =>
def normal(
    mat,
    location,
    normal_socket
):
    x,y = location
    normal_texture = mat.msfs_normal_texture
    detail_normal_texture = mat.msfs_detail_normal_texture

    if normal_texture is None and detail_normal_texture is None:
        return

    # Normal map
    node = mat.node_tree.nodes.new('ShaderNodeNormalMap')
    node.location = x - 150, y - 40
    # Set UVMap
    node.uv_map = 'UVMap'
    # Outputs
    mat.node_tree.links.new(normal_socket, node.outputs['Normal'])
    # Inputs
    color_socket = node.inputs['Color']

    x -= 200

    # Mix detail map
    detail_color_socket = None
    if normal_texture is not None and detail_normal_texture is not None:
        node = mat.node_tree.nodes.new('ShaderNodeMixRGB')
        node.label = 'Detail Normal Mix'
        node.location = x - 140, y
        node.blend_type = 'MULTIPLY'
        # Outputs
        mat.node_tree.links.new(color_socket, node.outputs[0])
        # Inputs
        node.inputs['Fac'].default_value = 1.0
        color_socket = node.inputs['Color1']
        detail_color_socket = node.inputs['Color2']
        node.inputs['Color2'].default_value = [1, 1, 1, 1]

        x -= 200

    if normal_texture is not None:
        texture(
            mat,
            texture=normal_texture,
            label='NORMALMAP',
            location=(x, y) if detail_normal_texture is None else (x, y + 150),
            is_data=True,
            color_socket=color_socket,
        )

    if detail_normal_texture is not None:
        texture(
            mat,
            texture=detail_normal_texture,
            label='DETAIL NORMALMAP',
            location=(x, y) if normal_texture is None else (x, y - 150),
            is_data=True,
            color_socket=detail_color_socket if normal_texture is not None else color_socket,
        )

# [Texture] => [Emissive Factor] =>
def emission(
    mat,
    location,
    color_socket,
):
    x, y = location
    emissive_texture = mat.msfs_emissive_texture
    emissive_factor = list(mat.msfs_emissive_factor)

    if color_socket is None:
        return

    if emissive_texture is None:
        color_socket.default_value = emissive_factor + [1]
        return

    if emissive_factor != [1, 1, 1]:
        node = mat.node_tree.nodes.new('ShaderNodeMixRGB')
        node.label = 'Emissive Factor'
        node.location = x - 140, y
        node.blend_type = 'MULTIPLY'
        # Outputs
        mat.node_tree.links.new(color_socket, node.outputs[0])
        # Inputs
        node.inputs['Fac'].default_value = 1.0
        color_socket = node.inputs['Color1']
        node.inputs['Color2'].default_value = emissive_factor + [1]

        x -= 200

    texture(
        mat,
        texture=emissive_texture,
        label='EMISSIVE',
        location=(x, y),
        color_socket=color_socket,
    )

# [Texture] => [Detail Texture Factor] =>
def blend_mask(mat, location):
    x, y = location
    blend_mask_texture = mat.msfs_blend_mask_texture

    if blend_mask_texture is None:
        return

    base_color_socket, comp_socket, occlusion_socket, normal_socket = utilities.get_detail_factor_sockets(mat)

    if base_color_socket is None and comp_socket is None and occlusion_socket is None and normal_socket is None:
        return

    blend_mask = texture(
        mat,
        texture=blend_mask_texture,
        label='BLEND MASK',
        location=(x, y),
    )

    if blend_mask_texture.channels > 3: # if there is more than 3 channels, we know that an alpha channel is present
        # if the entire alpha layer is all white we treat it as no alpha channel, and use the color channels as the blend mask
        width = blend_mask_texture.size[0]
        height = blend_mask_texture.size[1]
        pixels = np.empty(width * height * 4, dtype=np.float32)
        blend_mask_texture.pixels.foreach_get(pixels)
        pixels = pixels.reshape((-1, 4))
        alpha_pixels = pixels[:, -1]
        if not all(alpha_pixels == 1.0): # 1.0 is a white pixel
            if base_color_socket is not None:
                mat.node_tree.links.new(base_color_socket, blend_mask.outputs['Alpha'])
            if comp_socket is not None:
                mat.node_tree.links.new(comp_socket, blend_mask.outputs['Alpha'])
            if occlusion_socket is not None:
                mat.node_tree.links.new(occlusion_socket, blend_mask.outputs['Alpha'])
            if normal_socket is not None:
                mat.node_tree.links.new(normal_socket, blend_mask.outputs['Alpha'])
            return

    # use color output for blend mask
    if base_color_socket is not None:
        mat.node_tree.links.new(base_color_socket, blend_mask.outputs['Color'])
    if comp_socket is not None:
        mat.node_tree.links.new(comp_socket, blend_mask.outputs['Color'])
    if occlusion_socket is not None:
        mat.node_tree.links.new(occlusion_socket, blend_mask.outputs['Color'])
    if normal_socket is not None:
        mat.node_tree.links.new(normal_socket, blend_mask.outputs['Color'])

# [Texture] => [Wetness AO] =>
def wetness_ao(
    mat,
    location,
    wetness_ao_socket,
):
    x, y = location
    wetness_ao_texture = mat.msfs_wetness_ao_texture

    if wetness_ao_texture is not None:
        texture(
            mat,
            texture=wetness_ao_texture,
            label='WETNESS AO',
            location=(x, y),
            color_socket=wetness_ao_socket,
        )

def dirt(
    mat,
    location,
    clearcoat_socket,
    roughness_socket,
):
    x, y = location
    dirt_texture = mat.msfs_dirt_texture

    if roughness_socket is None: # some versions of Blender don't seem to have a clearcoat roughness socket
        return

    if dirt_texture is None:
        return

    # Separate RGB (amount is in R, roughness is in G)
    node = mat.node_tree.nodes.new('ShaderNodeSeparateRGB')
    node.location = x - 150, y - 75
    # Outputs
    mat.node_tree.links.new(clearcoat_socket, node.outputs['R'])
    mat.node_tree.links.new(roughness_socket, node.outputs['G'])
    # Inputs
    color_socket = node.inputs[0]

    x -= 200

    texture(
        mat,
        texture=dirt_texture,
        label='DIRT',
        location=(x, y),
        is_data=True,
        color_socket=color_socket,
    )

### Texture Update Functions
def update_base_color_texture(self, context):
    if not self.is_import:
        bsdf_node = utilities.get_bsdf_node(self) # Try finding the BSDF node

        if bsdf_node is not None: # maybe recreate the material in this case?
            # Clear Base Color
            utilities.clear_socket(self, bsdf_node.inputs['Base Color'])
            utilities.clear_socket(self, bsdf_node.inputs['Alpha'])
        
            locs = utilities.calc_locations(self)
            
            base_color(
                self,
                location=locs['base_color'],
                color_socket=bsdf_node.inputs['Base Color'],
                alpha_socket=bsdf_node.inputs['Alpha'] if not utilities.is_opaque(self) else None,
            )

            # update the blend mask
            update_blend_mask_texture(self, context)

def update_comp_texture(self, context):
    if not self.is_import:
        nodes = self.node_tree.nodes
        bsdf_node = utilities.get_bsdf_node(self) # Try finding the BSDF node

        if bsdf_node is not None:
            # The comp texture has 3 parts - Occlusion (R), Roughness (G), Metalness (B). We do Roughness and Metalness first.
            # Clear Roughness and Metalness
            utilities.clear_socket(self, bsdf_node.inputs['Roughness'])
            utilities.clear_socket(self, bsdf_node.inputs['Metallic'])

            locs = utilities.calc_locations(self)

            metallic_roughness(
                self,
                location=locs['metallic_roughness'],
                metallic_socket=bsdf_node.inputs['Metallic'],
                roughness_socket=bsdf_node.inputs['Roughness']
            )

            # Do Occlusion 
            occlusion_socket = utilities.get_socket_old(self, 'Occlusion')
            if occlusion_socket is not None:
                utilities.clear_socket(self, occlusion_socket)
                # check if it's safe to remove the gltf settings node
                if not utilities.is_node_linked(occlusion_socket.node):
                    nodes.remove(occlusion_socket.node)
                    occlusion_socket = None

            if self.msfs_comp_texture is not None or self.msfs_detail_comp_texture is not None:
                if occlusion_socket is None: # Create a settings node if one doesn't already exist
                    settings_node = utilities.make_settings_node(self)
                    settings_node.location = 40, -370
                    settings_node.width = 180
                    occlusion_socket = settings_node.inputs['Occlusion']
                occlusion(
                    self,
                    location=locs['occlusion'],
                    occlusion_socket=occlusion_socket,
                )

            # update the blend mask
            update_blend_mask_texture(self, context)

def update_normal_texture(self, context):
    if not self.is_import:
        bsdf_node = utilities.get_bsdf_node(self) # Try finding the BSDF node

        if bsdf_node is not None: # maybe recreate the material in this case?
            # Clear Normal
            utilities.clear_socket(self, bsdf_node.inputs['Normal'])
        
            locs = utilities.calc_locations(self)
            
            normal(
                self,
                location=locs['normal'],
                normal_socket=bsdf_node.inputs['Normal'],
            )

            # update the blend mask
            update_blend_mask_texture(self, context)

def update_emissive_texture(self, context):
    if not self.is_import:
        bsdf_node = utilities.get_bsdf_node(self) # Try finding the BSDF node

        if bsdf_node is not None: # maybe recreate the material in this case?
            # Clear Emission
            utilities.clear_socket(self, bsdf_node.inputs['Emission'])
        
            locs = utilities.calc_locations(self)
            
            emission(
                self,
                location=locs['emission'],
                color_socket=bsdf_node.inputs['Emission'],
            )

def update_blend_mask_texture(self, context):
    if not self.is_import:
        nodes = self.node_tree.nodes

        detail_base_color_factor_socket, detail_comp_factor_socket, detail_occlusion_factor_socket, detail_normal_factor_socket = utilities.get_detail_factor_sockets(self)

        # Remove blend masks

        # Base color blend mask
        if detail_base_color_factor_socket is not None:
            base_color_blend_mask = utilities.previous_node(detail_base_color_factor_socket)
            if base_color_blend_mask is not None:
                nodes.remove(base_color_blend_mask)

        # Comp blend mask
        if detail_comp_factor_socket is not None:
            comp_blend_mask = utilities.previous_node(detail_comp_factor_socket)
            if comp_blend_mask is not None:
                nodes.remove(comp_blend_mask)

        # Occlusion blend mask
        if detail_occlusion_factor_socket is not None:
            occlusion_blend_mask = utilities.previous_node(detail_occlusion_factor_socket)
            if occlusion_blend_mask is not None:
                nodes.remove(occlusion_blend_mask)

        # Normal blend mask
        if detail_normal_factor_socket is not None:
            normal_blend_mask = utilities.previous_node(detail_normal_factor_socket)
            if normal_blend_mask is not None:
                nodes.remove(normal_blend_mask)

        locs = utilities.calc_locations(self)

        blend_mask(
            self,
            location=locs['blend_mask'],
        )

def update_wetness_ao_texture(self, context):
    if not self.is_import:
        nodes = self.node_tree.nodes
        bsdf_node = utilities.get_bsdf_node(self) # Try finding the BSDF node

        if bsdf_node is not None:
            # We put the wetness ao in the settings node as Blender can't render this
            wetness_ao_socket = utilities.get_socket_old(self, 'Wetness AO')
            if wetness_ao_socket is not None:
                utilities.clear_socket(self, wetness_ao_socket)
                # check if it's safe to remove the gltf settings node
                if not utilities.is_node_linked(wetness_ao_socket.node):
                    nodes.remove(wetness_ao_socket.node)
                    wetness_ao_socket = None

            if self.msfs_wetness_ao_texture is not None:
                if wetness_ao_socket is None: # Create a settings node if one doesn't already exist
                    settings_node = utilities.make_settings_node(self)
                    settings_node.location = 40, -370
                    settings_node.width = 180
                    wetness_ao_socket = settings_node.inputs['Wetness AO']

                locs = utilities.calc_locations(self)

                wetness_ao(
                    self,
                    location=locs['wetness_ao'],
                    wetness_ao_socket=wetness_ao_socket,
                )

def update_dirt_texture(self, context):
    if not self.is_import:
        bsdf_node = utilities.get_bsdf_node(self) # Try finding the BSDF node

        if bsdf_node is not None: # maybe recreate the material in this case?
            # Clear Clearcoat and Clearcoat Roughness
            utilities.clear_socket(self, bsdf_node.inputs['Clearcoat'])
            utilities.clear_socket(self, bsdf_node.inputs['Clearcoat Roughness'])

            locs = utilities.calc_locations(self)

            dirt(
                self,
                location=locs['clearcoat'],
                clearcoat_socket=bsdf_node.inputs['Clearcoat'],
                roughness_socket=bsdf_node.inputs['Clearcoat Roughness'],
            )

### Other Update Functions
def update_base_color_factor(self, context):
    if not self.is_import:
        # Locate base color factor socket and change it
        base_color_socket = utilities.get_socket(self, 'Base Color')
        if base_color_socket is None:
            base_color_socket = utilities.get_socket(self, 'BaseColor')
        if base_color_socket is None:
            base_color_socket = utilities.get_socket_old(self, 'BaseColorFactor')
        if isinstance(base_color_socket, bpy.types.NodeSocket): # Make sure this is a node socket
            base_color_factor = list(self.msfs_base_color_factor)
            if base_color_socket.is_linked: # We have a node going into the socket
                base_color_socket = utilities.get_rgb_socket(base_color_socket)

                if base_color_socket is None: # If the socket is none, we trigger an update to the base color texture as that handles color factor creation, and it's easier to do that than redoing that here.
                    update_base_color_texture(self, context)
                else:
                    base_color_socket.default_value = base_color_factor
            else: # We just update the socket itself
                base_color_socket.default_value = base_color_factor

def update_emissive_factor(self, context):
    if not self.is_import:
        # Locate emissive factor socket and change it
        emissive_socket = utilities.get_socket(self, 'Emissive')
        if emissive_socket is None:
            emissive_socket = utilities.get_socket_old(self, 'EmissiveFactor')
        if isinstance(emissive_socket, bpy.types.NodeSocket): # Make sure this is a node socket
            emissive_factor = list(self.msfs_emissive_factor) + [1] # msfs_emissive_factor is an array of 3 items, but the socket takes an array of 4 items, so we add one
            if emissive_socket.is_linked: # We have a node going into the socket
                emissive_socket = utilities.get_rgb_socket(emissive_socket)

                if emissive_socket is None: # If the socket is none, we trigger an update to the emissive texture as that handles emissive factor creation, and it's easier to do that than redoing that here.
                    update_base_color_texture(self, context)
                else:
                    emissive_socket.default_value = emissive_factor
            else: # We just update the socket itself
                emissive_socket.default_value = emissive_factor
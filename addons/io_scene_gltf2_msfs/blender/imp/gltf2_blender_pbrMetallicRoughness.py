# Copyright 2018-2021 The glTF-Blender-IO authors.
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
from ...io.com.gltf2_io import TextureInfo, MaterialPBRMetallicRoughness
from ..com.gltf2_blender_material_helpers import get_gltf_node_name
from .gltf2_blender_texture import texture
from .gltf2_blender_KHR_materials_clearcoat import \
    clearcoat, clearcoat_roughness, clearcoat_normal
from ..com import gltf2_blender_flight_sim_material_utilities as utilities

class MaterialHelper:
    """Helper class. Stores material stuff to be passed around everywhere."""
    def __init__(self, gltf, pymat, mat, vertex_color):
        self.gltf = gltf
        self.pymat = pymat
        self.mat = mat
        self.node_tree = mat.node_tree
        self.vertex_color = vertex_color
        if pymat.pbr_metallic_roughness is None:
            pymat.pbr_metallic_roughness = \
                MaterialPBRMetallicRoughness.from_dict({})

    def is_opaque(self):
        alpha_mode = self.pymat.alpha_mode
        return alpha_mode is None or alpha_mode == 'OPAQUE'

    def needs_emissive(self):
        return (
            self.pymat.emissive_texture is not None or
            (self.pymat.emissive_factor or [0, 0, 0]) != [0, 0, 0]
        )


def pbr_metallic_roughness(mh: MaterialHelper):
    """Creates node tree for pbrMetallicRoughness materials."""
    pbr_node = mh.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
    pbr_node.location = 10, 300

    make_output_nodes(
        mh,
        location=(250, 260),
        shader_socket=pbr_node.outputs[0],
        make_emission_socket=False,
        make_alpha_socket=False,
    )

    locs = calc_locations(mh)


    # Create settings node if Occlusion or Wetness AO texture is present
    settings_node = None

    create_settings_node = False
    if mh.pymat.extensions is not None: # Wetness AO
        if 'ASOBO_material_windshield' in mh.pymat.extensions:
            if 'wiperMaskTexture' in mh.pymat.extensions['ASOBO_material_windshield']:
                create_settings_node = True
        if 'ASOBO_material_anisotropic' in mh.pymat.extensions:
            if 'anisotropicTexture' in mh.pymat.extensions['ASOBO_material_anisotropic']:
                create_settings_node = True
    
    if mh.pymat.occlusion_texture is not None or create_settings_node:
        settings_node = make_settings_node(mh)
        settings_node.location = 40, -370
        settings_node.width = 180

    emission(
        mh,
        location=locs['emission'],
        color_socket=pbr_node.inputs['Emission'],
        strength_socket=pbr_node.inputs['Emission Strength'],
    )

    base_color(
        mh,
        location=locs['base_color'],
        color_socket=pbr_node.inputs['Base Color'],
        alpha_socket=pbr_node.inputs['Alpha'] if not mh.is_opaque() else None,
    )

    metallic_roughness(
        mh,
        location=locs['metallic_roughness'],
        metallic_socket=pbr_node.inputs['Metallic'],
        roughness_socket=pbr_node.inputs['Roughness'],
    )

    normal(
        mh,
        location=locs['normal'],
        normal_socket=pbr_node.inputs['Normal'],
    )

    if settings_node is not None:
        occlusion(
            mh,
            location=locs['occlusion'],
            occlusion_socket=settings_node.inputs['Occlusion'],
        )

    clearcoat(
        mh,
        location=locs['clearcoat'],
        clearcoat_socket=pbr_node.inputs['Clearcoat'],
    )

    clearcoat_roughness(
        mh,
        location=locs['clearcoat_roughness'],
        roughness_socket=pbr_node.inputs['Clearcoat Roughness'],
    )

    clearcoat_normal(
        mh,
        location=locs['clearcoat_normal'],
        normal_socket=pbr_node.inputs['Clearcoat Normal'],
    )

    if settings_node is not None:
        wetness_ao(
            mh,
            location=locs['wetness_ao'],
            wetness_ao_socket=settings_node.inputs['Wetness AO']
        )
    
    # This is sort of repetitive, but we overwrite all other clearcoat textures if there is a MSFS clearcoat material
    dirt(
        mh,
        location=locs['clearcoat'],
        clearcoat_socket=pbr_node.inputs['Clearcoat'],
        roughness_socket=pbr_node.inputs['Clearcoat Roughness'],
    )

    # do blend mask last
    blend_mask(
        mh,
        location=locs['blend_mask'],
    )


def calc_locations(mh):
    """Calculate locations to place each bit of the node graph at."""
    # Lay the blocks out top-to-bottom, aligned on the right
    x = -200
    y = 0
    height = 460  # height of each block
    locs = {}

    try:
        clearcoat_ext = mh.pymat.extensions['KHR_materials_clearcoat']
    except Exception:
        clearcoat_ext = {}

    locs['base_color'] = (x, y)
    if mh.pymat.pbr_metallic_roughness.base_color_texture is not None or mh.vertex_color:
        y -= height
    if mh.pymat.extensions is not None: # Detail Color Texture
        if 'ASOBO_material_detail_map' in mh.pymat.extensions:
            if 'detailColorTexture' in mh.pymat.extensions['ASOBO_material_detail_map']:
                y -= 150
    locs['metallic_roughness'] = (x, y)
    if mh.pymat.pbr_metallic_roughness.metallic_roughness_texture is not None:
        y -= height
    if mh.pymat.extensions is not None: # Detail Metallic Roughness/Comp Texture
        if 'ASOBO_material_detail_map' in mh.pymat.extensions:
            if 'detailMetalRoughAOTexture' in mh.pymat.extensions['ASOBO_material_detail_map']:
                y -= 150
    locs['clearcoat'] = (x, y)
    if 'clearcoatTexture' in clearcoat_ext:
        y -= height
    locs['clearcoat_roughness'] = (x, y)
    if 'clearcoatRoughnessTexture' in clearcoat_ext:
        y -= height
    locs['blend_mask'] = (x - 650, y) # move the blend mask a bit back to make space
    if mh.pymat.extensions is not None: # Blend Mask Texture
        if 'ASOBO_material_detail_map' in mh.pymat.extensions:
            if 'blendMaskTexture' in mh.pymat.extensions['ASOBO_material_detail_map']:
                y -= height
    locs['emission'] = (x, y)
    if mh.pymat.emissive_texture is not None:
        y -= height
    locs['normal'] = (x, y)
    if mh.pymat.normal_texture is not None:
        y -= height
    if mh.pymat.extensions is not None: # Detail Normal Texture
        if 'ASOBO_material_detail_map' in mh.pymat.extensions:
            if 'detailNormalTexture' in mh.pymat.extensions['ASOBO_material_detail_map']:
                y -= 150
    locs['clearcoat_normal'] = (x, y)
    if 'clearcoatNormalTexture' in clearcoat_ext:
        y -= height
    locs['occlusion'] = (x, y)
    if mh.pymat.occlusion_texture is not None:
        y -= height
    if mh.pymat.extensions is not None: # Detail Occlusion/Comp Texture
        if 'ASOBO_material_detail_map' in mh.pymat.extensions:
            if 'detailMetalRoughAOTexture' in mh.pymat.extensions['ASOBO_material_detail_map']:
                y -= 150

    locs['wetness_ao'] = (x, y)
    if mh.pymat.extensions is not None: # Wetness AO
        if 'ASOBO_material_windshield' in mh.pymat.extensions:
            if 'wiperMaskTexture' in mh.pymat.extensions['ASOBO_material_windshield']:
                y -= height
        if 'ASOBO_material_anisotropic' in mh.pymat.extensions:
            if 'anisotropicTexture' in mh.pymat.extensions['ASOBO_material_anisotropic']:
                y -= height

    # Center things
    total_height = -y
    y_offset = total_height / 2 - 20
    for key in locs:
        x, y = locs[key]
        locs[key] = (x, y + y_offset)

    return locs


# These functions each create one piece of the node graph, slotting
# their outputs into the given socket, or setting its default value.
# location is roughly the upper-right corner of where to put nodes.


# [Texture] => [Emissive Factor] =>
def emission(mh: MaterialHelper, location, color_socket, strength_socket=None):
    x, y = location
    emissive_factor = mh.pymat.emissive_factor or [0, 0, 0]

    if color_socket is None:
        return

    if mh.pymat.emissive_texture is None:
        color_socket.default_value = emissive_factor + [1]
        return

    # Put grayscale emissive factors into the Emission Strength
    e0, e1, e2 = emissive_factor
    if strength_socket and e0 == e1 == e2:
        strength_socket.default_value = e0

    # Otherwise, use a multiply node for it
    else:
        if emissive_factor != [1, 1, 1]:
            node = mh.node_tree.nodes.new('ShaderNodeMixRGB')
            node.label = 'Emissive Factor'
            node.location = x - 140, y
            node.blend_type = 'MULTIPLY'
            # Outputs
            mh.node_tree.links.new(color_socket, node.outputs[0])
            # Inputs
            node.inputs['Fac'].default_value = 1.0
            color_socket = node.inputs['Color1']
            node.inputs['Color2'].default_value = emissive_factor + [1]

            x -= 200

    texture(
        mh,
        tex_info=mh.pymat.emissive_texture,
        label='EMISSIVE',
        location=(x, y),
        color_socket=color_socket,
    )
    
    mh.mat.msfs_emissive_factor = emissive_factor



#      [Texture] => [Mix Colors] => [Color Factor] =>
# [Vertex Color] => [Mix Alphas] => [Alpha Factor] =>
def base_color(
    mh: MaterialHelper,
    location,
    color_socket,
    alpha_socket=None,
    is_diffuse=False,
):
    """Handle base color (= baseColorTexture * vertexColor * baseColorFactor)."""
    x, y = location
    pbr = mh.pymat.pbr_metallic_roughness
    if not is_diffuse:
        base_color_factor = pbr.base_color_factor
        base_color_texture = pbr.base_color_texture
    else:
        # Handle pbrSpecularGlossiness's diffuse with this function too,
        # since it's almost exactly the same as base color.
        base_color_factor = \
            mh.pymat.extensions['KHR_materials_pbrSpecularGlossiness'] \
            .get('diffuseFactor', [1, 1, 1, 1])
        base_color_texture = \
            mh.pymat.extensions['KHR_materials_pbrSpecularGlossiness'] \
            .get('diffuseTexture', None)
        if base_color_texture is not None:
            base_color_texture = TextureInfo.from_dict(base_color_texture)

    detail_color_texture = None
    if mh.pymat.extensions is not None:
        if 'ASOBO_material_detail_map' in mh.pymat.extensions:
            if 'detailColorTexture' in mh.pymat.extensions['ASOBO_material_detail_map']:
                detail_color_texture = TextureInfo.from_dict(mh.pymat.extensions['ASOBO_material_detail_map']['detailColorTexture'])

    if base_color_factor is None:
        base_color_factor = [1, 1, 1, 1]

    if base_color_texture is None and detail_color_texture is None and not mh.vertex_color:
        color_socket.default_value = base_color_factor[:3] + [1]
        if alpha_socket is not None:
            alpha_socket.default_value = base_color_factor[3]
        return

    # Mix in base color factor
    needs_color_factor = base_color_factor[:3] != [1, 1, 1]
    needs_alpha_factor = base_color_factor[3] != 1.0 and alpha_socket is not None
    if needs_color_factor or needs_alpha_factor:
        if needs_color_factor:
            node = mh.node_tree.nodes.new('ShaderNodeMixRGB')
            node.label = 'Color Factor'
            node.location = x - 140, y
            node.blend_type = 'MULTIPLY'
            # Outputs
            mh.node_tree.links.new(color_socket, node.outputs[0])
            # Inputs
            node.inputs['Fac'].default_value = 1.0
            color_socket = node.inputs['Color1']
            node.inputs['Color2'].default_value = base_color_factor[:3] + [1]

        if needs_alpha_factor:
            node = mh.node_tree.nodes.new('ShaderNodeMath')
            node.label = 'Alpha Factor'
            node.location = x - 140, y - 200
            # Outputs
            mh.node_tree.links.new(alpha_socket, node.outputs[0])
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
            node = mh.node_tree.nodes.new('ShaderNodeMixRGB')
            node.label = 'Detail Color Mix'
            node.location = (x - 140, y) if alpha_socket is None else (x - 140, y + 100)
            node.blend_type = 'MULTIPLY'
            # Outputs
            mh.node_tree.links.new(color_socket, node.outputs[0])
            # Inputs
            node.inputs['Fac'].default_value = 1.0
            color_socket = node.inputs['Color1']
            detail_color_socket = node.inputs['Color2']
            node.inputs['Color2'].default_value = [1, 1, 1, 1]

        if alpha_socket is not None:
            node = mh.node_tree.nodes.new('ShaderNodeMixRGB')
            node.label = 'Detail Alpha Mix'
            node.location = (x - 140, y) if alpha_socket is None else (x - 140, y - 100)
            node.blend_type = 'MULTIPLY'
            # Outputs
            mh.node_tree.links.new(alpha_socket, node.outputs[0])
            # Inputs
            node.inputs['Fac'].default_value = 1.0
            base_alpha_socket = node.inputs['Color1']
            detail_alpha_socket = node.inputs['Color2']
            node.inputs['Color2'].default_value = [1, 1, 1, 1]

        x -= 200

    # These are where the texture/vertex color node will put its output.
    texture_color_socket = color_socket
    texture_alpha_socket = alpha_socket
    vcolor_color_socket = color_socket
    vcolor_alpha_socket = alpha_socket

    # Mix texture and vertex color together
    if base_color_texture is not None and mh.vertex_color:
        node = mh.node_tree.nodes.new('ShaderNodeMixRGB')
        node.label = 'Mix Vertex Color'
        node.location = x - 140, y
        node.blend_type = 'MULTIPLY'
        # Outputs
        mh.node_tree.links.new(color_socket, node.outputs[0])
        # Inputs
        node.inputs['Fac'].default_value = 1.0
        texture_color_socket = node.inputs['Color1']
        vcolor_color_socket = node.inputs['Color2']

        if alpha_socket is not None:
            node = mh.node_tree.nodes.new('ShaderNodeMath')
            node.label = 'Mix Vertex Alpha'
            node.location = x - 140, y - 200
            node.operation = 'MULTIPLY'
            # Outputs
            mh.node_tree.links.new(alpha_socket, node.outputs[0])
            # Inputs
            texture_alpha_socket = node.inputs[0]
            vcolor_alpha_socket = node.inputs[1]

        x -= 200

    # Vertex Color
    if mh.vertex_color:
        node = mh.node_tree.nodes.new('ShaderNodeVertexColor')
        node.layer_name = 'Col'
        node.location = x - 250, y - 240
        # Outputs
        mh.node_tree.links.new(vcolor_color_socket, node.outputs['Color'])
        if vcolor_alpha_socket is not None:
            mh.node_tree.links.new(vcolor_alpha_socket, node.outputs['Alpha'])

        x -= 280

    if base_alpha_socket is None:
        base_alpha_socket = alpha_socket

    # Texture
    if base_color_texture is not None:
        texture(
            mh,
            tex_info=base_color_texture,
            label='BASE COLOR' if not is_diffuse else 'DIFFUSE',
            location=(x, y) if detail_color_texture is None else (x, y + 150),
            color_socket=texture_color_socket,
            alpha_socket=base_alpha_socket,
        )

    if detail_color_texture is not None:
        texture(
            mh,
            tex_info=detail_color_texture,
            label='DETAIL COLOR' if not is_diffuse else 'DETAIL DIFFUSE',
            location=(x, y) if base_color_texture is None else (x, y - 150),
            color_socket=detail_color_socket if base_color_texture is not None else texture_color_socket,
            alpha_socket=detail_alpha_socket if base_color_texture is not None else base_alpha_socket,
        )

    mh.mat.msfs_base_color_factor = base_color_factor

# [Texture] => [Separate GB] => [Metal/Rough Factor] =>
def metallic_roughness(mh: MaterialHelper, location, metallic_socket, roughness_socket):
    x, y = location
    pbr = mh.pymat.pbr_metallic_roughness

    comp_texture = pbr.metallic_roughness_texture
    detail_comp_texture = None
    if mh.pymat.extensions is not None:
        if 'ASOBO_material_detail_map' in mh.pymat.extensions:
            if 'detailMetalRoughAOTexture' in mh.pymat.extensions['ASOBO_material_detail_map']:
                detail_comp_texture = TextureInfo.from_dict(mh.pymat.extensions['ASOBO_material_detail_map']['detailMetalRoughAOTexture'])
    
    metal_factor = pbr.metallic_factor
    rough_factor = pbr.roughness_factor
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
            node = mh.node_tree.nodes.new('ShaderNodeMath')
            node.label = 'Metallic Factor'
            node.location = x - 140, y
            node.operation = 'MULTIPLY'
            # Outputs
            mh.node_tree.links.new(metallic_socket, node.outputs[0])
            # Inputs
            metallic_socket = node.inputs[0]
            node.inputs[1].default_value = metal_factor

        # Mix rough factor
        if rough_factor != 1.0:
            node = mh.node_tree.nodes.new('ShaderNodeMath')
            node.label = 'Roughness Factor'
            node.location = x - 140, y - 200
            node.operation = 'MULTIPLY'
            # Outputs
            mh.node_tree.links.new(roughness_socket, node.outputs[0])
            # Inputs
            roughness_socket = node.inputs[0]
            node.inputs[1].default_value = rough_factor

        x -= 200

    # Separate RGB
    node = mh.node_tree.nodes.new('ShaderNodeSeparateRGB')
    node.location = x - 150, y - 75
    # Outputs
    mh.node_tree.links.new(metallic_socket, node.outputs['B'])
    mh.node_tree.links.new(roughness_socket, node.outputs['G'])
    # Inputs
    color_socket = node.inputs[0]

    x -= 200

    # Mix detail map
    detail_color_socket = None
    if comp_texture is not None and detail_comp_texture is not None:
        node = mh.node_tree.nodes.new('ShaderNodeMixRGB')
        node.label = 'Detail Comp Mix'
        node.location = x - 140, y
        node.blend_type = 'MULTIPLY'
        # Outputs
        mh.node_tree.links.new(color_socket, node.outputs[0])
        # Inputs
        node.inputs['Fac'].default_value = 1.0
        color_socket = node.inputs['Color1']
        detail_color_socket = node.inputs['Color2']
        node.inputs['Color2'].default_value = [1, 1, 1, 1]

        x -= 200

    if comp_texture is not None:
        texture(
            mh,
            tex_info=comp_texture,
            label='METALLIC ROUGHNESS',
            location=(x, y) if detail_comp_texture is None else (x, y + 150),
            is_data=True,
            color_socket=color_socket,
        )

    if detail_comp_texture is not None:
        texture(
            mh,
            tex_info=detail_comp_texture,
            label='DETAIL METALLIC ROUGHNESS',
            location=(x, y) if comp_texture is None else (x, y - 150),
            is_data=True,
            color_socket=detail_color_socket if comp_texture is not None else color_socket,
        )

    mh.mat.msfs_roughness_factor = rough_factor
    mh.mat.msfs_metallic_factor = metal_factor


# [Texture] => [Normal Map] =>
def normal(mh: MaterialHelper, location, normal_socket):
    x,y = location
    normal_texture = mh.pymat.normal_texture
    detail_normal_texture = None
    if mh.pymat.extensions is not None:
        if 'ASOBO_material_detail_map' in mh.pymat.extensions:
            if 'detailNormalTexture' in mh.pymat.extensions['ASOBO_material_detail_map']:
                detail_normal_texture = TextureInfo.from_dict(mh.pymat.extensions['ASOBO_material_detail_map']['detailNormalTexture'])

    if normal_texture is None and detail_normal_texture is None:
        return

    # Normal map
    node = mh.node_tree.nodes.new('ShaderNodeNormalMap')
    node.location = x - 150, y - 40
    # Set UVMap
    uv_idx = normal_texture.tex_coord or 0
    try:
        uv_idx = normal_texture.extensions['KHR_texture_transform']['texCoord']
    except Exception:
        pass
    node.uv_map = 'UVMap' if uv_idx == 0 else 'UVMap.%03d' % uv_idx
    # Set strength
    scale = normal_texture.scale
    scale = scale if scale is not None else 1
    node.inputs['Strength'].default_value = scale
    # Outputs
    mh.node_tree.links.new(normal_socket, node.outputs['Normal'])
    # Inputs
    color_socket = node.inputs['Color']

    x -= 200

    # Mix detail map
    detail_color_socket = None
    if normal_texture is not None and detail_normal_texture is not None:
        node = mh.node_tree.nodes.new('ShaderNodeMixRGB')
        node.label = 'Detail Normal Mix'
        node.location = x - 140, y
        node.blend_type = 'MULTIPLY'
        # Outputs
        mh.node_tree.links.new(color_socket, node.outputs[0])
        # Inputs
        node.inputs['Fac'].default_value = 1.0
        color_socket = node.inputs['Color1']
        detail_color_socket = node.inputs['Color2']
        node.inputs['Color2'].default_value = [1, 1, 1, 1]

        x -= 200

    if normal_texture is not None:
        texture(
            mh,
            tex_info=normal_texture,
            label='NORMALMAP',
            location=(x, y) if detail_normal_texture is None else (x, y + 150),
            is_data=True,
            color_socket=color_socket,
        )

    if detail_normal_texture is not None:
        texture(
            mh,
            tex_info=normal_texture,
            label='DETAIL NORMALMAP',
            location=(x, y) if normal_texture is None else (x, y - 150),
            is_data=True,
            color_socket=detail_color_socket if normal_texture is not None else color_socket,
        )


# [Texture] => [Separate R] => [Mix Strength] =>
def occlusion(mh: MaterialHelper, location, occlusion_socket):
    x, y = location

    comp_texture = mh.pymat.occlusion_texture
    detail_comp_texture = None
    if mh.pymat.extensions is not None:
        if 'ASOBO_material_detail_map' in mh.pymat.extensions:
            if 'detailMetalRoughAOTexture' in mh.pymat.extensions['ASOBO_material_detail_map']:
                detail_comp_texture = TextureInfo.from_dict(mh.pymat.extensions['ASOBO_material_detail_map']['detailMetalRoughAOTexture'])

    if comp_texture is None and detail_comp_texture is None:
        return

    strength = comp_texture.strength
    if strength is None: strength = 1.0
    if strength != 1.0:
        # Mix with white
        node = mh.node_tree.nodes.new('ShaderNodeMixRGB')
        node.label = 'Occlusion Strength'
        node.location = x - 140, y
        node.blend_type = 'MIX'
        # Outputs
        mh.node_tree.links.new(occlusion_socket, node.outputs[0])
        # Inputs
        node.inputs['Fac'].default_value = strength
        node.inputs['Color1'].default_value = [1, 1, 1, 1]
        occlusion_socket = node.inputs['Color2']

        x -= 200

    # Separate RGB
    node = mh.node_tree.nodes.new('ShaderNodeSeparateRGB')
    node.location = x - 150, y - 75
    # Outputs
    mh.node_tree.links.new(occlusion_socket, node.outputs['R'])
    # Inputs
    color_socket = node.inputs[0]

    x -= 200

    # Mix detail map
    detail_color_socket = None
    if comp_texture is not None and detail_comp_texture is not None:
        node = mh.node_tree.nodes.new('ShaderNodeMixRGB')
        node.label = 'Detail Occlusion Mix'
        node.location = x - 140, y
        node.blend_type = 'MULTIPLY'
        # Outputs
        mh.node_tree.links.new(color_socket, node.outputs[0])
        # Inputs
        node.inputs['Fac'].default_value = 1.0
        color_socket = node.inputs['Color1']
        detail_color_socket = node.inputs['Color2']
        node.inputs['Color2'].default_value = [1, 1, 1, 1]

        x -= 200

    if comp_texture is not None:
        texture(
            mh,
            tex_info=comp_texture,
            label='OCCLUSION',
            location=(x, y) if detail_comp_texture is None else (x, y + 150),
            is_data=True,
            color_socket=color_socket,
        )

    if detail_comp_texture is not None:
        texture(
            mh,
            tex_info=detail_comp_texture,
            label='DETAIL OCCLUSION',
            location=(x, y) if comp_texture is None else (x, y - 150),
            is_data=True,
            color_socket=detail_color_socket if comp_texture is not None else color_socket,
        )

# [Texture] => [Detail Texture Factor] =>
def blend_mask(mh: MaterialHelper, location):
    x, y = location
    blend_mask_texture = None
    if mh.pymat.extensions is not None:
        if 'ASOBO_material_detail_map' in mh.pymat.extensions:
            if 'blendMaskTexture' in mh.pymat.extensions['ASOBO_material_detail_map']:
                blend_mask_texture = TextureInfo.from_dict(mh.pymat.extensions['ASOBO_material_detail_map']['blendMaskTexture'])

    if blend_mask_texture is None:
        return

    base_color_socket, comp_socket, occlusion_socket, normal_socket = utilities.get_detail_factor_sockets(mh.mat)

    blend_mask = texture(
        mh,
        tex_info=blend_mask_texture,
        label='BLEND MASK',
        location=(x, y),
    )
    blend_mask_texture = blend_mask.image

    if blend_mask_texture.channels > 3: # if there is more than 3 channels, we know that an alpha channel is present
        # if the entire alpha layer is all white we treat it as no alpha channel, and use the color channels as the blend mask
        width = blend_mask_texture.size[0]
        height = blend_mask_texture.size[1]
        pixels = numpy.empty(width * height * 4, dtype=numpy.float32)
        blend_mask_texture.pixels.foreach_get(pixels)
        pixels = pixels.reshape((-1, 4))
        alpha_pixels = pixels[:, -1]
        if not all(alpha_pixels == 1.0): # 1.0 is a white pixel
            if base_color_socket is not None:
                mh.node_tree.links.new(base_color_socket, blend_mask.outputs['Alpha'])
            if comp_socket is not None:
                mh.node_tree.links.new(comp_socket, blend_mask.outputs['Alpha'])
            if occlusion_socket is not None:
                mh.node_tree.links.new(occlusion_socket, blend_mask.outputs['Alpha'])
            if normal_socket is not None:
                mh.node_tree.links.new(normal_socket, blend_mask.outputs['Alpha'])
            return

    # use color output for blend mask
    if base_color_socket is not None:
        mh.node_tree.links.new(base_color_socket, blend_mask.outputs['Color'])
    if comp_socket is not None:
        mh.node_tree.links.new(comp_socket, blend_mask.outputs['Color'])
    if occlusion_socket is not None:
        mh.node_tree.links.new(occlusion_socket, blend_mask.outputs['Color'])
    if normal_socket is not None:
        mh.node_tree.links.new(normal_socket, blend_mask.outputs['Color'])

# [Texture] => [Wetness AO] =>
def wetness_ao(mh: MaterialHelper, location, wetness_ao_socket):
    x, y = location
    wetness_ao_texture = None
    if mh.pymat.extensions is not None: # Wetness AO
        if 'ASOBO_material_windshield' in mh.pymat.extensions:
            if 'wiperMaskTexture' in mh.pymat.extensions['ASOBO_material_windshield']:
                wetness_ao_texture = TextureInfo.from_dict(mh.pymat.extensions['ASOBO_material_windshield']['wiperMaskTexture'])
        if 'ASOBO_material_anisotropic' in mh.pymat.extensions:
            if 'anisotropicTexture' in mh.pymat.extensions['ASOBO_material_anisotropic']:
                wetness_ao_texture = TextureInfo.from_dict(mh.pymat.extensions['ASOBO_material_anisotropic']['anisotropicTexture'])

    if wetness_ao_texture is not None:
        texture(
            mh,
            tex_info=wetness_ao_texture,
            label='WETNESS AO',
            location=(x, y),
            color_socket=wetness_ao_socket,
        )

def dirt(mh: MaterialHelper, location, clearcoat_socket, roughness_socket):
    x, y = location
    dirt_texture = None
    if mh.pymat.extensions is not None:
        if 'ASOBO_material_clear_coat' in mh.pymat.extensions:
            if 'dirtTexture' in mh.pymat.extensions['ASOBO_material_clear_coat']:
                dirt_texture = TextureInfo.from_dict(mh.pymat.extensions['ASOBO_material_clear_coat']['dirtTexture'])

    if roughness_socket is None: # some versions of Blender don't seem to have a clearcoat roughness socket
        return

    if dirt_texture is None:
        return

    # Separate RGB (amount is in R, roughness is in G)
    node = mh.node_tree.nodes.new('ShaderNodeSeparateRGB')
    node.location = x - 150, y - 75
    # Outputs
    mh.node_tree.links.new(clearcoat_socket, node.outputs['R'])
    mh.node_tree.links.new(roughness_socket, node.outputs['G'])
    # Inputs
    color_socket = node.inputs[0]

    x -= 200

    texture(
        mh,
        tex_info=dirt_texture,
        label='DIRT',
        location=(x, y),
        is_data=True,
        color_socket=color_socket,
    )


# => [Add Emission] => [Mix Alpha] => [Material Output]
def make_output_nodes(
    mh: MaterialHelper,
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
        node = mh.node_tree.nodes.new('ShaderNodeEmission')
        node.location = x + 50, y + 250
        # Inputs
        emission_socket = node.inputs[0]
        # Outputs
        emission_output = node.outputs[0]

        # Add
        node = mh.node_tree.nodes.new('ShaderNodeAddShader')
        node.location = x + 250, y + 160
        # Inputs
        mh.node_tree.links.new(node.inputs[0], emission_output)
        mh.node_tree.links.new(node.inputs[1], shader_socket)
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
        node = mh.node_tree.nodes.new('ShaderNodeBsdfTransparent')
        node.location = x + 100, y - 350
        # Outputs
        transparent_out = node.outputs[0]

        # Mix
        node = mh.node_tree.nodes.new('ShaderNodeMixShader')
        node.location = x + 340, y - 180
        # Inputs
        alpha_socket = node.inputs[0]
        mh.node_tree.links.new(node.inputs[1], transparent_out)
        mh.node_tree.links.new(node.inputs[2], shader_socket)
        # Outputs
        shader_socket = node.outputs[0]


        x += 480
        y -= 210

    # Material output
    node = mh.node_tree.nodes.new('ShaderNodeOutputMaterial')
    node.location = x + 70, y + 10
    # Outputs
    mh.node_tree.links.new(node.inputs[0], shader_socket)

    return emission_socket, alpha_socket


def make_settings_node(mh):
    """
    Make a Group node with a hookup for Occlusion and Wetness AO. No effect in Blender, but
    used to tell the exporter what the occlusion map should be.
    """
    node = mh.node_tree.nodes.new('ShaderNodeGroup')
    node.node_tree = get_settings_group()
    return node


def get_settings_group():
    gltf_node_group_name = get_gltf_node_name()
    if gltf_node_group_name in bpy.data.node_groups:
        gltf_node_group = bpy.data.node_groups[gltf_node_group_name]
    else:
        # Create a new node group
        gltf_node_group = bpy.data.node_groups.new(gltf_node_group_name, 'ShaderNodeTree')
        gltf_node_group.inputs.new("NodeSocketFloat", "Occlusion")
        gltf_node_group.inputs.new('NodeSocketFloat', 'Wetness AO')
        gltf_node_group.nodes.new('NodeGroupOutput')
        gltf_node_group_input = gltf_node_group.nodes.new('NodeGroupInput')
        gltf_node_group_input.location = -200, 0
    return gltf_node_group

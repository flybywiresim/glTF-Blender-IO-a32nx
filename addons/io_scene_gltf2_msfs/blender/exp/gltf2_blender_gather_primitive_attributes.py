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

import numpy as np

from . import gltf2_blender_export_keys
from io_scene_gltf2_msfs.io.com import gltf2_io
from io_scene_gltf2_msfs.io.com import gltf2_io_constants
from io_scene_gltf2_msfs.io.com import gltf2_io_debug
from io_scene_gltf2_msfs.io.exp import gltf2_io_binary_data


def gather_primitive_attributes(blender_primitive, export_settings):
    """
    Gathers the attributes, such as POSITION, NORMAL, TANGENT from a blender primitive.

    :return: a dictionary of attributes
    """
    attributes = {}
    if export_settings['emulate_asobo_optimization']:
        # Attributes should be in a different order for optimized meshes
        attributes.update(__gather_colors(blender_primitive, export_settings))
        attributes.update(__gather_normal(blender_primitive, export_settings))
        attributes.update(__gather_position(blender_primitive, export_settings))
        attributes.update(__gather_tangent(blender_primitive, export_settings))
        attributes.update(__gather_texcoord(blender_primitive, export_settings))
        attributes.update(__gather_skins(blender_primitive, export_settings))
    else:
        attributes.update(__gather_position(blender_primitive, export_settings))
        attributes.update(__gather_normal(blender_primitive, export_settings))
        attributes.update(__gather_tangent(blender_primitive, export_settings))
        attributes.update(__gather_texcoord(blender_primitive, export_settings))
        attributes.update(__gather_colors(blender_primitive, export_settings))
        attributes.update(__gather_skins(blender_primitive, export_settings))
    return attributes


def array_to_accessor(array, component_type, data_type, include_max_and_min=False, create_buffer_view=True, emulate_asobo_optimization=False):
    if emulate_asobo_optimization: # Asobo uses different data types for some components
        dtype = gltf2_io_constants.ComponentType.to_numpy_dtype_asobo(component_type)
    else:
        dtype = gltf2_io_constants.ComponentType.to_numpy_dtype(component_type)

    num_elems = gltf2_io_constants.DataType.num_elements(data_type)

    if type(array) is not np.ndarray:
        array = np.array(array, dtype=dtype)
        array = array.reshape(len(array) // num_elems, num_elems)

    assert array.dtype == dtype
    assert array.shape[1] == num_elems

    amax = None
    amin = None
    if include_max_and_min:
        amax = np.amax(array, axis=0).tolist()
        amin = np.amin(array, axis=0).tolist()

    return gltf2_io.Accessor(
        buffer_view=gltf2_io_binary_data.BinaryData(array.tobytes()) if create_buffer_view else array, # For optimized meshes, we convert the data into bytes later
        byte_offset=None,
        component_type=component_type,
        count=len(array),
        extensions=None,
        extras=None,
        max=amax,
        min=amin,
        name=None,
        normalized=None,
        sparse=None,
        type=data_type,
    )


def __gather_position(blender_primitive, export_settings):
    position = blender_primitive["attributes"]["POSITION"]
    return {
        "POSITION": array_to_accessor(
            position,
            component_type=gltf2_io_constants.ComponentType.Float,
            data_type=gltf2_io_constants.DataType.Vec3,
            include_max_and_min=True,
            create_buffer_view=False if export_settings['emulate_asobo_optimization'] else True,
            emulate_asobo_optimization=export_settings['emulate_asobo_optimization'],
        )
    }


def __gather_normal(blender_primitive, export_settings):
    if not export_settings[gltf2_blender_export_keys.NORMALS]:
        return {}
    if 'NORMAL' not in blender_primitive["attributes"]:
        return {}
    normal = blender_primitive["attributes"]['NORMAL']
    component_type = gltf2_io_constants.ComponentType.Float
    data_type = gltf2_io_constants.DataType.Vec3
    if export_settings['emulate_asobo_optimization']:
        component_type = gltf2_io_constants.ComponentType.Byte # Asobo uses bytes instead of floats
        data_type = gltf2_io_constants.DataType.Vec4 # Asobo uses a VEC4 instead of a VEC3 for normals
        normal *= 127
        normal = normal.astype(gltf2_io_constants.ComponentType.to_numpy_dtype_asobo(component_type)) # Convert the numpy array data type to bytes
    return {
        "NORMAL": array_to_accessor(
            normal,
            component_type=component_type,
            data_type=data_type,
            create_buffer_view=False if export_settings['emulate_asobo_optimization'] else True,
            emulate_asobo_optimization=export_settings['emulate_asobo_optimization'],
        )
    }


def __gather_tangent(blender_primitive, export_settings):
    if not export_settings[gltf2_blender_export_keys.TANGENTS] and not export_settings['emulate_asobo_optimization']: # Force export tangents for optimized meshes
        return {}
    if 'TANGENT' not in blender_primitive["attributes"]:
        return {}
    tangent = blender_primitive["attributes"]['TANGENT']
    component_type = gltf2_io_constants.ComponentType.Float
    if export_settings['emulate_asobo_optimization']:
        component_type = gltf2_io_constants.ComponentType.Byte # Asobo uses bytes instead of floats
        tangent *= 127
        tangent = tangent.astype(gltf2_io_constants.ComponentType.to_numpy_dtype_asobo(component_type)) # Convert the numpy array data type to bytes
    return {
        "TANGENT": array_to_accessor(
            tangent,
            component_type=component_type,
            data_type=gltf2_io_constants.DataType.Vec4,
            create_buffer_view=False if export_settings['emulate_asobo_optimization'] else True,
            emulate_asobo_optimization=export_settings['emulate_asobo_optimization'],
        )
    }


def __gather_texcoord(blender_primitive, export_settings):
    attributes = {}
    if export_settings[gltf2_blender_export_keys.TEX_COORDS]:
        tex_coord_index = 0
        tex_coord_id = 'TEXCOORD_' + str(tex_coord_index)
        while blender_primitive["attributes"].get(tex_coord_id) is not None:
            tex_coord = blender_primitive["attributes"][tex_coord_id]
            component_type = gltf2_io_constants.ComponentType.Float
            if export_settings['emulate_asobo_optimization']:
                component_type = gltf2_io_constants.ComponentType.Short # Asobo uses shorts instead of floats
                tex_coord = tex_coord.astype(gltf2_io_constants.ComponentType.to_numpy_dtype_asobo(component_type)) # Convert the numpy array data type to shorts
            attributes[tex_coord_id] = array_to_accessor(
                tex_coord,
                component_type=component_type,
                data_type=gltf2_io_constants.DataType.Vec2,
                create_buffer_view=False if export_settings['emulate_asobo_optimization'] else True,
                emulate_asobo_optimization=export_settings['emulate_asobo_optimization'],
            )
            tex_coord_index += 1
            tex_coord_id = 'TEXCOORD_' + str(tex_coord_index)
    return attributes


def __gather_colors(blender_primitive, export_settings): # TODO: I don't think this is right for optimization, the values don't match the same as the ones that were built by the sim
    attributes = {}
    if export_settings[gltf2_blender_export_keys.COLORS]:
        color_index = 0
        color_id = 'COLOR_' + str(color_index)
        while blender_primitive["attributes"].get(color_id) is not None:
            colors = blender_primitive["attributes"][color_id]

            if type(colors) is not np.ndarray:
                colors = np.array(colors, dtype=np.float32)
                colors = colors.reshape(len(colors) // 4, 4)

            component_type = gltf2_io_constants.ComponentType.UnsignedShort
            if export_settings['emulate_asobo_optimization']:
                if blender_primitive['VertexType'] == 'VTX':
                    colors[:] = 15360
                    component_type = gltf2_io_constants.ComponentType.UnsignedShort # Unskinned meshes use unsigned shorts
                else:
                    component_type = gltf2_io_constants.ComponentType.Byte # Skinned meshes use bytes
                    colors[:] = -1
                colors = colors.astype(gltf2_io_constants.ComponentType.to_numpy_dtype_asobo(component_type)) # Convert the numpy array data type
            else:
                # Convert to normalized ushorts
                colors *= 65535
                colors += 0.5  # bias for rounding
                colors = colors.astype(np.uint16)

            attributes[color_id] = gltf2_io.Accessor(
                buffer_view=gltf2_io_binary_data.BinaryData(colors.tobytes()) if not export_settings['emulate_asobo_optimization'] else colors,
                byte_offset=None,
                component_type=component_type,
                count=len(colors),
                extensions=None,
                extras=None,
                max=None,
                min=None,
                name=None,
                normalized=True if not export_settings['emulate_asobo_optimization'] else None, # MSFS doesn't support normalized vertex colors
                sparse=None,
                type=gltf2_io_constants.DataType.Vec4,
            )

            color_index += 1
            color_id = 'COLOR_' + str(color_index)
    return attributes


def __gather_skins(blender_primitive, export_settings):
    attributes = {}
    if export_settings[gltf2_blender_export_keys.SKINS]:
        bone_set_index = 0
        joint_id = 'JOINTS_' + str(bone_set_index)
        weight_id = 'WEIGHTS_' + str(bone_set_index)
        while blender_primitive["attributes"].get(joint_id) and blender_primitive["attributes"].get(weight_id):
            if bone_set_index >= 1:
                if not export_settings['gltf_all_vertex_influences']:
                    gltf2_io_debug.print_console("WARNING", "There are more than 4 joint vertex influences."
                                                            "The 4 with highest weight will be used (and normalized).")
                    break

            # joints
            internal_joint = blender_primitive["attributes"][joint_id]
            component_type = gltf2_io_constants.ComponentType.UnsignedShort
            if max(internal_joint) < 256:
                component_type = gltf2_io_constants.ComponentType.UnsignedByte
            joint = array_to_accessor(
                internal_joint,
                component_type,
                data_type=gltf2_io_constants.DataType.Vec4,
                create_buffer_view=False if export_settings['emulate_asobo_optimization'] else True,
                emulate_asobo_optimization=export_settings['emulate_asobo_optimization'],
            )
            attributes[joint_id] = joint

            # weights
            internal_weight = blender_primitive["attributes"][weight_id]
            # normalize first 4 weights, when not exporting all influences, except if the vertex type is BLEND1 since it's already normalized

            vertex_type = None # we need to set vertex type to none and only set it to its actual value if we are optimizing the mesh
            if export_settings['emulate_asobo_optimization']:
                vertex_type = blender_primitive['VertexType']

            if not export_settings['gltf_all_vertex_influences'] and not vertex_type == 'BLEND1':
                for idx in range(0, len(internal_weight), 4):
                    weight_slice = internal_weight[idx:idx + 4]
                    total = sum(weight_slice)
                    if total > 0:
                        factor = 1.0 / total
                        internal_weight[idx:idx + 4] = [w * factor for w in weight_slice]

            weight_component_type = gltf2_io_constants.ComponentType.Float
            weight_data_type = gltf2_io_constants.DataType.Vec4
            if export_settings['emulate_asobo_optimization']:
                if blender_primitive['VertexType'] == 'BLEND1':
                    weight_data_type = gltf2_io_constants.DataType.Scalar # BLEND1 primitives use scalar instead of VEC4
                else:
                    weight_component_type = gltf2_io_constants.ComponentType.UnsignedShort # BLEND4 primitives use unsigned shorts instead of floats
                    internal_weight = [round(x * 65535) for x in internal_weight]

            weight = array_to_accessor(
                internal_weight,
                component_type=weight_component_type,
                data_type=weight_data_type,
                create_buffer_view=False if export_settings['emulate_asobo_optimization'] else True,
                emulate_asobo_optimization=export_settings['emulate_asobo_optimization'],
            )
            attributes[weight_id] = weight

            bone_set_index += 1
            joint_id = 'JOINTS_' + str(bone_set_index)
            weight_id = 'WEIGHTS_' + str(bone_set_index)
    return attributes

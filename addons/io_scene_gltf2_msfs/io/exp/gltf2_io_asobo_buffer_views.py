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

import base64
import struct
import numpy as np

from io_scene_gltf2_msfs.io.com import gltf2_io
from io_scene_gltf2_msfs.io.com import gltf2_io_constants
from io_scene_gltf2_msfs.io.exp import gltf2_io_binary_data

STRUCT_POSITION = struct.Struct('fff')
STRUCT_TANGENT = struct.Struct('bbbb')
STRUCT_NORMAL = struct.Struct('bbbb')
STRUCT_UV = struct.Struct('ee')
STRUCT_JOINT = struct.Struct('HHHH')
STRUCT_WEIGHT1 = struct.Struct('f')
STRUCT_WEIGHT4 = struct.Struct('HHHH')
STRUCT_COLOR_VTX = struct.Struct('HHHH')
STRUCT_COLOR_BLEND = struct.Struct('bbbb')

class AsoboBuffer:
    def __init__(self, buffer_index=0):
        self.__data = b''
        self.__buffer_index = buffer_index

    def append_data(self, binary_data: gltf2_io_binary_data.BinaryData, check_padding=False, calculate_offset=False) -> gltf2_io.BufferView:
        """Add binary data to the buffer. Return a glTF BufferView."""
        offset = None
        if calculate_offset:
            offset = len(self.__data)

        self.__data += binary_data.data

        # offsets should be a multiple of 4 --> therefore add padding if necessary
        if check_padding:
            padding = (4 - (binary_data.byte_length % 4)) % 4
            if padding != 0:
                self.__data += b'\x00' * padding

        return offset

    def append_bytes(self, binary_data: bytes, calculate_offset=False) -> gltf2_io.BufferView:
        """Add binary data to the buffer. Return a glTF BufferView."""
        offset = None
        if calculate_offset:
            offset = len(self.__data)

        self.__data += binary_data

        return offset

    @property
    def byte_length(self):
        return len(self.__data)

    def to_bytes(self):
        return self.__data

    def to_embed_string(self):
        return 'data:application/octet-stream;base64,' + base64.b64encode(self.__data).decode('ascii')

    def clear(self):
        self.__data = b''

class AsoboBufferViews():

    def __init__(self):
        # These are the 8 buffer views that Asobo optimized meshes use
        self.bufferViewFloatMat4 = gltf2_io.BufferView(
            buffer=AsoboBuffer(),
            byte_length=0,
            byte_offset=None,
            byte_stride=None,
            extensions=None,
            extras=None,
            name='bufferViewFloatMat4',
            target=None
        )

        self.bufferViewAnimationFloatScalar = gltf2_io.BufferView(
            buffer=AsoboBuffer(),
            byte_length=0,
            byte_offset=0,
            byte_stride=None,
            extensions=None,
            extras=None,
            name='bufferViewAnimationFloatScalar',
            target=None
        )

        self.bufferViewAnimationFloatVec3 = gltf2_io.BufferView(
            buffer=AsoboBuffer(),
            byte_length=0,
            byte_offset=0,
            byte_stride=None,
            extensions=None,
            extras=None,
            name='bufferViewAnimationFloatVec3',
            target=None
        )

        self.bufferViewAnimationFloatVec4 = gltf2_io.BufferView(
            buffer=AsoboBuffer(),
            byte_length=0,
            byte_offset=0,
            byte_stride=None,
            extensions=None,
            extras=None,
            name='bufferViewAnimationFloatVec4',
            target=None
        )

        self.BufferViewVertexND = gltf2_io.BufferView(
            buffer=AsoboBuffer(),
            byte_length=0,
            byte_offset=0,
            byte_stride=36,
            extensions=None,
            extras=None,
            name='BufferViewVertexND',
            target=34962
        )

        self.BufferViewIndex = gltf2_io.BufferView(
            buffer=AsoboBuffer(),
            byte_length=0,
            byte_offset=0,
            byte_stride=None,
            extensions=None,
            extras=None,
            name='BufferViewIndex',
            target=34963
        )

        self.BufferViewVertex4Blend = gltf2_io.BufferView(
            buffer=AsoboBuffer(),
            byte_length=0,
            byte_offset=0,
            byte_stride=48,
            extensions=None,
            extras=None,
            name='BufferViewVertex4Blend',
            target=34962
        )

        self.BufferViewVertex1Blend = gltf2_io.BufferView(
            buffer=AsoboBuffer(),
            byte_length=0,
            byte_offset=0,
            byte_stride=44,
            extensions=None,
            extras=None,
            name='BufferViewVertex1Blend',
            target=34962
        )

        self.BufferViews = []

        self.Meshes = [] # Keep track of the meshes we have already handled (we need this since meshes can be shared across objects, and we don't want to handle a mesh twice)

    def traverse_scenes(self, scenes):
        for scene in scenes:
            for node in scene.nodes:
                self.__traverse_node(node, lambda node: self.__handle_node(node))

    
    def __traverse_node(self, node, f):
        f(node)
        if not (node.children is None):
            for child in node.children:
                self.__traverse_node(child, f)

    def __handle_node(self, node):
        if node.mesh is not None:
            if node.mesh not in self.Meshes:
                self.Meshes.append(node.mesh)
                is_skinned_mesh = any('BLEND' in primitive.extras['ASOBO_primitive']['VertexType'] for primitive in node.mesh.primitives)
                self.__handle_mesh(node.mesh, is_skinned_mesh)

    @staticmethod
    def get_primitive_attributes_count(primitive):
        attributes_count = [primitive.attributes[attribute].count for attribute in primitive.attributes] # Get a list of all attribute's count
        if all(x==attributes_count[0] for x in attributes_count): # Make sure they are all the same
            return attributes_count[0]
        else:
            raise RuntimeError('Not all attributes of primitive have the same count')

    def __handle_mesh(self, mesh, is_skinned):
        # The order in which we collect the buffer views is the same as defined in the class
        if is_skinned:
            for i, primitive in enumerate(mesh.primitives):

                #
                # Gather indices
                #
                
                indices = [] # Use a regular python list as appending is faster than using numpy

                # Reverse indices (this makes the faces render in the correct direction)
                for i in range(0, len(primitive.indices.buffer_view), 3):
                    indices.append(primitive.indices.buffer_view[i + 2])
                    indices.append(primitive.indices.buffer_view[i + 1])
                    indices.append(primitive.indices.buffer_view[i + 0])

                indices_accessor = primitive.indices

                # Set data type
                dtype = gltf2_io_constants.ComponentType.to_numpy_dtype_asobo(indices_accessor.component_type)
                indices = np.array(indices, dtype=dtype)

                binary_data = gltf2_io_binary_data.BinaryData(indices.tobytes())
                offset = self.BufferViewIndex.buffer.append_data(binary_data, check_padding=True, calculate_offset=True)
                if self.BufferViewIndex not in self.BufferViews:
                    self.BufferViews.append(self.BufferViewIndex)


                indices_accessor.buffer_view = self.BufferViews.index(self.BufferViewIndex)
                if offset != 0:
                    indices_accessor.byte_offset = offset
                indices_accessor.name = f'{mesh.name}_indices#{i}'

                #
                # Set mesh data
                #
                
                is_blend4 = primitive.extras['ASOBO_primitive']['VertexType'] == 'BLEND4'
                blend_buffer_view = self.BufferViewVertex4Blend if is_blend4 else self.BufferViewVertex1Blend
                expected_byte_stride = 48 if is_blend4 else 44

                # Get amount of elements we want to add into the buffer
                count = AsoboBufferViews.get_primitive_attributes_count(primitive)

                buffer = bytearray(expected_byte_stride * count) # could possibly cause an error? might need to multiply by 3

                # Assign offsets
                offset = blend_buffer_view.buffer.byte_length
                
                if 'POSITION' in primitive.attributes:
                    if offset != 0:
                        primitive.attributes['POSITION'].byte_offset = offset
                if 'TANGENT' in primitive.attributes:
                    primitive.attributes['TANGENT'].byte_offset = offset + 12
                if 'NORMAL' in primitive.attributes:
                    primitive.attributes['NORMAL'].byte_offset = offset + 16
                if 'TEXCOORD_0' in primitive.attributes:
                    primitive.attributes['TEXCOORD_0'].byte_offset = offset + 20
                if 'TEXCOORD_1' in primitive.attributes:
                    primitive.attributes['TEXCOORD_1'].byte_offset = offset + 24
                if 'JOINTS_0' in primitive.attributes:
                    primitive.attributes['JOINTS_0'].byte_offset = offset + 28
                if 'WEIGHTS_0' in primitive.attributes:
                    primitive.attributes['WEIGHTS_0'].byte_offset = offset + 36
                if 'COLOR_0' in primitive.attributes:
                    if is_blend4:
                        primitive.attributes['COLOR_0'].byte_offset = offset + 44
                    else:
                        primitive.attributes['COLOR_0'].byte_offset = offset + 40

                for vidx in range(count):
                    start = vidx * expected_byte_stride

                    # Pack data into buffer

                    if 'POSITION' in primitive.attributes:
                        STRUCT_POSITION.pack_into(buffer, start, *primitive.attributes['POSITION'].buffer_view[vidx])
                    if 'TANGENT' in primitive.attributes:
                        STRUCT_TANGENT.pack_into(buffer, start + 12, *primitive.attributes['TANGENT'].buffer_view[vidx])
                    if 'NORMAL' in primitive.attributes:
                        STRUCT_NORMAL.pack_into(buffer, start + 16, *primitive.attributes['NORMAL'].buffer_view[vidx])
                    if 'TEXCOORD_0' in primitive.attributes:
                        STRUCT_UV.pack_into(buffer, start + 20, *primitive.attributes['TEXCOORD_0'].buffer_view[vidx])
                    if 'TEXCOORD_1' in primitive.attributes:
                        STRUCT_UV.pack_into(buffer, start + 24, *primitive.attributes['TEXCOORD_1'].buffer_view[vidx])
                    if 'JOINTS_0' in primitive.attributes:
                        STRUCT_JOINT.pack_into(buffer, start + 28, *primitive.attributes['JOINTS_0'].buffer_view[vidx])
                    if 'WEIGHTS_0' in primitive.attributes:
                        if is_blend4:
                            STRUCT_WEIGHT4.pack_into(buffer, start + 36, *primitive.attributes['WEIGHTS_0'].buffer_view[vidx])
                        else:
                            STRUCT_WEIGHT1.pack_into(buffer, start + 36, *primitive.attributes['WEIGHTS_0'].buffer_view[vidx])
                    if 'COLOR_0' in primitive.attributes:
                        if is_blend4:
                            STRUCT_COLOR_BLEND.pack_into(buffer, start + 44, *primitive.attributes['COLOR_0'].buffer_view[vidx])
                        else:
                            STRUCT_COLOR_BLEND.pack_into(buffer, start + 40, *primitive.attributes['COLOR_0'].buffer_view[vidx])

                blend_buffer_view.buffer.append_bytes(bytes(buffer), calculate_offset=False)
                if blend_buffer_view not in self.BufferViews:
                    self.BufferViews.append(blend_buffer_view)

                # Set attribute names and  buffer view indexes
                for attribute in primitive.attributes:
                    primitive.attributes[attribute].buffer_view = self.BufferViews.index(blend_buffer_view)
                    primitive.attributes[attribute].name = f'{mesh.name}_vertices#0_{attribute}'

        else: # Mesh is not skinned

            #
            # Share accessors between the primitives
            #

            for attribute in mesh.primitives[0].attributes:
                # Put all data into one accessor per attribute, and share across primitives
                accessor = mesh.primitives[0].attributes[attribute] # Share the first primitive's accessors
                buffer_views = []
                for primitive in mesh.primitives:
                    buffer_views.extend(primitive.attributes[attribute].buffer_view) # Add other primitive's data into the accessor
                accessor.buffer_view = buffer_views
                accessor.count = len(buffer_views) # Recalculate the count

                if attribute == 'POSITION': # Since we've put all the data into a shared accessor, we need to also recalculate the position accessor's min and max values
                    accessor.min = list(map(float, np.amin(buffer_views, axis=0).tolist()))
                    accessor.max = list(map(float, np.amax(buffer_views, axis=0).tolist()))

                for primitive in mesh.primitives: # Set all primitives to use the shared accessor
                    primitive.attributes[attribute] = accessor
            
            #
            # Set mesh data
            #

            vertex_nd_buffer_view = self.BufferViewVertexND
            expected_byte_stride = 36

            # Get amount of elements we want to add into the buffer
            count = AsoboBufferViews.get_primitive_attributes_count(primitive)

            # Create an empty buffer with the expected size
            buffer = bytearray(expected_byte_stride * count) # could possibly cause an error? might need to multiply by 3

            # Assign offsets
            offset = vertex_nd_buffer_view.buffer.byte_length

            if 'POSITION' in primitive.attributes:
                if offset != 0:
                    primitive.attributes['POSITION'].byte_offset = offset
            if 'TANGENT' in primitive.attributes:
                primitive.attributes['TANGENT'].byte_offset = offset + 12
            if 'NORMAL' in primitive.attributes:
                primitive.attributes['NORMAL'].byte_offset = offset + 16
            if 'TEXCOORD_0' in primitive.attributes:
                primitive.attributes['TEXCOORD_0'].byte_offset = offset + 20
            if 'TEXCOORD_1' in primitive.attributes:
                primitive.attributes['TEXCOORD_1'].byte_offset = offset + 24
            if 'COLOR_0' in primitive.attributes:
                primitive.attributes['COLOR_0'].byte_offset = offset + 28

            for vidx in range(count):
                start = vidx * expected_byte_stride

                # Pack data into buffer

                if 'POSITION' in primitive.attributes:
                    STRUCT_POSITION.pack_into(buffer, start, *primitive.attributes['POSITION'].buffer_view[vidx])
                if 'TANGENT' in primitive.attributes:
                    STRUCT_TANGENT.pack_into(buffer, start + 12, *primitive.attributes['TANGENT'].buffer_view[vidx])
                if 'NORMAL' in primitive.attributes:
                    STRUCT_NORMAL.pack_into(buffer, start + 16, *primitive.attributes['NORMAL'].buffer_view[vidx])
                if 'TEXCOORD_0' in primitive.attributes:
                    STRUCT_UV.pack_into(buffer, start + 20, *primitive.attributes['TEXCOORD_0'].buffer_view[vidx])
                if 'TEXCOORD_1' in primitive.attributes:
                    STRUCT_UV.pack_into(buffer, start + 24, *primitive.attributes['TEXCOORD_1'].buffer_view[vidx])
                if 'COLOR_0' in primitive.attributes:
                    STRUCT_COLOR_VTX.pack_into(buffer, start + 28, *primitive.attributes['COLOR_0'].buffer_view[vidx])

            # Add data to the buffer view
            vertex_nd_buffer_view.buffer.append_bytes(bytes(buffer), calculate_offset=False)
            if vertex_nd_buffer_view not in self.BufferViews:
                    self.BufferViews.append(vertex_nd_buffer_view)

            # Set attribute buffer view index
            for attribute in primitive.attributes:
                primitive.attributes[attribute].buffer_view = self.BufferViews.index(vertex_nd_buffer_view)
                primitive.attributes[attribute].name = f'{mesh.name}_vertices#0_{attribute}'

            #
            # Gather indices
            #

            all_indices = [] # Use a regular python list as appending is faster than using numpy

            # Add max index to the indices (this makes sure that meshes with more than one primitive render correctly)
            max_index = 0
            for primitive in mesh.primitives:
                indices = primitive.indices.buffer_view
                indices = np.array([x + max_index for x in indices])
                max_index = max(indices) + 1

                # Reverse indices (this makes the faces render in the correct direction)
                for i in range(0, len(indices), 3):
                    all_indices.append(indices[i + 2])
                    all_indices.append(indices[i + 1])
                    all_indices.append(indices[i + 0])

            primitive = mesh.primitives[0] # use first primitive
            indices_accessor = primitive.indices

            # Convert to numpy array
            dtype = gltf2_io_constants.ComponentType.to_numpy_dtype_asobo(indices_accessor.component_type)
            all_indices = np.array(all_indices, dtype=dtype)

            # Set binary data and append to buffer view
            binary_data = gltf2_io_binary_data.BinaryData(all_indices.tobytes())
            offset = self.BufferViewIndex.buffer.append_data(binary_data, check_padding=True, calculate_offset=True)
            if self.BufferViewIndex not in self.BufferViews:
                    self.BufferViews.append(self.BufferViewIndex)

            indices_accessor.buffer_view = self.BufferViews.index(self.BufferViewIndex)
            if offset != 0:
                indices_accessor.byte_offset = offset
            indices_accessor.count = len(all_indices)
            indices_accessor.name = f'{mesh.name}_indices#{len(mesh.primitives) - 1}'

            #
            # Distribute the shared accessors between all the primitives
            #

            total_asobo_primitive_count = 0
            for pidx, mesh_primitive in enumerate(mesh.primitives):
                for attribute in mesh_primitive.attributes:
                    mesh_primitive.attributes[attribute] = primitive.attributes[attribute]
                mesh_primitive.indices = indices_accessor

                # Set StartIndex
                if pidx > 0:
                    mesh_primitive.extras['ASOBO_primitive']['StartIndex'] = total_asobo_primitive_count * 3
                total_asobo_primitive_count += mesh_primitive.extras['ASOBO_primitive']['PrimitiveCount']

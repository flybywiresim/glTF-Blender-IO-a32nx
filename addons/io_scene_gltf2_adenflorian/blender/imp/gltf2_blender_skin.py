# Copyright 2018-2019 The glTF-Blender-IO authors.
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
from mathutils import Vector, Matrix
from ..com.gltf2_blender_conversion import matrix_gltf_to_blender, scale_to_matrix
from ...io.imp.gltf2_io_binary import BinaryData
from ..com.gltf2_blender_extras import set_extras

class BlenderSkin():
    """Blender Skinning / Armature."""
    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def create_armature(gltf, skin_id, parent):
        """Armature creation."""
        pyskin = gltf.data.skins[skin_id]

        if pyskin.name is not None:
            name = pyskin.name
        else:
            name = "Armature_" + str(skin_id)

        armature = bpy.data.armatures.new(name)
        obj = bpy.data.objects.new(name, armature)
        if gltf.blender_active_collection is not None:
            bpy.data.collections[gltf.blender_active_collection].objects.link(obj)
        else:
            bpy.data.scenes[gltf.blender_scene].collection.objects.link(obj)

            
        # bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.context.view_layer.update()
        bpy.context.object.data.display_type = 'STICK'

        pyskin.blender_armature_name = obj.name
        if parent is not None:
            obj.parent = bpy.data.objects[gltf.data.nodes[parent].blender_object]

    @staticmethod
    def set_bone_transforms(gltf, skin_id, bone, node_id, parent):
        """Set bone transformations."""
        pyskin = gltf.data.skins[skin_id]
        pynode = gltf.data.nodes[node_id]
        print('set_bone_transforms node: ' + pynode.name)
        # print('transform: ' + str(pynode.transform))
        print('translation: ' + str(pynode.translation))
        print('rotation: ' + str(pynode.rotation))
        print('scale: ' + str(pynode.scale))

        obj = bpy.data.objects[pyskin.blender_armature_name]

        # Set bone bind_pose by inverting bindpose matrix
        if node_id in pyskin.joints:
            index_in_skel = pyskin.joints.index(node_id)
            if pyskin.inverse_bind_matrices is not None:
                inverse_bind_matrices = BinaryData.get_data_from_accessor(gltf, pyskin.inverse_bind_matrices)
                # Needed to keep scale in matrix, as bone.matrix seems to drop it
                if index_in_skel < len(inverse_bind_matrices):
                    pynode.blender_bone_matrix = matrix_gltf_to_blender(
                        inverse_bind_matrices[index_in_skel]
                    ).inverted()
                    bone.matrix = pynode.blender_bone_matrix
                else:
                    gltf.log.error("Error with inverseBindMatrix for skin " + pyskin)
            else:
                pynode.blender_bone_matrix = Matrix() # 4x4 identity matrix
        else:
            print('No invBindMatrix for bone ' + str(node_id))
            pynode.blender_bone_matrix = Matrix()

        # Parent the bone
        if parent is not None and hasattr(gltf.data.nodes[parent], "blender_bone_name"):
            bone.parent = obj.data.edit_bones[gltf.data.nodes[parent].blender_bone_name]  # TODO if in another scene

        # Switch to Pose mode
        bpy.ops.object.mode_set(mode="POSE")
        obj.data.pose_position = 'POSE'

        # Set posebone location/rotation/scale (in armature space)
        # location is actual bone location minus it's original (bind) location
        bind_location = Matrix.Translation(pynode.blender_bone_matrix.to_translation())
        bind_rotation = pynode.blender_bone_matrix.to_quaternion()
        bind_scale = scale_to_matrix(pynode.blender_bone_matrix.to_scale())

        location, rotation, scale = matrix_gltf_to_blender(pynode.transform).decompose()
        if parent is not None and hasattr(gltf.data.nodes[parent], "blender_bone_matrix"):
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA ' + bone.name)
            parent_mat = gltf.data.nodes[parent].blender_bone_matrix

            # Get armature space location (bindpose + pose)
            # Then, remove original bind location from armspace location, and bind rotation
            final_location = (bind_location.inverted() @ parent_mat @ Matrix.Translation(location)).to_translation()
            obj.pose.bones[pynode.blender_bone_name].location = \
                bind_rotation.inverted().to_matrix().to_4x4() @ final_location

            # Do the same for rotation & scale
            obj.pose.bones[pynode.blender_bone_name].rotation_quaternion = \
                (pynode.blender_bone_matrix.inverted() @ parent_mat @
                    matrix_gltf_to_blender(pynode.transform)).to_quaternion()
            obj.pose.bones[pynode.blender_bone_name].scale = \
                (bind_scale.inverted() @ parent_mat @ scale_to_matrix(scale)).to_scale()

        else:
            x, y, z = bind_location.to_translation()
            print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB ' + str(bind_location.to_translation()))
            obj.pose.bones[pynode.blender_bone_name].location = Vector((-x, -z, y))
            obj.pose.bones[pynode.blender_bone_name].rotation_quaternion = bind_rotation.inverted() @ rotation
            obj.pose.bones[pynode.blender_bone_name].scale = bind_scale.inverted() @ scale

    @staticmethod
    def create_bone(gltf, skin_id, node_id, parent):
        """Bone creation."""
        pyskin = gltf.data.skins[skin_id]
        pynode = gltf.data.nodes[node_id]

        scene = bpy.data.scenes[gltf.blender_scene]
        obj = bpy.data.objects[pyskin.blender_armature_name]

        if bpy.app.version < (2, 80, 0):
            bpy.context.screen.scene = scene
            scene.objects.active = obj
        else:
            bpy.context.window.scene = scene
            bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode="EDIT")

        if pynode.name:
            name = pynode.name
        else:
            name = "Bone_" + str(node_id)

        bone = obj.data.edit_bones.new(name)
        pynode.blender_bone_name = bone.name
        pynode.blender_armature_name = pyskin.blender_armature_name
        bone.tail = Vector((0.0, 1.0 / obj.matrix_world.to_scale()[1], 0.0))  # Needed to keep bone alive
        # Custom prop on edit bone
        set_extras(bone, pynode.extras)

        # set bind and pose transforms
        BlenderSkin.set_bone_transforms(gltf, skin_id, bone, node_id, parent)
        bpy.ops.object.mode_set(mode="OBJECT")
        # Custom prop on pose bone
        if pynode.blender_bone_name in obj.pose.bones:
            set_extras(obj.pose.bones[pynode.blender_bone_name], pynode.extras)

    @staticmethod
    def create_vertex_groups(gltf, skin_id):
        """Vertex Group creation."""
        pyskin = gltf.data.skins[skin_id]
        for node_id in pyskin.node_ids:
            obj = bpy.data.objects[gltf.data.nodes[node_id].blender_object]
            for bone in pyskin.joints:
                obj.vertex_groups.new(name=gltf.data.nodes[bone].blender_bone_name)

    @staticmethod
    def create_armature_modifiers(gltf, skin_id):
        """Create Armature modifier."""
        pyskin = gltf.data.skins[skin_id]

        if pyskin.blender_armature_name is None:
            # TODO seems something is wrong
            # For example, some joints are in skin 0, and are in another skin too
            # Not sure this is glTF compliant, will check it
            return

        for node_id in pyskin.node_ids:
            node = gltf.data.nodes[node_id]
            obj = bpy.data.objects[node.blender_object]

            for obj_sel in bpy.context.scene.objects:
                obj_sel.select_set(False)
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            # bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            # Reparent skinned mesh to it's armature to avoid breaking
            # skinning with interleaved transforms

            # Get bone matrix from root bone of armature
            armature_obj = bpy.data.objects[pyskin.blender_armature_name]
            for bone in armature_obj.data.bones:
                if bone.parent is None:
                    for pynode in gltf.data.nodes:
                        if pynode.name == bone.name:
                            bind_location = Matrix.Translation(pynode.blender_bone_matrix.to_translation())
                            x, y, z = bind_location.to_translation()
                            print('FOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO obj.location ' + str(obj.location))
                            print('FOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO foo ' + str(pynode.blender_bone_matrix.to_translation()))
                            obj.location += Vector((x, -z, y))

            # bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            # Selects the mesh obj
            obj.select_set(True)
            # Selects the armature obj
            bpy.data.objects[pyskin.blender_armature_name].select_set(True)
            # Makes sure the armature obj was selected last so that it becomes the parent
            bpy.context.view_layer.objects.active = bpy.data.objects[pyskin.blender_armature_name]
            bpy.context.view_layer.update()
            # Actually does the parenting operation
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

            # obj.parent = bpy.data.objects[pyskin.blender_armature_name]
            arma = obj.modifiers.new(name="Armature", type="ARMATURE")
            arma.object = bpy.data.objects[pyskin.blender_armature_name]

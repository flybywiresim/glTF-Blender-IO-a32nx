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
from ..com.gltf2_blender_extras import set_extras
from .gltf2_blender_mesh import BlenderMesh
from .gltf2_blender_camera import BlenderCamera
from .gltf2_blender_skin import BlenderSkin
from .gltf2_blender_light import BlenderLight
from ..com.gltf2_blender_conversion import scale_to_matrix, matrix_gltf_to_blender, correction_rotation


class BlenderNode():
    """Blender Node."""
    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def create(gltf, node_idx, parent):
        """Node creation."""
        pynode = gltf.data.nodes[node_idx]
        print('creating blender node ' + pynode.name)

        # Blender attributes initialization
        pynode.blender_object = ""
        pynode.parent = parent

        gltf.display_current_node += 1
        if bpy.app.debug_value == 101:
            gltf.log.critical("Node " + str(gltf.display_current_node) + " of " + str(gltf.display_total_nodes) + " (idx " + str(node_idx) + ")")

        # The original code was either a bug or msfs gltf breaking standards
        # The original code broke when you had a node that had both a mesh and was a joint
        # If it was a mesh, it would return early and not setup the is joint stuff
        flag = False

        if pynode.is_joint:
            flag = True
            if pynode.name:
                gltf.log.info("Blender create Bone node " + pynode.name)
            else:
                gltf.log.info("Blender create Bone node")
            # Check if corresponding armature is already created, create it if needed
            if gltf.data.skins[pynode.skin_id].blender_armature_name is None:
                BlenderSkin.create_armature(gltf, pynode.skin_id, parent)

            BlenderSkin.create_bone(gltf, pynode.skin_id, node_idx, parent)

        if pynode.mesh is not None:
            flag = True
            instance = False
            if gltf.data.meshes[pynode.mesh].blender_name is not None:
                # Mesh is already created, only create instance
                # Except is current node is animated with path weight
                # Or if previous instance is animation at node level
                if pynode.weight_animation is True:
                    instance = False
                else:
                    if gltf.data.meshes[pynode.mesh].is_weight_animated is True:
                        instance = False
                    else:
                        instance = True
                        mesh = bpy.data.meshes[gltf.data.meshes[pynode.mesh].blender_name]

            if instance is False:
                if pynode.name:
                    gltf.log.info("Blender create Mesh node " + pynode.name)
                else:
                    gltf.log.info("Blender create Mesh node")

                mesh = BlenderMesh.create(gltf, pynode.mesh, node_idx, parent)

            if pynode.weight_animation is True:
                # flag this mesh instance as created only for this node, because of weight animation
                gltf.data.meshes[pynode.mesh].is_weight_animated = True

            if pynode.name:
                name = pynode.name
            else:
                # Take mesh name if exist
                if gltf.data.meshes[pynode.mesh].name:
                    name = gltf.data.meshes[pynode.mesh].name
                else:
                    name = "Object_" + str(node_idx)

            obj = bpy.data.objects.new(name, mesh)
            set_extras(obj, pynode.extras)
            obj.rotation_mode = 'QUATERNION'
            if bpy.app.version < (2, 80, 0):
                bpy.data.scenes[gltf.blender_scene].objects.link(obj)
            else:
                if gltf.blender_active_collection is not None:
                    bpy.data.collections[gltf.blender_active_collection].objects.link(obj)
                else:
                    bpy.data.scenes[gltf.blender_scene].collection.objects.link(obj)

            # Transforms apply only if this mesh is not skinned
            # See implementation node of gltf2 specification
            # if not (pynode.mesh is not None and pynode.skin is not None):
                # if not pynode.is_joint:
                # if pynode.is_skeleton is not True:
            BlenderNode.set_transforms(gltf, node_idx, pynode, obj, parent)
                # else:
                #     print('not setting transforms for skeleton ' + pynode.name)
                # else:
                #     print('not setting transforms for joint ' + pynode.name)
            pynode.blender_object = obj.name
            BlenderNode.set_parent(gltf, obj, parent)

            if instance == False:
                BlenderMesh.set_mesh(gltf, gltf.data.meshes[pynode.mesh], mesh, obj)

        if pynode.camera is not None:
            flag = True
            if pynode.name:
                gltf.log.info("Blender create Camera node " + pynode.name)
            else:
                gltf.log.info("Blender create Camera node")
            obj = BlenderCamera.create(gltf, pynode.camera)
            set_extras(obj, pynode.extras)
            BlenderNode.set_transforms(gltf, node_idx, pynode, obj, parent)  # TODO default rotation of cameras ?
            pynode.blender_object = obj.name
            BlenderNode.set_parent(gltf, obj, parent)

        if flag:
            if pynode.children:
                for child_idx in pynode.children:
                    BlenderNode.create(gltf, child_idx, node_idx)
            return

        # No mesh, no camera, no light. For now, create empty #TODO

        if pynode.name:
            gltf.log.info("Blender create Empty node " + pynode.name)
            obj = bpy.data.objects.new(pynode.name, None)
        else:
            gltf.log.info("Blender create Empty node")
            obj = bpy.data.objects.new("Node", None)
        set_extras(obj, pynode.extras)
        obj.rotation_mode = 'QUATERNION'
        if bpy.app.version < (2, 80, 0):
            bpy.data.scenes[gltf.blender_scene].objects.link(obj)
        else:
            if gltf.blender_active_collection is not None:
                bpy.data.collections[gltf.blender_active_collection].objects.link(obj)
            else:
                bpy.data.scenes[gltf.blender_scene].collection.objects.link(obj)

        BlenderNode.set_transforms(gltf, node_idx, pynode, obj, parent)
        pynode.blender_object = obj.name
        BlenderNode.set_parent(gltf, obj, parent)

        if pynode.children:
            for child_idx in pynode.children:
                BlenderNode.create(gltf, child_idx, node_idx)

    @staticmethod
    def set_parent(gltf, obj, parent):
        """Set parent."""
        if parent is None:
            return

        for node_idx, node in enumerate(gltf.data.nodes):
            if node_idx == parent:
                if node.blender_object:
                    obj.parent = bpy.data.objects[node.blender_object]
                    return

        gltf.log.error("ERROR, parent not found")

    @staticmethod
    def set_transforms(gltf, node_idx, pynode, obj, parent):
        """Set transforms."""
        print('node set_transforms node: ' + pynode.name)
        # print('transform: ' + str(pynode.transform))
        print('translation: ' + str(pynode.translation))
        print('rotation: ' + str(pynode.rotation))
        print('scale: ' + str(pynode.scale))

        if not (pynode.mesh is not None and pynode.skin is not None):
            obj.matrix_world = matrix_gltf_to_blender(pynode.transform)
        else:
            # do transforms stuff for skinned meshes
            # apply inverse transform
            obj.matrix_world = matrix_gltf_to_blender(pynode.transform).inverted()
            # do blender apply trasform operation
            # bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.context.view_layer.update()
            bpy.ops.object.transform_apply()
            # apply normal transform
            obj.matrix_world = matrix_gltf_to_blender(pynode.transform)
            # sleep?

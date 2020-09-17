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
from math import sqrt
from mathutils import Quaternion
from .gltf2_blender_node import BlenderNode
from .gltf2_blender_skin import BlenderSkin
from .gltf2_blender_animation import BlenderAnimation
from .gltf2_blender_animation_utils import simulate_stash
from ..com.gltf2_blender_conversion import matrix_gltf_to_blender


class BlenderScene():
    """Blender Scene."""
    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def create(gltf, scene_idx):
        """Scene creation."""
        gltf.blender_active_collection = None
        if scene_idx is not None:
            pyscene = gltf.data.scenes[scene_idx]
            # list_nodes = list(pyscene.nodes)
            # list_nodes = list(filter(lambda x: 'YOKE' in gltf.data.nodes[x].name or 'THROTTLE' in gltf.data.nodes[x].name, pyscene.nodes))
            list_nodes = list(filter(lambda x: 'YOKE' in gltf.data.nodes[x].name or 'THROTTLE' in gltf.data.nodes[x].name or 'COCKPIT' in gltf.data.nodes[x].name, pyscene.nodes))

            # Create a new scene only if not already exists in .blend file
            # TODO : put in current scene instead ?
            if pyscene.name not in [scene.name for scene in bpy.data.scenes]:
                # TODO: There is a bug in 2.8 alpha that break CLEAR_KEEP_TRANSFORM
                # if we are creating a new scene
                if bpy.app.version < (2, 80, 0):
                    if pyscene.name:
                        scene = bpy.data.scenes.new(pyscene.name)
                    else:
                        scene = bpy.context.scene
                else:
                    scene = bpy.context.scene
                    if bpy.context.collection.name in bpy.data.collections: # avoid master collection
                        gltf.blender_active_collection = bpy.context.collection.name
                if bpy.app.version < (2, 80, 0):
                    scene.render.engine = "CYCLES"
                else:
                    if scene.render.engine not in ['CYCLES', 'BLENDER_EEVEE']:
                        scene.render.engine = "BLENDER_EEVEE"

                gltf.blender_scene = scene.name
            else:
                gltf.blender_scene = pyscene.name

            # Switch to newly created main scene
            if bpy.app.version < (2, 80, 0):
                bpy.context.screen.scene = bpy.data.scenes[gltf.blender_scene]
            else:
                bpy.context.window.scene = bpy.data.scenes[gltf.blender_scene]
                if bpy.context.collection.name in bpy.data.collections: # avoid master collection
                    gltf.blender_active_collection = bpy.context.collection.name
            if bpy.app.version < (2, 80, 0):
                scene = bpy.context.scene
                scene.render.engine = "CYCLES"

        else:
            # No scene in glTF file, create all objects in current scene
            scene = bpy.context.scene
            if bpy.app.version < (2, 80, 0):
                scene.render.engine = "CYCLES"
            else:
                if scene.render.engine not in ['CYCLES', 'BLENDER_EEVEE']:
                    scene.render.engine = "BLENDER_EEVEE"
                if bpy.context.collection.name in bpy.data.collections: # avoid master collection
                    gltf.blender_active_collection = bpy.context.collection.name
            gltf.blender_scene = scene.name
            list_nodes = BlenderScene.get_root_nodes(gltf)

        if bpy.app.debug_value != 100:
            # Create Yup2Zup empty
            obj_rotation = bpy.data.objects.new("Yup2Zup", None)
            obj_rotation.rotation_mode = 'QUATERNION'
            obj_rotation.rotation_quaternion = Quaternion((sqrt(2) / 2, sqrt(2) / 2, 0.0, 0.0))

            if gltf.blender_active_collection is not None:
                bpy.data.collections[gltf.blender_active_collection].objects.link(obj_rotation)
            else:
                bpy.data.scenes[gltf.blender_scene].collection.objects.link(obj_rotation)

        if list_nodes is not None:
            for node_idx in list_nodes:
                BlenderNode.create(gltf, node_idx, None)  # None => No parent

        for skin_id, skin in enumerate(gltf.data.skins):
            skeleton_node = gltf.data.nodes[skin.skeleton]
            armature_obj = bpy.data.objects[skin.blender_armature_name]
            print('set transform for armature: ' + armature_obj.name)
            # print('transform: ' + str(skeleton_node.transform))
            print('translation: ' + str(skeleton_node.translation))
            print('rotation: ' + str(skeleton_node.rotation))
            print('scale: ' + str(skeleton_node.scale))
            print('before rotation_quaternion: ' + str(armature_obj.rotation_quaternion))
            armature_obj.rotation_mode = 'QUATERNION'
            armature_obj.matrix_world = matrix_gltf_to_blender(skeleton_node.transform)
            # armature_obj.location = skeleton_node.translation
            # armature_obj.rotation_quaternion = skeleton_node.rotation
            # armature_obj.scale = skeleton_node.scale
            
            print('after rotation_quaternion: ' + str(armature_obj.rotation_quaternion))

        # if gltf.data.animations:
        #     for anim_idx, anim in enumerate(gltf.data.animations):
        #         if 'yoke' not in anim.name and 'throttle' not in anim.name:
        #             continue
        #         print('processing animation ' + anim.name)
        #         # Blender armature name -> action all its bones should use
        #         gltf.arma_cache = {}
        #         # Things we need to stash when we're done.
        #         gltf.needs_stash = []

        #         if list_nodes is not None:
        #             for node_idx in list_nodes:
        #                 BlenderAnimation.anim(gltf, anim_idx, node_idx)

        #         for (obj, anim_name, action) in gltf.needs_stash:
        #             simulate_stash(obj, anim_name, action)

        #     # Restore first animation
        #     anim_name = gltf.data.animations[0].track_name
        #     for node_idx in list_nodes:
        #         BlenderAnimation.restore_animation(gltf, node_idx, anim_name)

        if bpy.app.debug_value != 100:
            # Parent root node to rotation object
            if list_nodes is not None:
                exclude_nodes = []
                for node_idx in list_nodes:
                    node = gltf.data.nodes[node_idx]
                    if node.is_joint:
                        # Do not change parent if root node is already parented (can be the case for skinned mesh)
                        if not bpy.data.objects[node.blender_armature_name].parent:
                            print('set rotation parent for ' + bpy.data.objects[node.blender_armature_name].name)
                            bpy.data.objects[node.blender_armature_name].parent = obj_rotation
                            print('set rotation parent for ' + bpy.data.objects[node.blender_object].name)
                            bpy.data.objects[node.blender_object].parent = obj_rotation
                        else:
                            print('no rotation parent for ' + node.name)
                            exclude_nodes.append(node_idx)
                    else:
                        # Do not change parent if root node is already parented (can be the case for skinned mesh)
                        if not bpy.data.objects[node.blender_object].parent:
                            print('set rotation parent for ' + node.name)
                            bpy.data.objects[node.blender_object].parent = obj_rotation
                        else:
                            print('no rotation parent for ' + node.name)
                            exclude_nodes.append(node_idx)

                # if gltf.animation_object is False:
                # Avoid rotation bug if collection is hidden or disabled
                if gltf.blender_active_collection is not None:
                    gltf.collection_hide_viewport = bpy.data.collections[gltf.blender_active_collection].hide_viewport
                    bpy.data.collections[gltf.blender_active_collection].hide_viewport = False
                    # TODO for visibility ... but seems not exposed on bpy for now

                for node_idx in list_nodes:

                    if node_idx in exclude_nodes:
                        continue # for root node that are parented by the process
                        # for example skinned meshes

                    for obj_ in bpy.context.scene.objects:
                        obj_.select_set(False)
                    if gltf.data.nodes[node_idx].is_joint:
                        bpy.data.objects[gltf.data.nodes[node_idx].blender_armature_name].select_set(True)
                        bpy.context.view_layer.objects.active = bpy.data.objects[gltf.data.nodes[node_idx].blender_armature_name]

                    bpy.data.objects[gltf.data.nodes[node_idx].blender_object].select_set(True)
                    bpy.context.view_layer.objects.active = bpy.data.objects[gltf.data.nodes[node_idx].blender_object]

                    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

                # remove object
                #bpy.context.scene.collection.objects.unlink(obj_rotation)
                bpy.data.objects.remove(obj_rotation)

                # Restore collection hidden / disabled values
                if gltf.blender_active_collection is not None:
                    bpy.data.collections[gltf.blender_active_collection].hide_viewport = gltf.collection_hide_viewport
                    # TODO restore visibility when expose in bpy
        
        for skin_id, skin in enumerate(gltf.data.skins):
            skeleton_node = gltf.data.nodes[skin.skeleton]
            armature_obj = bpy.data.objects[skin.blender_armature_name]
            print('set transform for armature 2: ' + armature_obj.name)
            # print('transform: ' + str(skeleton_node.transform))
            print('translation: ' + str(skeleton_node.translation))
            print('rotation: ' + str(skeleton_node.rotation))
            print('scale: ' + str(skeleton_node.scale))
            print('before rotation_quaternion: ' + str(armature_obj.rotation_quaternion))
            # armature_obj.matrix_world = matrix_gltf_to_blender(skeleton_node.transform).to_q
            # armature_obj.location = skeleton_node.translation
            x, y, z, w = skeleton_node.rotation
            armature_obj.rotation_quaternion = Quaternion((w, x, y, z))
            # armature_obj.scale = skeleton_node.scale
            print('after rotation_quaternion: ' + str(armature_obj.rotation_quaternion))

        # Now that all mesh / bones are created, create vertex groups on mesh
        if gltf.data.skins:
            for skin_id, skin in enumerate(gltf.data.skins):
                if hasattr(skin, "node_ids"):
                    print('BlenderSkin.create_vertex_groups ' + skin.name)
                    BlenderSkin.create_vertex_groups(gltf, skin_id)

            for skin_id, skin in enumerate(gltf.data.skins):
                if hasattr(skin, "node_ids"):
                    print('BlenderSkin.create_armature_modifiers ' + skin.name)
                    BlenderSkin.create_armature_modifiers(gltf, skin_id)
        
        for pynode in gltf.data.nodes:
            if pynode.is_joint:
                print('parenting joint: ' + pynode.name)
                # print('transform: ' + str(pynode.transform))
                print('translation: ' + str(pynode.translation))
                print('rotation: ' + str(pynode.rotation))
                print('scale: ' + str(pynode.scale))
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[pynode.blender_armature_name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[pynode.blender_armature_name]

                bpy.ops.object.mode_set(mode='EDIT')
                # Sets a bone as active to become the parent bone of the mesh obj
                bpy.data.objects[pynode.blender_armature_name].data.edit_bones.active = \
                    bpy.data.objects[pynode.blender_armature_name].data.edit_bones[pynode.blender_bone_name]
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                obj = bpy.data.objects[pynode.blender_object]
                # Selects the mesh obj
                obj.select_set(True)
                # Selects the armature obj
                bpy.data.objects[pynode.blender_armature_name].select_set(True)
                # Makes sure the armature obj was selected last so that it becomes the parent
                bpy.context.view_layer.objects.active = bpy.data.objects[pynode.blender_armature_name]
                bpy.context.view_layer.update()
                # Actually does the parenting operation
                bpy.ops.object.parent_set(type='BONE_RELATIVE', keep_transform=True)
                # From world transform to local (-armature transform -bone transform)
                # bone_trans = bpy.data.objects[pynode.blender_armature_name] \
                #     .pose.bones[pynode.blender_bone_name].matrix.to_translation().copy()
                # bone_rot = bpy.data.objects[pynode.blender_armature_name] \
                #     .pose.bones[pynode.blender_bone_name].matrix.to_quaternion().copy()
                # bone_scale_mat = scale_to_matrix(pynode.blender_bone_matrix.to_scale())
                # obj.location = bone_scale_mat @ obj.location
                # obj.location = bone_rot @ obj.location
                # obj.location += bone_trans
                # obj.location = bpy.data.objects[pynode.blender_armature_name].matrix_world.to_quaternion() \
                #     @ obj.location
                # obj.rotation_quaternion = obj.rotation_quaternion \
                #     @ bpy.data.objects[pynode.blender_armature_name].matrix_world.to_quaternion()
                # obj.scale = bone_scale_mat @ obj.scale


        # Make first root object the new active one
        if list_nodes is not None:
            if gltf.data.nodes[list_nodes[0]].blender_object:
                bl_name = gltf.data.nodes[list_nodes[0]].blender_object
            else:
                bl_name = gltf.data.nodes[list_nodes[0]].blender_armature_name
            if bpy.app.version < (2, 80, 0):
                bpy.context.scene.objects.active = bpy.data.objects[bl_name]
            else:
                bpy.context.view_layer.objects.active = bpy.data.objects[bl_name]

    @staticmethod
    def get_root_nodes(gltf):
        if gltf.data.nodes is None:
            return None

        parents = {}
        for idx, node  in enumerate(gltf.data.nodes):
            pynode = gltf.data.nodes[idx]
            if pynode.children:
                for child_idx in pynode.children:
                    parents[child_idx] = idx

        roots = []
        for idx, node in enumerate(gltf.data.nodes):
            if idx not in parents.keys():
                roots.append(idx)

        return roots

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
from bpy.types import Material, Panel, PropertyGroup

class MATERIAL_PT_MSFSMaterials(Panel):
    """MSFS custom material panel"""
    bl_label = "MSFS Materials"
    bl_idname = "MATERIAL_PT_MSFSMaterials"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    def draw(self, context):
        layout = self.layout
        mat = context.active_object.active_material

        if mat:
            layout = layout.box()
            layout.label(text = "Material Type", icon = "MATERIAL")
            layout.prop(mat, "msfs_material_type", text = "Type")

            if mat.msfs_material_type != "NONE": # Just a note to anyone wondering why this isn't msfs_material_type is not None, it's because the material type is a string enum property
                # Properties
                if mat.msfs_show_colors:
                    box = layout.box()
                    box.label(text = "Colors", icon = "COLOR")
                    row = box.row()
                    row.prop(mat, "msfs_base_color_factor")
                    if mat.msfs_show_emissive_color:
                        row = box.row()
                        row.prop(mat, "msfs_emissive_factor")
                    if mat.msfs_show_sss_color:
                        row = box.row()
                        row.prop(mat, "msfs_sss_color")
                if mat.msfs_show_alpha_mode:
                    box = layout.box()
                    box.label(text = "Alpha Mode", icon = "NODE_MATERIAL")
                    box.prop(mat, "msfs_alpha_mode")
                if mat.msfs_show_render_options:
                    box = layout.box()
                    box.label(text = "Render Options", icon = "VIEW_CAMERA")
                    box.prop(mat, "msfs_draw_order")
                    box.prop(mat, "msfs_dont_cast_shadows")
                    box.prop(mat, "msfs_double_sided")
                    if mat.msfs_show_day_night_cycle:
                        box.prop(mat, "msfs_day_night_cycle")
                if mat.msfs_show_pearl:
                    box = layout.box()
                    box.label(text = "Pearlescent Options", icon = "NODE_MATERIAL")
                    box.prop(mat, "msfs_use_pearl_effect")
                    box.prop(mat, "msfs_pearl_shift")
                    box.prop(mat, "msfs_pearl_range")
                    box.prop(mat, "msfs_pearl_brightness")
                if mat.msfs_show_gameplay_options:
                    box = layout.box()
                    box.label(text = "Gameplay Options", icon = "GHOST_ENABLED")
                    box.prop(mat, "msfs_collision_material")
                    box.prop(mat, "msfs_road_material")
                if mat.msfs_show_uv_options:
                    box = layout.box()
                    box.label(text = "UV Options", icon = "UV")
                    box.prop(mat, "msfs_uv_offset_u")
                    box.prop(mat, "msfs_uv_offset_v")
                    box.prop(mat, "msfs_uv_tiling_u")
                    box.prop(mat, "msfs_uv_tiling_v")
                    box.prop(mat, "msfs_uv_rotation")
                    box.prop(mat, "msfs_uv_clamp_u")
                    box.prop(mat, "msfs_uv_clamp_v")
                if mat.msfs_show_material_options:
                    box = layout.box()
                    box.label(text = "Material Options", icon = "MATERIAL")
                    box.prop(mat, "msfs_roughness_factor")
                    box.prop(mat, "msfs_metallic_factor")
                    box.prop(mat, "msfs_normal_scale")
                    if mat.msfs_alpha_mode == "MASK" and mat.msfs_show_alpha_mode:
                        box.prop(mat, "msfs_alpha_cutoff")
                    # Detail options
                    if mat.msfs_show_material_detail_options:
                        box.prop(mat, "msfs_detail_uv_scale")
                        box.prop(mat, "msfs_detail_uv_offset_u")
                        box.prop(mat, "msfs_detail_uv_offset_v")
                        box.prop(mat, "msfs_detail_normal_scale")
                    if mat.msfs_show_blend_threshold:
                        box.prop(mat, "msfs_blend_threshold")
                if mat.msfs_show_decal_blend_factors:
                    box = layout.box()
                    box.label(text = "Decal Blend Factors", icon = "OUTLINER_OB_POINTCLOUD")
                    box.prop(mat, "msfs_decal_color_blend_factor")
                    box.prop(mat, "msfs_decal_metal_blend_factor")
                    box.prop(mat, "msfs_decal_normal_blend_factor")
                    box.prop(mat, "msfs_decal_roughness_blend_factor")
                    if mat.msfs_material_type == "msfs_geo_decal":
                        box.prop(mat, "msfs_decal_occlusion_blend_factor", text = "Blast Sys")
                        box.prop(mat, "msfs_decal_emissive_blend_factor", text = "Melt Sys")
                    else:
                        box.prop(mat, "msfs_decal_occlusion_blend_factor")
                        box.prop(mat, "msfs_decal_emissive_blend_factor")
                if mat.msfs_show_windshield_options:
                    box = layout.box()
                    box.label(text = "Windshield Options", icon = "MATFLUID")
                    box.prop(mat, "msfs_rain_drop_scale")
                    box.prop(mat, "msfs_wiper_1_state")
                    box.prop(mat, "msfs_wiper_2_state")
                if mat.msfs_show_glass_options:
                    box = layout.box()
                    box.label(text = "Glass Options", icon = "SHADING_RENDERED")
                    box.prop(mat, "msfs_glass_reflection_factor")
                    box.prop(mat, "msfs_glass_deformation_factor")
                if mat.msfs_show_parallax_options:
                    box = layout.box()
                    box.label(text = "Parallax Options", icon = "MATERIAL")
                    box.prop(mat, "msfs_parallax_scale")
                    box.prop(mat, "msfs_parallax_room_size_x")
                    box.prop(mat, "msfs_parallax_room_size_y")
                    box.prop(mat, "msfs_parallax_room_number")
                    box.prop(mat, "msfs_parallax_corridor")
                if mat.msfs_show_fresnel_options:
                    box = layout.box()
                    box.label(text = "Fresnel Options", icon = "COLORSET_13_VEC")
                    box.prop(mat, "msfs_fresnel_factor")
                    box.prop(mat, "msfs_fresnel_opacity_bias")

                # Textures
                if (mat.msfs_show_base_color_texture or mat.msfs_show_comp_texture or mat.msfs_show_normal_texture or mat.msfs_show_emissive_texture or mat.msfs_show_detail_color_texture \
                    or mat.msfs_show_detail_comp_texture or mat.msfs_show_detail_normal_texture or mat.msfs_show_blend_mask_texture or mat.msfs_show_wetness_ao_texture \
                        or mat.msfs_show_dirt_texture or mat.msfs_show_height_map_texture):
                    box = layout.box()
                    box.label(text = "Textures", icon = "TEXTURE")
                    if mat.msfs_show_base_color_texture: # Base Color
                        if mat.msfs_material_type == "msfs_parallax":
                            box.label(text = "Front Glass Color")
                        else:
                            box.label(text = "Base Color")
                        box.template_ID(mat, "msfs_base_color_texture", new = "image.new", open = "image.open")

                    if mat.msfs_show_comp_texture: # Composite
                        box.label(text = "Composite (Occlusion (R), Roughness (G), Metalness (B))")
                        box.template_ID(mat, "msfs_comp_texture", new = "image.new", open = "image.open")

                    if mat.msfs_show_normal_texture: # Normal
                        if mat.msfs_material_type == "msfs_parallax":
                            box.label(text = "Front Glass Normal")
                        else:
                            box.label(text = "Normal")
                        box.template_ID(mat, "msfs_normal_texture", new = "image.new", open = "image.open")

                    if mat.msfs_show_emissive_texture: # Emissive
                        if mat.msfs_material_type == "msfs_windshield":
                            box.label(text = "Secondary Details (A)")
                        elif mat.msfs_material_type == "msfs_parallax":
                            box.label(text = "Emissive Inside Window (RGB), Offset Time (A)")
                        else:
                            box.label(text = "Emissive")
                        box.template_ID(mat, "msfs_emissive_texture", new = "image.new", open = "image.open")
                        
                    if mat.msfs_show_detail_color_texture: # Detail Color
                        if mat.msfs_material_type == "msfs_windshield":
                            box.label(text = "Details Scratch (R), Icing Mask (G), Fingerprints (B)")
                        elif mat.msfs_material_type == "msfs_parallax":
                            box.label(text = "Behind Glass Color (RGB), Alpha (A)")
                        else:
                            if mat.msfs_blend_mask_texture is None:
                                box.label(text = "Detail Color (RGB), Alpha (A)")
                            else:
                                box.label(text = "Secondary Color (RGB), Alpha (A)")
                        box.template_ID(mat, "msfs_detail_color_texture", new = "image.new", open = "image.open")

                    if mat.msfs_show_detail_comp_texture: # Detail Composite
                        if mat.msfs_material_type == "msfs_geo_decal":
                            box.label(text = "Melt Pattern (R), Roughness (G), Metallic (B)")
                        else:
                            if mat.msfs_blend_mask_texture is None:
                                box.label(text = "Detail Composite (Occlusion (R), Roughness (G), Metallic (B))")
                            else:
                                box.label(text = "Secondary Occlusion (R), Roughness (G), Metallic (B)")
                        box.template_ID(mat, "msfs_detail_comp_texture", new = "image.new", open = "image.open")

                    if mat.msfs_show_detail_normal_texture: # Detail Normal
                        if mat.msfs_material_type == "msfs_windshield":
                            box.label(text = "Icing Normal (use Detail Map UV)")
                        else:
                            if mat.msfs_blend_mask_texture is None:
                                box.label(text = "Detail Normal")
                            else:
                                box.label(text = "Secondary Normal")
                        box.template_ID(mat, "msfs_detail_normal_texture", new = "image.new", open = "image.open")

                    if mat.msfs_show_blend_mask_texture: # Blend Mask
                        box.label(text = "Blend Mask")
                        box.template_ID(mat, "msfs_blend_mask_texture", new = "image.new", open = "image.open")

                    if mat.msfs_show_wetness_ao_texture: # Wetness AO
                        if mat.msfs_material_type == "msfs_windshield":
                            box.label(text = "Wiper Mask (RG)")
                        elif mat.msfs_material_type == "msfs_anisotropic" or mat.msfs_material_type == "msfs_hair":
                            box.label(text = "Anisotropic Direction (RG)")
                        box.template_ID(mat, "msfs_wetness_ao_texture", new = "image.new", open = "image.open")
                        
                    if mat.msfs_show_dirt_texture: # Dirt
                        if mat.msfs_material_type == "msfs_clearcoat":
                            box.label(text = "Clearcoat Amount (R), Clearcoat roughness (G)")
                        box.template_ID(mat, "msfs_dirt_texture", new = "image.new", open = "image.open")
                        
                    #if mat.msfs_show_height_map_texture: Doesn't seem to be enabled yet in the 3DS Max Plugin

classes = (
    MATERIAL_PT_MSFSMaterials,
)

register, unregister = bpy.utils.register_classes_factory(classes)

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
from bpy.types import Material, Panel, PropertyGroup, Image
from bpy.props import EnumProperty, FloatVectorProperty, FloatProperty, IntProperty, BoolProperty, PointerProperty

def updateMaterial(self, context):
    mat = context.active_object.active_material

    if mat is not None:
        if mat.msfs_material_type == "msfs_standard": # Standard
            # Properties
            mat.msfs_show_colors = True
            mat.msfs_show_emissive_color = True

            mat.msfs_show_alpha_mode = True

            mat.msfs_show_render_options = True
            mat.msfs_show_day_night_cycle = True

            mat.msfs_show_pearl = True

            mat.msfs_show_gameplay_options = True

            mat.msfs_show_uv_options = True

            mat.msfs_show_material_options = True
            mat.msfs_show_material_detail_options = True
            mat.msfs_show_blend_threshold = True

            mat.msfs_show_decal_blend_factors = False

            mat.msfs_show_windshield_options = False

            mat.msfs_show_glass_options = False

            mat.msfs_show_parallax_options = False

            mat.msfs_show_sss_color = False

            mat.msfs_show_fresnel_options = False

            # Textures
            Material.msfs_show_base_color_texture = True
            Material.msfs_show_comp_texture = True
            Material.msfs_show_normal_texture = True
            Material.msfs_show_emissive_texture = True
            Material.msfs_show_detail_color_texture = True
            Material.msfs_show_detail_comp_texture = True
            Material.msfs_show_detail_normal_texture = True
            Material.msfs_show_blend_mask_texture = True
            Material.msfs_show_wetness_ao_texture = False
            Material.msfs_show_dirt_texture = False
            Material.msfs_show_height_map_texture = False
            
        elif mat.msfs_material_type == "msfs_decal": # Decal
            # Properties
            mat.msfs_show_colors = True
            mat.msfs_show_emissive_color = True

            mat.msfs_show_alpha_mode = False

            mat.msfs_show_render_options = True
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_pearl = True

            mat.msfs_show_gameplay_options = True

            mat.msfs_show_uv_options = True

            mat.msfs_show_material_options = True
            mat.msfs_show_material_detail_options = True
            mat.msfs_show_blend_threshold = True

            mat.msfs_show_decal_blend_factors = True

            mat.msfs_show_windshield_options = False

            mat.msfs_show_glass_options = False

            mat.msfs_show_parallax_options = False

            mat.msfs_show_sss_color = False

            mat.msfs_show_fresnel_options = False

            # Textures
            Material.msfs_show_base_color_texture = True
            Material.msfs_show_comp_texture = True
            Material.msfs_show_normal_texture = True
            Material.msfs_show_emissive_texture = True
            Material.msfs_show_detail_color_texture = True
            Material.msfs_show_detail_comp_texture = True
            Material.msfs_show_detail_normal_texture = True
            Material.msfs_show_blend_mask_texture = True
            Material.msfs_show_wetness_ao_texture = False
            Material.msfs_show_dirt_texture = False
            Material.msfs_show_height_map_texture = False

        elif mat.msfs_material_type == "msfs_windshield": # Windshield
            # Properties
            mat.msfs_show_colors = True
            mat.msfs_show_emissive_color = True

            mat.msfs_show_alpha_mode = False

            mat.msfs_show_render_options = True
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_pearl = True

            mat.msfs_show_gameplay_options = True

            mat.msfs_show_uv_options = True

            mat.msfs_show_material_options = True
            mat.msfs_show_material_detail_options = True
            mat.msfs_show_blend_threshold = True

            mat.msfs_show_decal_blend_factors = False

            mat.msfs_show_windshield_options = True

            mat.msfs_show_glass_options = False

            mat.msfs_show_parallax_options = False

            mat.msfs_show_sss_color = False

            mat.msfs_show_fresnel_options = False

            # Textures
            Material.msfs_show_base_color_texture = True
            Material.msfs_show_comp_texture = True
            Material.msfs_show_normal_texture = True
            Material.msfs_show_emissive_texture = True
            Material.msfs_show_detail_color_texture = True
            Material.msfs_show_detail_comp_texture = True
            Material.msfs_show_detail_normal_texture = True
            Material.msfs_show_blend_mask_texture = True
            Material.msfs_show_wetness_ao_texture = True
            Material.msfs_show_dirt_texture = False
            Material.msfs_show_height_map_texture = False

        elif mat.msfs_material_type == "msfs_porthole": # Porthole
            # Properties
            mat.msfs_show_colors = True
            mat.msfs_show_emissive_color = True

            mat.msfs_show_alpha_mode = False

            mat.msfs_show_render_options = True
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_pearl = True

            mat.msfs_show_gameplay_options = True

            mat.msfs_show_uv_options = True

            mat.msfs_show_material_options = True
            mat.msfs_show_material_detail_options = True
            mat.msfs_show_blend_threshold = True

            mat.msfs_show_decal_blend_factors = False

            mat.msfs_show_windshield_options = False

            mat.msfs_show_glass_options = False

            mat.msfs_show_parallax_options = False

            mat.msfs_show_sss_color = False

            mat.msfs_show_fresnel_options = False

            # Textures
            Material.msfs_show_base_color_texture = True
            Material.msfs_show_comp_texture = True
            Material.msfs_show_normal_texture = True
            Material.msfs_show_emissive_texture = True
            Material.msfs_show_detail_color_texture = True
            Material.msfs_show_detail_comp_texture = True
            Material.msfs_show_detail_normal_texture = True
            Material.msfs_show_blend_mask_texture = True
            Material.msfs_show_wetness_ao_texture = False
            Material.msfs_show_dirt_texture = False
            Material.msfs_show_height_map_texture = False

        elif mat.msfs_material_type == "msfs_glass": # Glass
            # Properties
            mat.msfs_show_colors = True
            mat.msfs_show_emissive_color = True

            mat.msfs_show_alpha_mode = False

            mat.msfs_show_render_options = True
            mat.msfs_show_day_night_cycle = False
            
            mat.msfs_show_pearl = True

            mat.msfs_show_gameplay_options = True

            mat.msfs_show_uv_options = True

            mat.msfs_show_material_options = True
            mat.msfs_show_material_detail_options = True
            mat.msfs_show_blend_threshold = True

            mat.msfs_show_decal_blend_factors = False

            mat.msfs_show_windshield_options = False

            mat.msfs_show_glass_options = True

            mat.msfs_show_parallax_options = False

            mat.msfs_show_sss_color = False

            mat.msfs_show_fresnel_options = False

            # Textures
            Material.msfs_show_base_color_texture = True
            Material.msfs_show_comp_texture = True
            Material.msfs_show_normal_texture = True
            Material.msfs_show_emissive_texture = True
            Material.msfs_show_detail_color_texture = True
            Material.msfs_show_detail_comp_texture = True
            Material.msfs_show_detail_normal_texture = True
            Material.msfs_show_blend_mask_texture = True
            Material.msfs_show_wetness_ao_texture = False
            Material.msfs_show_dirt_texture = False
            Material.msfs_show_height_map_texture = False

        elif mat.msfs_material_type == "msfs_geo_decal": # Geo Decal (Frosted)
            # Properties
            mat.msfs_show_colors = True
            mat.msfs_show_emissive_color = True

            mat.msfs_show_alpha_mode = False

            mat.msfs_show_render_options = True
            mat.msfs_show_day_night_cycle = False
            
            mat.msfs_show_pearl = True

            mat.msfs_show_gameplay_options = True

            mat.msfs_show_uv_options = True

            mat.msfs_show_material_options = True
            mat.msfs_show_material_detail_options = True
            mat.msfs_show_blend_threshold = True

            mat.msfs_show_decal_blend_factors = True

            mat.msfs_show_windshield_options = False

            mat.msfs_show_glass_options = False

            mat.msfs_show_parallax_options = False

            mat.msfs_show_sss_color = False

            mat.msfs_show_fresnel_options = False

            # Textures
            Material.msfs_show_base_color_texture = True
            Material.msfs_show_comp_texture = True
            Material.msfs_show_normal_texture = True
            Material.msfs_show_emissive_texture = True
            Material.msfs_show_detail_color_texture = True
            Material.msfs_show_detail_comp_texture = True
            Material.msfs_show_detail_normal_texture = True
            Material.msfs_show_blend_mask_texture = False
            Material.msfs_show_wetness_ao_texture = False
            Material.msfs_show_dirt_texture = False
            Material.msfs_show_height_map_texture = False

        elif mat.msfs_material_type == "msfs_clearcoat": # Clearcoat
            # Properties
            mat.msfs_show_colors = True
            mat.msfs_show_emissive_color = True

            mat.msfs_show_alpha_mode = True

            mat.msfs_show_render_options = True
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_pearl = True

            mat.msfs_show_gameplay_options = True

            mat.msfs_show_uv_options = True

            mat.msfs_show_material_options = True
            mat.msfs_show_material_detail_options = True
            mat.msfs_show_blend_threshold = True

            mat.msfs_show_decal_blend_factors = False

            mat.msfs_show_windshield_options = False

            mat.msfs_show_glass_options = False

            mat.msfs_show_parallax_options = False

            mat.msfs_show_sss_color = False

            mat.msfs_show_fresnel_options = False

            # Textures
            Material.msfs_show_base_color_texture = True
            Material.msfs_show_comp_texture = True
            Material.msfs_show_normal_texture = True
            Material.msfs_show_emissive_texture = True
            Material.msfs_show_detail_color_texture = True
            Material.msfs_show_detail_comp_texture = True
            Material.msfs_show_detail_normal_texture = True
            Material.msfs_show_blend_mask_texture = True
            Material.msfs_show_wetness_ao_texture = False
            Material.msfs_show_dirt_texture = True
            Material.msfs_show_height_map_texture = False

        elif mat.msfs_material_type == "msfs_parallax": # Parallax
            # Properties
            mat.msfs_show_colors = True
            mat.msfs_show_emissive_color = True

            mat.msfs_show_alpha_mode = True

            mat.msfs_show_render_options = True
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_pearl = True

            mat.msfs_show_gameplay_options = True

            mat.msfs_show_uv_options = True

            mat.msfs_show_material_options = True
            mat.msfs_show_material_detail_options = False
            mat.msfs_show_blend_threshold = True

            mat.msfs_show_decal_blend_factors = False

            mat.msfs_show_windshield_options = False

            mat.msfs_show_glass_options = False

            mat.msfs_show_parallax_options = True

            mat.msfs_show_sss_color = False

            mat.msfs_show_fresnel_options = False

            # Textures
            Material.msfs_show_base_color_texture = True
            Material.msfs_show_comp_texture = True
            Material.msfs_show_normal_texture = True
            Material.msfs_show_emissive_texture = True
            Material.msfs_show_detail_color_texture = True
            Material.msfs_show_detail_comp_texture = False
            Material.msfs_show_detail_normal_texture = False
            Material.msfs_show_blend_mask_texture = False
            Material.msfs_show_wetness_ao_texture = False
            Material.msfs_show_dirt_texture = False
            Material.msfs_show_height_map_texture = False

        elif mat.msfs_material_type == "msfs_anisotropic": # Anisotropic
            # Properties
            mat.msfs_show_colors = True
            mat.msfs_show_emissive_color = True

            mat.msfs_show_alpha_mode = True

            mat.msfs_show_render_options = True
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_pearl = True

            mat.msfs_show_gameplay_options = True

            mat.msfs_show_uv_options = True

            mat.msfs_show_material_options = True
            mat.msfs_show_material_detail_options = True
            mat.msfs_show_blend_threshold = True

            mat.msfs_show_decal_blend_factors = False

            mat.msfs_show_windshield_options = False

            mat.msfs_show_glass_options = False

            mat.msfs_show_parallax_options = False

            mat.msfs_show_sss_color = False

            mat.msfs_show_fresnel_options = False

            # Textures
            Material.msfs_show_base_color_texture = True
            Material.msfs_show_comp_texture = True
            Material.msfs_show_normal_texture = True
            Material.msfs_show_emissive_texture = True
            Material.msfs_show_detail_color_texture = True
            Material.msfs_show_detail_comp_texture = True
            Material.msfs_show_detail_normal_texture = True
            Material.msfs_show_blend_mask_texture = True
            Material.msfs_show_wetness_ao_texture = True
            Material.msfs_show_dirt_texture = False
            Material.msfs_show_height_map_texture = False

        elif mat.msfs_material_type == "msfs_hair": # Hair
            # Properties
            mat.msfs_show_colors = True
            mat.msfs_show_emissive_color = True

            mat.msfs_show_alpha_mode = True

            mat.msfs_show_render_options = True
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_pearl = True

            mat.msfs_show_gameplay_options = True

            mat.msfs_show_uv_options = True

            mat.msfs_show_material_options = True
            mat.msfs_show_material_detail_options = True
            mat.msfs_show_blend_threshold = True

            mat.msfs_show_decal_blend_factors = False

            mat.msfs_show_windshield_options = False

            mat.msfs_show_glass_options = False

            mat.msfs_show_parallax_options = False

            mat.msfs_show_sss_color = False # Doesn't seem to be enabled in the 3DS Max plugin

            mat.msfs_show_fresnel_options = False

            # Textures
            Material.msfs_show_base_color_texture = True
            Material.msfs_show_comp_texture = True
            Material.msfs_show_normal_texture = True
            Material.msfs_show_emissive_texture = True
            Material.msfs_show_detail_color_texture = False
            Material.msfs_show_detail_comp_texture = False
            Material.msfs_show_detail_normal_texture = False
            Material.msfs_show_blend_mask_texture = False
            Material.msfs_show_wetness_ao_texture = True
            Material.msfs_show_dirt_texture = False
            Material.msfs_show_height_map_texture = False

        elif mat.msfs_material_type == "msfs_sss": # SSS
            # Properties
            mat.msfs_show_colors = True
            mat.msfs_show_emissive_color = True

            mat.msfs_show_alpha_mode = True

            mat.msfs_show_render_options = True
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_pearl = True

            mat.msfs_show_gameplay_options = True

            mat.msfs_show_uv_options = True

            mat.msfs_show_material_options = True
            mat.msfs_show_material_detail_options = False
            mat.msfs_show_blend_threshold = False

            mat.msfs_show_decal_blend_factors = False

            mat.msfs_show_windshield_options = False

            mat.msfs_show_glass_options = False

            mat.msfs_show_parallax_options = False

            mat.msfs_show_sss_color = False # Doesn't seem to be enabled in the 3DS Max plugin
            
            mat.msfs_show_fresnel_options = False

            # Textures
            Material.msfs_show_base_color_texture = True
            Material.msfs_show_comp_texture = True
            Material.msfs_show_normal_texture = True
            Material.msfs_show_emissive_texture = True
            Material.msfs_show_detail_color_texture = False
            Material.msfs_show_detail_comp_texture = False
            Material.msfs_show_detail_normal_texture = False
            Material.msfs_show_blend_mask_texture = False
            Material.msfs_show_wetness_ao_texture = False
            Material.msfs_show_dirt_texture = False
            Material.msfs_show_height_map_texture = False

        elif mat.msfs_material_type == "msfs_invisible": # Invisible
            # Properties
            mat.msfs_show_colors = True
            mat.msfs_show_emissive_color = False

            mat.msfs_show_alpha_mode = False

            mat.msfs_show_render_options = False
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_pearl = True

            mat.msfs_show_gameplay_options = True

            mat.msfs_show_uv_options = True

            mat.msfs_show_material_options = False
            mat.msfs_show_material_detail_options = False
            mat.msfs_show_blend_threshold = False

            mat.msfs_show_decal_blend_factors = False

            mat.msfs_show_windshield_options = False

            mat.msfs_show_glass_options = False

            mat.msfs_show_parallax_options = False

            mat.msfs_show_sss_color = False

            mat.msfs_show_fresnel_options = False

            # Textures
            Material.msfs_show_base_color_texture = False
            Material.msfs_show_comp_texture = False
            Material.msfs_show_normal_texture = False
            Material.msfs_show_emissive_texture = False
            Material.msfs_show_detail_color_texture = False
            Material.msfs_show_detail_comp_texture = False
            Material.msfs_show_detail_normal_texture = False
            Material.msfs_show_blend_mask_texture = False
            Material.msfs_show_wetness_ao_texture = False
            Material.msfs_show_dirt_texture = False
            Material.msfs_show_height_map_texture = False

        elif mat.msfs_material_type == "msfs_fake_terrain": # Fake Terrain
            # Properties
            mat.msfs_show_colors = True
            mat.msfs_show_emissive_color = True

            mat.msfs_show_alpha_mode = False

            mat.msfs_show_render_options = True
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_pearl = True

            mat.msfs_show_gameplay_options = True

            mat.msfs_show_uv_options = True
            
            mat.msfs_show_material_options = True
            mat.msfs_show_material_detail_options = True
            mat.msfs_show_blend_threshold = True

            mat.msfs_show_decal_blend_factors = False

            mat.msfs_show_windshield_options = False

            mat.msfs_show_glass_options = False

            mat.msfs_show_parallax_options = False

            mat.msfs_show_sss_color = False

            mat.msfs_show_fresnel_options = False

            # Textures
            Material.msfs_show_base_color_texture = True
            Material.msfs_show_comp_texture = True
            Material.msfs_show_normal_texture = True
            Material.msfs_show_emissive_texture = True
            Material.msfs_show_detail_color_texture = True
            Material.msfs_show_detail_comp_texture = True
            Material.msfs_show_detail_normal_texture = True
            Material.msfs_show_blend_mask_texture = True
            Material.msfs_show_wetness_ao_texture = False
            Material.msfs_show_dirt_texture = False
            Material.msfs_show_height_map_texture = False

        elif mat.msfs_material_type == "msfs_fresnel": # Fresnel
            # Properties
            mat.msfs_show_colors = True
            mat.msfs_show_emissive_color = True

            mat.msfs_show_alpha_mode = True

            mat.msfs_show_render_options = True
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_pearl = True

            mat.msfs_show_gameplay_options = True
            
            mat.msfs_show_uv_options = True

            mat.msfs_show_material_options = True
            mat.msfs_show_material_detail_options = False
            mat.msfs_show_blend_threshold = False

            mat.msfs_show_decal_blend_factors = False

            mat.msfs_show_windshield_options = False

            mat.msfs_show_glass_options = False

            mat.msfs_show_parallax_options = False

            mat.msfs_show_sss_color = False

            mat.msfs_show_fresnel_options = True

            # Textures
            Material.msfs_show_base_color_texture = True
            Material.msfs_show_comp_texture = True
            Material.msfs_show_normal_texture = True
            Material.msfs_show_emissive_texture = True
            Material.msfs_show_detail_color_texture = False
            Material.msfs_show_detail_comp_texture = False
            Material.msfs_show_detail_normal_texture = False
            Material.msfs_show_blend_mask_texture = False
            Material.msfs_show_wetness_ao_texture = False
            Material.msfs_show_dirt_texture = False
            Material.msfs_show_height_map_texture = False

        elif mat.msfs_material_type == "msfs_env_occluder": # Environment Occluder
            # Properties
            mat.msfs_show_colors = True
            mat.msfs_show_emissive_color = False

            mat.msfs_show_alpha_mode = False

            mat.msfs_show_render_options = False
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_pearl = True

            mat.msfs_show_gameplay_options = False

            mat.msfs_show_uv_options = False

            mat.msfs_show_material_options = False
            mat.msfs_show_material_detail_options = False
            mat.msfs_show_blend_threshold = False

            mat.msfs_show_decal_blend_factors = False

            mat.msfs_show_windshield_options = False

            mat.msfs_show_glass_options = False

            mat.msfs_show_parallax_options = False

            mat.msfs_show_sss_color = False
            
            mat.msfs_show_fresnel_options = False

            # Textures
            Material.msfs_show_base_color_texture = False
            Material.msfs_show_comp_texture = False
            Material.msfs_show_normal_texture = False
            Material.msfs_show_emissive_texture = False
            Material.msfs_show_detail_color_texture = False
            Material.msfs_show_detail_comp_texture = False
            Material.msfs_show_detail_normal_texture = False
            Material.msfs_show_blend_mask_texture = False
            Material.msfs_show_wetness_ao_texture = False
            Material.msfs_show_dirt_texture = False
            Material.msfs_show_height_map_texture = False

class MSFSMaterialProperties(PropertyGroup):

    Material.msfs_material_type = EnumProperty(items = (("NONE", "Disabled", ""),
                                                                  ("msfs_standard", "MSFS Standard", ""),
                                                                  ("msfs_decal", "MSFS Decal", ""),
                                                                  ("msfs_windshield", "MSFS Windshield", ""),
                                                                  ("msfs_porthole", "MSFS Porthole", ""),
                                                                  ("msfs_glass", "MSFS Glass", ""),
                                                                  ("msfs_geo_decal", "MSFS Geo Decal (Frosted)", ""),
                                                                  ("msfs_clearcoat", "MSFS Clearcoat", ""),
                                                                  ("msfs_parallax", "MSFS Parallax", ""),
                                                                  ("msfs_anisotropic", "MSFS Anisotropic", ""),
                                                                  ("msfs_hair", "MSFS Hair", ""),
                                                                  ("msfs_sss", "MSFS SSS", ""),
                                                                  ("msfs_invisible", "MSFS Invisible", ""),
                                                                  ("msfs_fake_terrain", "MSFS Fake Terrain", ""),
                                                                  ("msfs_fresnel", "MSFS Fresnel", ""),
                                                                  ("msfs_env_occluder", "MSFS Environment Occluder", ""),), default = "NONE", update = updateMaterial)

    # Material Parameters
    # Standard
    Material.msfs_base_color = FloatVectorProperty(name = "Base Color", subtype = "COLOR", min = 0.0, max = 1.0, size = 4, default = [1.0, 1.0, 1.0, 1.0])
    Material.msfs_emissive_color = FloatVectorProperty(name = "Emissive Color", subtype = "COLOR", min = 0.0, max = 1.0, size = 4, default = [0.0, 0.0, 0.0, 1.0])

    Material.msfs_alpha_mode = EnumProperty(name = "Alpha Mode", items = (("OPAQUE", "Opaque", ""),
                                                                                    ("MASK", "Mask", ""),
                                                                                    ("BLEND", "Blend", ""),
                                                                                    ("DITHER", "Dither", ""),
                                                                                    ), default = "OPAQUE")
    Material.msfs_draw_order = IntProperty(name = "Draw Order", default = 0, min = -999, max = 999)
    Material.msfs_double_sided = BoolProperty(name = "Double Sided", default = False)
    Material.msfs_dont_cast_shadows = BoolProperty(name = "Don't Cast Shadows", default = False)
    Material.msfs_day_night_cycle = BoolProperty(name = "Day Night Cycle", default = False)

    Material.msfs_use_pearl_effect = BoolProperty(name = "Use Pearl Effect", default = False)
    Material.msfs_pearl_shift = FloatProperty(name = "Color Shift", default = 0.0, min = -999.0, max = 999.0)
    Material.msfs_pearl_range = FloatProperty(name = "Color Range", default = 0.0, min = -999.0, max = 999.0)
    Material.msfs_pearl_brightness = FloatProperty(name = "Color Brightness", default = 0.0, min = -1.0, max = 1.0)
    
    Material.msfs_collision_material = BoolProperty(name = "Collision Material", default = False)
    Material.msfs_road_material = BoolProperty(name = "Road Material", default = False)

    Material.msfs_uv_offset_u = FloatProperty(name = "UV Offset U", default = 0.0, min = -10.0, max = 10.0)
    Material.msfs_uv_offset_v = FloatProperty(name = "UV Offset V", default = 0.0, min = -10.0, max = 10.0)
    Material.msfs_uv_tiling_u = FloatProperty(name = "UV Tiling U", default = 1.0, min = -10.0, max = 10.0)
    Material.msfs_uv_tiling_v = FloatProperty(name = "UV Tiling V", default = 1.0, min = -10.0, max = 10.0)
    Material.msfs_uv_rotation = FloatProperty(name = "UV Rotation", default = 0.0, min = -360.0, max = 360.0)
    Material.msfs_uv_clamp_u = BoolProperty(name = "UV Clamp U", default = False)
    Material.msfs_uv_clamp_v = BoolProperty(name = "UV Clamp V", default = False)

    Material.msfs_roughness = FloatProperty(name = "Roughness", default = 1.0, min = 0.0, max = 1.0)
    Material.msfs_metallic = FloatProperty(name = "Metallic", default = 1.0, min = 0.0, max = 1.0)
    Material.msfs_normal_scale = FloatProperty(name = "Normal Scale", default = 1.0, min = 0.0, max = 1.0)
    Material.msfs_alpha_cutoff = FloatProperty(name = "Alpha Cutoff", default = 0.5, min = 0.0, max = 1.0) # This is only used with the mask alpha mode

    Material.msfs_detail_uv_scale = FloatProperty(name = "Detail UV Scale", default = 1.0, min = 0.01, max = 100.0) # In 3DS Max the default is 2.0, might want to look more into this later
    Material.msfs_detail_uv_offset_u = FloatProperty(name = "Detail UV Offset U", default = 0.0, min = -10.0, max = 10.0)
    Material.msfs_detail_uv_offset_v = FloatProperty(name = "Detail UV Offset V", default = 0.0, min = -10.0, max = 10.0)
    Material.msfs_detail_normal_scale = FloatProperty(name = "Detail Normal Scale", default = 1.0, min = 0.0, max = 1.0)

    Material.msfs_blend_threshold = FloatProperty(name = "Blend Threshold", default = 0.1, min = 0.001, max = 1.0)

    # Decal / Geo Decal (Frosted)
    Material.msfs_decal_color_blend_factor = FloatProperty(name = "Color", default = 1.0, min = 0.0, max = 1.0)
    Material.msfs_decal_metal_blend_factor = FloatProperty(name = "Metal", default = 1.0, min = 0.0, max = 1.0)
    Material.msfs_decal_normal_blend_factor = FloatProperty(name = "Normal", default = 1.0, min = 0.0, max = 1.0)
    Material.msfs_decal_roughness_blend_factor = FloatProperty(name = "Roughness", default = 1.0, min = 0.0, max = 1.0)
    Material.msfs_decal_occlusion_blend_factor = FloatProperty(name = "Occlusion", default = 1.0, min = 0.0, max = 1.0) # This is Blast Sys on Geo Decals
    Material.msfs_decal_emissive_blend_factor = FloatProperty(name = "Emissive", default = 1.0, min = 0.0, max = 1.0) # This is Melt Sys on Geo Decals

    # Windshield
    Material.msfs_rain_drop_scale = FloatProperty(name = "Rain Drop Scale", default = 1.0, min = 0.0, max = 100.0)
    Material.msfs_wiper_1_state = FloatProperty(name = "Wiper 1 State", default = 0.0, min = 0.0, max = 1.0)
    Material.msfs_wiper_2_state = FloatProperty(name = "Wiper 2 State", default = 0.0, min = 0.0, max = 1.0) # The 3DS Max plugin has up to 4 states, but the last 2 aren't visible

    # Glass
    Material.msfs_glass_reflection_factor = FloatProperty(name = "Glass Reflection Mask Factor", default = 1.0, min = 0.0, max = 1.0)
    Material.msfs_glass_deformation_factor = FloatProperty(name = "Glass Deformation Factor", default = 0.0, min = 0.0, max = 1.0)

    # Parallax
    Material.msfs_parallax_scale = FloatProperty(name = "Parallax Scale", default = 0.0, min = 0.0, max = 1.0)
    Material.msfs_parallax_room_size_x = FloatProperty(name = "Parallax Room Size X", default = 0.5, min = 0.01, max = 10.0)
    Material.msfs_parallax_room_size_y = FloatProperty(name = "Parallax Room Size Y", default = 0.5, min = 0.01, max = 10.0)
    Material.msfs_parallax_room_number = FloatProperty(name = "Parallax Room Number XY", default = 1.0, min = 1.0, max = 16.0)
    Material.msfs_parallax_corridor = BoolProperty(name = "Corridor", default = False)

    # Hair / SSS
    Material.msfs_sss_color = FloatVectorProperty(name = "SSS Color", subtype = "COLOR", min = 0.0, max = 1.0, size = 4, default = [1.0, 1.0, 1.0, 1.0]) # This is disabled in the 3DS Max plugin

    # Fresnel
    Material.msfs_fresnel_factor = FloatProperty(name = "Fresnel Factor", default = 1.0, min = 0.001, max = 100.0)
    Material.msfs_fresnel_opacity_bias = FloatProperty(name = "Fresnel Opacity Bias", default = 0.0, min = -1.0, max = 1.0)

    # Textures
    Material.msfs_base_color_texture = PointerProperty(type = Image, name = "Base Color")
    Material.msfs_comp_texture = PointerProperty(type = Image, name = "Composite (Occlusion (R), Roughness (G), Metalness (B))")
    Material.msfs_normal_texture = PointerProperty(type = Image, name = "Normal")
    Material.msfs_emissive_texture = PointerProperty(type = Image, name = "Emissive")
    Material.msfs_detail_color_texture = PointerProperty(type = Image, name = "Detail Color")
    Material.msfs_detail_comp_texture = PointerProperty(type = Image, name = "Detail Composite (Occlusion (R), Roughness (G), Metalness (B))")
    Material.msfs_detail_normal_texture = PointerProperty(type = Image, name = "Detail Normal")
    Material.msfs_blend_mask_texture = PointerProperty(type = Image, name = "Blend Mask")
    Material.msfs_wetness_ao_texture = PointerProperty(type = Image, name = "Wetness AO")
    Material.msfs_dirt_texture = PointerProperty(type = Image, name = "Dirt")
    Material.msfs_height_map_texture = PointerProperty(type = Image, name = "Height Map")

    # Option visibility
    # Standard
    Material.msfs_show_colors = BoolProperty(name = "show_colors", default = False)
    Material.msfs_show_emissive_color = BoolProperty(name = "show_emissive_color", default = False)

    Material.msfs_show_alpha_mode = BoolProperty(name = "show_alpha_mode", default = False)

    Material.msfs_show_render_options = BoolProperty(name = "show_render_options", default = False)
    Material.msfs_show_day_night_cycle = BoolProperty(name = "show_day_night_cycle", default = False)

    Material.msfs_show_pearl = BoolProperty(name = "show_pearl", default = False)

    Material.msfs_show_gameplay_options = BoolProperty(name = "show_gameplay_options", default = False)

    Material.msfs_show_uv_options = BoolProperty(name = "show_uv_options", default = False)

    Material.msfs_show_material_options = BoolProperty(name = "show_material_options", default = False)
    Material.msfs_show_material_detail_options = BoolProperty(name = "show_material_detail_options", default = False)
    Material.msfs_show_blend_threshold = BoolProperty(name = "show_blend_threshold", default = False)

    # Decal / Geo Decal (Frosted)
    Material.msfs_show_decal_blend_factors = BoolProperty(name = "show_decal_blend_factors", default = False)

    # Windshield
    Material.msfs_show_windshield_options = BoolProperty(name = "show_windshield_options", default = False)

    # Glass
    Material.msfs_show_glass_options = BoolProperty(name = "show_glass_options", default = False)

    # Parallax
    Material.msfs_show_parallax_options = BoolProperty(name = "show_parallax_options", default = False)

    # Hair / SSS
    Material.msfs_show_sss_color = BoolProperty(name = "show_sss_property", default = False)

    # Fresnel
    Material.msfs_show_fresnel_options = BoolProperty(name = "show_fresnel_options", default = False)

    # Textures
    Material.msfs_show_base_color_texture = BoolProperty(name = "show_base_color_texture", default = False)
    Material.msfs_show_comp_texture = BoolProperty(name = "show_comp_texture", default = False)
    Material.msfs_show_normal_texture = BoolProperty(name = "show_normal_texture", default = False)
    Material.msfs_show_emissive_texture = BoolProperty(name = "show_emissive_texture", default = False)
    Material.msfs_show_detail_color_texture = BoolProperty(name = "show_detail_color_texture", default = False)
    Material.msfs_show_detail_comp_texture = BoolProperty(name = "show_detail_comp_texture", default = False)
    Material.msfs_show_detail_normal_texture = BoolProperty(name = "show_detail_normal_texture", default = False)
    Material.msfs_show_blend_mask_texture = BoolProperty(name = "show_blend_mask_texture", default = False)
    Material.msfs_show_wetness_ao_texture = BoolProperty(name = "show_wetness_ao_texture", default = False)
    Material.msfs_show_dirt_texture = BoolProperty(name = "show_dirt_texture", default = False)
    Material.msfs_show_height_map_texture = BoolProperty(name = "show_height_map_texture", default = False)

classes = (
    MSFSMaterialProperties,
)

register, unregister = bpy.utils.register_classes_factory(classes)
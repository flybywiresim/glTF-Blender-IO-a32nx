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
from . import gltf2_blender_flight_sim_material_functions as functions

def update_material(self, context):
    # Reset material properties
    self.msfs_base_color_factor = msfs_material_default_values.msfs_base_color_factor
    self.msfs_emissive_factor = msfs_material_default_values.msfs_emissive_factor

    self.msfs_alpha_mode = msfs_material_default_values.msfs_alpha_mode
    self.msfs_draw_order = msfs_material_default_values.msfs_draw_order
    self.msfs_double_sided = msfs_material_default_values.msfs_double_sided
    self.msfs_dont_cast_shadows = msfs_material_default_values.msfs_dont_cast_shadows
    self.msfs_day_night_cycle = msfs_material_default_values.msfs_day_night_cycle

    self.msfs_use_pearl_effect = msfs_material_default_values.msfs_use_pearl_effect
    self.msfs_pearl_shift = msfs_material_default_values.msfs_pearl_shift
    self.msfs_pearl_range = msfs_material_default_values.msfs_pearl_range
    self.msfs_pearl_brightness = msfs_material_default_values.msfs_pearl_brightness
    
    self.msfs_collision_material = msfs_material_default_values.msfs_collision_material
    self.msfs_road_material = msfs_material_default_values.msfs_road_material

    self.msfs_uv_offset_u = msfs_material_default_values.msfs_uv_offset_u
    self.msfs_uv_offset_v = msfs_material_default_values.msfs_uv_offset_v
    self.msfs_uv_tiling_u = msfs_material_default_values.msfs_uv_tiling_u
    self.msfs_uv_tiling_v = msfs_material_default_values.msfs_uv_tiling_v
    self.msfs_uv_rotation = msfs_material_default_values.msfs_uv_rotation
    self.msfs_uv_clamp_u = msfs_material_default_values.msfs_uv_clamp_u
    self.msfs_uv_clamp_v = msfs_material_default_values.msfs_uv_clamp_v

    self.msfs_roughness_factor = msfs_material_default_values.msfs_roughness_factor
    self.msfs_metallic_factor = msfs_material_default_values.msfs_metallic_factor
    self.msfs_normal_scale = msfs_material_default_values.msfs_normal_scale
    self.msfs_alpha_cutoff = msfs_material_default_values.msfs_alpha_cutoff

    self.msfs_detail_uv_scale = msfs_material_default_values.msfs_detail_uv_scale
    self.msfs_detail_uv_offset_u = msfs_material_default_values.msfs_detail_uv_offset_u
    self.msfs_detail_uv_offset_v = msfs_material_default_values.msfs_detail_uv_offset_v
    self.msfs_detail_normal_scale = msfs_material_default_values.msfs_detail_normal_scale

    self.msfs_blend_threshold = msfs_material_default_values.msfs_blend_threshold

    # Decal / Geo Decal (Frosted)
    self.msfs_decal_color_blend_factor = msfs_material_default_values.msfs_decal_color_blend_factor
    self.msfs_decal_metal_blend_factor = msfs_material_default_values.msfs_decal_metal_blend_factor
    self.msfs_decal_normal_blend_factor = msfs_material_default_values.msfs_decal_normal_blend_factor
    self.msfs_decal_roughness_blend_factor = msfs_material_default_values.msfs_decal_roughness_blend_factor
    self.msfs_decal_occlusion_blend_factor = msfs_material_default_values.msfs_decal_occlusion_blend_factor
    self.msfs_decal_emissive_blend_factor = msfs_material_default_values.msfs_decal_emissive_blend_factor

    # Windshield
    self.msfs_rain_drop_scale = msfs_material_default_values.msfs_rain_drop_scale
    self.msfs_wiper_1_state = msfs_material_default_values.msfs_wiper_1_state
    self.msfs_wiper_2_state = msfs_material_default_values.msfs_wiper_2_state

    # Glass
    self.msfs_glass_reflection_factor = msfs_material_default_values.msfs_glass_reflection_factor
    self.msfs_glass_deformation_factor = msfs_material_default_values.msfs_glass_deformation_factor

    # Parallax
    self.msfs_parallax_scale = msfs_material_default_values.msfs_parallax_scale
    self.msfs_parallax_room_size_x = msfs_material_default_values.msfs_parallax_room_size_x
    self.msfs_parallax_room_size_y = msfs_material_default_values.msfs_parallax_room_size_y
    self.msfs_parallax_room_number = msfs_material_default_values.msfs_parallax_room_number
    self.msfs_parallax_corridor = msfs_material_default_values.msfs_parallax_corridor

    # Hair / SSS
    self.msfs_sss_color = msfs_material_default_values.msfs_sss_color

    # Fresnel
    self.msfs_fresnel_factor = msfs_material_default_values.msfs_fresnel_factor
    self.msfs_fresnel_opacity_bias = msfs_material_default_values.msfs_fresnel_opacity_bias

    # Textures
    self.msfs_base_color_texture = None
    self.msfs_comp_texture = None
    self.msfs_normal_texture = None
    self.msfs_emissive_texture = None
    self.msfs_detail_color_texture = None
    self.msfs_detail_comp_texture = None
    self.msfs_detail_normal_texture = None
    self.msfs_blend_mask_texture = None
    self.msfs_wetness_ao_texture = None
    self.msfs_dirt_texture = None
    self.msfs_height_map_texture = None

    # Next, we decide which properties should be displayed to the user based off the material type

    if self.msfs_material_type == "msfs_standard": # Standard
        # Properties
        self.msfs_show_colors = True
        self.msfs_show_emissive_color = True

        self.msfs_show_alpha_mode = True

        self.msfs_show_render_options = True
        self.msfs_show_day_night_cycle = True

        self.msfs_show_pearl = True

        self.msfs_show_gameplay_options = True

        self.msfs_show_uv_options = True

        self.msfs_show_material_options = True
        self.msfs_show_material_detail_options = True
        self.msfs_show_blend_threshold = True

        self.msfs_show_decal_blend_factors = False

        self.msfs_show_windshield_options = False

        self.msfs_show_glass_options = False

        self.msfs_show_parallax_options = False

        self.msfs_show_sss_color = False

        self.msfs_show_fresnel_options = False

        # Textures
        self.msfs_show_base_color_texture = True
        self.msfs_show_comp_texture = True
        self.msfs_show_normal_texture = True
        self.msfs_show_emissive_texture = True
        self.msfs_show_detail_color_texture = True
        self.msfs_show_detail_comp_texture = True
        self.msfs_show_detail_normal_texture = True
        self.msfs_show_blend_mask_texture = True
        self.msfs_show_wetness_ao_texture = False
        self.msfs_show_dirt_texture = False
        self.msfs_show_height_map_texture = False
        
    elif self.msfs_material_type == "msfs_decal": # Decal
        # Properties
        self.msfs_show_colors = True
        self.msfs_show_emissive_color = True

        self.msfs_show_alpha_mode = False

        self.msfs_show_render_options = True
        self.msfs_show_day_night_cycle = False

        self.msfs_show_pearl = True

        self.msfs_show_gameplay_options = True

        self.msfs_show_uv_options = True

        self.msfs_show_material_options = True
        self.msfs_show_material_detail_options = True
        self.msfs_show_blend_threshold = True

        self.msfs_show_decal_blend_factors = True

        self.msfs_show_windshield_options = False

        self.msfs_show_glass_options = False

        self.msfs_show_parallax_options = False

        self.msfs_show_sss_color = False

        self.msfs_show_fresnel_options = False

        # Textures
        self.msfs_show_base_color_texture = True
        self.msfs_show_comp_texture = True
        self.msfs_show_normal_texture = True
        self.msfs_show_emissive_texture = True
        self.msfs_show_detail_color_texture = True
        self.msfs_show_detail_comp_texture = True
        self.msfs_show_detail_normal_texture = True
        self.msfs_show_blend_mask_texture = True
        self.msfs_show_wetness_ao_texture = False
        self.msfs_show_dirt_texture = False
        self.msfs_show_height_map_texture = False

    elif self.msfs_material_type == "msfs_windshield": # Windshield
        # Properties
        self.msfs_show_colors = True
        self.msfs_show_emissive_color = True

        self.msfs_show_alpha_mode = False

        self.msfs_show_render_options = True
        self.msfs_show_day_night_cycle = False

        self.msfs_show_pearl = True

        self.msfs_show_gameplay_options = True

        self.msfs_show_uv_options = True

        self.msfs_show_material_options = True
        self.msfs_show_material_detail_options = True
        self.msfs_show_blend_threshold = True

        self.msfs_show_decal_blend_factors = False

        self.msfs_show_windshield_options = True

        self.msfs_show_glass_options = False

        self.msfs_show_parallax_options = False

        self.msfs_show_sss_color = False

        self.msfs_show_fresnel_options = False

        # Textures
        self.msfs_show_base_color_texture = True
        self.msfs_show_comp_texture = True
        self.msfs_show_normal_texture = True
        self.msfs_show_emissive_texture = True
        self.msfs_show_detail_color_texture = True
        self.msfs_show_detail_comp_texture = True
        self.msfs_show_detail_normal_texture = True
        self.msfs_show_blend_mask_texture = True
        self.msfs_show_wetness_ao_texture = True
        self.msfs_show_dirt_texture = False
        self.msfs_show_height_map_texture = False

    elif self.msfs_material_type == "msfs_porthole": # Porthole
        # Properties
        self.msfs_show_colors = True
        self.msfs_show_emissive_color = True

        self.msfs_show_alpha_mode = False

        self.msfs_show_render_options = True
        self.msfs_show_day_night_cycle = False

        self.msfs_show_pearl = True

        self.msfs_show_gameplay_options = True

        self.msfs_show_uv_options = True

        self.msfs_show_material_options = True
        self.msfs_show_material_detail_options = True
        self.msfs_show_blend_threshold = True

        self.msfs_show_decal_blend_factors = False

        self.msfs_show_windshield_options = False

        self.msfs_show_glass_options = False

        self.msfs_show_parallax_options = False

        self.msfs_show_sss_color = False

        self.msfs_show_fresnel_options = False

        # Textures
        self.msfs_show_base_color_texture = True
        self.msfs_show_comp_texture = True
        self.msfs_show_normal_texture = True
        self.msfs_show_emissive_texture = True
        self.msfs_show_detail_color_texture = True
        self.msfs_show_detail_comp_texture = True
        self.msfs_show_detail_normal_texture = True
        self.msfs_show_blend_mask_texture = True
        self.msfs_show_wetness_ao_texture = False
        self.msfs_show_dirt_texture = False
        self.msfs_show_height_map_texture = False

    elif self.msfs_material_type == "msfs_glass": # Glass
        # Properties
        self.msfs_show_colors = True
        self.msfs_show_emissive_color = True

        self.msfs_show_alpha_mode = False

        self.msfs_show_render_options = True
        self.msfs_show_day_night_cycle = False
        
        self.msfs_show_pearl = True

        self.msfs_show_gameplay_options = True

        self.msfs_show_uv_options = True

        self.msfs_show_material_options = True
        self.msfs_show_material_detail_options = True
        self.msfs_show_blend_threshold = True

        self.msfs_show_decal_blend_factors = False

        self.msfs_show_windshield_options = False

        self.msfs_show_glass_options = True

        self.msfs_show_parallax_options = False

        self.msfs_show_sss_color = False

        self.msfs_show_fresnel_options = False

        # Textures
        self.msfs_show_base_color_texture = True
        self.msfs_show_comp_texture = True
        self.msfs_show_normal_texture = True
        self.msfs_show_emissive_texture = True
        self.msfs_show_detail_color_texture = True
        self.msfs_show_detail_comp_texture = True
        self.msfs_show_detail_normal_texture = True
        self.msfs_show_blend_mask_texture = True
        self.msfs_show_wetness_ao_texture = False
        self.msfs_show_dirt_texture = False
        self.msfs_show_height_map_texture = False

    elif self.msfs_material_type == "msfs_geo_decal": # Geo Decal (Frosted)
        # Properties
        self.msfs_show_colors = True
        self.msfs_show_emissive_color = True

        self.msfs_show_alpha_mode = False

        self.msfs_show_render_options = True
        self.msfs_show_day_night_cycle = False
        
        self.msfs_show_pearl = True

        self.msfs_show_gameplay_options = True

        self.msfs_show_uv_options = True

        self.msfs_show_material_options = True
        self.msfs_show_material_detail_options = True
        self.msfs_show_blend_threshold = True

        self.msfs_show_decal_blend_factors = True

        self.msfs_show_windshield_options = False

        self.msfs_show_glass_options = False

        self.msfs_show_parallax_options = False

        self.msfs_show_sss_color = False

        self.msfs_show_fresnel_options = False

        # Textures
        self.msfs_show_base_color_texture = True
        self.msfs_show_comp_texture = True
        self.msfs_show_normal_texture = True
        self.msfs_show_emissive_texture = True
        self.msfs_show_detail_color_texture = True
        self.msfs_show_detail_comp_texture = True
        self.msfs_show_detail_normal_texture = True
        self.msfs_show_blend_mask_texture = False
        self.msfs_show_wetness_ao_texture = False
        self.msfs_show_dirt_texture = False
        self.msfs_show_height_map_texture = False

    elif self.msfs_material_type == "msfs_clearcoat": # Clearcoat
        # Properties
        self.msfs_show_colors = True
        self.msfs_show_emissive_color = True

        self.msfs_show_alpha_mode = True

        self.msfs_show_render_options = True
        self.msfs_show_day_night_cycle = False

        self.msfs_show_pearl = True

        self.msfs_show_gameplay_options = True

        self.msfs_show_uv_options = True

        self.msfs_show_material_options = True
        self.msfs_show_material_detail_options = True
        self.msfs_show_blend_threshold = True

        self.msfs_show_decal_blend_factors = False

        self.msfs_show_windshield_options = False

        self.msfs_show_glass_options = False

        self.msfs_show_parallax_options = False

        self.msfs_show_sss_color = False

        self.msfs_show_fresnel_options = False

        # Textures
        self.msfs_show_base_color_texture = True
        self.msfs_show_comp_texture = True
        self.msfs_show_normal_texture = True
        self.msfs_show_emissive_texture = True
        self.msfs_show_detail_color_texture = True
        self.msfs_show_detail_comp_texture = True
        self.msfs_show_detail_normal_texture = True
        self.msfs_show_blend_mask_texture = True
        self.msfs_show_wetness_ao_texture = False
        self.msfs_show_dirt_texture = True
        self.msfs_show_height_map_texture = False

    elif self.msfs_material_type == "msfs_parallax": # Parallax
        # Properties
        self.msfs_show_colors = True
        self.msfs_show_emissive_color = True

        self.msfs_show_alpha_mode = True

        self.msfs_show_render_options = True
        self.msfs_show_day_night_cycle = False

        self.msfs_show_pearl = True

        self.msfs_show_gameplay_options = True

        self.msfs_show_uv_options = True

        self.msfs_show_material_options = True
        self.msfs_show_material_detail_options = False
        self.msfs_show_blend_threshold = True

        self.msfs_show_decal_blend_factors = False

        self.msfs_show_windshield_options = False

        self.msfs_show_glass_options = False

        self.msfs_show_parallax_options = True

        self.msfs_show_sss_color = False

        self.msfs_show_fresnel_options = False

        # Textures
        self.msfs_show_base_color_texture = True
        self.msfs_show_comp_texture = True
        self.msfs_show_normal_texture = True
        self.msfs_show_emissive_texture = True
        self.msfs_show_detail_color_texture = True
        self.msfs_show_detail_comp_texture = False
        self.msfs_show_detail_normal_texture = False
        self.msfs_show_blend_mask_texture = False
        self.msfs_show_wetness_ao_texture = False
        self.msfs_show_dirt_texture = False
        self.msfs_show_height_map_texture = False

    elif self.msfs_material_type == "msfs_anisotropic": # Anisotropic
        # Properties
        self.msfs_show_colors = True
        self.msfs_show_emissive_color = True

        self.msfs_show_alpha_mode = True

        self.msfs_show_render_options = True
        self.msfs_show_day_night_cycle = False

        self.msfs_show_pearl = True

        self.msfs_show_gameplay_options = True

        self.msfs_show_uv_options = True

        self.msfs_show_material_options = True
        self.msfs_show_material_detail_options = True
        self.msfs_show_blend_threshold = True

        self.msfs_show_decal_blend_factors = False

        self.msfs_show_windshield_options = False

        self.msfs_show_glass_options = False

        self.msfs_show_parallax_options = False

        self.msfs_show_sss_color = False

        self.msfs_show_fresnel_options = False

        # Textures
        self.msfs_show_base_color_texture = True
        self.msfs_show_comp_texture = True
        self.msfs_show_normal_texture = True
        self.msfs_show_emissive_texture = True
        self.msfs_show_detail_color_texture = True
        self.msfs_show_detail_comp_texture = True
        self.msfs_show_detail_normal_texture = True
        self.msfs_show_blend_mask_texture = True
        self.msfs_show_wetness_ao_texture = True
        self.msfs_show_dirt_texture = False
        self.msfs_show_height_map_texture = False

    elif self.msfs_material_type == "msfs_hair": # Hair
        # Properties
        self.msfs_show_colors = True
        self.msfs_show_emissive_color = True

        self.msfs_show_alpha_mode = True

        self.msfs_show_render_options = True
        self.msfs_show_day_night_cycle = False

        self.msfs_show_pearl = True

        self.msfs_show_gameplay_options = True

        self.msfs_show_uv_options = True

        self.msfs_show_material_options = True
        self.msfs_show_material_detail_options = True
        self.msfs_show_blend_threshold = True

        self.msfs_show_decal_blend_factors = False

        self.msfs_show_windshield_options = False

        self.msfs_show_glass_options = False

        self.msfs_show_parallax_options = False

        self.msfs_show_sss_color = False # Doesn't seem to be enabled in the 3DS Max plugin

        self.msfs_show_fresnel_options = False

        # Textures
        self.msfs_show_base_color_texture = True
        self.msfs_show_comp_texture = True
        self.msfs_show_normal_texture = True
        self.msfs_show_emissive_texture = True
        self.msfs_show_detail_color_texture = False
        self.msfs_show_detail_comp_texture = False
        self.msfs_show_detail_normal_texture = False
        self.msfs_show_blend_mask_texture = False
        self.msfs_show_wetness_ao_texture = True
        self.msfs_show_dirt_texture = False
        self.msfs_show_height_map_texture = False

    elif self.msfs_material_type == "msfs_sss": # SSS
        # Properties
        self.msfs_show_colors = True
        self.msfs_show_emissive_color = True

        self.msfs_show_alpha_mode = True

        self.msfs_show_render_options = True
        self.msfs_show_day_night_cycle = False

        self.msfs_show_pearl = True

        self.msfs_show_gameplay_options = True

        self.msfs_show_uv_options = True

        self.msfs_show_material_options = True
        self.msfs_show_material_detail_options = False
        self.msfs_show_blend_threshold = False

        self.msfs_show_decal_blend_factors = False

        self.msfs_show_windshield_options = False

        self.msfs_show_glass_options = False

        self.msfs_show_parallax_options = False

        self.msfs_show_sss_color = False # Doesn't seem to be enabled in the 3DS Max plugin
        
        self.msfs_show_fresnel_options = False

        # Textures
        self.msfs_show_base_color_texture = True
        self.msfs_show_comp_texture = True
        self.msfs_show_normal_texture = True
        self.msfs_show_emissive_texture = True
        self.msfs_show_detail_color_texture = False
        self.msfs_show_detail_comp_texture = False
        self.msfs_show_detail_normal_texture = False
        self.msfs_show_blend_mask_texture = False
        self.msfs_show_wetness_ao_texture = False
        self.msfs_show_dirt_texture = False
        self.msfs_show_height_map_texture = False

    elif self.msfs_material_type == "msfs_invisible": # Invisible
        # Properties
        self.msfs_show_colors = True
        self.msfs_show_emissive_color = False

        self.msfs_show_alpha_mode = False

        self.msfs_show_render_options = False
        self.msfs_show_day_night_cycle = False

        self.msfs_show_pearl = True

        self.msfs_show_gameplay_options = True

        self.msfs_show_uv_options = True

        self.msfs_show_material_options = False
        self.msfs_show_material_detail_options = False
        self.msfs_show_blend_threshold = False

        self.msfs_show_decal_blend_factors = False

        self.msfs_show_windshield_options = False

        self.msfs_show_glass_options = False

        self.msfs_show_parallax_options = False

        self.msfs_show_sss_color = False

        self.msfs_show_fresnel_options = False

        # Textures
        self.msfs_show_base_color_texture = False
        self.msfs_show_comp_texture = False
        self.msfs_show_normal_texture = False
        self.msfs_show_emissive_texture = False
        self.msfs_show_detail_color_texture = False
        self.msfs_show_detail_comp_texture = False
        self.msfs_show_detail_normal_texture = False
        self.msfs_show_blend_mask_texture = False
        self.msfs_show_wetness_ao_texture = False
        self.msfs_show_dirt_texture = False
        self.msfs_show_height_map_texture = False

    elif self.msfs_material_type == "msfs_fake_terrain": # Fake Terrain
        # Properties
        self.msfs_show_colors = True
        self.msfs_show_emissive_color = True

        self.msfs_show_alpha_mode = False

        self.msfs_show_render_options = True
        self.msfs_show_day_night_cycle = False

        self.msfs_show_pearl = True

        self.msfs_show_gameplay_options = True

        self.msfs_show_uv_options = True
        
        self.msfs_show_material_options = True
        self.msfs_show_material_detail_options = True
        self.msfs_show_blend_threshold = True

        self.msfs_show_decal_blend_factors = False

        self.msfs_show_windshield_options = False

        self.msfs_show_glass_options = False

        self.msfs_show_parallax_options = False

        self.msfs_show_sss_color = False

        self.msfs_show_fresnel_options = False

        # Textures
        self.msfs_show_base_color_texture = True
        self.msfs_show_comp_texture = True
        self.msfs_show_normal_texture = True
        self.msfs_show_emissive_texture = True
        self.msfs_show_detail_color_texture = True
        self.msfs_show_detail_comp_texture = True
        self.msfs_show_detail_normal_texture = True
        self.msfs_show_blend_mask_texture = True
        self.msfs_show_wetness_ao_texture = False
        self.msfs_show_dirt_texture = False
        self.msfs_show_height_map_texture = False

    elif self.msfs_material_type == "msfs_fresnel": # Fresnel
        # Properties
        self.msfs_show_colors = True
        self.msfs_show_emissive_color = True

        self.msfs_show_alpha_mode = True

        self.msfs_show_render_options = True
        self.msfs_show_day_night_cycle = False

        self.msfs_show_pearl = True

        self.msfs_show_gameplay_options = True
        
        self.msfs_show_uv_options = True

        self.msfs_show_material_options = True
        self.msfs_show_material_detail_options = False
        self.msfs_show_blend_threshold = False

        self.msfs_show_decal_blend_factors = False

        self.msfs_show_windshield_options = False

        self.msfs_show_glass_options = False

        self.msfs_show_parallax_options = False

        self.msfs_show_sss_color = False

        self.msfs_show_fresnel_options = True

        # Textures
        self.msfs_show_base_color_texture = True
        self.msfs_show_comp_texture = True
        self.msfs_show_normal_texture = True
        self.msfs_show_emissive_texture = True
        self.msfs_show_detail_color_texture = False
        self.msfs_show_detail_comp_texture = False
        self.msfs_show_detail_normal_texture = False
        self.msfs_show_blend_mask_texture = False
        self.msfs_show_wetness_ao_texture = False
        self.msfs_show_dirt_texture = False
        self.msfs_show_height_map_texture = False

    elif self.msfs_material_type == "msfs_env_occluder": # Environment Occluder
        # Properties
        self.msfs_show_colors = True
        self.msfs_show_emissive_color = False

        self.msfs_show_alpha_mode = False

        self.msfs_show_render_options = False
        self.msfs_show_day_night_cycle = False

        self.msfs_show_pearl = True

        self.msfs_show_gameplay_options = False

        self.msfs_show_uv_options = False

        self.msfs_show_material_options = False
        self.msfs_show_material_detail_options = False
        self.msfs_show_blend_threshold = False

        self.msfs_show_decal_blend_factors = False

        self.msfs_show_windshield_options = False

        self.msfs_show_glass_options = False

        self.msfs_show_parallax_options = False

        self.msfs_show_sss_color = False
        
        self.msfs_show_fresnel_options = False

        # Textures
        self.msfs_show_base_color_texture = False
        self.msfs_show_comp_texture = False
        self.msfs_show_normal_texture = False
        self.msfs_show_emissive_texture = False
        self.msfs_show_detail_color_texture = False
        self.msfs_show_detail_comp_texture = False
        self.msfs_show_detail_normal_texture = False
        self.msfs_show_blend_mask_texture = False
        self.msfs_show_wetness_ao_texture = False
        self.msfs_show_dirt_texture = False
        self.msfs_show_height_map_texture = False


    # Finally, we create the material nodes
    functions.create_material(self, context)

class msfs_material_default_values:
    # This class stores the default values for MSFS material properties for ease of access
    # Probably isn't the best way of doing this, but it works and is convenient 

    msfs_material_type = "NONE"

    msfs_base_color_factor = [1.0, 1.0, 1.0, 1.0]
    msfs_emissive_factor = [0.0, 0.0, 0.0]

    msfs_alpha_mode = "OPAQUE"
    msfs_draw_order = 0
    msfs_double_sided = False
    msfs_dont_cast_shadows = False
    msfs_day_night_cycle = False

    msfs_use_pearl_effect = False
    msfs_pearl_shift = 0.0
    msfs_pearl_range = 0.0
    msfs_pearl_brightness = 0.0
    
    msfs_collision_material = False
    msfs_road_material = False

    msfs_uv_offset_u = 0.0
    msfs_uv_offset_v = 0.0
    msfs_uv_tiling_u = 1.0
    msfs_uv_tiling_v = 1.0
    msfs_uv_rotation = 0.0
    msfs_uv_clamp_u = False
    msfs_uv_clamp_v = False

    msfs_roughness_factor = 1.0
    msfs_metallic_factor = 1.0
    msfs_normal_scale = 1.0
    msfs_alpha_cutoff = 0.5

    msfs_detail_uv_scale = 1.0 # In 3DS Max the default is 2.0, might want to look more into this later
    msfs_detail_uv_offset_u = 0.0
    msfs_detail_uv_offset_v = 0.0
    msfs_detail_normal_scale = 1.0

    msfs_blend_threshold = 0.1

    # Decal / Geo Decal (Frosted)
    msfs_decal_color_blend_factor = 1.0
    msfs_decal_metal_blend_factor = 1.0
    msfs_decal_normal_blend_factor = 1.0
    msfs_decal_roughness_blend_factor = 1.0
    msfs_decal_occlusion_blend_factor = 1.0
    msfs_decal_emissive_blend_factor = 1.0

    # Windshield
    msfs_rain_drop_scale = 1.0
    msfs_wiper_1_state = 0.0
    msfs_wiper_2_state = 0.0

    # Glass
    msfs_glass_reflection_factor = 1.0
    msfs_glass_deformation_factor = 0.0

    # Parallax
    msfs_parallax_scale = 0.0
    msfs_parallax_room_size_x = 0.5
    msfs_parallax_room_size_y = 0.5
    msfs_parallax_room_number = 1.0
    msfs_parallax_corridor = False

    # Hair / SSS
    msfs_sss_color = [1.0, 1.0, 1.0, 1.0]

    # Fresnel
    msfs_fresnel_factor = 1.0
    msfs_fresnel_opacity_bias = 0.0


class msfs_material_properties(PropertyGroup):
    # Declare all custom material properties here

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
                                                                  ("msfs_env_occluder", "MSFS Environment Occluder", ""),), default = msfs_material_default_values.msfs_material_type, update = update_material)

    # Material Parameters
    # Standard
    Material.msfs_base_color_factor = FloatVectorProperty(name = "Base Color", subtype = "COLOR", min = 0.0, max = 1.0, size = 4, default = msfs_material_default_values.msfs_base_color_factor, update = functions.update_base_color_factor)
    Material.msfs_emissive_factor = FloatVectorProperty(name = "Emissive Color", subtype = "COLOR", min = 0.0, max = 1.0, size = 3, default = msfs_material_default_values.msfs_emissive_factor, update = functions.update_emissive_factor)

    Material.msfs_alpha_mode = EnumProperty(name = "Alpha Mode", items = (("OPAQUE", "Opaque", ""),
                                                                                    ("MASK", "Mask", ""),
                                                                                    ("BLEND", "Blend", ""),
                                                                                    ("DITHER", "Dither", ""),
                                                                                    ), default = msfs_material_default_values.msfs_alpha_mode)
    Material.msfs_draw_order = IntProperty(name = "Draw Order", default = msfs_material_default_values.msfs_draw_order, min = -999, max = 999)
    Material.msfs_double_sided = BoolProperty(name = "Double Sided", default = msfs_material_default_values.msfs_double_sided)
    Material.msfs_dont_cast_shadows = BoolProperty(name = "Don't Cast Shadows", default = msfs_material_default_values.msfs_dont_cast_shadows)
    Material.msfs_day_night_cycle = BoolProperty(name = "Day Night Cycle", default = msfs_material_default_values.msfs_day_night_cycle)

    Material.msfs_use_pearl_effect = BoolProperty(name = "Use Pearl Effect", default = msfs_material_default_values.msfs_use_pearl_effect)
    Material.msfs_pearl_shift = FloatProperty(name = "Color Shift", default = msfs_material_default_values.msfs_pearl_shift, min = -999.0, max = 999.0)
    Material.msfs_pearl_range = FloatProperty(name = "Color Range", default = msfs_material_default_values.msfs_pearl_range, min = -999.0, max = 999.0)
    Material.msfs_pearl_brightness = FloatProperty(name = "Color Brightness", default = msfs_material_default_values.msfs_pearl_brightness, min = -1.0, max = 1.0)
    
    Material.msfs_collision_material = BoolProperty(name = "Collision Material", default = msfs_material_default_values.msfs_collision_material)
    Material.msfs_road_material = BoolProperty(name = "Road Material", default = msfs_material_default_values.msfs_road_material)

    Material.msfs_uv_offset_u = FloatProperty(name = "UV Offset U", default = msfs_material_default_values.msfs_uv_offset_u, min = -10.0, max = 10.0)
    Material.msfs_uv_offset_v = FloatProperty(name = "UV Offset V", default = msfs_material_default_values.msfs_uv_clamp_v, min = -10.0, max = 10.0)
    Material.msfs_uv_tiling_u = FloatProperty(name = "UV Tiling U", default = msfs_material_default_values.msfs_uv_tiling_u, min = -10.0, max = 10.0)
    Material.msfs_uv_tiling_v = FloatProperty(name = "UV Tiling V", default = msfs_material_default_values.msfs_uv_tiling_v, min = -10.0, max = 10.0)
    Material.msfs_uv_rotation = FloatProperty(name = "UV Rotation", default = msfs_material_default_values.msfs_uv_rotation, min = -360.0, max = 360.0)
    Material.msfs_uv_clamp_u = BoolProperty(name = "UV Clamp U", default = msfs_material_default_values.msfs_uv_clamp_u)
    Material.msfs_uv_clamp_v = BoolProperty(name = "UV Clamp V", default = msfs_material_default_values.msfs_uv_clamp_v)

    Material.msfs_roughness_factor = FloatProperty(name = "Roughness Factor", default = msfs_material_default_values.msfs_roughness_factor, min = 0.0, max = 1.0)
    Material.msfs_metallic_factor = FloatProperty(name = "Metallic Factor", default = msfs_material_default_values.msfs_metallic_factor, min = 0.0, max = 1.0)
    Material.msfs_normal_scale = FloatProperty(name = "Normal Scale", default = msfs_material_default_values.msfs_normal_scale, min = 0.0, max = 1.0)
    Material.msfs_alpha_cutoff = FloatProperty(name = "Alpha Cutoff", default = msfs_material_default_values.msfs_alpha_cutoff, min = 0.0, max = 1.0) # This is only used with the mask alpha mode

    Material.msfs_detail_uv_scale = FloatProperty(name = "Detail UV Scale", default = msfs_material_default_values.msfs_detail_uv_scale, min = 0.01, max = 100.0)
    Material.msfs_detail_uv_offset_u = FloatProperty(name = "Detail UV Offset U", default = msfs_material_default_values.msfs_detail_uv_offset_u, min = -10.0, max = 10.0)
    Material.msfs_detail_uv_offset_v = FloatProperty(name = "Detail UV Offset V", default = msfs_material_default_values.msfs_detail_uv_offset_v, min = -10.0, max = 10.0)
    Material.msfs_detail_normal_scale = FloatProperty(name = "Detail Normal Scale", default = msfs_material_default_values.msfs_detail_uv_scale, min = 0.0, max = 1.0)

    Material.msfs_blend_threshold = FloatProperty(name = "Blend Threshold", default = msfs_material_default_values.msfs_blend_threshold, min = 0.001, max = 1.0)

    # Decal / Geo Decal (Frosted)
    Material.msfs_decal_color_blend_factor = FloatProperty(name = "Color", default = msfs_material_default_values.msfs_decal_color_blend_factor, min = 0.0, max = 1.0)
    Material.msfs_decal_metal_blend_factor = FloatProperty(name = "Metal", default = msfs_material_default_values.msfs_decal_metal_blend_factor, min = 0.0, max = 1.0)
    Material.msfs_decal_normal_blend_factor = FloatProperty(name = "Normal", default = msfs_material_default_values.msfs_decal_normal_blend_factor, min = 0.0, max = 1.0)
    Material.msfs_decal_roughness_blend_factor = FloatProperty(name = "Roughness", default = msfs_material_default_values.msfs_decal_roughness_blend_factor, min = 0.0, max = 1.0)
    Material.msfs_decal_occlusion_blend_factor = FloatProperty(name = "Occlusion", default = msfs_material_default_values.msfs_decal_occlusion_blend_factor, min = 0.0, max = 1.0) # This is Blast Sys on Geo Decals
    Material.msfs_decal_emissive_blend_factor = FloatProperty(name = "Emissive", default = msfs_material_default_values.msfs_decal_emissive_blend_factor, min = 0.0, max = 1.0) # This is Melt Sys on Geo Decals

    # Windshield
    Material.msfs_rain_drop_scale = FloatProperty(name = "Rain Drop Scale", default = msfs_material_default_values.msfs_rain_drop_scale, min = 0.0, max = 100.0)
    Material.msfs_wiper_1_state = FloatProperty(name = "Wiper 1 State", default = msfs_material_default_values.msfs_wiper_1_state, min = 0.0, max = 1.0)
    Material.msfs_wiper_2_state = FloatProperty(name = "Wiper 2 State", default = msfs_material_default_values.msfs_wiper_2_state, min = 0.0, max = 1.0) # The 3DS Max plugin has up to 4 states, but the last 2 aren't visible

    # Glass
    Material.msfs_glass_reflection_factor = FloatProperty(name = "Glass Reflection Mask Factor", default = msfs_material_default_values.msfs_glass_reflection_factor, min = 0.0, max = 1.0)
    Material.msfs_glass_deformation_factor = FloatProperty(name = "Glass Deformation Factor", default = msfs_material_default_values.msfs_glass_deformation_factor, min = 0.0, max = 1.0)

    # Parallax
    Material.msfs_parallax_scale = FloatProperty(name = "Parallax Scale", default = msfs_material_default_values.msfs_parallax_scale, min = 0.0, max = 1.0)
    Material.msfs_parallax_room_size_x = FloatProperty(name = "Parallax Room Size X", default = msfs_material_default_values.msfs_parallax_room_size_x, min = 0.01, max = 10.0)
    Material.msfs_parallax_room_size_y = FloatProperty(name = "Parallax Room Size Y", default = msfs_material_default_values.msfs_parallax_room_size_y, min = 0.01, max = 10.0)
    Material.msfs_parallax_room_number = FloatProperty(name = "Parallax Room Number XY", default = msfs_material_default_values.msfs_parallax_room_number, min = 1.0, max = 16.0)
    Material.msfs_parallax_corridor = BoolProperty(name = "Corridor", default = msfs_material_default_values.msfs_parallax_corridor)

    # Hair / SSS
    Material.msfs_sss_color = FloatVectorProperty(name = "SSS Color", subtype = "COLOR", min = 0.0, max = 1.0, size = 4, default = msfs_material_default_values.msfs_sss_color) # This is disabled in the 3DS Max plugin

    # Fresnel
    Material.msfs_fresnel_factor = FloatProperty(name = "Fresnel Factor", default = msfs_material_default_values.msfs_fresnel_factor, min = 0.001, max = 100.0)
    Material.msfs_fresnel_opacity_bias = FloatProperty(name = "Fresnel Opacity Bias", default = msfs_material_default_values.msfs_fresnel_opacity_bias, min = -1.0, max = 1.0)

    # Textures
    Material.msfs_base_color_texture = PointerProperty(type = Image, name = "Base Color", update = functions.update_base_color_texture)
    Material.msfs_comp_texture = PointerProperty(type = Image, name = "Composite (Occlusion (R), Roughness (G), Metalness (B))", update = functions.update_comp_texture)
    Material.msfs_normal_texture = PointerProperty(type = Image, name = "Normal", update = functions.update_normal_texture)
    Material.msfs_emissive_texture = PointerProperty(type = Image, name = "Emissive", update = functions.update_emissive_texture)
    Material.msfs_detail_color_texture = PointerProperty(type = Image, name = "Detail Color", update = functions.update_base_color_texture)
    Material.msfs_detail_comp_texture = PointerProperty(type = Image, name = "Detail Composite (Occlusion (R), Roughness (G), Metalness (B))", update = functions.update_comp_texture)
    Material.msfs_detail_normal_texture = PointerProperty(type = Image, name = "Detail Normal", update = functions.update_normal_texture)
    Material.msfs_blend_mask_texture = PointerProperty(type = Image, name = "Blend Mask", update = functions.update_blend_mask_texture)
    Material.msfs_wetness_ao_texture = PointerProperty(type = Image, name = "Wetness AO", update = functions.update_wetness_ao_texture) # this is anisotropic direction but the 3DS Max plugin has the variable name as wetness_ao
    Material.msfs_dirt_texture = PointerProperty(type = Image, name = "Dirt", update = functions.update_dirt_texture) # similar to wetness ao, this is clearcoat but the 3DS Max plugin has the variable name as dirt
    Material.msfs_height_map_texture = PointerProperty(type = Image, name = "Height Map") # Doesn't seem to be enabled yet in the 3DS Max plugin

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

    # For importing
    Material.is_import = BoolProperty(name = "is_import", default = False)

classes = (
    msfs_material_properties,
)

register, unregister = bpy.utils.register_classes_factory(classes)

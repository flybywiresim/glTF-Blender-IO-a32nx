# Copyright 2018-2021 The glTF-Blender-IO authors, FlyByWire Simulations, bestdani.
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
import os
import tempfile
from os.path import dirname, join, isfile, basename, normpath
import urllib.parse
import re
import pathlib
import configparser
import codecs
import subprocess
import numpy

from ...io.imp.gltf2_io_binary import BinaryData
from ...io.com import gltf2_io_debug


# Note that Image is not a glTF2.0 object
class BlenderImage():
    """Manage Image."""
    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def create(gltf, img_idx, is_dds, label):
        """Image creation."""
        img = gltf.data.images[img_idx]
        img_name = img.name

        if img.blender_image_name is not None:
            # Image is already used somewhere
            return

        tmp_dir = None
        is_placeholder = False
        try:
            if img.uri is not None and not img.uri.startswith('data:'):
                # Image stored in a file
                if is_dds:
                    path = convert_dds(gltf, img)
                else:
                    path = join(dirname(gltf.filename), _uri_to_path(img.uri))
                if path is None:
                    return
                img_name = img_name or basename(path)

            else:
                # Image stored as data => create a tempfile, pack, and delete file
                img_data = BinaryData.get_image_data(gltf, img_idx)
                if img_data is None:
                    return
                img_name = img_name or 'Image_%d' % img_idx
                tmp_dir = tempfile.TemporaryDirectory(prefix='gltfimg-')
                filename = _filenamify(img_name) or 'Image_%d' % img_idx
                filename += _img_extension(img)
                path = join(tmp_dir.name, filename)
                with open(path, 'wb') as f:
                    f.write(img_data)

            num_images = len(bpy.data.images)

            try:
                blender_image = bpy.data.images.load(
                    os.path.abspath(path),
                    check_existing=tmp_dir is None,
                )
            except RuntimeError:
                gltf.log.error("Missing image file (index %d): %s" % (img_idx, path))
                blender_image = _placeholder_image(img_name, os.path.abspath(path))
                is_placeholder = True

            if is_dds and label == "NORMALMAP":
                BlenderImage.convert_normal_map(blender_image)

            if len(bpy.data.images) != num_images:  # If created a new image
                blender_image.name = img_name

                needs_pack = (
                    gltf.import_settings['import_pack_images'] or
                    tmp_dir is not None
                )
                if not is_placeholder and needs_pack:
                    blender_image.pack()

            img.blender_image_name = blender_image.name

        finally:
            if tmp_dir is not None:
                tmp_dir.cleanup()

    @staticmethod
    def convert_normal_map(normal_image):
        # asobo normal maps have no z (blue) channel, so we have to calculate one, as well as flip the y (green) channel
        width = normal_image.size[0]
        height = normal_image.size[1]
        pixels = numpy.empty(width * height * 4, dtype=numpy.float32)
        normal_image.pixels.foreach_get(pixels)
        pixels = pixels.reshape((-1, 4))
        rgb_pixels = pixels[:, 0:3]
        rgb_pixels[:, 1] = 1.0 - rgb_pixels[:, 1]
        rgb_pixels[:, 2] = numpy.sqrt(
            1 - (rgb_pixels[:, 0] - 0.5) ** 2 - (rgb_pixels[:, 1] - 0.5) ** 2
        )
        pixel_data = pixels.reshape((-1, 1)).transpose()[0]
        normal_image.pixels.foreach_set(pixel_data)
        try:
            normal_image.save()
            normal_image.reload()
        except RuntimeError:
            gltf2_io_debug.print_console("ERROR", "Could not save converted image {}".format(normal_image.name))

def _placeholder_image(name, path):
    image = bpy.data.images.new(name, 128, 128)
    # allow the path to be resolved later
    image.filepath = path
    image.source = 'FILE'
    return image

def _uri_to_path(uri):
    uri = urllib.parse.unquote(uri)
    return normpath(uri)

def _img_extension(img):
    if img.mime_type == 'image/png':
        return '.png'
    if img.mime_type == 'image/jpeg':
        return '.jpg'
    return ''

def _filenamify(s):
    s = s.strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def textures_allowed(gltf):
    texconv_path = pathlib.Path(gltf.addon_settings.texconv_file)
    texture_output_path = pathlib.Path(gltf.addon_settings.texture_output_dir)
    flight_sim_path = pathlib.Path(gltf.addon_settings.flight_sim_dir)
    if gltf.addon_settings.texconv_file == '' or not texconv_path.exists():
        return False
    if gltf.addon_settings.texture_output_dir == '' or not texture_output_path.exists() or not texture_output_path.is_dir():
        return False
    if gltf.addon_settings.flight_sim_dir == '' or not flight_sim_path.exists() or not flight_sim_path.is_dir():
        return False
    return True

def convert_dds(gltf, image):
    if textures_allowed(gltf):
        import_path = dirname(gltf.filename)
        local_texture_dir = pathlib.Path(import_path).parent / 'TEXTURE'
        dds_file = local_texture_dir / image.uri
        if gltf.addon_settings.flight_sim_dir in import_path or gltf.import_settings['include_sim_textures']: # we are importing from somewhere in the flight sim directory, or the user specified to include flight sim textures
            if not dds_file.exists():
                paths = get_texture_paths(gltf)
                for root, file in paths:
                    if file == image.uri:
                        if 'Community' in root: # community texture always overrides official files
                            config_file = pathlib.Path(root).parent / 'aircraft.cfg'
                            if config_file.exists():
                                config = configparser.ConfigParser(strict = False)
                                config.read_file(codecs.open(config_file, 'r', 'utf-8'))
                                if "VARIATION" in [i.upper() for i in config.sections()]: # if variation is present, we know that this is a livery and we shouldn't use this texture
                                    continue
                            dds_file = pathlib.Path(root) / file
                            break
                        else:
                            dds_file = pathlib.Path(root) / file # we don't break here because a community file may be present
        if not dds_file.exists():
            gltf2_io_debug.print_console("WARNING", "Could not find image {}".format(file))
            return None

        # convert the image
        texconv_path = gltf.addon_settings.texconv_file

        output_path = gltf.addon_settings.texture_output_dir
        try:
            output_lines = subprocess.run(
                [
                    texconv_path,
                    '-y',
                    '-o', output_path,
                    '-f', 'rgba',
                    '-ft', 'png',
                    str(dds_file)
                ],
                check=True,
                capture_output=True
            ).stdout.decode('cp1252').split('\r\n')
        except subprocess.CalledProcessError as e:
            gltf2_io_debug.print_console("ERROR", "Could not convert image {}: {}".format(dds_file, e))
            return None
        
        file_path = None
        for line in output_lines:
            line = line.lstrip()
            if line.startswith('writing '):
                file = pathlib.Path(line.split('writing ')[1])
                if file.exists():
                    file_path = file
                else:
                    gltf2_io_debug.print_console("WARNING", "Could not find image {}".format(file))
                    return None
        return file_path
                

    else:
        return None
    

def get_texture_paths(gltf):
    # gets every file in the sim installation directory (probably could change to just looking for certain image formats, but new ones may get supported)
    if gltf.texture_path_cache != []:
        return gltf.texture_path_cache
    else:
        gltf.texture_path_cache = []
        directory = pathlib.Path(gltf.addon_settings.flight_sim_dir)
        if directory is not None:
            for root, _, files in os.walk(directory):
                for file in files:
                    gltf.texture_path_cache.append((root, file))
        return gltf.texture_path_cache
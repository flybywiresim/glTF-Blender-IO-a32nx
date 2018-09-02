"""
 * ***** BEGIN GPL LICENSE BLOCK *****
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 *
 * Contributor(s): Julien Duroure.
 *
 * ***** END GPL LICENSE BLOCK *****
 * This development is done in strong collaboration with Airbus Defence & Space
 """

from .gltf2_io_node import *

class PyScene():
    def __init__(self, index, json, gltf):
        self.json = json   # Scene json
        self.gltf = gltf # Reference to global glTF instance

        # glTF2.0 scene properties required
        # No required !

        # glTF2.0 scene properties not required
        #TODO : note that all these properties are not managed yet
        self.nodes = {} #TODO: rename ? in specification, nodes contains only root nodes
        self.name = ""
        self.extensions = {}
        self.extras = {}

        # PyScene specific
        self.root_nodes_idx = [] #TODO: in specification, nodes contains only root nodes
        
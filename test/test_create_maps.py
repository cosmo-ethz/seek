# SEEK is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# SEEK is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with SEEK.  If not, see <http://www.gnu.org/licenses/>.


'''
Created on Mar 7, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.utils.struct import Struct
from seek.plugins import create_maps
import h5py

class TestCreateMapsPlugin(object):

    def test_create_maps(self, tmpdir):
        
        map_pixels = [0, 1]
        tod_path = str(tmpdir.join("tmp"))
        with h5py.File(tod_path, "w") as fp:
            for i, idx in enumerate(map_pixels, 1):
                fp["%s/data"%idx] = i * np.ones((2,2))
                fp["%s/mask"%idx] = np.zeros((2,2), np.bool)
        
        params = Struct(map_maker = "seek.mapmaking.simple_mapper")
        ctx = Struct(params=params,
                     frequencies = np.array([0, 1]),
                     map_pixels = map_pixels,
                     tod_paths = [tod_path],
                     )
        
        plugin = create_maps.Plugin(ctx)
        plugin()
        
        assert np.all(ctx.map_idxs == map_pixels)
        assert np.all(ctx.maps[:, 0, 0] == 1)
        assert np.all(ctx.maps[:, 0, 1] == 2)
        assert np.all(ctx.counts[:, 0, :] == 2)


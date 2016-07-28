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
Created on Feb 26, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import h5py
import importlib
from ivy.plugin.base_plugin import BasePlugin

class RestructuredTODStore(object):

    """
    This class restructures all the 'chunks' of data so that all the
    data points associated with the same healpix pixel is collected
    together.
    """

    def __init__(self, paths):
        self._paths = paths
        
    def __enter__(self):
        self._fps = [h5py.File(path, "r") for path in self._paths]
        return self
    
    def __exit__(self, *args):
        try:
            for fp in self._fps:
                fp.close()
        except:
            pass
        
    def get(self, idx):
        data, mask = [], []
        for fp in self._fps:
            try:
                data.append(fp["%s/data"%idx].value) 
                mask.append(fp["%s/mask"%idx].value)
            except KeyError: pass
        return np.ma.array(np.hstack(data),
                           mask=np.hstack(mask))

def _fill_maps(maps, map_counts, paths, pixels, mapper, ctx):
    """
    Restructure one TOD file.
    """
    xy_ind = 0
    with RestructuredTODStore(paths) as store:
        for i, tod_pixel in enumerate(pixels):
            re_data = store.get(tod_pixel)
            values, counts = mapper.get_mapped_values(re_data, ctx)
            maps[:, xy_ind, i] = values
            map_counts[:, xy_ind, i] = counts

class Plugin(BasePlugin):
    """
    This class fills the map pixels by delegating the computation to the 'map_maker'.
    """

    def __call__(self):
        nfreq = self.ctx.frequencies.shape[0]
        
        maps = np.zeros((nfreq, 2, len(self.ctx.map_pixels)))
        counts = np.zeros(maps.shape)

        mapper = importlib.import_module(self.ctx.params.map_maker)
        _fill_maps(maps, counts, self.ctx.tod_paths, self.ctx.map_pixels, mapper, self.ctx)
        
        self.ctx.map_idxs = self.ctx.map_pixels
        self.ctx.maps = maps
        self.ctx.counts = counts
        self.ctx.redshifts = [] #TODO: add redshifts
        
    def __str__(self):
        return "Create maps"

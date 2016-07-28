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
Created on Jan 5, 2015

author: seehars
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import h5py
import os
import numpy as np

from ivy.plugin.base_plugin import BasePlugin

MAPS_KEY = 'MAPS'
REDSHIFTS_KEY = 'REDSHIFTS'
COUNTS_KEY = 'COUNTS'

class Plugin(BasePlugin):
    """
    Writes map and associated information to HDF5 files.
    """

    def __call__(self):
        if os.path.exists(self.ctx.params.map_name):
            if self.ctx.params.overwrite:
                os.remove(self.ctx.params.map_name)
            else:
                raise IOError("File '%s' already exists!"%self.ctx.params.map_name)

        
        with h5py.File(self.ctx.params.map_name, "w") as hdf_file:
            hdf_file.create_dataset(MAPS_KEY, data=self.ctx.maps, compression="lzf", shuffle=True)
            hdf_file.create_dataset(REDSHIFTS_KEY, data=self.ctx.redshifts)
            hdf_file.create_dataset(COUNTS_KEY, data=self.ctx.counts, dtype=np.int8, compression="lzf", shuffle=True)
    
    def __str__(self):
        return "Write maps"
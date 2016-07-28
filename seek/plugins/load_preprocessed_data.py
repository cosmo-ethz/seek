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
Created on Jan 15, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.plugin.base_plugin import BasePlugin
import h5py
import os
import numpy as np
from seek.plugins import load_data
from seek import Coords

class Plugin(BasePlugin):
    """
    Loads the data, mask and frequencies of the current iteration from disk. Can
    be used for closer analysis of the masking (sum threshold). The data is
    read from the current folder using the same filename as the first input
    filename.
    """

    def __call__(self):
        filename = os.path.basename(self.ctx.file_paths[0])
        filepath = os.path.join(self.ctx.params.post_processing_prefix,
                                filename)
        
        if self.ctx.params.verbose:
            print(filepath)
        
        self.ctx.strategy_start = load_data.get_observation_start_from_hdf5(filepath)
        with h5py.File(filepath, "r") as fp:
            tod = np.ma.array(fp["data"].value, mask=fp["mask"].value)
            self.ctx.tod_vx = tod
            self.ctx.tod_vy = tod.copy()
            self.ctx.frequencies = fp["frequencies"].value
            self.ctx.time_axis = fp["time"].value
            self.ctx.coords = Coords(fp["ra"].value, fp["dec"].value, None, None, self.ctx.time_axis)
            self.ctx.ref_channel = fp["ref_channel"].value

            
    def __str__(self):
        return "loading processed data"
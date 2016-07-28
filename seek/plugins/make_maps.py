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

import numpy as np
import importlib

from ivy.plugin.base_plugin import BasePlugin

class Plugin(BasePlugin):
    """
    Make map from restructured TOD based on the specified map_maker.
    """

    def __call__(self):
        #load module
        mod = importlib.import_module(self.ctx.params.map_maker)
        
        #delegate map making
        maps, redshifts, counts = mod.get_map(self.ctx)
        idxs = np.where(counts!=0)
        self.ctx.map_idxs = idxs
        self.ctx.maps = maps[idxs]
        self.ctx.counts = counts[idxs]
        self.ctx.redshifts = redshifts
        
        del self.ctx.tod_vx
        del self.ctx.tod_vy
    
    def __str__(self):
        return "Make maps from TOD"
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
Created on Jan 7, 2015

@author: seehars
'''
from datetime import datetime
import os

from ivy.utils.struct import Struct
import numpy as np
from seek.plugins import process_coords


COORDS_ROOT = os.path.join(os.path.dirname(__file__), "res", "coords")


class TestLoadCoordsPlugin(object):
    
        
    def testLoadCoords(self):
        params = Struct(telescope_latitude = 47.2000007629395,
                        telescope_longitude = 8.5,
                        telescope_elevation = 500,
                        integration_time = 1
                        )
        ctx = Struct(params=params)
        coords_path = os.path.join(COORDS_ROOT, "coord5m20141121.txt")
        ctx.coords_paths = {"2014-11-22": coords_path}
        ctx.strategy_start = datetime(2014, 11, 22, 17, 0, 0)    
        ctx.tod_vx = np.empty((1, 3))
        ctx.time_axis = np.arange(3)
        
        plugin = process_coords.Plugin(ctx)
        plugin()
        assert ctx.coords is not None
        assert len(ctx.coords.ra) == 3
        assert len(ctx.coords.dec) == 3
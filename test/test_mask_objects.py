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
Created on Mar 20, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from ivy.utils.struct import Struct
from seek.plugins import mask_objects

import numpy as np
from datetime import datetime
from seek import Coords

class TestMaskObjectsPlugin(object):
    
    def setup(self):
        self.params = Struct(telescope_latitude = 47.344192,
                telescope_longitude = 8.114368,
                telescope_elevation = 500,
                min_sun_separation = 15,
                min_moon_separation = 5,
                min_moon_phase_separation = 10,
                min_moon_high_phase = 80,
                verbose=True
                )

    
    def test_no_moon_sun_masking(self):
        
        tod = np.ma.array(np.random.uniform(size=(10,100)),
                          mask=False)
        times = np.zeros((tod.shape[1], 5))
        ctx = Struct(params=self.params,
                     tod_vx = tod,
                     tod_vy = tod,
                     coords = Coords(times[:,0], times[:,1], times[:,1]*0.0, times[:,1]*0.0, times[:,1]*0.0),
                     strategy_start=datetime(2015, 1, 1, 0, 0, 0))
        
        plugin = mask_objects.Plugin(ctx)
        plugin.mask_objects()
        
        assert np.all(tod.mask == False)
        
    def test_sun_masking(self):
        tod = np.ma.array(np.random.uniform(size=(10,100)),
                          mask=False)
        
        coords = Coords([4.14857973] * tod.shape[1], [-0.51101287] * tod.shape[1], [0.0] * tod.shape[1], [0.0] * tod.shape[1], [0.0] * tod.shape[1])
        ctx = Struct(params=self.params,
                     tod_vx = tod,
                     tod_vy = tod,
                     coords = coords,
                     strategy_start=datetime(2014, 11, 25, 11, 00, 00))
        
        plugin = mask_objects.Plugin(ctx)
        plugin.mask_objects()
        
        assert np.any(tod.mask == True)
        
    def test_moon_masking(self):
        tod = np.ma.array(np.random.uniform(size=(10,100)),
                          mask=False)
        
        ras = np.linspace(1.5, 2.5, tod.shape[1])
        decs = [0.26] * tod.shape[1]
        times = np.linspace(0, 4, tod.shape[1])
        coords = Coords(ras, decs, None, None, times)
        ctx = Struct(params=self.params,
                     tod_vx = tod,
                     tod_vy = tod,
                     coords = coords,
                     strategy_start=datetime(2015, 12, 26, 00, 00, 00))
        
        plugin = mask_objects.Plugin(ctx)
        plugin.mask_objects()
        
        assert np.any(tod.mask == True)
        
    

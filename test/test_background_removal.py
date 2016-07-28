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
Created on Feb 24, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

from ivy.utils.struct import Struct
from seek.plugins import background_removal
from seek import Coords

class TestBackgroundRemovalPlugin(object):


    def test_bkg_removal_median(self):
        tod = np.ones((5, 9)) * np.arange(9)
        ctx = Struct(params=Struct(background_model = "median"),
                     tod_vx=np.ma.array(tod),
                     tod_vy=np.ma.array(tod))

        plugin = background_removal.Plugin(ctx)
        plugin()

        assert np.all(ctx.tod_vx.sum(axis=1) == 0)
        assert np.all(ctx.tod_vy.sum(axis=1) == 0)


    def test_bkg_removal_smooth(self):
        tod = np.ones((5, 9)) * np.arange(9)
        mask = np.zeros((5, 9))
        mask[:,0] = 1
        mask[:,-1] = 1
        mask = mask.astype('bool')
        ctx = Struct(params=Struct(background_model = "smooth",
                                   struct_size_0=1,
                                   struct_size_1=1,
                                   nside=1),
                     tod_vx=np.ma.array(tod, mask=mask),
                     tod_vy=np.ma.array(tod, mask=mask),
                     time_axis=np.arange(9),
                     coords=Coords(np.zeros(9), np.zeros(9), None, None, None),
                     simulation_mask=np.zeros(9, dtype=np.bool))

        plugin = background_removal.Plugin(ctx)
        plugin()

        assert np.all(ctx.tod_vx.sum(axis=1) == 0)
        assert np.all(ctx.tod_vy.sum(axis=1) == 0)
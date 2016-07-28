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
Created on Feb 16, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import healpy as hp
from ivy.utils.struct import Struct
from seek.mapmaking import healpy_mapper
from seek import Coords

class TestHealpyMapper(object):
    
    def test_get_map(self):
        
        params = Struct(nside=2, variance=False)
        
        npix = hp.nside2npix(params.nside)
        ind = 1
        theta, phi = hp.pix2ang(params.nside, ind)
        dec = np.pi * .5 - theta
        ra = phi
        times = np.array([[0,0,0,ra,dec],[0,0,0,ra,dec]])
        rfi_mask = np.array([[False, False]], dtype = bool)
        tod_vx = np.ma.array([[1., 2.]], mask=rfi_mask)
        tod_vy = np.ma.array([[2., 4.]], mask=rfi_mask)
        
        frequencies = np.array([1420.40575177])
        ctx = Struct(params = params,
                     frequencies = frequencies,
                     times = times,
                     tod_vx = tod_vx,
                     tod_vy = tod_vy,
                     coords = Coords(times[:,-2], times[:,-1], None, None, None)
                     )
        
        maps, z, counts = healpy_mapper.get_map(ctx)
        t = np.zeros((1, 2, npix))
        t[0, 0, 1] = 3.
        t[0, 1, 1] = 6.
        assert np.allclose(maps, t)
        t[0, 0, 1] = 2
        t[0, 1, 1] = 2
        assert np.allclose(counts, t)
        assert np.isclose(z, 0)
        ctx.params.variance = True
        maps, z, counts = healpy_mapper.get_map(ctx)
        t[0, 0, 1] = .5
        t[0, 1, 1] = 2.
        assert np.allclose(maps, t)

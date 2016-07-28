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

from collections import Counter
import healpy as hp
import h5py
import tempfile

from ivy.plugin.base_plugin import BasePlugin
from seek.mapmaking.healpy_mapper import eq2rad

def restructure(fp, tod, cntr, pix_numbers):
    for pix_number in cntr.keys():
        data = tod[:, pix_numbers==pix_number]
        grp = fp.create_group("%s"%pix_number)
        grp.create_dataset("data", data=data.data)
        grp.create_dataset("mask", data=data.mask, compression="gzip", compression_opts=4, shuffle=True)

class Plugin(BasePlugin):
    """
    Restructure each TOD all the data points associated with the same
    healpix pixel is collected together.
    """

    def __call__(self):
        theta, phi = eq2rad(self.ctx.coords.ra, self.ctx.coords.dec) 
        pix_numbers = hp.ang2pix(self.ctx.params.nside, theta, phi)
        
        cntr = Counter(pix_numbers)
        
        tod = self.ctx.tod_vx
        path = tempfile.mktemp()
        
        with h5py.File(path, "w") as fp:
            restructure(fp, tod, cntr, pix_numbers)
        
        self.ctx.restructured_tod_path = path
        self.ctx.restructured_tod_pixels = cntr.keys()
        
        del self.ctx.tod_vx
        del self.ctx.tod_vy
        del self.ctx.ref_channel
        del self.ctx.coords
    
    def __str__(self):
        return "Restructure TOD"
    
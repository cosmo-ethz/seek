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

@author: seehars
'''
import os
import tempfile

import pytest
import numpy as np
import h5py
from ivy.utils.struct import Struct

from seek.plugins import write_maps

class TestWriteMapsPlugin(object):
    
    def setup(self):
        self.maps = np.zeros((1,2))
        self.redshifts = np.array([0.1, 0.2])
        self.frequencies = np.array([0.1, 0.2])
        
        self.params = Struct()
        ctx = Struct(params = self.params,
                     maps = self.maps,
                     redshifts = self.redshifts,
                     counts = np.ones_like(self.maps),
                     frequencies = self.frequencies)
        self.plugin = write_maps.Plugin(ctx) 
        
    def testWriteMaps(self):
        _, name = tempfile.mkstemp()
        name1 = name + '_1.hdf'
        self.params.map_name = name1
        self.params.overwrite = False
        self.plugin()
        assert os.path.isfile(name1)
        f = h5py.File(name1)
        assert np.allclose(f[write_maps.MAPS_KEY].value, self.maps)
        assert np.allclose(f[write_maps.REDSHIFTS_KEY].value, self.redshifts)

        with pytest.raises(Exception):
            self.plugin()

        self.plugin.ctx.params.overwrite = True
        self.plugin()
        assert os.path.isfile(name1)

        name2 = name + "_2.hdf"
        self.params.map_name = name2
        self.params.overwrite = False
        self.plugin()
        assert os.path.isfile(name1)
        assert os.path.isfile(name2)

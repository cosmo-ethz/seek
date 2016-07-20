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
        self.params = Struct()
        ctx = Struct(params = self.params,
                     maps = self.maps,
                     redshifts = self.redshifts,
                     counts = np.ones_like(self.maps))
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

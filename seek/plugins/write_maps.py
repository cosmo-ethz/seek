# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

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
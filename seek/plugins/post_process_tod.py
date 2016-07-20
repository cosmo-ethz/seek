# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Feb 6, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.plugin.base_plugin import BasePlugin
import h5py
import os

class Plugin(BasePlugin):
    """
    Writes the data, mask and frequencies of the current iteration to disk. Can
    be used for closer analysis of the masking (sum threshold). Output is
    written to the current folder using the same filename as the first input
    filename (may overwrite the original file if not being careful)
    """

    def __call__(self):
        if not self.ctx.params.store_intermediate_result:
            return
        
        filename = os.path.basename(self.ctx.file_paths[0])
        filepath = os.path.join(self.ctx.params.post_processing_prefix,
                                filename)
        
        with h5py.File(filepath, "w") as fp:
            fp["data"] = self.ctx.tod_vx.data
            fp["mask"] = self.ctx.tod_vx.mask
            fp["frequencies"] = self.ctx.frequencies
            fp["time"] = self.ctx.time_axis
            fp["ra"] = self.ctx.coords.ra
            fp["dec"] = self.ctx.coords.dec
            fp["ref_channel"] = self.ctx.ref_channel
            
            
    def __str__(self):
        return "postprocessing TOD"
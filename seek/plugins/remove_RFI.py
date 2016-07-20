# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Jan 5, 2015

author: seehars
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import importlib

from ivy.plugin.base_plugin import BasePlugin
import numpy as np

class Plugin(BasePlugin):
    """ Call the specified RFI mitigation module. """

    def __call__(self):
        if hasattr(self.ctx.params, 'cleaner') and self.ctx.params.cleaner != "None":
            #load module
            mod = importlib.import_module(self.ctx.params.cleaner)        
    
            rfi_mask_vx, rfi_mask_vy = mod.rm_rfi(self.ctx)
            
            self.ctx.tod_vx.mask = np.bitwise_or(self.ctx.tod_vx.mask, rfi_mask_vx)
            self.ctx.tod_vy.mask = np.bitwise_or(self.ctx.tod_vy.mask, rfi_mask_vy)
    
    def __str__(self):
        return "Remove RFI"
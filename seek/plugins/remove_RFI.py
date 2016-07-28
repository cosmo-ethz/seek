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
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
Created on Jan 7, 2015

@author: seehars
'''
import os

import numpy as np
from ivy.utils.struct import Struct

from seek.plugins import remove_RFI

class TestRemoveRFIPlugin(object):
    
    def setup(self):
        params = Struct(cleaner = "seek.mitigation.outlier_masking",
                        multiplicator = 5)
        self.ctx = Struct(params = params,
                          tod_vx = np.ma.array([[1]]),
                          tod_vy = np.ma.array([[1]]))
        
    def testRemoveRFI(self):
        rm_RFI = remove_RFI.Plugin(self.ctx)
        rm_RFI()
        assert self.ctx.tod_vx.mask == False
        assert self.ctx.tod_vy.mask == False

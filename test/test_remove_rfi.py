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

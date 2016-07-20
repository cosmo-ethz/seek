'''
Created on Jan 7, 2015

@author: seehars
'''
import numpy as np
from ivy.utils.struct import Struct
from seek.plugins import calibration
import os

DATA_PATH = 'res/data'

class TestCalibrationPlugin(object):
    
    def setup(self):
        current_path = os.path.dirname(__file__)
        params = Struct(flux_calibration = "default",
                        gain_file_default=os.path.join(os.path.join(current_path, DATA_PATH),'gain_null.dat'))
        self.ctx = Struct(params = params)
        
    def testCalibration(self):
        calib = calibration.Plugin(self.ctx)
        calib()
        assert self.ctx.params.gain_file_default


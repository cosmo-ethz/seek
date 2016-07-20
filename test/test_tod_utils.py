# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Aug 18, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from seek.utils import tod_utils

class TestTodUtils(object):
    
    def test_smooth_axis0(self):
        #axis = 0
        tod = np.array([[1,1,1,1,2,2,2,2,3,3,3,3],
                         [4,4,4,4,5,5,5,5,6,6,6,6],
                         [7,7,7,7,8,8,8,8,9,9,9,9]]).T
        smoothed = tod_utils.smooth(tod, 1, axis=0)
        
        assert np.all(tod==smoothed)
        
        smoothed = tod_utils.smooth(tod, 4, axis=0)
        exp = np.array([[1,2,3],
                        [4,5,6],
                        [7,8,9]]).T
        assert np.all(exp==smoothed)

    def test_smooth_axis1(self):
        #axis = 1
        tod = np.array([[1,1,1,1,2,2,2,2,3,3,3,3],
                         [4,4,4,4,5,5,5,5,6,6,6,6],
                         [7,7,7,7,8,8,8,8,9,9,9,9]])
        smoothed = tod_utils.smooth(tod, 1, axis=1)
        
        assert np.all(tod==smoothed)
        
        smoothed = tod_utils.smooth(tod, 4, axis=1)
        exp = np.array([[1,2,3],
                        [4,5,6],
                        [7,8,9]])
        assert np.all(exp==smoothed)
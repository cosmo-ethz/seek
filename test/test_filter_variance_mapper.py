# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Feb 26, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from seek.mapmaking import filter_variance_mapper

def test_get_mapped_values():
    data = np.ones((2, 9))
    data[:,0] = 10 #outlier
    data = np.ma.array(data, mask=np.zeros((2,9), np.bool))
    
    values, counts = filter_variance_mapper.get_mapped_values(data, None)
    assert values.shape == (2,)
    assert np.all(values==0)
    
    assert counts.shape == (2,)
    assert np.all(counts==8)

# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Mar 20, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from seek.mitigation import sum_threshold

import numpy as np
from collections import Counter
from ivy.utils.struct import Struct

class TestSumThreshold(object):
    
    def test_no_masking(self):
        tod = np.ma.array(np.zeros((100,100)))
        mask = sum_threshold.get_empty_mask(tod.shape)
        rfi_mask = mask = sum_threshold.get_rfi_mask(tod, mask, normalize_standing_waves=False, plotting=False)
        
        assert np.all(rfi_mask == False)
        
    def test_masking(self):
        tod = np.ma.array(np.zeros((100,100)))
        
        tod[40:60, 40:60] = 5000000
        
        mask = sum_threshold.get_empty_mask(tod.shape)
        rfi_mask = mask = sum_threshold.get_rfi_mask(tod, mask, normalize_standing_waves=False, plotting=False)
        
        assert np.any(rfi_mask == True)
        
    def test_dilate_mask(self):
        mask = sum_threshold.get_empty_mask((50,50))
        mask[20:25,20:25] = True
        dilated_mask = sum_threshold.binary_mask_dilation(mask, 5, 5)
        
        mask_counts = Counter(mask.ravel().tolist())
        dilated_counts = Counter(dilated_mask.ravel().tolist())
        assert mask_counts[True] < dilated_counts[True]
        
        
    def test_rm_rfi(self):
        params = Struct(chi_1 = 1.5 ,
                        sm_kernel_m = 40,
                        sm_kernel_n = 20,
                        sm_sigma_m = 15,
                        sm_sigma_n = 7.5,
                        
                        struct_size_0 = 5,
                        struct_size_1 = 5,

                        eta_i = [1],
                        )
        
        data = np.zeros((100,100))
        tod = np.ma.array(data, mask=sum_threshold.get_empty_mask(data.shape))
        
        ctx = Struct(params=params,
                     tod_vx = tod)
        
        rfi_mask_vx, rfi_mask_vy = sum_threshold.rm_rfi(ctx)
        assert np.all(rfi_mask_vx == False)
        assert np.all(rfi_mask_vy == False)
        
        
        
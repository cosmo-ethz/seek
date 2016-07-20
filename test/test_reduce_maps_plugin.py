# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Feb 16, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.utils.struct import Struct
from seek.plugins import reduce_maps


class TestReduceMapsPlugin(object):

    def test_reduce(self):
        
        params = Struct(nside=16)
        
        frequencies = np.array([0,1])
        ctx = Struct(params = params,
                     frequencies = frequencies,
                     tod_paths = [],
                     redshifts=0)
        
        freq_0 = 1
        freq_1 = 2
        freq_2 = 3
        freq_3 = 4
        
        ctx1 = Struct(ctx, 
                     map_idxs = (0),
                     maps = np.array([[ freq_0, 0],[freq_1, 0]]),
                     counts = np.array([[1, 0],[1, 0]]))

        ctx2 = Struct(ctx, 
                     map_idxs = (1),
                     maps = np.array([[freq_2,  0],[freq_3, 0]]),
                     counts = np.array([[1, 0],[1, 0]]))
        
        ctxList = [ctx1, ctx2]
        
        plugin = reduce_maps.Plugin(ctx)
        plugin.reduce(ctxList)
        
        assert ctx.maps is not None
        assert ctx.maps[0,0,0] == freq_0
        assert ctx.maps[1,0,0] == freq_1
        assert ctx.maps[0,0,1] == freq_2
        assert ctx.maps[1,0,1] == freq_3
        assert np.all(ctx.maps[0,1,:] == 0)
        assert ctx.counts[:,0,:].sum() == 4
        assert ctx.counts[:,1,:].sum() == 0
        
        
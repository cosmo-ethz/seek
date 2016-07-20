# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Mar 7, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.utils.struct import Struct
from seek.plugins import reduce_map_indicies

class TestReduceMapIndiciesPlugin(object):

    def test_reduce(self):
        params = Struct()
        frequencies = []
        ctx = Struct(params=params,
                     frequencies = frequencies,
                     )
        
        pixels = [1,2,3,1]
        ctx1 = Struct(ctx,
                      restructured_tod_path="path1",
                      restructured_tod_pixels=pixels[:2])
        ctx2 = Struct(ctx,
                      restructured_tod_path="path2",
                      restructured_tod_pixels=pixels[2:])
        ctxList = [ctx1, ctx2]
        
        plugin = reduce_map_indicies.Plugin(ctx)
        plugin.reduce(ctxList)
        
        
        assert len(ctx.tod_paths) == 2
        assert np.all(ctx.restructured_tod_pixels == list(set(pixels)))
        assert ctx.frequencies == frequencies
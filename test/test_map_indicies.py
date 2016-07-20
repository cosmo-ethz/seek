# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Mar 7, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.utils.struct import Struct
from seek.plugins import map_indicies

class TestMapIndiciesPlugin(object):

    def test_map_indicies(self):
        params = Struct(cpu_count=2)
        ctx = Struct(params=params,
                     restructured_tod_pixels = [1,2,3,4])
        plugin = map_indicies.Plugin(ctx)
        
        for i, ctx in enumerate(plugin.getWorkload()):
            assert len(ctx.map_pixels) == 2
        
        assert i == 1

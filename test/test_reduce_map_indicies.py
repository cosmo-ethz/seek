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
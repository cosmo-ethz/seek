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

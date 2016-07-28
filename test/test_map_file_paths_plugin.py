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
Created on Feb 3, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.utils.struct import Struct
from seek.plugins import map_file_paths
import os

NAME = 'res/skymap/SKYMAP_2014-11-21-20:00:00.hdf'

class TestMapFilePathPlugin(object):

    def test_map_file_path(self):
        current_path = os.path.dirname(__file__)
        params = Struct(data_file_prefix = "SKYMAP_",
                        data_file_suffix = ".hdf",
                        file_date_format = "{0}%Y-%m-%d-%H:%M:%S{1}",
                        chunk_size = 1,
                        )
        
        full_path = os.path.join(current_path, NAME)
        ctx = Struct(params = params,
                     data_file_paths = [[full_path], # day 1
                                        [full_path]  # day 2
                                        ]
                     )
    
        plugin = map_file_paths.Plugin(ctx)
    
        for idx, ctx in enumerate(plugin.getWorkload()):
            assert ctx is not None
            assert ctx.file_paths[0] == full_path
        
        assert idx == 1
        
        ctx.data_file_paths = [[full_path, full_path], # day 1
                               [full_path]]            # day 2
        ctx.params.chunk_size = 2
        plugin = map_file_paths.Plugin(ctx)
        
        ctxs = list(plugin.getWorkload())
        assert len(ctxs[0].file_paths) == 2
        assert len(ctxs[1].file_paths) == 1
        
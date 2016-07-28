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
from seek.plugins import find_nested_files
import os
import pytest

DATA_PATH = 'res/data'

class TestFindNestedFilesPlugin(object):

    def test_find_file_in_range(self):
        current_path = os.path.dirname(__file__)
        file_prefix = os.path.join(current_path, DATA_PATH)
        params = Struct(strategy_start = "2015-01-01-00:00:00",
                        strategy_end   = "2015-01-01-18:00:10",
                        data_file_prefix = "HIMap_",
                        data_file_suffix = "_02.fit.gz",
                        file_date_format = "%Y%m%d_%H%M%S",
                        file_prefix = file_prefix,
                        coord_prefix = "coord5m",
                        verbose=True)
        ctx = Struct(params = params)
    
        plugin = find_nested_files.Plugin(ctx)
        
        with pytest.raises(AssertionError):
            plugin()
    
        params.strategy_start = "2015-05-04-00:00:00"
        params.strategy_end   = "2015-05-05-18:00:10"
        plugin()
    
        assert ctx.calibrations_paths is not None
        assert len(ctx.calibrations_paths) == 0
        assert ctx.data_file_paths is not None
        assert len(ctx.data_file_paths) == 2
        assert len(ctx.data_file_paths[0]) == 1
        assert len(ctx.data_file_paths[1]) == 1
        assert ctx.coords_paths is not None
        assert len(ctx.coords_paths) == 2

    def test_skip_folder(self):
        current_path = os.path.dirname(__file__)
        file_prefix = os.path.join(current_path, DATA_PATH)
        params = Struct(strategy_start = "2015-05-06-00:00:00",
                        strategy_end   = "2015-05-06-18:00:10",
                        file_prefix = file_prefix,
                        data_file_prefix = "HIMap_",
                        data_file_suffix = "_02.fit.gz",
                        file_date_format = "%Y%m%d_%H%M%S",
                        coord_prefix = "coord5m",)
        ctx = Struct(params = params)
    
        plugin = find_nested_files.Plugin(ctx)
        
        with pytest.raises(AssertionError):
            plugin()
        
    def test_calibration_in_range(self):
        current_path = os.path.dirname(__file__)
        file_prefix = os.path.join(current_path, DATA_PATH)
        params = Struct(strategy_start = "2015-05-07-00:00:00",
                        strategy_end   = "2015-05-07-18:00:10",
                        data_file_prefix = "HIMap_",
                        data_file_suffix = "_02.fit.gz",
                        file_date_format = "%Y%m%d_%H%M%S",
                        file_prefix = file_prefix,
                        coord_prefix = "coord5m",
                        verbose=True)
        ctx = Struct(params = params)
    
        plugin = find_nested_files.Plugin(ctx)
        
        plugin()
    
        assert ctx.calibrations_paths is not None
        assert len(ctx.calibrations_paths) == 1
        assert len(ctx.calibrations_paths["2015-05-07"][1]) == 1
        assert ctx.data_file_paths is not None
        assert len(ctx.data_file_paths) == 0

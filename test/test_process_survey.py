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


"""
Tests for `seek` module.
"""
from __future__ import print_function, division, absolute_import

import pytest
import tempfile
import ivy
import os

DATA_PATH = 'res/data'

try:
    os.environ["HUDSON_URL"]
    JENKINS = True
except KeyError:
    JENKINS = False
JENKINS = True
class TestSampleRun(object):

    def test_sampleRun(self):
        if JENKINS:
            pytest.skip("Only for local testing")
            
        _, prefix = tempfile.mkstemp()
        file_name = "%s_map.hdf"%prefix
        current_path = os.path.dirname(__file__)

        file_prefix = os.path.join(os.path.dirname(__file__), "res", "data")
        args = [
                "--strategy-start=2015-05-04-00:00:00",
                "--strategy-end=2015-05-05-18:00:10",
                "--file-prefix="+file_prefix,
                "--map-name="+file_name,
                "--coord-prefix=coord5m",
                "--data-file-prefix=HIMap_",
                "--data-file-suffix=_02.fit.gz",
                "--file-date-format=%Y%m%d_%H%M%S",
                "--max-frequency=1306",
                "--nside=16",
                "--flux-calibration='default'",
                "--gain-file-default="+os.path.join(os.path.join(current_path, DATA_PATH),'gain_null.dat'),
                "seek.config.process_survey"]
        
#         file_prefix = "/Volumes/astro/refreg/data/Radio/Bleien/"
#         args = [
#                 "--file-prefix="+file_prefix,
#                 "--strategy-start=2015-06-02-09:00:00", 
#                 "--strategy-end=2015-06-02-09:59:00",
#                 "--clean=None",
#                 "--chunk-size=1", 
#                 "--map-name="+file_name,
#                 "--coord-prefix=coord7m",
#                 "--data-file-prefix=HIMap_",
#                 "--data-file-suffix=_03.fit.gz",
#                 "--file-date-format=%Y%m%d_%H%M%S",
#                 "--max-frequency=1306",
#                 "seek.config.process_survey"]
        
        ivy.execute(args)
        
        #TODO: weak test. possible rewrite
        assert os.path.isfile(file_name)

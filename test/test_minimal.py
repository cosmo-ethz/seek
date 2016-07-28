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
Tests for `seekd` module.
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
        file_prefix = os.path.join(os.path.dirname(__file__), "res", "skymap") + "/SKYMAP_"
        file_prefix = "/Users/jakeret/workspace/seek/../hide/drift2015/HIMAP_2015-05-18-11:00:25"
        args = [
                "--file-prefix="+file_prefix,
                "--min-frequency=980",
                "--max-frequency=1260",
                #"--file-prefix="+"/Users/jakeret/workspace/seek/gsm_test/GSM_2015-01-01-00:00:00",
#                 "--file-prefix="+"/Users/jakeret/workspace/seek/nod/SKYMAP_2015-01-23-", 
#                 "--file-prefix="+"/Users/jakeret/workspace/seek/data/FFT20150129scan/M9703_2015-01-29-23:55:21", 
                "--flux-calibration='default'",
                "--gain-file-default="+os.path.join(os.path.join(current_path, DATA_PATH),'gain_null.dat'),
                "--cleaner=None", 
                "--integration-time=5", 
                "--map-name="+file_name,
                "seek.config.extended"]
        
        ivy.execute(args)
        
        #TODO: weak test. possible rewrite
        assert os.path.isfile(file_name)

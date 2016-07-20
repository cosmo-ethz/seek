# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

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

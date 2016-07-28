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
Created on Feb 2, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals
import os
import datetime

import numpy as np

from ivy.utils.struct import Struct
from seek.plugins import load_data

FITS_FILE = "SKYMAP_20141121_200000_01.fit.gz"
FITS_DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "res", "data", FITS_FILE)
HDF5_FILE = "M9703A_DPUA_20141121_200000.h5"
HDF5_DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "res", "data", HDF5_FILE)

FREQUENCY_COUNT = 200
TIME_STEP_SIZE = 0.25
OBSERVATION_DATE = datetime.datetime(2014,11,21,20,00,00)

class TestLoadDataPlugin(object):

    def setup(self):
        self.params = Struct(spectrometer = "custom",
                             verbose=True)
        self.ctx = Struct(params=self.params,
                          file_path = FITS_DATA_FILE_PATH)

    def test_get_observation_start(self):
        observation_start = load_data.get_observation_start(FITS_DATA_FILE_PATH, load_data.FITS_FILE_TYPE)
        assert observation_start == OBSERVATION_DATE
        
        observation_start = load_data.get_observation_start(HDF5_DATA_FILE_PATH, load_data.HDF5_FILE_TYPE)
        assert observation_start == OBSERVATION_DATE
        
    def test_get_observation_start_from_fits(self):
        observation_start = load_data.get_observation_start_from_fits(FITS_DATA_FILE_PATH)
        assert observation_start == OBSERVATION_DATE
        
    def test_get_observation_start_from_hdf5(self):
        observation_start = load_data.get_observation_start_from_hdf5(HDF5_DATA_FILE_PATH)
        assert observation_start == OBSERVATION_DATE
        
    def test_get_data(self):
        params = Struct(spectrometer="custom")
        ctx = Struct(params=params)
        
        params.file_type = load_data.FITS_FILE_TYPE
        tod, mask, frequencies, time_axis = load_data._get_data(FITS_DATA_FILE_PATH, ctx)
        #assert time_step_size == TIME_STEP_SIZE
        assert tod.shape == (FREQUENCY_COUNT, 1 / TIME_STEP_SIZE * 15 * 60)
        assert tod.dtype == np.float64

        assert mask is None
        
        assert frequencies is not None
        assert len(frequencies) == FREQUENCY_COUNT
        assert time_axis is not None
        assert len(time_axis) == (1 / TIME_STEP_SIZE * 15 * 60)

        params.file_type = load_data.HDF5_FILE_TYPE
        params.m9703a_mode = load_data.MODE_TOTAL_POWER
        params.spectral_kurtosis = True
        params.accumulations = 146484
        params.accumulation_offset = 10
        
        
        tod, mask, frequencies, time_axis = load_data._get_data(HDF5_DATA_FILE_PATH, ctx)
        assert tod.shape == (90, 14)
        assert tod.dtype == np.float64
        
        assert mask.shape == (90, 14)
        assert mask.dtype == np.bool
        
        assert np.all(tod == 2)
        
        assert frequencies is not None
        assert len(frequencies) == 90

        assert time_axis is not None
        assert len(time_axis) == 14

    def test_get_data_from_fits(self):
        tod, frequencies, time_axis = load_data._get_data_from_fits(FITS_DATA_FILE_PATH)
        #assert time_step_size == TIME_STEP_SIZE
        assert tod.shape == (FREQUENCY_COUNT, 1 / TIME_STEP_SIZE * 15 * 60)
        assert tod.dtype == np.float64
        assert frequencies is not None
        assert len(frequencies) == FREQUENCY_COUNT
        assert time_axis is not None
        assert len(time_axis) == (1 / TIME_STEP_SIZE * 15 * 60)

        
    def test_get_data_from_hdf5(self):
        tod, frequencies, time_axis = load_data._get_data_from_hdf5(HDF5_DATA_FILE_PATH, load_data.MODE_PHASE_SWITCH)
        assert tod.shape == (90, 14)
        assert tod.dtype == np.float64
        
        assert np.all(tod == 0)
        
        assert frequencies is not None
        assert len(frequencies) == 90

        assert time_axis is not None
        assert len(time_axis) == 14

        tod, frequencies, time_axis = load_data._get_data_from_hdf5(HDF5_DATA_FILE_PATH, load_data.MODE_TOTAL_POWER)
        assert tod.shape == (90, 14)
        assert tod.dtype == np.float64

        assert np.all(tod == 2)
        
        assert frequencies is not None
        assert len(frequencies) == 90
        assert time_axis is not None
        assert len(time_axis) == 14


    def test_get_spectral_kurtosis_mask(self):
        mask = load_data._get_spectral_kurtosis_mask(HDF5_DATA_FILE_PATH, 
                                                    accumulations = 146484, 
                                                    accumulation_offset = 10)
        assert mask.shape == (90, 14)
        assert mask.dtype == np.bool

    def test_load_tod_data(self):
        ctx = self.ctx.copy()
        ctx.params.integration_time = 1
        ctx.params.integration_frequency = 1
        ctx.params.min_frequency = 900
        ctx.params.max_frequency = 1300
        ctx.params.ref_channel_freq = 1200
        ctx.params.spectrometer = "custom"
        ctx.params.file_type = load_data.FITS_FILE_TYPE
        
        file_paths = [FITS_DATA_FILE_PATH, FITS_DATA_FILE_PATH]
        
        tod = load_data.load_tod(file_paths, ctx)
        
        assert tod.strategy_start is not None
        assert tod.vx is not None
        assert tod.vx.dtype == np.float64
        assert tod.vx.shape == (FREQUENCY_COUNT, (1 / TIME_STEP_SIZE * 15 * 60) * 2)
        assert len(tod.frequencies) == FREQUENCY_COUNT


    def test_call_fits(self):
        ctx = self.ctx.copy()
        ctx.params.integration_time = 1
        ctx.params.integration_frequency = 1
        ctx.params.min_frequency = 900
        ctx.params.max_frequency = 1300
        ctx.params.ref_channel_freq = 1200
        ctx.params.spectrometer = "custom"
        ctx.params.file_type = load_data.FITS_FILE_TYPE
        
        ctx.file_paths = [FITS_DATA_FILE_PATH, FITS_DATA_FILE_PATH]
        
        plugin = load_data.Plugin(ctx)
        plugin()
        
        assert ctx.strategy_start is not None
        assert ctx.tod_vx is not None
        assert ctx.tod_vx.dtype == np.float64
        assert ctx.tod_vx.shape == (FREQUENCY_COUNT, (1 / TIME_STEP_SIZE * 15 * 60) * 2)
        assert len(ctx.frequencies) == FREQUENCY_COUNT
        
        
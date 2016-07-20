# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Feb 26, 2016

author: cchang
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.utils.struct import Struct
from seek.calibration import flux_calibration_transit
import os
import pytest

DATA_PATH = 'res/data'

@pytest.fixture
def ctx():
    params = Struct(telescope_latitude = 47.344192,
                    telescope_longitude = 8.114368,
                    telescope_elevation = 500,
                    integration_time = 10, 
                    integration_frequency = 10, 
                    source_dec = 0.0,
                    calibration_chi1 = 1e10, 
                    calibration_sources = 'CasA', 
                    gain_file_sun = 'data/sun_gain_template.dat')

    ctx = Struct(params=params)
    return ctx

class TestCalibrationTransit(object):

    def test_fit_gaussian_source(self, ctx):   

        data = np.ones((100,200))
        mask = np.zeros((100,200))
        gauss = 1e10*np.exp(-(np.arange(200)-100.0)**2/(2*1.0**2)) + 5.0
        data *= data*gauss
        time_axis = np.arange(200)
        gauss_A = flux_calibration_transit.fit_gaussian_source(data, time_axis, mask, ctx.params.source_dec, ctx.params)
        assert np.allclose(gauss_A, 1e10*np.ones(100))

    def test_fit_sun_to_gain(self, ctx):

        gauss = np.ones((5,100))*1e11
        gauss_amp = np.ma.array(gauss, mask=gauss<=0)
        freq = np.arange(100) + 1000.0
        gain = flux_calibration_transit.fit_sun_to_gain(gauss_amp, freq, ctx.params)
        assert gain[0].shape==(100,2)
        assert np.all(gain[0][:,1]>1e5)

    def test_calibrate(self, ctx):

        current_path = os.path.dirname(__file__)                    
        prefix = os.path.join(current_path, DATA_PATH)
        cal_file = os.path.join(prefix, '2015/05/07/CALIBRATION_RSG_7m_20150507.txt')

        ctx.params.sm_kernel_m = 40
        ctx.params.sm_kernel_n = 20
        ctx.params.sm_sigma_m = 15
        ctx.params.sm_sigma_n = 7.5
        ctx.params.struct_size_0 = 6
        ctx.params.struct_size_1 = 6 
        ctx.params.calibration_sources = 'CasA'
        ctx.params.spectrometer = "M9703A"
        ctx.params.data_file_prefix = "HIMap_RSG7M_A1_24_MP_PXX_Z0_C0-M9703A_DPUA_"
        ctx.params.data_file_suffix = ".h5"
        ctx.params.file_type = "hdf5"
        ctx.params.file_date_format = "%Y%m%d_%H%M%S"
        ctx.params.max_frequency = 1005
        ctx.params.min_frequency = 1000
        ctx.params.ref_channel_freq = 1001
        ctx.params.m9703a_mode = "phase_switch" 
        ctx.params.spectral_kurtosis = False     
        ctx.params.accumulations = 146484  
        ctx.params.accumulation_offset = 10   
        ctx.params.gain_file_default = "data/gain_template_7m_FFT_phase_switch_ADU_K.dat"  

        calibration_file_paths = [os.path.join(prefix, '2015/05/07/HIMap_RSG7M_A1_24_MP_PXX_Z0_C0-M9703A_DPUA_20150507_131404.h5'),
                                  os.path.join(prefix, '2015/05/07/HIMap_RSG7M_A1_24_MP_PXX_Z0_C0-M9703A_DPUA_20150507_171403.h5')]
        ctx.calibrations_paths = {'2015-05-07': (cal_file, calibration_file_paths)}

        gain_file = flux_calibration_transit.calibrate(ctx)
        assert gain_file.shape==(10,2)


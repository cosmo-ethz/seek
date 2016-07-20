'''
Created on Feb 29, 2016

@author: cchang
'''

import numpy as np
from ivy.utils.struct import Struct
from seek.calibration import astro_calibration_source

class TestAstroCalibrationSource(object):
           
    def test_astro_sources(self):

        freq = (np.arange(100) + 1000.0)*1e6
        sun = astro_calibration_source.source("Sun", freq)
        sun_true = astro_calibration_source.benz_sun(freq)/2
        casA = astro_calibration_source.source("CasA", freq)
        F = (0.68 - 0.15*np.log10(freq/1.0e9)*(2015-1970))*0.01
        casA_true = (1.0+F)*astro_calibration_source.barrs77_power_law(freq, 5.88, -0.792, 0.0)/2
        moon = astro_calibration_source.source("Moon", freq)

        assert np.allclose(sun, sun_true)
        assert np.allclose(casA, casA_true)
        assert np.allclose(moon, np.zeros(len(freq)))
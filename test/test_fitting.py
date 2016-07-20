'''
Created on Feb 29, 2016

@author: cchang
'''

import numpy as np
from ivy.utils.struct import Struct
from seek.calibration import fitting

class TestFitting(object):
           
    def test_fitting(self):

        x = np.arange(200)*0.1 - 10.0
        a = 1.0
        x0 = 0.0
        sigma = 2.0
        b = 1.0
        c = 5.0
        gauss = fitting.gauss(x, a, x0, sigma, b, c)
        
        fit_gauss, perr, rsquared = fitting.fit_func(x, gauss, 'gauss', [1.01, 0.0, 2.0, 1.0, 5.01])
        fit_gauss_true = np.array([a,x0,sigma,b,c])
        assert np.allclose(fit_gauss, fit_gauss_true)
        assert rsquared == 1
        
        a_1 = 2.0
        x0_1 = 0.0
        sigma_1 = 2.0
        a_2 = 1.0
        x0_2 = 2.0
        sigma_2 = 1.0
        b = 1.0
        c = 5.0
        gauss2 = fitting.gauss2(x, a_1, x0_1, sigma_1, a_2, x0_2, sigma_2, b, c)
        
        fit_gauss2, perr, rsquared = fitting.fit_func(x, gauss2, 'gauss2', [2.01, 0.0, 2.0, 1.0, 2.0, 1.0, 1.0, 5.01])
        fit_gauss2_true = np.array([a_1,x0_1,sigma_1,a_2,x0_2,sigma_2,b,c])
        assert np.allclose(fit_gauss2, fit_gauss2_true)
        assert rsquared == 1


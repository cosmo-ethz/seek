# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Aug 18, 2015

author: cchang

'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from scipy.optimize import curve_fit
import hope

@hope.jit
def gauss(x, a, x0, sigma, b, c):
    """
    Gaussian model plus a linear background.
    """
    if a>0:
        return a * np.exp(-(x - x0)**2 / (2 * sigma**2)) + b * x + c
    else:
        return 1e30 * x

def gauss2(x, a_1, x0_1, sigma_1, a_2, x0_2, sigma_2, b, c):
    """
    Double Gaussian model plus a linear background.
    """
    if a_1>0 and a_2>0:
        return a_1 * np.exp(-(x - x0_1)**2 / (2 * sigma_1**2)) + a_2 * np.exp(-(x - x0_2)**2 / (2 * sigma_2**2)) + b * x + c
    else:
        return 1e30

FUNCTION_MAP = dict(gauss=gauss,
                    gauss2=gauss2
                    )

def fit_func(x, y, func_name, p0):
    """
    Fit different functions to curve. The current choices for functions
    are single or double Gaussians plus a linear background.
    """
    try:
        func = FUNCTION_MAP[func_name]
        fit, pcov = curve_fit(func, x, y, p0=p0)
        perr = np.sqrt(np.diag(pcov))
        residuals = y - func(x, *fit)
        ss_err = (residuals**2).sum()
        ss_tot = ((y - y.mean())**2).sum()
        rsquared = 1 - (ss_err / ss_tot)
    except RuntimeError:
        fit = np.zeros(len(p0))
        perr = np.zeros(len(p0))
        rsquared = 0
    
    return fit, perr, rsquared


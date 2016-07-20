# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Aug 18, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

import hope

def get_empty_mask(shape):
    mask = np.empty(shape, dtype=np.bool)
    mask[:] = False
    return mask
    
def smooth(tod, factor, axis = 1):
    """
    Smoothes a tod by the given factor. E.g. (axis=1)::
    
    [[1,1,2,2,3,3], -- factor 2 --> [[1,2,3],
    [4,4,5,5,6,6]]                  [4,5,6]]

    :param tod: the data to be smoothed
    :param factor: the factor to use for the integration
    """
    m,n = tod.shape
    if axis==0:
        nnew = m // factor
        smooth_tod = tod[:nnew*factor].reshape(nnew, factor, n)
        return smooth_tod.mean(axis = 1)
    else:        
        nnew = n // factor
        smooth_tod = tod[:, :nnew*factor].reshape(m, nnew, factor)
        return smooth_tod.mean(axis = 2)

@hope.jit
def spectral_kurtosis(p, p2, M, offset):
    """
    Computes the spectral kurtosis for the given P and P^2 values

    :param p: array of P values
    :param p2: array of P^2 values
    :param M: number of accumulations
    :param offset: P_select 0
    
    :returns SK: array with the spectral kurtosis values
    """
    S1 = p
    S2 = 2**(2 * offset) * p2
    return (M + 1) / (M - 1) * (-1 + (M * S2) / S1**2)

def spectral_kurtosis_mask(p_phase0, p_phase1, p2_phase0, p2_phase1, M, offset):
    """
    Creates a mask using the spectral kurtosis for the given arrays

    :param p_phase0: array of P values for phase0
    :param p_phase1: array of P values for phase1
    :param p2_phase0: array of P^2 values for phase0
    :param p2_phase1: array of P^2 values for phase1
    :param M: number of accumulations
    :param offset: P_select 0
    
    :returns mask: boolean array containing the mask
    """
    SK1 = spectral_kurtosis(p_phase0, p2_phase0, M, offset)
    SK2 = spectral_kurtosis(p_phase1, p2_phase1, M, offset)    
    mask = (1 < SK1) + (1 < SK2)
    return mask


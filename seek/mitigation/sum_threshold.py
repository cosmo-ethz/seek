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
Created on Jan 21, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from scipy import ndimage

import hope

from seek.mitigation import sum_threshold_utils
from seek.utils.tod_utils import get_empty_mask
from seek.utils import filter

# Maximum neighbourhood size
MAX_PIXELS = 8

# smoothing default params
KERNEL_M = 40
KERNEL_N = 20
SIGMA_M = 7.5
SIGMA_N = 15

# dilation default params
STRUCT_SIZE = 3


@hope.jit
def _sumthreshold(data, mask, i, chi, ds0, ds1):
    """
    The operation of summing and thresholding.

    :param data: data
    :param mask: original mask
    :param i: number of iterations
    :param chi: thresholding criteria
    :param ds0: dimension of the first axis
    :param ds1: dimension of hte second axis

    :return: SumThredshold mask
    """
    tmp_mask = mask[:]
    for x in range(ds0):
        sum = 0.0
        cnt = 0
        
        for ii in range(0, i):
            if mask[x, ii] != True:
                sum += data[x, ii]
                cnt += 1
        
        for y in range(i, ds1):
            if sum > chi * cnt:
                for ii2 in range(0, i):
                    tmp_mask[x, y-ii2-1] = True
                    
            if mask[x, y] != True:
                sum += data[x, y]
                cnt += 1
            
            if mask[x, y-i] != 1:
                sum -= data[x, y-i]
                cnt -= 1
                
    return tmp_mask

def _run_sumthreshold(data, init_mask, eta, M, chi_i, sm_kwargs, plotting=True):
    """
    Perform one SumThreshold operation: sum the un-masked data after
    subtracting a smooth background and threshold it.

    :param data: data
    :param init_mask: initial mask
    :param eta: number that scales the chi value for each iteration
    :param M: number of iterations
    :param chi: thresholding criteria
    :param sm_kwargs: smoothing keyword
    :param plotting: whether to plot

    :return: SumThreshold mask

    """

    smoothed_data = filter.gaussian_filter(data, init_mask, **sm_kwargs)
    res = data-smoothed_data
    
    st_mask = init_mask.copy()

    for m, chi in zip(M, chi_i):
        chi = chi / eta
        if m==1:
            st_mask = st_mask | (chi<=res)
        else:
            st_mask = _sumthreshold(res,   st_mask,   m, chi, *res.shape)
            st_mask = _sumthreshold(res.T, st_mask.T, m, chi, *res.T.shape).T

    if plotting:
        sum_threshold_utils.plot_steps(data, st_mask, smoothed_data, res, "%s (%s)"%(eta, chi_i))
        
    return st_mask

def binary_mask_dilation(mask, struct_size_0, struct_size_1):
    """
    Dilates the mask.

    :param mask: original mask
    :param struct_size_0: dilation parameter
    :param struct_size_1: dilation parameter

    :return: dilated mask
    """
    struct = np.ones((struct_size_0, struct_size_1), np.bool)
    return ndimage.binary_dilation(mask, structure=struct, iterations=2)


def normalize(data, mask):
    """
    Simple normalization of standing waves: subtracting the median over time
    for each frequency.

    :param data: data
    :param mask: mask

    :return: normalized data
    """
    median = np.ma.median(np.ma.MaskedArray(data, mask), axis=1).reshape(data.shape[0], -1)
    data = np.abs(data - median)
    return data.data

def get_rfi_mask(tod, mask=None, chi_1=35000, eta_i=[0.5, 0.55, 0.62, 0.75, 1], normalize_standing_waves=True, suppress_dilation=False, plotting=True, sm_kwargs=None, di_kwargs=None):
    """
    Computes a mask to cover the RFI in a data set.
    
    :param data: array containing the signal and RFI
    :param mask: the initial mask
    :param chi_1: First threshold
    :param eta_i: List of sensitivities  
    :param normalize_standing_waves: whether to normalize standing waves
    :param suppress_dilation: if true, mask dilation is suppressed
    :param plotting: True if statistics plot should be displayed
    :param sm_kwargs: smoothing key words
    :param di_kwargs: dilation key words
    
    :return mask: the mask covering the identified RFI
    """
    data = tod.data
    
    if mask is None:
        mask = get_empty_mask(data.shape)
    
    if sm_kwargs is None: sm_kwargs = get_sm_kwargs()
    
    if plotting: sum_threshold_utils.plot_moments(data)

    if normalize_standing_waves:
        data = normalize(data, mask)

        if plotting: sum_threshold_utils.plot_moments(data)
    
    p = 1.5
    m = np.arange(1, MAX_PIXELS)
    M = 2**(m-1)
    chi_i = chi_1 / p**np.log2(m)

    st_mask = mask
    for eta in eta_i:
        st_mask = _run_sumthreshold(data, st_mask, eta, M, chi_i, sm_kwargs, plotting)

    dilated_mask = st_mask
    if not suppress_dilation:
        if di_kwargs is None: di_kwargs = get_di_kwrags()

        dilated_mask = binary_mask_dilation(dilated_mask - mask, **di_kwargs)
    
        if plotting: sum_threshold_utils.plot_dilation(st_mask, mask, dilated_mask)
        
    return dilated_mask+mask

def get_sm_kwargs(kernel_m=KERNEL_M, kernel_n=KERNEL_N, sigma_m=SIGMA_M, sigma_n=SIGMA_N):
    """
    Creates a dict with the smoothing keywords.

    :param kernel_m: kernel window size in axis=1
    :param kernel_n: kernel window size in axis=0
    :param sigma_m: kernel sigma in axis=1
    :param sigma_n: kernel sigma in axis=0

    :return: dictionary with the smoothing keywords
    """
    return dict(M=kernel_m, N=kernel_n, sigma_m=sigma_m, sigma_n=sigma_n)

def get_di_kwrags(struct_size_0=STRUCT_SIZE, struct_size_1=STRUCT_SIZE):
    """
    Creates a dict with the dilation keywords.

    :param struct_size_0: struct size in axis=0
    :param struct_size_1: struct size in axis=1

    :return: dictionary with the dilation keywords
    """
    return dict(struct_size_0=struct_size_0, struct_size_1=struct_size_1)

def get_sumthreshold_kwargs(params):
    """
    Creates the smoothing and dilation kwargs from a params objects.

    :param params: the params object containing the configuration 

    :return: smoothing and dilation kwargs
    """
    sm_kwargs = get_sm_kwargs(params.sm_kernel_m,
                              params.sm_kernel_n,
                              params.sm_sigma_m,
                              params.sm_sigma_n,)

    di_kwargs = get_di_kwrags(params.struct_size_0, params.struct_size_1)
    
    return sm_kwargs, di_kwargs

def rm_rfi(ctx):
    """
    Call the main SumThreshold routine.

    :param ctx: context

    :return: SumThreshold RFI mask.
    """
    sm_kwars, di_kwargs = get_sumthreshold_kwargs(ctx.params)
    
    rfi_mask_vx = get_rfi_mask(ctx.tod_vx, 
                               mask=ctx.tod_vx.mask,
                               chi_1 = ctx.params.chi_1,
                               eta_i=ctx.params.eta_i,
                               plotting=False,
                               sm_kwargs=sm_kwars,
                               di_kwargs=di_kwargs)

    return rfi_mask_vx, rfi_mask_vx

# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Jan 22, 2015

author: seehars
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from numpy import std, mean, bitwise_or

def rm_rfi(ctx):
    """
    Remove RFI by outlier rejection of a number of measurements in
    the same healpix pixel.

    :param ctx: context

    :return: outlier mask
    """

    rfi_mask_vx = getMask(ctx.tod_vx, ctx.params.multiplicator)
    rfi_mask_vy = getMask(ctx.tod_vy, ctx.params.multiplicator)

    return rfi_mask_vx, rfi_mask_vy

def getMask(tod, multiplicator):
    """
    Construct outlier mask based on user-specified rejection criterion.

    :param tod: TOD
    :param multiplicator: the number of standard deviation from the mean
     beyond which the data point is considered an outlier

    :return: outlier mask
    """
    std_time = std(tod, axis=0)
    mean_time = mean(tod, axis=0)
    std_frequency = std(tod, axis=1)
    mean_frequency = mean(tod, axis=1)

    mask = tod > (multiplicator * std_time + mean_time)
    return bitwise_or(mask, tod > multiplicator * std_frequency + mean_frequency)
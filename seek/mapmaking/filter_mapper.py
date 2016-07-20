# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Feb 26, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

def get_mapped_values(data, ctx):
    """
    Maps the data by removing outliers and then computing the median per pixel.
    Follows http://stackoverflow.com/a/16562028/4067032
    :param data: data in the restructured form after create_maps.py
    :param ctx: context

    :return: median and sum of all the un-masked data in each healpix pixel
    """
    
    filtered = filter_data(data)
    
    return np.ma.median(filtered, axis=1), np.sum(~filtered.mask, axis=1)

def filter_data(data):
    """
    remove outliers in data array.

    :param data: data in the restructured form after create_maps.py

    :return: data with outlier removed
    """
    m=2
    d = np.abs(data - np.ma.median(data, axis=1)[:, np.newaxis])
    mdev = np.ma.median(d, axis=1)[:, np.newaxis]
    s = d/mdev
    filtered = np.ma.array(data, mask=[s>m])
    return filtered
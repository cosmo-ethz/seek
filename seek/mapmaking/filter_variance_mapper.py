# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Feb 26, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from seek.mapmaking import filter_mapper

def get_mapped_values(data, ctx):
    """
    Maps the data by removing outliers and then computing the variance per pixel.
    :param data: data in the restructured form after create_maps.py
    :param ctx: context

    :return: variance and sum of unmasked map
    """
    
    filtered = filter_mapper.filter_data(data)
    return np.ma.var(filtered, axis=1), np.sum(~filtered.mask, axis=1)


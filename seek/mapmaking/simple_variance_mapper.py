# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Feb 26, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

def get_mapped_values(re_data, ctx):
    """
    Maps the data by simply computing the variance per pixel
    :param re_data: data in the restructured form after create_maps.py

    :return: variance and sum of unmasked data
    """
    
    return re_data.var(axis=1), np.sum(~re_data.mask, axis=1)
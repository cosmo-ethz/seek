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


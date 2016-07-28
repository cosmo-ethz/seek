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
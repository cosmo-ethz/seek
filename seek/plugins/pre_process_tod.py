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
Created on Jan 20, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.plugin.base_plugin import BasePlugin

import numpy as np

SPECTROMETER_CALLISTO = 'callisto'
SPECTROMETER_M9703A = 'M9703A'


def apply_gain(frequencies, data, gain_file):
    """
    Converts the digits into kelvins using a gain template
    
    :param frequencies: the frequencies of the data
    :param data: array containing the data [freq, time]
    
    :returns data: the converted data
    """
    freq = gain_file[:,0]
    gain = gain_file[:,1]
    
    tod_gain = np.interp(frequencies, freq, gain).reshape(-1, 1)
    
    return 1. / tod_gain * data

class Plugin(BasePlugin):
    """
    Converts the TOD's depending on the spectrometer
    """

    def __call__(self):
        try:
            data = apply_gain(self.ctx.frequencies, self.ctx.tod_vx, self.ctx.gain_file)
            self.ctx.tod_vx = np.ma.array(data, mask=self.ctx.tod_vx.mask)

            data = apply_gain(self.ctx.frequencies, self.ctx.tod_vy, self.ctx.gain_file)
            self.ctx.tod_vy = np.ma.array(data, mask=self.ctx.tod_vy.mask)

        except KeyError:
            pass

    def __str__(self):
        return "Convert TOD"


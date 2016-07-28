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
Created on Feb 4, 2016

author: cchang
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.plugin.base_plugin import BasePlugin
from seek.calibration import flux_calibration_transit
from seek.utils import load_file

class Plugin(BasePlugin):
    """ This class is used to specify which calibration type
    to use. If the case "data" is specified, derive gain curve
    from separate module in calibration directory."""

    def __call__(self):
        
        if self.ctx.params.flux_calibration=='default':
            self.ctx.gain_file = load_file(self.ctx.params.gain_file_default)

        if self.ctx.params.flux_calibration=='flat':
            self.ctx.gain_file = load_file(self.ctx.params.gain_file_flat)

        if self.ctx.params.flux_calibration=='data':
            self.ctx.gain_file = flux_calibration_transit.calibrate(self.ctx)
            
    def __str__(self):
        return "Generate gain files"
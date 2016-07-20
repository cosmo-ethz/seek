# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

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
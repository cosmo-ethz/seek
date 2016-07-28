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
Created on Dec 8, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from pkg_resources import resource_filename
from ivy.plugin.base_plugin import BasePlugin
import numpy as np
import healpy as hp

import seek


class Plugin(BasePlugin):
    """
    Read in healpix mask from GSM if 'smooth' background model is specified.
    """

    def __call__(self):
        if self.ctx.params.background_model == "smooth":
            self.ctx.simulation_mask = hp.read_map(resource_filename(seek.__name__, self.ctx.params.gsm_mask),
                                                   dtype=np.bool, verbose=False)

    def __str__(self):
        return "Initialize"

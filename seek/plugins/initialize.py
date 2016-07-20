# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

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

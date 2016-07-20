# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Jun 6, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

from ivy.plugin.base_plugin import BasePlugin
from seek.utils import parse_datetime
from seek import utils


class Plugin(BasePlugin):
    """
    First masks given frequency ranges that are known to be
    RFI-contaminatedm. Next masks artefacts based on a custom file
    in the data directory.
    """

    def __call__(self):
        self.mask_frequencies()
        self.mask_artefacts()
        
        
    def mask_frequencies(self):
        """
        Mask bad frequency channels.

        :return: mask after specified frequencies are masked.
        """
        for freqs in self.ctx.params.mask_freqs:
            idx0 = np.searchsorted(self.ctx.frequencies, freqs[0])
            idx1 = np.searchsorted(self.ctx.frequencies, freqs[1])
            self.ctx.tod_vx.mask[idx0:idx1] = True


    def mask_artefacts(self):
        """
        Mask artefacts.

        :return: mask after specified artefacts are masked.
        """
        date = self.ctx.strategy_start
        artefacts = utils.load_file(self.ctx.params.artefacts_file, dtype="S", delimiter=", ")
        
        for artefact_date, start, end in artefacts:
            artefact_start_date = parse_datetime("%s-%s:00"%(artefact_date, start))
            artefact_end_date = parse_datetime("%s-%s:59"%(artefact_date, end))
            
            if date.date() == artefact_start_date.date():
                start_date_in_h = artefact_start_date.hour + artefact_start_date.minute / 60 + artefact_start_date.second / 3600
                end_date_in_h = artefact_end_date.hour + artefact_end_date.minute / 60 + artefact_end_date.second / 3600
                
                idx0 = np.searchsorted(self.ctx.time_axis, start_date_in_h)
                idx1 = np.searchsorted(self.ctx.time_axis, end_date_in_h)
                self.ctx.tod_vx.mask[:, idx0:idx1] = True
                
    def __str__(self):
        return "Masking artefacts"
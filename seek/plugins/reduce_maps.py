# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Feb 3, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import healpy as hp
import os

class Plugin(object):
    """
    Aggregates the partial maps to one complete healpy map.
    """

    def __init__(self, ctx):
        self.ctx = ctx
    
    def reduce(self, ctxList):
        npix = hp.nside2npix(self.ctx.params.nside)
        nfreq = ctxList[-1].frequencies.shape[0]
        
        healpy_maps = np.zeros((nfreq, 2, npix))
        healpy_counts = np.zeros(healpy_maps.shape)
        
        for ctx in ctxList:
            idxs = ctx.map_idxs
            healpy_maps[:,:, idxs] = ctx.maps
            healpy_counts[:,:, idxs] = ctx.counts
        
        self.ctx.maps = healpy_maps
        self.ctx.counts = healpy_counts
        self.ctx.redshifts = ctxList[-1].redshifts
        
        for path in ctxList[-1].tod_paths:
            try:
                os.remove(path)
            except: pass
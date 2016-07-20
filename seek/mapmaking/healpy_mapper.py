# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Jan 5, 2015

author: seehars
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import healpy as hp

def get_map(ctx):
    """
    Function for creating maps from TOD by a simple averaging in healpy
    pixels.
    :param ctx: context that contains TOD, frequencies, coordinate
    information, and an RFI mask
    """
    npix = hp.nside2npix(ctx.params.nside)
    nfreq = ctx.frequencies.shape[0]
    theta, phi = eq2rad(ctx.coords.ra, ctx.coords.dec) 
    inds = hp.ang2pix(ctx.params.nside, theta, phi)
    
    maps = np.zeros((nfreq, 2, npix))
    counts = np.zeros(maps.shape)
    varflag = ctx.params.variance
    
    varmaps = np.zeros((nfreq, 2, npix)) if varflag else None
    
    for tod_ind in range(min(theta.shape[0], ctx.tod_vx.shape[1])):
        ind = inds[tod_ind]
        updateMaps(ctx.tod_vx, maps, counts, tod_ind, ind, 0, varmaps)
        updateMaps(ctx.tod_vy, maps, counts, tod_ind, ind, 1, varmaps)            
            
    redshifts = 1420.40575177 / ctx.frequencies - 1
    return_maps = varmaps if varflag else maps * counts
    return return_maps, redshifts, counts

def updateMaps(tod, maps, counts, tod_ind, map_ind, xy_ind, varmaps = None):
    """
    Running update of map as more data is included.

    :param tod: TOD that is added to the map
    :param maps: the map that is being updated
    :param counts: number of measurements per pixel
    :param tod_ind: index for TOD pixel
    :param map_ind: index for healpix pixel
    :param xy_ind: polarization index
    :param varmaps: variance map

    :return: updated map and variance map
    """
    m = ~(tod.mask[:, tod_ind])
    counts[m, xy_ind, map_ind] += 1.0
    tmpMaps = maps[m, xy_ind, map_ind].copy()
    maps[m, xy_ind, map_ind] += ((tod.data[m, tod_ind] - tmpMaps) /
                                 counts[m, xy_ind, map_ind])
    if varmaps is None:
        return maps
    else:
        p1 = tod.data[m, tod_ind] - tmpMaps
        p2 = tod.data[m, tod_ind] - maps[m, xy_ind, map_ind]
        varmaps[m, xy_ind, map_ind] += p1 * p2
        return maps, varmaps

def eq2rad(ra, dec):
    """
    Convert RA/DEC coordinates to theta/phi used in healpix

    :param ra: RA coordinate
    :param dec:  DEC coordinate

    :return: theta/phi coordinate
    """
    theta = np.pi * .5  - dec
    phi = ra
    return theta, phi

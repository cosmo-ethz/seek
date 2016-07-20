# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Feb 6, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

from ivy.plugin.base_plugin import BasePlugin
from datetime import datetime
from datetime import timedelta
from seek.utils import sphere
from seek.utils import parse_datetime
from seek import utils

try:
    import ephem as ephem
except ImportError:
    ephem = None
    

EPHEM_DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

def get_object_separation(obs, start_date, time, ra, dec):
    """
    Get separation between the Sun/Moon and the RA/DEC of a pixel.

    :param obs: pyephem observer
    :param start_date: date
    :param time: time axis of TOD
    :param ra: RA for TOD
    :param dec: DEC for TOD

    :return: separation of the TOD positions with the Sun and the Moon
    """
    sun_separation = []
    moon_separation = []
    for (t, ra, dec) in zip(time, ra, dec):
        date = start_date + timedelta(hours=t)
        obs.date = datetime.strftime(date, EPHEM_DATE_FORMAT)
        sun = ephem.Sun()
        moon = ephem.Moon(obs)
        sun.compute(obs)
        moon.compute(obs)
        sun_separation.append(ephem.separation(sun, (ra, dec)))
        moon_separation.append(ephem.separation(moon, (ra, dec)))
        
    return np.array(sun_separation),  np.array(moon_separation)

class Plugin(BasePlugin):
    """
    Masks the Sun and the Moon using ephem.
    """

    def __call__(self):
        self.mask_objects()
        
        
    def mask_objects(self):
        obs = sphere.get_observer(self.ctx.params)

        # loop over the files to mask according to position of sun/moon 
        # at time of the beginning of each file
        start_date = datetime(self.ctx.strategy_start.year, self.ctx.strategy_start.month, self.ctx.strategy_start.day)
        
        sun_separation, moon_separation = get_object_separation(obs, 
                                                                start_date, 
                                                                self.ctx.coords.t, 
                                                                self.ctx.coords.ra, 
                                                                self.ctx.coords.dec)
        
        # ra/dec can be nan due to being out of the interpolation boundaries, mask them out for now
        nan_mask_idx = np.isnan(sun_separation)
        sun_separation[nan_mask_idx] = 100
        moon_separation[nan_mask_idx] = 100

        sun_mask_idx = sun_separation <= np.radians(self.ctx.params.min_sun_separation)
        
        obs.date = datetime.strftime(start_date, EPHEM_DATE_FORMAT)
        moon = ephem.Moon(obs)
        moon.compute(obs)
        moon_mask_idx = (moon_separation < np.radians(self.ctx.params.min_moon_separation)) | ((moon_separation < np.radians(self.ctx.params.min_moon_phase_separation)) * (moon.phase > self.ctx.params.min_moon_high_phase))
        
        if np.any(sun_mask_idx==True):
            if self.ctx.params.verbose:
                print("Sun", start_date, sun_mask_idx.sum())
            self.ctx.tod_vx.mask[:, sun_mask_idx] = True
            self.ctx.tod_vy.mask[:, sun_mask_idx] = True
        if np.any(moon_mask_idx==True):
            if self.ctx.params.verbose:
                print("Moon", start_date, moon_mask_idx.sum())
            self.ctx.tod_vx.mask[:, moon_mask_idx] = True
            self.ctx.tod_vy.mask[:, moon_mask_idx] = True
        
        if np.any(nan_mask_idx==True):
            if self.ctx.params.verbose:
                print("Nan", start_date, nan_mask_idx.sum())
            self.ctx.tod_vx.mask[:, nan_mask_idx] = True
            self.ctx.tod_vy.mask[:, nan_mask_idx] = True
            self.ctx.coords.ra[nan_mask_idx] = -1
            self.ctx.coords.dec[nan_mask_idx] = -1
            
    def __str__(self):
        return "Masking objects"
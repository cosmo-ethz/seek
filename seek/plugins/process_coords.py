# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Jul 28, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.plugin.base_plugin import BasePlugin
from datetime import timedelta

import numpy as np
from datetime import datetime

from seek import Coords
from seek.utils import format_date
from seek.utils import sphere

EPS = 1e-5


def convert_coords(date, time_steps, azs, els, obs):
    """
    Convert the time/az/ele coordinates to RA/DEC.

    :param date: date
    :param time_steps: time interval between two TOD pixels
    :param azs: Azimuth coordinate
    :param els: Elevation coordinate
    :param obs: pyephem observer

    :return: RA/DEC array corresponding to TOD
    """
    coord_start_day = datetime(date.year, date.month, date.day)
    
    strategy = []
    for time_step, az, el in zip(time_steps, azs, els):
        if az % np.pi == 0.0: 
            az += EPS
            
        ra, dec = sphere.altaz_to_ra_dec(coord_start_day + timedelta(hours=time_step), az, el, obs)
        strategy.append([ra, dec])
        
    return np.array(strategy)

class Plugin(BasePlugin):
    """
    Loads the telescope coordinate file for the current observation date and
    converts AZ/EL to RA/DEC.
    """
    
    def __call__(self):
        if self.ctx.tod_vx.shape[0] > 0:
            date = self.ctx.strategy_start
            coord_path = self.ctx.coords_paths[format_date(date)]
            coords = np.genfromtxt(coord_path, delimiter = ',', names = True)
            time_axis = self.ctx.time_axis
            
            azs = np.radians(np.interp(time_axis, coords['Time'], coords['AzAntenna']))
            els = np.radians(np.interp(time_axis, coords['Time'], coords['ElAntenna']))
            
            obs = sphere.get_observer(self.ctx.params)
            
            strategy = convert_coords(date, time_axis, azs, els,obs)
            
            self.ctx.coords = Coords(strategy[:, 0], strategy[:, 1], azs, els, time_axis)
        else:
            self.ctx.coords = Coords([], [], [], [], [])
        
    def __str__(self):
        return "Process coordinates"
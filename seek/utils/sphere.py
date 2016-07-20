# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Dec 22, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import ephem

def get_observer(params):
    """
    Define pyephem observer.

    :param params: telescope parameters from context

    :return: pyephem observer
    """
    
    obs = ephem.Observer()
    obs.lon = str(params.telescope_longitude)
    obs.lat = str(params.telescope_latitude)
    obs.elevation = params.telescope_elevation
    obs.pressure = 0
    return obs

def altaz_to_ra_dec(date, az, alt, obs=None, params=None):
    """
    Convert Azimuth/Elevation/time to RA/DEC coordinates.

    :param date: date and time
    :param az: Azimuth coordinate
    :param alt: Elevation coordinate
    :param obs: pyephem observer
    :param params: context parameters

    :return: RA/DEC coordinates
    """
    
    if obs is None:
        obs = get_observer(params)
    obs.date = (date.year, date.month, date.day, date.hour, date.minute, date.second)
    
    return obs.radec_of(az, alt)


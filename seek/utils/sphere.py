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


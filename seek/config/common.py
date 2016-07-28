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
Created on Jan 5, 2015

author: seehars

Common parameters that are always loaded.

'''

# ==================================================================
# G E N E R A L
# ==================================================================
verbose = False

#seeds
seed = 1


map_name = "BGS_maps.hdf"

overwrite = False                  # True if file should be overwritten 

# ==================================================================
# T E L E S C O P E
# ==================================================================
telescope_latitude = 47.3412278
telescope_longitude = 8.112215

telescope_elevation = 500

# ==================================================================
# D A T A  L O A D I N G
# ==================================================================
file_prefix = "./"

integration_time = 1                # no of pixel to use for integration in time (axis=1)
integration_frequency = 1           # no of pixel to use for integration in freq (axis=0)
data_file_prefix = "SKYMAP_"        # First part of fit file name
data_file_suffix = ".hdf"           # Suffix of file name
file_date_format = "{0}%Y-%m-%d-%H:%M:%S{1}" # Format of date part of file name
min_frequency = 980                 # minimum frequency to use
max_frequency = 1306                # maximum frequency to use


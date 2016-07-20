# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Jan 23, 2015

author: seehars

Config file that specifies the Ivy workflow and other parameters used
to run SEEK.

'''
from __future__ import print_function, division, absolute_import, unicode_literals

from ivy.plugin.parallel_plugin_collection import ParallelPluginCollection

plugins = ["seek.plugins.find_nested_files",
           "seek.plugins.calibration",
            "seek.plugins.initialize",
# comment out everything below when doing calibration-only analysis
           ParallelPluginCollection([
#                                     "seek.plugins.load_preprocessed_data",
                                    "seek.plugins.load_data",
                                    "seek.plugins.pre_process_tod",
                                    "seek.plugins.process_coords",
                                    "seek.plugins.mask_objects",
                                    "seek.plugins.mask_artefacts",
                                    "seek.plugins.remove_RFI",
                                    "seek.plugins.post_process_tod",
                                    "seek.plugins.background_removal",
                                    "seek.plugins.restructure_tod",
                                     ],
                                     "seek.plugins.map_file_paths",
                                     "seek.plugins.reduce_map_indicies"
                                     ),
            ParallelPluginCollection(["seek.plugins.create_maps"],
                                     "seek.plugins.map_indicies",
                                     "seek.plugins.reduce_maps"),
            "seek.plugins.write_maps",
            "ivy.plugin.show_stats",
            ]

from seek.config import common

for name in [name for name in dir(common) if not name.startswith("__")]:
    globals()[name] = getattr(common, name)

backend = "sequential"
cpu_count = 1


# ==================================================================
# F I L E   I N P U T
# ==================================================================
strategy_start = "2015-12-14-00:00:00"      # survey start time. Format YYYY-mm-dd-HH:MM:SS
strategy_end   = "2016-05-28-23:59:00"      # survey end time. Format YYYY-mm-dd-HH:MM:SS

spectrometer = "callisto"
data_file_prefix = "HIMap_"                 # First part of fit file name
data_file_suffix = "_03.fit(.gz)?"          # Suffix of file name
file_date_format = "%Y%m%d_%H%M%S"          # Format of date part of file name
file_type = "fits"
ref_channel_freq = 1269.97                  # frequency of the reference channel
integration_time = 24                       # no of pixel to use for integration in time (axis=1)
integration_frequency = 1                   # no of pixel to use for integration in freq (axis=0)

coord_prefix = "coord7m"                    # prefix of coord file

chunk_size = 100                              # number of files to be grouped together


# ==================================================================
# R F I  C L E A N I N G
# ==================================================================
cleaner = "seek.mitigation.sum_threshold"

# ---------------------------
# F R E Q U E N C Y   M A S K I N G 
# ---------------------------
mask_freqs = ()                             # list of frequency ranges to be masked

# ---------------------------
# S u m   t h r e s h o l d 
# ---------------------------
chi_1 = 35000                                # First threshold value 
sm_kernel_m = 40                            # Smoothing, kernel window size in axis=1
sm_kernel_n = 20                            # Smoothing, kernel window size in axis=0
sm_sigma_m = 15                             # Smoothing, kernel sigma in axis=1
sm_sigma_n = 7.5                            # Smoothing, kernel sigma in axis=0

struct_size_0 = 1                           # size of struct for dilation on freq direction [pixels]
struct_size_1 = 6                           # size of struct for dilation on time direction [pixels]

eta_i = [0.5, 0.55, 0.62, 0.75, 1]

# ==================================================================
# C A L I B R A T I O N
# ==================================================================
flux_calibration = "default"                   # calibration mode, options: default, flat, data
gain_file_default = "data/gain_template_7m_callisto_phase_switch_ADU_K.dat"
gain_file_sun = "data/sun_gain_template.dat"
calibration_sources = 'CasA' 
calibration_chi1 = 1e6 

# -------------------------------
# R E F R E N C E   C H A N N E L
# -------------------------------
# calibrator = "seek.calibration.reference_channel"
# ref_ids = [194, 195, 196]
# baselines = [0.0, 0.0, 0.0]

# -------------------------------
# B A C K G R O U N D   M O D E L
# -------------------------------
background_model = "median" # or smooth
gsm_mask = 'data/1k_gsm_990_mask.fits' # this is GSM at 990 MHz, at 1K for the single polarization


# ==================================================================
# M A P  M A K I N G
# ==================================================================
map_maker = "seek.mapmaking.filter_mapper"

nside = 64
variance = False

# ==================================================================
# M A S K I N G
# ==================================================================
min_sun_separation = 15               # minimum separation form pointing to sun [deg]
min_moon_separation = 5               # minimum separation form pointing to moon [deg]
min_moon_phase_separation = 10        # minimum separation form pointing to moon during high phase [deg]
min_moon_high_phase = 80              # minimum phase of moon to switch to min_moon_phase_separation

artefacts_file = "data/masking_dates.txt" #file storing dates and times to mask

# ==================================================================
# P O S T P R O C E S S I N G
# ==================================================================
store_intermediate_result = True    # Flag if data, mask etc should be written to file
post_processing_prefix =".cache"         # Prefix used
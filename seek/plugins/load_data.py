# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Jul 28, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import os
from collections import namedtuple

from ivy.plugin.base_plugin import BasePlugin

import numpy as np
from numpy import ma
from astropy.io import fits
import h5py

from seek.utils import parse_datetime
from seek.utils.tod_utils import smooth
from seek.utils.tod_utils import get_empty_mask
from seek.utils.tod_utils import spectral_kurtosis_mask

FREQUENCIES_KEY = "FREQUENCY"
TIME_KEY = "TIME"
P_PHASE0_KEY = "P/Phase0"
P_PHASE1_KEY = "P/Phase1"
MODE_PHASE_SWITCH = "phase_switch"
MODE_TOTAL_POWER = "total_power"

SPECTROMETER_M9703A = 'M9703A'
FITS_FILE_TYPE = 'fits'
HDF5_FILE_TYPE = 'hdf5'

TimeOrderedData = namedtuple("TimeOrderedData", ["strategy_start", "frequencies", "time_axis", "vx", "vy", "ref_channel"])


def get_observation_start(path, file_type):
    """
    Extracts the observation date
    
    :param path: path to the file
    
    :returns observation_start: datetime object with the date
    """
    
    if file_type == FITS_FILE_TYPE:
        observation_start = get_observation_start_from_fits(path)
    elif file_type == HDF5_FILE_TYPE:
        observation_start = get_observation_start_from_hdf5(path)
    else:
        raise TypeError("Unsupported file type: '%s'"%file_type)

    return observation_start


def get_observation_start_from_fits(path):
    """
    Extracts the observation date
    
    :param path: path to the file
    
    :returns observation_start: datetime object with the date
    """
    with fits.open(path, mode='readonly', memmap=False) as hdu:
        primary = hdu[0]
        date_format = "%Y/%m/%d-%H:%M:%S"
        observation_start = primary.header["DATE-OBS"] + "-" + primary.header["TIME-OBS"][:-4]
        observation_start = parse_datetime(observation_start, date_format)
        del hdu[0].data

    return observation_start

def get_observation_start_from_hdf5(path):
    """
    Extracts the observation date
    
    :param path: path to the file
    
    :returns observation_start: datetime object with the date
    """
    file_name = os.path.basename(path)
    datelen = 15 #yyyymmdd_hhmmss
    name = file_name.split(".")[0] 
    date = name[-datelen:]
    return parse_datetime(date, "%Y%m%d_%H%M%S")

def load_tod(file_paths, ctx):
    """
    Load the time ordered data from the given file paths
    :param file_paths: list of absolute file paths pointing to the data files
    :param ctx: Context object with the configuration
    
    :returns TimeOrderedData: returns a TimeOrderedData namedtupel
    """
    min_frequency = ctx.params.min_frequency
    max_frequency = ctx.params.max_frequency
    assert min_frequency <= max_frequency
    
    tod, mask, frequencies, time_axis = _get_data(file_paths[0], ctx)
    
    assert min_frequency <= frequencies[-1] 
    
    min_freq_idx = np.sum(frequencies<min_frequency)
    max_freq_idx = np.sum(frequencies<=max_frequency)
    main_freqs = frequencies[min_freq_idx:max_freq_idx] 
    strategy_start = get_observation_start(file_paths[0], ctx.params.file_type)
    
    tods = [tod[min_freq_idx:max_freq_idx, :]]
    time_axes = [time_axis]
    masks = []
    if mask is not None:
        masks.append(mask[min_freq_idx:max_freq_idx, :])
    
    for file_path in file_paths[1:]:
        tod, mask, frequencies, time_axis = _get_data(file_path, ctx)       
        frequencies = frequencies[min_freq_idx:max_freq_idx]
        assert np.all(main_freqs == frequencies)
        tods.append(tod[min_freq_idx:max_freq_idx, :])
        time_axes.append(time_axis)
        if mask is not None:
            masks.append(mask[min_freq_idx:max_freq_idx, :])
    
    tods = np.hstack(tods)
    time_axes = np.hstack(time_axes)
    if len(masks)>0:
        masks = np.hstack(masks)
    else:
        masks = None
    
    ref_channel_freq = ctx.params.ref_channel_freq
    ref_channel_idx = (np.fabs(main_freqs-ref_channel_freq)).argmin()
    ref_channel = tods[ref_channel_idx]
    tod_vx, tod_vy, frequencies, time_axes = _integrate(tods, masks, main_freqs, time_axes, ctx)
    return TimeOrderedData(strategy_start, frequencies, time_axes, tod_vx, tod_vy, ref_channel)
    


def convert_to_radio_frequency(frequencies, spectrometer):
    """
    Conversion between internal frequency and the actual physical frequency
    
    :param IF: internal frequency array
    :param ctx: context object
    
    :returns RF: converted frequency array
    """
    if spectrometer == SPECTROMETER_M9703A:
        start = 800 / (2**14-1) * (len(frequencies)-1)
        return (start - frequencies[::-1]) + 960
    
    return frequencies

def _get_data(path, ctx):
    """
    Loads the data from a fits file
    
    :param path: path to the data
    :param spectrometer: type of spectrometer
    
    :returns tod, frequencies: data and the frequency of the data
    """
    mask = None
    if ctx.params.file_type == FITS_FILE_TYPE:
        tod, frequencies, time_axis = _get_data_from_fits(path)
    elif ctx.params.file_type == HDF5_FILE_TYPE:
        tod, frequencies, time_axis = _get_data_from_hdf5(path, ctx.params.m9703a_mode)
        if ctx.params.spectral_kurtosis:
            mask = _get_spectral_kurtosis_mask(path, 
                                              ctx.params.accumulations,
                                              ctx.params.accumulation_offset)
            
    else:
        raise TypeError("Unsupported file type: '%s'"%ctx.params.file_type)

    frequencies = convert_to_radio_frequency(frequencies, ctx.params.spectrometer)

    return tod, mask, frequencies, time_axis

def _get_data_from_fits(path):
    """
    Loads the data from a fits file
    
    :param path: path to the data
    
    :returns tod, frequencies: data and the frequency of the data
    """
    with fits.open(path, mode='readonly', memmap=False) as hdu:
        frequencies = hdu[1].data["FREQUENCY"][0]
        time_step_size = hdu[0].header["CDELT1"]
        data = hdu[0].data.astype(np.float64)
        del hdu[0].data
        del hdu[1].data
        
    date = get_observation_start_from_fits(path)
    time_axis = time_step_size * (1 +np.arange(data.shape[1]))
    date_in_h = date.hour + date.minute / 60 + date.second / 3600
    time_axis = date_in_h + 1. / 3600 * time_axis

    tod = convert_callisto(data)
    return tod[::-1], frequencies[::-1], time_axis

def convert_callisto(data):
    """
    Converts the digits into kelvins
    
    :param frequencies: the frequencies of the data
    :param data: array containing the data [freq, time]
    
    :returns data: the converted data
    """
    return 10**(data/255*2500/25.4/10.0)        # TODO: replace magic numbers! define a conversion parameter? 

def _get_data_from_hdf5(path, m9703a_mode):
    """
    Loads the data from a hdf file
    
    :param path: path to the data
    
    :returns tod, frequencies: data and the frequency of the data
    """
    with h5py.File(path, "r") as fp:
        p_phase0 = fp["P/Phase0"].value
        p_phase1 = fp["P/Phase1"].value

        if m9703a_mode == MODE_PHASE_SWITCH:
            tod = p_phase1 - p_phase0
        elif m9703a_mode == MODE_TOTAL_POWER:
            tod = p_phase0 + p_phase1
        else:
            raise TypeError("Unsupported M9703A_MODE: '%s'"%m9703a_mode)
        
        frequencies = fp[FREQUENCIES_KEY].value
        time_axis = fp[TIME_KEY].value
    date = get_observation_start_from_hdf5(path)
    date_in_h = date.hour + date.minute / 60 + date.second / 3600
    time_axis = date_in_h + 1. / 3600 * time_axis
    return tod, frequencies, time_axis

def _get_spectral_kurtosis_mask(path, accumulations, accumulation_offset):
    """
    Get RFI mask based on the spectra kurtosis.

    :param path: path to the file
    :param accumulations: number of accumulations for the kurtosis calculation
    :param accumulation_offset: offset to convert the recorded values to physical
    kurtosis values

    :return: kurtosis-based RFI mask
    """
    with h5py.File(path, "r") as fp:
        p_phase0 = fp["P/Phase0"].value
        p_phase1 = fp["P/Phase1"].value
        p2_phase0 = fp["P2/Phase0"].value
        p2_phase1 = fp["P2/Phase1"].value
        mask = spectral_kurtosis_mask(p_phase0, 
                                      p_phase1, 
                                      p2_phase0, 
                                      p2_phase1, 
                                      accumulations, 
                                      accumulation_offset)
        return mask



def _integrate(data, masks, frequencies, time_axes, ctx):
    """
    Integrate over time and frequency on the TOD plane.

    :param data: TOD
    :param masks: mask
    :param frequencies: frequency axis after integration
    :param time_axes: time axis after integration
    :param ctx: context

    :return: TOD, time axis, frequency axis after integration
    """
    integration_time = ctx.params.integration_time
    integration_frequency = ctx.params.integration_frequency

    frequencies = smooth(np.atleast_2d(frequencies), integration_frequency, axis=1)[0]
    time_axes = smooth(np.atleast_2d(time_axes), integration_time, axis=1)[0]
    
    data = smooth(data, integration_time, axis=1)
    data = smooth(data, integration_frequency, axis=0)
    
    if masks is not None:
        # 'real' mask
        masks = masks
        masks = smooth(masks, integration_time, axis=1)
        masks = (smooth(masks, integration_frequency, axis=0) > 0)
    else:
        masks=get_empty_mask(data.shape)

    tod_vx = ma.array(data, mask=masks)
    tod_vy = ma.array(data, mask=masks)
    
    return tod_vx, tod_vy, frequencies, time_axes
    


class Plugin(BasePlugin):
    """
    Loads the data from files, applies cuts in frequency direction and also
    integrates the data in time and freq
    """

    def __call__(self):
        if self.ctx.params.verbose:
            print("Current files: %s"%("\n".join(self.ctx.file_paths)))
    
        tod = load_tod(self.ctx.file_paths, self.ctx)
        self.ctx.strategy_start = tod.strategy_start
        self.ctx.frequencies = tod.frequencies
        self.ctx.time_axis = tod.time_axis
        self.ctx.tod_vx = tod.vx
        self.ctx.tod_vy = tod.vy
        self.ctx.ref_channel = tod.ref_channel
        
    def __str__(self):
        return "Load data"


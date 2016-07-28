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
Created on Feb 4, 2016

author: cchang
'''

from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

import ephem
from datetime import timedelta
from scipy import optimize
from collections import namedtuple

from seek.plugins import load_data
from seek.utils import parse_datetime
from seek.mitigation import sum_threshold                
from seek.calibration import astro_calibration_source
from seek.calibration import fitting
from seek.utils import sphere
from seek.utils import load_file

# define constants
HOUR = timedelta(1.0/24.)
MINUTE = timedelta(1.0/24./60)
k = 1.38e-23
c = 3e8

CalibrationSource = namedtuple("CalibrationSource", ["date", "azimut", "elevation", "target"])
GaussFitResult = namedtuple("GaussFitResult", ["gauss_A", "gauss_x0", "gauss_sigma", "sky1", "sky2", 
                                               "gauss_A_err", "gauss_x0_err", "gauss_sigma_err", "sky1_err", "sky2_err", 
                                               "rsquared"])

def _find_file_list(datetime, cal_paths, params):
    """
    Given a datetime, find files that corresponding to two hours from this datetime.
    This is used for calibration only.

    :param datetime: datetime of interest (transit time)
    :param cal_paths: path of calibration files
    :param params: context parameters
    :return: list of files
    """

    file_list_temp = []
    for path in cal_paths:
        file_datetime = load_data.get_observation_start(path, params.file_type)
        
        if (datetime-15*MINUTE) <= file_datetime < (datetime+2*HOUR):
            file_list_temp.append(path)
            
    return file_list_temp

def _get_source_dec(source, params):
    """
    Get the declination coordinate of a given source in degrees.

    :param source: name of source
    :param params: context parameters

    :return: declination coordinate of source in degrees
    """
    if source.target == 'Sun':
        obs = ephem.Observer()
        obs.lon = params.telescope_longitude
        obs.lat = params.telescope_latitude
        obs.elevation = params.telescope_elevation
        obs.pressure = 0
        obs.date = source.date + HOUR
        s = ephem.Sun(obs)
        source_dec = s.dec/np.pi*180.0

    else:
        time = source.date + timedelta(seconds=3600)
        ra, dec = sphere.altaz_to_ra_dec(time, source.azimut, source.elevation, params=params)
        source_dec = np.degrees(dec)
        
    return source_dec

def fit_gaussian_source(data, time_axis, rfi_mask, source_dec, ctx):
    """
    Given a chunck of 2D data, fit a 1D Gaussian to each frequency.
    Here only return the amplitude.

    :param data: data
    :param time_axis: time axis
    :param rfi_mask: mask
    :param source_dec: declination coordinate of source
    :param ctx: context

    :return: amplitude of Gaussian fit
    """
    return fit_gaussian_source_full(data, time_axis, rfi_mask, source_dec, ctx)[0]

def fit_gaussian_source_full(data, time_axis, rfi_mask, source_dec, params):
    """
    Given a chunck of 2D data, fit a 1D Gaussian to each frequency.
    Here return all fitted parameters.
    
    :param data: data
    :param time_axis: time axis
    :param rfi_mask: mask
    :param source_dec: declination coordinate of source
    :param params: context parameters

    :return: all Gaussian fit parameters
    """
    no_params = 5
    fit_results = np.zeros((data.shape[0], 2*no_params+1))
    deg = np.arange(data.shape[1]) * (time_axis[1] - time_axis[0]) * 60 * 60 * (360. / 24 / 60 / 60) * params.integration_time * np.cos(source_dec / 180. * np.pi) # deg

    for k in range(data.shape[0]):
        ratio = np.sum(rfi_mask[k]) / rfi_mask.shape[1]
        if ratio<0.5: # hard code this?
            x = deg[rfi_mask[k]==False]
            y = data[k][rfi_mask[k]==False]
            if params.calibration_sources=='CygA':
                fit, perr, rsquared = fitting.fit_func(x, y, 'gauss2', [params.calibration_chi1, np.mean(deg), 1.0, params.calibration_chi1, np.mean(deg)+5.0, 1.5, 0.0, 1e10])
                fit_results[k, 0] = fit[0]

            else:
                fit, perr, rsquared = fitting.fit_func(x, y, 'gauss', [params.calibration_chi1, np.mean(deg), 1.0, 0.0, 1e10])
                fit_results[k, :no_params] = fit
                fit_results[k, no_params:2*no_params] = perr
                fit_results[k, -1] = rsquared

    return GaussFitResult(*[fit_results[:, i] for i in range(fit_results.shape[1])])

# def _plot_fit(x, y, func, fit, rsquared, ax):
#     ax.plot(x, y, label="R^2: %4.2f"%rsquared)
#     ax.plot(x, func(x, *fit), lw=2.0, color="k")
#     ax.legend()

def _sun_model_func(a, freq, data, gain):
    """
    Define module for fitting sun template to gain files
    """

    return np.sum((data - (gain * a[0] + (freq - a[2]) * a[1]))**2)


def fit_sun_to_gain(gauss_amp, freq, params):
    """
    Takes the array of Gaussian fit parameters and fits the sun template to it. 
    Then calculate the actual gain that converts the map ADU to K.
    """
    gauss_median = np.ma.median(gauss_amp, axis=0).data
    
    ref = astro_calibration_source.source(params.calibration_sources, freq*1e6)  
    Gain_median = ref/gauss_median
    Gain_median = np.nan_to_num(Gain_median)

    # outlier rejection -- need further generalization!
    mm = (Gain_median!=0)
    med = np.median(Gain_median[mm])
    std = np.std(Gain_median[mm])
    # this is to say that the gain should not vary drastically over frequency!
    Gain_median[(np.abs(Gain_median/med) > 3)|(np.abs(med/Gain_median) > 3)] = 0.0

    # fit measurement with sun spectra
    gain_sun = load_file(params.gain_file_sun, skip_header=True)
    sun_freq = gain_sun[:,0]
    sun_gain = gain_sun[:,1]
    sun_Ae = gain_sun[:,3]
    # sun_sigma = gain_sun[:,2]*(2*np.sqrt(2*np.log(2)))*(1.22/1.028)/2  # sigma ==> FWHM ==> FNBW

    # interpolate onto frequency grid
    sun_gain_interp = np.interp(freq, sun_freq, sun_gain)
    sun_Ae_interp = np.interp(freq, sun_freq, sun_Ae)

    # adjust this cut when doing the templates
    mask = (Gain_median!=0) * (freq>1000) * (freq<1280)
    cal_freq = freq[mask]
    cal = Gain_median[mask]
    
    opt = optimize.minimize(_sun_model_func, (350.0, 0.0001, 1120), args=(cal_freq, cal, sun_gain_interp[mask]), method='Powell')
    
    cal_gain = sun_gain_interp * opt['x'][0] + (freq - opt['x'][2]) * opt['x'][1]
    # lam = c / (freq * 1e6)
    # map_to_k = (lam**2/(np.pi*(sun_sigma_interp/180*np.pi)**2)*cal_gain/2./k*1e-26)**(-1)
    map_to_k = (sun_Ae_interp * cal_gain / 2. / k * 1e-26)**(-1)

    # print(opt)

    # here's to see by eye weather the fit is doing what it's suppose to do...
    # import pylab as mplot
    # import seaborn as sns 
    # sns.set_style("whitegrid")
    # sns.set_context("talk")
    # mplot.figure(figsize=(8,6))
    # mplot.scatter(cal_freq, cal, c='r')
    # mplot.plot(freq, cal_gain, color='k')
    # mplot.ylim(0, 7e-7)
    # mplot.title(str(params.calibration_sources)+'; N='+str(len(Gauss)))
    # mplot.grid(True)
    # mplot.savefig(str(params.strategy_start)+'_'+str(params.calibration_sources)+'.png')
    # mplot.show()

    return np.vstack((freq, map_to_k)).T, freq[mask], (sun_Ae_interp[mask]*Gain_median[mask]/2./k*1e-26)**(-1) 


def _parse_source(source_entry, cal_date):
    return CalibrationSource(parse_datetime(cal_date + '-' + source_entry[0]),
                             np.radians(source_entry[1]),
                             np.radians(source_entry[2]),
                             source_entry[3].split(':')[1].strip()
                             )

def calibrate(ctx, plot=False):
    """
    Main function that performs the calibration, including 
    the following steps:
    
    * loop through the calibration sources
        
        -- find the corresponding list of files

        -- RFI removal
      
        -- for each frequency fit 1D Gaussian to data
      
        -- divide amplitude by reference spectra
      
        -- store the final pseudo-gain value
    
    * take median pseudo-gain over all calibration sources
    * fit this final spectra with a template derived from Sun
    * store this final fit to memory

    :param ctx: context that contains all parameters for RFI removal and file paths

    :return: 2D array with first column frequency and second gain factor
    """

    frequencies, sun_fits = process_calibration_transits(ctx.calibrations_paths, ctx)
        
    sun_fit_means = np.mean(np.vstack(sun_fits), axis=0)
    return np.vstack((frequencies, sun_fit_means)).T

def process_calibration_transits(calibration_paths, ctx):
    """

    Derive gain as a function of frequency for each transit measurement.

    :param calibration_paths: path for calibration files
    :param ctx: context

    :return: gain as a function of frequency
    """
    params = ctx.params
    sm_kwargs, di_kwargs = sum_threshold.get_sumthreshold_kwargs(params)
    sun_fits = []
    
    source_cnt = 0
    
    file_path = calibration_paths.values()[0][1]
    frequencies = load_data.load_tod(file_path, ctx).frequencies
    
    gain_file = load_file(ctx.params.gain_file_default) 
    gain_template = np.interp(frequencies, gain_file[:, 0], gain_file[:, 1]).reshape(-1, 1)
    
    for cal_date, cal_paths in calibration_paths.items():
        gauss_amps = []
        # read in calibration files
        sources = np.genfromtxt(cal_paths[0], comments='#', delimiter=',', dtype=None)
        for source_entry in sources:
            source = _parse_source(source_entry, cal_date)
            # select only sources we want to use
            
            if source.target == params.calibration_sources:
                fit_result = process_source(source, cal_paths[1], gain_template, sm_kwargs, di_kwargs, ctx)
                if fit_result is not None:
                    gauss_amps.append(fit_result.gauss_A)
                    source_cnt += 1
        
        gauss_amps = np.array(gauss_amps)
        gauss_amps = np.ma.array(gauss_amps, mask=gauss_amps==0.0)
    
        sun_fit = fit_sun_to_gain(gauss_amps, frequencies, params)[0]
        sun_fits.append(sun_fit[:, 1])
        
    print('total calibration sources:', source_cnt)
    return frequencies, sun_fits

def process_source(source, file_paths, gain_template, sm_kwargs, di_kwargs, ctx):
    """
    Process a single transit measurement.

    :param source: name of source
    :param file_paths: file path
    :param gain_template: template derived from the Sun
    :param sm_kwargs: SumThreshold parameters
    :param di_kwargs: SumThreshold parameters
    :param ctx: context

    :return: parameters for Gaussian fit
    """
    # load data
    print('processing: ' + source.target, source.date)
    params = ctx.params
    file_list = _find_file_list(source.date, file_paths, params)
    
    if len(file_list) == 0:
        return None
    
    tod = load_data.load_tod(file_list, ctx)
    # cut further on time axis
    data_temp = tod.vx.copy()
    mask_temp = np.arange(len(tod.time_axis))
    mask_temp = mask_temp[(tod.time_axis >= source.date.hour)*(tod.time_axis < source.date.hour+2)] 
    data = data_temp[:,mask_temp]
    time_axis = tod.time_axis[mask_temp]

    # RFI removal
    rfi_mask = sum_threshold.get_rfi_mask(data/gain_template, 
                                          chi_1=100000,  #TODO: make configurable
                                          plotting=False, 
                                          sm_kwargs=sm_kwargs, 
                                          di_kwargs=di_kwargs)

    # fit Gaussian (everything, this is to get the sun size measurement)
    return fit_gaussian_source_full(data, time_axis, rfi_mask, _get_source_dec(source, params), params)

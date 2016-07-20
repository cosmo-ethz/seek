# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on May 30, 2016

author: cchang
'''

from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.plugin.base_plugin import BasePlugin
from seek.mitigation import sum_threshold
import healpy as hp
from scipy.ndimage.filters import gaussian_filter as gaussian


def mask_galaxy(nside, mask_original, mask_gal, ra, dec):
    """ Mask the galaxy on the TOD level with a given threshold in Kelvin.
    This is used in case one wants to model the baseline only based on the
    low Galactic emission regions. There is one mask template under the
    data directory that can be used.

    :param nside: Nside of healpix mask
    :param mask_original: the original TOD mask
    :param mask_gal: the healpix mask
    :param ra: RA coordinates corresponding to the TOD
    :param dec: DEC coordinates corresponding to the TOD

    :return: final TOD mask
    """

    theta = (np.pi / 2 - dec)
    phi = ra
    pix = hp.ang2pix(nside, theta, phi, nest=False)

    new_mask = np.zeros_like(mask_original)
    new_mask[:, mask_gal[pix]] = True

    return new_mask


class Plugin(BasePlugin):
    """ If specified "median", take the median of the masked data as the
    background model. If specified "smooth", the code will take the mask
    after sum-threshold and mask additionally the expected region of high
    Galactic emission. The final mask is used to build a smooth
    balckground model. """

    def __call__(self):


        if self.ctx.params.background_model == 'median':

            bg_modelx = np.ma.median(self.ctx.tod_vx, axis=1)[:, np.newaxis]
            bg_modely = np.ma.median(self.ctx.tod_vy, axis=1)[:, np.newaxis]

        if self.ctx.params.background_model == 'smooth':


            # more aggressive settings
            chi_1 = 3
            sm_kwars = sum_threshold.get_sm_kwargs(kernel_m = 12,
                                                   kernel_n = 150,
                                                   sigma_m = 2,
                                                   sigma_n = 25)

            di_kwargs = sum_threshold.get_di_kwrags(self.ctx.params.struct_size_0,
                                                    self.ctx.params.struct_size_1)

            mask_gal = self.ctx.simulation_mask
            mask_originalx = self.ctx.tod_vx.mask

            # to save time only run this once, the second polarization is the same as the first
            mask_newx2 = mask_originalx + mask_galaxy(self.ctx.params.nside, mask_originalx, mask_gal, self.ctx.coords.ra, self.ctx.coords.dec)
            mask_newy2 = mask_newx2.copy()

            # TODO: mask point sources
            # mask_newx = mask_point_source(mask_newx)
            # mask_newy = mask_point_source(mask_newy)

            mask_newx2 = sum_threshold.get_rfi_mask(self.ctx.tod_vx,
                               mask=mask_newx2,
                               chi_1 = chi_1,
                               eta_i=[1],
                               plotting=False,
                               sm_kwargs=sm_kwars,
                               di_kwargs=di_kwargs)

            mask_newy2 = mask_newx2.copy()

            # some of the time-axes are shorter than the TOD, need to fix this!
            if len(self.ctx.time_axis)==len(mask_newx2[0]):
                time_axis = self.ctx.time_axis.copy()
            else:
                print('wrong time-axis length!')
                time_axis = np.arange(mask_newx2.shape[1])

            # this is a rough mask for the ocasional very low values, need to improve on this
            median_x = np.ma.median(self.ctx.tod_vx, axis=1)[:, np.newaxis]
            median_y = np.ma.median(self.ctx.tod_vx, axis=1)[:, np.newaxis]
            mask_newx2[(self.ctx.tod_vx.data < (median_x - 50))] = True
            mask_newy2[(self.ctx.tod_vy.data < (median_y - 50))] = True

            bg_modelx = np.zeros(mask_newx2.shape)
            bg_modely = np.zeros(mask_newy2.shape)
            
            for i in range(len(bg_modelx)):
                mask_size = np.sum(~mask_newx2[i])
                if (mask_size > 100):
                    y = np.interp(time_axis, 
                                  time_axis[mask_newx2[i]], 
                                  self.ctx.tod_vx.data[i][mask_newx2[i]], 
                                  left=self.ctx.tod_vx.data[i][mask_newx2[i]][0], 
                                  right=self.ctx.tod_vx.data[i][mask_newx2[i]][-1])
                    
                    # smoothing around 1hr-time scale
                    bg_modelx[i] = gaussian(y, sigma=600)
                    bg_modely[i] = gaussian(y, sigma=600)

                elif (mask_size > 0):
                    bg_modelx[i, :] = np.median(self.ctx.tod_vx.data[i][mask_newx2[i]])
                    bg_modely[i, :] = np.median(self.ctx.tod_vy.data[i][mask_newy2[i]])

            # make diagnostic plot
            # import pylab as mplot
            # mplot.figure()
            # mplot.plot(self.ctx.tod_vx.data[0])
            # temp = self.ctx.tod_vx.data[0]
            # temp[mask_newx2[0]==1] = 'nan'
            # mplot.plot(temp)
            # mplot.plot(bg_modelx[0])
            # mplot.ylim(30,80)
            # mplot.title(str(self.ctx.file_paths[0][-20:])+'\n'+str(self.ctx.coords.ra[0]/np.pi*180)[:5])
            #
            # mplot.show()

        # subtract background

        self.ctx.tod_vx.bg = bg_modelx
        self.ctx.tod_vy.bg = bg_modely
        self.ctx.tod_vx -= bg_modelx
        self.ctx.tod_vy = self.ctx.tod_vx.copy()


    def __str__(self):
        return "remove background baseline"
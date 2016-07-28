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
Created on Dec 21, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

def get_stats(rfi, rfi_mask):
    """
    Returns the stats needed to compute a ROC curve.

    :param rfi: array containing the RFI pixels
    :param rfi_mask: boolean array that masks the RFI
    
    :returns rl, ml, il: count of rfi pixels, count of masked pixels, count of intersecting pixels
    """
    rfi_idx = np.where(rfi!=0)
    mask_idx = np.where(rfi_mask==True)
    rfi_idx_set = set([(x,y) for (x,y) in zip(rfi_idx[0], rfi_idx[1])])
    mask_idx_set = set([(x,y) for (x,y) in zip(mask_idx[0], mask_idx[1])])
    
    intersect = rfi_idx_set.intersection(mask_idx_set)
    
    return len(rfi_idx_set), len(mask_idx_set), len(intersect)
    
def plot_data(data, ax, title, vmin=None, vmax=None, cb=True, norm=None, extent=None, cmap=None):
    """
    Plot TOD.
    """
    import pylab
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    
    ax.set_title(title)
    im = ax.imshow(data, 
            aspect="auto", 
            origin="lower",
            norm=norm,
            extent=extent,
            cmap=cmap,
            interpolation="nearest", vmin=vmin, vmax=vmax)
    
    if cb:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="20%", pad=0.05)
        cbar = pylab.colorbar(im, cax=cax)

def plot_moments(data):
    """
    Plot standard divation and mean of data.
    """
    import pylab

    std_time = np.std(data, axis=0)
    mean_time = np.mean(data, axis=0)
    std_freuqency = np.std(data, axis=1)
    mean_freuqency = np.mean(data, axis=1)
    pylab.subplot(121)
    pylab.plot(mean_time)
    pylab.xlabel("time") 
    pylab.ylabel("mean")
    pylab.subplot(122)
    pylab.plot(std_time)
    pylab.xlabel("time") 
    pylab.ylabel("std")
    pylab.show()
    pylab.subplot(121)
    pylab.plot(mean_freuqency)
    pylab.xlabel("freuqency") 
    pylab.ylabel("mean")
    pylab.subplot(122)
    pylab.plot(std_freuqency)
    pylab.xlabel("freuqency") 
    pylab.ylabel("std")
    pylab.tight_layout()
    pylab.show()

def plot_steps(data, st_mask, smoothed_data, res, eta):
    """
    Plot individual steps of SumThreshold.
    """
    import pylab
    f, ax = pylab.subplots(2,2, figsize=(15,8))
    f.suptitle("Eta: %s"%eta)
    plot_data(data, ax[0,0], "data")
    plot_data(st_mask, ax[1,0], "mask (%s)"%(st_mask.sum()), 0, 1)
    smoothed = np.ma.MaskedArray(smoothed_data, st_mask)
    plot_data(smoothed, ax[0,1], "_smooth")
    plot_data(res, ax[1,1], "residuals")
    f.show()


def plot_dilation(st_mask, mask, dilated_mask):
    """
    Plot mask and dilation.
    """
    import pylab
    fig, ax = pylab.subplots(2,2, figsize=(15,8))
    fig.suptitle("Mask analysis")
    plot_data(mask, ax[0,0], "Original mask")
    plot_data(st_mask.astype(np.bool)-mask, ax[0,1], "Sum threshold mask", 0, 1)
    plot_data(dilated_mask, ax[1,0], "dilated mask")
    plot_data(dilated_mask+mask, ax[1,1], "New mask")
    fig.show()

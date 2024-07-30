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
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

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

def plot_data(data, ax, title, vmin=None, vmax=None, 
              cb=True, norm=None, extent=None, cmap=None):
    """
    Plot TOD with customization options.

    :param data: 2D array to be plotted
    :param ax: matplotlib axis object where the plot will be drawn
    :param title: title of the plot
    :param vmin: minimum value for colormap scaling
    :param vmax: maximum value for colormap scaling
    :param cb: boolean flag to add a colorbar
    :param norm: normalization for the colormap
    :param extent: data limits for the axes
    :param cmap: colormap to be used for the plot
    """

    ax.set_title(title)

    im = ax.imshow(
        data,
        aspect="auto",
        origin="lower",
        norm=norm,
        extent=extent,
        cmap=cmap,
        interpolation="nearest",
        vmin=vmin,
        vmax=vmax,
    )

    # Add colorbar if flagged
    if cb:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="20%", pad=0.05)
        plt.colorbar(im, cax=cax)


def plot_moments(data, title):
    """
    Plot standard deviation and mean of data.
    """

    std_time = np.std(data, axis=0)
    mean_time = np.mean(data, axis=0)
    std_frequency = np.std(data, axis=1)
    mean_frequency = np.mean(data, axis=1)

    fig, ax = plt.subplots(2, 2, figsize=(12, 8))

    # Plot mean and std over time
    ax[0, 0].plot(mean_time)
    ax[0, 0].set_xlabel("Time")
    ax[0, 0].set_ylabel("Mean")
    ax[0, 0].set_title("Mean over Time")

    ax[0, 1].plot(std_time)
    ax[0, 1].set_xlabel("Time")
    ax[0, 1].set_ylabel("Standard Deviation")
    ax[0, 1].set_title("Std Dev over Time")

    # Plot mean and std over frequency
    ax[1, 0].plot(mean_frequency)
    ax[1, 0].set_xlabel("Frequency")
    ax[1, 0].set_ylabel("Mean")
    ax[1, 0].set_title("Mean over Frequency")

    ax[1, 1].plot(std_frequency)
    ax[1, 1].set_xlabel("Frequency")
    ax[1, 1].set_ylabel("Standard Deviation")
    ax[1, 1].set_title("Std Dev over Frequency")

    fig.suptitle(title, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to make room for suptitle

    plt.tight_layout()
    plt.show()


def plot_steps(data, st_mask, smoothed_data, res, eta):
    """
    Plot individual steps of SumThreshold.

    :param data: Original data
    :param st_mask: Sum threshold mask
    :param smoothed_data: Smoothed data
    :param res: Residuals
    :param eta: Eta value
    """

    fig, ax = plt.subplots(2, 2, figsize=(15, 8))
    fig.suptitle(f"Eta: {eta}")

    plot_data(data, ax[0, 0], "Data")
    plot_data(st_mask, ax[1, 0], f"Mask ({st_mask.sum()})", 0, 1)

    smoothed = np.ma.MaskedArray(smoothed_data, st_mask)
    plot_data(smoothed, ax[0, 1], "Smoothed")
    plot_data(res, ax[1, 1], "Residuals")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust layout to fit title
    plt.show()


def plot_dilation(st_mask, mask, dilated_mask):
    """
    Plot mask and dilation.

    :param st_mask: Sum threshold mask
    :param mask: Original mask
    :param dilated_mask: Dilated mask
    """
    fig, ax = plt.subplots(2, 2, figsize=(15, 8))
    fig.suptitle("Mask analysis")

    plot_data(mask, ax[0, 0], "Original mask")
    plot_data(
        np.logical_xor(st_mask.astype(np.bool_), mask),
        ax[0, 1],
        "Sum threshold mask",
        0,
        1,
    )
    plot_data(dilated_mask, ax[1, 0], "dilated mask")
    plot_data(dilated_mask + mask, ax[1, 1], "New mask")

    plt.show()

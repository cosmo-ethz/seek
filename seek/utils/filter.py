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
Created on Jan 23, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
import hope

def gaussian_filter(V, mask, M=40, N=20, sigma_m=0.5, sigma_n=0.5):
    """
    Applies a gaussian filter (smoothing) to the given array taking into account masked values
    :param V: the value array to be smoothed
    :param mask: boolean array defining masked values
    :param M: kernel window size in axis=1
    :param N: kernel window size in axis=0
    :param sigma_m: kernel sigma in axis=1
    :param sigma_n: kernel sigma in axis=0
    
    :returns vs: the filtered array 
    """
    
    def wd(n, m, sigma_n, sigma_m):
        return np.exp(-n**2/(2*sigma_n**2) - m**2/(2*sigma_m**2))
    
    Vp = np.zeros((V.shape[0]+N, V.shape[1]+M))
    Vp[N//2:-N//2,M//2:-M//2] = V[:]

    Wfp = np.zeros((V.shape[0]+N, V.shape[1]+M))
    Wfp[N//2:-N//2,M//2:-M//2] = ~mask[:]
    Vh = np.zeros((V.shape[0]+N, V.shape[1]+M))
    Vh2 = np.zeros((V.shape[0]+N, V.shape[1]+M))
    
    n = np.arange(-N/2, N/2+1)
    m = np.arange(-M/2, M/2+1)
    kernel_0 = wd(n, 0, sigma_n=sigma_n, sigma_m=sigma_m).T
    kernel_1 = wd(0, m, sigma_n=sigma_n, sigma_m=sigma_m).T
    
    Vh = _gaussian_filter(Vp, V.shape[0], V.shape[1], Wfp, mask, Vh, Vh2, kernel_0, kernel_1, M, N)
    Vh = Vh[N//2:-N//2,M//2:-M//2]
    Vh[mask] = V[mask]
    return Vh

@hope.jit
def _gaussian_filter(Vp, vs0, vs1, Wfp, mask, Vh, Vh2, kernel_0, kernel_1, M, N):

    n2 = N/2
    m2 = M/2
    for i in range((N//2), vs0+(N//2)):
        for j in range((M//2), vs1+(M//2)):
            if mask[i-n2, j-m2]:
                Vh[i, j] = 0#V[i-n2, j-m2]
            else:
                val = np.sum((Wfp[i-n2:i+n2+1, j] * Vp[i-n2:i+n2+1, j] * kernel_0))
                Vh[i, j] = val / np.sum(Wfp[i-n2:i+n2+1, j] * kernel_0)
    
    for j2 in range((M//2), vs1+(M//2)):
        for i2 in range((N//2), vs0+(N//2)):
            if mask[i2-n2, j2-m2]:
                Vh2[i2, j2] = 0#V[i2-n2, j2-m2]
            else:
                val = np.sum((Wfp[i2, j2-m2:j2+m2+1] * Vh[i2, j2-m2:j2+m2+1] * kernel_1))
                Vh2[i2, j2] = val / np.sum(Wfp[i2, j2-m2:j2+m2+1] * kernel_1)
    return Vh2
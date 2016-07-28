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
Created on Aug 11, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import

import healpy as hp
import numpy as np
from hide.utils import sphere
import matplotlib.pyplot as plt

def cubehelix_palette():
    import seaborn as sns
    return sns.cubehelix_palette(as_cmap=True, start=.5, rot=-.75)

def mollview(hpmap, mark_unseen=True, radiosrc=True, cmap=None, **kwargs):
    if cmap is None:
        cmap = cubehelix_palette()
    
    if mark_unseen:
        hpmap = hpmap.copy()
        hpmap[hpmap==0] = hp.UNSEEN

    figsize = kwargs.pop("figsize", (15,10))
    fig, ax = plt.subplots(figsize=figsize)

    title = kwargs.pop("title", "")

    hp.mollview(hpmap, coord="C",
                hold=True, 
                cmap=cmap,
                title=title,
                **kwargs)
    
    hp.graticule(coord="g", verbose=False)
    
    if radiosrc:
        ax=hp.projaxes.HpxMollweideAxes(fig, (0.02,0.05,0.96,0.9),coord="g")
        fig.add_axes(ax)
    
        def add_radiosrc(ra, dec):
            hpmollaxes = fig.axes[-1]
            phi = sphere.ra2phi(ra * 2 * np.pi / 25)
            theta = sphere.dec2theta(np.radians(dec))
            scatter_kwargs = dict(marker="o", facecolors='none', edgecolors='r', linewidth=2.)
            hpmollaxes.projscatter(theta,phi, 700, **scatter_kwargs)
            
        add_radiosrc(5.58, 22.02)
        add_radiosrc(20.62, 42.03)
        add_radiosrc(23.0, 62.03)
    return fig
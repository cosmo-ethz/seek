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
Created on Feb 26, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from ivy.utils.struct import Struct
from seek.plugins import restructure_tod
import h5py
from seek.plugins.create_maps import RestructuredTODStore

def test_restructure(tmpdir):
    
    idxs = np.arange(9)
    data = np.ones((2, 9)) * idxs * [[1],[2]]
    tod = np.ma.array(data, mask=np.zeros((2,9), np.bool))
    
    cntr = dict(zip(idxs, idxs))
    pix_numbers = idxs
    tempfile = str(tmpdir.join("tmp.h5"))
    with h5py.File(tempfile, "w") as fp:
        restructure_tod.restructure(fp, tod, cntr, pix_numbers)
    
    with RestructuredTODStore([tempfile]) as store:
        for idx in idxs:
            data = store.get(idx)
            assert np.all(data.data.flatten() == [idx, 2 * idx])
            assert np.all(data.mask == False)
    

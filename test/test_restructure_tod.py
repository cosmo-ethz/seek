# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

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
    

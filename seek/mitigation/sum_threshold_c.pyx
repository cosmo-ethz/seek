# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Feb 16, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

cimport cython
import numpy as np
cimport numpy as np


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef _sumthreshold(np.ndarray[np.double_t, ndim=2] data, 
                     np.ndarray[np.int_t, ndim=2] mask, 
                     np.ndarray[np.int_t, ndim=2] tmask, 
                     int i, float chi):
    cdef float sum = 0
    cdef float t
    cdef int x,y,ii, cnt
    
    if i > data.shape[1]:
        return
    
    for x in range(data.shape[0]):
        sum = 0
        cnt = 0
        
        for ii in range(0, i):
            if mask[x, ii] != 1:
                sum += data[x, ii]
                cnt = cnt + 1
        
        for y in range(i, data.shape[1]):
            #print( y, sum, cnt)
            if sum > chi * cnt:
                for ii in range(0, i):
                    tmask[x, y-ii-1] = 1
                    
            if mask[x, y] != 1:
                sum += data[x, y]
                cnt += 1
            
            if mask[x, y-i] != 1:
                sum -= data[x, y-i]
                cnt -= 1
    mask[:] = tmask
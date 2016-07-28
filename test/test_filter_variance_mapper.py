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
from seek.mapmaking import filter_variance_mapper

def test_get_mapped_values():
    data = np.ones((2, 9))
    data[:,0] = 10 #outlier
    data = np.ma.array(data, mask=np.zeros((2,9), np.bool))
    
    values, counts = filter_variance_mapper.get_mapped_values(data, None)
    assert values.shape == (2,)
    assert np.all(values==0)
    
    assert counts.shape == (2,)
    assert np.all(counts==8)

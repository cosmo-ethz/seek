# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Jan 20, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from mock import patch
from seek.plugins import pre_process_tod

def test_convert_m9703a():
    frequencies = np.arange(980, 1300)

    gain_file = np.vstack((frequencies, np.linspace(1, 10, len(frequencies)))).T
    gain = np.linspace(1, 10, len(frequencies))
    data = np.ones((len(frequencies), 100)) * gain.reshape(-1, 1)
    converted_data = pre_process_tod.apply_gain(frequencies, data, gain_file)
    
    assert np.allclose(converted_data[:, 0], 1.)

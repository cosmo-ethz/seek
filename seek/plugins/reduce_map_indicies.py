# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Feb 26, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

class Plugin(object):
    """
    Reduces the restructured TODs constructed per chunk to one.
    """

    def __init__(self, ctx):
        self.ctx = ctx
    
    def reduce(self, ctxList):
        paths = []
        pixels = []
        for ctx in ctxList:
            paths.append(ctx.restructured_tod_path)
            pixels.extend(ctx.restructured_tod_pixels)
        
        self.ctx.tod_paths = paths
        self.ctx.restructured_tod_pixels = list(set(pixels)) #remove duplicates
        self.ctx.frequencies = ctx.frequencies

# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Mar 7, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

class Plugin(object):
    """
    Maps the file paths to the plugin collection.
    """
    
    def __init__(self, ctx):
        self.ctx = ctx
    
    def getWorkload(self):
        pixels = self.ctx.restructured_tod_pixels
        chunk_size = int(len(pixels) / self.ctx.params.cpu_count)
        for map_pixels in chunk(pixels, chunk_size):
            ctx = self.ctx.copy()
            ctx.map_pixels = map_pixels
            
            yield ctx
            
def chunk(iterable, n):
    for i in xrange(0, len(iterable), n):
        yield iterable[i:i+n]
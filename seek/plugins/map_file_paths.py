# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Feb 3, 2015

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
        chunk_size = self.ctx.params.chunk_size
        for files_per_day in self.ctx.data_file_paths:
            for file_paths in chunk(files_per_day, chunk_size):
                ctx = self.ctx.copy()
                ctx.file_paths = file_paths
                
                yield ctx
            
def chunk(iterable, n):
    for i in xrange(0, len(iterable), n):
        yield iterable[i:i+n]
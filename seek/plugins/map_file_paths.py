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
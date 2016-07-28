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
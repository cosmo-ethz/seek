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

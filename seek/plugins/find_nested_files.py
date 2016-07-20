# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Jul 27, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from datetime import timedelta
import os
import re

from collections import OrderedDict
from ivy.plugin.base_plugin import BasePlugin

from seek.utils import parse_datetime
from seek.utils import format_date


COORD_FILE_FORMAT = "%s%04d%02d%02d.txt"
CALIBRATION_FILE_FORMAT = "CALIBRATION_RSG_7m_%04d%02d%02d.txt"

SKIP_FILE_NAME = "skip"

def is_skiped(path, date, prefix):
    """
    Determine whether the date is skipped.

    :param path: path where files are stored
    :param date: date corresponding to the files
    :param prefix: file prefix

    :return: TRUE or FALSE
    """
    skip_path = os.path.join(path, SKIP_FILE_NAME)
    coord_path = get_coords_path(path, date, prefix)
    return os.path.exists(skip_path) or not os.path.isfile(coord_path)

def is_calibration_day(path, date):
    """
    Determine whether the date is a calibration day.

    :param path: path where files are stored
    :param date: date corresponding to the files
    :param prefix: file prefix

    :return: TRUE or FALSE
    """
    calibration_path = get_calibration_path(path, date)
    return os.path.exists(calibration_path)

def get_coords_path(path, date, prefix):
    """
    Get path for coordinate file.

    :param path: path for the data files
    :param date: date corresponding to the files
    :param prefix: file prefix

    :return: full path to coordinate file
    """
    coord_filename = COORD_FILE_FORMAT%(prefix, date.year, date.month, date.day)
    return os.path.join(path, coord_filename)

def get_calibration_path(path, date):
    """
    Get path for calibration file.

    :param path: path for the data files
    :param date: date corresponding to the files
    :param prefix: file prefix

    :return: full path to calibration file
    """
    calibration_filename = CALIBRATION_FILE_FORMAT%(date.year, date.month, date.day)
    return os.path.join(path, calibration_filename)

class Plugin(BasePlugin):
    """
    Traverses the file system from the `file_prefix` and collects all data and
    coord paths within the scanning strategy start and end date
    """
    
    def __call__(self):
        strategy_start = parse_datetime(self.ctx.params.strategy_start)
        strategy_end   = parse_datetime(self.ctx.params.strategy_end)
        
        pattern = "^%s(?P<date>\w+)%s$"%(self.ctx.params.data_file_prefix,
                                         self.ctx.params.data_file_suffix)
        
        p = re.compile(pattern)
        
        date_format = self.ctx.params.file_date_format
        
        file_prefix = self.ctx.params.file_prefix
        prefix = self.ctx.params.coord_prefix
        
        data_file_paths = []
        coords_paths = {}
        calibrations_paths = OrderedDict()
        
        date = strategy_start
        DAY = timedelta(1)
        
        while strategy_start <= date <= strategy_end:
            path = os.path.join(file_prefix, "%04d"%date.year, "%02d"%date.month, "%02d"%date.day)
            
            if not is_skiped(path, date, prefix):
                coords_paths[format_date(date)] = get_coords_path(path, date, prefix)
                data_files_per_day = []
                for filename in sorted(os.listdir(path)):
                    match = p.match(filename)
                    if match is not None:
                        file_date = parse_datetime(match.group("date"), date_format)
                        #TODO: something smarter needs to be done here!
                        if strategy_start <= file_date <= strategy_end:
                            if date.year == file_date.year and date.month == file_date.month and date.day == file_date.day:
                                data_files_per_day.append(os.path.join(path, filename))
                        else:
                            if self.ctx.params.verbose:
                                print("skipping", os.path.join(path, filename))
                            
                if len(data_files_per_day) > 0:
                    if is_calibration_day(path, date):
                        calibrations_paths[format_date(date)] = (get_calibration_path(path, date), data_files_per_day)
                    else:
                        data_file_paths.append(data_files_per_day)
                        
            date = date + DAY
        
        assert len(data_file_paths)!=0 or len(calibrations_paths)!=0, "No files match requirements"
        
        if self.ctx.params.verbose:
            print("Total number of days found: ", len(data_file_paths))
            print("Total number of calibration days found: ", len(calibrations_paths))
            
        self.ctx.data_file_paths = data_file_paths
        self.ctx.coords_paths = coords_paths
        self.ctx.calibrations_paths = calibrations_paths

    def __str__(self):
        return "Traversing file system"

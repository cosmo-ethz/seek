
from pkg_resources import resource_filename
from datetime import datetime
import os
import numpy as np

import seek
from seek import DATE_FORMAT, DATETIME_FORMAT

def parse_datetime(s, fmt=DATETIME_FORMAT):
    """
    Parse datetime object with specific format.

    :param s: datetime string
    :param fmt: format definition

    :return: parsed datetime object
    """
    return datetime.strptime(s, fmt)

def format_date(date, fmt=DATE_FORMAT):
    """
    Format datetime object into specific format string.

    :param date: datetime object
    :param fmt: format definition

    :return: formatted string
    """
    return date.strftime(fmt)

def load_file(path, **kwargs):
    """
    Load text file within the main code directory.

    :param path: path of file within the main code directory

    :return: array generated from text file
    """
    
    if not os.path.exists(path):
        path = resource_filename(seek.__name__, path)
        
    return np.genfromtxt(path, **kwargs)
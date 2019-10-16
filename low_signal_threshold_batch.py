# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 21:23:05 2018

@author: pjh523
"""

import gwy
import math
from pygwy_functions import low_signal_threshold

plugin_menu = "/Grains/Batch/Low Signal Image..."
plugin_type = "PROCESS"
plugin_desc = '''Threshold algorithm for low signal images. Performs a Gaussian blur and then Otsu's power scaled threshold.'''

def run():
    # get all containers
    containers = gwy.gwy_app_data_browser_get_containers()
    # save each container as gwy file with file name
    for c in containers:
        # do algorithm
        low_signal_threshold(c)

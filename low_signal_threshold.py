# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 21:23:05 2018

@author: pjh523
"""

import gwy
import math
from functions.pygwy_functions import low_signal_threshold

plugin_menu = "/Grains/Mark by Low Signal Method..."
plugin_type = "PROCESS"
plugin_desc = '''Threshold algorithm for low signal images. Performs a Gaussian blur and then Otsu's power scaled threshold.'''

def run():
    # get open container
    container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
    # run algorithm
    low_signal_threshold(container)

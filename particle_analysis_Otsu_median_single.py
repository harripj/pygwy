#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:51:38 2018

@author: pjh523
"""

import gwy
from pygwy_functions import analyse_particles_otsu_median

plugin_menu = "/Grains/Analyse Particles/Otsu's Method (Median)/Single"
plugin_type = "PROCESS"
plugin_desc = '''Analyse particles on image using histogram modal classifier.
                Works well for skewed height/intensity distribution.
                Finds grains and saves data to JSON of same file name.'''

def run():
    # get current image data
    datafield_id = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)
    container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)

    analyse_particles_otsu_median(container, datafield_id=datafield_id)
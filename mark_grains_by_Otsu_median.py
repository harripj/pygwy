#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 21:23:05 2018

@author: pjh523
"""

import gwy
from pygwy_functions import analyse_particles_otsu_median

plugin_menu = "/Grains/Mark by Otsu's (Median)"
plugin_type = "PROCESS"
plugin_desc = '''Mark grains in datafield by Otsu's method with a median descriptor.'''

def run():
    # get current data and correct container for file
    datafield_id = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)
    container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)

    # create undo point
    gwy.gwy_undo_qcheckpoint(container, container.keys())
    
    analyse_particles_otsu_median(container, datafield_id, save=False)
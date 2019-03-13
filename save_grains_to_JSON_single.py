#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 21:27:38 2018

@author: pjh523
"""

import gwy
from pygwy_functions import save_gwy_grain_mask_to_JSON

plugin_menu = "/Grains/Analyse Particles/Save Grains to JSON/Single"
plugin_type = "PROCESS"
plugin_desc = '''Calculate parameters of current grain field and save to JSON file.'''

def run():
    # get current data and correct container for file
    datafield_id = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)
    container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
    
    save_gwy_grain_mask_to_JSON(container, datafield_id=datafield_id)

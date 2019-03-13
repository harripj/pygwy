#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 15:25:03 2018

@author: pjh523
"""

import gwy
from pygwy_functions import laplacian_of_gaussian

plugin_menu = "/Integral Transforms/Laplacian of Gaussian"
plugin_type = "PROCESS"
plugin_desc = '''Apply a Laplacian of Gaussian filter to an image.
                This is useful for finding edges on sloped surfaces.'''

def run():
    # get current image data
    datafield_id = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)
    container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)

    laplacian_of_gaussian(container, datafield_id=datafield_id)

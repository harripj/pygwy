#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:55:05 2018

@author: pjh523
"""

import gwy
from pygwy_functions import analyse_particles_otsu_median

plugin_menu = "/Grains/Analyse Particles/Otsu's Method (Median)/Batch"
plugin_type = "PROCESS"
plugin_desc = '''Equivalent to 'Otsu Modal Method -> Single, but works on all
                open containers.'''

def run():
    # get containers
    containers = gwy.gwy_app_data_browser_get_containers()
    # get current image data
    for container in containers:
        # get dictionary of all datafields
        #datafield_ids = gwy.gwy_app_data_browser_get_data_ids(container)
        
        analyse_particles_otsu_median(container)#, datafield_id=0)
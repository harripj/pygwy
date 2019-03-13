##!/usr/bin/env python3
## -*- coding: utf-8 -*-
#"""
#Created on Thu Jun 14 00:50:20 2018
#
#@author: pjh523
#"""
#
#import gwy
#from pygwy_functions import super_find_particles
#
#plugin_menu = "/Grains/Analyse Particles/Otsu x LoG/Single"
#plugin_type = "PROCESS"
#plugin_desc = '''Super method involves combinign masks of Otsu thresholds and LoG.'''
#
#def run():
#    # get current image data
#    datafield_id = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)
#    container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
#
#    super_find_particles(container, datafield_id=datafield_id)
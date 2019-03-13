##!/usr/bin/env python3
## -*- coding: utf-8 -*-
#"""
#Created on Thu Jun 14 11:23:56 2018
#
#@author: pjh523
#"""
#
#import gwy
#from pygwy_functions import super_find_particles
#
#plugin_menu = "/Grains/Analyse Particles/Otsu x LoG/Multiple"
#plugin_type = "PROCESS"
#plugin_desc = '''Equivalent to 'Analyse Particles -> Single, but works on all
#                open containers.'''
#
#def run():
#    # get containers
#    containers = gwy.gwy_app_data_browser_get_containers()
#    # get current image data
#    for container in containers:
#        # get dictionary of all datafields
#        datafield_ids = gwy.gwy_app_data_browser_get_data_ids(container)
#        
#        for _id in datafield_ids:
#            super_find_particles(container, datafield_id=_id)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 21:23:05 2018

@author: pjh523
"""

import gwy
import os

plugin_menu = "/Basic Operations/Export All/.gwy"
plugin_type = "PROCESS"
plugin_desc = '''Save all open containers as .gwy files.'''

def run():
    # get all containers
    containers = gwy.gwy_app_data_browser_get_containers()
    # save each container as gwy file with file name
    for c in containers:
        fname = gwy.gwy_file_get_filename_sys(c)
        _, ext = os.path.splitext(fname)

        gwy.gwy_file_save(c, fname.replace(ext, '.gwy'), gwy.RUN_NONINTERACTIVE)

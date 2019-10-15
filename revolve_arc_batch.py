# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 21:23:05 2018

@author: pjh523
"""

import gwy

plugin_menu = "/Level/Revolve Arc Batch..."
plugin_type = "PROCESS"
plugin_desc = '''Revolve arc for all open containers.'''

def run():
    # get all containers
    containers = gwy.gwy_app_data_browser_get_containers()
    # save each container as gwy file with file name
    for c in containers:
        # get datafield 0 for each container for func to operate on
	    gwy.gwy_app_data_browser_select_data_field(c, 0)
	    gwy.gwy_process_func_run('arc_revolve', c, gwy.RUN_IMMEDIATE)
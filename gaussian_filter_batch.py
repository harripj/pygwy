# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 21:23:05 2018

@author: pjh523
"""

import gwy
import math
from pygwy_functions import get_data_key

plugin_menu = "/Basic Operations/Gaussian Filter Batch..."
plugin_type = "PROCESS"
plugin_desc = '''Batch gaussian filter for all open containers. Sigma is as set in Tools->Filters->Gaussian Size'''

def run():
    # stored app settings
    settings = gwy.gwy_app_settings_get()
    # get sigma from settings, ie. vlaue last used in toolbox->filters
    size = settings['/module/filter/gauss_size']
    sigma = size / (2.*math.sqrt(2.*math.log(2.)))
    # get all containers
    containers = gwy.gwy_app_data_browser_get_containers()
    # save each container as gwy file with file name
    for c in containers:
        # create checkpoint
        gwy.gwy_app_undo_checkpoint(c, c.keys_by_name())
        # get datafield 0 for each container for func to operate on
        data = c[get_data_key()]
        # do gaussian filter
        data.filter_gaussian(sigma)
        # emit signal to container to update UI
        data.data_changed()
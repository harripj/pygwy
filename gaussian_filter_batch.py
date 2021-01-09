# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 21:23:05 2018

@author: pjh523
"""

import gwy
import math
from functions.pygwy_functions import get_gaussian_sigma

plugin_menu = "/Basic Operations/Gaussian Filter Batch..."
plugin_type = "PROCESS"
plugin_desc = """Batch gaussian filter for all open containers. Sigma is as set in Tools->Filters->Gaussian Size"""


def run():
    # get gauss size from settings, ie. value last used in toolbox->filters
    sigma = get_gaussian_sigma()
    # get all containers
    containers = gwy.gwy_app_data_browser_get_containers()
    # save each container as gwy file with file name
    for c in containers:
        # create checkpoint
        gwy.gwy_app_undo_checkpoint(c, c.keys_by_name())
        # get datafield 0 for each container for func to operate on
        datafield = c[gwy.gwy_app_get_data_key_for_id(0)]
        # do gaussian filter
        datafield.filter_gaussian(sigma)
        # emit signal to container to update UI
        datafield.data_changed()

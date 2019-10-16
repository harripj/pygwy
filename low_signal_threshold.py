# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 21:23:05 2018

@author: pjh523
"""

import gwy
import math
from pygwy_functions import get_data_key, threshold_otsu_power, get_mask_key,\
                            set_mask_colour, get_gaussian_sigma

plugin_menu = "/Grains/Batch/Low Signal Image..."
plugin_type = "PROCESS"
plugin_desc = '''Threshold algorithm for low signal images. Performs a Gaussian blur and then Otsu's power scaled threshold.'''

def run():
    # datafield id to operate on
    _id = 0
    # get sigma from settings, ie. value last used in toolbox->filters
    sigma = get_gaussian_sigma()
    # get all containers
    containers = gwy.gwy_app_data_browser_get_containers()
    # save each container as gwy file with file name
    for c in containers:
        # create checkpoint
        gwy.gwy_app_undo_checkpoint(c, c.keys_by_name())
        # get datafield 0 for each container for func to operate on
        data = c[get_data_key(_id)]
        # create new blurred data
        blurred = data.duplicate()
        # do gaussian filter
        blurred.filter_gaussian(sigma)
        # add to container
        gwy.gwy_app_data_browser_add_data_field(blurred, c, False)
        # create grain mask
        grains = threshold_otsu_power(blurred)
        # add grain field to container and set mask colour
        c.set_object_by_name(get_mask_key(_id), grains)
        set_mask_colour(c, _id)

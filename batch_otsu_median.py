"""
Created on Tue Nov  6 16:55:05 2018

@author: pjh523
"""

import gwy
from functions.pygwy_functions import threshold_otsu_median, set_mask_colour, create_mask

plugin_menu = "/Grains/Batch/Otsu's (Median)"
plugin_type = "PROCESS"
plugin_desc = """Equivalent to 'Otsu Modal Method -> Single, but works on all
                open containers."""


def run():
    # do thresholding on main (id=0) data
    _id = 0
    # get containers
    containers = gwy.gwy_app_data_browser_get_containers()
    # get current image data
    for container in containers:
        # get datafield and compute threshold
        datafield = container.get_object(gwy.gwy_app_get_data_key_for_id(_id))
        threshold = threshold_otsu_median(datafield)
        # create grain mask
        grains = create_mask(datafield, threshold)
        # add mask field to container
        container.set_object(gwy.gwy_app_get_mask_key_for_id(_id), grains)

        # set mask colour and opacity
        set_mask_colour(container, _id)

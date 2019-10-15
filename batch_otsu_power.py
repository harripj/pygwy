"""
Created on Tue Nov  6 16:55:05 2018

@author: pjh523
"""

import gwy
from pygwy_functions import threshold_otsu_power, set_mask_colour, \
                            get_data_key, get_mask_key, create_mask

plugin_menu = "/Grains/Batch/Otsu's (Power)"
plugin_type = "PROCESS"
plugin_desc = '''Batch process datafields using Otsu's method on power scaled data.'''

def run():
    # do thresholding on main (id=0) data
    _id = 0
    # get containers
    containers = gwy.gwy_app_data_browser_get_containers()
    # get current image data
    for container in containers:
        # get datafield and compute threshold
        datafield = container.get_object_by_name(get_data_key(_id))
        # create grain mask
        grains = threshold_otsu_power(datafield)
        # add mask field to container
        container.set_object_by_name(get_mask_key(_id), grains)
        
        # set mask colour and opacity
        set_mask_colour(container, _id)
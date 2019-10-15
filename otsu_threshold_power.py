"""
Created on Tue Nov  6 16:51:38 2018

@author: pjh523
"""

import gwy
import os
from pygwy_functions import threshold_otsu_power, set_mask_colour, \
                            get_mask_key, get_data_key

plugin_menu = '/Grains/Mark by Otsu\'s (Power)'
plugin_type = "PROCESS"
plugin_desc = '''Computes Otsu's threshold on power scaled data.'''

def run():
    # get current image data
    _id = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)
    container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)

    mask_key = get_mask_key(_id)
    # power raised to 1./10 by default, get grain field
    grains = threshold_otsu_power(container[get_data_key(_id)])
    # set grain field mask in container
    container.set_object_by_name(mask_key, grains)
    # set mask colour in container
    set_mask_colour(container, _id)

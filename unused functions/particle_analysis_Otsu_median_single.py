"""
Created on Tue Nov  6 16:51:38 2018

@author: pjh523
"""

import gwy
from pygwy_functions import threshold_otsu_median, set_mask_colour, \
                            create_mask, get_mask_key, get_data_key

plugin_menu = "/Grains/Analyse Particles/Otsu's Method (Median)/Single"
plugin_type = "PROCESS"
plugin_desc = '''Analyse particles on image using histogram modal classifier.
                Works well for skewed height/intensity distribution.
                Finds grains and saves data to JSON of same file name.'''

def run():
    # get current image data
    _id = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)
    container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)

    # analyse_particles_otsu_median(container, datafield_id=datafield_id)
    
    # get datafield and compute threshold
    datafield = container.get_object_by_name(get_data_key(_id))
    threshold = threshold_otsu_median(datafield)
    # create grain mask
    grains = create_mask(datafield, threshold)
    # add mask field to container
    container.set_object_by_name(get_mask_key(_id), grains)
    
    # set mask colour and opacity
    set_mask_colour(container, _id)

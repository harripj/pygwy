"""
Created on Tue Nov 13 21:23:05 2018

@author: pjh523
"""

import gwy
import os
from pygwy_functions import (
    threshold_otsu_median,
    get_relative_value,
    create_mask,
    set_mask_colour,
)

plugin_menu = "/Grains/Mark by Otsu's (Median)"
plugin_type = "PROCESS"
plugin_desc = """Mark grains in datafield by Otsu's method with a median descriptor."""


def run():
    # get current data and correct container for file
    _id = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)
    container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)

    # create undo point
    gwy.gwy_undo_qcheckpoint(container, container.keys())

    # get datafield and compute threshold
    datafield = container.get_object_by_name(gwy.gwy_app_get_data_key_for_id(_id))
    threshold = threshold_otsu_median(datafield)
    # create grain mask
    grains = create_mask(datafield, threshold)
    # add mask field to container
    container.set_object_by_name(gwy.gwy_app_get_mask_key_for_id(_id), grains)

    # set mask colour and opacity
    set_mask_colour(container, _id)

# CREATED BY PJH 2017
# works well on HAADF STEM images, not tested on SPM

import gwy
import os
# from pygwy_functions import median_level

plugin_menu = "/Grains/Analyse Particles/Median Level Batch..."
plugin_type = "PROCESS"
plugin_desc = '''Perform batch median level of open images, df index = 0.
                Median kernel = 60 by deafult.'''

def median_level(datafield, container, kernel_size=60, show=False):
    '''
    Compute a median level of the data. Original data is changed, a copy of the original data is added to the container.
    
    Parameters
    ----------
    datafield: gwy.DataField
        Data to level.
    container: gwy.Container
        Container to add new levelled data to.
    kernel_size: int
        Median filter kernel size in pixels. Default is 20.
    show: bool
        Show the newly added data in the container after computation.
        Defualt is False.
        
    '''
    # # add original data to container
    # original_id = gwy.gwy_app_data_browser_add_data_field( \
    #         datafield.duplicate(), container, False)
    # # don't show background
    # gwy.gwy_app_set_data_field_title(container, original_id, 'Original Data')
    
    # compute levelled background
    background = datafield.duplicate()
    background.filter_median(kernel_size)

    bg_id = gwy.gwy_app_data_browser_add_data_field(background, container, show)
    gwy.gwy_app_set_data_field_title(container, bg_id, 'Background')
    
    # subtract background from data
    datafield.subtract_fields(datafield, background)
    # show on screen
    datafield.data_changed()

def run():
    # get containers
    containers = gwy.gwy_app_data_browser_get_containers()
    # get current image data
    for container in containers:
        gwy.gwy_app_undo_qcheckpoint(container, container.keys())
        # get dictionary of all datafields
        # datafield_ids = gwy.gwy_app_data_browser_get_data_ids(container)
        
        # for _id in datafield_ids:
        # median_level_batch(container, datafield_id=0)
        # get stored data key, usually index 0
        datafield_id = 0
        data_key = os.path.join(os.sep, str(datafield_id), 'data')
        # get datafield
        datafield = container[data_key]

        median_level(datafield, container, kernel_size=60)
        # # copy datafield
        # datafield_median = datafield.duplicate()
        # datafield_median.filter_median(60)

        # # add background to container, under datafield id tree
        # container.set_object_by_name(os.path.join(data_key, 'background'), datafield_median)

        # # do bg subtraction
        # datafield.subtract(datafield, datafield_median)
        # datafield.data_changed()

        # # show in app (window not raised -> False)
        # gwy.gwy_app_data_browser_add_data_field(datafield_median, container, False)
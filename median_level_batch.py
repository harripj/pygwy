# CREATED BY PJH 2017
# works well on HAADF STEM images, not tested on SPM

import gwy
import os

plugin_menu = "/Level/Median Level Batch..."
plugin_type = "PROCESS"
plugin_desc = '''Perform batch median level of open images, df index = 0.
                Median kernel = 30 by deafult.'''

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
        # copy datafield
        datafield_median = datafield.duplicate()
        datafield_median.filter_median(30)

        # add background to container, under datafield id tree
        container.set_object_by_name(os.path.join(data_key, 'background'), datafield_median)

        # do bg subtraction
        datafield.subtract(datafield, datafield_median)
        datafield.data_changed()

        # show in app (window not raised -> False)
        gwy.gwy_app_data_browser_add_data_field(datafield_median, container, False)
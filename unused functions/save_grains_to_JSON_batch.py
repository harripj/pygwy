#CREATED BY PJH 2017
#works well on HAADF STEM images, not tested on SPM

import gwy
from pygwy_functions import save_gwy_grain_mask_to_JSON

plugin_menu = "/Grains/Analyse Particles/Save Grains to JSON/Batch"
plugin_type = "PROCESS"
plugin_desc = '''Calculate parameters of all open grain fields and save to JSON files.'''

def run():
    # get containers
    containers = gwy.gwy_app_data_browser_get_containers()
    # get current image data
    for container in containers:
        # get dictionary of all datafields
        #datafield_ids = gwy.gwy_app_data_browser_get_data_ids(container)
        
        #for _id in datafield_ids:
        save_gwy_grain_mask_to_JSON(container, datafield_id=0)
        
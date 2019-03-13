#CREATED BY PJH 2017
#works well on HAADF STEM images, not tested on SPM

import gwy
from pygwy_functions import save_all_open_to_PNG

plugin_menu = "/Basic Operations/Export All Open To PNG..."
plugin_type = "PROCESS"
plugin_desc = '''Exports all data in open containers to PNG in nested folder.'''

def run():
    #get containers
    containers = gwy.gwy_app_data_browser_get_containers()
    
    save_all_open_to_PNG(containers)
    

# CREATED BY PJH 2017
# works well on HAADF STEM images, not tested on SPM

import gwy
from pygwy_functions import analyse_particles_otsu

plugin_menu = "/Grains/Analyse Particles/Otsu's Method/Batch"
plugin_type = "PROCESS"
plugin_desc = '''Equivalent to 'Analyse Particles -> Single, but works on all
                open containers.'''

def run():
    # get containers
    containers = gwy.gwy_app_data_browser_get_containers()
    # get current image data
    for container in containers:
        # get dictionary of all datafields
        #datafield_ids = gwy.gwy_app_data_browser_get_data_ids(container)
        
        analyse_particles_otsu(container)#, datafield_id=0)
